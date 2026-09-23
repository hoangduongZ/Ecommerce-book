# Chapter 05 — Order Lifecycle

- Source of truth: `chapter-05-order-lifecycle.md` (20 technical sections).
- Offline reader: `chapter-05-order-lifecycle.html` (TOC, search by headings, theme toggle, Mermaid source, SVG illustrations).
- Illustrations: `assets/chapter-05/diagram-01.svg` through `diagram-16.svg`.
- PostgreSQL lab: `labs/chapter-05/` (schema, seed, queries, concurrency and crash exercises).
- Rebuild chapter HTML/SVG: `python tools/build_chapter05.py` with Python `mistune`, `beautifulsoup4`, and Graphviz `dot` installed.
- SQL examples reflect a deliberately narrow prepaid lab model; do not equate payment gateway timeout to payment failure.
- SQL **not integration-tested on a running PostgreSQL instance** in this delivery environment.
