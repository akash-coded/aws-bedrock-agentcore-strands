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
    s.note(330, 494, "build: two days", (294, 430), "aside", size=54, anchor="start")


def timer(s: Sk):
    # an egg timer as tall as the worker: it runs at the speed of its neck, however hard it is shaken
    s.ground(550, 50, 1150, tufts=2)
    s.rect(520, 92, 250, 18, fill="p")
    s.rect(520, 532, 250, 18, fill="p")
    s.poly([(554, 176), (736, 176), (716, 246), (654, 312), (636, 312), (574, 246)], "faint", fill="faint")   # the sand still to run
    s.poly([(590, 532), (700, 532), (645, 486)], "faint", fill="faint")                                       # what has come through
    s.line(645, 318, 645, 484, "faint", "t")
    s.curve([(540, 110), (562, 240), (636, 318), (562, 400), (540, 532)], "ink", "h")
    s.curve([(750, 110), (728, 240), (654, 318), (728, 400), (750, 532)], "ink", "h")
    s.worker(290, 349, look=(1, 0), arms=[(548, 420), (552, 226)], lean=6)
    for x0, y0, k in ((800, 120, 1), (806, 520, 1), (494, 100, -1)):             # it is being shaken
        s.curve([(x0, y0), (x0 + k * 14, y0 + 18), (x0, y0 + 38)], "ink", "t")
    s.note(960, 150, "500 cases", (726, 206), "ink")
    s.label(1150, 336, "5% of 240 a day", "aside", anchor="end")
    s.arrow(790, 322, 676, 318, "aside", w="t", head=15)
    s.label(960, 470, "42 days", "point")
    s.squiggle(880, 486, 160)


def oven(s: Sk):
    # the pie is made and in the worker's hands; the oven nobody switched on is still cold
    s.ground(540, 50, 1150, tufts=2)
    s.rect(750, 250, 300, 290, fill="p")                        # the oven
    s.line(750, 300, 1050, 300, w="t")
    s.oval(800, 275, 11, 11)
    s.oval(850, 275, 11, 11)
    s.rect(790, 350, 220, 150)
    s.line(800, 328, 1000, 328, w="h")
    for a, b in (((868, 425), (932, 425)), ((884, 397), (916, 453)), ((916, 397), (884, 453))):      # cold inside
        s.line(a[0], a[1], b[0], b[1], "aside", "t")
    s.worker(380, 339, look=(1, 0.1), arms=[None, (548, 372)])
    s.line(532, 378, 700, 372, w="h")                           # the tray
    s.curve([(556, 372), (616, 326), (676, 370)], "ink")        # the pie
    s.curve([(586, 354), (616, 342), (646, 352)], "ink", "t")
    s.note(500, 150, "the work, ready", (606, 316), "ink")
    s.label(900, 130, "model access:", "ink")
    s.label(900, 196, "still cold", "point")
    s.label(160, 300, "ask in|week one", "aside")


SKETCHES = [
    {"name": "sawing-two-days-off-the-plank",
     "idea": "AI shortens the build, and the build was the smallest part of the wait",
     "verb": "saw the end off", "prop": "a long plank on two trestles",
     "alt": "A long plank lies on two trestles, marked along its length as three months to launch. A worker has sawn "
            "a small piece off one end, marked build, two days. The plank looks as long as before.",
     "caption": "The agent wrote the feature in two days and it launched in three months. The time went to the parts nobody redesigned.",
     "draw": saw},
    {"name": "everything-ready-oven-cold",
     "idea": "some waits sit in someone else's queue, so start them on day one",
     "verb": "stand with a pie at", "prop": "a cold oven",
     "alt": "A worker stands holding a finished pie on a tray in front of an oven. The oven is marked model access and "
            "it is still cold.",
     "caption": "SkyWays lost six days because nobody had requested model access in the region the data had to stay in. Request every one in week one.",
     "draw": oven},
    {"name": "shaking-the-egg-timer",
     "idea": "live evidence arrives at the speed of traffic: the arithmetic, not the effort",
     "verb": "shake", "prop": "an egg timer as tall as the worker",
     "alt": "A worker grips an egg timer as tall as itself and shakes it. The sand marked 500 cases still runs through "
            "the narrow neck, marked 5% of 240 a day, a grain at a time.",
     "caption": "500 cases at a 5% canary of 240 cases a day takes 42 days. That is the arithmetic, not the effort.",
     "h": 620, "draw": timer},
]
