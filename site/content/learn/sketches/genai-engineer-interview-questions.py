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
    # a glass on the interview table, already full of passages; the worker tips in still more from a carafe,
    # and the one passage that mattered is a single dot somewhere in the middle
    s.ground(540, 50, 1150, tufts=2)
    s.table(520, 440, w=330, h=100)
    s.stroke([(596, 262), (614, 440), (766, 440), (784, 262)], "ink", "h")          # the glass
    s.curve([(600, 290), (650, 296), (720, 286), (780, 292)], "aside")              # nearly full
    for x, y in ((640, 322), (722, 318), (752, 352), (630, 366), (744, 398), (668, 404), (708, 424), (640, 420)):
        dot(s, x, y)
    dot(s, 690, 362, "point", 10)                           # the one that mattered
    s.worker(280, 339, look=(1, -0.3), arms=[None, (470, 134)])
    lx, ly = carafe(s, 484, 88)
    s.curve([(lx, ly), (lx + 22, ly + 10), (lx + 34, ly + 34), (lx + 38, ly + 68)], "aside")   # what it pours
    dot(s, lx + 44, ly + 22)
    dot(s, lx + 58, ly + 50)
    s.label(240, 110, "more passages", "ink")
    s.note(990, 180, "the one that|mattered", (708, 360), "point")
    s.route([(880, 500), (960, 400), (1030, 410), (1110, 500)], "path")
    s.label(1000, 370, "accuracy", "path")


SKETCHES = [
    {"name": "one-drop-in-a-full-glass",
     "idea": "retrieving more passages sounds like the safe fix; past a point they dilute the one that mattered",
     "verb": "dilute", "prop": "glass of water",
     "alt": "A worker tips a carafe of small drops into a glass that is already full of them. One red drop sits in "
            "the middle of the glass. Beside it a dashed line rises and then falls.",
     "caption": "More retrieved passages sounds like the safe fix. Past a point they dilute the one that mattered, "
                "so measure accuracy against k before adding more.",
     "draw": pour},
]
