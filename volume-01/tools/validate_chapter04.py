#!/usr/bin/env python3
from pathlib import Path
import re, sys, zipfile, xml.etree.ElementTree as ET
from decimal import Decimal
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
slug='chapter-04-product-pricing'
md=(ROOT/f'{slug}.md').read_text(encoding='utf-8')
page=(ROOT/f'{slug}.html').read_text(encoding='utf-8')
soup=BeautifulSoup(page,'html.parser')
assert len(re.findall(r'^## 4\.\d+\.',md,re.M)) == 17, 'wrong chapter section count'
assert len(re.findall(r'^```mermaid\s*$',md,re.M)) == 14, 'wrong Mermaid count'
assert md.count('```')%2 == 0, 'unpaired markdown fence'
assert 'Chương 04 — Product & Pricing Engineering' in page, 'wrong HTML title'
assert len(soup.find_all('figure',class_='diagram'))==14, 'wrong figure count'
assert len(soup.select('nav a.h2'))>=17, 'missing TOC headings'
print('PASS: 17 main sections, 14 Mermaid diagrams, 14 HTML figures, TOC, HTML title')
files=list((ROOT/'assets/chapter-04').glob('diagram-*.svg'))
assert len(files)==14,'missing SVG'
for f in files:
    tree=ET.parse(f)
    assert tree.getroot().tag.endswith('svg'),f'not SVG: {f}'
    assert f.stat().st_size>800,f'empty SVG: {f}'
print('PASS: all 14 SVG files are nonempty, valid XML/SVG')
for chapter in range(1,5):
    h=list(ROOT.glob(f'chapter-{chapter:02d}-*.html'))
    m=list(ROOT.glob(f'chapter-{chapter:02d}-*.md'))
    assert h and m, f'missing Chapter {chapter} HTML/MD'
    doc=BeautifulSoup(h[0].read_text(encoding='utf-8'),'html.parser')
    broken=[]
    for elem in doc.find_all(['a','img']):
        target=elem.get('href') or elem.get('src') or ''
        if not target or target.startswith(('http://','https://','#','mailto:','data:','javascript:')):continue
        target=target.split('#')[0].split('?')[0]
        if not target:continue
        if not (ROOT/target).is_file():broken.append(target)
    assert not broken,f'Chapter {chapter} broken relative refs: {broken[:7]}'
print('PASS: chapters 01–04 HTML/MD exist and all linked local HTML/SVG assets resolve')
lab=ROOT/'labs/chapter-04'
for file in ['README.md','schema.sql','queries.sql','test-scenarios.md']:
    assert (lab/file).stat().st_size>500, f'lab missing/empty: {file}'
assert 'CHECK (reserved_uses + consumed_uses <= usage_limit)' in (lab/'schema.sql').read_text()
assert 'UNIQUE (buyer_id, checkout_request_key)' in (lab/'schema.sql').read_text()
print('PASS: lab files present; quota and checkout idempotency SQL constraints included (static review only)')
gross=Decimal(500000)*2
line_discount=gross*Decimal('0.1')
total=gross-line_discount-Decimal(50000)+Decimal(30000)
assert total==Decimal(880000)
assert sum([3334,3333,3333])==10000
print('PASS: illustrative monetary calculation and residual discount allocation')
assert (ROOT/'index.html').read_text(encoding='utf-8').count('chapter-04-product-pricing.html')==1
print('PASS: Volume 1 index contains Chapter 04')
