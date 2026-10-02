"""Sketches for the lesson on team structure."""

from pages.sketch import Sk


def chart(s: Sk, x: float, y: float):
    """An org chart on a board on an easel, the board's top left at ``x, y``."""
    s.line(x + 60, y + 250, x + 30, 540)
    s.line(x + 260, y + 250, x + 290, 540)
    s.rect(x, y, 320, 250, fill="p")
    s.rect(x + 120, y + 30, 80, 46)
    s.stroke([(x + 160, y + 76), (x + 160, y + 112)], "ink", "t")
    s.stroke([(x + 56, y + 150), (x + 56, y + 112), (x + 264, y + 112), (x + 264, y + 150)], "ink", "t")
    s.stroke([(x + 160, y + 112), (x + 160, y + 150)], "ink", "t")
    for i in range(3):
        s.rect(x + 20 + i * 104, y + 150, 72, 46)


def conway(s: Sk):
    # the org chart on an easel, and the agents set out on the floor to match it, one under each box
    s.ground(540, 50, 1150, tufts=2)
    chart(s, 60, 120)
    s.worker(530, 339, look=(-1, -0.2), arms=[(384, 300), (704, 446)])
    for i in range(3):
        s.bot(770 + i * 160, 472, 1.15, look=(1 if i < 2 else -1, 0))
    for x in (850, 1010):                                    # where one hands to the next
        s.stroke([(x - 16, 450), (x + 8, 464), (x - 10, 480), (x + 14, 494)], "point", "h", amp=0.5)
    s.label(220, 86, "the org chart", "ink")
    s.label(930, 110, "one agent|per department", "aside")
    s.label(900, 310, "breaks at the hand-offs", "point")
    s.arrow(860, 330, 852, 430, "point", w="t", head=15)
    s.arrow(990, 330, 1008, 430, "point", w="t", head=15)


SKETCHES = [
    {"name": "the-org-chart-set-out-on-the-floor",
     "idea": "agent boundaries copy team boundaries unless someone decides them",
     "verb": "copy from", "prop": "org chart on an easel",
     "alt": "An org chart stands on an easel. A worker looks at it with one hand on the chart and the other placing the "
            "first of three small machines, which stand in a row to match the chart's three boxes. Red marks sit "
            "between the machines.",
     "caption": "One agent per department is often an org chart, not a design. Decide the seams on purpose, and give each hand-off a named limit.",
     "draw": conway},
]
