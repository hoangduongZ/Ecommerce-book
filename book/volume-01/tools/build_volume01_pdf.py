#!/usr/bin/env python3
"""Make an offline PDF from existing, validated chapter HTML. No network assets."""
from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML
from html import escape
ROOT=Path(__file__).resolve().parents[1]
CHAPTERS=[
('The E-commerce Ecosystem','chapter-01-ecommerce-ecosystem.html'),
('E-commerce Business Models','chapter-02-ecommerce-business-models.html'),
('Domain Modeling','chapter-03-domain-modeling.html'),
('Product & Pricing Engineering','chapter-04-product-pricing.html'),
('Order Lifecycle','chapter-05-order-lifecycle.html')]
css='''
@page {size:A4; margin: 20mm 17mm 18mm 17mm;
  @bottom-center {content:"Inside E-commerce · Volume 1   |   " counter(page); font-size:9pt; color:#687d8e}}
@page :first { @bottom-center {content:""} }
body {font-family:"Noto Sans", "DejaVu Sans", sans-serif; font-size:9.6pt; line-height:1.52; color:#20394b}
h1 {font-size:22pt;color:#173c59;margin-bottom:15px}
h2 {font-size:15.5pt; border-bottom:1px solid #b7cadb;padding-bottom:6px;margin-top:25px;color:#205477;break-after:avoid}
h3 {font-size:12pt;color:#26628d;break-after:avoid}
h4 {font-size:10pt;color:#26628d;break-after:avoid}
p, li {orphans:2; widows:2} ul,ol {padding-left:19px}
blockquote {margin:12px 0;padding:7px 12px;background:#eaf3fa;border-left:3px solid #438ab9}
pre {white-space:pre-wrap;word-break:break-word; overflow-wrap:anywhere; font:8pt/1.38 "DejaVu Sans Mono",monospace;color:#e9f2fc;background:#132739;padding:10px;border-radius:5px;}
pre code {color:inherit;background:inherit} code {font:8.6pt "DejaVu Sans Mono",monospace;background:#eaf1f7;padding:0 2px}
table {border-collapse:collapse;width:100%;font-size:8.2pt;table-layout:auto}
th,td {border:1px solid #cbd9e4;padding:5px;vertical-align:top;word-break:break-word}
th {background:#eaf2f8;text-align:left} tr {break-inside:avoid}
figure.diagram {margin:13px 0;break-inside:avoid; text-align:center; padding:7px;border:1px solid #d7e4ec;background:#f6faff}
figure.diagram img {max-width:100%;max-height:145mm;object-fit:contain}
figcaption {font-size:8pt;color:#58768e;text-align:left}
figcaption details {display:none}
.cover {height:245mm;display:flex;flex-direction:column;justify-content:center;background:#152a3a;color:white;padding:26mm;margin:-20mm -17mm -18mm -17mm}
.cover small {letter-spacing:2px;color:#9fd0e9}.cover h1 {color:#fff;font-size:35pt}.cover h2 {color:#a4daff;border:0;font-size:20pt}
.cover p {font-size:12pt;color:#d4e5ed}
.toc {page-break-before:always}.toc li {margin:10px 0;font-size:11pt}
.chapter {page-break-before:always}
a {color:#245b86;text-decoration:none}
hr {border:0;border-top:1px solid #cadbe7}
'''
cover='<div class="cover"><small>BACKEND ENGINEERING · SYSTEM DESIGN</small><h1>INSIDE E-COMMERCE</h1><h2>Volume 1<br>Understanding E-commerce</h2><p>Business Domain · Marketplace · Domain Modeling · Pricing · Order Lifecycle</p><p>Tiếng Việt · Bản đọc PDF offline · 23/09/2026</p></div>'
toc='<section class="toc"><h1>Mục lục · Volume 1</h1><ol>'+''.join(f'<li><a href="#vol01-ch{n:02d}">{n:02d} — {escape(label)}</a></li>' for n,(label,_) in enumerate(CHAPTERS,1))+'</ol><p>Source Markdown và sơ đồ chỉnh sửa được nằm trong gói ZIP cùng Volume.</p></section>'
parts=[]
for n,(label,fn) in enumerate(CHAPTERS,1):
  path=ROOT/fn;soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
  art=soup.find('article')
  if art is None: raise RuntimeError('No article: '+fn)
  for script in art.find_all(['script','iframe']):script.decompose()
  for tag in art.find_all('a',href=True):
    href=tag['href']
    if href.startswith('assets/'):
      tag['href']=(ROOT/href).as_uri()
  for img in art.find_all('img',src=True):
    if img['src'].startswith('assets/'):
      img['src']=(ROOT/img['src']).as_uri()
  art['id']=f'vol01-ch{n:02d}'
  art['class']=['chapter']
  parts.append(str(art))
html='<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Inside E-commerce | Volume 1</title><style>'+css+'</style></head><body>'+cover+toc+'\n'.join(parts)+'</body></html>'
root_out=ROOT/'Inside-Ecommerce-Volume-01.pdf'
HTML(string=html,base_url=str(ROOT)).write_pdf(str(root_out))
print(root_out,root_out.stat().st_size)
