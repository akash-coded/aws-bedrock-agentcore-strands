"""The home page's two pictures of the method: the spine, and the methods on it.

:func:`figure` draws the SkyWays PDLC as what it is: one thick line in the four phase hues that closes
into a loop, a station at the start of each phase, the hard gate before the third. Above the line each
phase asks its question; below it is the thing a team hears when that question was skipped. That pair
is the reason the spine exists, so it is the first thing a visitor is shown.

:func:`coverage` is the table that follows it: each building method as a row of bars under the same
four phases, and a last row for what the spine adds that no method carries. The lifecycle and a method
are different kinds of thing, so the last row is words, not a fifth bar.

Both are HTML first. The phases and method names are links, every bar has a text reading, and the
drawing itself is hidden from a screen reader.
"""
from __future__ import annotations

from html import escape as _E

# Wide layout, in px from the top of the figure. base.css mirrors these.
CORE_Y = 36                  # centre of the spine's own name
TRUNK_Y = 150                # centre of the line
H = 190                      # how far down the curve from the name to the line has to reach


def _fan() -> str:
    """The curve from the spine's name into the line. Stretched sideways with the page, so the stroke
    is told not to scale."""
    return (f'<svg class="sp-fan" viewBox="0 0 100 {H}" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            f'<path d="M0 {CORE_Y} C55 {CORE_Y} 45 {TRUNK_Y} 100 {TRUNK_Y}"/></svg>')


def figure(phases: list[tuple], skipped: list[str], core_href: str) -> str:
    """``phases`` is render.PHASES. ``skipped`` holds one line per phase: what a team hears when the
    phase's question went unasked, each taken from that phase's own lesson."""
    segs = "".join(f'<i style="--c:var(--dg-{hue});--j:{j}" data-k="{key}"></i>'
                   for j, (key, _n, _q, hue, _h) in enumerate(phases))
    core = (f'<div class="sp-core"><a href="{core_href}"><b>SkyWays PDLC</b><small>An agentic PDLC: the spine itself</small></a>'
            f'<span class="sp-trunk" aria-hidden="true">{segs}'
            '<svg class="sp-loop" focusable="false"><rect width="100%" height="100%" rx="20"/></svg>'
            '<em class="sp-back"><svg viewBox="0 0 12 10" focusable="false"><path d="M11 5H2M5.5 1.5 2 5l3.5 3.5"/></svg>the way back</em>'
            '<em class="sp-gate">hard gate</em></span>'
            f'<span class="vh"> Four phases in order, with a hard gate between {phases[1][1]} and {phases[2][1]}, '
            f'and a way back from {phases[3][1]} to {phases[0][1]}.</span></div>')
    ph = "".join(
        f'<li style="--c:var(--dg-{hue});--i:{i}"><a href="{href}"><span class="c-key">{key}</span>'
        f'<span class="c-name">{name}</span><span class="c-ask">{q}</span></a>'
        f'<p class="sp-skip"><span class="vh">Skip it, and you hear: </span>{_E(skipped[i])}</p></li>'
        for i, (key, name, q, hue, href) in enumerate(phases))
    return ('<figure class="spine" aria-label="The SkyWays PDLC: four phases, the question each one asks, '
            'and what a team hears when the question is skipped">'
            f'{core}{_fan()}<p class="sp-cap" aria-hidden="true">Skip one, and you hear</p>'
            f'<ol class="sp-ph">{ph}</ol></figure>')


READ = {2: "covers this phase", 1: "touches this phase lightly", 0: "says nothing here",
        "x": "extended in this manual: learn and adjust, into the next plan"}


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
    rows.append(f'<tr class="adds"><th scope="row"><a href="{core_href}">SkyWays PDLC</a>'
                f'<small>What the spine adds, and none of the four carries</small></th>{added}</tr>')
    # the same four lines as a list, for a screen too narrow to hold them in columns
    listed = "".join(f'<li style="--c:var(--dg-{phases[i][3]})"><b>{phases[i][0]} {phases[i][1]}</b>{_E(a)}</li>'
                     for i, a in enumerate(adds))
    narrow = (f'<div class="cover-adds"><p><a href="{core_href}">SkyWays PDLC</a>'
              f'<small>What the spine adds, and none of the four carries</small></p><ol>{listed}</ol></div>')
    return ('<div class="cover"><table><caption class="vh">Which phases each agentic method covers, and what the '
            'SkyWays PDLC adds in each</caption>'
            f'<thead><tr><th scope="col" class="corner"><span class="vh">Method</span></th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>{narrow}'
            '<p class="cover-key"><span><i class="bar r2"></i>covers the phase</span>'
            '<span><i class="bar r1"></i>touches it lightly</span>'
            '<span><i class="bar rx"></i>extended in this manual</span>'
            '<span><i class="gatekey"></i>the one hard gate: nothing is built until the spec is signed</span></p>')
