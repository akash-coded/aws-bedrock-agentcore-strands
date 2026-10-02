"""Sketches for the lesson for product managers."""
from pages.sketch import Sk


def _pin(s: Sk, x: float, y: float):
    s.stroke([(x, y), (x + 15, y - 19)], "point", "t", amp=0.4)
    s.oval(x + 17, y - 23, 6, 6, "point", fill="point")


def _scissors(s: Sk, x: float, y: float, pen: str = "aside"):
    # open scissors, blades to the left, the pivot at x, y
    s.stroke([(x - 84, y - 24), (x + 40, y + 14)], pen, "h", amp=0.5)
    s.stroke([(x - 84, y + 24), (x + 40, y - 14)], pen, "h", amp=0.5)
    s.oval(x + 58, y + 22, 19, 14, pen)
    s.oval(x + 58, y - 22, 19, 14, pen)


def pattern(s: Sk):
    # a cutting table: the worker pins the paper pattern to the cloth, and the model waits with the
    # scissors. It will cut where the pins are and nowhere else, and it will not ask.
    s.ground(540, 60, 1140, tufts=2)
    s.poly([(340, 330), (820, 330), (872, 450), (288, 450)], fill="p")       # the table top
    s.line(306, 452, 306, 540)
    s.line(854, 452, 854, 540)
    s.poly([(378, 344), (770, 344), (806, 436), (346, 436)], "faint")                # the cloth
    s.poly([(424, 356), (560, 356), (606, 390), (590, 426), (412, 426)], fill="p")   # the pattern piece
    s.worker(190, 339, look=(1, 0.4), arms=[None, (438, 376)])
    for px, py in ((440, 372), (548, 370), (476, 420)):
        _pin(s, px, py)
    s.bot(1020, 447, 1.6, look=(-1, 0.3))
    s.stroke([(946, 448), (890, 420)], "aside")
    _scissors(s, 814, 398)
    s.arrow(722, 398, 622, 394, "path", dash=True, w="h")
    s.note(500, 210, "the spec", (500, 352), "ink")
    s.note(950, 110, "cannot ask|what you meant", (1016, 322), "point")
    s.label(580, 514, "cuts what is pinned", "path")


SKETCHES = [
    {"name": "pin-the-pattern-before-the-cut",
     "idea": "a coding agent builds exactly what the spec says and cannot ask what you meant, so the deciding moves before the build",
     "verb": "pin down", "prop": "paper pattern on a cutting table",
     "alt": "A worker pins a paper pattern to cloth on a cutting table. Across the table a small machine holds open "
            "scissors at the edge of the cloth, waiting to cut where the pins are.",
     "caption": "A coding agent builds exactly what the spec says and cannot ask what you meant. The deciding happens before the cut.",
     "draw": pattern},
]
