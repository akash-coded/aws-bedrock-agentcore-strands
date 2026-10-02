"""Sketches for the lesson for QA."""
from pages.sketch import Sk


def tape(s: Sk):
    # the judge's own tape measure laid along a wooden rule. The marks drift apart, and by the far end
    # they are well out. The worker pins the tape's end to the rule's with both hands.
    s.ground(540, 50, 1150, tufts=2)
    s.table(380, 430, w=540, h=110)
    s.rect(420, 380, 470, 50, fill="p", sw="h")                            # the rule: wood, with even marks
    for i in range(1, 10):
        s.stroke([(420 + i * 47, 380), (420 + i * 47, 400 if i % 2 else 410)], "ink", amp=0.3)
    s.rect(420, 332, 540, 40, "aside", fill="p", sw="h")                   # the judge's tape, laid along it
    for i in range(1, 9):
        s.stroke([(420 + i * 58, 372), (420 + i * 58, 354 if i % 2 else 346)], "aside", amp=0.3)
    s.oval(988, 350, 34, 34, "aside", fill="p", w="h")                     # its case
    s.oval(988, 350, 9, 9, "aside")
    s.bot(1066, 459, 1.4, look=(-1, -0.4))
    s.stroke([(1010, 452), (994, 386)], "aside")
    s.worker(210, 339, look=(1, 0.5), arms=[(424, 352), (470, 398)], lean=10)
    s.ring(848, 376, 54, 40)
    s.label(1040, 262, "the judge", "aside")
    s.note(620, 110, "error: unknown|until checked", (832, 330), "point")
    s.label(650, 506, "human labels", "ink")


SKETCHES = [
    {"name": "check-the-judges-tape",
     "idea": "a model judge is a measuring instrument with an unknown error until it is calibrated against people",
     "verb": "lay against a rule", "prop": "tape measure and a wooden rule",
     "alt": "A worker pins a small machine's blue tape measure against a wooden rule on a table with both hands. The marks "
            "on the two drift apart, and the far end is ringed in red.",
     "caption": "A model judge is a measuring instrument. Until it is checked against human labels, nobody knows how far off it reads.",
     "draw": tape},
]
