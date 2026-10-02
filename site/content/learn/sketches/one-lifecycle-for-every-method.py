"""Sketches for the lesson that lays every method on one lifecycle."""
from pages.sketch import Sk


def unwatched(s: Sk):
    # the worker holds up two recipe cards and compares them; behind its back the pot nobody watches boils over
    s.ground(540, 50, 1150, tufts=2)
    s.worker(390, 339, look=(-0.8, -0.7), arms=[(262, 268), (522, 262)])
    s.rect(90, 160, 200, 108, fill="p", tilt=-6)                # two recipe cards, one in each hand
    s.rect(500, 152, 232, 108, fill="p", tilt=5)
    s.label(190, 234, "Scrum", "ink", rot=-6)
    s.label(616, 226, "Spec Kit", "ink", rot=5)
    s.rect(850, 410, 250, 130, fill="p")                        # the stove
    s.line(850, 436, 1100, 436, w="t")
    s.stroke([(905, 330), (912, 408), (1038, 408), (1045, 330)], "ink", "h")      # a saucepan
    s.line(1045, 352, 1128, 340, w="h")
    s.blob(975, 322, 84, 22, "point", fill="p", lumps=6, depth=0.2)               # the froth, over the rim
    s.curve([(900, 334), (890, 370), (896, 404)], "point")
    s.curve([(1050, 338), (1058, 380), (1052, 404)], "point")
    s.drop(872, 392, 0.9, "point")
    s.burst(975, 300, 26, 5)
    s.label(390, 92, "which one wins?", "aside")
    s.note(985, 130, "no method|watches this", (975, 262), "point")


def hatch(s: Sk):
    # a kitchen wall with one serving hatch: three different pans behind it, and the worker at the hatch
    # with a probe in the dish before it goes out
    s.ground(540, 50, 1150, tufts=2)
    s.table(90, 380, w=400, h=160)
    s.rect(130, 300, 96, 80, fill="p")                          # a tall pot, lid on
    s.line(122, 300, 234, 300, w="h")
    s.oval(178, 290, 10, 7, fill="p")
    s.stroke([(268, 352), (276, 380), (366, 380), (374, 352)], "ink", "h")        # a frying pan
    s.line(268, 352, 374, 352)
    s.line(374, 358, 446, 340, w="h")
    s.route([(250, 262), (400, 296), (566, 334)], "path")
    for y0, y1 in ((-8, 250), (372, 540)):                      # the wall, above and below the hatch
        s.rect(600, y0, 76, y1 - y0, fill="p")
        s.hatch(600, y0, 76, y1 - y0, gap=20)
    s.line(566, 372, 724, 372, w="h")                           # the sill
    s.oval(652, 362, 46, 8, fill="p")                           # a dish on it
    s.curve([(622, 358), (652, 330), (682, 358)], "ink")
    s.worker(990, 339, look=(-1, 0.1), arms=[(820, 262), None])
    s.line(820, 262, 668, 346, w="h")                           # the probe, in the dish
    s.oval(820, 262, 17, 17, fill="p")
    s.label(250, 228, "any method", "aside")
    s.label(812, 506, "one way out", "path", size=54)
    s.note(930, 104, "checked before|it leaves", (700, 318), "point")


SKETCHES = [
    {"name": "recipes-and-the-unwatched-pot",
     "idea": "the argument is about which method wins; the same things are missing from all of them",
     "verb": "compare recipe cards beside", "prop": "a saucepan boiling over",
     "alt": "A worker holds up two recipe cards, one marked Scrum and one marked Spec Kit, and looks from one to the "
            "other. Behind its back a saucepan boils over on the stove with nobody watching it.",
     "caption": "The argument is about which method wins. No method says who watches the agent once it is live.",
     "draw": unwatched},
    {"name": "one-hatch-out-of-the-kitchen",
     "idea": "what makes it work is the exits, held on evidence, whatever method does the cooking",
     "verb": "probe each dish at", "prop": "the serving hatch of a kitchen",
     "alt": "Three different pans stand on a kitchen counter behind a wall. The wall has one serving hatch, and a "
            "worker on the other side has a probe in the dish on its sill before letting it out.",
     "caption": "A team can run any method. What it cannot skip is the exit: each phase ends on evidence.",
     "draw": hatch},
]
