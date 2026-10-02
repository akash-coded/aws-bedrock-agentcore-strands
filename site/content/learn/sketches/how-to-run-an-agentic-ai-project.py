"""Sketches for the twelve-step playbook lesson."""
from pages.sketch import Sk


def underpin(s: Sk):
    # the house is already up, standing on two props, and the worker is digging its foundations in underneath
    s.curve([(50, 452), (250, 448), (452, 452)], "ink")                           # the ground, left of the trench
    s.stroke([(452, 452), (476, 560), (914, 560), (936, 452)], "ink")             # the trench
    s.curve([(936, 452), (1040, 450), (1150, 454)], "ink")
    s.worker(250, 251, look=(1, 0.7), arms=[(330, 390), (402, 330)], lean=8)
    s.line(402, 330, 500, 520, w="h")                           # the spade
    s.poly([(486, 506), (522, 498), (532, 544), (498, 552)], fill="p")
    s.blob(130, 430, 64, 26, lumps=3, depth=0.1)                # what has come out so far
    for px in (560, 800):                                       # the props
        s.rect(px, 440, 26, 120, fill="p")
    s.rect(520, 200, 350, 240, fill="p")                        # the house
    s.poly([(486, 204), (695, 70), (904, 204)], fill="p")
    s.rect(730, 330, 70, 110)
    s.rect(570, 330, 80, 62)
    s.label(695, 290, "prototype", "ink", size=54)
    s.note(1024, 312, "requirements|dug in after", (906, 524), "point", size=54)


SKETCHES = [
    {"name": "foundations-dug-under-the-house",
     "idea": "when the prototype comes first, what it should stand on is dug in under it afterwards",
     "verb": "dig foundations under", "prop": "a finished house on two props",
     "alt": "A small house marked prototype stands on two props over a trench. A worker digs under it with a spade, "
            "putting the foundations in after the house.",
     "caption": "Build the prototype first and the requirements get written around it. The order of the twelve steps is the point.",
     "h": 620, "draw": underpin},
]
