"""Lesson maps: the picture at the top of a lesson, drawn from a short spec in the same grammar as
every other picture on the site (``bb.py``).

A lesson used to open with a mermaid flowchart. Every one of those fell into one of five shapes,
so each is now a spec in ``mapspecs.py`` and this module lays it out:

    bands     rows, one per phase or theme, each with a solid label column and its cells
    flow      a chain of nodes left to right, with an optional gate, terminal or decision
    pairs     two panels side by side, row-aligned, with or without arrows across
    funnel    a ladder of questions; each "no" exits to the right, the last "yes" lands
    fan       one question and its outcomes

Each shape is laid out twice from the same spec. The drawing is an 880-unit canvas whose smallest
type is ``bb.MIN``; every box is sized from the measured lines it holds, so nothing is cut and no
label leaves its box. Under about 745px of column the drawing would fall below 11px on screen, so
the figure carries the same content as wrapping HTML and base.css shows that instead.

A lesson's map is held to a height: at most 70% of a 1440 by 900 screen (``CAP``). A bands map or a
funnel over it is tightened one step at a time (less air, more cells across, a wider label column,
the bands as cards, the aside beside the end), and the first layout that fits is drawn; a map that
fits keeps the layout it always had. Type never shrinks. A map still over at its tightest is named
in the build's output, and its words are what to shorten.

A lesson embeds its map with ``{{map:<slug>}}``; the wiki shows a screenshot of it.
"""
from __future__ import annotations

import re

from . import bb
from .bb import INK, INK2, NODE, ON, MIN

W = 880
PX, PW = 24, 832           # every panel spans this
LCW = 168                  # the label column
CX0 = PX + 8 + LCW + 12    # where cells begin
CXW = PX + PW - 10 - CX0   # the width cells share
GAP = 10
LH = 17                    # the line height of a label set at MIN


# ------------------------------------------------------------------------------------ pieces
def _nh(w, c, fs=bb.T, icon=True):
    if c.get("quiet"):
        return bb.quiet_h(w, c["t"])
    return bb.node_h(w, c["t"], c.get("s", ""), c.get("i", "") if icon else "", fs)


def _node(x, y, w, h, c, hue, *, fs=bb.T, icon=True, top=0):
    if c.get("quiet"):
        return bb.quiet(x, y, w, h, c["t"], hue)
    return bb.node(x, y, w, h, title_=c["t"], sub=c.get("s", ""), icon=c.get("i", "") if icon else "",
                   hue=c.get("h", hue), fs=fs, r=11, top=top)


VIA = 9     # the head a node keeps clear under a label set on its top edge


def _hcell(c, hue, **kw):
    if c.get("quiet"):
        return bb.h_cell(c["t"], hue=hue, is_quiet=True)
    return bb.h_cell(c["t"], c.get("s", ""), c.get("i", ""), c.get("h", hue), **kw)


def _terminal_lines(w, title, sub):
    return bb.fit(title, w - 30, bb.T, 700), (bb.fit(sub, w - 30, MIN, 500) if sub else [])


def _terminal_h(w, title, sub=""):
    tl, sl = _terminal_lines(w, title, sub)
    return max(44, len(tl) * 18 + len(sl) * LH + 18)


def _terminal_w(title, sub="", cap=320):
    """A stadium as wide as its longest line, up to ``cap``."""
    return min(cap, max(bb.tw(title, bb.T, 700), bb.tw(sub, MIN, 500) if sub else 0) + 40)


def _terminal(cx, y, w, h, title, sub="", hue="n"):
    """The stadium at the start or the end of a chain: rounded, tinted, bold."""
    tl, sl = _terminal_lines(w, title, sub)
    block = len(tl) * 18 + len(sl) * LH
    ty = y + (h - block) / 2 + 13.5
    m = (f'<rect x="{cx - w / 2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{min(h / 2, 24):.1f}" '
         f'fill="{bb.tint(hue)}" stroke="{bb.solid(hue)}" stroke-width="1.8"/>')
    m += bb.lines(cx, ty, tl, a="middle", fs=bb.T, b=True, lh=18)
    if sl:
        m += bb.lines(cx, ty + len(tl) * 18, sl, a="middle", fs=MIN, c=INK2, lh=LH)
    return m


def _via(x, y, s, hue):
    """The label for the way into a node, set on the node's top edge so it never lies on a line."""
    w = bb.tw(s, MIN, 700) + 16
    return (f'<rect x="{x:.1f}" y="{y - 11:.1f}" width="{w:.1f}" height="22" rx="11" fill="{NODE}" '
            f'stroke="{bb.solid(hue)}" stroke-width="1.2"/>'
            + bb.text(x + w / 2, y + 4.7, s, a="middle", fs=MIN, b=True))


def _cols(n):
    """Cells across: up to three, four as two and two."""
    return n if n <= 3 else (2 if n == 4 else 3)


def _grid_rows(cells, avail_w, gap=GAP):
    """Rows of cells with the height each row needs. Returns (cell width, [(row cells, height)])."""
    cols = _cols(len(cells))
    cw = (avail_w - (cols - 1) * gap) / cols
    rows = []
    for i in range(0, len(cells), cols):
        row = cells[i:i + cols]
        rows.append((row, max(_nh(cw, c) for c in row)))
    return cw, rows


def _wraps(c, cw):
    """The lines a cell's title and its second line take at this width."""
    if c.get("quiet"):
        return 1, 0
    tw_ = cw - (58 if c.get("i") else 26)
    return len(bb.fit(c["t"], tw_, bb.T, 700)), len(bb.fit(c.get("s", ""), tw_, bb.S, 500)) if c.get("s") else 0


def _grid_fit(cells, avail_w, gap=GAP):
    """Rows of cells, as many across as makes the band shortest, each row spread across the band, and no
    title or second line running to three lines. Returns [(row cells, height, cell width)]."""
    best = None
    for cols in range(1, min(len(cells), 5) + 1):
        rows = []
        for i in range(0, len(cells), cols):
            r = cells[i:i + cols]
            cw = (avail_w - (len(r) - 1) * gap) / len(r)
            rows.append((r, max(_nh(cw, c) for c in r), cw))
        if cols > 1 and any(max(_wraps(c, cw)) > 2 for r, _h, cw in rows for c in r):
            continue
        h = sum(rh for _r, rh, _w in rows) + (len(rows) - 1) * 8
        if best is None or h < best[0] - 0.5:
            best = (h, rows)
    return best[1]


# ------------------------------------------------------------------------------ the height cap
# Council 9 capped a lesson's map at 70% of a 1440 by 900 screen: 630px for the figure. There the drawing is
# 906px wide for its 880 units and the figure's frame adds 30px, so the canvas may be 582 units tall. A shape
# lays itself out as it always has; a map over the cap is tightened one step at a time, and the first layout
# that fits is the one drawn. Type never shrinks: what changes is where things sit and how much air is
# between them. A bands map's steps, from the lightest:
#   tight     less air around a label, between bands, under the title and at the foot; the arrow from one
#             band to the next runs from label column to label column
#   cols      a band's cells as many across as makes it shortest, each row spread across the band, no
#             title or line running to three lines
#   inline    every label's key on its name's line, the column as wide as that needs
#   lcw       a wider label column, so a name or its line stops wrapping
#   cards     the bands side by side as cards, a few to a row, each with its cells under its label
# A funnel's: tight (less air, the way down named beside its arrow), the aside beside the end, and the
# questions wide enough to take one line each.
CAP = 582


def _inline_w(b):
    """The width a label column needs to set its key on the same line as its name."""
    return bb.tw(b.get("key", ""), MIN, 700) + 8 + bb.tw(b["name"], 17, 700) + 26


def _tight_label(w, b, inline):
    """A label column with less air: its key, name and line, and whether the key shares the name's line
    (``inline`` is set for a whole map or not at all, so its labels stay alike)."""
    key, name, sub = b.get("key", ""), b["name"], b.get("sub", "")
    tw_ = w - 26
    one = inline and bool(key)
    kl = [] if one or not key else bb.fit(key, tw_, MIN, 700)
    nl = [name] if one else bb.fit(name, tw_, 17, 700)
    sl = bb.fit(sub, tw_, MIN, 600) if sub else []
    return one, kl, nl, sl


def _label_h(w, b, v):
    if not v.get("tight"):
        return bb.label_h(w, b["name"], b.get("key", ""), b.get("sub", ""))
    one, kl, nl, sl = _tight_label(w, b, v.get("inline"))
    return 11 + (len(kl) * 17 + 2 if kl else 0) + len(nl) * 20 + (3 + len(sl) * 17 if sl else 0) + 10


def _label(x, y, w, h, b, v):
    if not v.get("tight"):
        return bb.label_col(x, y, w, h, b["hue"], name=b["name"], key=b.get("key", ""), sub=b.get("sub", ""))
    one, kl, nl, sl = _tight_label(w, b, v.get("inline"))
    m = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{bb.solid(b["hue"])}"/>'
    ty = y + 11
    if one:
        m += bb.text(x + 13, ty + 15, b["key"], fs=MIN, b=True, c=ON)
        m += bb.text(x + 13 + bb.tw(b["key"], MIN, 700) + 8, ty + 15, b["name"], fs=17, b=True, c=ON)
        ty += 20
    else:
        if kl:
            m += bb.lines(x + 13, ty + 12, kl, fs=MIN, b=True, c=ON, lh=17)
            ty += len(kl) * 17 + 2
        m += bb.lines(x + 13, ty + 15, nl, fs=17, b=True, c=ON, lh=20)
        ty += len(nl) * 20
    if sl:
        m += bb.lines(x + 13, ty + 3 + 12, sl, fs=MIN, c=ON, w=600, lh=17)
    return m


# -------------------------------------------------------------------------------------- bands
def _bands_html(spec):
    html = bb.h_title(spec["title"])
    flow = spec.get("flow", True)
    B = spec["bands"]
    for k, b in enumerate(B):
        html += bb.h_block(b["hue"], b["name"], "".join(_hcell(c, b["hue"]) for c in b["cells"]),
                           key=b.get("key", ""), sub=b.get("sub", ""))
        if k < len(B) - 1 and flow:
            html += bb.h_arrow(b.get("to_label", ""))
    if spec.get("terminal"):
        t = spec["terminal"]
        html += bb.h_arrow(t.get("label", "")) + bb.h_chip(t["t"], t.get("h", "n"), sub=t.get("s", ""))
    return html


def _bands_rows(spec, v, m, y):
    """One band under another, each a label column and its cells. Returns (markup, bottom, the middle and
    the width of the room a terminal sits in)."""
    tight = v.get("tight")
    flow = spec.get("flow", True)
    lcw = v.get("lcw", LCW)
    cx0 = PX + 8 + lcw + (10 if tight else 12)
    cxw = PX + PW - (8 if tight else 10) - cx0
    B = spec["bands"]
    over = ""       # a tight map's arrows run from one label column to the next, over the bands' edges
    for k, b in enumerate(B):
        if v.get("cols"):
            rows = _grid_fit(b["cells"], cxw)
        else:
            cw, rows = _grid_rows(b["cells"], cxw)
            rows = [(r, rh, cw) for r, rh in rows]
        inner = sum(rh for _r, rh, _w in rows) + (len(rows) - 1) * 8
        bh = max(inner + (16 if tight else 20), _label_h(lcw, b, v) + 16)
        m += (f'<rect x="{PX}" y="{y:.1f}" width="{PW}" height="{bh:.1f}" rx="14" fill="{bb.tint(b["hue"])}" '
              f'stroke="{bb.border(b["hue"])}" stroke-width="1.6"/>')
        m += _label(PX + 8, y + 8, lcw, bh - 16, b, v)
        cy = y + (bh - inner) / 2
        for row, rh, cw in rows:
            for j, c in enumerate(row):
                m += _node(cx0 + j * (cw + GAP), cy, cw, rh, c, b["hue"])
            cy += rh + 8
        if k < len(B) - 1:
            lx = PX + 8 + lcw / 2
            if flow and tight:
                bgap = 22 if b.get("to_label") else 14
                over += bb.flow([(lx, y + bh - 5), (lx, y + bh + bgap + 5)], sw=2)
                if b.get("to_label"):
                    over += bb.text(lx + 16, y + bh + bgap / 2 + 4.7, b["to_label"], fs=MIN, b=True, c=INK2)
            elif flow:
                bgap = 28
                m += bb.flow([(lx, y + bh + 3), (lx, y + bh + bgap - 3)], sw=2)
                if b.get("to_label"):
                    m += bb.text(lx + 16, y + bh + bgap / 2 + 4.7, b["to_label"], fs=MIN, b=True, c=INK2)
            else:
                bgap = 10 if tight else 12
            y += bh + bgap
        else:
            y += bh
    return m + over, y, cx0 + cxw / 2, cxw


def _bands_cards(spec, v, m, y):
    """The bands side by side as cards, ``v["cards"]`` to a row: each card its label across the top and its
    cells under it, the n-th cells of a row level with each other. Same return as ``_bands_rows``."""
    flow = spec.get("flow", True)
    k = v["cards"]
    cg = 26 if flow else 12
    cw = (PW - (k - 1) * cg) / k
    iw = cw - 16
    B = spec["bands"]
    v = v | dict(inline=all(b.get("key") and _inline_w(b) <= iw for b in B))
    rows = [B[i:i + k] for i in range(0, len(B), k)]
    for r, row in enumerate(rows):
        hh = max(_label_h(iw, b, v) for b in row)
        depth = max(len(b["cells"]) for b in row)
        hs = [max(_nh(iw, b["cells"][i]) for b in row if i < len(b["cells"])) for i in range(depth)]
        ch = 8 + hh + 8 + sum(hs) + (depth - 1) * 8 + (8 if v.get("tight") else 10)
        for j, b in enumerate(row):
            x = PX + j * (cw + cg)
            m += (f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="14" fill="{bb.tint(b["hue"])}" '
                  f'stroke="{bb.border(b["hue"])}" stroke-width="1.6"/>')
            m += _label(x + 8, y + 8, iw, hh, b, v)
            cy = y + 8 + hh + 8
            for i, c in enumerate(b["cells"]):
                m += _node(x + 8, cy, iw, hs[i], c, b["hue"])
                cy += hs[i] + 8
            if flow and j < len(row) - 1:
                m += bb.flow([(x + cw + 2, y + 8 + hh / 2), (x + cw + cg - 3, y + 8 + hh / 2)], sw=2)
        if r < len(rows) - 1:
            if flow:
                # the row turns: down from its last card, back under the row, down into the next row's first
                lx, fx = PX + (len(row) - 1) * (cw + cg) + cw / 2, PX + cw / 2
                m += bb.flow([(lx, y + ch + 3), (lx, y + ch + 17), (fx, y + ch + 17), (fx, y + ch + 34 - 3)], sw=2)
                y += ch + 34
            else:
                y += ch + 12
        else:
            y += ch
    return m, y, PX + PW / 2, PW


def _bands_draw(spec, v):
    """The drawing in one layout. Returns (markup, canvas height)."""
    m, y = bb.title(PX + 2, 14, spec["title"], maxw=PW - 4)
    y += 14 if v.get("tight") else 18
    m, y, cx, room = (_bands_cards if v.get("cards") else _bands_rows)(spec, v, m, y)
    if spec.get("terminal"):
        t = spec["terminal"]
        tw_ = _terminal_w(t["t"], t.get("s", ""), cap=room)
        th = _terminal_h(tw_, t["t"], t.get("s", ""))
        m += bb.flow([(cx, y + 3), (cx, y + 31)], sw=2)
        if t.get("label"):
            m += bb.text(cx + 16, y + 21, t["label"], fs=MIN, b=True, c=INK2)
        m += _terminal(cx, y + 34, tw_, th, t["t"], t.get("s", ""), t.get("h", "n"))
        y += 34 + th
    m, y = _foot(spec, m, y, tight=v.get("tight"))
    return _close(spec, m, y, tight=v.get("tight"))


def _band_steps(spec):
    """The layouts a bands map may take, from the one it has always had to the tightest."""
    yield {}
    v = dict(tight=True)
    yield v
    v = v | dict(cols=True)
    yield v
    # every key on its name's line, in a column as wide as that needs (never narrower than it was)
    need = max(_inline_w(b) for b in spec["bands"])
    if all(b.get("key") for b in spec["bands"]) and need <= 200:
        v = v | dict(inline=True, lcw=max(LCW, -(-need // 4) * 4))
        yield v
    for lcw in (196, 224):
        if lcw > v.get("lcw", LCW):
            yield v | dict(lcw=lcw, inline=all(b.get("key") for b in spec["bands"]) and need <= lcw)
    n = len(spec["bands"])
    if n > 2 and not any(b.get("to_label") for b in spec["bands"]):
        for k in sorted({min(n, 4), 3}, reverse=True):
            yield v | dict(cards=k)


def _fitted(steps, draw, cap):
    """The first layout whose canvas is no taller than ``cap`` (the shortest, if none is)."""
    best = None
    for v in steps:
        m, h = draw(v)
        if cap is None or h <= cap:
            return m, h
        if best is None or h < best[1]:
            best = (m, h)
    return best


def bands(spec, cap=None):
    m, h = _fitted(_band_steps(spec), lambda v: _bands_draw(spec, v), cap)
    return _frame(spec, m, h, _bands_html(spec) + _foot_html(spec))


# ------------------------------------------------------------------------------ footer, frame
def _foot_html(spec, best=None):
    cal, best = spec.get("callout"), best or spec.get("best")
    html = bb.h_call(cal[0], cal[1]) if cal else ""
    if best:
        html += bb.h_list(best[0], best[1], best[2])
    if spec.get("note"):
        html += bb.h_note(spec["note"])
    return html


def _foot(spec, m, y, best=None, tight=False):
    """Callout and best-for box under a picture, side by side when both are present."""
    cal, best = spec.get("callout"), best or spec.get("best")
    if not cal and not best:
        return m, y + (8 if tight else 10)
    y += 16 if tight else 22
    if cal and best:
        cw_, lw = 380, PW - 380 - 20
        h = max(bb.callout_h(cw_, cal[0]) + 12, bb.listbox_h(lw, best[1]))
        m += bb.callout(PX, y + 12, cw_, cal[0], cal[1], h=h - 12)
        m += bb.listbox(PX + cw_ + 20, y, lw, best[0], best[1], best[2], h=h)
        return m, y + h + 8
    if cal:
        m += bb.callout(PX, y, PW, cal[0], cal[1])
        return m, y + bb.callout_h(PW, cal[0]) + 8
    m += bb.listbox(PX, y, PW, best[0], best[1], best[2])
    return m, y + bb.listbox_h(PW, best[1]) + 8


def _close(spec, m, y, tight=False):
    """The note, if any, and the canvas's foot. Returns (markup, canvas height)."""
    if spec.get("note"):
        pm, ph = bb.para(PX + 4, y + 4, spec["note"], PW - 8)
        m += pm
        y += ph + 8
    return m, int(y) + (8 if tight else 12)


def _frame(spec, m, h, html):
    return bb.svg(W, h, m, spec["alt"], caption=spec.get("caption", ""), narrow=html)


def _footer(spec, m, y, html, best=None):
    """The foot as the other shapes use it: the drawing and the same as text."""
    m, y = _foot(spec, m, y, best)
    cal, best = spec.get("callout"), best or spec.get("best")
    if cal:
        html += bb.h_call(cal[0], cal[1])
    if best:
        html += bb.h_list(best[0], best[1], best[2])
    return m, y, html


def _finish(spec, m, y, html):
    if spec.get("note"):
        html += bb.h_note(spec["note"])
    m, h = _close(spec, m, y)
    return _frame(spec, m, h, html)


# --------------------------------------------------------------------------------------- flow
def _flow_rows(n_items, per_row, gate_after):
    """How many items sit on each row: one row up to five, otherwise two or more level rows of at
    most four, and never a row that ends on the gate (a wall cannot stand on a corner)."""
    if n_items <= 5 and not per_row:
        return [n_items]
    cols = min(per_row or 4, 4)
    if not per_row and n_items <= 8:
        cols = -(-n_items // 2)
    sizes, left = [], n_items
    while left > 0:
        sizes.append(min(cols, left))
        left -= cols
    if gate_after is not None and len(sizes) > 1:
        edge = 0
        for i, s in enumerate(sizes[:-1]):
            edge += s
            if gate_after == edge - 1 and s > 1:
                sizes[i] -= 1
                sizes[i + 1] += 1
                break
    return sizes


def flow(spec, cap=None):
    m, y = bb.title(PX + 2, 14, spec["title"], maxw=PW - 4)
    html = bb.h_title(spec["title"])
    nodes = list(spec["nodes"])
    term, dec = spec.get("terminal"), spec.get("decision")
    gate_after = spec.get("gate_after")
    hard = not spec.get("gate_soft")
    hue = spec.get("hue", "b")
    labels = spec.get("edge_labels", [])
    back = spec.get("back")
    # every item on the chain, in order: nodes, then a terminal, then a decision and its outcomes
    items = [("node", n) for n in nodes]
    if term:
        items.append(("term", term))
    if dec:
        items += [("ask", dec), ("outs", dec)]
    sizes = _flow_rows(len(items), spec.get("per_row"), gate_after)
    if back and len(sizes) > 1:
        # a line cannot come back across two rows without crossing them: say it at the end instead
        to = back[1] if len(back) > 1 else 0
        items.append(("term", {"t": back[0], "s": f"back to step {to + 1}", "h": "o"}))
        sizes = _flow_rows(len(items), spec.get("per_row"), gate_after)
        back = None
    cols = max(sizes)
    icons = cols <= 4
    cgap = 24 if cols > 3 else 32
    gate_w = 30 if gate_after is not None else 0
    nw = (PW - (cols - 1) * cgap - gate_w) / cols
    y += 20 + (24 if gate_after is not None and hard else 0)

    def item_h(kind, d):
        if kind == "node":
            return _nh(nw, d, icon=icons)
        if kind == "term":
            return _terminal_h(nw, d["t"], d.get("s", ""))
        if kind == "ask":
            return bb.node_h(nw, d["q"], "", "ask" if icons else "")
        return 2 * (max(bb.node_h(nw, d["yes"][0]), bb.node_h(nw, d["no"][0])) + VIA) + 34

    idx, node_x, last_bottom, fol = 0, {}, y, []
    for r, n_in_row in enumerate(sizes):
        row = items[idx:idx + n_in_row]
        rh = max(item_h(k, d) for k, d in row)
        cy = y + rh / 2
        x = PX
        lab_h = 0
        for j, (kind, d) in enumerate(row):
            i = idx + j
            if kind == "node":
                m += _node(x, y, nw, rh, d, hue, icon=icons)
                node_x[i] = x + nw / 2
                if spec.get("numbered"):
                    m += bb.num(x + 8, y - 2, i + 1, d.get("h", hue))
                fol.append(_hcell(d, hue, n=(i + 1) if spec.get("numbered") else None))
            elif kind == "term":
                th = _terminal_h(nw, d["t"], d.get("s", ""))
                m += _terminal(x + nw / 2, cy - th / 2, nw, th, d["t"], d.get("s", ""), d.get("h", "n"))
                fol.append(f'<li class="bbn-e" style="--c:var(--bb-{d.get("h", "n")})"><b>{bb.E(d["t"])}</b>'
                           + (f'<small>{bb.E(d["s"])}</small>' if d.get("s") else "") + "</li>")
            elif kind == "ask":
                m += bb.node(x, y, nw, rh, title_=d["q"], icon="ask" if icons else "", hue="o")
                fol.append(bb.h_cell(d["q"], "", "ask", "o"))
            else:
                oh = (rh - 34) / 2
                for o, key, oy in ((d["yes"], "yes", y + 12), (d["no"], "no", y + rh - oh)):
                    m += bb.node(x, oy, nw, oh, title_=o[0], hue=o[1], top=VIA)
                    m += _via(x + 12, oy, d.get(f"{key}_label", key), o[1])
                    m += bb.flow([(x - cgap + 2, cy + (-6 if key == "yes" else 6)), (x - 3, oy + oh / 2)])
                    fol.append(bb.h_cell(o[0], "", o[2] if len(o) > 2 else "", o[1], via=d.get(f"{key}_label", key)))
            nx = x + nw
            last = j == len(row) - 1
            lab = labels[i] if i < len(labels) else ""
            nxt = items[i + 1][0] if i + 1 < len(items) else ""
            if not last and nxt != "outs":
                if gate_after is not None and i == gate_after:
                    gx = nx + cgap / 2 + gate_w / 2
                    m += bb.flow([(nx + 2, cy), (gx - 7, cy)]) + bb.gate(gx, y - 12, rh + 24, hard=hard)
                    m += bb.flow([(gx + 7, cy), (nx + cgap + gate_w - 3, cy)])
                    if hard:
                        m += bb.text(gx, y - 20, bb.SIGN_OFF, a="middle", fs=MIN, b=True, c=bb.dark("k"))
                    if lab:
                        ls = bb.fit(lab, nw + cgap - 12, MIN, 700)
                        m += bb.lines(gx, y + rh + 28, ls, a="middle", fs=MIN, b=True,
                                      c=bb.dark("k" if hard else "o"), lh=LH)
                        lab_h = max(lab_h, len(ls) * LH + 16)
                    fol.append(bb.h_gate(bb.SIGN_OFF + (": " + lab if lab else "") if hard else lab, hard=hard, el="li"))
                    x = nx + cgap + gate_w
                else:
                    m += bb.flow([(nx + 2, cy), (nx + cgap - 3, cy)])
                    if lab:
                        ls = bb.fit(lab, nw + cgap - 14, MIN, 700)
                        m += bb.lines(nx + cgap / 2, y + rh + 20, ls, a="middle", fs=MIN, b=True, c=INK2, lh=LH)
                        lab_h = max(lab_h, len(ls) * LH + 8)
                    fol.append(bb.h_arrow(lab, el="li"))
                    x = nx + cgap
            elif nxt == "outs":
                x = nx + cgap
            elif r < len(sizes) - 1:
                # the row turns: down from the last item, back to the start of the next row
                turn = y + rh + lab_h + 22
                m += bb.flow([(x + nw / 2, y + rh + 3), (x + nw / 2, turn), (PX + nw / 2, turn),
                              (PX + nw / 2, turn + 22 - 3 + (10 if spec.get("numbered") else 0))], label=lab)
                fol.append(bb.h_arrow(lab, el="li"))
        last_bottom = y + rh + lab_h
        idx += n_in_row
        if r < len(sizes) - 1:
            y += rh + lab_h + 44 + (10 if spec.get("numbered") else 0)
        else:
            y += rh + lab_h
    if back:
        # the line that comes back: from under the last node to under the first (or a named one)
        lab, to = back[0], back[1] if len(back) > 1 else 0
        fx, tx = node_x[len(nodes) - 1], node_x[to]
        by = last_bottom + 28
        m += bb.flow([(fx, last_bottom - lab_h + 3), (fx, by), (tx, by), (tx, last_bottom - lab_h + 5)],
                     c=bb.dark("o"), label=lab)
        fol.append(f'<li class="bbn-e" style="--c:var(--bb-o)"><b>{bb.E(lab)}</b>'
                   f"<small>back to step {to + 1}</small></li>")
        y = by + 14
    html += f'<ol class="bbn-f">{"".join(fol)}</ol>'
    m, y, html = _footer(spec, m, y, html)
    return _finish(spec, m, y, html)


# -------------------------------------------------------------------------------------- pairs
def pairs(spec, cap=None):
    m, y = bb.title(PX + 2, 14, spec["title"], maxw=PW - 4)
    html = bb.h_title(spec["title"])
    y += 18
    L, R = spec["left"], spec["right"]
    centre = spec.get("centre")
    arrows = spec.get("arrows", True)
    mid = 196 if centre else (44 if arrows else 20)
    pw = (PW - mid) / 2
    n = max(len(L["cells"]), len(R["cells"]))
    cw = pw - 24
    hs = []
    for i in range(n):
        hs.append(max([_nh(cw, p["cells"][i]) for p in (L, R) if i < len(p["cells"])]))
    HEAD = 52
    body = sum(hs) + (n - 1) * 10
    if centre:
        hw = mid - 40
        nl = bb.fit(centre[0], hw - 22, 17, 700)
        sl = bb.fit(centre[1], hw - 22, MIN, 600) if centre[1] else []
        block = 40 + 10 + len(nl) * 20 + (len(sl) * LH + 4 if sl else 0)
        if block + 24 > body:       # the middle needs more room than the rows give: open the rows up
            extra = (block + 24 - body) / n
            hs = [h + extra for h in hs]
            body = sum(hs) + (n - 1) * 10
    ph = HEAD + body + 14
    ys = [y + HEAD + sum(hs[:i]) + i * 10 for i in range(n)]
    for p, x in ((L, PX), (R, PX + pw + mid)):
        m += bb.panel(x, y, pw, ph, p["hue"], r=16)
        pwid, _, pm = bb.pill(x + 12, y + 12, p["name"], p["hue"], fs=14, r=8, hh=28)
        m += pm
        if p.get("sub") and bb.tw(p["sub"], MIN) < pw - pwid - 36:
            m += bb.text(x + 12 + pwid + 10, y + 31, p["sub"], fs=MIN, c=INK2, w=500)
        for i, c in enumerate(p["cells"]):
            m += _node(x + 12, ys[i], cw, hs[i], c, p["hue"])
    if centre:
        cx = PX + pw + mid / 2
        m += f'<rect x="{cx - hw / 2:.1f}" y="{ys[0]:.1f}" width="{hw}" height="{body:.1f}" rx="18" fill="{bb.solid(centre[2])}"/>'
        top = ys[0] + (body - block) / 2
        m += bb.icon(centre[3] if len(centre) > 3 else "person", cx, top, 40, c=ON, ink=ON, fill="none")
        m += bb.lines(cx, top + 50 + 15, nl, a="middle", fs=17, b=True, c=ON, lh=20)
        if sl:
            m += bb.lines(cx, top + 50 + len(nl) * 20 + 4 + 12, sl, a="middle", fs=MIN, c=ON, w=600, lh=LH)
        for i in range(len(L["cells"])):
            m += bb.flow([(PX + pw - 10, ys[i] + hs[i] / 2), (cx - hw / 2 - 3, ys[i] + hs[i] / 2)], sw=1.8)
        for i in range(len(R["cells"])):
            m += bb.flow([(cx + hw / 2 + 2, ys[i] + hs[i] / 2), (PX + pw + mid + 9, ys[i] + hs[i] / 2)], sw=1.8)
    elif arrows:
        for i in range(min(len(L["cells"]), len(R["cells"]))):
            m += bb.flow([(PX + pw - 10, ys[i] + hs[i] / 2), (PX + pw + mid + 9, ys[i] + hs[i] / 2)], sw=1.8)
    # the same as text: row by row when the rows are matched, otherwise panel after panel
    if arrows and not centre:
        rows = "".join(
            '<li class="bbn-pair">' + _hcell(L["cells"][i], L["hue"], el="div") + '<i aria-hidden="true"></i>'
            + _hcell(R["cells"][i], R["hue"], el="div") + "</li>"
            for i in range(min(len(L["cells"]), len(R["cells"]))))
        html += (f'<p class="bbn-ph"><b style="--c:var(--bb-{L["hue"]})">{bb.E(L["name"])}</b>'
                 f'<i aria-hidden="true"></i><b style="--c:var(--bb-{R["hue"]})">{bb.E(R["name"])}</b></p>'
                 f'<ul class="bbn-ps">{rows}</ul>')
    else:
        html += bb.h_block(L["hue"], L["name"], "".join(_hcell(c, L["hue"]) for c in L["cells"]), sub=L.get("sub", ""))
        if centre:
            html += bb.h_arrow() + bb.h_chip(centre[0], centre[2], sub=centre[1]) + bb.h_arrow()
        html += bb.h_block(R["hue"], R["name"], "".join(_hcell(c, R["hue"]) for c in R["cells"]), sub=R.get("sub", ""))
    y += ph
    m, y, html = _footer(spec, m, y, html)
    return _finish(spec, m, y, html)


# ------------------------------------------------------------------------------------- funnel
def _funnel_html(spec):
    steps, shared = spec["steps"], spec.get("shared")
    html = bb.h_title(spec["title"]) + bb.h_chip(spec["start"], "s")
    fol = [bb.h_arrow(el="li")]
    for st in steps:
        out, lab = st.get("out"), st.get("exit", "no")
        fol.append(bb.h_cell(st["q"], "", "ask", "o"))
        if out:
            fol.append(_hcell(out, "k", via=lab).replace('class="bbn-c', 'class="bbn-c out', 1))
        fol.append(bb.h_arrow(st.get("go", "yes"), el="li"))
    fol.append(_hcell(spec["end"], "g"))
    if shared:
        fol.append(_hcell(shared, "k", via="any " + steps[0].get("exit", "no")).replace('class="bbn-c', 'class="bbn-c out', 1))
    return html + f'<ol class="bbn-f">{"".join(fol)}</ol>'


def _funnel_draw(spec, v):
    """The drawing in one layout. Returns (markup, canvas height). ``v`` may ask for less air (``tight``: the
    way down from a question named beside its arrow, not on it) and for the aside to stand in the outcomes'
    column under the last outcome (``aside``) rather than at the foot."""
    tight = v.get("tight")
    m, y = bb.title(PX + 2, 14, spec["title"], maxw=PW - 4)
    y += 14 if tight else 20
    steps, shared = spec["steps"], spec.get("shared")
    # a short "no" rides on its arrow; a long reason sits on the outcome's top edge instead
    labw = max(bb.tw(st.get("exit", "no"), MIN, 700) + 16 for st in steps)
    on_arrow = labw <= 96
    gapx = (labw + 36) if on_arrow else 44
    qx, qw = PX, v.get("qw", 360)
    ox = qx + qw + gapx
    ow = min(PX + PW - ox, 400)
    cx = qx + qw / 2
    # the start
    sw_ = min(qw, bb.tw(spec["start"], bb.T, 700) + 44)
    sh = _terminal_h(sw_, spec["start"])
    sg = 22 if tight else 26
    m += _terminal(cx, y, sw_, sh, spec["start"], hue="s")
    m += bb.flow([(cx, y + sh + 3), (cx, y + sh + sg - 3)])
    y += sh + sg
    firsty = y
    VG = 30 if tight else 46     # between questions: room for the "yes" on the way down
    for i, st in enumerate(steps):
        out = st.get("out")
        lab = st.get("exit", "no")
        qh = bb.node_h(qw, st["q"], "", "ask", 15)
        if out:
            qh = max(qh, _nh(ow, out, 15) + (0 if on_arrow else VIA))
        m += bb.node(qx, y, qw, qh, title_=st["q"], icon="ask", hue="o", fs=15)
        if out or shared:
            m += bb.flow([(qx + qw + 2, y + qh / 2), (ox - 3, y + qh / 2)], label=lab if on_arrow else "")
        if out:
            m += _node(ox, y, ow, qh, out, "k", fs=15, top=0 if on_arrow else VIA)
            if not on_arrow:
                m += _via(ox + 12, y, lab, out.get("h", "k"))
        if tight:
            m += bb.flow([(cx, y + qh + 3), (cx, y + qh + VG - 3)])
            m += bb.text(cx + 12, y + qh + VG / 2 + 4.7, st.get("go", "yes"), fs=MIN, b=True, c=INK2)
        else:
            m += bb.flow([(cx, y + qh + 3), (cx, y + qh + VG - 3)], label=st.get("go", "yes"))
        y += qh + VG
    lasty = y - VG
    if shared:
        m += _node(ox, firsty, ow, lasty - firsty, shared, "k", fs=16)
    end = spec["end"]
    eh = _nh(qw, end, 15)
    m += _node(qx, y, qw, eh, end, "g", fs=15)
    y += eh
    best = spec.get("aside")
    if best and v.get("aside"):
        # the outcomes' column is empty under its last outcome, beside the end: the aside stands there
        ay = lasty + 18
        m += bb.listbox(ox, ay, ow, best[0], best[1], best[2])
        y, best = max(y, ay + bb.listbox_h(ow, best[1])), None
    m, y = _foot(spec, m, y, best=best, tight=tight)
    return _close(spec, m, y, tight=tight)


def _funnel_steps(spec):
    """The layouts a funnel may take: as it has always been; with less air (``tight``); with the aside
    beside the end (``aside``); with the questions wide enough to take one line each (``qw``)."""
    yield {}
    v = dict(tight=True)
    yield v
    if spec.get("aside"):
        v = v | dict(aside=True)
        yield v
    one = max(bb.tw(st["q"], 15, 700) for st in spec["steps"]) + 60
    if 360 < one <= 420:
        yield v | dict(qw=round(one))


def funnel(spec, cap=None):
    m, h = _fitted(_funnel_steps(spec), lambda v: _funnel_draw(spec, v), cap)
    return _frame(spec, m, h, _funnel_html(spec) + _foot_html(spec, best=spec.get("aside")))


# ---------------------------------------------------------------------------------------- fan
def fan(spec, cap=None):
    m, y = bb.title(PX + 2, 14, spec["title"], maxw=PW - 4)
    html = bb.h_title(spec["title"])
    outs = spec["outs"]
    has_via = any(o.get("via") for o in outs)
    ogap = 22 if has_via else 14
    sw_ = bb.tw(spec["start"], bb.T, 700) + 40
    qx = PX + sw_ + 28
    qw = 250
    ox = qx + qw + 60
    ow = PX + PW - ox
    hs = [_nh(ow, o, 15) + (VIA if o.get("via") else 0) for o in outs]
    total = sum(hs) + (len(outs) - 1) * ogap
    y0 = y + 22 + (10 if has_via else 0)
    cy = y0 + total / 2
    m += _terminal(PX + sw_ / 2, cy - 20, sw_, 40, spec["start"], hue="s")
    m += bb.flow([(PX + sw_ + 2, cy), (qx - 3, cy)])
    qh = bb.node_h(qw, spec["q"], "", "ask", 15)
    m += bb.node(qx, cy - qh / 2, qw, qh, title_=spec["q"], icon="ask", hue="o", fs=15)
    fol = []
    oy = y0
    for o, oh in zip(outs, hs):
        m += bb.flow([(qx + qw + 2, cy), (ox - 36, oy + oh / 2), (ox - 3, oy + oh / 2)])
        m += _node(ox, oy, ow, oh, o, "b", fs=15, top=VIA if o.get("via") else 0)
        if o.get("via"):
            m += _via(ox + 12, oy, o["via"], o.get("h", "b"))
        fol.append(_hcell(o, "b", via=o.get("via", "")))
        oy += oh + ogap
    html += (bb.h_chip(spec["start"], "s") + bb.h_arrow()
             + bb.h_cell(spec["q"], "", "ask", "o", el="p") + bb.h_arrow()
             + f'<ul class="bbn-g one">{"".join(fol)}</ul>')
    y = y0 + total + 4
    m, y, html = _footer(spec, m, y, html)
    return _finish(spec, m, y, html)


KINDS = {"bands": bands, "flow": flow, "pairs": pairs, "funnel": funnel, "fan": fan}


_WARNED: set[str] = set()


def draw(slug: str) -> str:
    """A lesson's map, held to the cap and marked with its slug (``data-map``, which the acceptance gate's
    map-height pass looks for). The wiki's own pictures (``wikimaps``) are drawn without the cap."""
    from . import mapspecs
    spec = mapspecs.MAPS[slug]
    out = KINDS[spec["kind"]](spec, cap=CAP)
    h = int(re.search(r'viewBox="0 0 \d+ (\d+)"', out).group(1))
    if h > CAP and slug not in _WARNED:
        _WARNED.add(slug)
        print(f"  maps: warning: {slug} is {h} units tall at its tightest, over the cap of {CAP}: shorten its words")
    return out.replace('<figure class="bbw">', f'<figure class="bbw" data-map="{slug}">', 1)


def slugs() -> list[str]:
    from . import mapspecs
    return list(mapspecs.MAPS)


def alt(slug: str) -> str:
    from . import mapspecs
    return mapspecs.MAPS[slug]["alt"]
