"""Sketches for the lesson on catching drift."""
import math

from pages.sketch import Sk


def exhaust(s: Sk):
    # the machine runs fine; what comes out of its exhaust has changed. The worker nets a puff to look at it
    s.ground(540, 50, 1150, tufts=0)
    s.bot(190, 441, 1.7, look=(1, 0))
    s.pipe([(270, 478), (372, 478)], r=11)
    s.cloud(826, 186, 130, 76, "aside")                      # the old puffs, drifting off
    s.cloud(1000, 104, 150, 84, "aside")
    s.cloud(432, 452, 64, 40, "point")                       # the new ones
    s.cloud(530, 394, 90, 56, "point")
    s.cloud(650, 316, 96, 56, "point")
    s.oval(650, 318, 68, 44, w="h")                          # the net
    s.curve([(584, 326), (640, 412), (716, 326)], "ink")
    s.stroke([(712, 340), (806, 404)], "ink", "h")
    s.worker(940, 339, look=(-1, -0.1), arms=[(800, 400), None])
    s.label(190, 290, "up and fast", "ink")
    s.note(540, 110, "used to be refunds", (752, 176), "aside")
    s.label(480, 510, "now: more credits", "point", anchor="start")


def puncture(s: Sk):
    # a tyre going down a little every week: a squeeze says it is the same as last week, the gauge says
    # how far it is from where it started
    s.ground(540, 50, 1150, tufts=2)
    s.oval(720, 392, 152, 148, w="h")                        # the tyre
    s.oval(720, 388, 86, 86)
    s.oval(720, 388, 14, 14, fill="ink")
    s.stroke([(836, 498), (872, 530)], "point", "h", amp=0.3)                    # the nail
    s.stroke([(862, 540), (882, 520)], "point", "h", amp=0.3)
    s.curve([(848, 306), (900, 334), (954, 330)], "ink")     # the hose to the gauge
    s.dial(1040, 330, r=88, at=0.38, zone=(0.38, 0.7))
    a = math.pi * 0.3
    s.stroke([(1040 + 94 * math.cos(a), 330 - 94 * math.sin(a)), (1040 + 120 * math.cos(a), 330 - 120 * math.sin(a))],
             "aside", "h", amp=0.3)
    s.worker(400, 339, look=(1, 0.2), arms=[None, (566, 384)])
    s.label(430, 96, "1.9 points a week", "ink")
    s.label(430, 160, "5% alert: never fired", "aside")
    s.note(1010, 104, "thirteen points|since week one", (1058, 224), "point")


SKETCHES = [
    {"name": "what-comes-out-of-the-exhaust",
     "idea": "up-and-fast monitoring cannot see a change in behaviour; the mix of what comes out can, the same day",
     "verb": "net a puff from", "prop": "exhaust pipe of the machine",
     "alt": "A small machine runs with puffs coming out of its exhaust pipe. The older puffs drifting away are drawn in "
            "blue and the newest in red. A worker catches one of the new ones in a net.",
     "caption": "The dashboards say the system is up and fast. Only the mix of what comes out shows it now offers "
                "credits where it offered refunds.",
     "draw": exhaust},
    {"name": "a-slow-puncture",
     "idea": "a slide too slow for a weekly alert is still a long way from where it started",
     "verb": "squeeze", "prop": "tyre with a slow puncture",
     "alt": "A worker squeezes a tyre that has a small nail in it. A gauge on a hose shows the needle well below a mark "
            "made in week one.",
     "caption": "A slide of 1.9 points a week never trips a 5% weekly alert. Against a frozen baseline it is thirteen "
                "points by week eight.",
     "draw": puncture},
]
