"""The explainer-illustration grammar, as SVG primitives.

A port of the ``explainer-illustrations`` skill's ``bb-engine.js`` to the build: the same vocabulary
— a title row with a green accent bar and solid pills, rounded panels with a pale fill, a solid
label column at the left of each panel, white nodes with a flat two-tone icon, dashed flows that
move, numbered circles, tinted callouts and "Best for" lists — drawn once here so every picture
on the site is the same picture.

Colours are CSS tokens (``--bb-*`` in base.css), never literals, so a drawing follows the theme.
Text is Inter. Nothing is drawn below 10px on a 1180px canvas; ``wrap`` keeps lines inside their
box so a label can never run past its node.
"""
from __future__ import annotations

import html

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731

# palette keys: g green · b blue · p purple · t teal · o orange (warnings) · k pink (hard gates)
# · n navy (the spine, "this manual") · s slate (neutral). Each has solid, dark, tint and border.
HUES = ("g", "b", "p", "t", "o", "k", "n", "s")
INK, INK2, NODE, ON = "var(--bb-ink)", "var(--bb-ink2)", "var(--bb-node)", "var(--bb-on)"
FONT = "Inter,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"


def solid(h: str) -> str: return f"var(--bb-{h})"
def dark(h: str) -> str: return f"var(--bb-{h}-d)"
def tint(h: str) -> str: return f"color-mix(in oklab,var(--bb-{h}) var(--bb-tint),var(--bb-node))"
def border(h: str) -> str: return f"color-mix(in oklab,var(--bb-{h}) var(--bb-bord),var(--bb-node))"


def width(s: str, fs: float) -> float:
    """Text width for a bold Inter label: 0.58em a character plus padding. Generous on purpose."""
    return round(len(s) * fs * 0.58 + 26)


def wrap(text: str, chars: int) -> list[str]:
    """Greedy word wrap to ``chars`` per line. Never splits a word."""
    out, line = [], ""
    for w in str(text).split():
        cand = f"{line} {w}".strip()
        if len(cand) <= chars or not line:
            line = cand
        else:
            out.append(line)
            line = w
    if line:
        out.append(line)
    return out


def text(x: float, y: float, s: str, *, fs: float = 12, b: bool = False, w: int | None = None,
         c: str = INK, a: str = "start", ls: str = "") -> str:
    weight = w if w is not None else (700 if b else 500)
    spacing = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="{weight}" fill="{c}" '
            f'text-anchor="{a}" font-family="{FONT}"{spacing}>{E(s)}</text>')


def lines(x: float, y: float, ls: list[str], *, lh: float = 14, **kw) -> str:
    return "".join(text(x, y + i * lh, l, **kw) for i, l in enumerate(ls))


def pill(x: float, y: float, s: str, h: str, *, fs: float = 13, w: float | None = None,
         hh: float | None = None, r: float | None = None, fill: str | None = None,
         c: str = ON, stroke: str = "") -> tuple[float, float, str]:
    """A solid pill with centred bold text. Returns (width, height, markup)."""
    pw = w or width(s, fs)
    ph = hh or fs + 14
    rr = ph / 2 if r is None else r
    st = f' stroke="{stroke}" stroke-width="1.6"' if stroke else ""
    m = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{pw:.1f}" height="{ph:.1f}" rx="{rr}" fill="{fill or solid(h)}"{st}/>'
         + text(x + pw / 2, y + ph / 2 + fs * 0.36, s, a="middle", fs=fs, b=True, c=c))
    return pw, ph, m


def title(x: float, y: float, parts: list[tuple[str, str] | tuple[str]], *, fs: float = 22) -> str:
    """The title row: a green accent bar, then pills for the subjects and plain bold text between."""
    cx, m = x, f'<rect x="{x - 14}" y="{y - 4}" width="5" height="{fs + 18}" rx="2.5" fill="{solid("g")}"/>'
    for p in parts:
        if len(p) == 1:
            m += text(cx + 10, y + fs * 0.98, p[0], fs=fs - 2, b=True)
            cx += width(p[0], fs - 2) - 8
        else:
            pw, _, pm = pill(cx, y, p[0], p[1], fs=fs, r=8, hh=fs + 16)
            m += pm
            cx += pw + 12
    return m


def panel(x: float, y: float, w: float, h: float, hue: str, *, r: float = 18) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{tint(hue)}" '
            f'stroke="{border(hue)}" stroke-width="2"/>')


def label_col(x: float, y: float, w: float, h: float, hue: str, *, name: str, sub: str = "",
              icon: str = "", fs: float = 19) -> str:
    """The solid column at the left of a panel: icon, name in white, one-line definition."""
    ls = wrap(sub, int(w / 6.6)) if sub else []
    m = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{solid(hue)}"/>'
    cy = y + h / 2
    if icon:
        m += icon_(icon, x + w / 2, cy - 46, 44, c=ON, ink=ON, fill="rgba(255,255,255,.22)")
    m += text(x + w / 2, cy + 20, name, a="middle", fs=fs, b=True, c=ON)
    m += lines(x + w / 2, cy + 40, ls, a="middle", fs=11.5, c=ON, w=600, lh=13.5)
    return m


def node(x: float, y: float, w: float, h: float, *, title_: str, sub: str = "", icon: str = "",
         hue: str = "n", fs: float = 12.5, r: float = 12, href: str = "", sw: float = 1.8,
         fill: str = NODE) -> str:
    """A white node: flat icon at the left, bold title, grey subtitle. Two lines each at most."""
    tx = x + 52 if icon else x + 12
    tl = wrap(title_, int((w - (58 if icon else 20)) / 6.4))[:2]
    sl = wrap(sub, int((w - (58 if icon else 20)) / 5.6))[:2] if sub else []
    ty = y + h / 2 - (len(tl) + len(sl) - 1) * 6.5 + 4
    m = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
         f'stroke="{solid(hue)}" stroke-width="{sw}"/>')
    if icon:
        m += icon_(icon, x + 28, y + h / 2 - 16, 32, c=solid(hue), ink=INK, fill=tint(hue))
    m += lines(tx, ty, tl, fs=fs, b=True)
    if sl:
        m += lines(tx, ty + len(tl) * 14, sl, fs=10.5, c=INK2, lh=12.5)
    if href:
        return f'<a href="{E(href)}">{m}</a>'
    return m


def num(x: float, y: float, n: int | str, hue: str = "b") -> str:
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="{tint(hue)}" stroke="{INK}" stroke-width="1.5"/>'
            + text(x, y + 4, str(n), a="middle", fs=11, b=True))


def flow(pts: list[tuple[float, float]], *, c: str = INK, sw: float = 2, solid_: bool = False,
         head: bool = True, label: str = "", lx: float = 0, ly: float = -8) -> str:
    """A dashed connector with a filled arrowhead. Dashed means flow; ``solid_`` is for containment."""
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
        i = (len(pts) - 1) // 2
        mx = (pts[i][0] + pts[i + 1][0]) / 2 + lx
        my = (pts[i][1] + pts[i + 1][1]) / 2 + ly
        w = width(label, 10.5) - 8
        m += (f'<rect x="{mx - w / 2:.1f}" y="{my - 11:.1f}" width="{w:.1f}" height="17" rx="8.5" '
              f'fill="{NODE}" stroke="{INK}" stroke-width="1" opacity=".97"/>'
              + text(mx, my + 1.5, label, a="middle", fs=10.5, b=True))
    return m


def callout(x: float, y: float, w: float, s: str, hue: str, *, h: float | None = None,
            fs: float = 11.5) -> str:
    ls = wrap(s, int(w / 6.2))
    hh = h or len(ls) * 14 + 18
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="10" fill="{tint(hue)}" '
            f'stroke="{border(hue)}" stroke-width="1.6"/>'
            + lines(x + w / 2, y + 18 + (hh - (len(ls) * 14 + 18)) / 2, ls, a="middle", fs=fs, b=True))


def listbox(x: float, y: float, w: float, head: str, items: list[str], hue: str,
            *, h: float | None = None) -> str:
    """"Best for" / "Workflow" / "Examples": a white box with a tinted heading pill and a numbered list."""
    pw, _, pm = pill(x, y, head, hue, fs=12, r=8, hh=24, c=INK, fill=tint(hue), stroke=border(hue))
    m = (f'<rect x="{x}" y="{y + 12}" width="{w}" height="{h or len(items) * 30 + 30}" rx="12" '
         f'fill="{NODE}" stroke="{border(hue)}" stroke-width="1.6"/>' + pm)
    yy = y + 44
    for i, it in enumerate(items):
        ls = wrap(it, int((w - 40) / 5.9))[:2]
        m += text(x + 12, yy + 4, f"{i + 1}.", fs=11, b=True) + lines(x + 28, yy + 4, ls, fs=11, w=500, lh=12.5)
        yy += 30 if len(ls) > 1 else 22
    return m


def gate(x: float, y: float, h: float, *, hard: bool = True, label: str = "") -> str:
    """The wall the flow has to get through. Hard is pink and solid; soft is orange and dashed."""
    hue = "k" if hard else "o"
    dash = "" if hard else ' stroke-dasharray="6 5"'
    m = (f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + h}" stroke="{solid(hue)}" stroke-width="3"{dash}/>'
         f'<rect x="{x - 12}" y="{y + h / 2 - 16}" width="24" height="32" rx="6" fill="{solid(hue)}"/>'
         f'<path d="M{x - 6} {y + h / 2 - 4}h12M{x - 6} {y + h / 2 + 4}h12" stroke="{ON}" stroke-width="2.4" stroke-linecap="round"/>')
    if label:
        m += text(x, y + h + 14, label, a="middle", fs=10.5, b=True, c=dark(hue))
    return m


def svg(w: float, h: float, inner: str, label: str, *, caption: str = "", cls: str = "") -> str:
    """The frame: a figure with the drawing and an optional caption underneath."""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    role = "group" if "<a " in inner else "img"   # an image may not contain links; a group may
    return (f'<figure class="bbw{(" " + cls) if cls else ""}"><svg class="bb" viewBox="0 0 {w} {h}" role="{role}" '
            f'aria-label="{E(label)}">{inner}</svg>{cap}</figure>')


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
        "shield": f'<path d="M16 3l11 4v9c0 7-5 11-11 13C10 27 5 23 5 16V7z" fill="{c}"/><path d="M11 16l3.5 3.5L21 13" stroke="#fff" stroke-width="2.6"/>',
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
        "check": f'<circle cx="16" cy="16" r="12" fill="{c}"/><path d="M10 16l4 4 8-8" stroke="#fff" stroke-width="2.8"/>',
        "eye": f'<path d="M3 16s5-8 13-8 13 8 13 8-5 8-13 8S3 16 3 16z" fill="{f}"/><circle cx="16" cy="16" r="4" fill="{c}"/>',
        "gate": f'<rect x="4" y="12" width="24" height="8" rx="2" fill="{c}"/><path d="M8 12V6M24 12V6M8 20v7M24 20v7"/>',
        "users": f'<circle cx="11" cy="10" r="5" fill="{f}"/><circle cx="22" cy="12" r="4" fill="{c}"/><path d="M3 28c1-6 4-9 8-9s7 3 8 9" fill="{f}"/><path d="M19 28c0-4 2-7 4-8 3 0 5 3 6 8" fill="{c}"/>',
        "ladder": f'<path d="M9 4v24M23 4v24"/><path d="M9 9h14M9 16h14M9 23h14" stroke="{c}" stroke-width="3"/>',
        "mag": f'<circle cx="13" cy="13" r="8" fill="{f}"/><path d="M19 19l9 9" stroke="{c}" stroke-width="3.4"/><path d="M13 9v8M9 13h8" stroke="{c}"/>',
        "target": f'<circle cx="16" cy="16" r="12" fill="{f}"/><circle cx="16" cy="16" r="7" fill="{c}"/><circle cx="16" cy="16" r="2.5" fill="#fff" stroke="none"/>',
        "handoff": f'<path d="M4 20c4-6 8-6 12 0s8 6 12 0" stroke="{c}" stroke-width="3"/><path d="M22 14l6 6-6 6"/>',
        "loop": f'<path d="M6 16a10 10 0 0 1 17-7" stroke="{c}" stroke-width="3"/><path d="M26 16a10 10 0 0 1-17 7" stroke="{c}" stroke-width="3"/><path d="M23 4v6h-6M9 28v-6h6"/>',
        "lock": f'<rect x="6" y="14" width="20" height="14" rx="3" fill="{c}"/><path d="M10 14V9a6 6 0 0 1 12 0v5" fill="{f}"/><circle cx="16" cy="21" r="2" fill="#fff" stroke="none"/>',
        "undo": f'<path d="M10 8H4v6" /><path d="M4 14a12 12 0 1 1 3 9" stroke="{c}" stroke-width="3"/>',
        "stop": f'<path d="M10 3h12l7 7v12l-7 7H10l-7-7V10z" fill="{c}"/><path d="M11 16h10" stroke="#fff" stroke-width="3"/>',
        "warn": f'<path d="M16 4L29 27H3z" fill="{c}"/><path d="M16 12v7M16 22v1.5" stroke="#fff" stroke-width="2.8"/>',
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
