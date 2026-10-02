"""Sketch for the agentic AI engineer question bank."""
from pages.sketch import Sk


def chips(s: Sk):
    # a card table: the engineer behind it slides a short stack of chips to the model and keeps a hand on the
    # locked box that holds the rest; the note on the wall that says "please don't" is the prompt
    s.ground(540, 50, 1150, tufts=2)
    s.doc(84, 96, 130, 150, tilt=-5, lines=3, mark="cross")
    s.bot(170, 447, 1.6, look=(1, -0.2))
    s.worker(650, 300, look=(-1, 0.5), arms=[(470, 392), (850, 322)])
    s.rect(300, 410, 680, 30, fill="p")                     # the table's edge, in front of the worker
    s.line(330, 440, 322, 540)
    s.line(950, 440, 958, 540)
    s.stack(412, 398, 3, 84)
    s.box(790, 326, 150, 84)
    s.lock(865, 376, 0.8)
    s.label(450, 112, "a rule in|the prompt", "point")
    s.arrow(308, 130, 238, 156, "point", bend=10, w="t", head=15)
    s.label(400, 330, "$400", "ink")
    s.note(1010, 190, "more?|ask first", (880, 318), "path")


SKETCHES = [
    {"name": "only-the-chips-it-holds",
     "idea": "a rule in a prompt asks; a limit in the tool is all the agent holds, and more needs approval",
     "verb": "stake", "prop": "short stack of chips",
     "alt": "At a card table a worker slides a short stack of chips to a small machine and keeps the other hand on a "
            "locked box. On the wall behind the machine a note is pinned up, crossed out in red.",
     "caption": "A rule in the prompt asks the agent not to. A limit in the tool means it only holds $400 "
                "and must ask for more.",
     "draw": chips},
]
