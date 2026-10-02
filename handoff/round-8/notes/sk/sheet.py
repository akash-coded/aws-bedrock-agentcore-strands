"""sheet.py <out-name> [filter ...]: render the sketches whose lesson slug or name contains a filter to
scratchpad/sk/<out-name>.html, each at 760px (a lesson column) and at 320px (a phone), with any rule it breaks in red."""
import sys, zlib
sys.path.insert(0, "site")
from pathlib import Path
from pages import learn, sketch
out_name, want = sys.argv[1], sys.argv[2:]
HERE = Path(__file__).resolve().parent
cells = []
for name, spec in learn.sketches().items():
    if want and not any(w in spec["lesson"] or w in name for w in want):
        continue
    html, sk = sketch.render(spec)
    probs = sketch.lint(spec, sk, html)
    size = len(zlib.compress(html.encode(), 9))
    cells.append(f'<div class="cell"><p class="n">{spec["lesson"]} · {name} · {size}B gz · {len(sk.words)} labels'
                 f'{" · <b style=color:#f66>" + "; ".join(probs) + "</b>" if probs else ""}</p>{html}</div>')
CSS = Path("site/theme/base.css").read_text().replace(
    "../assets/", "file://site/assets/")
page = f"""<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style>
<style>body{{padding:24px;display:grid;grid-template-columns:760px 320px;gap:24px 40px;align-items:start}}
.cell{{display:contents}}.n{{grid-column:1/-1;font:12px var(--f-mono);color:var(--soft);margin:0}}
.cell figure{{margin:0}}</style></head><body>
{"".join(cells)}
<script>document.querySelectorAll('.cell').forEach(c=>{{const f=c.querySelector('figure');c.appendChild(f.cloneNode(true))}})</script>
</body></html>"""
(HERE / f"{out_name}.html").write_text(page)
print(len(cells), "sketches ->", HERE / f"{out_name}.html")
