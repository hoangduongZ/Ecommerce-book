# Inside E-commerce — Volume 1 / Chapter 04

**Product & Pricing Engineering — Vì sao giá không chỉ là một cột `price`?**

## Bắt đầu đọc

1. Mở `chapter-04-product-pricing.html` bằng trình duyệt; đây là bản đọc offline, có mục lục, dark mode và 14 sơ đồ SVG.
2. Markdown gốc: `chapter-04-product-pricing.md` (17 mục nội dung).
3. Sơ đồ SVG: `assets/chapter-04/diagram-01.svg` ... `diagram-14.svg`. Mã Mermaid có trong Markdown và có thể mở từ HTML để chỉnh sửa.
4. Bài thực hành PostgreSQL: `labs/chapter-04/README.md`, `schema.sql`, `queries.sql`, `test-scenarios.md`.
5. `index.html` đưa bạn về mục lục Volume 1.

## Nhiệm vụ thực hành

- Thiết kế price quote và order item snapshot.
- Atomic voucher reservation không vượt quota khi mua đồng thời.
- So sánh offer current price với order snapshot sau khi admin đổi giá.
- Revalidation chống giả mạo client total, cache giá cũ, checkout quote hết hạn.

**Tình trạng kiểm thử:** Markdown/HTML, sơ đồ và ZIP được kiểm tra tự động về cấu trúc. SQL là lab giáo dục chưa chạy integration test PostgreSQL nếu môi trường không có server PostgreSQL. Không áp nguyên trạng cho production.
