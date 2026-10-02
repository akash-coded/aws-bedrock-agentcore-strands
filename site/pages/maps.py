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

A lesson embeds its map with ``{{map:<slug>}}``; the wiki shows a screenshot of it.
"""
from __future__ import annotations

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


# -------------------------------------------------------------------------------------- bands
def bands(spec):
    m, y = bb.title(PX + 2, 14, spec["title"], maxw=PW - 4)
    html = bb.h_title(spec["title"])
    y += 18
    flow = spec.get("flow", True)
    bgap = 28 if flow else 12
    B = spec["bands"]
    for k, b in enumerate(B):
        cw, rows = _grid_rows(b["cells"], CXW)
        inner = sum(h for _r, h in rows) + (len(rows) - 1) * 8
        bh = max(inner + 20, bb.label_h(LCW, b["name"], b.get("key", ""), b.get("sub", "")) + 16)
        m += (f'<rect x="{PX}" y="{y:.1f}" width="{PW}" height="{bh:.1f}" rx="14" fill="{bb.tint(b["hue"])}" '
              f'stroke="{bb.border(b["hue"])}" stroke-width="1.6"/>')
        m += bb.label_col(PX + 8, y + 8, LCW, bh - 16, b["hue"], name=b["name"], key=b.get("key", ""),
                          sub=b.get("sub", ""))
        cy = y + (bh - inner) / 2
        for row, rh in rows:
            for j, c in enumerate(row):
                m += _node(CX0 + j * (cw + GAP), cy, cw, rh, c, b["hue"])
            cy += rh + 8
        html += bb.h_block(b["hue"], b["name"], "".join(_hcell(c, b["hue"]) for c in b["cells"]),
                           key=b.get("key", ""), sub=b.get("sub", ""))
        if k < len(B) - 1:
            if flow:
                lx = PX + 8 + LCW / 2
                m += bb.flow([(lx, y + bh + 3), (lx, y + bh + bgap - 3)], sw=2)
                if b.get("to_label"):
                    m += bb.text(lx + 16, y + bh + bgap / 2 + 4.7, b["to_label"], fs=MIN, b=True, c=INK2)
                html += bb.h_arrow(b.get("to_label", ""))
            y += bh + bgap
        else:
            y += bh
    if spec.get("terminal"):
        t = spec["terminal"]
        cx = CX0 + CXW / 2
        tw_ = _terminal_w(t["t"], t.get("s", ""), cap=CXW)
        th = _terminal_h(tw_, t["t"], t.get("s", ""))
        m += bb.flow([(cx, y + 3), (cx, y + 31)], sw=2)
        if t.get("label"):
            m += bb.text(cx + 16, y + 21, t["label"], fs=MIN, b=True, c=INK2)
        m += _terminal(cx, y + 34, tw_, th, t["t"], t.get("s", ""), t.get("h", "n"))
        html += bb.h_arrow(t.get("label", "")) + bb.h_chip(t["t"], t.get("h", "n"), sub=t.get("s", ""))
        y += 34 + th
    m, y, html = _footer(spec, m, y, html)
    return _finish(spec, m, y, html)


# ------------------------------------------------------------------------------ footer, frame
def _footer(spec, m, y, html, best=None):
    """Callout and best-for box under a picture, side by side when both are present."""
    cal, best = spec.get("callout"), best or spec.get("best")
    if cal:
        html += bb.h_call(cal[0], cal[1])
    if best:
        html += bb.h_list(best[0], best[1], best[2])
    if not cal and not best:
        return m, y + 10, html
    y += 22
    if cal and best:
        cw_, lw = 380, PW - 380 - 20
        h = max(bb.callout_h(cw_, cal[0]) + 12, bb.listbox_h(lw, best[1]))
        m += bb.callout(PX, y + 12, cw_, cal[0], cal[1], h=h - 12)
        m += bb.listbox(PX + cw_ + 20, y, lw, best[0], best[1], best[2], h=h)
        return m, y + h + 8, html
    if cal:
        m += bb.callout(PX, y, PW, cal[0], cal[1])
        return m, y + bb.callout_h(PW, cal[0]) + 8, html
    m += bb.listbox(PX, y, PW, best[0], best[1], best[2])
    return m, y + bb.listbox_h(PW, best[1]) + 8, html


def _finish(spec, m, y, html):
    if spec.get("note"):
        pm, ph = bb.para(PX + 4, y + 4, spec["note"], PW - 8)
        m += pm
        y += ph + 8
        html += bb.h_note(spec["note"])
    return bb.svg(W, int(y) + 12, m, spec["alt"], caption=spec.get("caption", ""), narrow=html)


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


def flow(spec):
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
def pairs(spec):
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
def funnel(spec):
    m, y = bb.title(PX + 2, 14, spec["title"], maxw=PW - 4)
    html = bb.h_title(spec["title"])
    y += 20
    steps, shared = spec["steps"], spec.get("shared")
    # a short "no" rides on its arrow; a long reason sits on the outcome's top edge instead
    labw = max(bb.tw(st.get("exit", "no"), MIN, 700) + 16 for st in steps)
    on_arrow = labw <= 96
    gapx = (labw + 36) if on_arrow else 44
    qx, qw = PX, 360
    ox = qx + qw + gapx
    ow = min(PX + PW - ox, 400)
    cx = qx + qw / 2
    # the start
    sw_ = min(qw, bb.tw(spec["start"], bb.T, 700) + 44)
    sh = _terminal_h(sw_, spec["start"])
    m += _terminal(cx, y, sw_, sh, spec["start"], hue="s")
    m += bb.flow([(cx, y + sh + 3), (cx, y + sh + 26 - 3)])
    html += bb.h_chip(spec["start"], "s")
    fol = [bb.h_arrow(el="li")]
    y += sh + 26
    firsty = y
    VG = 46                     # between questions: room for the "yes" on the way down
    for i, st in enumerate(steps):
        out = st.get("out")
        lab = st.get("exit", "no")
        qh = bb.node_h(qw, st["q"], "", "ask", 15)
        if out:
            qh = max(qh, _nh(ow, out, 15) + (0 if on_arrow else VIA))
        m += bb.node(qx, y, qw, qh, title_=st["q"], icon="ask", hue="o", fs=15)
        fol.append(bb.h_cell(st["q"], "", "ask", "o"))
        if out or shared:
            m += bb.flow([(qx + qw + 2, y + qh / 2), (ox - 3, y + qh / 2)], label=lab if on_arrow else "")
        if out:
            m += _node(ox, y, ow, qh, out, "k", fs=15, top=0 if on_arrow else VIA)
            if not on_arrow:
                m += _via(ox + 12, y, lab, out.get("h", "k"))
            fol.append(_hcell(out, "k", via=lab).replace('class="bbn-c', 'class="bbn-c out', 1))
        m += bb.flow([(cx, y + qh + 3), (cx, y + qh + VG - 3)], label=st.get("go", "yes"))
        fol.append(bb.h_arrow(st.get("go", "yes"), el="li"))
        y += qh + VG
    lasty = y - VG
    if shared:
        m += _node(ox, firsty, ow, lasty - firsty, shared, "k", fs=16)
    end = spec["end"]
    eh = _nh(qw, end, 15)
    m += _node(qx, y, qw, eh, end, "g", fs=15)
    fol.append(_hcell(end, "g"))
    if shared:
        fol.append(_hcell(shared, "k", via="any " + steps[0].get("exit", "no")).replace('class="bbn-c', 'class="bbn-c out', 1))
    html += f'<ol class="bbn-f">{"".join(fol)}</ol>'
    y += eh
    m, y, html = _footer(spec, m, y, html, best=spec.get("aside"))
    return _finish(spec, m, y, html)


# ---------------------------------------------------------------------------------------- fan
def fan(spec):
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


def draw(slug: str) -> str:
    from . import mapspecs
    spec = mapspecs.MAPS[slug]
    return KINDS[spec["kind"]](spec)


def slugs() -> list[str]:
    from . import mapspecs
    return list(mapspecs.MAPS)


def alt(slug: str) -> str:
    from . import mapspecs
    return mapspecs.MAPS[slug]["alt"]
