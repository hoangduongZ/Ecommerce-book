---
name: inside-ecommerce-ui-consistency
description: >-
  Standardize the interface of the Inside E-commerce technical book across
  all volumes and chapters. Use when creating, editing, or reviewing chapter
  HTML, volume landing pages, navigation, sidebars, code blocks, tables,
  diagrams, or book-wide CSS/JS. Reuse the established Volume 1 design
  system and shared reader.css/reader.js; preserve technical content while
  enforcing consistent typography, spacing, layout, components, responsive
  behavior, and chapter navigation. Validate links and assets before delivery.
---

# Skill: Inside E-commerce UI Consistency

## Purpose

Giữ toàn bộ giao diện của bộ sách **Inside E-commerce** đồng nhất từ Volume 1 đến Volume 8.

Skill này được dùng mỗi khi tạo mới hoặc chỉnh sửa:

- Chapter HTML
- Volume index / landing page
- Diagram container
- Code block
- Table
- Callout / note / warning
- Chapter navigation
- Sidebar / table of contents
- PDF-oriented HTML
- Các page phụ trợ của bộ sách

Mục tiêu quan trọng nhất:

> Mọi chapter phải trông như cùng thuộc một bộ sách duy nhất.

Không được tạo một phong cách riêng cho từng chapter.

---

# 1. Source of Truth

Design system hiện tại của Volume 1 là chuẩn giao diện gốc. Nó không nằm ở một thư
mục `shared/` dùng chung nhiều Volume — hiện tại **mỗi Volume tự mang theo asset của
chính nó**:

```text
book/
└── volume-01/
    ├── index.html
    ├── DESIGN-SYSTEM.md
    ├── chapter-01-*.html / .md
    ├── chapter-02-*.html / .md
    ├── ...
    └── assets/
        ├── reader.css
        ├── reader.js
        └── diagram-*.svg, chapter-0N/diagram-*.svg
```

Nếu Volume hiện tại đã có:

```text
assets/reader.css
assets/reader.js
```

thì **phải reuse**, không viết lại từ đầu.

Không được tạo:

```text
chapter-06.css
chapter-07-style.css
custom-theme-chapter-08.css
```

trừ khi user yêu cầu rõ ràng.

Mọi thay đổi design system phải được thực hiện ở `assets/reader.css` /
`assets/reader.js` dùng chung cho cả Volume, không patch riêng từng chapter.

Khi tạo Volume 2 trở đi: bắt đầu bằng cách **copy** `book/volume-01/assets/reader.css`
và `assets/reader.js` làm điểm xuất phát (đổi `--accent` nếu cần, xem
[reference.md §3](reference.md#3-color-system)), rồi mới chỉnh tiếp. Chỉ tạo một thư
mục `shared/` thật sự khi user yêu cầu hợp nhất nhiều Volume — đừng giả định nó đã
tồn tại.

---

# 2. Core Principle

## Content changes per chapter.

## Interface does not.

Các chapter được phép khác nhau ở:

- title
- subtitle
- nội dung
- diagrams
- code
- exercises
- chapter accent metadata nếu design system hỗ trợ

Các chapter KHÔNG được tự ý khác nhau ở:

- font
- page width
- sidebar width
- màu nền
- heading hierarchy
- code style
- table style
- diagram frame
- navigation layout
- spacing system
- border radius
- shadow system

---

# 3. Required Page Skeleton

Đây là skeleton **thật** đang được `assets/reader.css` style, lấy nguyên trạng từ
`chapter-01-ecommerce-ecosystem.html`. Mọi chapter HTML mới phải tái sử dụng đúng
class name này — không đổi tên, không bọc thêm layer:

```html
<link rel="stylesheet" href="assets/reader.css">
...
<body>
  <div class="reader-shell">

    <aside class="sidebar">
      <a class="brand-link" href="index.html">
        <span class="kicker">...</span><strong>INSIDE E-COMMERCE</strong><small>Volume ...</small>
      </a>
      <div class="volume-progress">...</div>
      <div class="nav-label">Chapters</div>
      <div class="chapter-list">
        <a class="chapter-link active" href="...">...</a>
        <!-- chapter-link cho từng chapter, .active trên chapter hiện tại -->
      </div>
      <div class="nav-label">In this chapter</div>
      <nav class="toc">
        <a class="toc-h2" href="#...">...</a>
        <a class="toc-h3" href="#...">...</a>
      </nav>
    </aside>

    <section class="content-wrap">
      <header class="topbar">
        <button class="menu-btn" aria-label="Mở mục lục">☰</button>
        <div class="crumb">Volume N / Chapter NN</div>
        <a href="index.html">Volume home</a>
      </header>

      <article>
        <!-- hero: div.eyebrow + h1 (book title) + h2 (volume) + h3 (chapter title)
             + blockquote (leading question) — chi tiết ở reference.md §4 -->
        <!-- nội dung chapter: h2/h3/h4, p, blockquote, table, pre/code, figure.diagram -->
      </article>

      <div class="chapter-nav">
        <a href="chapter-prev.html"><small>← Chương trước</small>Tên chapter trước</a>
        <!-- hoặc <span class="empty"></span> nếu là chapter đầu tiên -->
        <a href="chapter-next.html"><small>Chương tiếp theo →</small>Tên chapter sau</a>
      </div>
    </section>

  </div>
  <script src="assets/reader.js"></script>
</body>
```

Lưu ý:

- Không có class `book-shell` / `book-sidebar` / `book-main` / `chapter-hero` /
  `chapter-content` / `chapter-pagination` — đó là tên **không tồn tại** trong
  `reader.css`. Class thật là `reader-shell`, `sidebar`, `content-wrap`, `chapter-nav`.
- `article` không cần class riêng — style áp trực tiếp lên thẻ `<article>`.
- `index.html` (Volume landing page) **không** dùng skeleton này — nó là một trang
  độc lập với style riêng. Xem [reference.md §6](reference.md).

Không tạo một cấu trúc trang mới nếu cấu trúc trên giải quyết được yêu cầu.

---

# 4. Detailed Rules (Reference)

Các quy tắc chi tiết — typography, spacing, color, chapter hero, sidebar, volume index,
content component library, chapter learning pattern, diagrams, responsive, navigation,
CSS/JS architecture, accessibility, content preservation, file naming, validation
checklist, delivery contract — nằm trong [reference.md](reference.md).

Đọc `reference.md` trước khi tạo hoặc chỉnh sửa bất kỳ chapter/volume nào.

---

# 5. Anti-patterns

KHÔNG:

- tạo CSS riêng cho mỗi chapter
- đổi font giữa chapter
- đổi toàn bộ palette tùy chapter
- tạo landing page bằng list link đơn giản
- để diagram có style khác nhau
- inline style hàng trăm dòng
- duplicate sidebar markup không cần thiết
- hardcode navigation mà không kiểm tra
- rebuild nội dung chỉ để đổi giao diện
- thêm animation gây phân tâm
- ưu tiên đẹp hơn khả năng đọc

---

# 6. Definition of Done

Một chapter chỉ được coi là hoàn tất khi:

```text
CONTENT
  ✓ đầy đủ kiến thức

STRUCTURE
  ✓ đúng chapter template

UI
  ✓ dùng shared design system

NAVIGATION
  ✓ previous/index/next hoạt động

DIAGRAMS
  ✓ render đúng

RESPONSIVE
  ✓ desktop/mobile usable

CONSISTENCY
  ✓ nhìn vào biết ngay thuộc bộ Inside E-commerce
```

Nếu chapter mới trông như một website khác so với chapter trước:

> Chapter chưa hoàn tất.

---

# 7. Instruction for AI Agent

Khi được yêu cầu tạo chapter tiếp theo của **Inside E-commerce**, luôn thực hiện theo thứ tự:

```text
1. Inspect existing Volume design system.
2. Reuse shared HTML shell.
3. Reuse reader.css and reader.js.
4. Write chapter content.
5. Generate diagrams.
6. Insert content into the existing shell.
7. Update sidebar / TOC / navigation.
8. Update Volume index.
9. Validate local links and assets.
10. Package artifacts.
```

Không được bắt đầu bằng việc tự thiết kế một giao diện mới.

Nếu style hiện có và prompt mới mâu thuẫn:

> Ưu tiên design system hiện có, trừ khi user yêu cầu redesign toàn bộ.

Trước khi bàn giao, chạy qua checklist "Required Validation Before Delivery" và
"Delivery Contract" trong [reference.md](reference.md).

---

# 8. One-line Rule

> **New chapter = new knowledge, not a new visual identity.**
