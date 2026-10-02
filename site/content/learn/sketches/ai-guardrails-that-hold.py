"""Sketches for the lesson on guardrails that hold."""
import math

from pages.sketch import Sk


def novalve(s: Sk):
    # a notice hangs from the pipe and says what the limit is; where the valve should be there is only pipe,
    # and the worker's hands close on nothing while the money runs out of the far end
    s.ground(540, 50, 1150, tufts=2)
    s.pipe([(60, 190), (870, 190), (902, 222), (902, 300)], r=20)
    ring = [(430 + 52 * math.cos(i * math.pi / 8), 186 + 52 * math.sin(i * math.pi / 8)) for i in range(16)]
    s.stroke(ring, "point", "", closed=True, dash=True, raw=True)                # the valve that is not there
    s.line(606, 212, 614, 270, w="t")                        # the notice, on its strings
    s.line(774, 212, 766, 270, w="t")
    s.rect(560, 270, 260, 104, fill="p", tilt=2)
    s.label(690, 342, "limit $400", "ink", rot=2, note=False)
    for x, y in ((900, 336), (912, 396), (892, 452)):        # what comes out of the far end
        s.coin(x, y, 22)
    s.stack(902, 530, 4, 110)
    s.worker(430, 339, look=(0, -1), arms=[(392, 214), (468, 214)])
    s.note(640, 84, "nothing here refuses", (490, 150), "point")
    s.label(980, 470, "$2,000", "point", anchor="start")


def letter(s: Sk):
    # a letter comes in from outside with an order written in it; the worker ties a label on it before the
    # machine gets to read it
    s.ground(540, 50, 1150, tufts=2)
    s.route([(60, 236), (180, 300), (300, 336)], "path")
    s.envelope(320, 280, 200, 126, tilt=-6)
    s.stroke([(356, 376), (474, 366)], "point", "h")         # the line that is an order
    s.curve([(506, 396), (532, 428), (540, 452)], "ink", "t")
    s.rect(474, 452, 160, 76, fill="p", tilt=-5)             # the label
    s.oval(492, 474, 5, 5, w="t")
    s.label(560, 510, "data", "aside", size=56, rot=-5, note=False)
    s.worker(720, 339, look=(-1, 0.3), arms=[(526, 344), (636, 490)])
    s.bot(1020, 441, 1.7, look=(-1, 0))
    s.arrow(836, 446, 924, 446, "path", dash=True, w="h")
    s.label(160, 190, "from outside", "path")
    s.note(420, 120, "an order hidden inside", (410, 356), "point")
    s.label(1020, 296, "the model", "aside")


SKETCHES = [
    {"name": "a-notice-where-the-valve-should-be",
     "idea": "a limit that is only written down reads like a limit and stops nothing",
     "verb": "reach for the valve on", "prop": "pipe with a notice and no valve",
     "alt": "A notice reading limit $400 hangs from a pipe. A worker reaches up for a valve that is not there, and "
            "coins marked $2,000 pour out of the far end of the pipe.",
     "caption": "A limit written in a prompt reads like a limit and refuses nothing. Ask to see the line of code that "
                "says no.",
     "draw": novalve},
    {"name": "a-label-on-the-letter",
     "idea": "anything the agent reads can carry an order, so what arrives from outside is marked as data",
     "verb": "tie a label on", "prop": "letter from outside",
     "alt": "A letter arrives from outside with one line in it drawn in red. A worker ties a label reading data to it "
            "before passing it to a small machine.",
     "caption": "Any text the agent reads can carry instructions. Tag what arrives from outside as data, and test that "
                "no attack string moves money.",
     "draw": letter},
]
