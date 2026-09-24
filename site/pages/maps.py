"""Lesson maps: the picture at the top of a lesson, drawn from a short spec in the same grammar as
every other picture on the site (``bb.py``).

A lesson used to open with a mermaid flowchart. Every one of those fell into one of five shapes,
so each is now a spec in ``mapspecs.py`` and this module lays it out:

    bands     rows, one per phase or theme, each with a solid label column and its cells
    flow      a chain of nodes left to right, with an optional gate, terminal or decision
    pairs     two panels side by side, row-aligned, with or without arrows across
    funnel    a ladder of questions; each "no" exits to the right, the last "yes" lands
    fan       one question and its outcomes

A lesson embeds its map with ``{{map:<slug>}}``; the wiki shows a screenshot of it.
"""
from __future__ import annotations

from . import bb
from .bb import INK, INK2, NODE, ON

W = 1180
PX, PW = 30, 1120          # every panel spans this
LCW = 172                  # the label column
CX0 = PX + 8 + LCW + 16    # where cells begin
CXW = PX + PW - 12 - CX0   # the width cells share
GAP = 10


# ------------------------------------------------------------------------------------ pieces
def _node(x, y, w, h, title, sub="", icon="", hue="n", *, fs=12.5, r=11, sub_lines=2, quiet=False,
          fill=None):
    """A node whose subtitle may run to three lines; ``quiet`` draws the dashed empty-by-design cell."""
    if quiet:
        ls = bb.wrap(title, int((w - 24) / 6.0))[:3]
        y0 = y + h / 2 - (len(ls) - 1) * 7 + 4
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" '
                f'stroke="{bb.border(hue)}" stroke-width="1.4" stroke-dasharray="5 4"/>'
                + bb.lines(x + w / 2, y0, ls, a="middle", fs=11, c=INK2, w=500, lh=14))
    tx = x + 52 if icon else x + 14
    tl = bb.wrap(title, int((w - (60 if icon else 26)) / 6.4))[:2]
    sl = bb.wrap(sub, int((w - (60 if icon else 26)) / 5.5))[:sub_lines] if sub else []
    total = len(tl) * 14 + (len(sl) * 12.5 + 2 if sl else 0)
    ty = y + h / 2 - total / 2 + 11
    m = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or NODE}" '
         f'stroke="{bb.solid(hue)}" stroke-width="1.8"/>')
    if icon:
        m += bb.icon(icon, x + 28, y + h / 2 - 15, 30, c=bb.solid(hue), ink=INK, fill=bb.tint(hue))
    m += bb.lines(tx, ty, tl, fs=fs, b=True, lh=14)
    if sl:
        m += bb.lines(tx, ty + len(tl) * 14 + 1, sl, fs=10.5, c=INK2, lh=12.5)
    return m


def _terminal(cx, y, title, sub="", hue="n", *, w=None, h=48):
    """The stadium at the end of a chain: rounded, tinted, bold."""
    tw = w or max(bb.width(title, 12.5) + 30, (bb.width(sub, 10.5) if sub else 0) + 30)
    x = cx - tw / 2
    m = (f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{h}" rx="{h / 2}" fill="{bb.tint(hue)}" '
         f'stroke="{bb.solid(hue)}" stroke-width="1.8"/>')
    if sub:
        m += bb.text(cx, y + h / 2 - 2, title, a="middle", fs=12.5, b=True)
        m += bb.text(cx, y + h / 2 + 13, sub, a="middle", fs=10.5, c=INK2)
    else:
        m += bb.text(cx, y + h / 2 + 4.5, title, a="middle", fs=12.5, b=True)
    return m


def _label_col(x, y, w, h, hue, key, name, sub=""):
    m = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bb.solid(hue)}"/>'
    ty = y + 24
    if key:
        m += bb.text(x + 14, ty, key.upper(), fs=10.5, b=True, c=ON, ls=".08em")
        ty += 20
    nl = bb.wrap(name, 17)[:2]
    m += bb.lines(x + 14, ty, nl, fs=15, b=True, c=ON, lh=17)
    ty += len(nl) * 17 + 2
    if sub:
        m += bb.lines(x + 14, ty, bb.wrap(sub, 26)[:2], fs=10.5, c=ON, w=600, lh=13)
    return m


def _grid(cells, x0, y0, avail_w, ch, hue, *, gap=GAP, rgap=8):
    """Cells laid out in rows: up to four across, five and six as three-and-three."""
    n = len(cells)
    cols = n if n <= 4 else (3 if n in (5, 6) else 4)
    cw = (avail_w - (cols - 1) * gap) / cols
    m, y = "", y0
    for i in range(0, n, cols):
        row = cells[i:i + cols]
        for j, c in enumerate(row):
            x = x0 + j * (cw + gap)
            if c.get("quiet"):
                m += _node(x, y, cw, ch, c["t"], hue=hue, quiet=True)
            else:
                m += _node(x, y, cw, ch, c["t"], c.get("s", ""), c.get("i", ""), c.get("h", hue))
        y += ch + rgap
    return m, y - rgap


def _rows(n):
    cols = n if n <= 4 else (3 if n in (5, 6) else 4)
    return -(-n // cols)


# -------------------------------------------------------------------------------------- bands
def bands(spec):
    m = bb.title(34, 12, spec["title"])
    y = 66
    flow = spec.get("flow", True)
    bgap = 24 if flow else 14
    B = spec["bands"]
    bottoms = []
    for k, b in enumerate(B):
        cells = b["cells"]
        has_sub = any(c.get("s") for c in cells)
        ch = 54 if has_sub else 42
        rows = _rows(len(cells))
        inner = rows * ch + (rows - 1) * 8
        need = 76 + (20 if b.get("key") else 0) + (16 * len(bb.wrap(b.get("sub", ""), 26)[:2]) if b.get("sub") else 0)
        bh = max(inner + 22, need)
        m += f'<rect x="{PX}" y="{y}" width="{PW}" height="{bh}" rx="14" fill="{bb.tint(b["hue"])}" stroke="{bb.border(b["hue"])}" stroke-width="1.6"/>'
        m += _label_col(PX + 8, y + 8, LCW, bh - 16, b["hue"], b.get("key", ""), b["name"], b.get("sub", ""))
        cy = y + (bh - inner) / 2
        gm, _ = _grid(cells, CX0, cy, CXW, ch, b["hue"])
        m += gm
        bottoms.append((y, y + bh))
        if k < len(B) - 1:
            if flow:
                lx = PX + 8 + LCW / 2
                m += bb.flow([(lx, y + bh + 2), (lx, y + bh + bgap - 2)], sw=2)
                if b.get("to_label"):
                    m += bb.text(lx + 14, y + bh + bgap / 2 + 4, b["to_label"], fs=10.5, b=True, c=INK2)
            y += bh + bgap
        else:
            y += bh
    if spec.get("terminal"):
        t = spec["terminal"]
        cx = CX0 + CXW / 2
        m += bb.flow([(cx, y + 2), (cx, y + 26)], sw=2, label=t.get("label", ""), ly=-1, lx=120)
        m += _terminal(cx, y + 28, t["t"], t.get("s", ""), t.get("h", "n"))
        y += 28 + 48
    m, y = _footer(spec, m, y)
    return _finish(spec, m, y)


# ------------------------------------------------------------------------------ footer, frame
def _footer(spec, m, y):
    """Callout and best-for box under a picture, side by side when both are present."""
    cal, best = spec.get("callout"), spec.get("best")
    if not cal and not best:
        return m, y + 12
    y += 22
    ch_ = lambda w: (cal[2] if len(cal) > 2 else len(bb.wrap(cal[0], int(w / 6.2))) * 14 + 18)  # noqa: E731
    if cal and best:
        m += bb.callout(PX, y + 8, 520, cal[0], cal[1], h=cal[2] if len(cal) > 2 else None)
        m += bb.listbox(PX + 546, y, PW - 546, best[0], best[1], best[2])
        return m, y + max(len(best[1]) * 30 + 42, ch_(520) + 8) + 10
    if cal:
        m += bb.callout(PX, y, PW, cal[0], cal[1], h=cal[2] if len(cal) > 2 else None)
        return m, y + ch_(PW) + 10
    m += bb.listbox(PX, y, PW, best[0], best[1], best[2])
    return m, y + len(best[1]) * 30 + 42 + 10


def _finish(spec, m, y):
    if spec.get("note"):
        m += bb.text(PX + 4, y + 6, spec["note"], fs=11, c=INK2, w=500)
        y += 20
    return bb.svg(W, int(y) + 10, m, spec["alt"], caption=spec.get("caption", ""))


def flow(spec):
    m = bb.title(34, 12, spec["title"])
    nodes = list(spec["nodes"])
    term = spec.get("terminal")
    dec = spec.get("decision")
    gate_after = spec.get("gate_after")
    count = len(nodes) + (1 if term else 0) + (2 if dec else 0)
    cgap = spec.get("gap", 30)
    total_gaps = (count - 1) * cgap + (28 if gate_after is not None else 0)
    nw = (PW - total_gaps) / count
    tall = spec.get("tall", False)
    nh = 84 if tall else 64
    y = 76
    cy = y + nh / 2
    x = PX
    labels = spec.get("edge_labels", [])
    for i, n in enumerate(nodes):
        m += _node(x, y, nw, nh, n["t"], n.get("s", ""), n.get("i", ""), n.get("h", spec.get("hue", "b")),
                   sub_lines=3 if tall else 2)
        if spec.get("numbered"):
            m += bb.num(x + 8, y - 2, i + 1, n.get("h", spec.get("hue", "b")))
        nx = x + nw
        if i < len(nodes) - 1 or term or dec:
            lab = labels[i] if i < len(labels) else ""
            if gate_after is not None and i == gate_after:
                gx = nx + cgap / 2 + 14
                m += bb.flow([(nx + 2, cy), (gx - 6, cy)]) + bb.gate(gx, y - 10, nh + 20)
                m += bb.flow([(gx + 6, cy), (nx + cgap + 28 - 3, cy)])
                m += bb.text(gx, y + nh + 24, lab or "hard gate", a="middle", fs=10.5, b=True, c=bb.dark("k"))
                x = nx + cgap + 28
            else:
                m += bb.flow([(nx + 2, cy), (nx + cgap - 3, cy)])
                if lab:
                    m += bb.text(nx + cgap / 2, y + nh + 24, lab, a="middle", fs=10.5, b=True, c=INK2)
                x = nx + cgap
    if term:
        m += _terminal(x + nw / 2, y + (nh - 48) / 2, term["t"], term.get("s", ""), term.get("h", "n"), w=nw)
        x += nw
    if dec:
        # a question, then two outcomes stacked to its right
        m += _node(x, y, nw, nh, dec["q"], icon="ask", hue="o")
        ox = x + nw + cgap
        oh = 44
        m += bb.flow([(x + nw + 2, cy - 8), (ox - 3, y - 8 + oh / 2)], label=dec.get("yes_label", "yes"), ly=-8)
        m += bb.flow([(x + nw + 2, cy + 8), (ox - 3, y + nh + 8 - oh / 2)], label=dec.get("no_label", "no"), ly=12)
        m += _node(ox, y - 8, nw, oh, dec["yes"][0], hue=dec["yes"][1], icon=dec["yes"][2] if len(dec["yes"]) > 2 else "")
        m += _node(ox, y + nh + 8 - oh, nw, oh, dec["no"][0], hue=dec["no"][1], icon=dec["no"][2] if len(dec["no"]) > 2 else "")
    y = y + nh + (30 if gate_after is not None or labels else 8)
    m, y = _footer(spec, m, y)
    return _finish(spec, m, y)


# -------------------------------------------------------------------------------------- pairs
def pairs(spec):
    m = bb.title(34, 12, spec["title"])
    L, R = spec["left"], spec["right"]
    arrows = spec.get("arrows", True)
    mid = 40 if arrows else 24
    pw = (PW - mid) / 2
    nh = 50 if any(c.get("s") for c in L["cells"] + R["cells"]) else 42
    rows = max(len(L["cells"]), len(R["cells"]))
    ph = 56 + rows * (nh + 10) + 6
    y = 66
    for k, (p, x) in enumerate(((L, PX), (R, PX + pw + mid))):
        m += bb.panel(x, y, pw, ph, p["hue"], r=16)
        pwid, _, pm = bb.pill(x + 14, y + 12, p["name"], p["hue"], fs=13, r=8, hh=28)
        m += pm
        if p.get("sub"):
            m += bb.text(x + 14 + pwid + 10, y + 31, p["sub"], fs=11, c=INK2, w=500)
        for i, c in enumerate(p["cells"]):
            cy = y + 56 + i * (nh + 10)
            m += _node(x + 14, cy, pw - 28, nh, c["t"], c.get("s", ""), c.get("i", ""), c.get("h", p["hue"]))
    if arrows:
        for i in range(min(len(L["cells"]), len(R["cells"]))):
            cy = y + 56 + i * (nh + 10) + nh / 2
            m += bb.flow([(PX + pw - 12, cy), (PX + pw + mid + 11, cy)], sw=1.8)
    y += ph
    m, y = _footer(spec, m, y)
    return _finish(spec, m, y)


# ------------------------------------------------------------------------------------- funnel
def funnel(spec):
    m = bb.title(34, 12, spec["title"])
    qx, qw, qh = PX, 430, 58
    ox, ow = 520, 320
    y = 70
    # the start
    m += _terminal(qx + qw / 2, y, spec["start"], hue="s", w=260, h=40)
    m += bb.flow([(qx + qw / 2, y + 42), (qx + qw / 2, y + 66)])
    y += 70
    shared = spec.get("shared")   # one outcome every "no" lands on
    firsty = y
    for i, st in enumerate(spec["steps"]):
        m += _node(qx, y, qw, qh, st["q"], icon="ask", hue="o", fs=13)
        out = st.get("out")
        exit_label = st.get("exit", "no")
        if out:
            m += bb.flow([(qx + qw + 2, y + qh / 2), (ox - 3, y + qh / 2)], label=exit_label, ly=-9)
            m += _node(ox, y, ow, qh, out["t"], out.get("s", ""), out.get("i", ""), out.get("h", "k"), fs=13)
        elif shared:
            m += bb.flow([(qx + qw + 2, y + qh / 2), (ox - 3, y + qh / 2)], label=exit_label, ly=-9)
        last = i == len(spec["steps"]) - 1
        cont = st.get("go", "yes")
        m += bb.flow([(qx + qw / 2, y + qh + 2), (qx + qw / 2, y + qh + 36 - 3)], label=cont, ly=-6, lx=60)
        y += qh + 36
    lasty = y - 36
    if shared:
        sh = lasty + qh - firsty
        m += _node(ox, firsty, ow, sh, shared["t"], shared.get("s", ""), shared.get("i", ""), shared.get("h", "k"), fs=14,
                   sub_lines=3)
    end = spec["end"]
    m += _node(qx, y, qw, qh, end["t"], end.get("s", ""), end.get("i", ""), end.get("h", "g"), fs=13)
    if spec.get("aside"):
        a = spec["aside"]
        ax = ox + ow + 30
        m += bb.listbox(ax, firsty, PX + PW - ax, a[0], a[1], a[2])
    y += qh
    m, y = _footer(spec, m, y)
    return _finish(spec, m, y)


# ---------------------------------------------------------------------------------------- fan
def fan(spec):
    m = bb.title(34, 12, spec["title"])
    outs = spec["outs"]
    oh, ogap = 66, 16
    total = len(outs) * oh + (len(outs) - 1) * ogap
    y0 = 76
    cy = y0 + total / 2
    m += _terminal(PX + 90, cy - 20, spec["start"], hue="s", w=170, h=40)
    m += bb.flow([(PX + 177, cy), (PX + 206, cy)])
    qx, qw = PX + 210, 270
    m += _node(qx, cy - 34, qw, 68, spec["q"], icon="ask", hue="o", fs=13)
    ox, ow = 790, 360
    for i, o in enumerate(outs):
        oy = y0 + i * (oh + ogap)
        m += bb.flow([(qx + qw + 2, cy), (ox - 40, oy + oh / 2), (ox - 3, oy + oh / 2)])
        if o.get("via"):
            # the label sits just before the outcome, on its own backing, so it never lies on the line
            lw = bb.width(o["via"], 10.5) - 10
            m += (f'<rect x="{ox - 10 - lw:.1f}" y="{oy + oh / 2 - 22}" width="{lw:.1f}" height="17" rx="8" '
                  f'fill="{NODE}" stroke="{INK}" stroke-width="1" opacity=".97"/>'
                  + bb.text(ox - 10 - lw / 2, oy + oh / 2 - 9.5, o["via"], a="middle", fs=10.5, b=True))
        m += _node(ox, oy, ow, oh, o["t"], o.get("s", ""), o.get("i", ""), o.get("h", "b"), fs=13)
    y = y0 + total + 8
    m, y = _footer(spec, m, y)
    return _finish(spec, m, y)


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
