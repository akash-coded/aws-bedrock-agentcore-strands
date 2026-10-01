"""Section two of the home page: the line, and the methods that run along it.

One figure answers "which agentic method should you follow?". The SkyWays PDLC is drawn as what it is:
a thick line in the four phase hues that closes into a loop, with a station at the start of each phase,
the hard gate on it, and the four phase questions inside the loop. Each building method is a thin
neutral strand that leaves its name and runs alongside the line: solid where the method has a stage,
dashed where it touches the phase lightly, a hairline where it says nothing.

The two kinds of thing get two kinds of mark on purpose. The line is the lifecycle, about a product
with a model inside it; a strand is a way of building. A method that has a stage in every phase is
still a strand, so it never reads as a second copy of the line.

One piece of markup, two layouts (``theme/base.css``, ``.weave``). On a wide screen the names fan
into a bundle; at 1000px and under each name sits beside its own strand, the line first, and the
phase questions follow as a list. Everything a reader needs is HTML: the names and the phases are
links, each strand has a text reading, and the drawing itself is hidden from a screen reader.
"""
from __future__ import annotations

from html import escape as _E

# Wide layout, in px from the top of the figure. base.css mirrors these.
H = 292                      # the figure's height
CORE_Y = 36                  # centre of the line's own name
ROW_Y = (100, 148, 196, 244)  # centres of the four method names
TRUNK_Y = 150                # centre of the line
LANE_Y = (178, 193, 208, 223)  # centres of the four strands, under the line

READ = {2: "has a stage in", 1: "touches lightly", 0: "no stage in"}


def _join(names: list[str]) -> str:
    if len(names) < 2:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def reading(reach: tuple[int, ...], phases: list[tuple]) -> str:
    """A strand in words, for a reader who cannot see it."""
    names = [p[1] for p in phases]
    full = [n for n, r in zip(names, reach) if r == 2]
    light = [n for n, r in zip(names, reach) if r == 1]
    if len(full) == len(names):
        return "Has a stage in every phase."
    out = []
    if full:
        out.append(f"Has a stage in {_join(full)}{' only' if not light and len(full) == 1 else ''}.")
    if light:
        out.append(f"Touches {_join(light)} lightly.")
    return " ".join(out)


def _fan() -> str:
    """The curves from each name into its place in the bundle. Stretched sideways with the page, so the
    strokes are told not to scale."""
    def curve(y0: int, y1: int, cls: str) -> str:
        return f'<path class="{cls}" d="M0 {y0} C55 {y0} 45 {y1} 100 {y1}"/>'
    paths = curve(CORE_Y, TRUNK_Y, "f-core") + "".join(
        curve(y0, y1, f"f-m f{i}") for i, (y0, y1) in enumerate(zip(ROW_Y, LANE_Y)))
    return (f'<svg class="wv-fan" viewBox="0 0 100 {H}" preserveAspectRatio="none" aria-hidden="true" '
            f'focusable="false">{paths}</svg>')


def figure(phases: list[tuple], coverage: list[tuple], core_href: str) -> str:
    """``phases`` and ``coverage`` are render.PHASES and render.COVERAGE: the same data the frameworks
    page reads, so the two cannot disagree."""
    segs = "".join(f'<i style="--c:var(--dg-{hue});--j:{j}" data-k="{key}"></i>'
                   for j, (key, _n, _q, hue, _h) in enumerate(phases))
    core = (f'<li class="wv-core"><a href="{core_href}"><b>SkyWays PDLC</b><small>An agentic PDLC: the spine itself</small></a>'
            f'<span class="wv-lane wv-trunk" aria-hidden="true">{segs}'
            '<svg class="wv-loop" focusable="false"><rect width="100%" height="100%" rx="20"/></svg>'
            '<em class="wv-back"><svg viewBox="0 0 12 10" focusable="false"><path d="M11 5H2M5.5 1.5 2 5l3.5 3.5"/></svg>the way back</em>'
            '<em class="wv-gate">hard gate</em></span>'
            f'<span class="vh"> All four phases, with the hard gate between {phases[1][1]} and {phases[2][1]}, '
            f'and a way back from {phases[3][1]} to {phases[0][1]}.</span></li>')
    rows = []
    for i, (name, href, line, reach) in enumerate(coverage):
        lane = "".join(f'<i class="r{r}" style="--c:var(--dg-{phases[j][3]})"></i>' for j, r in enumerate(reach))
        rows.append(f'<li class="wv-m" style="--i:{i}"><a href="{href}"><b>{_E(name)}</b><small>{_E(line)}</small></a>'
                    f'<span class="wv-lane" aria-hidden="true">{lane}</span>'
                    f'<span class="vh"> {reading(reach, phases)}</span></li>')
    ph = "".join(
        f'<li style="--c:var(--dg-{hue});--i:{i}"><a href="{href}"><span class="c-key">{key}</span>'
        f'<span class="c-name">{name}</span><span class="c-ask">{q}</span></a></li>'
        for i, (key, name, q, hue, href) in enumerate(phases))
    return ('<figure class="weave" aria-label="The SkyWays PDLC as one spine, and four building methods along it">'
            f'<ol class="wv-names" aria-label="The spine and the four methods, and where each method has a stage">'
            f'{core}{"".join(rows)}</ol>{_fan()}'
            f'<ol class="wv-ph" aria-label="The four phases, and the question each one asks">{ph}</ol></figure>'
            '<p class="wv-key"><span><i class="k2"></i>a method has a stage here</span>'
            '<span><i class="k1"></i>it touches the phase lightly</span>'
            '<span><i class="kg"></i>the hard gate: nothing is built until the spec is signed</span></p>')
