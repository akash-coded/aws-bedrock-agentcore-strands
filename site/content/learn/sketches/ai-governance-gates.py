"""Sketches for the lesson on the five governance gates."""
from pages.sketch import Sk


def utube(s: Sk):
    # a U-shaped tube of liquid: the worker pushes one side down and the other side comes up
    s.ground(540, 50, 1150, tufts=2)
    s.poly([(564, 410), (620, 410), (620, 448), (642, 470), (758, 470), (780, 448), (780, 236), (836, 236),
            (836, 468), (794, 518), (606, 518), (564, 468)], "aside", fill="aside")
    s.stroke([(560, 170), (560, 470), (604, 522), (796, 522), (840, 470), (840, 170)], "ink", "h")
    s.stroke([(624, 170), (624, 446), (644, 466), (756, 466), (776, 446), (776, 170)], "ink", "h")
    s.line(640, 522, 640, 540)
    s.line(760, 522, 760, 540)
    s.rect(566, 396, 52, 14, fill="ink")                     # the plunger
    s.line(592, 396, 592, 236, w="h")
    s.line(556, 236, 628, 236, w="h")
    s.worker(340, 339, look=(1, 0.2), arms=[None, (558, 238)], lean=7)
    s.arrow(900, 330, 900, 240, "point", w="h")
    s.note(430, 110, "one number, pushed", (586, 222), "ink")
    s.note(1010, 150, "its side effect", (852, 228), "point")
    s.label(1010, 420, "report|the pair", "aside")


SKETCHES = [
    {"name": "push-one-side-down",
     "idea": "a number reported alone gets pushed, and the cost shows up in the number beside it",
     "verb": "push down", "prop": "U-shaped tube of liquid",
     "alt": "A worker pushes a plunger down one arm of a U-shaped tube. The liquid in the other arm rises.",
     "caption": "A number reported alone gets pushed. Report what the feature saved and what it cost, with the review "
                "hours and re-runs beside them.",
     "draw": utube},
]
