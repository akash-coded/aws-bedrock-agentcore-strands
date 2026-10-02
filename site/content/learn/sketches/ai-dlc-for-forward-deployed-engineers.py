"""Sketches for the field guide for forward-deployed engineers."""
from pages.sketch import Sk


def back_over(s: Sk):
    # the contract as a line down the floor. Their desk is on their side; the decision has ended up on
    # yours, and the worker is shoving it back across.
    s.ground(540, 50, 1150, tufts=2)
    s.line(430, 70, 430, 540, pen="faint", dash=True)
    s.table(100, 420, w=210, h=120)
    s.doc(160, 330, 70, 90, tilt=-6, lines=3)
    s.rock(650, 540, 204, 160)
    s.worker(960, 339, look=(-1, 0.4), arms=[(732, 442), (744, 492)], lean=-12)
    s.arrow(552, 478, 340, 478, "path", dash=True, w="h")
    s.label(230, 130, "theirs to decide", "ink")
    s.label(900, 110, "yours to do", "ink")
    s.note(650, 236, "the refund limit", (648, 372), "point")


SKETCHES = [
    {"name": "back-over-the-contract-line",
     "idea": "a decision that is the customer's, made by the engineer because it was faster, becomes the engineer's risk",
     "verb": "shove back across", "prop": "contract line down the floor",
     "alt": "A dashed line runs down the floor. On one side is the customer's desk. On the other, a worker leans into a "
            "rock labelled the refund limit and shoves it back across the line.",
     "caption": "Setting the customer's refund limit yourself is faster, and it makes their risk yours. Push the decision back to their side of the contract.",
     "draw": back_over},
]
