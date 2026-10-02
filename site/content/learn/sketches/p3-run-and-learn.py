"""Sketches for the P3 Run & Learn lesson."""
from pages.sketch import Sk


def hull(s: Sk, x: float, y: float, w: float = 250, pen: str = "ink", wt: str = "h"):
    """A rowing boat seen from the side, its waterline centred at ``x, y``."""
    s.stroke([(x - w / 2, y - 46), (x - w * 0.36, y + 8), (x + w * 0.36, y + 8), (x + w / 2, y - 46)], pen, wt)
    s.stroke([(x - w / 2, y - 46), (x + w / 2, y - 46)], pen, "t" if pen == "faint" else "")


def drift(s: Sk):
    # a boat that has slid a little each week away from a stake on the bank; the worker in it pulls a
    # measuring line tight with both hands, back to the stake
    s.cliff(40, 400, 190, side="left", depth=150)
    s.hatch(60, 404, 150, 40, gap=22)
    s.rect(150, 262, 20, 138, "ink", fill="ink")                               # the stake: where it started
    for x in (340, 500, 660):                                                     # where it was, week by week
        hull(s, x, 470, 150, "faint", "t")
    s.worker(910, 296, 1.6, look=(-1, 0.1), arms=[(800, 326), (768, 322)], lean=9)
    hull(s, 910, 474, 270)
    s.curve([(170, 280), (470, 312), (768, 322)], "point", "h")                # the line back to the stake
    for x0 in (260, 1080):                                                     # the water
        s.curve([(x0, 500), (x0 + 24, 492), (x0 + 48, 500), (x0 + 72, 492)], "faint", "t")
    s.note(300, 150, "the fixed mark", (184, 256), "ink")
    s.label(520, 276, "thirteen points", "point", rot=3)
    s.arrow(330, 562, 700, 562, "path", dash=True, w="h")
    s.label(520, 540, "1.9 points a week", "path", rot=0)


SKETCHES = [
    {"name": "measure-back-to-the-stake",
     "idea": "drift moves too little each week to trip a weekly alarm, so also measure against a fixed mark",
     "verb": "pull a line tight", "prop": "rowing boat and a stake on the bank",
     "alt": "A rowing boat has slid away from a stake on the bank, a little at a time; fainter outlines show where it "
            "was. A worker in the boat leans back and pulls a measuring line tight with both hands, back to the stake.",
     "caption": "The mix slid thirteen points by week eight and never tripped the weekly alert. Measure against a fixed "
                "mark as well as against last week.",
     "draw": drift},
]
