"""Figures for a step's worked example.

A step earns a figure when the shape of the thing is the lesson — a bar sheet, a prompt layout, a
ten-day cut, a widening cut-over. Where prose is clearer, the step has no figure, which is most of
them. All share one frame so a role page reads as one document, and all use theme tokens so they
follow light and dark.
"""
from __future__ import annotations

import html

E = lambda s: html.escape(str(s), quote=False)  # noqa: E731
W, H = 560, 190


def _svg(inner: str, label: str, caption: str) -> str:
    return (f'<figure class="fig"><svg viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{E(label)}">{inner}</svg>'
            f"<figcaption>{E(caption)}</figcaption></figure>")


def bar_sheet() -> str:
    rows = [("same-day", 50, "$4 / $4", "var(--dg-teal)"),
            ("codeshare", 80, "$9 / $36", "var(--dg-indigo)"),
            ("refund, unheld", 98, "$12 / $600", "var(--dg-rose)"),
            ("refund, with a hold", 71, "$12 / $30", "var(--dg-green)")]
    out = ['<line x1="150" y1="16" x2="150" y2="168" stroke="currentColor" opacity=".18"/>']
    for i, (name, bar, costs, colour) in enumerate(rows):
        y = 26 + i * 36
        w = (bar / 100) * 300          # leaves room for the cost column at the right
        out.append(f'<text x="142" y="{y+15}" text-anchor="end" font-size="12" '
                   f'fill="currentColor">{name}</text>')
        out.append(f'<rect x="150" y="{y}" width="{w:.0f}" height="21" rx="3" fill="{colour}" '
                   f'opacity=".78"/>')
        # A wide bar carries its own label inside it; a narrow one sets it just outside.
        if w > 235:
            out.append(f'<text x="{144+w:.0f}" y="{y+15}" text-anchor="end" font-size="12" '
                       f'font-weight="700" fill="var(--dg-on)">{bar}%</text>')
        else:
            out.append(f'<text x="{156+w:.0f}" y="{y+15}" font-size="12" font-weight="700" '
                       f'fill="{colour}">{bar}%</text>')
        out.append(f'<text x="544" y="{y+15}" text-anchor="end" font-size="10.5" '
                   f'fill="currentColor" opacity=".55">{costs}</text>')
    # the hold joins the unheld refund (row 3) to the held one (row 4)
    out.append('<path d="M462 108 C496 108 496 144 402 144" fill="none" stroke="var(--dg-green)" '
               'stroke-width="1.6" stroke-dasharray="3 3"/>')
    out.append('<text x="498" y="130" text-anchor="middle" font-size="11" fill="var(--dg-green)" '
               'font-weight="600">the hold</text>')
    return _svg("".join(out),
                "Four slices with their derived bars, the held refund far below the unheld one",
                "The bar is derived per slice from damage and saving. A hold cuts the damage, "
                "so it cuts the bar.")


def chain() -> str:
    out = ['<text x="12" y="20" font-size="11" fill="currentColor" opacity=".6">each step 90% right</text>']
    x = 12
    for i in range(6):
        out.append(f'<rect x="{x}" y="34" width="56" height="34" rx="5" fill="var(--dg-indigo)" '
                   f'fill-opacity=".14" stroke="var(--dg-indigo)"/>')
        out.append(f'<text x="{x+28}" y="56" text-anchor="middle" font-size="12" fill="var(--dg-indigo)">0.9</text>')
        if i < 5:
            out.append(f'<text x="{x+66}" y="56" text-anchor="middle" font-size="12" fill="currentColor" '
                       f'opacity=".4">×</text>')
        x += 80
    pts = []
    for n in range(1, 7):
        p = 0.9 ** n
        px, py = 40 + (n - 1) * 80, 170 - p * 76
        pts.append(f"{px},{py:.0f}")
        out.append(f'<circle cx="{px}" cy="{py:.0f}" r="3.4" fill="var(--dg-rose)"/>')
        out.append(f'<text x="{px}" y="{py-8:.0f}" text-anchor="middle" font-size="11" '
                   f'font-weight="600" fill="var(--dg-rose)">{p*100:.0f}%</text>')
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="var(--dg-rose)" stroke-width="1.8"/>')
    out.append('<line x1="12" y1="172" x2="548" y2="172" stroke="currentColor" opacity=".18"/>')
    return _svg("".join(out),
                "Six steps at ninety percent, with the end-to-end rate falling to fifty-three percent",
                "Chained steps multiply. Four at 90% is 66%, and it fails fluently.")


def cache_prefix() -> str:
    blocks = [("tools", 96, "var(--dg-indigo)"), ("system", 88, "var(--dg-indigo)"),
              ("shared context", 120, "var(--dg-indigo)"), ("domain context", 116, "var(--dg-indigo)")]
    out, x = [], 12
    for name, w, colour in blocks:
        out.append(f'<rect x="{x}" y="46" width="{w}" height="40" rx="4" fill="{colour}" '
                   f'fill-opacity=".16" stroke="{colour}"/>')
        out.append(f'<text x="{x+w/2:.0f}" y="71" text-anchor="middle" font-size="11.5" fill="{colour}">{name}</text>')
        x += w + 6
    out.append(f'<line x1="{x-3}" y1="34" x2="{x-3}" y2="100" stroke="var(--dg-amber)" stroke-width="2.5"/>')
    out.append(f'<text x="{x-3}" y="28" text-anchor="middle" font-size="10.5" font-weight="700" '
               f'fill="var(--dg-amber)">cache marker</text>')
    out.append(f'<rect x="{x+4}" y="46" width="{540-x}" height="40" rx="4" fill="var(--dg-rose)" '
               f'fill-opacity=".13" stroke="var(--dg-rose)" stroke-dasharray="4 3"/>')
    out.append(f'<text x="{x+4+(540-x)/2:.0f}" y="71" text-anchor="middle" font-size="11.5" '
               f'fill="var(--dg-rose)">the request</text>')
    out.append('<text x="12" y="120" font-size="11" fill="currentColor" opacity=".62">'
               'stable — written once at 1.25×, read at 0.1×</text>')
    out.append('<text x="12" y="150" font-size="11.5" fill="currentColor" opacity=".8">'
               'Move the request before the marker and no two calls share a prefix.</text>')
    out.append('<text x="12" y="168" font-size="11.5" fill="var(--dg-rose)" opacity=".9">'
               'The hit ratio goes to zero and the caching line item still says it is on.</text>')
    return _svg("".join(out),
                "A prompt laid out as tools, system and context before the cache marker, request after",
                "The cache matches an exact prefix. Stable first, marker, then whatever changes.")


def bolt_days() -> str:
    bolts = [("walking skeleton", 0, "var(--dg-teal)"), ("fare maths", 1, "var(--dg-indigo)"),
             ("eligibility rules", 2, "var(--dg-indigo)"), ("ranking", 3, "var(--dg-indigo)"),
             ("checker", 4, "var(--dg-indigo)"), ("MCP server", 5, "var(--dg-amber)"),
             ("rebook (gated)", 6, "var(--dg-amber)"), ("refund (gated)", 7, "var(--dg-rose)"),
             ("shadow path", 8, "var(--dg-violet)"), ("harness", 9, "var(--dg-violet)")]
    out = []
    for name, d, colour in bolts:
        x = 12 + d * 54
        out.append(f'<rect x="{x}" y="42" width="48" height="52" rx="5" fill="{colour}" fill-opacity=".17" '
                   f'stroke="{colour}"/>')
        out.append(f'<text x="{x+24}" y="36" text-anchor="middle" font-size="10" fill="currentColor" '
                   f'opacity=".55">day {d+1}</text>')
        for wi, word in enumerate(name.split()):
            out.append(f'<text x="{x+24}" y="{62+wi*12}" text-anchor="middle" font-size="9.5" '
                       f'fill="{colour}">{word}</text>')
    out.append('<path d="M36 104 V116 H520" stroke="currentColor" opacity=".3" fill="none"/>')
    out.append('<text x="12" y="140" font-size="11.5" fill="currentColor" opacity=".8">'
               'Skeleton first with no model in it. Exact code early — it stands alone.</text>')
    out.append('<text x="12" y="158" font-size="11.5" fill="currentColor" opacity=".8">'
               'The plug lands before the gated write that needs it. The proof goes last.</text>')
    out.append('<text x="12" y="176" font-size="11" fill="var(--dg-rose)" opacity=".85">'
               'A bolt that cannot be built alone was cut wrong — say so before you start it.</text>')
    return _svg("".join(out), "Ten daily bolts in dependency order across two weeks",
                "The cut is by dependency, not by priority. One unknown per day.")


def shadow_widen() -> str:
    stages = [("shadow", "decides, never acts", 120, "var(--soft)"),
              ("5%", "12 cases a day", 90, "var(--dg-amber)"),
              ("25%", "60 a day", 110, "var(--dg-indigo)"),
              ("100%", "widened on evidence", 150, "var(--dg-green)")]
    out, x = [], 12
    for name, sub, w, colour in stages:
        out.append(f'<rect x="{x}" y="42" width="{w}" height="46" rx="6" fill="{colour}" fill-opacity=".15" '
                   f'stroke="{colour}"/>')
        out.append(f'<text x="{x+w/2:.0f}" y="64" text-anchor="middle" font-size="14" font-weight="700" '
                   f'fill="{colour}">{name}</text>')
        out.append(f'<text x="{x+w/2:.0f}" y="79" text-anchor="middle" font-size="10" fill="currentColor" '
                   f'opacity=".62">{sub}</text>')
        if w != 150:
            out.append(f'<path d="M{x+w+3} 65 h14" stroke="currentColor" opacity=".4" stroke-width="1.6"/>')
            out.append(f'<path d="M{x+w+12} 61 l5 4 -5 4" fill="none" stroke="currentColor" opacity=".4" '
                       f'stroke-width="1.6"/>')
        x += w + 20
    out.append('<text x="12" y="112" font-size="11" fill="currentColor" opacity=".6">'
               'each arrow is a condition, never a date</text>')
    out.append('<text x="12" y="140" font-size="11.5" fill="currentColor" opacity=".8">'
               '500 cases at 5% of 240 a day takes 42 days. That is arithmetic, not effort.</text>')
    out.append('<text x="12" y="162" font-size="11.5" fill="var(--dg-rose)" opacity=".9">'
               'Money actions stay gated at every stage, whatever the shadow shows.</text>')
    return _svg("".join(out), "Shadow, then five percent, then twenty-five, then full traffic",
                "The safe share is the slow one. That is why a cut-over widens.")


def bill_factors() -> str:
    facs = [("context", "1.6", "2,100→3,360 tokens"), ("tier", "1.5", "50%→100% frontier"),
            ("cache", "1.3", "71%→9% hit, f=0.40"), ("attempts", "1.42", "1.2→1.7 per case")]
    out, x = [], 12
    for name, v, sub in facs:
        out.append(f'<rect x="{x}" y="40" width="112" height="56" rx="6" fill="var(--dg-amber)" fill-opacity=".16" '
                   f'stroke="var(--dg-amber)"/>')
        out.append(f'<text x="{x+56}" y="34" text-anchor="middle" font-size="10.5" fill="currentColor" '
                   f'opacity=".6">{name}</text>')
        out.append(f'<text x="{x+56}" y="70" text-anchor="middle" font-size="19" font-weight="700" '
                   f'fill="var(--dg-amber)">{v}</text>')
        out.append(f'<text x="{x+56}" y="87" text-anchor="middle" font-size="9" fill="currentColor" '
                   f'opacity=".55">{sub}</text>')
        if x < 360:
            out.append(f'<text x="{x+122}" y="72" text-anchor="middle" font-size="13" fill="currentColor" '
                       f'opacity=".45">×</text>')
        x += 134
    out.append('<text x="276" y="128" text-anchor="middle" font-size="18" font-weight="700" '
               'fill="var(--dg-rose)">= 4.4× the estimate, on flat traffic</text>')
    out.append('<text x="276" y="152" text-anchor="middle" font-size="11.5" fill="currentColor" opacity=".78">'
               'Four ordinary habits, each a sensible decision by a careful person.</text>')
    out.append('<text x="276" y="172" text-anchor="middle" font-size="11.5" fill="currentColor" opacity=".78">'
               'Fix in order of (factor − 1) ÷ days: context, tier, cache, then the breaker.</text>')
    return _svg("".join(out), "Four cost factors multiplying to four point four times",
                "They multiply. The largest ratio change is not the largest factor.")


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
        y = 12 + i * 34
        out.append(f'<rect x="12" y="{y}" width="{150+i*22}" height="27" rx="5" fill="{colour}" '
                   f'fill-opacity=".15" stroke="{colour}"/>')
        out.append(f'<text x="24" y="{y+18}" font-size="12" font-weight="700" fill="{colour}">{band}</text>')
        out.append(f'<text x="50" y="{y+18}" font-size="11" font-family="ui-monospace,monospace" '
                   f'fill="currentColor" opacity=".8">{tool}</text>')
        out.append(f'<text x="290" y="{y+18}" font-size="11" fill="currentColor" opacity=".55">{kind}</text>')
        out.append(f'<text x="400" y="{y+18}" font-size="11.5" font-weight="600" fill="{colour}">{check}</text>')
    return _svg("".join(out),
                "Five risk bands from a read tool to an identity change, each with its check",
                "The band belongs to the tool. A change inherits the band of whatever it touches.")


def two_numbers() -> str:
    out = ['<rect x="12" y="14" width="536" height="120" rx="8" fill="var(--paper)" stroke="var(--rule)"/>']
    rows = [("person-days per story", "8.0", "4.6", "−43%", "var(--dg-green)"),
            ("token spend per story", "—", "$310", "", "var(--dg-amber)"),
            ("review hours added", "1.2", "2.0", "+0.8", "var(--dg-amber)"),
            ("re-runs per story", "—", "1.4", "", "var(--soft)")]
    out.append('<text x="300" y="32" font-size="10" fill="currentColor" opacity=".5">baseline</text>')
    out.append('<text x="388" y="32" font-size="10" fill="currentColor" opacity=".5">now</text>')
    out.append('<text x="490" y="32" font-size="10" fill="currentColor" opacity=".5">change</text>')
    for i, (name, a, b, c, colour) in enumerate(rows):
        y = 52 + i * 21
        out.append(f'<text x="28" y="{y}" font-size="11.5" fill="currentColor" opacity=".85">{name}</text>')
        out.append(f'<text x="330" y="{y}" text-anchor="end" font-size="11.5" fill="currentColor" '
                   f'opacity=".7">{a}</text>')
        out.append(f'<text x="416" y="{y}" text-anchor="end" font-size="11.5" font-weight="600" '
                   f'fill="currentColor">{b}</text>')
        out.append(f'<text x="524" y="{y}" text-anchor="end" font-size="11.5" font-weight="700" '
                   f'fill="{colour}">{c}</text>')
    out.append('<text x="12" y="156" font-size="11.5" fill="currentColor" opacity=".8">'
               'The review row and the re-run row are what keep the first number honest.</text>')
    out.append('<text x="12" y="176" font-size="11.5" fill="var(--dg-rose)" opacity=".9">'
               'The programme is cancelled on the number you hid, never the one you showed.</text>')
    return _svg("".join(out), "A cycle report with four rows: person-days, tokens, review hours, re-runs",
                "Two numbers, and the two rows that stop either being gamed.")


FIGURES = {
    "bar_sheet": bar_sheet, "chain": chain, "cache_prefix": cache_prefix, "bolt_days": bolt_days,
    "shadow_widen": shadow_widen, "bill_factors": bill_factors,
    "authority_ladder": authority_ladder, "two_numbers": two_numbers,
}
