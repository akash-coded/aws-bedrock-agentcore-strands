#!/usr/bin/env python3
"""Render every mermaid diagram the way readers will see it, and fail on what a reader would notice.

    python3 site/tools/check_diagrams.py            # lessons and wiki pages
    python3 site/tools/check_diagrams.py --only site/content/learn/lessons/p0-frame.md

Local only: it needs Google Chrome and network access to the pinned mermaid build. CI does not run it.

Each diagram is drawn with mermaid's ``dark`` and ``default`` themes — GitHub picks one per reader —
at the width of GitHub's wiki column, and four things are asserted:

* it renders at all;
* no label is smaller than 11px once the drawing is scaled to fit the column;
* every node border clears 3:1 against the surface it sits on, and every label 4.5:1 against its own
  fill — with alpha composited, and with the surface found by geometry, because a cluster is a
  *sibling* of the nodes inside it, not their parent;
* in a banded diagram, the bands come out in the order they were declared — a back edge makes a
  cycle that dagre breaks by reversing a forward edge, which silently reorders the phases.

Two more are reported as warnings, because they hurt reading without breaking it:

* a label line that mermaid wrapped — it wraps any line wider than about 200px, so a subtitle breaks
  mid-phrase and the node grows a line; counted by comparing rendered lines with written ``<br/>`` lines;
* a drawing wider than 720px, which the README asks authors to avoid: it fits the wiki column but
  shrinks below legibility on a phone.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.esm.min.mjs"
COLUMN = 896          # GitHub's wiki content width at a 1440px window
MIN_TEXT = 11.0
WIDE = 720            # px of drawing before a phone shrinks its text below legibility
FENCE = re.compile(r"```mermaid\n([\s\S]*?)```")

JS = r"""
import mermaid from "%MERMAID%";
const P = new URLSearchParams(location.search);
const THEME = P.get("t");
mermaid.initialize({startOnLoad:false, theme:THEME, flowchart:{htmlLabels:true, curve:"basis"}});
const names = {}, fails = [];
for (const el of document.querySelectorAll("pre.mermaid")) {
  names[el.id + "-svg"] = el.dataset.src;
  try { const {svg} = await mermaid.render(el.id + "-svg", el.textContent);
        el.outerHTML = '<div class="mermaid">' + svg + '</div>'; }
  catch (e) { fails.push(el.dataset.src + ": " + (e && e.message || e)); el.remove(); }
}
const probe = document.createElement("span"); probe.style.display = "none"; document.body.appendChild(probe);
function rgba(c) { if (!c || c === "none") return null; probe.style.color = ""; probe.style.color = c;
  const m = getComputedStyle(probe).color.match(/[\d.]+/g); if (!m) return null;
  return [+m[0], +m[1], +m[2], m.length > 3 ? +m[3] : 1]; }
const over = (f, b) => f ? [0,1,2].map(i => f[i]*f[3] + b[i]*(1-f[3])).concat([1]) : b.slice();
const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); };
  return .2126*f(c[0]) + .7152*f(c[1]) + .0722*f(c[2]); };
const ratio = (a, b) => { const L1 = lum(a), L2 = lum(b); return +((Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05)).toFixed(2); };
const page = rgba(getComputedStyle(document.body).backgroundColor);
const out = [];
for (const s of document.querySelectorAll("div.mermaid svg")) {
  const vb = s.viewBox.baseVal, r = s.getBoundingClientRect(), k = r.width / vb.width;
  const base = over(rgba(getComputedStyle(s).backgroundColor), page);
  const clusters = [...s.querySelectorAll("g.cluster")].map(c => {
    const rr = c.querySelector("rect");
    return {t: c.textContent.trim().split("\n")[0], box: c.getBoundingClientRect(),
            fill: rr ? rgba(getComputedStyle(rr).fill) : null}; });
  let minText = 99, badStroke = [], badLabel = [];
  for (const t of s.querySelectorAll("text, span, p, div.nodeLabel")) {
    const fs = parseFloat(getComputedStyle(t).fontSize);
    if (t.textContent.trim() && fs) minText = Math.min(minText, fs * k); }
  for (const n of s.querySelectorAll("g.node")) {
    const shape = n.querySelector("rect, polygon, path"); if (!shape) continue;
    const cs = getComputedStyle(shape), nb = n.getBoundingClientRect();
    const cx = nb.left + nb.width/2, cy = nb.top + nb.height/2;
    let surface = base;
    for (const c of clusters)
      if (cx >= c.box.left && cx <= c.box.right && cy >= c.box.top && cy <= c.box.bottom) surface = over(c.fill, base);
    const fill = over(rgba(cs.fill), surface);
    const stroke = rgba(cs.stroke);
    if (stroke && stroke[3] > 0) {
      const sr = ratio(over(stroke, surface), surface);
      if (sr < 3) badStroke.push(cs.stroke + " " + sr); }
    const lab = n.querySelector(".nodeLabel, span, p");
    if (lab && lab.textContent.trim()) {
      const lr = ratio(over(rgba(getComputedStyle(lab).color), fill), fill);
      if (lr < 4.5) badLabel.push(lab.textContent.trim().slice(0, 30) + " " + lr); }
  }
  const wrapped = [];
  for (const div of s.querySelectorAll("g.node foreignObject div, g.cluster foreignObject div")) {
    const text = div.textContent.trim(); if (!text) continue;
    const range = document.createRange(); range.selectNodeContents(div);
    const tops = [...range.getClientRects()].filter(q => q.width > 0).map(q => q.top).sort((a, b) => a - b);
    let lines = 0, last = -1e9;
    for (const t of tops) if (t - last > 4 * k) { lines++; last = t; }
    const written = (div.innerHTML.match(/<br\s*\/?>/gi) || []).length + 1;
    if (lines > written) wrapped.push(div.innerText.trim().replace(/\s*\n\s*/g, " / ").slice(0, 60));
  }
  const xs = clusters.map(c => c.box.left), ys = clusters.map(c => c.box.top);
  const axis = clusters.length > 1 && (Math.max(...xs) - Math.min(...xs)) > (Math.max(...ys) - Math.min(...ys)) ? "x" : "y";
  const drawn = clusters.slice().sort((a, b) => axis === "x" ? a.box.left - b.box.left : a.box.top - b.box.top).map(c => c.t);
  out.push({src: names[s.id], width: Math.round(vb.width), minText: +minText.toFixed(1),
            badStroke, badLabel, drawn, wrapped});
}
const tag = document.createElement("script"); tag.type = "application/json"; tag.id = "report";
tag.textContent = JSON.stringify({fails, out}); document.body.appendChild(tag);
"""


def collect(paths: list[Path]) -> list[tuple[str, str, list[str]]]:
    """(label, source, declared band titles) for every mermaid block."""
    out = []
    for p in paths:
        for i, m in enumerate(FENCE.finditer(p.read_text(encoding="utf-8"))):
            src = m.group(1)
            bands = re.findall(r'^\s*subgraph\s+\w+\["([^"]+)"\]', src, re.M)
            out.append((f"{p.relative_to(ROOT)}#{i}", src, bands))
    return out


def run(figs, theme: str, bg: str, tmp: Path) -> dict:
    cards = "\n".join(f'<pre class="mermaid" id="g{i}" data-src="{html.escape(n)}">{html.escape(s)}</pre>'
                      for i, (n, s, _) in enumerate(figs))
    page = (f'<!doctype html><meta charset="utf-8"><body style="background:{bg};margin:0">'
            f'<main style="width:{COLUMN}px">{cards}</main>'
            f'<script type="module">{JS.replace("%MERMAID%", MERMAID)}</script></body>')
    f = tmp / f"sheet-{theme}.html"
    f.write_text(page, encoding="utf-8")
    dom = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--virtual-time-budget=60000",
                          "--dump-dom", f"file://{f}?t={theme}"], capture_output=True, text=True, timeout=240)
    m = re.search(r'id="report">([\s\S]*?)</script>', dom.stdout)
    if not m:
        sys.exit(f"{theme}: the harness produced no report — is the mermaid CDN reachable?")
    return json.loads(m.group(1))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", nargs="*", help="check just these markdown files")
    a = ap.parse_args()
    if not Path(CHROME).exists():
        print("check_diagrams: Google Chrome not found; skipping")
        return 0
    paths = ([ROOT / p for p in a.only] if a.only else
             sorted((ROOT / "site/content/learn/lessons").glob("*.md")) + [ROOT / "site/content/learn/start-here.md"]
             + sorted((ROOT / "wiki").glob("*.md")))
    figs = collect(paths)
    declared = {n: b for n, _, b in figs}
    tmp = Path(tempfile.mkdtemp(prefix="diagrams-"))
    problems, warnings = [], []
    try:
        for theme, bg in (("dark", "#0d1117"), ("default", "#ffffff")):
            rep = run(figs, theme, bg, tmp)
            problems += [f"[{theme}] does not render: {f}" for f in rep["fails"]]
            for d in rep["out"]:
                if d["minText"] < MIN_TEXT:
                    problems.append(f"[{theme}] {d['src']}: smallest label {d['minText']}px at {COLUMN}px "
                                    f"(drawing is {d['width']}px wide)")
                for s in d["badStroke"][:3]:
                    problems.append(f"[{theme}] {d['src']}: node border {s}:1 against its surface")
                for s in d["badLabel"][:3]:
                    problems.append(f"[{theme}] {d['src']}: label '{s}':1 against its fill")
                if theme == "default":
                    warnings += [f"{d['src']}: wraps '{w}'" for w in d["wrapped"]]
                    if d["width"] > WIDE:
                        warnings.append(f"{d['src']}: {d['width']}px wide; keep under {WIDE}px for phones")
                want = declared.get(d["src"]) or []
                if len(want) > 1 and d["drawn"][: len(want)] != want:
                    problems.append(f"[{theme}] {d['src']}: bands drawn {d['drawn']} but declared {want}")
            print(f"{theme:>8}: {len(rep['out'])} of {len(figs)} diagrams rendered")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for w in warnings:
        print("  ⚠", w)
    for p in problems:
        print("  ✗", p)
    print(f"{len(figs)} diagrams, {len(problems)} problems, {len(warnings)} warnings")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
