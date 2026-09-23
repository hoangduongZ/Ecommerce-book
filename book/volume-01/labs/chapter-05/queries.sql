-- INSIDE E-COMMERCE · Ch05 lab · intended for psql
-- After schema.sql + seed.sql, run lines individually or whole script in psql.
SET search_path TO ecommerce_ch05, public;

-- 1) Create 1 order and reserve the only Phone X.
SELECT create_demo_order(101,'checkout-101-a','sha256:same-payload',1001,1,10000000.00) AS order_a;
SELECT sku_id,on_hand,reserved,on_hand-reserved AS available FROM inventory WHERE sku_id=1001;

-- 2) Repeated identical checkout returns the original order ID; no second reserve.
SELECT create_demo_order(101,'checkout-101-a','sha256:same-payload',1001,1,10000000.00) AS same_order_a;

-- 3) Out-of-stock attempt: uncomment to observe exception (intentionally fails script if enabled).
-- SELECT create_demo_order(102,'checkout-102-a','sha256:other',1001,1,10000000.00);

-- 4) Cancellation twice must only release stock once.
SELECT request_demo_cancel(1) AS cancellation_one;
SELECT request_demo_cancel(1) AS cancellation_two;
SELECT sku_id,on_hand,reserved,on_hand-reserved AS available FROM inventory WHERE sku_id=1001;

-- 5) Duplicate webhook event should conflict, so second operation must be handled as a no-op.
INSERT INTO payment_webhook_events(provider,event_id) VALUES ('psp_demo','evt-abc')
ON CONFLICT (provider,event_id) DO NOTHING;
INSERT INTO payment_webhook_events(provider,event_id) VALUES ('psp_demo','evt-abc')
ON CONFLICT (provider,event_id) DO NOTHING;
SELECT provider,event_id,count(*) FROM payment_webhook_events GROUP BY provider,event_id;

-- 6) Duplicate consumption of an outbox event should be a no-op.
INSERT INTO processed_messages(consumer_name,event_id)
SELECT 'fulfillment',id FROM outbox_events WHERE event_type='OrderPlaced' LIMIT 1
ON CONFLICT DO NOTHING;
INSERT INTO processed_messages(consumer_name,event_id)
SELECT 'fulfillment',id FROM outbox_events WHERE event_type='OrderPlaced' LIMIT 1
ON CONFLICT DO NOTHING;
SELECT consumer_name,event_id,count(*) FROM processed_messages GROUP BY consumer_name,event_id;

-- 7) Inspect state transitions and outstanding events.
SELECT o.id,o.status,o.version,r.status AS reservation_status
FROM orders o JOIN stock_reservations r ON r.order_id=o.id ORDER BY o.id;
SELECT id,order_id,old_status,new_status,event_name FROM order_transitions ORDER BY id;
SELECT id,event_type,published_at FROM outbox_events ORDER BY id;
