# Pricing & Product lab — Chapter 04

**Requirement:** Local PostgreSQL and `psql`; use a DISPOSABLE database. `schema.sql` drops `ecommerce_pricing_lab` schema before recreating it.

```bash
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f schema.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f queries.sql
```

Expected key results:
- Offer 701: `active_price=21000000`, `price_version=2`.
- Offer 702: `active_price=19700000`, `price_version=1`.
- Order 9001: `unit_price_snapshot=20000000`, `price_version=1`.
- First voucher reserve: one updated row; second: zero rows.
- Reservation release: `reserved_uses=0`, redemption status `RELEASED`.

**Warning:** This is an educational schema for VND only; it omits buyer auth tables, payment ledger, FX, tax and production migration practices. Promotion update and redemption write should form one transaction; reserve must only create redemption when its atomic update succeeds. Server must verify buyer identity and idempotency key ownership. This sample does not contain a job that releases expired reservations automatically.

**Test limitation:** SQL is statically reviewed; if PostgreSQL is unavailable in the current environment, no database integration-test claim is made.
