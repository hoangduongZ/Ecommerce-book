#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from lxml import etree
from pypdf import PdfReader
import re,zipfile
ROOT=Path(__file__).resolve().parents[1]
md=ROOT/'chapter-05-order-lifecycle.md';ht=ROOT/'chapter-05-order-lifecycle.html'
text=md.read_text(encoding='utf8');html=ht.read_text(encoding='utf8');soup=BeautifulSoup(html,'html.parser')
headers=re.findall(r'^## 5\.(\d+)\.',text,re.M)
assert headers==[str(i) for i in range(1,21)],'Section order/count wrong'
merm=text.count('```mermaid');svgs=list((ROOT/'assets/chapter-05').glob('diagram-*.svg'))
assert merm==len(svgs)==16,(merm,len(svgs))
for f in svgs:
 tree=etree.parse(str(f));assert tree.getroot().tag.endswith('svg') and f.stat().st_size>200
fig=soup.select('figure.diagram');assert len(fig)==16
for i in range(1,6):
 stem={1:'chapter-01-ecommerce-ecosystem',2:'chapter-02-ecommerce-business-models',3:'chapter-03-domain-modeling',4:'chapter-04-product-pricing',5:'chapter-05-order-lifecycle'}[i]
 assert (ROOT/f'{stem}.md').exists() and (ROOT/f'{stem}.html').exists(),stem
for html_file in ROOT.glob('*.html'):
 page=BeautifulSoup(html_file.read_text(encoding='utf8'),'html.parser')
 for t in page.find_all(['a','img']):
  rel=t.get('href') if t.name=='a' else t.get('src')
  if rel and not (rel.startswith(('#','http:','https:','mailto:','data:','javascript:','file:'))):
   target=ROOT/rel.split('#')[0]
   assert target.exists(),f'{html_file.name}: broken {rel}'
pdf=ROOT/'Inside-Ecommerce-Volume-01.pdf';reader=PdfReader(str(pdf));assert len(reader.pages)>=35
assert 'Order Lifecycle' in '\n'.join((reader.pages[-1].extract_text() or '',reader.pages[-2].extract_text() or ''))
for lab in ['README.md','schema.sql','seed.sql','queries.sql','test-scenarios.md']:
 assert (ROOT/'labs/chapter-05'/lab).exists()
archive=Path('/mnt/data/Inside-Ecommerce-Volume-01-Complete.zip')
assert archive.exists()
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 names=z.namelist()
 assert any(x.endswith('chapter-05-order-lifecycle.md') for x in names)
 assert any(x.endswith('Inside-Ecommerce-Volume-01.pdf') for x in names)
print('PASS: 20 numbered content sections and 16 editable Mermaid diagrams')
print('PASS: 16 valid SVG illustrations and 16 HTML diagram figures')
print('PASS: chapters 01–05 Markdown + HTML and all HTML local links resolve')
print(f'PASS: PDF {len(reader.pages)} pages, text extractable, includes final chapter')
print('PASS: Chapter 05 SQL Lab has 5 documented artifacts (static review only; no PostgreSQL integration run)')
print(f'PASS: ZIP valid, {len(names)} entries, {archive.stat().st_size} bytes')
