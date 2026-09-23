# Chapter 03 — Acceptance scenarios

| ID | Given | When | Then |
|---|---|---|---|
| A01 | One seller, two product variants | Create two offers | Catalog identity and variant identity stay distinct |
| A02 | Same variant, two sellers | Set prices 10m and 9.8m | Each offer has its own price and inventory |
| A03 | Seller A order | Insert item tied to Seller B offer | Composite foreign key rejects cross-seller mismatch |
| A04 | Offer price 10m, order price snapshot 10m | Change offer price to 11m | Existing order item snapshot remains 10m |
| A05 | on-hand 1, reserved 0 | Two concurrent conditional reservation updates | Exactly one succeeds; other sees zero rows |
| A06 | Reservation ACTIVE, reserved 1 | Two workers try to release same reservation | Only one conditional transition changes stock |
| A07 | Same customer and idempotency key | Two order-group inserts | UNIQUE prevents duplicate checkout group |
| A08 | Order group has two sellers | Cancel Seller A portion | Seller B portion remains unaffected subject to group policy |
| A09 | Payment attempt failed | Customer retries | New attempt possible; original attempt remains for audit |
| A10 | Order cancelled | Directly mark it paid | Domain state machine rejects unless explicit recovery policy |

Run A05 using separate DB connections with transactions; a single-threaded sequential test does not establish concurrency safety. A06 must check transition and stock adjustment commit together, not only the final status.
