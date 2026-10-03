"""Sketches for the lesson on cutting delivery time."""
from pages.sketch import Sk


def trestle(s: Sk, x: float, top: float, foot: float):
    s.line(x - 10, top, x - 50, foot)
    s.line(x + 10, top, x + 50, foot)
    s.line(x - 32, top + 96, x + 32, top + 96, w="t")


def saw(s: Sk):
    # a long plank on two trestles; the worker saws a sliver off one end, and the plank is as long as ever
    s.ground(540, 50, 1150, tufts=2)
    trestle(s, 700, 364, 540)
    trestle(s, 1050, 364, 540)
    s.rect(302, 330, 820, 34, fill="p")                         # the plank
    s.rect(246, 404, 40, 34, fill="p", tilt=24)                 # the bit that came off
    s.line(232, 380, 240, 396, "faint", "t")
    s.line(262, 372, 266, 390, "faint", "t")
    s.worker(140, 339, look=(1, 0.2), arms=[None, (300, 250)])
    s.poly([(278, 250), (324, 250), (304, 398), (292, 398)], fill="p")            # the saw
    s.stroke([(324, 250), (310, 270), (320, 284), (307, 304), (316, 318), (304, 338)], "ink", "t", amp=0.4)
    s.stroke([(336, 190), (1120, 190)], "ink", "t")             # how long the whole thing is
    s.line(336, 176, 336, 204, w="t")
    s.line(1120, 176, 1120, 204, w="t")
    s.label(728, 160, "launch: three months", "ink")
    s.note(740, 278, "nobody redesigned this", (890, 326), "point", bend=6)
    s.note(330, 494, "build: two days", (294, 430), "aside", anchor="start")


SKETCHES = [
    {"name": "sawing-two-days-off-the-plank",
     "idea": "AI shortens the build, and the build was the smallest part of the wait",
     "verb": "saw the end off", "prop": "a long plank on two trestles",
     "alt": "A long plank lies on two trestles, marked along its length as three months to launch. A worker has sawn "
            "a small piece off one end, marked build, two days. The plank looks as long as before.",
     "caption": "The agent wrote the feature in two days and it launched in three months. The time went to the parts nobody redesigned.",
     "draw": saw},
]
