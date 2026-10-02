"""Sketch for the forward deployed engineer question bank."""
from pages.sketch import Sk


def knock(s: Sk):
    # the customer's door, padlocked; the engineer knocking on it with the model standing ready beside it;
    # a wall calendar that has already reached week three
    s.ground(540, 50, 1150, tufts=2)
    s.bot(180, 447, 1.6, look=(1, 0))
    s.door(640, 540, w=170, h=310)
    s.lock(800, 404, 1.25, pen="point")
    s.worker(440, 339, look=(1, -0.1), arms=[None, (628, 300)])
    s.burst(640, 300, r=18, n=3, pen="ink", a0=150, a1=210)  # knock, knock
    s.calendar(900, 150, 200, 190)
    s.label(1000, 248, "week|three", "ink")
    s.note(250, 140, "the model: ready", (190, 320), "aside")
    s.label(730, 196, "no access yet", "point")
    s.note(1010, 446, "ask on|day one", (840, 410), "path")


SKETCHES = [
    {"name": "model-ready-door-locked",
     "idea": "an engagement stalls on access to the customer's systems, not on the model; ask for access first",
     "verb": "knock", "prop": "customer's padlocked door",
     "alt": "A worker knocks on a padlocked door. A small machine stands ready beside it. A wall calendar by the "
            "door reads week three.",
     "caption": "Most engagement risk is access and alignment, not the model. "
                "The security review and the data request start on day one.",
     "draw": knock},
]
