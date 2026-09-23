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

Design system hiện tại của Volume 1 là chuẩn giao diện gốc.

Ưu tiên tái sử dụng các asset dùng chung:

```text
shared/
├── reader.css
├── reader.js
├── components/
└── assets/
```

Nếu project hiện tại đã có:

```text
reader.css
reader.js
```

thì **phải reuse**.

Không được tạo:

```text
chapter-06.css
chapter-07-style.css
custom-theme-chapter-08.css
```

trừ khi user yêu cầu rõ ràng.

Mọi thay đổi design system phải được thực hiện ở stylesheet dùng chung.

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

Mọi chapter HTML phải tuân theo skeleton logic sau:

```html
<body>
  <div class="book-shell">

    <aside class="book-sidebar">
      <!-- book title -->
      <!-- volume -->
      <!-- chapter navigation -->
      <!-- in-page TOC -->
    </aside>

    <main class="book-main">

      <header class="chapter-hero">
        <!-- volume label -->
        <!-- chapter number -->
        <!-- chapter title -->
        <!-- subtitle -->
        <!-- optional metadata -->
      </header>

      <article class="chapter-content">
        <!-- chapter content -->
      </article>

      <nav class="chapter-pagination">
        <!-- previous -->
        <!-- volume index -->
        <!-- next -->
      </nav>

    </main>

  </div>
</body>
```

Không tạo một cấu trúc trang mới nếu cấu trúc trên giải quyết được yêu cầu.

---

# 4. Typography Rules

Sử dụng cùng một font stack cho toàn bộ sách.

Không được đổi font riêng từng chapter.

Hierarchy:

```text
Book / Volume label
    ↓
Chapter title (H1)
    ↓
Major section (H2)
    ↓
Sub-section (H3)
    ↓
Detail heading (H4)
    ↓
Body
```

Quy tắc:

- Chỉ có **1 H1** trong mỗi chapter.
- Không dùng heading chỉ để làm chữ to.
- Không nhảy trực tiếp H2 → H4.
- Paragraph phải có line-height dễ đọc.
- Độ rộng phần đọc phải được giới hạn để tránh dòng quá dài.

Ưu tiên readability hơn density.

---

# 5. Spacing System

Không dùng margin/padding tùy hứng.

Sử dụng spacing scale thống nhất, ví dụ:

```text
4px
8px
12px
16px
24px
32px
48px
64px
```

Ví dụ:

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 24px;
--space-6: 32px;
--space-7: 48px;
--space-8: 64px;
```

Không tạo các giá trị ngẫu nhiên như:

```css
margin-top: 37px;
padding: 19px;
gap: 27px;
```

nếu không có lý do đặc biệt.

---

# 6. Color System

Không chọn màu riêng cho từng component.

Dùng semantic tokens:

```css
--bg-page
--bg-surface
--bg-muted

--text-primary
--text-secondary
--text-muted

--border-default

--accent
--accent-soft

--success
--warning
--danger
--info
```

Nếu muốn mỗi Volume có màu nhận diện riêng:

- chỉ thay `--accent`
- không thay toàn bộ visual language

Ví dụ:

```text
Volume 1 → blue
Volume 2 → teal
Volume 3 → violet
...
```

nhưng:

- sidebar vẫn cùng layout
- card vẫn cùng style
- code vẫn cùng style
- typography vẫn cùng hệ thống

---

# 7. Chapter Hero

Mỗi chapter phải có chapter hero cùng cấu trúc.

Ví dụ:

```text
VOLUME 02 · BUILDING THE E-COMMERCE CORE

CHAPTER 06

Modular Monolith Architecture

How to organize an e-commerce backend before microservices become necessary.
```

Hero không được biến đổi thành:

- banner hình ảnh lớn ở chapter này
- card nhỏ ở chapter khác
- title centered ở chapter khác

Nếu design system hiện tại sử dụng left-aligned hero thì giữ nguyên toàn bộ.

---

# 8. Sidebar Rules

Sidebar phải nhất quán ở tất cả chapter.

Bao gồm:

```text
Inside E-commerce
Volume title

Chapters
01 ...
02 ...
03 ...

On this page
1. ...
2. ...
3. ...
```

Yêu cầu:

- Highlight chapter hiện tại.
- TOC lấy từ H2/H3 của chapter.
- Không render danh sách quá sâu.
- Sidebar desktop sticky nếu design hiện tại hỗ trợ.
- Mobile phải collapse thành menu/drawer hoặc block đơn giản.

Không được tạo sidebar khác riêng cho từng Volume.

---

# 9. Volume Index Rules

`index.html` của mỗi Volume phải là landing page thật sự, không phải danh sách hyperlink thô.

Bắt buộc có:

1. Volume number
2. Volume title
3. Mục tiêu Volume
4. Chapter list
5. Progress / status nếu phù hợp
6. Learning path
7. Link vào từng chapter
8. Previous / next Volume nếu đã tồn tại

Chapter cards phải dùng cùng component.

Ví dụ:

```text
Chapter 06
Modular Monolith Architecture

Tổ chức backend theo domain/module.

→ Read chapter
```

---

# 10. Content Component Library

Các chapter phải reuse cùng các component.

## 10.1 Callout

Các loại:

```text
Concept
Important
Warning
Production Note
Example
Key Takeaway
```

Không tự thiết kế callout mới.

---

## 10.2 Tables

Tất cả table dùng chung style:

- header rõ ràng
- border nhẹ
- zebra optional nhưng thống nhất
- responsive horizontal scroll trên màn hình nhỏ

Không inline CSS riêng trên từng table.

---

## 10.3 Code Blocks

Tất cả code block:

- cùng background
- cùng monospace font
- cùng padding
- cùng border radius
- có horizontal scroll
- language label nếu infrastructure hỗ trợ

Không đổi theme syntax riêng theo chapter.

---

## 10.4 Diagram Containers

Mermaid/SVG/image technical diagram phải được đặt trong component:

```html
<figure class="diagram">
  ...
  <figcaption>...</figcaption>
</figure>
```

Quy tắc:

- cùng border
- cùng background
- cùng padding
- max-width 100%
- SVG responsive
- diagram không bị crop

Diagram kỹ thuật không dùng AI image nếu Mermaid/SVG có thể diễn đạt chính xác hơn.

---

## 10.5 Engineering Scenario

Các tình huống thực tế nên dùng component thống nhất:

```text
SCENARIO

Flash Sale
100 products
10,000 concurrent buyers
```

Sau đó:

```text
Naive solution
↓
Failure
↓
Root cause
↓
Improved design
↓
Trade-off
↓
New bottleneck
```

Đây là visual pattern cốt lõi của bộ sách.

---

# 11. Chapter Learning Pattern

Mỗi chapter ưu tiên cùng pedagogical structure:

```text
1. Business Context
2. Naive Implementation
3. Breaking Point
4. Root Cause
5. Engineering Solution
6. Trade-offs
7. New Bottleneck
8. Production Considerations
9. Hands-on Lab
10. Key Takeaways
11. Knowledge Map
```

Không bắt buộc mọi chapter có đủ 11 mục nếu không phù hợp.

Nhưng không được thay đổi cách học một cách tùy tiện.

---

# 12. Diagrams

Ưu tiên theo thứ tự:

```text
1. Mermaid
2. SVG
3. HTML/CSS simulation
4. PNG/JPG illustration
```

Mermaid phù hợp cho:

- architecture
- flowchart
- state machine
- sequence
- dependency
- lifecycle

AI/generated illustration chỉ dùng khi cần giải thích trực giác hoặc business context.

Không dùng hình trang trí nếu không tăng giá trị học tập.

---

# 13. Responsive Requirements

HTML phải usable ở:

```text
Desktop
Tablet
Mobile
```

Desktop:

```text
sidebar | content
```

Mobile:

```text
header/menu
content
```

Không để:

- code vượt viewport
- table phá layout
- diagram bị cắt
- sidebar chiếm phần lớn màn hình

---

# 14. Navigation

Cuối mỗi chapter luôn có:

```text
← Previous Chapter

Volume Index

Next Chapter →
```

Chapter đầu:

- không cần Previous hoặc link về Volume trước nếu chưa có

Chapter cuối:

- Next có thể dẫn sang Volume tiếp theo nếu Volume đó tồn tại

Không hardcode link sai.

Trước khi bàn giao phải kiểm tra toàn bộ local links.

---

# 15. CSS Architecture

Ưu tiên:

```text
shared/reader.css
```

Không inline CSS dài trong từng HTML.

Nếu cần component mới:

1. xác định component có reusable không
2. nếu reusable → thêm vào `reader.css`
3. nếu chỉ phục vụ một diagram đặc biệt → scoped CSS nhỏ được phép

Không duplicate CSS giữa chapter.

---

# 16. JavaScript Rules

Ưu tiên static HTML.

JavaScript chỉ dùng cho:

- sidebar toggle
- TOC interaction
- diagram interaction
- simulation
- copy code
- search

Không thêm framework frontend lớn chỉ để render nội dung tĩnh.

Nếu đã có `reader.js`, mở rộng nó thay vì tạo script riêng từng chapter.

---

# 17. Accessibility

Bắt buộc:

- semantic headings
- đủ contrast
- `alt` cho informative images
- keyboard usable navigation
- link text có nghĩa
- không encode thông tin chỉ bằng màu sắc

Diagram nên có caption hoặc explanation bằng text.

---

# 18. Content Preservation Rule

Khi unify giao diện của chapter cũ:

**không regenerate nội dung nếu không cần thiết.**

Ưu tiên:

```text
Preserve <article>
Replace page shell
Apply shared CSS
Apply shared navigation
```

Mục tiêu là sửa UI mà không làm mất kiến thức.

---

# 19. File Naming

Dùng naming convention:

```text
chapter-06-modular-monolith.html
chapter-06-modular-monolith.md

chapter-07-database-design.html
chapter-07-database-design.md
```

Assets:

```text
assets/
  diagrams/
    chapter-06/
    chapter-07/
```

Không dùng tên:

```text
final.html
final2.html
new-final.html
book-newest.html
```

---

# 20. Required Validation Before Delivery

Trước khi bàn giao chapter/volume:

## Structure

- [ ] Có H1 duy nhất
- [ ] Heading hierarchy hợp lệ
- [ ] Shared stylesheet được load
- [ ] Shared JS được load nếu cần

## Navigation

- [ ] Previous link đúng
- [ ] Next link đúng
- [ ] Volume index đúng
- [ ] Sidebar active state đúng
- [ ] TOC đúng section

## Assets

- [ ] Không có missing image
- [ ] Không có missing SVG
- [ ] Không có broken relative path

## Responsive

- [ ] Table không phá layout
- [ ] Code scroll được
- [ ] Diagram responsive
- [ ] Mobile usable

## Visual Consistency

- [ ] Hero giống các chapter trước
- [ ] Code block cùng style
- [ ] Table cùng style
- [ ] Callout cùng style
- [ ] Diagram frame cùng style
- [ ] Chapter pagination cùng style

---

# 21. Delivery Contract

Mỗi lần tạo chapter mới phải output:

```text
chapter-NN-name.md
chapter-NN-name.html
assets/diagrams/chapter-NN/*
```

Khi hoàn thành Volume:

```text
volume-NN/
├── index.html
├── reader.css
├── reader.js
├── chapter-*.html
├── chapter-*.md
├── assets/
└── Volume-NN.zip
```

Nếu PDF được tạo:

```text
Inside-Ecommerce-Volume-NN.pdf
```

PDF phải lấy từ cùng source/design system, không thiết kế lại độc lập.

---

# 22. Anti-patterns

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

# 23. Definition of Done

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

# 24. Instruction for AI Agent

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

---

# 25. One-line Rule

> **New chapter = new knowledge, not a new visual identity.**
