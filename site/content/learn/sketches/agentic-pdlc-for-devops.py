"""Sketches for the lesson on DevOps and platform teams."""
from pages.sketch import Sk


def tap(s: Sk):
    # a garden tap left running into a bed with nothing in it; the meter on the hose has been turning all along,
    # and the worker has only now got a hand to the tap
    s.ground(530, 50, 1150, tufts=2)
    s.rect(80, 468, 380, 62, fill="p")                       # the raised bed, bare
    s.curve([(88, 466), (150, 452), (230, 462), (310, 450), (390, 462), (452, 456)], "ink", "t")
    s.line(680, 530, 680, 290, w="h")                        # the standpipe
    s.stroke([(680, 312), (610, 312), (610, 346)], "ink", "h")
    s.line(652, 284, 720, 284, w="h")                        # its handle
    s.curve([(610, 346), (606, 430), (570, 486)], "ink")     # the hose, down to the meter
    s.curve([(520, 470), (480, 446), (440, 436)], "ink")     # and on to the bed
    s.oval(548, 484, 42, 42, fill="p")                       # the meter, on the hose
    s.stroke([(548, 484), (572, 460)], "point", "h", amp=0.4)
    for dx, dy in ((0, 0), (-24, 16), (-8, -22)):
        s.drop(420 + dx, 436 + dy, 0.8)
    s.worker(900, 328, look=(-1, 0.3), arms=[(724, 284), None], lean=-5)
    s.label(222, 404, "nothing planted", "ink")
    s.note(440, 130, "meter already running", (544, 432), "point")
    s.note(930, 110, "on since week two", (700, 268), "aside")


SKETCHES = [
    {"name": "a-tap-left-on-over-bare-soil",
     "idea": "some of what this workload needs bills for existing, so the cost starts before the feature does",
     "verb": "shut off", "prop": "garden tap running onto a bare bed",
     "alt": "A garden tap runs through a hose onto a raised bed with nothing planted in it. A meter on the hose is "
            "turning. A worker has just got a hand to the tap.",
     "caption": "Some services bill for existing, not for use. The meter starts before a single line of the feature is written.",
     "draw": tap},
]
