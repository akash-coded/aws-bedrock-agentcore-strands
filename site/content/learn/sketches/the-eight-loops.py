"""Sketches for the lesson on the eight loops."""
from pages.sketch import Sk


def parcel(s: Sk, x: float, y: float, w: float = 120, h: float = 90):
    """A parcel tied with string, its top left at ``x, y``."""
    s.rect(x, y, w, h, fill="p")
    s.line(x + w * 0.5, y, x + w * 0.5, y + h, w="t")
    for k in (-1, 1):                                         # the bow
        s.curve([(x + w * 0.5, y), (x + w * 0.5 + k * 22, y - 20), (x + w * 0.5 + k * 30, y - 4), (x + w * 0.5, y)], "ink", "t")


def readdress(s: Sk):
    # the bill arrives in an envelope addressed to finance; the worker holds it steady, strikes that out
    # and writes design
    s.ground(540, 50, 1150, tufts=2)
    s.table(250, 420, w=520, h=120)
    s.rect(290, 170, 440, 250, fill="p", tilt=-2)             # the envelope, standing on the desk
    s.rect(640, 188, 56, 66, sw="t", tilt=-2)                 # its stamp
    s.label(480, 290, "to: finance", "ink", rot=-2)
    s.stroke([(352, 278), (612, 268)], "point", "h", note=True)
    s.label(480, 374, "to: design", "point", rot=-2)
    s.worker(930, 339, look=(-1, 0.3), arms=[(736, 250), (690, 372)], lean=-9)
    s.stroke([(690, 372), (636, 384)], "ink", "h")            # the pen
    s.note(950, 84, "4.4 times|the estimate", (716, 180), "ink")


SKETCHES = [
    {"name": "the-bill-readdressed-to-design",
     "idea": "a bill over its estimate is a design question, not a finance question; it closes in a decision record",
     "verb": "re-address", "prop": "envelope with the bill in it",
     "alt": "A large envelope stands on a desk. A worker holds it steady with one hand. The address to finance is "
            "struck out in red and the worker writes to design beneath it.",
     "caption": "A bill that left its estimate goes to design, not to finance. The cost loop closes when a decision "
                "record has a new version.",
     "draw": readdress},
]
