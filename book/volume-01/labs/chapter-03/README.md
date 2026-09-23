# Chapter 03 — PostgreSQL lab

## Contents

- `schema.sql` — a coherent teaching schema for single-warehouse reservation per order item.
- `queries.sql` — parameterized SQL examples for atomic reservation, conditional release and historical snapshot reads.
- `test-scenarios.md` — manual acceptance and concurrency cases.

## Run

```bash
createdb hoang_marketplace_lab
psql -v ON_ERROR_STOP=1 -d hoang_marketplace_lab -f schema.sql
```

Use an empty disposable database; `schema.sql` intentionally creates tables and has no DROP statements. `queries.sql` uses `:named_parameters` for a Java prepared-query context and isn't runnable in psql without substitution.

## Intentional simplifications

- One seller order per seller per checkout (`UNIQUE (order_group_id, seller_id)`).
- One stock reservation per order item, drawn from one warehouse. Multi-warehouse split allocations require a different design.
- `products` are canonical catalog entries; unique second-hand listings may not need this model.
- `payment_attempts` are *attempts*, not a settlement ledger, refund ledger or financial accounting system.
- Amount calculations, promotion allocation, tax and currency exchange remain outside this chapter.
- `seller_id` and warehouse ownership are strict by design here. Shared fulfillment facilities require a different policy and schema.
- Schema CHECKs cannot by themselves enforce cross-row stock sums or payment-provider truth.

## Safety and production questions

- Who controls stock-adjustment permissions? Who can modify on-hand quantity?
- How are reservation expiry workers coordinated under concurrency?
- How is a payment callback validated and made idempotent?
- How is state transition history/audit recorded?
- Are order lines immutable snapshots after placement?
- How is a DB transaction coordinated with message publishing?

See chapter 03 for the business rationale behind each table.
