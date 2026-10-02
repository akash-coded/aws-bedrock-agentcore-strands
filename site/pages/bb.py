"""The explainer-illustration grammar, as SVG primitives.

A port of the ``explainer-illustrations`` skill's ``bb-engine.js`` to the build: a title row with
solid pills, rounded panels with a pale fill, a solid label column at the left of each panel,
nodes with a flat two-tone icon, dashed flows, numbered circles, tinted callouts and "Best for"
lists, drawn once here so every picture on the site is the same picture.

Three rules the builder keeps so that a picture can be read at every width:

* Text is measured, not guessed. ``tw`` adds up the real advance widths of the site's body font
  (Geist, measured in a browser at weights 500, 600 and 700), and ``fit`` wraps on that measure.
  A box is sized from the lines it holds; nothing is cut to make it fit.
* Nothing is drawn below ``MIN`` units. A drawing is only shown while its canvas is at least
  ``MIN`` / 11 of its drawn width on screen, so its smallest label is 11px or more.
* Below that width the figure does not shrink: ``svg(..., narrow=...)`` carries the same content
  as plain HTML (the ``h_*`` helpers), which wraps like any other text, and base.css swaps the two
  on the figure's own width.

Colours are CSS tokens (``--bb-*`` in base.css, which point at the site's phase hues), never
literals, so a drawing follows the theme and a phase keeps its hue on every page.
"""
from __future__ import annotations

import html

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731

# palette keys. Phases: g = P0 (slate) · b = P1 (indigo) · p = P2 (teal) · o = P3 (amber) ·
# k = the sign-off, and what is owed (rose). Not phases: t (violet), y (green), u (sky),
# n (ink, "this manual") and s (neutral grey).
HUES = ("g", "b", "p", "t", "o", "k", "n", "s", "y", "u")
INK, INK2, NODE, ON = "var(--bb-ink)", "var(--bb-ink2)", "var(--bb-node)", "var(--bb-on)"
FONT = "Geist,Inter,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
MIN = 13.5          # the smallest type on any canvas, in canvas units
T, S = 14.5, 13.5   # a node's title and its second line


def solid(h: str) -> str: return f"var(--bb-{h})"
def dark(h: str) -> str: return f"var(--bb-{h}-d)"
def tint(h: str) -> str: return f"color-mix(in oklab,var(--bb-{h}) var(--bb-tint),var(--bb-node))"
def border(h: str) -> str: return f"color-mix(in oklab,var(--bb-{h}) var(--bb-bord),var(--bb-node))"


# ------------------------------------------------------------------------------------ measuring
# Advance widths of Geist in thousandths of an em, measured with canvas.measureText in Chrome.
# Kerning only ever tightens a line, so a sum of advances is a safe upper bound.
_CH = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~·×→←↑↓≤≥Σ−÷’‘“”…–—≈±½é°•✓✗∞↺€£'
_ADV = {
    500: (243,228,361,515,643,810,649,186,290,290,427,562,213,418,213,494,673,406,630,625,629,641,604,531,624,606,302,302,546,544,546,570,925,689,688,713,701,609,595,713,716,280,607,656,583,890,745,751,657,745,680,654,568,694,688,968,633,594,561,361,470,361,438,558,258,565,608,563,608,576,412,607,591,256,284,609,282,885,591,588,608,608,394,537,410,586,560,829,607,553,552,395,274,395,523,213,515,1000,1000,710,710,549,549,611,528,548,218,218,399,399,612,592,908,549,542,815,576,412,329,764,571,713,602,740,623),
    600: (236,243,376,552,656,818,677,195,306,306,424,566,225,418,225,508,683,427,642,637,643,656,615,538,644,618,306,306,548,548,548,581,944,709,695,724,708,615,600,726,719,290,617,672,586,902,748,763,664,757,689,668,584,699,709,991,660,613,577,375,485,375,450,560,268,580,621,580,621,591,429,620,601,269,308,628,297,892,601,603,621,621,409,553,427,597,584,839,628,570,567,401,284,401,523,225,528,1000,1000,708,708,549,549,667,536,556,232,232,431,431,654,594,910,549,546,830,591,420,345,764,571,713,602,752,635),
    700: (228,257,390,589,670,825,706,203,323,323,422,570,236,417,236,522,693,449,653,650,656,671,627,544,664,631,311,311,550,552,550,591,962,730,703,734,716,622,604,738,721,300,627,689,589,915,750,776,672,769,697,681,599,703,730,1015,688,631,594,390,501,390,461,561,278,594,634,598,634,605,447,634,611,281,331,647,313,900,611,618,634,634,425,570,445,607,609,849,650,586,583,408,294,408,523,236,540,1000,1000,706,706,549,549,667,544,564,247,247,462,462,695,595,911,549,550,846,605,428,362,764,571,713,602,765,647),
}
_IDX = {c: i for i, c in enumerate(_CH)}


def tw(s: str, fs: float, weight: int = 500) -> float:
    """The width of ``s`` set in Geist at ``fs``, in the same units as ``fs``."""
    adv = _ADV[700 if weight >= 650 else (600 if weight >= 550 else 500)]
    return sum(adv[_IDX[c]] if c in _IDX else 640 for c in str(s)) * fs / 1000 * 1.015


def fit(text: str, maxw: float, fs: float, weight: int = 500) -> list[str]:
    """Greedy word wrap to a measured width. Never splits a word, never drops one."""
    out, line = [], ""
    for w in str(text).split():
        cand = f"{line} {w}".strip()
        if not line or tw(cand, fs, weight) <= maxw:
            line = cand
        else:
            out.append(line)
            line = w
    if line:
        out.append(line)
    return out


def width(s: str, fs: float) -> float:
    """The width of a pill holding ``s`` in bold: the measured text plus its padding."""
    return round(tw(s, fs, 700) + fs * 1.5, 1)


def text(x: float, y: float, s: str, *, fs: float = MIN, b: bool = False, w: int | None = None,
         c: str = INK, a: str = "start") -> str:
    weight = w if w is not None else (700 if b else 500)
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="{weight}" fill="{c}" '
            f'text-anchor="{a}" font-family="{FONT}">{E(s)}</text>')


def lines(x: float, y: float, ls: list[str], *, lh: float = 17, **kw) -> str:
    return "".join(text(x, y + i * lh, l, **kw) for i, l in enumerate(ls))


def para(x: float, y: float, s: str, maxw: float, *, fs: float = MIN, w: int = 500, c: str = INK2,
         lh: float | None = None, a: str = "start") -> tuple[str, float]:
    """A wrapped sentence whose first line's top is ``y``. Returns (markup, height)."""
    lh = lh or round(fs * 1.3, 1)
    ls = fit(s, maxw, fs, w)
    return lines(x, y + fs * 0.86, ls, fs=fs, w=w, c=c, lh=lh, a=a), len(ls) * lh


def pill(x: float, y: float, s: str, h: str, *, fs: float = 14, w: float | None = None,
         hh: float | None = None, r: float | None = None, fill: str | None = None,
         c: str = ON, stroke: str = "") -> tuple[float, float, str]:
    """A solid pill with centred bold text. Returns (width, height, markup)."""
    pw = w or width(s, fs)
    ph = hh or round(fs * 1.9)
    rr = ph / 2 if r is None else r
    st = f' stroke="{stroke}" stroke-width="1.6"' if stroke else ""
    m = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{pw:.1f}" height="{ph:.1f}" rx="{rr}" fill="{fill or solid(h)}"{st}/>'
         + text(x + pw / 2, y + ph / 2 + fs * 0.35, s, a="middle", fs=fs, b=True, c=c))
    return pw, ph, m


def tag(cx: float, cy: float, s: str, *, fs: float = MIN, c: str = INK, a: str = "middle") -> tuple[float, str]:
    """A label that has to sit on a line: bold text on its own backing. Returns (width, markup)."""
    w = tw(s, fs, 700) + 16
    x = cx - w / 2 if a == "middle" else (cx if a == "start" else cx - w)
    return w, (f'<rect x="{x:.1f}" y="{cy - 11:.1f}" width="{w:.1f}" height="22" rx="11" fill="{NODE}" '
               f'stroke="{c}" stroke-width="1"/>' + text(x + w / 2, cy + fs * 0.35, s, a="middle", fs=fs, b=True, c=c))


def title(x: float, y: float, parts: list[tuple[str, str] | tuple[str]], *, fs: float = 20,
          maxw: float = 820) -> tuple[str, float]:
    """The title row: pills for the subjects and plain bold text between. Returns (markup, bottom).

    The row is measured: a title too long for the canvas steps down in size, and below 16 its plain
    words move to a second line, so it can never run off the picture."""
    def total(f):
        return sum((width(p[0], f) + 12) if len(p) == 2 else (tw(p[0], f - 2, 700) + 14) for p in parts)
    while fs > 16 and total(fs) > maxw:
        fs -= 1
    wrap_plain = total(fs) > maxw
    cx, cy, m, hh = x, y, "", fs + 16
    for p in parts:
        if len(p) == 2:
            pw, _, pm = pill(cx, cy, p[0], p[1], fs=fs, r=8, hh=hh)
            m += pm
            cx += pw + 12
        else:
            pw = tw(p[0], fs - 2, 700)
            if wrap_plain and cx > x and cx + pw > x + maxw:
                cx, cy = x, cy + hh + 6
            m += text(cx, cy + hh / 2 + (fs - 2) * 0.35, p[0], fs=fs - 2, b=True)
            cx += pw + 14
    return m, cy + hh


def panel(x: float, y: float, w: float, h: float, hue: str, *, r: float = 16) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{tint(hue)}" '
            f'stroke="{border(hue)}" stroke-width="1.6"/>')


def label_h(w: float, name: str, key: str = "", sub: str = "") -> float:
    """The height a label column needs for its key, name and one-line definition."""
    h = 16 + len(fit(key, w - 26, MIN, 700)) * 17 + (3 if key else 0) + len(fit(name, w - 26, 17, 700)) * 20
    if sub:
        h += 4 + len(fit(sub, w - 26, MIN, 600)) * 17
    return h + 14


def label_col(x: float, y: float, w: float, h: float, hue: str, *, name: str, key: str = "",
              sub: str = "") -> str:
    """The solid column at the left of a panel: a key, the name, a one-line definition."""
    m = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{solid(hue)}"/>'
    ty = y + 16
    if key:
        kl = fit(key, w - 26, MIN, 700)
        m += lines(x + 13, ty + 12, kl, fs=MIN, b=True, c=ON, lh=17)
        ty += len(kl) * 17 + 3
    nl = fit(name, w - 26, 17, 700)
    m += lines(x + 13, ty + 15, nl, fs=17, b=True, c=ON, lh=20)
    ty += len(nl) * 20
    if sub:
        m += lines(x + 13, ty + 4 + 12, fit(sub, w - 26, MIN, 600), fs=MIN, c=ON, w=600, lh=17)
    return m


def _node_lines(w: float, title_: str, sub: str, icon: str, fs: float) -> tuple[list[str], list[str]]:
    tw_ = w - (58 if icon else 26)
    return fit(title_, tw_, fs, 700), (fit(sub, tw_, S, 500) if sub else [])


def node_h(w: float, title_: str, sub: str = "", icon: str = "", fs: float = T) -> float:
    """The height a node of this width needs: every line of its title and subtitle, plus padding."""
    tl, sl = _node_lines(w, title_, sub, icon, fs)
    return max(46 if icon else 40, len(tl) * (fs + 3.5) + (len(sl) * 17 + 2 if sl else 0) + 20)


def node(x: float, y: float, w: float, h: float | None = None, *, title_: str, sub: str = "", icon: str = "",
         hue: str = "n", fs: float = T, r: float = 12, href: str = "", sw: float = 1.8,
         fill: str = NODE, top: float = 0) -> str:
    """A node: flat icon at the left, bold title, grey subtitle, every line kept. ``h`` defaults to
    what the text needs; pass the tallest ``node_h`` of a row to keep its nodes level. ``top`` keeps
    that much of the node's head clear, for a label that sits on its top edge."""
    h = h or node_h(w, title_, sub, icon, fs) + top
    tl, sl = _node_lines(w, title_, sub, icon, fs)
    lh = fs + 3.5
    block = len(tl) * lh + (len(sl) * 17 + 2 if sl else 0)
    tx = x + 48 if icon else x + 13
    ty = y + top + (h - top - block) / 2 + fs * 0.9
    m = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" '
         f'stroke="{solid(hue)}" stroke-width="{sw}"/>')
    if icon:
        m += icon_(icon, x + 26, y + top + (h - top) / 2 - 14, 28, c=solid(hue), ink=INK, fill=tint(hue))
    m += lines(tx, ty, tl, fs=fs, b=True, lh=lh)
    if sl:
        m += lines(tx, ty + len(tl) * lh + 1, sl, fs=S, c=INK2, lh=17)
    if href:
        return f'<a href="{E(href)}">{m}</a>'
    return m


def quiet_h(w: float, s: str) -> float:
    return max(40, len(fit(s, w - 26, MIN, 500)) * 17 + 20)


def quiet(x: float, y: float, w: float, h: float, s: str, hue: str) -> str:
    """The dashed, empty-by-design cell: one centred sentence."""
    ls = fit(s, w - 26, MIN, 500)
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="11" fill="none" '
            f'stroke="{border(hue)}" stroke-width="1.4" stroke-dasharray="5 4"/>'
            + lines(x + w / 2, y + (h - len(ls) * 17) / 2 + 12.5, ls, a="middle", fs=MIN, c=INK2, w=500, lh=17))


def num(x: float, y: float, n: int | str, hue: str = "b") -> str:
    return (f'<circle cx="{x}" cy="{y}" r="12" fill="{tint(hue)}" stroke="{INK}" stroke-width="1.5"/>'
            + text(x, y + 4.7, str(n), a="middle", fs=MIN, b=True))


def flow(pts: list[tuple[float, float]], *, c: str = INK, sw: float = 2, solid_: bool = False,
         head: bool = True, label: str = "", lx: float = 0, ly: float = 0) -> str:
    """A dashed connector with a filled arrowhead. Dashed means flow; ``solid_`` is for containment.
    A label sits on the middle of the longest run, on its own backing."""
    import math
    d = " ".join(("L" if i else "M") + f"{p[0]:.1f} {p[1]:.1f}" for i, p in enumerate(pts))
    (ax, ay), (bx, by) = pts[-1], pts[-2]
    ang = math.atan2(ay - by, ax - bx)
    L, W = 9, 5.5
    x1 = ax - L * math.cos(ang) + W * math.sin(ang); y1 = ay - L * math.sin(ang) - W * math.cos(ang)
    x2 = ax - L * math.cos(ang) - W * math.sin(ang); y2 = ay - L * math.sin(ang) + W * math.cos(ang)
    cls = "" if solid_ else ' class="bb-flow"'
    dash = "" if solid_ else ' stroke-dasharray="7 5"'
    m = (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" '
         f'stroke-linejoin="round"{cls}{dash}/>')
    if head:
        m += f'<path d="M{ax:.1f} {ay:.1f}L{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}Z" fill="{c}"/>'
    if label:
        i = max(range(len(pts) - 1), key=lambda k: abs(pts[k + 1][0] - pts[k][0]) + abs(pts[k + 1][1] - pts[k][1]))
        mx = (pts[i][0] + pts[i + 1][0]) / 2 + lx
        my = (pts[i][1] + pts[i + 1][1]) / 2 + ly
        m += tag(mx, my, label, c=INK)[1]
    return m


def callout_h(w: float, s: str, fs: float = 14) -> float:
    return len(fit(s, w - 30, fs, 600)) * (fs + 4.5) + 22


def callout(x: float, y: float, w: float, s: str, hue: str, *, h: float | None = None,
            fs: float = 14) -> str:
    """A tinted box that says what the picture proves. Grows to hold its sentence."""
    ls = fit(s, w - 30, fs, 600)
    lh = fs + 4.5
    hh = max(h or 0, len(ls) * lh + 22)
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{hh:.1f}" rx="10" fill="{tint(hue)}" '
            f'stroke="{border(hue)}" stroke-width="1.6"/>'
            + lines(x + w / 2, y + (hh - len(ls) * lh) / 2 + fs * 0.98, ls, a="middle", fs=fs, w=600, lh=lh))


def _list_lines(w: float, items: list[str]) -> list[list[str]]:
    return [fit(it, w - 48, MIN, 500) for it in items]


def listbox_h(w: float, items: list[str]) -> float:
    return 12 + 30 + sum(len(ls) * 17 + 8 for ls in _list_lines(w, items)) + 6


def listbox(x: float, y: float, w: float, head: str, items: list[str], hue: str,
            *, h: float | None = None) -> str:
    """"Best for" / "Workflow" / "Examples": a box with a tinted heading pill and a numbered list."""
    _, _, pm = pill(x + 12, y, head, hue, fs=MIN, r=8, hh=26, c=INK, fill=tint(hue), stroke=border(hue))
    hh = (h or listbox_h(w, items)) - 12
    m = (f'<rect x="{x:.1f}" y="{y + 12:.1f}" width="{w:.1f}" height="{hh:.1f}" rx="12" '
         f'fill="{NODE}" stroke="{border(hue)}" stroke-width="1.6"/>' + pm)
    yy = y + 42
    for i, ls in enumerate(_list_lines(w, items)):
        m += text(x + 14, yy + 12, f"{i + 1}.", fs=MIN, b=True) + lines(x + 34, yy + 12, ls, fs=MIN, w=500, lh=17)
        yy += len(ls) * 17 + 8
    return m


def gate(x: float, y: float, h: float, *, hard: bool = True, at: float | None = None) -> str:
    """The wall the flow has to get through. The sign-off is rose and solid; a soft one is amber
    and dashed. Its label is the caller's, so it can be placed clear of its neighbours. ``at`` is
    where the badge sits on the wall (its centre, in canvas units); the middle by default."""
    hue = "k" if hard else "o"
    dash = "" if hard else ' stroke-dasharray="6 5"'
    by = y + h / 2 if at is None else at
    return (f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + h}" stroke="{solid(hue)}" stroke-width="3"{dash}/>'
            f'<rect x="{x - 12}" y="{by - 16}" width="24" height="32" rx="6" fill="{solid(hue)}"/>'
            f'<path d="M{x - 6} {by - 4}h12M{x - 6} {by + 4}h12" stroke="{ON}" stroke-width="2.4" stroke-linecap="round"/>')


SIGN_OFF = "sign-off (the hard gate)"   # the two names for the P1 to P2 crossing, joined


def svg(w: float, h: float, inner: str, label: str, *, caption: str = "", cls: str = "",
        narrow: str = "") -> str:
    """The frame: a figure with the drawing, the same content as wrapping HTML for a narrow column
    (``narrow``, from the ``h_*`` helpers), and an optional caption underneath."""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    role = "group" if "<a " in inner else "img"   # an image may not contain links; a group may
    alt = f'<div class="bbn" role="group" aria-label="{E(label)}">{narrow}</div>' if narrow else ""
    return (f'<figure class="bbw{(" " + cls) if cls else ""}{"" if narrow else " solo"}">'
            f'<svg class="bb" viewBox="0 0 {w:.0f} {h:.0f}" style="max-width:{w * 1.06:.0f}px" role="{role}" '
            f'aria-label="{E(label)}">{inner}</svg>{alt}{cap}</figure>')


# ------------------------------------------------------------------------- the same, as HTML
# A narrow column gets the picture's content as text that wraps: a title, blocks with a solid
# head, cells with an icon, arrows and the sign-off between them, the callout and the list.
def _c(hue: str) -> str:
    return f' style="--c:var(--bb-{hue})"' if hue else ""


def h_title(parts: list[tuple[str, str] | tuple[str]]) -> str:
    out = []
    for p in parts:
        out.append(f'<b{_c(p[1])}>{E(p[0])}</b>' if len(p) == 2 else f"<span>{E(p[0])}</span>")
    return f'<p class="bbn-t">{" ".join(out)}</p>'


def h_icon(name: str) -> str:
    return ('<svg class="bbn-i" viewBox="0 0 32 32" aria-hidden="true">'
            + icon_(name, 16, 0, 32, c="var(--c)", ink=INK,
                    fill="color-mix(in oklab,var(--c) var(--bb-tint),var(--bb-node))") + "</svg>")


def h_cell(t: str, s: str = "", icon: str = "", hue: str = "", *, via: str = "", n: int | str | None = None,
           is_quiet: bool = False, href: str = "", el: str = "li") -> str:
    """One cell: an optional label for the way in (``via``), a number or an icon, a title, a line."""
    if is_quiet:
        return f'<{el} class="bbn-c q"{_c(hue)}><span>{E(t)}</span></{el}>'
    lead = f'<i class="bbn-num">{E(n)}</i>' if n is not None else (h_icon(icon) if icon else "")
    v = f'<em class="bbn-via">{E(via)}</em>' if via else ""
    body = f'<span><b>{E(t)}</b>{f"<small>{E(s)}</small>" if s else ""}</span>'
    inner = f'<a href="{E(href)}">{lead}{body}</a>' if href else f"{lead}{body}"
    return f'<{el} class="bbn-c{"" if lead else " bare"}{" bbn-a" if href else ""}"{_c(hue)}>{v}{inner}</{el}>'


def h_block(hue: str, name: str, cells: str, *, key: str = "", sub: str = "", foot: str = "",
            one: bool = False) -> str:
    """A panel: a solid head (key, name, one line) over its cells. ``one`` keeps the cells in a
    single column, for a panel whose cells are a sequence."""
    k = f"<i>{E(key)}</i>" if key else ""
    sb = f"<span>{E(sub)}</span>" if sub else ""
    return (f'<section class="bbn-b"{_c(hue)}><header>{k}<b>{E(name)}</b>{sb}</header>'
            f'<ul class="bbn-g{" seq" if one else ""}">{cells}</ul>{foot}</section>')


def h_cells(cells: str, cls: str = "") -> str:
    return f'<ul class="bbn-g{(" " + cls) if cls else ""}">{cells}</ul>'


def h_arrow(label: str = "", *, el: str = "p") -> str:
    return f'<{el} class="bbn-x">{f"<span>{E(label)}</span>" if label else ""}</{el}>'


def h_gate(label: str = SIGN_OFF, *, hard: bool = True, el: str = "p") -> str:
    return f'<{el} class="bbn-x gate{"" if hard else " soft"}"><span>{E(label)}</span></{el}>'


def h_chip(s: str, hue: str = "s", *, sub: str = "") -> str:
    """The stadium at the start or the end of a chain."""
    return f'<p class="bbn-e"{_c(hue)}><b>{E(s)}</b>{f"<small>{E(sub)}</small>" if sub else ""}</p>'


def h_call(s: str, hue: str) -> str:
    return f'<p class="bbn-k"{_c(hue)}>{E(s)}</p>'


def h_list(head: str, items: list[str], hue: str) -> str:
    return (f'<div class="bbn-l"{_c(hue)}><b>{E(head)}</b><ol>'
            + "".join(f"<li>{E(i)}</li>" for i in items) + "</ol></div>")


def h_note(s: str) -> str:
    return f'<p class="bbn-n">{E(s)}</p>'


# --------------------------------------------------------------------------------------- icons
# Flat two-tone icons on a 32-box: ``c`` is the hue, ``ink`` the outline, ``f`` the pale fill.
def icon_(name: str, x: float, y: float, s: float, *, c: str = "var(--bb-b)", ink: str = INK,
          fill: str = NODE) -> str:
    k = s / 32
    f = fill
    I = {
        "person": f'<circle cx="16" cy="10" r="6" fill="{f}"/><path d="M4 30c1-7 6-10 12-10s11 3 12 10" fill="{c}"/>',
        "doc": f'<path d="M8 3h11l7 7v19H8z" fill="{f}"/><path d="M19 3v7h7" fill="{c}"/><path d="M12 16h9M12 21h9M12 26h6" stroke="{c}"/>',
        "spec": f'<path d="M8 3h11l7 7v19H8z" fill="{f}"/><path d="M19 3v7h7" fill="{c}"/><rect x="11" y="14" width="11" height="3" rx="1" fill="{c}" stroke="none"/><rect x="11" y="20" width="11" height="3" rx="1" fill="{c}" stroke="none"/><path d="M11 27h7" stroke="{c}"/>',
        "brain": f'<path d="M12 5c-4 0-6 3-6 6-2 1-3 3-3 5s1 4 3 5c0 4 3 7 7 7h3V5h-4z" fill="{c}"/><path d="M20 5c4 0 6 3 6 6 2 1 3 3 3 5s-1 4-3 5c0 4-3 7-7 7h-3V5h4z" fill="{f}"/>',
        "gear": f'<circle cx="16" cy="16" r="6" fill="{f}"/><path d="M16 3v4M16 25v4M3 16h4M25 16h4M6.8 6.8l2.8 2.8M22.4 22.4l2.8 2.8M6.8 25.2l2.8-2.8M22.4 9.6l2.8-2.8" stroke="{c}" stroke-width="3"/>',
        "server": f'<rect x="5" y="4" width="22" height="10" rx="3" fill="{f}"/><rect x="5" y="18" width="22" height="10" rx="3" fill="{c}"/><circle cx="10" cy="9" r="1.6" fill="{c}" stroke="none"/><circle cx="10" cy="23" r="1.6" fill="{f}" stroke="none"/>',
        "db": f'<ellipse cx="16" cy="8" rx="11" ry="4" fill="{f}"/><path d="M5 8v16c0 2.2 5 4 11 4s11-1.8 11-4V8" fill="{c}"/><path d="M5 16c0 2.2 5 4 11 4s11-1.8 11-4"/>',
        "shield": f'<path d="M16 3l11 4v9c0 7-5 11-11 13C10 27 5 23 5 16V7z" fill="{c}"/><path d="M11 16l3.5 3.5L21 13" stroke="{ON}" stroke-width="2.6"/>',
        "tool": f'<path d="M20 4a7 7 0 0 0-7 9L4 22l6 6 9-9a7 7 0 0 0 9-7l-4 4-4-1-1-4z" fill="{c}"/>',
        "chart": f'<path d="M4 28h24"/><rect x="7" y="16" width="5" height="12" fill="{f}"/><rect x="14" y="10" width="5" height="18" fill="{c}"/><rect x="21" y="5" width="5" height="23" fill="{f}"/>',
        "robot": f'<rect x="6" y="10" width="20" height="16" rx="5" fill="{f}"/><path d="M16 4v6M11 4h10"/><circle cx="12" cy="18" r="2.2" fill="{c}" stroke="none"/><circle cx="20" cy="18" r="2.2" fill="{c}" stroke="none"/><path d="M12 23h8" stroke="{c}"/>',
        "clipboard": f'<rect x="7" y="6" width="18" height="23" rx="3" fill="{f}"/><rect x="11" y="3" width="10" height="6" rx="2" fill="{c}"/><path d="M11 15h10M11 20h10M11 25h6" stroke="{c}"/>',
        "code": f'<rect x="3" y="5" width="26" height="22" rx="4" fill="{f}"/><path d="M12 12l-4 4 4 4M20 12l4 4-4 4" stroke="{c}" stroke-width="2.4"/>',
        "cloud": f'<path d="M9 26h14a6 6 0 0 0 1-12 8 8 0 0 0-15 2 5 5 0 0 0 0 10z" fill="{c}"/>',
        "search": f'<circle cx="14" cy="14" r="8" fill="{f}"/><path d="M20 20l7 7" stroke="{c}" stroke-width="3.4"/>',
        "flag": f'<path d="M8 29V4"/><path d="M8 5h17l-4 6 4 6H8z" fill="{c}"/>',
        "money": f'<rect x="3" y="8" width="26" height="17" rx="3" fill="{f}"/><circle cx="16" cy="16.5" r="4.5" fill="{c}"/><path d="M7 12h1M24 21h1" stroke="{c}"/>',
        "bolt": f'<path d="M18 3L7 18h8l-1 11 11-15h-8z" fill="{c}"/>',
        "check": f'<circle cx="16" cy="16" r="12" fill="{c}"/><path d="M10 16l4 4 8-8" stroke="{ON}" stroke-width="2.8"/>',
        "eye": f'<path d="M3 16s5-8 13-8 13 8 13 8-5 8-13 8S3 16 3 16z" fill="{f}"/><circle cx="16" cy="16" r="4" fill="{c}"/>',
        "gate": f'<rect x="4" y="12" width="24" height="8" rx="2" fill="{c}"/><path d="M8 12V6M24 12V6M8 20v7M24 20v7"/>',
        "users": f'<circle cx="11" cy="10" r="5" fill="{f}"/><circle cx="22" cy="12" r="4" fill="{c}"/><path d="M3 28c1-6 4-9 8-9s7 3 8 9" fill="{f}"/><path d="M19 28c0-4 2-7 4-8 3 0 5 3 6 8" fill="{c}"/>',
        "ladder": f'<path d="M9 4v24M23 4v24"/><path d="M9 9h14M9 16h14M9 23h14" stroke="{c}" stroke-width="3"/>',
        "mag": f'<circle cx="13" cy="13" r="8" fill="{f}"/><path d="M19 19l9 9" stroke="{c}" stroke-width="3.4"/><path d="M13 9v8M9 13h8" stroke="{c}"/>',
        "target": f'<circle cx="16" cy="16" r="12" fill="{f}"/><circle cx="16" cy="16" r="7" fill="{c}"/><circle cx="16" cy="16" r="2.5" fill="{ON}" stroke="none"/>',
        "handoff": f'<path d="M4 20c4-6 8-6 12 0s8 6 12 0" stroke="{c}" stroke-width="3"/><path d="M22 14l6 6-6 6"/>',
        "loop": f'<path d="M6 16a10 10 0 0 1 17-7" stroke="{c}" stroke-width="3"/><path d="M26 16a10 10 0 0 1-17 7" stroke="{c}" stroke-width="3"/><path d="M23 4v6h-6M9 28v-6h6"/>',
        "lock": f'<rect x="6" y="14" width="20" height="14" rx="3" fill="{c}"/><path d="M10 14V9a6 6 0 0 1 12 0v5" fill="{f}"/><circle cx="16" cy="21" r="2" fill="{ON}" stroke="none"/>',
        "undo": f'<path d="M10 8H4v6" /><path d="M4 14a12 12 0 1 1 3 9" stroke="{c}" stroke-width="3"/>',
        "stop": f'<path d="M10 3h12l7 7v12l-7 7H10l-7-7V10z" fill="{c}"/><path d="M11 16h10" stroke="{ON}" stroke-width="3"/>',
        "warn": f'<path d="M16 4L29 27H3z" fill="{c}"/><path d="M16 12v7M16 22v1.5" stroke="{ON}" stroke-width="2.8"/>',
        "scale": f'<path d="M16 5v22M6 27h20"/><path d="M4 12h24" stroke="{c}" stroke-width="3"/><path d="M4 12l-2 8h8zM28 12l-2 8h8z" fill="{f}"/>',
        "steps": f'<path d="M3 28h8v-7h7v-7h7V7h4" fill="none" stroke="{c}" stroke-width="3"/>',
        "table": f'<rect x="3" y="5" width="26" height="22" rx="3" fill="{f}"/><path d="M3 12h26M3 19h26M12 5v22M21 5v22" stroke="{c}"/>',
        "pen": f'<path d="M5 27l3-9L22 4l6 6-14 14z" fill="{f}"/><path d="M18 8l6 6" stroke="{c}" stroke-width="3"/><path d="M5 27l7-2" stroke="{c}"/>',
        "bill": f'<path d="M7 3h18v26l-3-2-3 2-3-2-3 2-3-2-3 2z" fill="{f}"/><path d="M11 10h10M11 15h10M11 20h6" stroke="{c}"/>',
        "wave": f'<path d="M3 20c3-8 6-8 9 0s6 8 9 0 6-8 9 0" stroke="{c}" stroke-width="3" fill="none"/><path d="M3 12c3-6 6-6 9 0s6 6 9 0 6-6 9 0" fill="none"/>',
        "ask": f'<circle cx="16" cy="16" r="12" fill="{f}"/><path d="M12 12.5a4 4 0 1 1 5.5 3.7c-1 .5-1.5 1.3-1.5 2.3v1" stroke="{c}" stroke-width="2.6"/><circle cx="16" cy="23.5" r="1.6" fill="{c}" stroke="none"/>',
        "clock": f'<circle cx="16" cy="16" r="12" fill="{f}"/><path d="M16 9v7l5 3" stroke="{c}" stroke-width="2.8"/>',
        "calendar": f'<rect x="4" y="6" width="24" height="22" rx="3" fill="{f}"/><path d="M4 13h24M10 3v6M22 3v6"/><rect x="9" y="17" width="5" height="5" rx="1" fill="{c}" stroke="none"/><rect x="18" y="17" width="5" height="5" rx="1" fill="{c}" stroke="none"/>',
        "board": f'<rect x="3" y="4" width="26" height="24" rx="3" fill="{f}"/><rect x="6" y="8" width="6" height="14" rx="1.5" fill="{c}" stroke="none"/><rect x="13" y="8" width="6" height="9" rx="1.5" fill="{c}" stroke="none"/><rect x="20" y="8" width="6" height="5" rx="1.5" fill="{c}" stroke="none"/>',
        "book": f'<path d="M4 5h9a3 3 0 0 1 3 3v19a3 3 0 0 0-3-3H4z" fill="{f}"/><path d="M28 5h-9a3 3 0 0 0-3 3v19a3 3 0 0 1 3-3h9z" fill="{c}"/>',
        "mail": f'<rect x="3" y="7" width="26" height="18" rx="3" fill="{f}"/><path d="M3 10l13 8 13-8" stroke="{c}" stroke-width="2.6"/>',
        "plane": f'<path d="M4 18l10-3 6-11 3 1-3 11 8 3-1 3-9-1-4 6-2-1 1-7-9-0z" fill="{c}"/>',
        "trend": f'<path d="M4 26l8-9 5 4 11-12" stroke="{c}" stroke-width="3"/><path d="M21 9h7v7"/>',
        "layers": f'<path d="M16 4l12 6-12 6L4 10z" fill="{c}"/><path d="M4 17l12 6 12-6M4 23l12 6 12-6" fill="none"/>',
        "swap": f'<path d="M6 11h18l-5-5M26 21H8l5 5" stroke="{c}" stroke-width="2.8"/>',
    }
    body = I.get(name, I["doc"])
    return (f'<g transform="translate({x - s / 2:.1f} {y:.1f}) scale({k:.3f})" fill="none" stroke="{ink}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{body}</g>')


icon = icon_


import re as _re


def rebase(fragment: str, prefix: str) -> str:
    """Pictures link to site pages as if drawn at the site root; move those links to a page's depth."""
    return _re.sub(r'\b(href|src)="(?![a-zA-Z][a-zA-Z0-9+.-]*:|/|#|\.)([^"]+)"',
                   lambda m: f'{m.group(1)}="{prefix}{m.group(2)}"', fragment)
