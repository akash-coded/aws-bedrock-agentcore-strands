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


SKETCHES = [
    {"name": "the-missing-length-of-lead",
     "idea": "a capable model stops short of the customer's systems, and the gap can only be closed by someone standing in it",
     "verb": "stretch between", "prop": "lead too short for the socket",
     "alt": "A small machine's lead stops short of a socket in a wall. A worker stands between them at full stretch, "
            "one hand on the end of the lead and the other on the plug in the socket.",
     "caption": "A capable model stops short of the customer's systems. Most of the gap is integration, access, evidence "
                "and trust, and someone has to stand in it.",
     "draw": gap},
]
