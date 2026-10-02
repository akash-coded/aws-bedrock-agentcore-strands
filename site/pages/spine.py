"""The home page's methods band: how AI-DLC, BMAD and the rest fit together (verdict-home 1.2).

:func:`methods_band` builds the band: its heading, its line, the method map and two links. The map draws the
SkyWays PDLC as a frame with its four phases across the top. Inside it each method is a soft shape as long as
the phases it covers, so every overlap is true: all five meet in the build. A handwritten note beside each says
who made it and when. Under the shapes is the row no method reaches: the question each phase asks, and what a
team hears when it was skipped.

It is a CSS grid, not a drawing: every word is real text and nothing scales. The shapes are a list of links,
and each link says in words what its shape shows, from the same ``reach`` that places the shape and draws the
phone's strip. The frame, the wash, the arrows and the ends are hidden from a screen reader. The parts that
only make sense laid out (the ends, the margin notes, the pills on the sign-off) also carry ``hidden``, which
the stylesheet overrides, so a page read without its stylesheet is a legend, four phase links, a list of five
methods with a sentence each, and the four questions.

Everything on the map comes from ``content/library/frameworks.json`` (the four ``methods``, the ``names`` a
reader meets that are not methods a team adopts, and the ``pdlc``), checked here each time the page is built:
every note carries the addresses it was read at, the words it rests on, and the day they were read.
"""
from __future__ import annotations

import json
import re
from datetime import date
from html import escape as _E
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "content" / "library" / "frameworks.json"
# How far a shape reaches into each phase: 2 covers it, 1 a sketch or an update at that end (its words in "ends"),
# 0 none, "x" a stage this manual adds to the method (extended BMAD).
ADDED = "added in this manual"
SHAPES = 5                  # base.css lays the map out for five shapes: four methods and the agentic SDLC
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")
NUMBER = {3: "three", 4: "four", 5: "five", 6: "six"}
# The two hand-drawn arrows: one points back at what it names, one points up at the build. Every small drawing on
# the map carries its size and its pen as attributes, in the colour of the words beside it, so it needs no rule of
# its own and stays small on a page read without its stylesheet.
PEN = 'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"'
ARROW = (f'<svg viewBox="0 0 30 14" width="28" height="14" {PEN}>'
         '<path d="M29 8.5C21 10.5 11 9.6 3 6.2M3 6.2 9.4 2.2M3 6.2l5.6 5.3"/></svg>')
ARROW_UP = (f'<svg viewBox="0 0 14 30" width="14" height="20" {PEN}>'
            '<path d="M7.5 29C9 21 8.2 11 5.6 3M5.6 3 2 9.2M5.6 3l5 5.6"/></svg>')


def _reach_ok(r) -> bool:
    return (isinstance(r, list) and len(r) == 4
            and all(x == "x" or (type(x) is int and x in (0, 1, 2)) for x in r))


def check(d: dict) -> list[str]:
    """What the map's data must keep to. An empty list is a pass."""
    err = []
    entries = ([("pdlc", d.get("pdlc"))] + [(f"methods[{i}]", m) for i, m in enumerate(d.get("methods", []))]
               + [(f"names[{i}]", m) for i, m in enumerate(d.get("names", []))])
    for where, m in entries:
        if not isinstance(m, dict):
            err.append(f"{where} is missing")
            continue
        s = m.get("title") or where
        for k in ("title", "lesson", "note", "note_source", "checked"):
            if not m.get(k):
                err.append(f"{s}: no {k}")
        sources = m.get("note_source") or []
        if not isinstance(sources, list):
            err.append(f"{s}: note_source is a list of sources, each an address and the words the note rests on")
            sources = []
        for src in sources:
            if not str(src.get("url", "")).startswith("https://"):
                err.append(f"{s}: a note's source is the https address it was read at")
            if not src.get("quotes"):
                err.append(f"{s}: a source carries the words the note rests on, exactly as the page has them")
        try:
            if date.fromisoformat(str(m.get("checked"))) > date.today():
                err.append(f"{s}: checked on a day that has not happened")
        except ValueError:
            err.append(f"{s}: checked is the day the sources were read, written 2026-10-03")
        # a day only where a source gives one: "31 July 2025" needs a source that says 31, July and 2025
        said = " ".join(q for src in sources for q in src.get("quotes", [])).lower()
        for day, month, year in re.findall(rf"\b(\d{{1,2}}) ({'|'.join(MONTHS)}) (\d{{4}})\b", m.get("note", "")):
            if not (re.search(rf"\b{day}\b", said) and month[:3].lower() in said and year in said):
                err.append(f"{s}: the note gives a day, {day} {month} {year}, that no source gives")
        if where == "pdlc":
            continue
        r = m.get("reach")
        if not _reach_ok(r):
            err.append(f"{s}: reach is four values, each 0, 1, 2 or \"x\"")
            continue
        cov = [i for i, x in enumerate(r) if x == 2]
        if not cov or cov != list(range(cov[0], cov[-1] + 1)):
            err.append(f"{s}: a shape is one span: the phases it covers (2) run without a gap")
            continue
        if any(x in (1, "x") and i not in (cov[0] - 1, cov[-1] + 1) for i, x in enumerate(r)):
            err.append(f"{s}: a sketch, an update (1) or an added stage (\"x\") sits at an end of the span")
        if len(m.get("ends") or []) != r.count(1):
            err.append(f"{s}: ends gives the words drawn in each phase the shape touches (1), in order")
    if not err and len(shapes(d)) != SHAPES:
        err.append(f"the map is laid out for {SHAPES} shapes (base.css, block H3); the data has {len(shapes(d))}")
    return err


def load() -> dict:
    """The map's data, checked: the build stops on a note without its source or date, or a reach it cannot draw."""
    d = json.loads(DATA.read_text(encoding="utf-8"))
    err = check(d)
    if err:
        raise SystemExit("frameworks.json, the method map's data:\n  " + "\n  ".join(err))
    return d


def shapes(d: dict) -> list[dict]:
    """The methods and the names, widest reach first: most phases covered, then most phases touched."""
    every = d["methods"] + d.get("names", [])
    return sorted(every, key=lambda m: (-m["reach"].count(2), -sum(1 for x in m["reach"] if x)))


def reading(m: dict, phases: list[str]) -> str:
    """What a shape shows, as a sentence, from the same reach that draws it: "covers Frame to Build and Prove;
    this manual adds Run and Learn"."""
    r = m["reach"]
    cov = [i for i, x in enumerate(r) if x == 2]
    s = ("covers all four phases" if len(cov) == 4 else f"covers {phases[cov[0]]}" if len(cov) == 1
         else f"covers {phases[cov[0]]} to {phases[cov[-1]]}")
    touched = [i for i, x in enumerate(r) if x == 1]
    if touched:
        # the ends' words are nouns as drawn ("spec sketch", "spec updates"); a singular one takes "a"
        s += ", with " + " and ".join(f"{'' if w.endswith('s') else 'a '}{w} in {phases[i]}"
                                      for w, i in zip(m["ends"], touched))
    added = [phases[i] for i, x in enumerate(r) if x == "x"]
    if added:
        s += "; this manual adds " + " and ".join(added)
    return s


def _craft(i: int) -> str:
    """The form the hero's flight takes in phase ``i``: a dart, then a drawing (dashed), then the airliner built,
    then the jet. The column head draws it in the phase's hue (verdict-home 1.1 and 1.2)."""
    from pages import globe
    shape, look = globe.CRAFT[i]
    pen = PEN.replace('fill="none"', 'fill="currentColor"') if look == "built" else PEN
    if (shape, look) == ("liner", "drawn"):
        pen = 'stroke-dasharray="3.4 2.4" ' + pen          # a drawing: the airliner in dashes
    return f'<svg viewBox="-20 -15 40 30" width="30" height="20" {pen}><path d="{globe.SHAPES[shape]}"/></svg>'


def methods_band() -> str:
    """The home page's second band (verdict-home 1.2). The phases, their questions and the line each skipped
    question leaves are render's (render.PHASES, render.SKIPPED); the methods and their notes are the data's."""
    import render
    d = load()
    pdlc, every = d["pdlc"], shapes(d)
    spoken = [name.replace("&amp;", "and") for _k, name, _q, _h, _href in render.PHASES]
    meet = [i for i in range(4) if all(m["reach"][i] == 2 for m in every)]
    if meet != [2]:
        raise SystemExit(f"frameworks.json: the map's wash and its note say every shape meets in {render.PHASES[2][1]}; "
                         f"the data has them meeting in {[render.PHASES[i][0] for i in meet] or 'no phase'}")
    heads = "\n      ".join(
        f'<a class="vm-p" style="--c:var(--dg-{hue});grid-column:{i + 1}" href="{href}">'
        f'<span class="c-key">{key}</span> <span class="c-name">{name}</span>{_craft(i)}</a>'
        for i, (key, name, _q, hue, href) in enumerate(render.PHASES))
    rows = []
    for j, m in enumerate(every):
        r = m["reach"]
        cov = [i for i, x in enumerate(r) if x == 2]
        after = max(i for i, x in enumerate(r) if x) + 2          # the first column past the shape and its ends
        parts = [f'<a class="vm-pl" href="{m["lesson"]}"><span class="vm-nm">{_E(m["title"])}</span>'
                 f'<span class="hand vm-pn"><span class="vh">, </span>{_E(m["note"])}</span>'
                 f'<span class="vh">. It {reading(m, spoken)}.</span></a>',
                 '<span class="vm-bar" aria-hidden="true"></span>']
        ends = iter(m.get("ends") or [])
        for i, x in enumerate(r):
            if x == 1:
                parts.append(f'<span class="vm-lt{" l" if i < cov[0] else ""}" style="--c1:{i + 1}" hidden aria-hidden="true">'
                             f'<span>{_E(next(ends))}</span></span>')
            elif x == "x":
                parts.append(f'<span class="vm-ex" style="--c1:{i + 1}" hidden aria-hidden="true"><span>{ADDED}</span></span>')
        parts.append(f'<span class="hand vm-n" style="--e:{after}" hidden>{ARROW}<span>{_E(m["note"])}</span></span>')
        rows.append(f'<li class="vm-r" style="--r:{j + 3};--a:{cov[0] + 1};--b:{cov[-1] + 2}">{"".join(parts)}</li>')
    qs = "".join(
        f'<li style="--c:var(--dg-{hue});grid-column:{i + 1}"><b class="vm-k">{key} {name}</b> '
        f'<span class="vm-ask">{q}</span> <q>{_E(render.SKIPPED[i])}</q></li>'
        for i, (key, name, q, hue, _href) in enumerate(render.PHASES))
    band = f"""<section class="band" id="methods" aria-labelledby="h-methods"><div class="wrap">
  <header class="sec-h split"><p class="eyebrow">The methods</p>
    <h2 id="h-methods">How AI-DLC, BMAD and the rest fit together.</h2>
    <p>Each one is a way to build with AI. They all meet in the build, and they leave the same four questions to you.</p></header>
  <figure class="vm" aria-labelledby="vm-cap">
    <div class="vm-hd"><a class="vm-me" href="{pdlc["lesson"]}">{_E(pdlc["title"])}</a> <span class="hand vm-by">{_E(pdlc["note"])}</span>
      <span class="vm-loop"><svg viewBox="0 0 12 10" width="12" height="10" {PEN}><path d="M11 5H2M5.5 1.5 2 5l3.5 3.5"/></svg>back to Frame, with what you learned</span></div>
    <div class="vm-g">
      <span class="vm-fr" aria-hidden="true"></span><span class="vm-meet" aria-hidden="true"></span>
      <span class="vm-so" hidden aria-hidden="true"><em>sign-off</em><em class="b">nothing is built until the spec is signed</em></span>
      {heads}
      <p class="vm-l vm-l1"><span>How your team builds with AI</span></p>
      <ul class="vm-rows" role="list">{"".join(rows)}</ul>
      <span class="hand vm-n vm-all" hidden aria-hidden="true">{ARROW_UP}<span>all {NUMBER[len(every)]} meet here: the build</span></span>
      <p class="vm-l vm-l2"><span>Agent projects go wrong in four places. These are the questions the methods leave open.</span></p>
      <ol class="vm-q" role="list">{qs}</ol>
      <span class="hand vm-n vm-none" hidden aria-hidden="true">{ARROW}<span>no method reaches this row</span></span>
    </div>
    <figcaption id="vm-cap">Each shape spans the phases its method covers; the handwriting says who made it and when. The dashed line is the sign-off: nothing is built until the spec is signed.</figcaption>
  </figure>
  <p class="links"><a class="more" href="learn/one-lifecycle-for-every-method/">Where each method sits, stage by stage <i aria-hidden="true">→</i></a>
    <a class="more" href="learn/ai-dlc-vs-aidd-vs-agentic-sdlc/">AIDLC, AIDDLC and other names, sorted <i aria-hidden="true">→</i></a></p>
</div></section>"""
    # eight handwritten notes on the map, no more (verdict-home 1.2). Each method's note is written twice, in its shape
    # for the middle widths and in the margin for the wide one, so this counts the words, not the marks.
    notes = set(re.findall(r'class="hand[^"]*"[^>]*>(?:<svg.*?</svg>)?(?:<span class="vh">, </span>)?(?:<span>)?([^<]+)<', band))
    if len(notes) > 8:
        raise SystemExit(f"the method map carries {len(notes)} handwritten notes; eight is the most it may carry")
    return band
