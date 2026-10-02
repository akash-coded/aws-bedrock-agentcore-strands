"""Sketches for the lesson on proving an agent meets its bar."""
from pages.sketch import Sk


def pick(s: Sk):
    # a jar of plain marbles with a red one or two in it; the worker lifts the red ones out one at a time
    # and puts them in a tray of their own
    s.ground(540, 50, 1150, tufts=2)
    s.stroke([(170, 320), (184, 540), (436, 540), (450, 320)], "ink", "h")       # the jar
    for i, (x, y) in enumerate(((222, 514), (274, 516), (326, 514), (378, 516), (248, 470), (300, 472),
                                (352, 470), (404, 474), (222, 428), (274, 428), (326, 430), (378, 428),
                                (248, 386), (300, 384), (352, 386), (404, 388))):
        s.oval(x, y, 24, 24, fill="point" if i == 5 else "p")
    s.stroke([(800, 478), (814, 540), (1006, 540), (1020, 478)], "ink", "h")     # the tray
    for x in (856, 910, 964):
        s.oval(x, 512, 24, 24, "point", fill="point")
    s.worker(610, 339, look=(1, 0.5), arms=[(450, 262), (800, 420)])
    s.oval(432, 250, 24, 24, "point", fill="point")
    s.oval(818, 430, 24, 24, "point", fill="point")
    s.label(300, 200, "everyday cases", "ink")
    s.note(640, 110, "rare, costly", (452, 226), "point")
    s.note(960, 300, "take extra|of these", (930, 470), "aside")


SKETCHES = [
    {"name": "pick-the-rare-ones-by-hand",
     "idea": "a sample that looks like traffic holds almost none of the rare, costly cases, so those are drawn on purpose",
     "verb": "pick out one by one", "prop": "jar of marbles and a tray",
     "alt": "A jar is full of plain marbles with one red one among them. A worker lifts a red marble out with one hand "
            "and sets another in a tray that holds only red ones.",
     "caption": "A sample that looks like traffic holds few of the rare, costly cases. Draw each kind separately and "
                "take extra of those.",
     "draw": pick},
]
