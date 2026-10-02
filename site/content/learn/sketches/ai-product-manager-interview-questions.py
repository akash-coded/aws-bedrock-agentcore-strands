"""Sketch for the AI product manager question bank."""
import math

from pages.sketch import Sk


def marker(s: Sk, x: float, y: float, ang: float, pen: str = "ink", fill: str = "p", n: float = 136) -> None:
    """A whiteboard marker, its middle at ``x, y``, pointing along ``ang`` degrees: a barrel and a cap."""
    co, si = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    s.rect(x - n / 2, y - 16, n, 32, pen, fill=fill, tilt=ang)
    cx, cy = x + co * n * 0.36, y + si * n * 0.36
    s.rect(cx - n * 0.14, cy - 16, n * 0.28, 32, pen, fill=pen, tilt=ang)


def pens(s: Sk):
    # an interview-room whiteboard, the model in front of it, and a person holding two markers:
    # the one that wipes off is held out to the model, the permanent one is kept up and away
    s.ground(540, 50, 1150, tufts=2)
    s.rect(70, 200, 300, 210, fill="p")                     # the whiteboard
    s.line(112, 410, 102, 540)
    s.line(328, 410, 338, 540)
    s.curve([(110, 262), (160, 248), (200, 270), (250, 252)], "aside", "t")
    s.curve([(110, 318), (170, 306), (230, 322)], "aside", "t")
    s.hatch(246, 296, 84, 56, gap=13)                       # a mistake, already wiped
    s.bot(480, 447, 1.6, look=(1, -0.2))
    s.worker(880, 339, look=(-1, 0.1), arms=[(748, 404), (1030, 266)])
    marker(s, 690, 384, 200)                                # offered, cap first
    marker(s, 1044, 206, -76, "point", "point")             # kept
    s.note(540, 110, "right most|of the time", (490, 318), "aside")
    s.label(690, 500, "wipes off", "path")
    s.arrow(690, 446, 686, 414, "path", w="t", head=15)
    s.note(990, 92, "permanent", (1050, 136), "point")


SKETCHES = [
    {"name": "the-pen-that-wipes-off",
     "idea": "the one question under every round: what may software that is right most of the time do alone; "
             "the reversible things, yes, the permanent ones stay with a person",
     "verb": "hand over", "prop": "whiteboard marker that wipes off",
     "alt": "A small machine stands at a whiteboard with a wiped patch on it. A worker holds out a whiteboard marker "
            "to it, and keeps a second, permanent marker raised out of its reach.",
     "caption": "Software that is right most of the time may hold the pen that wipes off. "
                "The permanent one stays with a person.",
     "draw": pens},
]
