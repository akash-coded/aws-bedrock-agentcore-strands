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


def plumb(s: Sk):
    # a wall already built, and only now a plumb line held up beside it: it leans
    s.ground(540, 50, 1150, tufts=3)
    s.poly([(650, 540), (780, 540), (850, 150), (720, 150)], fill="p")            # the wall, leaning
    for i in range(1, 9):
        t = i / 9
        s.line(650 + 70 * t, 540 - 390 * t, 780 + 70 * t, 540 - 390 * t, w="t")
    s.worker(380, 339, look=(1, -0.5), arms=[None, (600, 170)])
    s.line(600, 170, 600, 470, w="t")                           # the line
    s.poly([(586, 470), (614, 470), (600, 508)], fill="ink")    # the bob
    s.arrow(612, 196, 706, 196, "point", w="t", head=13)        # the gap at the top
    s.arrow(706, 196, 612, 196, "point", w="t", head=13)
    s.note(960, 300, "built first", (838, 330), "ink")
    s.note(330, 96, "pass mark|set after", (590, 160), "point")
    s.label(970, 470, "argued at|launch", "aside")


SKETCHES = [
    {"name": "foundations-dug-under-the-house",
     "idea": "when the prototype comes first, what it should stand on is dug in under it afterwards",
     "verb": "dig foundations under", "prop": "a finished house on two props",
     "alt": "A small house marked prototype stands on two props over a trench. A worker digs under it with a spade, "
            "putting the foundations in after the house.",
     "caption": "Build the prototype first and the requirements get written around it. The order of the twelve steps is the point.",
     "h": 620, "draw": underpin},
    {"name": "plumb-line-after-the-wall",
     "idea": "if the build starts before the pass mark is set, good enough is argued at launch",
     "verb": "hold a plumb line to", "prop": "a wall already built",
     "alt": "A worker holds a plumb line up beside a brick wall that is already built. The line hangs straight and the "
            "wall leans away from it.",
     "caption": "When the build starts before the bar is set, \"good enough\" is argued at launch, against a wall that is already up.",
     "draw": plumb},
]
