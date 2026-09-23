-- Chapter 03 — illustrative PostgreSQL commands. Substitute :named_parameters
-- using application prepared statements; do not paste SQL :params into bare psql.

-- 1) Atomic reservation inside an appropriate transaction:
UPDATE inventory_stock
SET reserved_quantity = reserved_quantity + :quantity
WHERE offer_id = :offer_id
  AND warehouse_id = :warehouse_id
  AND on_hand_quantity - reserved_quantity >= :quantity
RETURNING offer_id, warehouse_id, on_hand_quantity, reserved_quantity;
-- Zero rows = reservation not granted. Do not create a successful order.

-- 2) Idempotent release: the status transition and stock adjustment must
-- happen in the SAME DB transaction. Only release ACTIVE reservations.
-- BEGIN;
WITH released AS (
  UPDATE stock_reservations
  SET status = 'RELEASED'
  WHERE reservation_id = :reservation_id
    AND status = 'ACTIVE'
  RETURNING offer_id, warehouse_id, quantity
)
UPDATE inventory_stock AS s
SET reserved_quantity = s.reserved_quantity - r.quantity
FROM released AS r
WHERE s.offer_id = r.offer_id AND s.warehouse_id = r.warehouse_id
RETURNING s.offer_id, s.warehouse_id, s.reserved_quantity;
-- COMMIT; 
-- If released reservation has no matching stock row, abort and diagnose:
-- the FK should ordinarily keep that from happening unless constraints are
-- bypassed or mutations in the same transaction are malformed.

-- 3) Historical order items: never derive their prices from current offers.
SELECT i.order_item_id, i.title_snapshot, i.sku_code_snapshot,
       i.quantity, i.unit_price_snapshot, i.currency,
       i.quantity * i.unit_price_snapshot AS line_subtotal
FROM order_items AS i
WHERE i.seller_order_id = :seller_order_id;

-- 4) Read current stock availability by offer/warehouse:
SELECT offer_id, warehouse_id,
       on_hand_quantity - reserved_quantity AS available_quantity
FROM inventory_stock
WHERE offer_id = :offer_id;

-- 5) Consume confirmed reservation: illustrative transaction. Inventory moves
-- out of on-hand stock when business considers goods dispatched/consumed.
-- This flow applies only if ACTIVE -> CONFIRMED is the chosen lifecycle rule.
-- BEGIN;
WITH confirmed AS (
  UPDATE stock_reservations
  SET status = 'CONFIRMED'
  WHERE reservation_id = :reservation_id AND status = 'ACTIVE'
  RETURNING offer_id, warehouse_id, quantity
)
UPDATE inventory_stock AS s
SET on_hand_quantity = s.on_hand_quantity - c.quantity,
    reserved_quantity = s.reserved_quantity - c.quantity
FROM confirmed AS c
WHERE s.offer_id = c.offer_id AND s.warehouse_id = c.warehouse_id
RETURNING s.offer_id, s.on_hand_quantity, s.reserved_quantity;
-- COMMIT;
-- Handle a late payment success versus released reservation using an
-- explicit recovery policy, not by moving CONFIRMED/RELEASED freely.
