-- INSIDE E-COMMERCE · Chapter 05 · PostgreSQL 15+ lab
-- Run ONLY in a disposable lab database; DROP SCHEMA CASCADE destroys prior lab data.
DROP SCHEMA IF EXISTS ecommerce_ch05 CASCADE;
CREATE SCHEMA ecommerce_ch05;
SET search_path TO ecommerce_ch05, public;

CREATE TABLE customers (
  id BIGINT PRIMARY KEY,
  name TEXT NOT NULL
);
CREATE TABLE inventory (
  sku_id BIGINT PRIMARY KEY,
  on_hand INTEGER NOT NULL CHECK (on_hand >= 0),
  reserved INTEGER NOT NULL DEFAULT 0 CHECK (reserved >= 0),
  CHECK (reserved <= on_hand)
);
CREATE TABLE orders (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES customers(id),
  idempotency_key TEXT NOT NULL,
  request_fingerprint TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'PENDING_PAYMENT'
    CHECK (status IN ('PENDING_PAYMENT','CANCELLING','CANCELLED','CONFIRMED','PROCESSING','SHIPPED','DELIVERED','COMPLETED')),
  version INTEGER NOT NULL DEFAULT 0,
  currency CHAR(3) NOT NULL DEFAULT 'VND',
  total_amount NUMERIC(18,2) NOT NULL CHECK(total_amount >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(user_id, idempotency_key)
);
CREATE TABLE order_items (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id BIGINT NOT NULL REFERENCES orders(id),
  sku_id BIGINT NOT NULL REFERENCES inventory(sku_id),
  product_name_snapshot TEXT NOT NULL,
  qty INTEGER NOT NULL CHECK(qty > 0),
  unit_price NUMERIC(18,2) NOT NULL CHECK(unit_price >= 0),
  CHECK (unit_price * qty >= 0)
);
CREATE TABLE stock_reservations (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id BIGINT NOT NULL REFERENCES orders(id),
  sku_id BIGINT NOT NULL REFERENCES inventory(sku_id),
  qty INTEGER NOT NULL CHECK(qty > 0),
  status TEXT NOT NULL DEFAULT 'ACTIVE'
    CHECK (status IN ('ACTIVE','RELEASED','CONSUMED')),
  expires_at TIMESTAMPTZ NOT NULL,
  UNIQUE(order_id, sku_id)
);
CREATE TABLE payment_attempts (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id BIGINT NOT NULL REFERENCES orders(id),
  provider TEXT NOT NULL,
  provider_payment_id TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('PENDING','PROCESSING','UNKNOWN','SUCCEEDED','FAILED','CANCELLED')),
  amount NUMERIC(18,2) NOT NULL CHECK(amount >= 0),
  currency CHAR(3) NOT NULL,
  UNIQUE(provider, provider_payment_id)
);
CREATE TABLE payment_webhook_events (
  provider TEXT NOT NULL,
  event_id TEXT NOT NULL,
  received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY(provider,event_id)
);
CREATE TABLE order_transitions (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id BIGINT NOT NULL REFERENCES orders(id),
  old_status TEXT,
  new_status TEXT NOT NULL,
  event_name TEXT NOT NULL,
  actor TEXT NOT NULL,
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE outbox_events (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id BIGINT NOT NULL REFERENCES orders(id),
  event_type TEXT NOT NULL,
  event_payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  published_at TIMESTAMPTZ
);
CREATE TABLE processed_messages (
  consumer_name TEXT NOT NULL,
  event_id BIGINT NOT NULL REFERENCES outbox_events(id),
  processed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY(consumer_name,event_id)
);
CREATE INDEX ix_orders_user_recent ON orders(user_id,created_at DESC);
CREATE INDEX ix_reservation_expiry ON stock_reservations(expires_at) WHERE status='ACTIVE';
CREATE INDEX ix_outbox_pending ON outbox_events(id) WHERE published_at IS NULL;

-- Short DB-only checkout: does NOT call an external payment provider.
-- Caller sends stable idempotency key + a hash of canonical request payload.
CREATE OR REPLACE FUNCTION create_demo_order(
    p_user BIGINT, p_key TEXT, p_fingerprint TEXT,
    p_sku BIGINT, p_qty INTEGER, p_unit_price NUMERIC
) RETURNS BIGINT LANGUAGE plpgsql AS $$
DECLARE v_order BIGINT; v_old_fingerprint TEXT; v_rows INT;
BEGIN
  IF p_qty <= 0 OR p_unit_price < 0 THEN
    RAISE EXCEPTION 'Invalid qty or price';
  END IF;
  -- Fast repeat path; UNIQUE below still protects true concurrent duplicate inserts.
  SELECT id, request_fingerprint INTO v_order, v_old_fingerprint
  FROM orders WHERE user_id=p_user AND idempotency_key=p_key;
  IF FOUND THEN
    IF v_old_fingerprint <> p_fingerprint THEN
      RAISE EXCEPTION 'Idempotency key reused for different payload';
    END IF;
    RETURN v_order;
  END IF;
  INSERT INTO orders(user_id,idempotency_key,request_fingerprint,total_amount)
  VALUES(p_user,p_key,p_fingerprint,p_qty*p_unit_price)
  RETURNING id INTO v_order;
  UPDATE inventory SET reserved=reserved+p_qty
  WHERE sku_id=p_sku AND on_hand-reserved >= p_qty;
  GET DIAGNOSTICS v_rows=ROW_COUNT;
  IF v_rows<>1 THEN RAISE EXCEPTION 'Out of stock'; END IF;
  INSERT INTO order_items(order_id,sku_id,product_name_snapshot,qty,unit_price)
  VALUES(v_order,p_sku,'Phone X / Black / 256 GB',p_qty,p_unit_price);
  INSERT INTO stock_reservations(order_id,sku_id,qty,expires_at)
  VALUES(v_order,p_sku,p_qty,now()+interval '15 minutes');
  INSERT INTO order_transitions(order_id,old_status,new_status,event_name,actor)
  VALUES(v_order,NULL,'PENDING_PAYMENT','OrderPlaced','checkout');
  INSERT INTO outbox_events(order_id,event_type,event_payload)
  VALUES(v_order,'OrderPlaced',jsonb_build_object('orderId',v_order));
  RETURN v_order;
END $$;

-- DB-only cancel: valid only when no possible in-flight/succeeded PSP payment.
-- Otherwise move to CANCELLING, and PSP verification is an external follow-up.
CREATE OR REPLACE FUNCTION request_demo_cancel(p_order BIGINT)
RETURNS TEXT LANGUAGE plpgsql AS $$
DECLARE v_old TEXT; v_res RECORD;
BEGIN
  SELECT status INTO v_old FROM orders WHERE id=p_order FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'Order not found'; END IF;
  IF v_old='CANCELLED' THEN RETURN 'ALREADY_CANCELLED'; END IF;
  IF v_old NOT IN ('PENDING_PAYMENT','CANCELLING') THEN
    RAISE EXCEPTION 'Order not cancellable by this demo flow: %', v_old;
  END IF;
  IF EXISTS(
      SELECT 1 FROM payment_attempts
      WHERE order_id=p_order AND status IN ('PENDING','PROCESSING','UNKNOWN','SUCCEEDED')
  ) THEN
    IF v_old <> 'CANCELLING' THEN
      UPDATE orders SET status='CANCELLING',version=version+1 WHERE id=p_order;
      INSERT INTO order_transitions(order_id,old_status,new_status,event_name,actor)
      VALUES(p_order,v_old,'CANCELLING','CancelRequested','customer');
    END IF;
    RETURN 'AWAITING_PAYMENT_RESOLUTION';
  END IF;
  FOR v_res IN
    SELECT sku_id, qty FROM stock_reservations
    WHERE order_id=p_order AND status='ACTIVE' FOR UPDATE
  LOOP
    UPDATE stock_reservations
    SET status='RELEASED'
    WHERE order_id=p_order AND sku_id=v_res.sku_id AND status='ACTIVE';
    IF FOUND THEN
      UPDATE inventory SET reserved=reserved-v_res.qty
      WHERE sku_id=v_res.sku_id AND reserved>=v_res.qty;
      IF NOT FOUND THEN RAISE EXCEPTION 'Inconsistent inventory'; END IF;
    END IF;
  END LOOP;
  UPDATE orders SET status='CANCELLED',version=version+1 WHERE id=p_order;
  INSERT INTO order_transitions(order_id,old_status,new_status,event_name,actor)
  VALUES(p_order,v_old,'CANCELLED','OrderCancelled','customer');
  INSERT INTO outbox_events(order_id,event_type,event_payload)
  VALUES(p_order,'OrderCancelled',jsonb_build_object('orderId',p_order));
  RETURN 'CANCELLED';
END $$;
