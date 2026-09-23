# Inside E-commerce — Chapter 05 SQL Lab

**Purpose:** Observe real Order/Reservation transition semantics using PostgreSQL 15+; payment provider actions are intentionally simulated **only as recorded states**. Never interpret this lab as a complete production payment integration.

**Warning:** `schema.sql` drops the `ecommerce_ch05` schema with CASCADE. Use a disposable lab database only.

```bash
createdb ecommerce_ch05_lab
psql -v ON_ERROR_STOP=1 -d ecommerce_ch05_lab -f schema.sql
psql -v ON_ERROR_STOP=1 -d ecommerce_ch05_lab -f seed.sql
psql -v ON_ERROR_STOP=1 -d ecommerce_ch05_lab -f queries.sql
```

Run `test-scenarios.md` in two terminal sessions to observe lock waiting and CAS. `create_demo_order` assumes a trusted server already produced the authoritative price; no user-supplied pricing verification is implemented in SQL lab. `request_demo_cancel` refuses to finalize cancellation when payment may still be in flight/succeeded; **payment reconciliation and refund are separate workflows for later volumes**.

Main learning artifacts:

- `schema.sql`: relationships, UNIQUE/CHECK, reservation and outbox tables, example PL/pgSQL functions.
- `seed.sql`: two customers, two SKUs.
- `queries.sql`: manual walk-through of order/replay/cancel/replay/dedupe.
- `test-scenarios.md`: concurrent sessions and failure-injection checklist.

**Not a drop-in production module:** Has no gateway cryptographic verification, order amount signature, authz, price engine, payout ledger, rich order line state, payment reconcile worker, refund endpoint, or automatic expiry service. Error behavior under simultaneous *same-key* requests needs a production replay handler.
