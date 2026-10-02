"""The home page's two pictures of the method: the lifecycle, and the methods on it.

:func:`figure` draws the SkyWays PDLC as what it is. On the left, four methods each give it one idea:
four lines run into one point. Out of that point comes one thick line in the four phase hues that closes
into a loop, a station at the start of each phase, the sign-off before the third. Above the line each
phase asks its question; below it is the thing a team hears when that question was skipped. That pair
is the reason the lifecycle exists, so it is the first thing a visitor is shown.

:func:`coverage` is the table that follows it: each building method as a row of bars under the same
four phases, and a last row for what the spine adds that no method carries. The lifecycle and a method
are different kinds of thing, so the last row is words, not a fifth bar.

Both are HTML first. The phases and method names are links, every bar has a text reading, and the
drawing itself is hidden from a screen reader.
"""
from __future__ import annotations

from html import escape as _E

# Wide layout, in px from the top of the figure. base.css mirrors these.
TRUNK_Y = 150                # centre of the line
ROW, GAP = 44, 10            # one method's row in the funnel, and the space between two
FUN_H = 4 * ROW + 3 * GAP    # the funnel is as tall as its four rows
FUN_TOP = TRUNK_Y - FUN_H // 2

# The aircraft a phase flies, the same four the hero's flight changes through (pages/globe.py).
CRAFT_LABEL = ["a paper plane", "a plan", "an airliner", "a jet"]


def _funnel() -> str:
    """Four lines, one from each method, running into one point. Stretched with the page, so the
    stroke is told not to scale."""
    mid = FUN_H / 2
    paths = "".join(
        f'<path d="M0 {ROW / 2 + i * (ROW + GAP):g} C58 {ROW / 2 + i * (ROW + GAP):g} 42 {mid:g} 100 {mid:g}" '
        f'pathLength="1" style="--m:{i}"/>' for i in range(4))
    return (f'<svg class="sp-fun" viewBox="0 0 100 {FUN_H}" preserveAspectRatio="none" aria-hidden="true" '
            f'focusable="false">{paths}</svg>')


def _craft(i: int) -> str:
    from pages import globe
    shape, look = globe.CRAFT[i]
    flame = f'<path d="{globe.FLAME}" class="sc-flame"/>' if look == "flown" else ""
    return (f'<svg class="sp-craft" viewBox="-26 -15 46 30" aria-hidden="true" focusable="false">{flame}'
            f'<path d="{globe.SHAPES[shape]}" class="sc-still k-{look}"/></svg>')


def figure(phases: list[tuple], skipped: list[str], core_href: str, methods: list[tuple]) -> str:
    """``phases`` is render.PHASES. ``skipped`` holds one line per phase: what a team hears when the
    phase's question went unasked, each taken from that phase's own lesson. ``methods`` is the four
    methods the lifecycle borrows from: (name, href, the idea it keeps)."""
    took = "".join(
        f'<li style="--m:{i}"><a href="{href}"><b>{_E(name)}</b><small>{_E(idea)}</small></a></li>'
        for i, (name, href, idea) in enumerate(methods))
    segs = "".join(f'<i style="--c:var(--dg-{hue});--j:{j}" data-k="{key}"></i>'
                   for j, (key, _n, _q, hue, _h) in enumerate(phases))
    core = (f'<div class="sp-core"><a href="{core_href}"><b>SkyWays PDLC</b><small>four phases, one loop</small></a>'
            f'<span class="sp-trunk" aria-hidden="true">{segs}'
            '<svg class="sp-loop" focusable="false"><rect width="100%" height="100%" rx="20"/></svg>'
            '<em class="sp-back"><svg viewBox="0 0 12 10" focusable="false"><path d="M11 5H2M5.5 1.5 2 5l3.5 3.5"/></svg>back to Frame<span>, with what you learned</span></em>'
            '<em class="sp-gate">sign-off</em></span>'
            f'<span class="vh"> Four phases in order. Between {phases[1][1]} and {phases[2][1]} there is a sign-off: '
            f'nothing is built until it is signed. After {phases[3][1]} the work goes back to {phases[0][1]}.</span></div>')
    ph = "".join(
        f'<li style="--c:var(--dg-{hue});--i:{i}"><a href="{href}"><span class="c-key">{key}{_craft(i)}</span>'
        f'<span class="c-name">{name}</span><span class="c-ask">{q}</span></a>'
        f'<p class="sp-skip"><span class="vh">Skip it, and you hear: </span>{_E(skipped[i])}</p></li>'
        for i, (key, name, q, hue, href) in enumerate(phases))
    return ('<figure class="spine" aria-label="How the SkyWays PDLC is made: one idea from each of four methods, '
            'joined into four phases that loop, with the question each phase asks and what a team hears when the question is skipped">'
            f'<p class="vh">The SkyWays PDLC keeps one idea from each of four methods.</p>'
            f'<ol class="sp-in">{took}</ol>{_funnel()}<p class="sp-into" aria-hidden="true">one idea from each</p>'
            f'{core}<p class="sp-cap" aria-hidden="true">Skip one, and you hear</p>'
            f'<ol class="sp-ph">{ph}</ol>'
            '<figcaption class="sp-note">SkyWays PDLC takes one idea from each method and joins them in one loop. '
            'You still pick the method your team works in.</figcaption></figure>')


READ = {2: "covers this phase", 1: "touches this phase lightly", 0: "says nothing here",
        "x": "extended in this manual: learn and adjust, into the next plan"}
# The table's own last row, in plain words: four decisions no method makes for you.


def coverage(phases: list[tuple], methods: list[tuple], adds: list[str], core_href: str) -> str:
    """Four methods as bars along the four phases, then what the spine adds. A real table, so a screen
    reader gets rows and columns; the bars are its cells."""
    head = "".join(
        f'<th scope="col" style="--c:var(--dg-{hue})"{" class=gated" if key == "P2" else ""}>'
        f'<a href="{href}"><span class="c-key">{key}</span><span class="c-name">{name}</span></a></th>'
        for key, name, _q, hue, href in phases)
    rows = []
    for name, href, line, reach in methods:
        cells = "".join(
            f'<td style="--c:var(--dg-{phases[i][3]})"{" class=gated" if i == 2 else ""}>'
            f'<i class="bar r{r}"></i><span class="vh">{READ[r]}</span></td>'
            for i, r in enumerate(reach))
        rows.append(f'<tr style="--r:{len(rows)}"><th scope="row"><a href="{href}">{_E(name)}</a>'
                    f'<small>{_E(line)}</small></th>{cells}</tr>')
    added = "".join(f'<td style="--c:var(--dg-{phases[i][3]})"{" class=gated" if i == 2 else ""}>{_E(a)}</td>'
                    for i, a in enumerate(adds))
    rows.append(f'<tr class="adds"><th scope="row"><a href="{core_href}">What this manual adds</a>'
                f'<small>Four decisions no method makes for you</small></th>{added}</tr>')
    # the same four lines as a list, for a screen too narrow to hold them in columns
    listed = "".join(f'<li style="--c:var(--dg-{phases[i][3]})"><b>{phases[i][0]} {phases[i][1]}</b>{_E(a)}</li>'
                     for i, a in enumerate(adds))
    narrow = (f'<div class="cover-adds"><p><a href="{core_href}">What this manual adds</a>'
              f'<small>Four decisions no method makes for you</small></p><ol>{listed}</ol></div>')
    return ('<div class="cover"><table><caption class="vh">Which phases each agentic method covers, and what the '
            'SkyWays PDLC adds in each</caption>'
            f'<thead><tr><th scope="col" class="corner"><span class="vh">Method</span></th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>{narrow}'
            '<p class="cover-key"><span><i class="bar r2"></i>covers the phase</span>'
            '<span><i class="bar r1"></i>touches it lightly</span>'
            '<span><i class="bar rx"></i>extended in this manual</span>'
            '<span><i class="gatekey"></i>sign-off: nothing is built until it is signed. The lessons call it the hard gate.</span></p>')
