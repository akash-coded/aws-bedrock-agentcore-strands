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


def _brick_wall(s: Sk, x: float, y: float, w: float, h: float, lean: float, courses: int = 7):
    """A brick wall standing on ``y`` from ``x`` to ``x + w``, its top pushed ``lean`` units to the right."""
    def at(u: float, v: float) -> tuple[float, float]:        # u along the course, v up the wall, both 0 to 1
        return x + w * u + lean * v, y - h * v

    s.poly([at(0, 0), at(1, 0), at(1, 1), at(0, 1)], fill="p", w="h")
    for i in range(1, courses):
        s.stroke([at(0, i / courses), at(1, i / courses)], "ink", "t", amp=0.6)
    for i in range(courses):                                   # the joints, one course staggered against the next
        for u in ((0.25, 0.75) if i % 2 else (0.5,)):
            s.stroke([at(u, i / courses), at(u, (i + 1) / courses)], "ink", "t", amp=0.3)


def plumb(s: Sk):
    # a brick wall already built, and only now a plumb line held up beside it: it leans
    s.ground(540, 50, 1150, tufts=2)
    _brick_wall(s, 640, 540, 210, 380, 74)
    for bx, by, tilt in ((930, 520, 0), (968, 498, -14)):      # two bricks left over
        s.rect(bx, by, 76, 22, fill="p", tilt=tilt)
    s.worker(350, 339, look=(1, -0.6), arms=[(596, 300), (596, 172)], lean=5)
    s.line(596, 172, 596, 462, w="t")                           # the line
    s.poly([(582, 462), (610, 462), (596, 502)], fill="ink")    # the bob
    s.arrow(608, 186, 700, 186, "point", w="t", head=13)        # the gap at the top
    s.arrow(700, 186, 608, 186, "point", w="t", head=13)
    s.label(280, 100, "pass mark|set after", "point")
    s.arrow(420, 136, 578, 164, "point", bend=-10, w="t", head=15)
    s.note(1036, 250, "built first", (912, 300), "ink")
    s.label(1040, 410, "argued at|launch", "aside")


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
