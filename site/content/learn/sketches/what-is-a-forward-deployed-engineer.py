"""Sketches for the lesson on the forward deployed engineer."""
from pages.sketch import Sk


def _plug(s: Sk, x: float, y: float, pen: str = "ink") -> None:
    """A travel adaptor standing on ``y``, centred on ``x``: a block with two pins up."""
    s.rect(x - 28, y - 46, 56, 46, pen, fill="p")
    for dx in (-11, 11):
        s.stroke([(x + dx, y - 46), (x + dx, y - 66)], pen, "h", amp=0.3)


def gap(s: Sk):
    # the model's lead stops short of the customer's socket, and the worker is the missing length:
    # one hand on the lead, the other on the plug in the wall
    s.ground(540, 50, 1150, tufts=2)
    s.bot(170, 453, 1.5, look=(1, 0))
    s.curve([(239, 440), (300, 424), (370, 372), (424, 326)], "aside")          # the lead, pulled tight
    s.rect(884, 150, 266, 390, fill="p")                                        # the customer's wall
    s.rect(900, 380, 58, 58, fill="p")                                          # and the socket in it
    for dx in (20, 38):
        s.stroke([(900 + dx, 398), (900 + dx, 420)], "ink", "h", amp=0.3)
    s.rect(864, 396, 34, 26, fill="ink")                                        # the plug, home
    s.curve([(864, 409), (852, 408), (842, 404)], "ink")
    s.worker(640, 339, look=(1, 0.2), arms=[(424, 326), (842, 404)])
    s.label(170, 258, "capable|model", "aside")
    s.label(1018, 252, "customer's|systems", "ink")
    s.stroke([(428, 198), (428, 178), (428, 188), (840, 188), (840, 178), (840, 198)], "point", "t", note=True)
    s.label(634, 152, "the distance", "point")


def home(s: Sk):
    # back from the trip with a suitcase open on the floor: the worker sets a third adaptor on the product team's
    # bench beside two that are just the same
    s.ground(540, 50, 1150, tufts=2)
    s.poly([(150, 452), (120, 352), (306, 332), (336, 452)], fill="p")          # the suitcase, lid up
    s.curve([(196, 344), (200, 324), (236, 320), (244, 339)], "ink")            # the handle on the lid
    s.rect(150, 450, 190, 90, fill="p")
    for sx in (196, 294):
        s.line(sx, 454, sx, 536, w="t")
    s.tag(340, 440, 70, 42)
    s.table(770, 400, w=350, h=140)
    _plug(s, 930, 398)
    _plug(s, 1040, 398)
    _plug(s, 820, 392)
    s.ring(820, 362, 56, 52)
    s.worker(560, 339, look=(1, 0.2), arms=[None, (790, 372)], legs="walk")
    s.note(640, 140, "built a third time", (806, 300), "point")
    s.label(1010, 262, "now a pattern", "aside")
    s.label(946, 496, "product team", "ink")
    s.route([(360, 586), (560, 578), (760, 586)], "path")


SKETCHES = [
    {"name": "the-missing-length-of-lead",
     "idea": "a capable model stops short of the customer's systems, and the gap can only be closed by someone standing in it",
     "verb": "stretch between", "prop": "lead too short for the socket",
     "alt": "A small machine's lead stops short of a socket in a wall. A worker stands between them at full stretch, "
            "one hand on the end of the lead and the other on the plug in the socket.",
     "caption": "A capable model stops short of the customer's systems. Most of the gap is integration, access, evidence "
                "and trust, and someone has to stand in it.",
     "draw": gap},
    {"name": "the-third-adaptor-goes-home",
     "idea": "a connector built for the third time is a pattern, and the trip is not over until it reaches the product team",
     "verb": "carry home", "prop": "travel adaptor in a suitcase",
     "alt": "A suitcase stands open on the floor. A worker walks from it to a bench and sets down a travel adaptor beside "
            "two identical ones.",
     "caption": "A connector built for the third time is a gap in the product. The FDE carries it home as a pattern.",
     "draw": home},
]
