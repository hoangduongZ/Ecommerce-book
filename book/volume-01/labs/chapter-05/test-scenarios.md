# Chapter 05 — Test scenarios

## A. Inventory reservation: maximum one winner

`seed.sql`: SKU 1001 has `on_hand=1`, `reserved=0`.

- Session A executes `SELECT ecommerce_ch05.create_demo_order(101,'a','payload-a',1001,1,10000000);`
- Session B executes `SELECT ecommerce_ch05.create_demo_order(102,'b','payload-b',1001,1,10000000);`
- At most one returns an order; loser raises `Out of stock`. Check active reservations = 1 and inventory reserved = 1.
- For a deterministic overlap experiment, execute checkout SQL as explicit transactions in two shells, hold Session A before COMMIT; DB lock must block the conflicting stock write.

## B. Duplicate checkout

Repeat `create_demo_order(101,'a','payload-a',...)`: same order ID. Repeat key `a` with another fingerprint: rejected. For truly simultaneous *same-key* requests on different connections, UNIQUE ensures at most one committed order, but the losing request may receive a unique-violation rather than a convenient replay response. Production layer should resolve conflict by reading committed existing key/response and checking its fingerprint.

## C. Release once

Call `request_demo_cancel(order_id)` twice while no payment is in flight. First returns `CANCELLED`; second returns `ALREADY_CANCELLED`. `inventory.reserved` must decrement only once.

## D. Payment unknown

Insert payment attempt in `UNKNOWN` for an ACTIVE order. Request cancellation: expected `CANCELLING`, *not* released. Resolve with verified PSP status, then design separate handler for chosen compensation policy; demo function deliberately does not fake PSP resolution.

## E. Webhook/outbox deduplication

Same `(provider,event_id)` inserted twice with `ON CONFLICT DO NOTHING`: one row. Same `(consumer_name,event_id)` inserted twice: one row. This merely deduplicates a *marker*. Production must include business side effect + marker in the same local transaction.

## F. Status race

Use the following in two psql sessions with the same order ID, after creating a fresh PENDING_PAYMENT order:

Session A: `BEGIN; SELECT id,status,version FROM ecommerce_ch05.orders WHERE id=... FOR UPDATE;` then pause.

Session B: `UPDATE ecommerce_ch05.orders SET status='CONFIRMED',version=version+1 WHERE id=... AND status='PENDING_PAYMENT' AND version=0;` -- waits.

Session A: `UPDATE ecommerce_ch05.orders SET status='CANCELLING', version=version+1 WHERE id=... AND status='PENDING_PAYMENT'; COMMIT;`

Session B resumes; its affected-row count = 0. Handler must reload state. Do not blindly turn CANCELLING into CONFIRMED.

## G. Recovery

Observe `outbox_events WHERE published_at IS NULL`. Publishing after a committed order is replayable. A relay may publish then crash before marking published; downstream handler must be idempotent.

## H. Independent refund lifecycle

Design `refunds(refund_id, order_id, provider_refund_id, amount, status)` and partial return lines. Test `SUM(successful_refund_amount) <= captured_amount`; note that pending refunds must also be considered during authorization of a new refund to avoid double initiation.
