# Inside E-commerce UI Consistency — Reference

Chi tiết đầy đủ cho skill [SKILL.md](SKILL.md). Đọc file này trước khi tạo hoặc
chỉnh sửa chapter HTML, volume index, component, hoặc book-wide CSS/JS.

---

# 1. Typography Rules

Font stack thật (định nghĩa trên `body` trong `reader.css`, không khai báo lại ở chapter khác):

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
font-size: 16px;
line-height: 1.72;
```

Không được đổi font riêng từng chapter.

Hierarchy thật đang dùng trong `article` (xem chapter-01 làm ví dụ tham chiếu):

```text
div.eyebrow  → "VOLUME N · CHAPTER NN" (pill nhỏ, không phải heading)
    ↓
h1 (chỉ 1 lần/chapter) → tên sách: "INSIDE E-COMMERCE"
    ↓
h2  → "Volume N — Tên Volume" (ngay dưới H1, vẫn là phần hero)
    ↓
h3  → "Chapter NN — Tên chapter" (vẫn là phần hero)
    ↓
h2  → các section nội dung N.1, N.2, ... (mức chính của chapter)
    ↓
h3  → sub-section trong mỗi N.x
    ↓
h4  → detail heading khi cần (article>h1:first-of-type có size riêng, size chuẩn:
      h1 38px / h2 27px / h3 20px / h4 17px)
    ↓
Body (p)
```

Lưu ý quan trọng: H1 hiện tại là **tên sách**, không phải tên chapter — tên chapter
nằm ở H3 của khối hero. Đây là hành vi thật đang triển khai, giữ nguyên khi thêm
chapter mới; đừng "sửa" H1 thành tên chapter vì sẽ làm hero khác với 5 chapter đã có.

Quy tắc:

- Chỉ có **1 H1** trong mỗi chapter (đang là tên sách, đặt ở đầu hero).
- Không dùng heading chỉ để làm chữ to.
- Không nhảy trực tiếp H2 → H4 trong phần nội dung (N.1, N.2, ...).
- Paragraph dùng `line-height: 1.72` như đã định nghĩa, không override riêng.
- Độ rộng phần đọc bị giới hạn bởi `article { width: min(var(--content), calc(100% - 56px)) }`,
  với `--content: 900px` — không set `max-width` khác trên chapter riêng lẻ.

Ưu tiên readability hơn density.

---

# 2. Spacing System

`reader.css` **hiện chưa** khai báo spacing scale dạng CSS custom property
(không có `--space-1`...`--space-8`). Thay vào đó, mỗi component tự dùng giá trị
px cố định nhưng nhất quán theo ngữ cảnh của nó. Các giá trị đang thực sự dùng:

```text
Sidebar padding      : 26px 20px 30px
Article padding      : 54px 62px  (mobile ≤640px: 28px 20px)
Article margin       : 46px auto 70px  (mobile: 24px auto 40px)
Topbar height/padding: 58px cao, 0 28px ngang
Chapter-link padding : 10px 9px
Chapter-nav gap       : 14px
Table cell padding   : 12px 14px
Diagram padding      : 18px
Blockquote padding   : 15px 18px
Heading top-margin   : h2 = 52px, h3 = 34px, h4 = 26px
```

Khi thêm component mới:

- **Không bịa số ngẫu nhiên** (`margin-top: 37px; padding: 19px; gap: 27px;`).
  Chọn giá trị gần nhất với các mốc đã liệt kê ở trên cho cùng loại phần tử
  (ví dụ: một box nội dung mới nên dùng padding tương tự `.diagram` hoặc
  `blockquote`, không tự nghĩ ra số mới).
- Nếu cảm thấy cần một spacing scale chính thức (dạng `--space-N`), đó là một
  thay đổi ở `reader.css` `:root`, áp dụng cho toàn bộ book — không thêm biến
  cục bộ trong một chapter.

---

# 3. Color System

Không chọn màu riêng cho từng component. Token thật đang khai báo trong
`assets/reader.css :root` (Volume 1):

```css
--bg:      #f5f7fb;   /* nền toàn trang (body) */
--surface: #ffffff;   /* nền article/card chính */
--surface-2: #f8fbfe; /* nền phụ: table header nhạt, diagram bg (#fbfdff gần giống) */
--ink:     #182230;   /* màu chữ chính */
--muted:   #64748b;   /* chữ phụ / meta / caption */
--line:    #dce4ed;   /* border mặc định */
--brand:   #183b56;   /* heading, topbar link */
--brand-2: #256b91;   /* link thường, eyebrow text */
--accent:  #eaf4fa;   /* nền pill (eyebrow), nền chapter-link active */
--code:    #0f172a;   /* nền code block (pre) */
--shadow:  0 12px 35px rgba(15,23,42,.08);
--radius:  18px;       /* khai báo nhưng KHÔNG áp dụng đồng bộ — mỗi component
                          đang tự set border-radius riêng (article 24px,
                          diagram/chapter-nav 14-16px, inline code 6px,
                          progress bar 99px). Nếu chuẩn hoá lại, sửa ở đây rồi
                          áp `border-radius: var(--radius)` cho từng nơi. */
--sidebar: 300px;      /* độ rộng sidebar */
--content: 900px;      /* max-width phần đọc (article) */
```

Không có `--success/--warning/--danger/--info` hay các biến semantic khác — chưa
có nhu cầu (không có callout theo loại, xem §7.1). Nếu cần thêm, khai báo trong
cùng khối `:root` này, không tạo file CSS riêng.

Nếu muốn mỗi Volume có màu nhận diện riêng:

- chỉ thay `--accent` (và có thể `--brand-2` nếu cần tương phản) trong bản
  `reader.css` của Volume đó
- không thay toàn bộ visual language

Ví dụ (định hướng, Volume 1 hiện là xanh dương/`--brand: #183b56`):

```text
Volume 1 → blue (hiện tại)
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

# 4. Chapter Hero

Không có class `chapter-hero` hay thẻ `<header>` riêng. Hero thật là mấy phần tử
đầu tiên nằm phẳng bên trong `<article>`, không bọc thêm gì — copy đúng pattern
này (rút từ `chapter-01-ecommerce-ecosystem.html`):

```html
<article>
  <div class="eyebrow">VOLUME 1 · CHAPTER 01</div>
  <h1 id="...">INSIDE E-COMMERCE</h1>
  <h2 id="...">Volume 1 — Understanding E-commerce</h2>
  <h3 id="...">Chapter 01 — The E-commerce Ecosystem</h3>
  <blockquote>
    <p><strong>Câu hỏi dẫn đường:</strong> ... (câu hỏi mở đầu chapter)</p>
  </blockquote>
  <!-- nội dung chapter bắt đầu từ đây bằng h2 tiếp theo -->
```

Quy tắc:

- `div.eyebrow` luôn có dạng `VOLUME N · CHAPTER NN`.
- `h1` luôn là tên sách "INSIDE E-COMMERCE" — giống hệt nhau ở mọi chapter.
- `h2` là "Volume N — Tên Volume", `h3` là "Chapter NN — Tên chapter".
- `blockquote` ngay sau đó là câu hỏi dẫn đường/subtitle — tùy chọn nhưng nên có,
  dùng đúng style `blockquote` chung, không tạo hero-quote riêng.

Hero không được biến đổi thành:

- banner hình ảnh lớn ở chapter này
- card nhỏ ở chapter khác
- title centered ở chapter khác
- bọc trong `<header>`/`<section>` riêng ở một số chapter nhưng không phải chapter khác

Giữ nguyên toàn bộ pattern left-aligned, flat-inside-`<article>` này cho mọi chapter mới.

---

# 5. Sidebar Rules

Sidebar (`<aside class="sidebar">`) phải nhất quán ở tất cả chapter. Cấu trúc thật:

```html
<aside class="sidebar">
  <a class="brand-link" href="index.html">
    <span class="kicker">Backend Engineering · System Design</span>
    <strong>INSIDE E-COMMERCE</strong>
    <small>Volume 1 · Understanding E-commerce</small>
  </a>

  <div class="volume-progress">
    <div class="row"><span>Volume progress</span><span>5 / 5</span></div>
    <div class="progress"><span></span></div>
  </div>

  <div class="nav-label">Chapters</div>
  <div class="chapter-list">
    <a class="chapter-link active" href="chapter-01-....html"><b>01</b><span>Tên chapter</span></a>
    <a class="chapter-link" href="chapter-02-....html"><b>02</b><span>Tên chapter</span></a>
    <!-- ... -->
  </div>

  <div class="nav-label">In this chapter</div>
  <nav class="toc">
    <a class="toc-h2" href="#...">Section H2</a>
    <a class="toc-h3" href="#...">Sub-section H3</a>
  </nav>
</aside>
```

Yêu cầu:

- `.chapter-link.active` trên chapter hiện tại (chỉ 1 item).
- `.toc` build từ H2/H3 thật của bài (`a.toc-h2` cho H2, `a.toc-h3` cho H3 — H3
  được thụt vào bằng `padding-left:18px` trong CSS, không cần class lồng thêm).
- Sidebar rộng cố định `var(--sidebar)` = 300px, nền tối `#122b3d`, `position: sticky`
  trên desktop (`min-width: 981px`).
- Dưới 980px: sidebar chuyển thành drawer cố định (`position: fixed`, ẩn bằng
  `transform: translateX(-105%)`), mở bằng nút `.menu-btn` (☰) trong `.topbar`,
  toggle qua class `.sidebar.open` + `body.nav-open` (logic nằm trong `reader.js`,
  xem §13). Không tự viết lại logic toggle này trong chapter mới — dùng chung
  `reader.js`.
- `.volume-progress .progress span` hiện luôn render `width:100%` (chưa thật sự
  tính theo vị trí đọc) — đây là giới hạn hiện tại, không phải bug cần bạn tự sửa
  khi chỉ đang thêm chapter.

Không được tạo sidebar khác riêng cho từng Volume (ngoại trừ nội dung `brand-link`/
`chapter-list` đổi theo Volume đó).

---

# 6. Volume Index Rules

`index.html` của mỗi Volume phải là landing page thật sự, không phải danh sách
hyperlink thô. Lưu ý quan trọng: **`index.html` cố ý KHÔNG dùng `reader.css` /
`.reader-shell`** — nó là một trang độc lập với `<style>` riêng ngay trong
`<head>`, vì đây là landing page (hero + stats + card grid), khác mục đích với
reading shell của chapter. Đây là quyết định thiết kế thật, không phải chỗ lệch
chuẩn cần "sửa cho giống chapter".

Component thật (từ `book/volume-01/index.html`), tái dùng nguyên bộ class này
cho Volume 2 trở đi, chỉ đổi nội dung:

```text
.wrap            container, max-width: 1120px
.hero            banner gradient tối (#102b40 → #1c5575), bo góc 28px
  .eyebrow         nhãn nhỏ uppercase phía trên h1
  h1               tên sách, viết hoa, size clamp(42px,7vw,72px)
  h2               "Volume N — Tên Volume"
  p                đoạn mục tiêu Volume
  .hero-actions    nhóm nút
    .btn.primary     nút chính: "Bắt đầu đọc →" → chapter đầu tiên
    .btn.secondary   nút phụ: link PDF Volume (nếu có)
.stats           grid 3 cột, mỗi .stat là 1 thẻ trắng (số chapter, trạng thái, range)
.section-title   nhãn nhỏ + h2 giới thiệu phần chapter list
.chapter-grid    grid 1 cột, danh sách .book-card
  .book-card       <a> tới từng chapter: .num (số) + h3 (tên) + p (mô tả) + mũi tên →
.next            box viền nét đứt, teaser cho Volume tiếp theo (nếu chưa tồn tại
                 file thật thì vẫn hiển thị dạng "Tiếp theo: Volume N — ...")
.footer          dòng chữ nhỏ cuối trang
```

Bắt buộc có trong nội dung:

1. Volume number
2. Volume title
3. Mục tiêu Volume (đoạn mở đầu trong `.hero`)
4. Chapter list (`.chapter-grid` gồm các `.book-card`, mỗi card 1 chapter)
5. Progress / status nếu phù hợp (`.stats`)
6. Learning path (thứ tự chapter trong `.chapter-grid` chính là learning path)
7. Link vào từng chapter (`.book-card` href tới `chapter-NN-*.html`)
8. Previous / next Volume nếu đã tồn tại (`.next` box; trỏ tới `../volume-0(N+1)/index.html`
   khi Volume đó đã có file thật — không hardcode link tới Volume chưa tồn tại)

Chapter cards phải dùng cùng component `.book-card`, ví dụ thật:

```html
<a class="book-card" href="chapter-06-modular-monolith.html">
  <div class="num">06</div>
  <div><h3>Modular Monolith Architecture</h3><p>Tổ chức backend theo domain/module.</p></div>
  <span>→</span>
</a>
```

---

# 7. Content Component Library

Các chapter phải reuse cùng các component.

## 7.1 Callout

Hiện tại **chỉ có một loại callout** đã được style: `<blockquote>` thường (viền
trái xanh, nền `#f0f7fb`, chữ `#345266`, bo góc phải). Chưa có class riêng cho
từng loại (`Concept`, `Important`, `Warning`, `Production Note`, `Example`,
`Key Takeaway`) — nội dung của các loại này hiện được viết bằng `blockquote` +
`<strong>` mở đầu câu (ví dụ `<strong>Đóng Volume 1:</strong> ...`), không phải
bằng biến thể màu sắc khác nhau.

Vì vậy:

- Dùng `<blockquote>` cho mọi callout/note/warning cho đến khi có class riêng.
- Nếu thật sự cần phân biệt trực quan theo loại (ví dụ Warning phải có màu khác
  Concept), thêm modifier class kiểu `blockquote.warning` **vào `reader.css`**
  trước, rồi mới dùng trong chapter — không inline-style một callout riêng lẻ.

---

## 7.2 Tables

Thẻ `<table>` trần (không cần class) đã được style toàn cục trong `reader.css`:

- `th`: nền `#eef5f9`, chữ đậm, `text-align: left`
- border nhẹ `1px solid var(--line)`, bo góc ngoài 14px, `border-collapse: separate`
- zebra qua `tbody tr:nth-child(even)` (nền `#fbfdff`)
- responsive: dưới 640px, `table { display: block; overflow: auto }`

Không inline CSS riêng trên từng table, không thêm class thừa như `class="table"`.

---

## 7.3 Code Blocks

`<pre><code>...</code></pre>` trần, style toàn cục:

- nền tối `var(--code)` (#0f172a), chữ `#dbeafe`, padding `20px 22px`, bo góc 14px
- `pre { overflow: auto }` cho horizontal scroll
- inline code (`p code`, `li code`, `td code`) style riêng, nhạt: nền `#edf3f7`,
  chữ `#173b55`, bo góc 6px — không dùng nền tối cho inline code

Chưa có language label hay nút copy-code trong `reader.css`/`reader.js` hiện tại —
đây là tính năng **cho phép thêm sau** (mở rộng `reader.js`), không phải yêu cầu
đã tồn tại. Đừng giả định nó đã hoạt động khi viết chapter mới.

Không đổi theme syntax riêng theo chapter.

---

## 7.4 Diagram Containers

Đây là component **đã khớp đúng thực tế** — tiếp tục dùng nguyên như vậy:

```html
<figure class="diagram">
  <img alt="Sơ đồ kỹ thuật N" loading="lazy" src="assets/diagram-NN.svg">
  <figcaption>Sơ đồ NN · SVG có thể phóng to</figcaption>
</figure>
```

Style thật của `.diagram`: nền `#fbfdff`, border `1px solid var(--line)`, bo góc
16px, padding 18px, `text-align: center`; `img`/`svg` bên trong `max-width: 100%`.

Quy tắc:

- luôn dùng `<img loading="lazy">` trỏ tới file `.svg` tĩnh, không nhúng inline `<svg>`.
- cùng border / background / padding như trên — không style riêng từng diagram.
- SVG responsive (max-width 100%), không bị crop.
- `alt` luôn có nội dung mô tả (không để rỗng), `figcaption` luôn có.

Diagram kỹ thuật không dùng AI image nếu Mermaid/SVG có thể diễn đạt chính xác hơn.

---

## 7.5 Engineering Scenario

Chưa có class `.scenario` hay box riêng trong `reader.css` — các tình huống kiểu
"Bad case / Failure scenario / Bottleneck Shifting" trong 5 chapter hiện tại đều
được viết bằng heading H2/H3 thường (ví dụ `4.1. Bad case: ...`, `4.15. Failure
Scenarios và nguyên tắc xử lý`, `4.13. Bottleneck Shifting: ...`) kết hợp
paragraph, table, blockquote — không phải một component hình ảnh riêng.

Vì vậy:

- Viết engineering scenario bằng heading + nội dung thường như các chapter đã có
  (xem §8 để biết vị trí các phần này thường xuất hiện trong một chapter).
- Chỉ tạo một box `.scenario` mới trong `reader.css` nếu bạn (hoặc user) quyết
  định thêm hẳn một component trực quan mới cho toàn bộ sách — không tự vẽ box
  đó bằng inline style trong một chapter.

Đây vẫn là một pattern nội dung cốt lõi của bộ sách, chỉ khác là hiện thực hoá
bằng heading/table/blockquote sẵn có, không phải bằng một component CSS riêng.

---

# 8. Chapter Learning Pattern

Đối chiếu heading thật của cả 5 chapter Volume 1, pattern chung — không cứng nhắc
11 bước cố định, mà là khung linh hoạt sau:

```text
1. Hero (xem §4): Volume label + Chapter title + câu hỏi dẫn đường
2. Learning objectives — H3: "Sau chương này, bạn có thể" /
   "Sau chương này, bạn sẽ có khả năng"
3. N.1 → N.k — các section nội dung đánh số (H2), số lượng thay đổi theo chapter
   (7 mục ở chapter 01, tới 20 mục ở chapter 05). Trong dải này thường có:
   - một "Bad case: ..." mở đầu (ví dụ có sẵn từ đầu chương)
   - ít nhất một "Failure scenarios: ..." hoặc "Race Condition ..."
   - một phần thiết kế kỹ thuật (schema/API/Spring Boot design)
   - một phần "Bottleneck Shifting" ở các chapter về pricing/order (04, 05)
4. Engineering Lab / Hands-on Lab — thường là mục N.k cuối cùng trước phần đóng
   chương, có thể chia Lab A / Lab B / Lab C (H3) bên trong
5. Khối đóng chương — mỗi chapter dùng MỘT TẬP HỢP CON của:
   "Knowledge Map" (figure.diagram), "Key Takeaways" (ol), hoặc
   "Chapter Review" (câu hỏi tự kiểm tra) — chapter 01–03 dùng Knowledge Map +
   Key Takeaways; chapter 04–05 dùng Chapter Review thay vì Key Takeaways
6. Tài liệu tham khảo — "Tài liệu tham khảo", "Tài liệu tham khảo và giới hạn áp
   dụng", hoặc "Kết nối chương tiếp theo" (tên khác nhau nhưng luôn có 1 mục đóng
   dạng này ở cuối)
```

Không bắt buộc mọi chapter dùng đúng tên mục hay đủ mọi phần trên — nhưng thứ tự
lớn (hero → objectives → nội dung đánh số → lab → khối đóng chương → tham khảo)
là pattern thật đang lặp lại ở cả 5 chapter, hãy giữ đúng thứ tự này.

Không được thay đổi cách học một cách tùy tiện.

---

# 9. Diagrams

Hiện trạng thật: **mọi diagram trong HTML đã xuất bản đều là file `.svg` tĩnh**,
nhúng qua `<figure class="diagram"><img src="assets/diagram-NN.svg">` (xem §7.4).
Không có Mermaid render trực tiếp (client-side) trong các file `.html` đã publish.
Theo README.md, mã nguồn Mermaid (nếu có) chỉ nằm trong file `.md` nguồn của
chapter — HTML luôn nhận SVG đã export sẵn.

Pipeline thật: tác giả diagram bằng Mermaid (hoặc vẽ tay) trong `.md` → export/
convert thành `.svg` tĩnh → đặt vào `assets/` → nhúng bằng `figure.diagram`.

Ưu tiên nguồn khi tạo diagram mới, vẫn theo thứ tự:

```text
1. Mermaid (nguồn trong .md, sau đó export ra .svg tĩnh để nhúng vào .html)
2. SVG vẽ tay/trực tiếp
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

# 10. Responsive Requirements

Breakpoint thật trong `reader.css` (đừng dùng số khác):

```text
> 980px   Desktop: .reader-shell là grid 2 cột `var(--sidebar) minmax(0,1fr)`
          → sidebar 300px sticky | content-wrap
≤ 980px   Tablet/Mobile: .reader-shell chuyển display:block; .sidebar thành
          drawer cố định off-canvas (ẩn bằng translateX(-105%), mở bằng
          .sidebar.open); .menu-btn hiện ra trong .topbar
≤ 640px   Mobile nhỏ: article padding giảm còn 28px 20px, h1 32px, h2 23px,
          table { display:block; overflow:auto }, .chapter-nav xuống 1 cột
@media print  .sidebar/.topbar/.chapter-nav ẩn hoàn toàn — dùng cho xuất PDF
```

Không để:

- code vượt viewport (`pre { overflow: auto }` đã xử lý, đừng tắt)
- table phá layout (dựa vào `table { display:block; overflow:auto }` ở ≤640px)
- diagram bị cắt (`.diagram img { max-width: 100% }`)
- sidebar chiếm phần lớn màn hình trên mobile — phải là drawer ẩn mặc định,
  không phải block luôn hiển thị chiếm chỗ nội dung

---

# 11. Navigation

Component thật là `<div class="chapter-nav">` — grid **2 cột** (Previous / Next),
**không có** link "Volume Index" ở giữa. Link về Volume home nằm riêng, trong
`.topbar` ở đầu trang ("Volume home"), không lặp lại ở chapter-nav.

Chapter giữa (02–04), cả hai cột đều có link:

```html
<div class="chapter-nav">
  <a href="chapter-02-....html"><small>← Chương trước</small>Tên chapter trước</a>
  <a href="chapter-04-....html"><small>Chương tiếp theo →</small>Tên chapter sau</a>
</div>
```

Chapter đầu tiên (01): cột trái là placeholder rỗng để giữ layout 2 cột, **không
xoá cột đó**:

```html
<div class="chapter-nav">
  <span class="empty"></span>
  <a href="chapter-02-....html"><small>Chương tiếp theo →</small>...</a>
</div>
```

Chapter cuối cùng của Volume hiện tại (05, khi chưa có Volume 2 dạng file thật):
cột phải trỏ về `index.html` với copy đóng chương, không để trống và không
hardcode sang một Volume chưa tồn tại:

```html
<a href="index.html"><small>Hoàn tất Volume 1 →</small>Về trang chủ</a>
```

Khi Volume tiếp theo đã có file thật, đổi cột phải của chapter cuối cùng trỏ
sang chapter đầu tiên của Volume đó.

Không hardcode link sai. Trước khi bàn giao phải kiểm tra toàn bộ local links.

---

# 12. CSS Architecture

Ưu tiên (đường dẫn thật, không phải `shared/`):

```text
book/volume-NN/assets/reader.css
```

Chapter HTML chỉ có đúng 1 dòng liên kết CSS trong `<head>`:

```html
<link rel="stylesheet" href="assets/reader.css">
```

Không inline CSS dài trong từng HTML. Ngoại lệ thật đang tồn tại: `index.html`
(Volume landing page) có `<style>` riêng trong `<head>` — đây là chủ đích (xem
§6), không phải điều nên bắt chước cho chapter.

Nếu cần component mới:

1. xác định component có reusable không
2. nếu reusable → thêm vào `assets/reader.css` (khối `:root` cho token, sau đó
   selector riêng theo class — theo đúng thứ tự đang có trong file: `:root` →
   reset → sidebar → content → component → responsive → print)
3. nếu chỉ phục vụ một diagram đặc biệt → scoped CSS nhỏ được phép

Không duplicate CSS giữa chapter. Chưa có thư mục `shared/` cross-Volume — xem
§1 về việc copy `reader.css` khi tạo Volume mới.

---

# 13. JavaScript Rules

Ưu tiên static HTML. Hiện trạng thật của `assets/reader.js` (toàn bộ file, 6 dòng):

```js
const btn=document.querySelector('.menu-btn'), side=document.querySelector('.sidebar');
function closeNav(){side?.classList.remove('open');document.body.classList.remove('nav-open')}
btn?.addEventListener('click',()=>{side?.classList.toggle('open');document.body.classList.toggle('nav-open')});
document.addEventListener('click',e=>{if(document.body.classList.contains('nav-open')&&!side.contains(e.target)&&e.target!==btn)closeNav()});
document.querySelectorAll('.toc a').forEach(a=>a.addEventListener('click',closeNav));
```

Nó **chỉ** làm 2 việc: toggle sidebar drawer (`.menu-btn` click, click ra ngoài
để đóng) và tự đóng drawer khi bấm link trong `.toc`. Các mục dưới đây là
**phạm vi được PHÉP mở rộng thêm**, không phải tính năng đã có sẵn:

- sidebar toggle (đã có)
- TOC interaction (đã có: đóng drawer khi click TOC link)
- diagram interaction (chưa có)
- simulation (chưa có)
- copy code (chưa có)
- search (chưa có)

Không thêm framework frontend lớn chỉ để render nội dung tĩnh.

Nếu cần một trong các tính năng "chưa có" ở trên, **mở rộng `assets/reader.js`**
thay vì tạo script riêng từng chapter — và cập nhật lại mục này khi đã thêm.

---

# 14. Accessibility

Bắt buộc:

- semantic headings
- đủ contrast
- `alt` cho informative images
- keyboard usable navigation
- link text có nghĩa
- không encode thông tin chỉ bằng màu sắc

Diagram nên có caption hoặc explanation bằng text.

---

# 15. Content Preservation Rule

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

# 16. File Naming

Dùng naming convention (đúng như 5 chapter Volume 1 đang có):

```text
chapter-06-modular-monolith.html
chapter-06-modular-monolith.md

chapter-07-database-design.html
chapter-07-database-design.md
```

Diagram assets — quy ước thật là **`assets/chapter-NN/diagram-NN.svg`** (không có
tầng `diagrams/` trung gian như bản cũ của skill này từng ghi):

```text
assets/
  chapter-02/
    diagram-01.svg
    diagram-02.svg
    ...
  chapter-03/
    diagram-01.svg
    ...
```

Lưu ý lệch chuẩn có thật: `chapter-01` là ngoại lệ lịch sử — diagram của nó nằm
phẳng ở `assets/diagram-01.svg` … `diagram-10.svg`, không có subfolder riêng.
Đừng copy theo ngoại lệ này cho chapter mới — dùng pattern `assets/chapter-NN/`
như chapter 02–05.

Artifact phụ trợ khác cũng đang tồn tại thật, theo đúng convention khi có:

```text
chapter-NN-README.md        # ghi chú biên tập/build cho riêng chapter đó
chapter-NN-build-log.txt    # log build, không bắt buộc mọi chapter đều có

labs/chapter-NN/
  README.md
  schema.sql
  queries.sql
  seed.sql               # chỉ khi lab cần seed data
  test-scenarios.md

tools/build_chapterNN.py      # script build riêng chapter (nếu chapter cần build step)
tools/validate_chapterNN.py   # script validate riêng chapter
```

Không dùng tên:

```text
final.html
final2.html
new-final.html
book-newest.html
```

---

# 17. Required Validation Before Delivery

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

- [ ] Hero giống các chapter trước (div.eyebrow + h1 + h2 + h3 + blockquote, xem §4)
- [ ] Code block cùng style (pre/code, không tự đổi theme)
- [ ] Table cùng style (table trần, không thêm class)
- [ ] Callout cùng style (blockquote, xem §7.1)
- [ ] Diagram frame cùng style (figure.diagram, xem §7.4)
- [ ] `.chapter-nav` cùng style, đúng layout 2 cột prev/next (xem §11)

---

# 18. Delivery Contract

Mỗi lần tạo chapter mới phải output (đường dẫn thật trong `book/volume-NN/`):

```text
chapter-NN-name.md
chapter-NN-name.html
assets/chapter-NN/diagram-*.svg
chapter-NN-README.md        # nếu theo đúng convention hiện có, xem §16
```

Khi hoàn thành Volume, layout thật (tham chiếu `book/volume-01/`):

```text
book/volume-NN/
├── index.html
├── DESIGN-SYSTEM.md
├── README.md
├── chapter-*.html
├── chapter-*.md
├── chapter-*-README.md
├── assets/
│   ├── reader.css
│   ├── reader.js
│   └── chapter-NN/diagram-*.svg
├── labs/chapter-NN/          # nếu chapter có lab SQL/kỹ thuật
├── tools/                    # build/validate scripts riêng của Volume
└── Inside-Ecommerce-Volume-NN.pdf   # nếu đã xuất PDF
```

Không có bước "zip" hay file `Volume-NN.zip` trong quy trình thật hiện tại —
README.md của Volume 1 mô tả người đọc tự giải nén gói phân phối bên ngoài repo
này; đừng tạo file `.zip` trong `book/volume-NN/` trừ khi user yêu cầu.

Nếu PDF được tạo, đặt tên `Inside-Ecommerce-Volume-NN.pdf` và build bằng script
kiểu `tools/build_volumeNN_pdf.py` (xem `tools/build_volume01_pdf.py`), lấy từ
cùng source/design system, không thiết kế lại độc lập.
