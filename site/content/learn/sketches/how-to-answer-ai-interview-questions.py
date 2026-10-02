"""Sketches for the lesson on answering AI interview questions."""
from pages.sketch import Sk


def weigh(s: Sk):
    # a check-in scale: the worker heaves a lumpy sack onto the plate before it will say any number, and the
    # pass mark is read off the dial afterwards
    s.ground(540, 50, 1150, tufts=2)
    s.line(850, 540, 850, 262, w="h")
    s.dial(850, 262, 96, at=0.78)
    s.rect(560, 500, 290, 40, fill="p")
    s.sack(690, 500, 180, 160)
    s.stroke([(668, 420), (712, 464)], "point", "h", amp=0.6)
    s.stroke([(712, 420), (668, 464)], "point", "h", amp=0.6)
    s.worker(330, 339, look=(1, 0.4), arms=[None, (606, 420)], lean=6)
    s.note(420, 120, "what a mistake costs", (668, 340), "point")
    s.arrow(790, 470, 790, 300, "path", dash=True, w="h")
    s.label(1040, 376, "then the|pass mark", "aside")
    s.arrow(1020, 326, 948, 236, "aside", bend=-14, w="t", head=15)


SKETCHES = [
    {"name": "weigh-the-mistake-first",
     "idea": "the answer that scores starts with what a mistake costs, and only then says how good is good enough",
     "verb": "weigh first", "prop": "check-in scale",
     "alt": "A worker heaves a lumpy sack marked with a cross onto the plate of a check-in scale. A dial stands at the "
            "end of the plate, and its needle has moved.",
     "caption": "The strongest signal in an AI interview: the candidate asks what a mistake costs before saying how good is good enough.",
     "draw": weigh},
]
