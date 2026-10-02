"""Figures for a step's worked example.

A step earns a figure when the shape of the thing is the lesson, a bar sheet, a prompt layout, a
ten-day cut, a widening cut-over. Where prose is clearer, the step has no figure, which is most of
them. All share one frame so a role page reads as one document, and all use theme tokens so they
follow light and dark.

Each figure is drawn twice: on a 560-unit canvas for a column of 520px or more, and on a 260-unit
canvas, re-set upright, for anything narrower. No label is under 12.5 units on the first or 13 on
the second, so none is under 11px on screen at any width. base.css swaps the two on the figure's own
width. The sentences that used to be drawn inside the picture are text under it (``notes``): text
wraps, a drawing cannot.

A label drawn in a hue sits on that hue's own tint, where the light theme's hue alone reads 3.4 to
4.5 to 1. ``_label`` deepens it toward the ink by ``--dg-text`` (base.css: 78% of the hue in the light
theme, all of it in the dark), so every label reads 4.5 to 1 or more and the tints stay as they are.
"""
from __future__ import annotations

import html

from .bb import tw

E = lambda s: html.escape(str(s), quote=False)  # noqa: E731
W, NW = 560, 260
F, NF = 12.5, 13            # the smallest type on the wide canvas and on the narrow one
ROSE = "color-mix(in oklab,var(--dg-rose) 82%,var(--ink))"


def _svg(wide: tuple[int, str], narrow: tuple[int, str], label: str, caption: str,
         notes: list[tuple[str, bool]] | None = None) -> str:
    """The frame. ``wide`` and ``narrow`` are (height, markup); ``notes`` are the sentences under
    the drawing, each (text, whether it is the warning)."""
    (h, inner), (nh, ninner) = wide, narrow
    ns = "".join(f'<p class="fn{" hot" if hot else ""}">{E(t)}</p>' for t, hot in (notes or []))
    return (f'<figure class="fig"><svg class="w" viewBox="0 0 {W} {h}" role="img" aria-label="{E(label)}">{inner}</svg>'
            f'<svg class="n" viewBox="0 0 {NW} {nh}" role="img" aria-label="{E(label)}">{ninner}</svg>'
            f"{ns}<figcaption>{E(caption)}</figcaption></figure>")


def _label(fill: str) -> str:
    """The colour a label is drawn in. A hue keeps ``--dg-text`` of itself and takes the rest from the
    ink; the ink, the ink that sits on a solid hue and a colour already deepened with ink stay as given."""
    if fill in ("currentColor", "var(--dg-on)") or "var(--ink)" in fill:
        return fill
    return f"color-mix(in oklab,{fill} var(--dg-text),var(--ink))"


def _t(x: float, y: float, s: str, fs: float = F, *, a: str = "start", w: int = 0, fill: str = "currentColor",
       op: float = 0, mono: bool = False) -> str:
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}"'
            + (f' text-anchor="{a}"' if a != "start" else "")
            + (f' font-weight="{w}"' if w else "")
            + (' font-family="ui-monospace,SFMono-Regular,Menlo,monospace"' if mono else "")
            + f' fill="{_label(fill)}"' + (f' opacity="{op}"' if op else "") + f">{E(s)}</text>")


def bar_sheet() -> str:
    rows = [("same-day", 50, "$4 / $4", "var(--dg-teal)"),
            ("codeshare", 80, "$9 / $36", "var(--dg-indigo)"),
            ("refund, unheld", 98, "$12 / $600", "var(--dg-rose)"),
            ("refund, with a hold", 71, "$12 / $30", "var(--dg-green)")]
    out = ['<line x1="150" y1="14" x2="150" y2="164" stroke="currentColor" opacity=".18"/>']
    for i, (name, bar, costs, colour) in enumerate(rows):
        y = 24 + i * 36
        w = (bar / 100) * 300          # leaves room for the cost column at the right
        out.append(_t(142, y + 15.5, name, a="end"))
        out.append(f'<rect x="150" y="{y}" width="{w:.0f}" height="22" rx="3" fill="{colour}" opacity=".95"/>')
        # A wide bar carries its own label inside it; a narrow one sets it just outside.
        if w > 235:
            out.append(_t(144 + w, y + 15.5, f"{bar}%", a="end", w=700, fill="var(--dg-on)"))
        else:
            out.append(_t(156 + w, y + 15.5, f"{bar}%", w=700, fill=colour))
        out.append(_t(546, y + 15.5, costs, a="end", op=.8))
    # the hold joins the unheld refund (row 3) to the held one (row 4); its name sits beside the
    # curve's apex, between the two cost figures
    out.append('<path d="M452 107 C474 107 474 143 402 143" fill="none" stroke="var(--dg-green)" '
               'stroke-width="1.6" stroke-dasharray="3 3"/>')
    out.append(_t(476, 130, "the hold", w=600, fill="var(--dg-green)"))
    # narrow: the name and the costs on one line, the bar under them
    n = []
    for i, (name, bar, costs, colour) in enumerate(rows):
        y = 6 + i * 48
        w = (bar / 100) * 206
        n.append(_t(8, y + 13, name, NF))
        n.append(_t(252, y + 13, costs, NF, a="end", op=.8))
        n.append(f'<rect x="8" y="{y + 20}" width="{w:.0f}" height="20" rx="3" fill="{colour}" opacity=".95"/>')
        if w > 150:
            n.append(_t(8 + w - 6, y + 34.5, f"{bar}%", NF, a="end", w=700, fill="var(--dg-on)"))
        else:
            n.append(_t(8 + w + 6, y + 34.5, f"{bar}%", NF, w=700, fill=colour))
    return _svg((176, "".join(out)), (196, "".join(n)),
                "Four slices with their derived bars, the held refund far below the unheld one",
                "The bar is derived per slice from damage and saving. A hold cuts the damage, "
                "so it cuts the bar.")


def chain() -> str:
    def draw(x0, bw, pitch, fs, top, hgt):
        o = [_t(x0, top - 14, "each step 90% right", fs, op=.78)]
        for i in range(6):
            x = x0 + i * pitch
            o.append(f'<rect x="{x}" y="{top}" width="{bw}" height="34" rx="5" fill="var(--dg-indigo)" '
                     f'fill-opacity=".14" stroke="var(--dg-indigo)"/>')
            o.append(_t(x + bw / 2, top + 22, "0.9", fs, a="middle", fill="var(--dg-indigo)"))
            if i < 5:
                o.append(_t(x + (bw + pitch) / 2, top + 22, "×", fs, a="middle", op=.78))
        pts = []
        base = top + 34 + hgt
        for n in range(1, 7):
            p = 0.9 ** n
            px, py = x0 + bw / 2 + (n - 1) * pitch, base - 4 - p * (hgt - 44)
            pts.append(f"{px:.0f},{py:.0f}")
            o.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3.4" fill="var(--dg-rose)"/>')
            o.append(_t(px, py - 9, f"{p * 100:.0f}%", fs, a="middle", w=600, fill=ROSE))
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="var(--dg-rose)" stroke-width="1.8"/>')
        o.append(f'<line x1="{x0}" y1="{base}" x2="{x0 + 5 * pitch + bw}" y2="{base}" stroke="currentColor" opacity=".18"/>')
        return base + 8, "".join(o)
    return _svg(draw(12, 56, 96, F, 34, 116), draw(5, 30, 44, NF, 30, 124),
                "Six steps at ninety percent, with the end-to-end rate falling to fifty-three percent",
                "Chained steps multiply. Four at 90% is 66%, and it fails fluently.")


def cache_prefix() -> str:
    blocks = [("tools", 96), ("system", 88), ("shared context", 124), ("domain context", 120)]
    ind = "var(--dg-indigo)"
    out, x = [], 10
    for name, w in blocks:
        out.append(f'<rect x="{x}" y="36" width="{w}" height="40" rx="4" fill="{ind}" fill-opacity=".16" stroke="{ind}"/>')
        out.append(_t(x + w / 2, 61, name, a="middle", fill=ind))
        x += w + 6
    out.append(f'<line x1="{x - 3}" y1="24" x2="{x - 3}" y2="90" stroke="var(--dg-amber)" stroke-width="2.5"/>')
    out.append(_t(x - 3, 18, "cache marker", a="middle", w=700, fill="var(--dg-amber)"))
    out.append(f'<rect x="{x + 4}" y="36" width="{548 - x}" height="40" rx="4" fill="var(--dg-rose)" '
               f'fill-opacity="{.13}" stroke="var(--dg-rose)" stroke-dasharray="4 3"/>')
    out.append(_t(x + 4 + (548 - x) / 2, 61, "the request", a="middle", fill=ROSE))
    out.append(_t(10, 108, "stable: written once at 1.25×, read at 0.1×", op=.8))
    # narrow: the prompt top to bottom, the marker a line across it
    n, y = [], 6
    for name, _w in blocks:
        n.append(f'<rect x="8" y="{y}" width="244" height="30" rx="4" fill="{ind}" fill-opacity=".16" stroke="{ind}"/>')
        n.append(_t(130, y + 19.5, name, NF, a="middle", fill=ind))
        y += 35
    n.append(f'<line x1="8" y1="{y + 16}" x2="252" y2="{y + 16}" stroke="var(--dg-amber)" stroke-width="2.5"/>')
    n.append(_t(8, y + 9, "stable above", NF, op=.8))
    n.append(_t(252, y + 9, "cache marker", NF, a="end", w=700, fill="var(--dg-amber)"))
    y += 26
    n.append(f'<rect x="8" y="{y}" width="244" height="30" rx="4" fill="var(--dg-rose)" fill-opacity=".13" '
             f'stroke="var(--dg-rose)" stroke-dasharray="4 3"/>')
    n.append(_t(130, y + 19.5, "the request", NF, a="middle", fill=ROSE))
    return _svg((120, "".join(out)), (y + 38, "".join(n)),
                "A prompt laid out as tools, system and context before the cache marker, request after",
                "The cache matches an exact prefix. Stable first, marker, then whatever changes.",
                notes=[("Move the request before the marker and no two calls share a prefix.", False),
                       ("The hit ratio goes to zero and the caching line item still says it is on.", True)])


def bolt_days() -> str:
    bolts = [("walking skeleton", "var(--dg-teal)"), ("fare maths", "var(--dg-indigo)"),
             ("eligibility rules", "var(--dg-indigo)"), ("ranking", "var(--dg-indigo)"),
             ("checker", "var(--dg-indigo)"), ("MCP server", "var(--dg-amber)"),
             ("rebook (gated)", "var(--dg-amber)"), ("refund (gated)", "var(--dg-rose)"),
             ("shadow path", "var(--dg-violet)"), ("harness", "var(--dg-violet)")]
    # wide: two weeks, five days each
    out = []
    for d, (name, colour) in enumerate(bolts):
        r, c = divmod(d, 5)
        x, y = 10 + c * 110, 22 + r * 76
        out.append(_t(x + 2, y - 5, f"day {d + 1}", op=.8))
        out.append(f'<rect x="{x}" y="{y}" width="100" height="40" rx="5" fill="{colour}" fill-opacity=".17" stroke="{colour}"/>')
        words = name.split()
        ls = [name] if tw(name, F) <= 90 else [words[0], " ".join(words[1:])]
        for i, l in enumerate(ls):
            out.append(_t(x + 50, y + (24.5 if len(ls) == 1 else 17 + i * 15), l, a="middle"))
        if c < 4:
            out.append(f'<path d="M{x + 101} {y + 20} h8" stroke="currentColor" opacity=".4" stroke-width="1.4"/>')
    # narrow: ten days down the page
    n = []
    for d, (name, colour) in enumerate(bolts):
        y = 4 + d * 31
        n.append(_t(8, y + 17.5, f"day {d + 1}", NF, op=.8))
        n.append(f'<rect x="58" y="{y}" width="194" height="26" rx="5" fill="{colour}" fill-opacity=".17" stroke="{colour}"/>')
        n.append(_t(68, y + 17.5, name, NF))
    return _svg((146, "".join(out)), (4 + 10 * 31 + 2, "".join(n)), "Ten daily bolts in dependency order across two weeks",
                "The cut is by dependency, not by priority. One unknown per day.",
                notes=[("Skeleton first with no model in it. Exact code early: it stands alone.", False),
                       ("The plug lands before the gated write that needs it. The proof goes last.", False),
                       ("A bolt that cannot be built alone was cut wrong. Say so before you start it.", True)])


def shadow_widen() -> str:
    stages = [("shadow", "decides, never acts", "var(--soft)"),
              ("5%", "12 cases a day", "var(--dg-amber)"),
              ("25%", "60 a day", "var(--dg-indigo)"),
              ("100%", "widened on evidence", "var(--dg-green)")]
    # wide: each box as wide as its words need, the spare shared out
    need = [max(tw(a, 15, 700), tw(b, F)) + 22 for a, b, _c in stages]
    spare = (W - 20 - 3 * 24 - sum(need)) / 4
    out, x = [], 10
    for i, (name, sub, colour) in enumerate(stages):
        w = need[i] + spare
        out.append(f'<rect x="{x:.0f}" y="12" width="{w:.0f}" height="50" rx="6" fill="{colour}" fill-opacity=".15" stroke="{colour}"/>')
        out.append(_t(x + w / 2, 34, name, 15, a="middle", w=700, fill=colour))
        out.append(_t(x + w / 2, 52, sub, a="middle", op=.8))
        if i < 3:
            out.append(f'<path d="M{x + w + 4:.0f} 37 h13" stroke="currentColor" opacity=".45" stroke-width="1.6"/>')
            out.append(f'<path d="M{x + w + 13:.0f} 33 l5 4 -5 4" fill="none" stroke="currentColor" opacity=".45" stroke-width="1.6"/>')
        x += w + 24
    # narrow: the four stages down the page
    n = []
    for i, (name, sub, colour) in enumerate(stages):
        y = 4 + i * 56
        n.append(f'<rect x="8" y="{y}" width="244" height="38" rx="6" fill="{colour}" fill-opacity=".15" stroke="{colour}"/>')
        n.append(_t(20, y + 24.5, name, 15, w=700, fill=colour))
        n.append(_t(240, y + 24, sub, NF, a="end", op=.8))
        if i < 3:
            n.append(f'<path d="M130 {y + 41} v10" stroke="currentColor" opacity=".45" stroke-width="1.6"/>')
            n.append(f'<path d="M126 {y + 47} l4 5 4 -5" fill="none" stroke="currentColor" opacity=".45" stroke-width="1.6"/>')
    return _svg((74, "".join(out)), (4 + 3 * 56 + 38 + 6, "".join(n)), "Shadow, then five percent, then twenty-five, then full traffic",
                "The safe share is the slow one. That is why a cut-over widens.",
                notes=[("Each arrow is a condition, never a date.", False),
                       ("500 cases at 5% of 240 a day takes 42 days. That is arithmetic, not effort.", False),
                       ("Money actions stay gated at every stage, whatever the shadow shows.", True)])


def bill_factors() -> str:
    facs = [("context", "1.6", "2,100→3,360", "tokens"), ("tier", "1.5", "50%→100%", "frontier"),
            ("cache", "1.3", "71%→9% hit,", "f = 0.40"), ("attempts", "1.42", "1.2→1.7", "per case")]
    amber = "var(--dg-amber)"

    def box(x, y, w, fs, name, v, s1, s2):
        return (_t(x + w / 2, y - 6, name, fs, a="middle", op=.8)
                + f'<rect x="{x}" y="{y}" width="{w}" height="74" rx="6" fill="{amber}" fill-opacity=".16" stroke="{amber}"/>'
                + _t(x + w / 2, y + 26, v, 20, a="middle", w=700, fill=amber)
                + _t(x + w / 2, y + 46, s1, fs, a="middle", op=.8) + _t(x + w / 2, y + 62, s2, fs, a="middle", op=.8))
    out = []
    for i, (name, v, s1, s2) in enumerate(facs):
        x = 10 + i * 138
        out.append(box(x, 22, 116, F, name, v, s1, s2))
        if i < 3:
            out.append(_t(x + 127, 64, "×", 15, a="middle", op=.8))
    out.append(_t(280, 126, "= 4.4× the estimate, on flat traffic", 18, a="middle", w=700, fill=ROSE))
    # narrow: two by two
    n = []
    for i, (name, v, s1, s2) in enumerate(facs):
        r, c = divmod(i, 2)
        x, y = 8 + c * 134, 22 + r * 102
        n.append(box(x, y, 110, NF, name, v, s1, s2))
        if c == 0:
            n.append(_t(130, y + 42, "×", 15, a="middle", op=.8))
    n.append(_t(130, 114, "×", 15, a="middle", op=.8))
    n.append(_t(130, 226, "= 4.4× the estimate,", 17, a="middle", w=700, fill=ROSE))
    n.append(_t(130, 247, "on flat traffic", 17, a="middle", w=700, fill=ROSE))
    return _svg((140, "".join(out)), (258, "".join(n)), "Four cost factors multiplying to four point four times",
                "They multiply. The largest ratio change is not the largest factor.",
                notes=[("Four ordinary habits, each a sensible decision by a careful person.", False),
                       ("Fix in order of (factor − 1) ÷ days: context, tier, cache, then the breaker.", False)])


def authority_ladder() -> str:
    # A monotone ramp: the hue carries the risk, so the ordering reads before the labels
    # do. Tokens, never literals, or the ladder stays light against a dark page.
    deep = "color-mix(in oklab,var(--dg-rose) 74%,var(--ink))"
    rows = [("R1", "search_flights", "read only", "nothing", "var(--dg-slate)"),
            ("R2", "draft_message", "reversible", "one reader", "var(--dg-sky)"),
            ("R3", "rebook(...)", "hard to reverse", "approve first", "var(--dg-amber)"),
            ("R4", "issue_refund(≤400)", "money", "named approver", "var(--dg-rose)"),
            ("R5", "change_identity", "irreversible", "not delegated", deep)]
    out = []
    for i, (band, tool, kind, check, colour) in enumerate(rows):
        y = 8 + i * 36
        out.append(f'<rect x="10" y="{y}" width="{176 + i * 22}" height="28" rx="5" fill="{colour}" fill-opacity=".15" stroke="{colour}"/>')
        out.append(_t(21, y + 18.5, band, 13, w=700, fill=colour))
        out.append(_t(48, y + 18.5, tool, mono=True, op=.85))
        out.append(_t(300, y + 18.5, kind, op=.8))
        out.append(_t(550, y + 18.5, check, a="end", w=600, fill=colour))
    # narrow: the band and its tool on the bar, what it is and its check under it
    n = []
    for i, (band, tool, kind, check, colour) in enumerate(rows):
        y = 4 + i * 54
        n.append(f'<rect x="8" y="{y}" width="{188 + i * 14}" height="26" rx="5" fill="{colour}" fill-opacity=".15" stroke="{colour}"/>')
        n.append(_t(17, y + 17.5, band, NF, w=700, fill=colour))
        n.append(_t(42, y + 17.5, tool, 12.5, mono=True, op=.85))
        n.append(_t(10, y + 42, kind, NF, op=.8))
        n.append(_t(252, y + 42, check, NF, a="end", w=600, fill=colour))
    return _svg((190, "".join(out)), (4 + 5 * 54, "".join(n)),
                "Five risk bands from a read tool to an identity change, each with its check",
                "The band belongs to the tool. A change inherits the band of whatever it touches.")


def two_numbers() -> str:
    # a row with no baseline says so in a word: tokens and re-runs did not exist before the agent did
    rows = [("person-days per story", "8.0", "4.6", "−43%", "var(--dg-green)"),
            ("token spend per story", "none", "$310", "", "var(--dg-amber)"),
            ("review hours added", "1.2", "2.0", "+0.8", "var(--dg-amber)"),
            ("re-runs per story", "none", "1.4", "", "var(--soft)")]
    out = ['<rect x="10" y="6" width="540" height="128" rx="8" fill="var(--paper)" stroke="var(--rule)"/>']
    for x, hd in ((332, "baseline"), (420, "now"), (530, "change")):
        out.append(_t(x, 27, hd, a="end", op=.8))
    for i, (name, a, b, c, colour) in enumerate(rows):
        y = 51 + i * 23
        out.append(_t(26, y, name, op=.9))
        out.append(_t(332, y, a, a="end", op=.8))
        out.append(_t(420, y, b, a="end", w=600))
        out.append(_t(530, y, c, a="end", w=700, fill=colour))
    # narrow: the name on one line, its three figures under it
    n = ['<rect x="4" y="4" width="252" height="216" rx="8" fill="var(--paper)" stroke="var(--rule)"/>']
    for x, hd in ((110, "baseline"), (176, "now"), (246, "change")):
        n.append(_t(x, 24, hd, NF, a="end", op=.8))
    for i, (name, a, b, c, colour) in enumerate(rows):
        y = 48 + i * 44
        n.append(_t(14, y, name, NF, op=.9))
        n.append(_t(110, y + 19, a, NF, a="end", op=.8))
        n.append(_t(176, y + 19, b, NF, a="end", w=600))
        n.append(_t(246, y + 19, c, NF, a="end", w=700, fill=colour))
    return _svg((140, "".join(out)), (224, "".join(n)), "A cycle report with four rows: person-days, tokens, review hours, re-runs",
                "Two numbers, and the two rows that stop either being gamed.",
                notes=[("The review row and the re-run row are what keep the first number honest.", False),
                       ("The programme is cancelled on the number you hid, never the one you showed.", True)])


FIGURES = {
    "bar_sheet": bar_sheet, "chain": chain, "cache_prefix": cache_prefix, "bolt_days": bolt_days,
    "shadow_widen": shadow_widen, "bill_factors": bill_factors,
    "authority_ladder": authority_ladder, "two_numbers": two_numbers,
}
