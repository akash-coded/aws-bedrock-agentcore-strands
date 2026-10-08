"""Sketches for the lesson on the BMAD Method."""
from pages.sketch import Sk


def hatch(s: Sk):
    # a pile of six binders in the worker's arms, and a hatch in the wall the size of a postcard
    s.ground(540, 50, 1150, tufts=2)
    s.rect(880, 170, 290, 370, fill="p")                        # the wall
    s.hatchway(965, 330, 120, 84)
    s.worker(400, 339, look=(1, 0.1), arms=[(650, 436), (612, 436)], lean=5)
    for i in range(6):
        s.binder(610 + (i % 2) * 8, 392 - i * 42, 200, 40)
    s.burst(850, 300, r=14, n=3, a0=-40, a1=40)
    s.label(1025, 288, "a typo fix", "ink")
    s.note(715, 124, "six documents", (715, 176), "point")
    s.note(250, 88, "\"we are a|BMAD shop\"", (385, 214), "aside")


SKETCHES = [
    {"name": "six-binders-one-small-hatch",
     "idea": "the document trail is right for audited work and dead weight on a one-line fix",
     "verb": "squeeze through", "prop": "six binders at a small hatch",
     "alt": "A worker carries a pile of six binders up to a wall. The only way through is a hatch the size of a postcard.",
     "caption": "Six documents suit a product three teams build. For a typo fix, BMAD's own advice is to skip it.",
     "draw": hatch},
]
