#!/usr/bin/env python3
"""Generate Chapter 05 offline HTML and Graphviz SVG from the Markdown master.
Dependencies: mistune, beautifulsoup4, Graphviz (dot).
Mermaid remains the canonical editable diagram description; SVG is offline visual companion.
"""
from __future__ import annotations
import re, html, subprocess, textwrap
from pathlib import Path
from collections import OrderedDict
from bs4 import BeautifulSoup
import mistune

ROOT = Path(__file__).resolve().parents[1]
SLUG='chapter-05-order-lifecycle'
MD=ROOT / f'{SLUG}.md'
OUT=ROOT / f'{SLUG}.html'
ASSETS=ROOT / 'assets' / 'chapter-05'
ASSETS.mkdir(parents=True, exist_ok=True)
text=MD.read_text(encoding='utf-8')
fm=re.match(r'^---\n.*?\n---\n',text,re.S)
if fm: text=text[fm.end():]
blocks=re.findall(r'```mermaid\n(.*?)\n```', text, flags=re.S)

DOT_THEME='''graph [bgcolor="transparent", pad="0.26", nodesep="0.42", ranksep="0.65", splines=polyline];
node [shape=box, style="rounded,filled", fillcolor="#eef6ff", color="#a4c4e2", fontcolor="#17324b", fontname="Noto Sans", fontsize=12, margin="0.22,0.14"];
edge [color="#7093b6", arrowsize=0.8, penwidth=1.6, fontname="Noto Sans", fontcolor="#56718a", fontsize=10];'''

def node_id(s):
    m=re.match(r'\s*([A-Za-z_][A-Za-z_0-9]*)',s)
    return m.group(1) if m else None

def label_clean(s):
    s=s.strip().strip('"').strip("'")
    if s.startswith('(') and s.endswith(')'): s=s[1:-1]
    return s.strip().strip('"')

def gquote(s): return '"'+s.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')+'"'

def wrap(s, width=30):
    return '\\n'.join(textwrap.wrap(s,width=width,break_long_words=False,break_on_hyphens=False))

def graph_from_mermaid(src, idx):
    lines=[x.strip() for x in src.splitlines() if x.strip()]
    kind=lines[0].split()[0]
    if kind=='sequenceDiagram':
        return render_sequence(lines[1:],idx)
    rank='LR' if kind=='flowchart' and lines[0].endswith('LR') else 'TB'
    nodes=OrderedDict(); edges=[]
    if kind=='stateDiagram-v2':
        for l in lines[1:]:
            m=re.match(r'(\[\*\]|[A-Z_]+)\s*-->\s*([A-Z_]+)(?::\s*(.*))?',l)
            if not m:continue
            left='START' if m.group(1)=='[*]' else m.group(1)
            right=m.group(2)
            nodes[left]='Start' if left=='START' else left.replace('_',' ').title()
            nodes[right]=right.replace('_',' ').title()
            edges.append((left,right,m.group(3) or ''))
    elif kind=='erDiagram':
        for l in lines[1:]:
            m=re.match(r'([A-Z_]+)\s+(\S+)\s+([A-Z_]+)\s*:\s*(.*)',l)
            if not m: continue
            left,card,right,rel=m.groups();nodes[left]=left.replace('_',' ').title();nodes[right]=right.replace('_',' ').title()
            card_label='1:N' if 'o{' in card or '|{' in card else ('1:0..1' if 'o|' in card else '1:1')
            edges.append((left,right,rel+' ('+card_label+')'))
    else:
        pat=r'\b([A-Za-z_][A-Za-z_0-9]*)\[([^\]]+)\]'
        for l in lines[1:]:
            for m in re.finditer(pat,l): nodes[m.group(1)]=label_clean(m.group(2))
        for l in lines[1:]:
            if l.startswith('subgraph ') or l=='end' or l.startswith('flowchart'):continue
            ln=re.sub(pat,lambda m:m.group(1),l)
            # Arrow label forms: -->|"Event"|, -. "sellerId" .->, or -.->
            e_label=''
            ml=re.search(r'\|\s*"?([^"|]+)"?\s*\|',ln)
            if ml:e_label=ml.group(1).strip();ln=ln.replace(ml.group(0),'')
            ml=re.search(r'\-\.\s*"([^"]+)"\s*\.\->',ln)
            if ml:e_label=ml.group(1);ln=ln.replace(ml.group(0),' --> ')
            if '-->' in ln or '-.->' in ln or '.->' in ln:
                tokens=re.split(r'\s*(?:-->|-\.->|\.->)\s*',ln)
                ids=[node_id(t) for t in tokens]
                for a,b in zip(ids,ids[1:]):
                    if a and b:
                        nodes.setdefault(a,a);nodes.setdefault(b,b)
                        edges.append((a,b,e_label))
    dot=['digraph G {', f'graph [rankdir={rank}];',DOT_THEME]
    for k,lbl in nodes.items():
        extra=' fillcolor="#dcfce7" color="#7ec99d"' if any(w in lbl.lower() for w in ['payment','postgres','inventory','stock','database']) else ''
        dot.append(f'{k} [label={gquote(wrap(lbl))}{extra}];')
    for a,b,lbl in edges:
        dot.append(f'{a} -> {b}'+ (f' [label={gquote(lbl)}]' if lbl else '') + ';')
    dot.append('}')
    d='\n'.join(dot)
    try:
        subprocess.run(['dot','-Tsvg','-o',str(ASSETS/f'diagram-{idx:02d}.svg')],input=d,text=True,check=True,capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('dot failed for diagram '+str(idx)+'\n'+e.stderr+'\n'+d)

def render_sequence(lines,idx):
    participants=OrderedDict(); messages=[]
    for l in lines:
        m=re.match(r'participant\s+(\w+)\s+as\s+(.+)',l)
        if m: participants[m.group(1)]=m.group(2)
        m=re.match(r'(\w+)\s*(-+>>?)\s*(\w+)\s*:\s*(.*)',l)
        if m:
            a,arrow,b,msg=m.groups();participants.setdefault(a,a);participants.setdefault(b,b);messages.append((a,b,msg,arrow))
    ids=list(participants); gap=190 if len(ids)>4 else 230
    w=150+(len(ids)-1)*gap+150; h=115+len(messages)*67+45
    x={k:110+i*gap for i,k in enumerate(ids)}
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
         '<defs><marker id="a" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#487ca7" stroke-width="1.5"/></marker></defs>',
         f'<rect width="{w}" height="{h}" rx="16" fill="#f6faff"/>']
    for k,label in participants.items():
        xx=x[k];out+=[f'<rect x="{xx-82}" y="20" width="164" height="44" rx="10" fill="#e5f0ff" stroke="#8db6db"/>',
                    f'<text x="{xx}" y="47" text-anchor="middle" font-family="Noto Sans, sans-serif" font-size="13" fill="#193b57">{html.escape(label)}</text>',
                    f'<line x1="{xx}" x2="{xx}" y1="67" y2="{h-20}" stroke="#bad0e2" stroke-dasharray="6 5"/>']
    for i,(a,b,msg,arr) in enumerate(messages):
        y=100+i*67
        xa,xb=x[a],x[b]
        if xa==xb:
            out.append(f'<path d="M{xa} {y} h45 v24 h-45" fill="none" stroke="#487ca7" stroke-width="1.7" marker-end="url(#a)"/>')
        else:
            out.append(f'<line x1="{xa}" y1="{y}" x2="{xb}" y2="{y}" stroke="#487ca7" stroke-width="1.7" {"stroke-dasharray=\"5 4\"" if arr.startswith("--") else ""} marker-end="url(#a)"/>')
        xpos=(xa+xb)/2 if xa!=xb else xa+30
        out.append(f'<text x="{xpos}" y="{y-9}" text-anchor="middle" font-family="Noto Sans, sans-serif" font-size="12" fill="#274760">{html.escape(msg[:76])}</text>')
    out.append('</svg>')
    (ASSETS/f'diagram-{idx:02d}.svg').write_text('\n'.join(out),encoding='utf-8')

for i,source in enumerate(blocks,1): graph_from_mermaid(source,i)

md=mistune.create_markdown(renderer='html',plugins=['table','strikethrough','url'])
body=md(text)
soup=BeautifulSoup(body,'html.parser')
headings=[]
for h in soup.find_all(['h1','h2','h3']):
    slug=re.sub(r'[^a-z0-9]+','-',h.get_text(' ',strip=True).lower().replace('đ','d')).strip('-')
    base=slug;n=2
    while slug in {s for _,s,_ in headings}:slug=f'{base}-{n}';n+=1
    h['id']=slug
    headings.append((h.name,slug,h.get_text(' ',strip=True)))
codeblocks=[p for p in soup.find_all('pre') if p.code and 'language-mermaid' in p.code.get('class',[])]
for i,p in enumerate(codeblocks,1):
    source=p.code.get_text()
    figure=soup.new_tag('figure',**{'class':'diagram'})
    a=soup.new_tag('a',href=f'assets/chapter-05/diagram-{i:02d}.svg',target='_blank',rel='noopener noreferrer',title='Mở sơ đồ SVG')
    img=soup.new_tag('img',src=f'assets/chapter-05/diagram-{i:02d}.svg',alt=f'Sơ đồ kỹ thuật {i:02d}',loading='lazy')
    a.append(img);figure.append(a)
    cap=soup.new_tag('figcaption');cap.append(BeautifulSoup(f'<strong>Sơ đồ {i:02d}</strong> · SVG đọc offline · ', 'html.parser'))
    details=soup.new_tag('details');summ=soup.new_tag('summary');summ.string='Xem / sao chép Mermaid';details.append(summ)
    pre=soup.new_tag('pre');pre.string=source;details.append(pre);cap.append(details);figure.append(cap)
    p.replace_with(figure)

nav=[]
for kind,slug,label in headings:
    if kind=='h1':continue
    nav.append(f'<a class="{kind}" href="#{html.escape(slug)}">{html.escape(label)}</a>')
nav='\n'.join(nav)
css='''
:root{--bg:#edf3f8;--paper:#fff;--ink:#172f44;--muted:#597186;--accent:#17609e;--line:#d5e1eb;--nav:#142b3f;--code:#112638;--codeink:#e8f6ff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--bg);font:16px/1.78 "Noto Sans",system-ui,sans-serif}
nav{position:fixed;inset:0 auto 0 0;width:308px;background:var(--nav);padding:28px 18px 48px;overflow-y:auto;box-shadow:2px 0 20px #0d26361a;z-index:10}
nav strong{color:#fff;display:block;letter-spacing:.12em;font-size:13px;margin:4px 10px}nav small{display:block;margin:8px 10px 20px;color:#b9d1df;line-height:1.7}
nav input{width:100%;border-radius:9px;padding:10px 11px;border:1px solid #42617a;background:#1d3b53;color:white;margin-bottom:13px}nav input::placeholder{color:#a9c2d5}
nav a{display:block;color:#c6d9e7;text-decoration:none;line-height:1.5;font-size:12px;padding:7px 10px;border-radius:7px}nav a:hover,nav a.active{background:#244b68;color:white}nav a.h2{font-weight:700;color:#ecf6fe;margin-top:4px}nav a.h3{padding-left:22px;font-size:11px}
nav .back{margin:5px 0 16px;border-bottom:1px solid #476174;padding-bottom:12px}
main{margin-left:308px;padding:40px 34px 90px}article{max-width:1000px;margin:auto;background:var(--paper);padding:60px 66px;border:1px solid var(--line);border-radius:16px;box-shadow:0 17px 48px #2a4b6e12}
.eyebrow{letter-spacing:.14em;font-weight:800;color:var(--accent);font-size:12px}h1,h2,h3,h4{line-height:1.3;scroll-margin-top:24px}h1{font-size:36px;color:#163f60;margin:8px 0 14px}h2{font-size:25px;border-bottom:1px solid var(--line);padding-bottom:12px;margin:52px 0 20px}h3{font-size:19px;color:#1c5987;margin:30px 0 12px}p{margin:13px 0}blockquote{margin:22px 0;background:#eef6ff;border-left:4px solid #4189bd;padding:10px 21px;border-radius:0 10px 10px 0}blockquote p{margin:7px 0}
a{color:#126aa3}a:hover{text-decoration:none}code{font:13px/1.5 ui-monospace,Consolas,monospace;background:#eef3f8;padding:2px 5px;border-radius:4px}pre{overflow:auto;background:var(--code);color:var(--codeink);padding:21px;border-radius:11px;line-height:1.58;font-size:13px}pre code{padding:0;background:none;color:inherit;font-size:inherit}
.table-wrap{overflow-x:auto;margin:20px 0}table{border-collapse:collapse;width:100%;font-size:14px;min-width:560px}th{background:#e9f3fa;text-align:left}th,td{border:1px solid #d4e2ea;padding:10px 13px;vertical-align:top}tr:nth-child(even) td{background:#f7fafc}hr{border:0;border-top:1px solid var(--line);margin:38px 0}
.diagram{margin:22px 0;padding:15px;background:#f6faff;border:1px solid #d9e5f0;border-radius:11px;text-align:center;overflow:hidden}.diagram img{max-width:100%;height:auto;min-width: min(280px,100%)}.diagram figcaption{text-align:left;font-size:12px;color:#42607a;padding:11px 5px 0}.diagram details{display:inline-block}.diagram summary{cursor:pointer;color:#13659e;font-weight:700}.diagram pre{text-align:left;max-height:290px;font-size:11px;white-space:pre-wrap}
.toolbar{position:fixed;right:24px;top:15px;z-index:8;display:flex;gap:8px}.toolbar button,.mobile-toggle{background:#17609e;color:white;border:0;border-radius:8px;padding:9px 13px;cursor:pointer}.mobile-toggle{display:none;position:fixed;bottom:18px;right:18px;z-index:11}
#progress{position:fixed;left:0;top:0;height:4px;background:#22a1bc;width:0;z-index:12}footer{color:#728698;text-align:center;font-size:13px;margin-top:30px}
body.dark{--bg:#071522;--paper:#10263a;--ink:#dbe9f4;--muted:#9bb5c8;--accent:#8dcaff;--line:#30485a;--code:#06131e;--codeink:#e9f5ff}
body.dark h1,body.dark h3{color:#a9d9fa}body.dark h2{color:#dbe9f4}body.dark th{background:#203e55}body.dark tr:nth-child(even) td{background:#162f43}body.dark blockquote{background:#1a3a52}body.dark .diagram{background:#f2f7fd}body.dark code{background:#28445b;color:#e9f5ff}body.dark pre code{background:none}
@media(max-width:1000px){nav{transform:translateX(-103%);transition:transform .25s}body.nav-open nav{transform:translateX(0)}main{margin:0;padding:20px 10px 65px}article{padding:40px 26px}.mobile-toggle{display:block}}
@media(max-width:600px){article{padding:27px 17px}h1{font-size:28px}h2{font-size:22px}body{font-size:15px}.toolbar{right:12px;top:9px}.toolbar button{font-size:11px}}
@media print{nav,.toolbar,.mobile-toggle,#progress{display:none}main{padding:0;margin:0}article{max-width:none;border:0;box-shadow:none;padding:0}h2,h3{break-after:avoid}.diagram{break-inside:avoid}body{background:white;color:black}a{color:inherit}}
'''
js='''
const nav=document.querySelector('nav');
document.getElementById('search').addEventListener('input',e=>{
 const s=e.target.value.trim().toLocaleLowerCase('vi');
 nav.querySelectorAll('a.h2,a.h3').forEach(x=>x.style.display=x.textContent.toLocaleLowerCase('vi').includes(s)?'block':'none');
});
document.getElementById('mobile').onclick=()=>document.body.classList.toggle('nav-open');
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>document.body.classList.remove('nav-open')));
document.getElementById('theme').onclick=()=>{document.body.classList.toggle('dark');document.getElementById('theme').textContent=document.body.classList.contains('dark')?'☀ Sáng':'☾ Tối';};
window.addEventListener('scroll',()=>{let d=document.documentElement;let max=d.scrollHeight-d.clientHeight;document.getElementById('progress').style.width=(max?100*d.scrollTop/max:0)+'%';},{passive:true});
const obs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){nav.querySelectorAll('a.active').forEach(x=>x.classList.remove('active'));let a=nav.querySelector('a[href="#'+e.target.id+'"]');if(a)a.classList.add('active');}}),{rootMargin:'-16% 0px -73% 0px'});
document.querySelectorAll('article h2[id],article h3[id]').forEach(h=>obs.observe(h));
'''
page=f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>Inside E-commerce · Chương 05 — Order Lifecycle</title><style>{css}</style></head><body>
<div id="progress"></div><nav><strong>INSIDE E-COMMERCE</strong><small>Volume 1 — Understanding E-commerce<br>Chapter 05 · Order Lifecycle</small>
<a class="back" href="chapter-04-product-pricing.html">← Chương 04: Product & Pricing</a>
<input id="search" placeholder="Tìm tiêu đề trong chương…" aria-label="Tìm trong mục lục">{nav}</nav>
<div class="toolbar"><button id="theme" type="button">☾ Tối</button><button onclick="window.print()" type="button">⎙ In / Save PDF</button></div><button id="mobile" class="mobile-toggle">☰ Mục lục</button>
<main><article><div class="eyebrow">BACKEND ENGINEERING · SYSTEM DESIGN · ORDER LIFECYCLE</div>{str(soup)}</article><footer>Inside E-commerce · Volume 1 · Chapter 05 · Offline edition</footer></main>
<script>{js}</script></body></html>'''
OUT.write_text(page,encoding='utf-8')
print('Chapter:',MD.name,'Mermaid:',len(blocks),'SVG:',len(list(ASSETS.glob('*.svg'))),'HTML bytes:',OUT.stat().st_size)
