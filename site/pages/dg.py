"""Boards: the full-width explanatory illustrations.

A board is an argument the reader takes in before reading a word. The grammar is stated
once in base.css and obeyed here: one hue per concept carried through header, badge,
border and takeaway; dashed means flow and solid means containment; meta-labels are ink
rather than a hue; every region ends with its takeaway.

Boards are HTML, not SVG, because they are wide and text-heavy: HTML wraps, themes,
scales to a phone, prints, and reads out to a screen reader. SVG stays where the drawing
is genuinely geometric, which is figures.py.
"""
from __future__ import annotations

import html

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731

# --------------------------------------------------------------------------- glyphs
# One line weight, one 24-box, drawn white on the header's own hue. A glyph is a
# mnemonic for the phase, never information the words do not already carry.
GLYPH = {
    "frame": '<path d="M3 8V5a2 2 0 0 1 2-2h3M16 3h3a2 2 0 0 1 2 2v3M21 16v3a2 2 0 0 1-2 2h-3'
             'M8 21H5a2 2 0 0 1-2-2v-3"/><circle cx="12" cy="12" r="3"/>',
    "blueprint": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 3v18"/>',
    "prove": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8 12l2.5 2.5L16 9"/>',
    "gauge": '<path d="M3.5 18a8.5 8.5 0 1 1 17 0"/><path d="M12 18l5-5.5"/><circle cx="12" cy="18" r="1.4"/>',
    "people": '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 5.6A3 3 0 0 1 16 11"'
              '/><path d="M17.5 14.6A6 6 0 0 1 21 20"/>',
    "shield": '<path d="M12 3l7 3v5.5c0 4.3-2.9 8-7 9.5-4.1-1.5-7-5.2-7-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
}


def glyph(name: str) -> str:
    d = GLYPH.get(name)
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{d}</svg>' if d else ""


# --------------------------------------------------------------------------- frame
def board(kicker: str, title: str, sub: str, inner: str, note: str = "", bid: str = "") -> str:
    """The outer frame every board shares: kicker, title, thesis, canvas, conclusion."""
    i = f' id="{E(bid)}"' if bid else ""
    n = f'<p class="bn">{note}</p>' if note else ""
    return (f'<figure class="dgb"{i}><figcaption><span class="bk">{E(kicker)}</span>'
            f'<span class="bt">{E(title)}</span><span class="bs">{sub}</span></figcaption>'
            f"{inner}{n}</figure>")


GATE_GLYPH = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="10.5" width="16" '
              'height="10.5" rx="2"/><path d="M8 10.5V7a4 4 0 0 1 8 0v3.5"/></svg>')


def connector(gate: bool = False) -> str:
    """Soft crossings are a marching dash. The one hard crossing is a wall the flow has to
    get through, drawn full height so it cannot be read as decoration."""
    if gate:
        return ('<div class="dgx gate"><span class="gl">' + GATE_GLYPH
                + "</span><span class=\"gt\">Hard gate</span></div>")
    return '<div class="dgx" aria-hidden="true"><i></i><b></b></div>'


def column(hue: str, name: str, owner: str, icon: str, thesis: str,
           steps: list[tuple[str, str]], takeaway: tuple[str, list[str]]) -> str:
    """One column of a parallel flow: header, owner, thesis, numbered steps, takeaway.

    The owner sits on its own strip rather than inside the header pill: a pill that has to
    hold a phase name and a role name wraps at column width, and a wrapped header pill is
    the fastest way to make a set of columns stop reading as a set."""
    li = "".join(f"<li><b>{E(t)}</b><span>{E(s)}</span></li>" for t, s in steps)
    lab, items = takeaway
    tk = "".join(f"<li>{E(x)}</li>" for x in items)
    return (f'<section class="dgc" style="--c:var(--dg-{hue})">'
            f'<header class="ch">{glyph(icon)}<b>{E(name)}</b></header>'
            f'<p class="cw">Accountable <b>{E(owner)}</b></p>'
            f'<p class="ct">{E(thesis)}</p><ol class="co">{li}</ol>'
            f'<div class="cb"><span class="bl">{E(lab)}</span><ul>{tk}</ul></div></section>')


def flow(columns: list[str], gate_after: int | None = None) -> str:
    """Columns joined by marching connectors. gate_after marks the one hard crossing, which
    gets a wider gutter than the soft ones because it carries a label."""
    out, tracks = [], []
    for i, c in enumerate(columns):
        out.append(c)
        tracks.append("minmax(0,1fr)")
        if i < len(columns) - 1:
            hard = gate_after is not None and i == gate_after
            out.append(connector(gate=hard))
            tracks.append("84px" if hard else "44px")
    return (f'<div class="dgf" style="grid-template-columns:{" ".join(tracks)}">'
            f'{"".join(out)}</div>')


def returns(label: str) -> str:
    return (f'<div class="dgr" aria-hidden="true"><b></b><i></i>'
            f'<span>{E(label)}</span></div>')


def matrix(cols: list[tuple[str, str, str]], rows: list[dict], legend: str = "") -> str:
    """Two dimensions crossing. Columns carry one hue each, rows carry theirs, cells stay
    neutral so the chart does not become plaid. One accent device marks accountability."""
    cells = ['<div class="mc"></div>']
    for hue, name, sub in cols:
        cells.append(f'<div class="mh" style="--c:var(--dg-{hue})"><b>{E(name)}</b>'
                     f"<span>{E(sub)}</span></div>")
    for r in rows:
        cells.append(f'<div class="mr" style="--c:{r["accent"]}"><b>{E(r["name"])}</b>'
                     f'<span>{E(r["note"])}</span></div>')
        for c in r["cells"]:
            cls = "md own" if c.get("own") else ("md q" if c.get("quiet") else "md")
            k = '<span class="ok">Accountable</span>' if c.get("own") else ""
            body = f'{k}<b>{E(c["head"])}</b><span>{E(c["sub"])}</span>'
            if c.get("href"):
                cells.append(f'<a class="{cls}" href="{E(c["href"])}" '
                             f'style="--c:{r["accent"]}">{body}</a>')
            else:
                cells.append(f'<div class="{cls}" style="--c:{r["accent"]}">{body}</div>')
    lg = f'<p class="dgmk"><span><i></i>{legend}</span></p>' if legend else ""
    return (f'<div class="dgmw"><div class="dgm" style="--n:{len(cols)}">'
            f'{"".join(cells)}</div></div>{lg}')


def band(hue: str, key: str, name: str, sub: str, lanes: list[tuple[str, str, list[str], bool]]) -> str:
    """A left rail in the concept hue and its canvas: the frame for things that are
    successive rather than alternative."""
    ln = []
    for lhue, label, items, stop in lanes:
        li = "".join(f"<li>{E(x)}</li>" for x in items)
        cls = "lane stop" if stop else "lane"
        ln.append(f'<div class="{cls}" style="--l:var(--dg-{lhue})">'
                  f'<span class="lt">{E(label)}</span><ul>{li}</ul></div>')
    return (f'<section class="dglb" style="--c:var(--dg-{hue})">'
            f'<div class="lr"><span class="lk">{E(key)}</span><b>{E(name)}</b>'
            f'<span class="ls">{E(sub)}</span></div>'
            f'<div class="ll">{"".join(ln)}</div></section>')


def bands(items: list[str]) -> str:
    return f'<div class="dgl">{"".join(items)}</div>'


def section_band(label: str) -> str:
    return f'<div class="dgsb"><span class="dgt">{E(label)}</span></div>'


# --------------------------------------------------------------------------- svg + cards
def svg(width: int, height: int, inner: str, label: str) -> str:
    """A board-scale drawing. Used only where the geometry is the argument — a ring, a
    set of arcs, a spine with returns. Anything text-heavy stays in HTML."""
    return (f'<div class="dgs"><svg viewBox="0 0 {width} {height}" role="img" '
            f'aria-label="{E(label)}">{inner}</svg></div>')


def cards(items: list[dict]) -> str:
    """A row of small cards under a drawing: the unpacking half of diagram-then-unpack."""
    out = []
    for c in items:
        meta = "".join(f"<dt>{E(k)}</dt><dd>{E(v)}</dd>" for k, v in c.get("meta", []))
        out.append(f'<article class="dgcard" style="--c:var(--dg-{c["hue"]})">'
                   f'<header><span class="ck">{E(c["key"])}</span><b>{E(c["name"])}</b></header>'
                   f'<p>{E(c["body"])}</p><dl>{meta}</dl></article>')
    return f'<div class="dgcards">{"".join(out)}</div>'
