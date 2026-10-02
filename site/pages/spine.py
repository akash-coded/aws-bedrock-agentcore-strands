"""The home page's methods band: how AI-DLC, BMAD and the rest fit together.

:func:`methods_band` builds the band, its heading, its line, its picture and its links. Until the method
map replaces it (verdict-home 1.2, parcel H3), the picture is the lifecycle figure below.

:func:`figure` draws the SkyWays PDLC as what it is. On the left, four methods each give it one idea:
four lines run into one point. Out of that point comes one thick line in the four phase hues that closes
into a loop, a station at the start of each phase, the sign-off before the third. Above the line each
phase asks its question; below it is the thing a team hears when that question was skipped. That pair
is the reason the lifecycle exists, so it is the first thing a visitor is shown.

It is HTML first. The phases and method names are links, and the drawing itself is hidden from a
screen reader. The table of methods that followed it is now the chooser's (pages/chooser.py).
"""
from __future__ import annotations

from html import escape as _E

# Wide layout, in px from the top of the figure. base.css mirrors these.
TRUNK_Y = 150                # centre of the line
ROW, GAP = 44, 10            # one method's row in the funnel, and the space between two
FUN_H = 4 * ROW + 3 * GAP    # the funnel is as tall as its four rows
FUN_TOP = TRUNK_Y - FUN_H // 2

# The aircraft a phase flies, the same four the hero's flight changes through (pages/globe.py).
CRAFT_LABEL = ["a paper plane", "a drawing of an airliner", "the airliner, built", "a jet"]
# What the lifecycle keeps from each method: the one idea, in a few plain words (the funnel on the home page).
BORROWED = [
    ("AI-DLC", "learn/what-is-ai-dlc/", "short build cycles"),
    ("BMAD Method", "learn/what-is-the-bmad-method/", "one document per decision"),
    ("Spec-driven development", "learn/what-is-spec-driven-development/", "the spec is the source"),
    ("AIDD", "learn/what-is-aidd/", "the daily coding craft"),
]


def methods_band() -> str:
    """The home page's second band (verdict-home 1.2): its heading, its line, the lifecycle figure until the
    map replaces it, and its two links. The phases and the line each skipped question leaves are render's."""
    import render
    return f"""<section class="band" id="methods" aria-labelledby="h-methods"><div class="wrap">
  <header class="sec-h split"><p class="eyebrow">The methods</p>
    <h2 id="h-methods">How AI-DLC, BMAD and the rest fit together.</h2>
    <p>Each one is a way to build with AI. They all meet in the build, and they leave the same four questions to you.</p></header>
  <div>{figure(render.PHASES, render.SKIPPED, "learn/what-is-the-agentic-pdlc/", BORROWED)}</div>
  <p class="links"><a class="more" href="learn/one-lifecycle-for-every-method/">Where each method sits, stage by stage <i aria-hidden="true">→</i></a>
    <a class="more" href="learn/ai-dlc-vs-aidd-vs-agentic-sdlc/">AIDLC, AIDDLC and other names, sorted <i aria-hidden="true">→</i></a></p>
</div></section>"""


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
    return (f'<svg class="sp-craft" viewBox="-20 -15 40 30" aria-hidden="true" focusable="false">'
            f'<path d="{globe.SHAPES[shape]}" class="k-{look}"/></svg>')


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
            '<em class="sp-back"><svg viewBox="0 0 12 10" focusable="false"><path d="M11 5H2M5.5 1.5 2 5l3.5 3.5"/></svg><span class="t">back to Frame<span class="x">, with what you learned</span></span></em>'
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
            f'<p class="sp-head" aria-hidden="true">Four methods you may know</p>'
            f'<ol class="sp-in">{took}</ol>{_funnel()}<p class="sp-into" aria-hidden="true">one idea from each</p>'
            f'{core}<p class="sp-cap" aria-hidden="true">When it is skipped</p>'
            f'<ol class="sp-ph">{ph}</ol>'
            '<figcaption class="sp-note">SkyWays PDLC takes one idea from each method and joins them in one loop. '
            'You still pick the method your team works in.</figcaption></figure>')
