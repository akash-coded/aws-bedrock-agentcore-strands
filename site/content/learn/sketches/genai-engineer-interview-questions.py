"""Sketch for the GenAI engineer question bank."""
import math

from pages.sketch import Sk


def dot(s: Sk, x: float, y: float, pen: str = "aside", r: float = 8) -> None:
    s.oval(x, y, r, r, pen, fill=pen if pen == "point" else "")


def carafe(s: Sk, x: float, y: float, ang: float = 35) -> tuple[float, float]:
    """A carafe tipped to pour, the middle of its base at ``x, y``, its neck pointing along ``ang`` degrees.
    Returns the low side of its lip, where the water leaves."""
    co, si = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def t(u: float, v: float) -> tuple[float, float]:
        return x + u * co - v * si, y + u * si + v * co

    s.poly([t(0, -46), t(118, -46), t(152, -17), t(214, -17), t(214, 17), t(152, 17), t(118, 46), t(0, 46)], fill="p")
    return t(214, 17)


def pour(s: Sk):
    # a glass on the interview table, already full of passages; the worker tips in still more from a carafe
    # with both hands, and the one passage that mattered is a single dot somewhere in the middle
    s.ground(540, 50, 1150, tufts=2)
    s.table(560, 440, w=330, h=100)
    s.stroke([(636, 262), (654, 440), (806, 440), (824, 262)], "ink", "h")          # the glass
    s.curve([(640, 290), (690, 296), (760, 286), (820, 292)], "aside")              # nearly full
    for x, y in ((680, 322), (762, 318), (792, 352), (670, 366), (784, 398), (708, 404), (748, 424), (680, 420)):
        dot(s, x, y)
    dot(s, 730, 362, "point", 10)                           # the one that mattered
    s.worker(320, 339, look=(1, -0.2), arms=[(500, 124), (578, 184)], lean=8)
    lx, ly = carafe(s, 524, 88)
    s.curve([(lx, ly), (lx + 22, ly + 10), (lx + 34, ly + 34), (lx + 38, ly + 68)], "aside")   # what it pours
    dot(s, lx + 44, ly + 22)
    dot(s, lx + 58, ly + 50)
    s.label(60, 110, "more passages", "ink", anchor="start")
    s.note(1010, 190, "the one that|mattered", (748, 360), "point")


SKETCHES = [
    {"name": "one-drop-in-a-full-glass",
     "idea": "retrieving more passages sounds like the safe fix; past a point they dilute the one that mattered",
     "verb": "dilute", "prop": "glass of water",
     "alt": "A worker tips a carafe of small drops, with both hands, into a glass that is already full of them. "
            "One red drop sits in the middle of the glass.",
     "caption": "More retrieved passages sounds like the safe fix. Past a point they dilute the one that mattered, "
                "so measure accuracy against k before adding more.",
     "draw": pour},
]
