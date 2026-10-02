"""The home page's chooser band: which agentic methods should your team use?

:func:`band` builds the band, its heading, its line, its body and its links. The chooser itself, one pair
every team needs and three yes-or-no questions that each add one method (verdict-home 1.3), is parcel H4's.
Until it lands the body is the table it replaces, below: each building method as a row of bars under the
four phases, and a last row for what the lifecycle adds that no method carries. The lifecycle and a method
are different kinds of thing, so the last row is words, not a fifth bar. Every bar has a text reading.
"""
from __future__ import annotations

from html import escape as _E

# How far each method reaches along the spine: 2 covers the phase, 1 touches it lightly, 0 says nothing,
# "x" is a stage this manual adds to the method (extended BMAD). The same reading as the frameworks
# page's plug board, which carries the detail.
COVERAGE = [
    ("AI-DLC", "learn/what-is-ai-dlc/", "From AWS, built in bolts of days", (2, 2, 2, 2)),
    ("BMAD Method", "learn/what-is-the-bmad-method/", "AI personas, working as an agile team", (2, 2, 2, "x")),
    ("Spec-driven development", "learn/what-is-spec-driven-development/", "The spec is what you maintain", (1, 2, 2, 1)),
    ("AIDD", "learn/what-is-aidd/", "The daily craft with a coding agent", (0, 0, 2, 0)),
]
# What this manual adds in each phase, in words a newcomer can read (the table's last row on the home page;
# the frameworks page keeps the terms of art, illos.ADDS).
HOME_ADDS = [
    "How much the agent may do alone, decided before anything is built",
    "A pass mark for each kind of case and a limit on each action, agreed at sign-off",
    "Proof that it meets the pass mark before real users see it",
    "One report of what it saved and what it cost, which opens the next round",
]


def band() -> str:
    """The home page's third band (verdict-home 1.3). The phases are render's."""
    import render
    return f"""<section class="band" id="choose" aria-labelledby="h-choose"><div class="wrap">
  <header class="sec-h split"><p class="eyebrow">Your team</p>
    <h2 id="h-choose">Which agentic methods should your team use?</h2>
    <p>Every team needs the first pair. Add each of the others when your work matches its question.</p></header>
  <div>{coverage(render.PHASES, COVERAGE, HOME_ADDS, "learn/what-is-the-agentic-pdlc/")}</div>
  <p class="links"><a class="more" href="learn/how-much-process-does-a-change-need/">How much process a change needs <i aria-hidden="true">→</i></a>
    <a class="more" href="method/">The four phases on one page <i aria-hidden="true">→</i></a></p>
</div></section>"""


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
