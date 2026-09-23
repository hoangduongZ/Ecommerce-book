# INSIDE E-COMMERCE — Volume 1 / Chapter 03

**Domain Modeling — Từ nghiệp vụ E-commerce đến thiết kế dữ liệu và cấu trúc Backend**

## Cách đọc

1. Mở `chapter-03-domain-modeling.html` trực tiếp trong trình duyệt. Không cần Internet.
2. Dùng sidebar để chuyển mục; chọn **Xem / sao chép Mermaid** dưới mỗi sơ đồ nếu muốn chỉnh diagram.
3. Markdown gốc: `chapter-03-domain-modeling.md`.
4. Sơ đồ vector: `assets/chapter-03/diagram-01.svg` đến `diagram-14.svg`. SVG là bản diễn họa trực quan từ Mermaid; khi cần kiểm tra ký hiệu ER chi tiết, xem mã Mermaid gốc.
5. SQL lab: `labs/chapter-03/README.md`.

## Nội dung trọng tâm

- Ubiquitous Language, Entity / Value Object, Bounded Context, Aggregate và invariants.
- Product / Variant / Seller Offer / Inventory / Order Snapshot.
- Transaction boundaries, state machines, idempotency, conditional reservation.
- Spring Boot modular monolith, PostgreSQL schema và failure scenarios.

## Trạng thái

Completed editorial draft; mã SQL là ví dụ thiết kế được review cấu trúc và ràng buộc tĩnh, **chưa chạy integration test trên PostgreSQL thực** trong bộ build này. Không dùng nguyên trạng cho production.

Các chapter khác trong volume được giữ trong bản ZIP tích lũy để điều hướng ngoại tuyến không bị gãy.
