"""Sketches for the lesson for QA."""
from pages.sketch import Sk


def frayed(s: Sk):
    # a length of cloth hangs from a rail and has to reach a line. Its loose threads reach; the woven
    # edge stops short. The worker pins the place where the weave ends.
    s.ground(600, 50, 430, tufts=2)
    s.line(440, 58, 790, 58, w="h")
    s.rect(474, 60, 280, 372, fill="p")
    for i, ln in enumerate((52, 78, 40, 92, 64, 84, 48, 72, 96, 58, 80, 44)):                # the fray
        x = 486 + i * 23.5
        s.stroke([(x, 434), (x + (4 if i % 2 else -3), 434 + ln)], "ink", "t", amp=0.9)
    s.line(380, 456, 812, 456, pen="path", w="h", dash=True)
    s.worker(250, 399, look=(1, 0.3), arms=[None, (470, 428)])
    s.stroke([(470, 428), (494, 420)], "point", "h", amp=0.4)
    s.oval(468, 428, 7, 7, "point", fill="point")
    s.label(614, 250, "412 of 500", "ink")
    s.note(960, 250, "lower bound:|79.1%", (764, 430), "point")
    s.label(830, 474, "pass mark: 80%", "path", anchor="start")
    s.note(950, 596, "score: 82.4%", (760, 516), "ink")


def tape(s: Sk):
    # the judge's own tape measure laid along a wooden rule. The marks drift apart, and by the far end
    # they are well out.
    s.ground(540, 50, 1150, tufts=2)
    s.table(400, 420, w=500, h=120)
    s.rect(430, 392, 440, 27, fill="p")                                    # the rule
    for i in range(1, 8):
        s.stroke([(430 + i * 55, 392), (430 + i * 55, 406)], "ink", "t", amp=0.3)
    s.line(430, 354, 930, 354, pen="aside", w="h")                         # the judge's tape
    for i in range(1, 8):
        s.stroke([(430 + i * 63, 354), (430 + i * 63, 368)], "aside", "t", amp=0.3)
    s.oval(948, 350, 20, 20, "aside", fill="p")
    s.oval(948, 350, 7, 7, "aside")
    s.bot(1050, 447, 1.6, look=(-1, -0.2))
    s.stroke([(976, 440), (956, 372)], "aside")
    s.worker(220, 339, look=(1, 0.3), arms=[None, (428, 372)])
    s.ring(858, 374, 40, 34)
    s.label(1040, 300, "the judge", "aside")
    s.note(640, 110, "error: unknown|until checked", (848, 336), "point")
    s.label(650, 492, "human labels", "ink")


SKETCHES = [
    {"name": "the-last-sure-thread",
     "idea": "a score from a sample has a ragged edge; only the part you are sure of counts against the pass mark",
     "verb": "pin the woven edge of", "prop": "frayed length of cloth",
     "alt": "A length of cloth hangs from a rail and has to reach a dashed line. Its loose threads hang past the line, "
            "but the woven edge stops just short of it. A worker pins the woven edge.",
     "caption": "412 of 500 is 82.4%, but the sample only proves 79.1%. That is under the 80% pass mark, so this kind of case does not pass.",
     "h": 640, "draw": frayed},
    {"name": "check-the-judges-tape",
     "idea": "a model judge is a measuring instrument with an unknown error until it is calibrated against people",
     "verb": "lay against a rule", "prop": "tape measure and a wooden rule",
     "alt": "A worker lays a small machine's blue tape measure along a wooden rule on a table. The marks on the two "
            "drift apart, and the far end is ringed in red.",
     "caption": "A model judge is a measuring instrument. Until it is checked against human labels, nobody knows how far off it reads.",
     "draw": tape},
]
