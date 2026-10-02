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


SKETCHES = [
    {"name": "recipes-and-the-unwatched-pot",
     "idea": "the argument is about which method wins; the same things are missing from all of them",
     "verb": "compare recipe cards beside", "prop": "a saucepan boiling over",
     "alt": "A worker holds up two recipe cards, one marked Scrum and one marked Spec Kit, and looks from one to the "
            "other. Behind its back a saucepan boils over on the stove with nobody watching it.",
     "caption": "The argument is about which method wins. No method says who watches the agent once it is live.",
     "draw": unwatched},
]
