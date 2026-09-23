from pathlib import Path
from bs4 import BeautifulSoup
import re, html, shutil, zipfile

ROOT = Path('/mnt/data/inside-ecommerce/volume-01')
ASSETS = ROOT/'assets'
ASSETS.mkdir(exist_ok=True)

chapters = [
 ('01','The E-commerce Ecosystem','Nghiệp vụ, luồng thông tin · tồn kho · tiền và business invariants','chapter-01-ecommerce-ecosystem.html'),
 ('02','E-commerce Business Models','B2C, B2B, D2C, Marketplace và multi-seller commerce','chapter-02-ecommerce-business-models.html'),
 ('03','Domain Modeling','Entity, Value Object, Aggregate, schema và transaction boundary','chapter-03-domain-modeling.html'),
 ('04','Product & Pricing Engineering','Pricing pipeline, voucher, checkout revalidation và price snapshot','chapter-04-product-pricing.html'),
 ('05','Order Lifecycle','State machine, cancellation, refund, idempotency và recovery','chapter-05-order-lifecycle.html'),
]

css = r'''
:root{
  --bg:#f5f7fb; --surface:#ffffff; --surface-2:#f8fbfe; --ink:#182230; --muted:#64748b;
  --line:#dce4ed; --brand:#183b56; --brand-2:#256b91; --accent:#eaf4fa; --code:#0f172a;
  --shadow:0 12px 35px rgba(15,23,42,.08); --radius:18px; --sidebar:300px; --content:900px;
}
*{box-sizing:border-box} html{scroll-behavior:smooth} body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.72;font-size:16px}
a{color:var(--brand-2)}
.reader-shell{min-height:100vh;display:grid;grid-template-columns:var(--sidebar) minmax(0,1fr)}
.sidebar{position:sticky;top:0;height:100vh;overflow:auto;background:#122b3d;color:#dbe9f2;border-right:1px solid rgba(255,255,255,.06);padding:26px 20px 30px}
.brand-link{display:block;color:white;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.12);padding-bottom:20px;margin-bottom:16px}
.brand-link .kicker{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#9dc2d8;font-weight:700}
.brand-link strong{display:block;font-size:20px;letter-spacing:.02em;margin-top:3px}.brand-link small{display:block;color:#aac3d2;margin-top:3px}
.volume-progress{margin:14px 0 20px}.volume-progress .row{display:flex;justify-content:space-between;font-size:12px;color:#b8ceda;margin-bottom:7px}.progress{height:6px;background:rgba(255,255,255,.12);border-radius:99px;overflow:hidden}.progress span{display:block;height:100%;width:100%;background:#72bddf}
.nav-label{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:#789caf;font-weight:800;margin:18px 8px 8px}.chapter-list{display:grid;gap:6px}.chapter-link{display:grid;grid-template-columns:30px 1fr;gap:8px;align-items:start;text-decoration:none;color:#c9dce7;padding:10px 9px;border-radius:10px}.chapter-link:hover{background:rgba(255,255,255,.07);color:white}.chapter-link.active{background:#eaf4fa;color:#17374d}.chapter-link b{font-size:12px;opacity:.8;padding-top:3px}.chapter-link span{font-size:13px;line-height:1.35;font-weight:650}
.toc{margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,.1)}.toc a{display:block;color:#aac3d2;text-decoration:none;font-size:12.5px;line-height:1.4;padding:6px 8px;border-radius:7px}.toc a:hover{background:rgba(255,255,255,.06);color:white}.toc a.toc-h3{padding-left:18px;font-size:12px;color:#8fb0c1}
.content-wrap{min-width:0}.topbar{height:58px;background:rgba(245,247,251,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;padding:0 28px}.topbar a{text-decoration:none;font-weight:700;color:var(--brand)}.topbar .crumb{font-size:13px;color:var(--muted)}.menu-btn{display:none;border:1px solid var(--line);background:white;border-radius:10px;padding:8px 11px;font-size:18px}
article{width:min(var(--content),calc(100% - 56px));margin:46px auto 70px;background:var(--surface);border:1px solid #e4eaf0;border-radius:24px;padding:54px 62px;box-shadow:var(--shadow)}
article>.eyebrow,article>.topline,article>.tag{display:inline-block;font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--brand-2);background:var(--accent);padding:7px 10px;border-radius:999px;margin-bottom:10px}
article>h1:first-of-type{font-size:clamp(34px,5vw,54px);line-height:1.02;letter-spacing:-.045em;margin:10px 0 12px;color:#102d43}h1{font-size:38px;line-height:1.12;color:#102d43;letter-spacing:-.03em}h2{font-size:27px;line-height:1.22;margin:52px 0 18px;color:#173b55;scroll-margin-top:82px;letter-spacing:-.02em;padding-top:4px}h3{font-size:20px;line-height:1.35;margin:34px 0 12px;color:#214e69;scroll-margin-top:82px}h4{font-size:17px;color:#315d76;margin-top:26px}p{margin:12px 0 18px}strong{color:#153e58}hr{border:0;border-top:1px solid var(--line);margin:42px 0}ul,ol{padding-left:24px}li{margin:7px 0}
blockquote{margin:22px 0;padding:15px 18px;border-left:4px solid #62a6c8;background:#f0f7fb;color:#345266;border-radius:0 12px 12px 0}blockquote p:last-child{margin-bottom:0}
pre{overflow:auto;background:var(--code);color:#dbeafe;padding:20px 22px;border-radius:14px;font-size:13.5px;line-height:1.6;border:1px solid #24334b;box-shadow:inset 0 1px 0 rgba(255,255,255,.05)}code{font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace}p code,li code,td code{background:#edf3f7;color:#173b55;border:1px solid #d9e4eb;border-radius:6px;padding:1px 5px;font-size:.9em}
table{width:100%;border-collapse:separate;border-spacing:0;margin:22px 0 30px;border:1px solid var(--line);border-radius:14px;overflow:hidden;font-size:14.5px}th{background:#eef5f9;color:#173b55;text-align:left;font-weight:750}th,td{padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}tr:last-child td{border-bottom:0}tbody tr:nth-child(even){background:#fbfdff}
.diagram{margin:26px 0 34px;padding:18px;background:#fbfdff;border:1px solid var(--line);border-radius:16px;text-align:center;overflow:auto}.diagram img,.diagram svg{max-width:100%;height:auto}.diagram figcaption{font-size:12px;color:var(--muted);margin-top:10px}
img{max-width:100%;height:auto}.chapter-nav{display:grid;grid-template-columns:1fr 1fr;gap:14px;width:min(var(--content),calc(100% - 56px));margin:0 auto 70px}.chapter-nav a{display:block;text-decoration:none;background:white;border:1px solid var(--line);border-radius:14px;padding:15px 17px;color:var(--brand);box-shadow:0 4px 16px rgba(15,23,42,.04)}.chapter-nav a:last-child{text-align:right}.chapter-nav small{display:block;color:var(--muted);font-weight:500;margin-bottom:3px}.chapter-nav .empty{visibility:hidden}
.footer,.foot{margin-top:46px;padding-top:20px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
/* neutralize legacy reader controls */
aside:not(.sidebar),nav:not(.chapter-list):not(.toc),.toolbar,.mobile-toggle,.toggle,.back{display:none!important}
@media(max-width:980px){.reader-shell{display:block}.sidebar{position:fixed;z-index:50;left:0;top:0;width:min(86vw,330px);transform:translateX(-105%);transition:.22s}.sidebar.open{transform:none}.content-wrap{width:100%}.menu-btn{display:block}.topbar{padding:0 16px}article{width:min(100% - 24px,var(--content));margin:24px auto 40px;padding:34px 26px}.chapter-nav{width:calc(100% - 24px)}body.nav-open:after{content:"";position:fixed;inset:0;background:rgba(15,23,42,.42);z-index:40}}
@media(max-width:640px){article{padding:28px 20px;border-radius:18px}h1{font-size:32px}h2{font-size:23px;margin-top:42px}table{display:block;overflow:auto}.chapter-nav{grid-template-columns:1fr}.chapter-nav a:last-child{text-align:left}}
@media print{.sidebar,.topbar,.chapter-nav{display:none!important}.reader-shell{display:block}article{box-shadow:none;border:0;width:100%;max-width:none;margin:0;padding:0}body{background:white}}
'''
(ASSETS/'reader.css').write_text(css,encoding='utf-8')
js = '''
const btn=document.querySelector('.menu-btn'), side=document.querySelector('.sidebar');
function closeNav(){side?.classList.remove('open');document.body.classList.remove('nav-open')}
btn?.addEventListener('click',()=>{side?.classList.toggle('open');document.body.classList.toggle('nav-open')});
document.addEventListener('click',e=>{if(document.body.classList.contains('nav-open')&&!side.contains(e.target)&&e.target!==btn)closeNav()});
document.querySelectorAll('.toc a').forEach(a=>a.addEventListener('click',closeNav));
'''
(ASSETS/'reader.js').write_text(js,encoding='utf-8')

def chapter_sidebar(current, soup):
    links=''.join(f'<a class="chapter-link {"active" if n==current else ""}" href="{fn}"><b>{n}</b><span>{html.escape(title)}</span></a>' for n,title,desc,fn in chapters)
    toc=[]
    for h in soup.select('article h2[id], article h3[id]'):
        text=' '.join(h.get_text(' ',strip=True).split())
        if len(text)>72: text=text[:69]+'…'
        toc.append(f'<a class="{"toc-h3" if h.name=="h3" else "toc-h2"}" href="#{h["id"]}">{html.escape(text)}</a>')
    return f'''<aside class="sidebar"><a class="brand-link" href="index.html"><span class="kicker">Backend Engineering · System Design</span><strong>INSIDE E-COMMERCE</strong><small>Volume 1 · Understanding E-commerce</small></a><div class="volume-progress"><div class="row"><span>Volume progress</span><span>5 / 5</span></div><div class="progress"><span></span></div></div><div class="nav-label">Chapters</div><div class="chapter-list">{links}</div><div class="nav-label">In this chapter</div><nav class="toc">{''.join(toc)}</nav></aside>'''

for idx,(num,title,desc,fn) in enumerate(chapters):
    p=ROOT/fn
    original=p.read_text(encoding='utf-8')
    backup=ROOT/(fn+'.legacy')
    if not backup.exists(): backup.write_text(original,encoding='utf-8')
    s=BeautifulSoup(original,'html.parser')
    article=s.find('article')
    if article is None:
        # fall back to main content, strip legacy aside/nav
        main=s.find('main') or s.body
        article=BeautifulSoup('<article></article>','html.parser').article
        for child in list(main.children):
            if getattr(child,'name',None) not in ('aside','nav'):
                article.append(child)
    # remove controls embedded inside article
    for sel in ['.toolbar','.mobile-toggle','.toggle','.back']:
        for el in article.select(sel): el.decompose()
    # Ensure chapter title identity is visible and consistent without altering content headings
    titleband=BeautifulSoup(f'<div class="eyebrow">VOLUME 1 · CHAPTER {num}</div>','html.parser').div
    # remove old eyebrow-like immediate first element(s)
    first_tags=[x for x in article.children if getattr(x,'name',None)]
    if first_tags and any(c in (first_tags[0].get('class') or []) for c in ['eyebrow','topline','tag']): first_tags[0].decompose()
    article.insert(0,titleband)
    # add IDs when missing on h2/h3
    used=set()
    for h in article.find_all(['h2','h3']):
        if not h.get('id'):
            base=re.sub(r'[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
            x=base; k=2
            while x in used: x=f'{base}-{k}'; k+=1
            h['id']=x
        used.add(h['id'])
    # Re-soup needed for TOC after IDs
    holder=BeautifulSoup('<div></div>','html.parser').div; holder.append(article)
    sidebar=chapter_sidebar(num,holder)
    prev = chapters[idx-1] if idx>0 else None; nxt=chapters[idx+1] if idx<len(chapters)-1 else None
    nav=f'''<div class="chapter-nav">{f'<a href="{prev[3]}"><small>← Chương trước</small>{html.escape(prev[1])}</a>' if prev else '<span class="empty"></span>'}{f'<a href="{nxt[3]}"><small>Chương tiếp theo →</small>{html.escape(nxt[1])}</a>' if nxt else '<a href="index.html"><small>Hoàn tất Volume 1 →</small>Về trang chủ</a>'}</div>'''
    out=f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Inside E-commerce Volume 1 Chapter {num} — {html.escape(title)}"><title>Inside E-commerce · Chapter {num} · {html.escape(title)}</title><link rel="stylesheet" href="assets/reader.css"></head><body><div class="reader-shell">{sidebar}<section class="content-wrap"><header class="topbar"><button class="menu-btn" aria-label="Mở mục lục">☰</button><div class="crumb">Volume 1 / Chapter {num}</div><a href="index.html">Volume home</a></header>{str(article)}{nav}</section></div><script src="assets/reader.js"></script></body></html>'''
    p.write_text(out,encoding='utf-8')

# index landing
cards=''.join(f'''<a class="book-card" href="{fn}"><div class="num">{num}</div><div><h3>{html.escape(title)}</h3><p>{html.escape(desc)}</p></div><span>→</span></a>''' for num,title,desc,fn in chapters)
index_css = '''
body{margin:0;background:#f3f6fa;color:#182230;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.65}.wrap{max-width:1120px;margin:auto;padding:32px 24px 70px}.hero{background:linear-gradient(135deg,#102b40,#1c5575);color:white;border-radius:28px;padding:54px 58px;box-shadow:0 24px 55px #14334824}.eyebrow{font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#a9d4e8;font-weight:800}.hero h1{font-size:clamp(42px,7vw,72px);line-height:.98;letter-spacing:-.055em;margin:14px 0 12px}.hero h2{margin:0;font-size:23px;font-weight:600;color:#d9edf6}.hero p{max-width:760px;color:#c4dce8;font-size:17px}.hero-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}.btn{display:inline-block;text-decoration:none;padding:11px 16px;border-radius:11px;font-weight:750}.btn.primary{background:white;color:#173c53}.btn.secondary{border:1px solid #5f8ca5;color:white}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:18px 0 36px}.stat{background:white;border:1px solid #dce5ed;border-radius:15px;padding:17px 19px}.stat strong{display:block;font-size:24px;color:#153e58}.stat span{font-size:13px;color:#64748b}.section-title{margin:38px 0 14px}.section-title small{display:block;color:#6c8292;text-transform:uppercase;letter-spacing:.12em;font-weight:800}.section-title h2{font-size:30px;margin:4px 0;color:#183b56;letter-spacing:-.025em}.chapter-grid{display:grid;grid-template-columns:1fr;gap:11px}.book-card{display:grid;grid-template-columns:54px 1fr 24px;align-items:center;gap:16px;background:white;border:1px solid #dce5ed;border-radius:16px;padding:20px 22px;text-decoration:none;color:#173c53;transition:.15s;box-shadow:0 5px 18px rgba(15,23,42,.035)}.book-card:hover{transform:translateY(-2px);border-color:#91b9cf;box-shadow:0 12px 26px rgba(15,23,42,.08)}.book-card .num{height:42px;width:42px;display:grid;place-items:center;border-radius:12px;background:#eaf4fa;color:#286986;font-weight:850}.book-card h3{margin:0 0 3px;font-size:19px}.book-card p{margin:0;color:#64748b;font-size:14px}.book-card>span{font-size:22px;color:#6598b3}.next{margin-top:32px;border:1px dashed #afc2cf;border-radius:18px;padding:23px 25px;background:#f8fbfd}.next strong{color:#173c53}.footer{color:#718395;font-size:13px;margin-top:34px}@media(max-width:680px){.wrap{padding:16px 12px 50px}.hero{padding:35px 25px;border-radius:20px}.stats{grid-template-columns:1fr}.book-card{grid-template-columns:44px 1fr}.book-card>span{display:none}}
'''
index=f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Inside E-commerce · Volume 1</title><style>{index_css}</style></head><body><main class="wrap"><section class="hero"><div class="eyebrow">Backend Engineering · System Design</div><h1>INSIDE<br>E-COMMERCE</h1><h2>Volume 1 — Understanding E-commerce</h2><p>Hiểu cách một hệ thống thương mại điện tử thực sự vận hành trước khi scale nó: domain, business model, pricing, order lifecycle và những invariants backend phải bảo vệ.</p><div class="hero-actions"><a class="btn primary" href="chapter-01-ecommerce-ecosystem.html">Bắt đầu đọc →</a><a class="btn secondary" href="Inside-Ecommerce-Volume-01.pdf">PDF Volume 1</a></div></section><section class="stats"><div class="stat"><strong>5</strong><span>Chapters</span></div><div class="stat"><strong>Volume 1</strong><span>Hoàn thành nội dung</span></div><div class="stat"><strong>01 → 05</strong><span>Business → Order Lifecycle</span></div></section><div class="section-title"><small>Reading path</small><h2>Năm chương · một mạch tư duy</h2></div><section class="chapter-grid">{cards}</section><section class="next"><strong>Tiếp theo: Volume 2 — Building the E-commerce Core</strong><br><span>Modular Monolith, Database Design, API Design, Transaction Management, Authentication & Authorization.</span></section><div class="footer">Inside E-commerce · Volume 1 · Unified Reader Edition</div></main></body></html>'''
(ROOT/'index.html').write_text(index,encoding='utf-8')

# create style guide/readme
(ROOT/'DESIGN-SYSTEM.md').write_text('''# Inside E-commerce — Reader Design System\n\n- Shared shell: `assets/reader.css` + `assets/reader.js`\n- Sidebar width: 300px; content max-width: 900px\n- One typography/color system across every chapter\n- Chapter navigation and table of contents use one component\n- Technical content remains unchanged; only HTML reading shell was normalized\n- Index is the Volume landing page, not a raw list of files\n''',encoding='utf-8')

# ZIP updated volume
zip_path=Path('/mnt/data/Inside-Ecommerce-Volume-01-Complete-Unified.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in ROOT.rglob('*'):
        if f.is_file() and not f.name.endswith('.legacy') and '_pdf-check' not in f.parts:
            z.write(f,Path('inside-ecommerce/volume-01')/f.relative_to(ROOT))
print(zip_path)
