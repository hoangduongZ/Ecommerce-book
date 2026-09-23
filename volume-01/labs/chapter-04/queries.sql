-- Run AFTER schema.sql, in a disposable DB. Re-running this script without schema reset may conflict with PKs.
\set ON_ERROR_STOP on
SET search_path TO ecommerce_pricing_lab;

INSERT INTO seller(id,display_name) VALUES (1,'Hoàng Phone'),(2,'Seller B');
INSERT INTO product_variant(id,sku,product_name,variant_label)
VALUES (101,'PHONE-X-BLACK-256','Phone X','Black / 256 GB');
INSERT INTO seller_offer(id,seller_id,variant_id,active_price,currency,status)
VALUES (701,1,101,20000000,'VND','ACTIVE'),(702,2,101,19700000,'VND','ACTIVE');
INSERT INTO offer_price_history(offer_id,price_version,amount)
SELECT id,price_version,active_price FROM seller_offer;

-- Commit a legitimate order snapshot at seller A's original price.
BEGIN;
INSERT INTO customer_order(id,buyer_id,currency,payable_total,status,checkout_request_key)
VALUES (9001,101,'VND',20000000,'PENDING_PAYMENT','checkout-101-1');
INSERT INTO order_item_snapshot(order_id,offer_id,product_name_snapshot,
       variant_label_snapshot,unit_price_snapshot,quantity,allocated_discount,
       net_line_amount,currency,price_version)
VALUES (9001,701,'Phone X','Black / 256 GB',20000000,1,0,20000000,'VND',1);
COMMIT;

-- Admin changes seller A price but must not mutate an existing order snapshot.
BEGIN;
UPDATE seller_offer SET active_price=21000000,
    price_version=price_version+1,updated_at=now()
WHERE id=701 AND price_version=1;
INSERT INTO offer_price_history(offer_id,price_version,amount)
SELECT id,price_version,active_price FROM seller_offer WHERE id=701;
COMMIT;

SELECT o.id, o.active_price, o.price_version FROM seller_offer o ORDER BY o.id;
SELECT i.order_id,i.unit_price_snapshot,i.price_version FROM order_item_snapshot i;

-- Quota reservation: only the first request may succeed for a budget of 1.
INSERT INTO promotion_budget(promotion_id,code,usage_limit) VALUES (501,'WELCOME500',1);

BEGIN;
UPDATE promotion_budget SET reserved_uses=reserved_uses+1
WHERE promotion_id=501
  AND reserved_uses+consumed_uses < usage_limit
RETURNING promotion_id,reserved_uses,consumed_uses;
INSERT INTO promotion_redemption(promotion_id,buyer_id,request_key,status)
VALUES (501,101,'redeem-101-1','RESERVED');
COMMIT;

-- This must return ZERO rows; do NOT insert a redemption if the update returned none.
UPDATE promotion_budget SET reserved_uses=reserved_uses+1
WHERE promotion_id=501
  AND reserved_uses+consumed_uses < usage_limit
RETURNING promotion_id;

-- Teach idempotent release with a state transition protected by the transaction.
BEGIN;
WITH released AS (
  UPDATE promotion_redemption SET status='RELEASED'
  WHERE promotion_id=501 AND buyer_id=101 AND request_key='redeem-101-1'
    AND status='RESERVED'
  RETURNING promotion_id
)
UPDATE promotion_budget p SET reserved_uses=p.reserved_uses-1
FROM released r WHERE p.promotion_id=r.promotion_id
RETURNING p.promotion_id,p.reserved_uses;
COMMIT;

SELECT * FROM promotion_budget WHERE promotion_id=501;
SELECT * FROM promotion_redemption WHERE promotion_id=501;
-- Repeat the release block: no row should update and quota must not decrement again.
