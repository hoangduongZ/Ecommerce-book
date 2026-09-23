# Test scenarios — Chapter 04

## Contract tests
1. Seller A/B same SKU, independent `active_price` and version.
2. Order snapshot remains 20M when Seller A offer changes 20M -> 21M.
3. Reject negative prices, negative discounts, zero/negative order item quantity.
4. Reject duplicate `buyer_id + checkout_request_key`.
5. Reject duplicate voucher redemption request by `promotion_id + buyer_id + request_key`.
6. Two sessions reserving a budget of 1: exactly ONE update succeeds (affected rows = 1), the other gets 0 after the first commits.
7. Releasing same reservation twice must decrement budget once only.
8. `clientTotal=1000` must not determine persisted payable amount.
9. Expired/changed quote must reprice or reject according to documented policy.
10. Three-way allocation of 10,000 VND must sum to 10,000 exactly.

## Concurrent transaction drill
- Reset lab (`schema.sql`, then `queries.sql` may pre-use the voucher; for concurrency test create a NEW promotion ID 502).
- Session A: `BEGIN; UPDATE promotion_budget SET reserved_uses=reserved_uses+1 WHERE promotion_id=502 AND reserved_uses+consumed_uses<usage_limit RETURNING *;` do not commit.
- Session B: run the same UPDATE; it should wait on the row lock.
- Session A: `COMMIT;`.
- Session B: should return 0 rows. `ROLLBACK;`.

## Metrics to observe
`quote_latency_p95`, DB pool wait, `pg_stat_activity.wait_event`, invalidations delayed, voucher quota failures, pricing rule CPU, checkout `PRICE_CHANGED`, order idempotent replays.
