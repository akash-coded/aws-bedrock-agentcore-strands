"""Sketch for the lesson on what a forward-deployed engineer is."""
import math

from pages.sketch import Sk


def _arc(s: Sk, cx: float, by: float, rx: float, ry: float, a0: float = 180, a1: float = 0, n: int = 10,
         tilt: float = 0.0) -> list[tuple[float, float]]:
    """Points on an ellipse round ``cx, by`` from angle ``a0`` to ``a1`` (degrees, y up), with a slight wobble."""
    ph, co, si = s.r.uniform(0, 6.28), math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    out = []
    for i in range(n + 1):
        th = math.radians(a0 + (a1 - a0) * i / n)
        k = 1 + 0.025 * math.sin(2 * th + ph)
        dx, dy = rx * k * math.cos(th), -ry * k * math.sin(th)
        out.append((cx + dx * co - dy * si, by + dx * si + dy * co))
    return out


def _crown(s: Sk, pts: list[tuple[float, float]]):
    """A hat's crown: the outline in one smooth line over a paper fill that hides what is behind it.
    (``Sk.poly`` draws each side as its own stroke, which turns a curve into scallops.)"""
    s._fill(pts, "p")
    s.stroke(pts, raw=True)


# The hats, each standing on ``cx, by``, the middle of its base. Each has a shape a stranger names at a
# glance; the hats that were only a dome read as dish covers.
def hard_hat(s: Sk, cx: float, by: float):
    _crown(s, _arc(s, cx, by, 60, 62))
    s.line(cx - 84, by, cx + 92, by - 2, w="h")
    s.line(cx - 2, by - 60, cx - 4, by - 2, w="t")


def cap(s: Sk, cx: float, by: float, face: int = -1):
    """A peaked cap, the peak to the left (``face`` -1) or the right (1): a pale crown and a dark peak."""
    s.poly([(cx + face * x, by + y) for x, y in ((28, -6), (72, -2), (106, 12), (66, 16), (26, 8))], fill="ink")
    _crown(s, _arc(s, cx, by, 48, 52))
    s.line(cx - 44, by + 1, cx + 48, by, w="t")
    s.line(cx + 2, by - 52, cx - 6 * face, by - 2, w="t")
    s.oval(cx + 2, by - 54, 8, 6, fill="ink")


def top_hat(s: Sk, cx: float, by: float):
    s.curve([(cx - 62, by - 8), (cx - 40, by + 4), (cx, by + 7), (cx + 40, by + 4), (cx + 62, by - 8)], w="h")
    s.rect(cx - 34, by - 78, 68, 76, fill="p")
    s.rect(cx - 34, by - 22, 68, 13, fill="ink")


def beret(s: Sk, cx: float, by: float):
    _crown(s, _arc(s, cx, by - 6, 66, 30, tilt=-7) + _arc(s, cx, by - 6, 66, 9, 0, -180, 6, tilt=-7)[1:])
    s.line(cx - 2, by - 36, cx + 6, by - 54, w="h")


def beanie(s: Sk, cx: float, by: float):
    _crown(s, _arc(s, cx, by - 18, 46, 54))
    s.rect(cx - 52, by - 22, 104, 24, fill="p")
    s.blob(cx, by - 80, 15, 14, lumps=6, depth=0.12)


def bowler(s: Sk, cx: float, by: float):
    _crown(s, _arc(s, cx, by - 6, 46, 56))
    s.rect(cx - 46, by - 20, 92, 12, fill="ink")
    s.curve([(cx - 80, by - 16), (cx - 56, by + 2), (cx, by + 6), (cx + 56, by + 2), (cx + 80, by - 16)], w="h")


def stand(s: Sk, x: float, foot: float, top: float, hooks: list[tuple[int, float]]):
    """A hat stand: a pole on three feet, a knob on top, and hooks that turn up at the tip. ``hooks`` is
    (side, height) for each: -1 to the left of the pole, 1 to the right."""
    s.line(x, foot - 34, x, top, w="h")
    for dx in (-74, 0, 74):
        s.line(x, foot - 34, x + dx, foot, w="h")
    s.oval(x, top - 10, 13, 13, fill="p")
    for side, y in hooks:
        s.curve([(x, y + 14), (x + side * 40, y + 10), (x + side * 60, y - 8)], w="h")


def swap(s: Sk):
    # A hat stand with the jobs on its hooks. The worker wears one hat and takes the next off its hook; the two
    # arrows trade them: one person, every hat, one at a time. Learnt from the strangers' readings: a label
    # beside the worker becomes who it is (so it is the engineer's, an FDE's own trade), labels stacked close
    # read as one title (so the stand's are a line apart), and a coloured label becomes the subject (so all
    # are ink, and only the swap is in the path's orange).
    s.ground(600, 50, 1150, tufts=2)
    stand(s, 470, 600, 92, [(-1, 158), (-1, 270), (-1, 382), (-1, 494), (1, 290)])
    top_hat(s, 388, 150)
    beret(s, 384, 262)
    beanie(s, 386, 376)
    bowler(s, 388, 488)
    cap(s, 548, 288, face=1)
    s.worker(800, 399, look=(-1, -0.3), arms=[(652, 298), None], lean=-4)
    hard_hat(s, 798, 306)
    s.arrow(604, 232, 742, 232, "path", bend=34, dash=True, w="h")
    s.arrow(782, 222, 590, 218, "path", bend=-70, dash=True, w="h")
    s.label(522, 204, "QA", "ink")
    s.label(902, 252, "engineer", "ink", anchor="start")
    s.label(296, 136, "product", "ink", anchor="end")
    s.label(296, 254, "architect", "ink", anchor="end")
    s.label(296, 366, "platform", "ink", anchor="end")
    s.label(296, 478, "consultant", "ink", anchor="end")


SKETCHES = [
    {"name": "six-hats-one-head",
     "idea": "an FDE may do every job at a customer, one at a time, and no job lets the FDE take the customer's decisions",
     "verb": "swap", "prop": "hat stand", "h": 660,
     "alt": "Beside a hat stand holding hats labelled product, architect, platform and consultant, a small worker in a "
            "hard hat labelled engineer takes a cap labelled QA off the stand, and two arrows swap the cap and the hard hat.",
     "caption": "Some weeks you are the whole team at a customer, one hat at a time. No hat lets you take the customer's own decisions.",
     "draw": swap},
]
