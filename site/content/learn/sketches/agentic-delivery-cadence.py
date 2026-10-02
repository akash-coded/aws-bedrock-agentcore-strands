"""Sketches for the lesson on the operating rhythm."""
from pages.sketch import Sk


def _sock(s: Sk, x: float, top: float, d: int, ghost: bool = False) -> None:
    """A windsock flying from the top of a pole at ``x``, to the right if ``d`` is 1."""
    pen = "faint" if ghost else "ink"
    a, b, c, e = (x, top - 32), (x + d * 214, top + 4), (x + d * 214, top + 40), (x, top + 34)
    if not ghost:
        s._fill([a, b, c, e], "p")
        for t0, t1 in ((0.2, 0.4), (0.6, 0.8)):                 # two red bands
            q = [(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1),
                 (e[0] + (c[0] - e[0]) * t1, e[1] + (c[1] - e[1]) * t1), (e[0] + (c[0] - e[0]) * t0, e[1] + (c[1] - e[1]) * t0)]
            s.poly(q, "point", fill="point", w="t")
    s.stroke([a, b, c, e], pen, "t" if ghost else "", closed=True, dash=ghost)


def windsock(s: Sk):
    # a windsock that has swung round since it was last read: nothing on the ground changed, and nothing rang.
    # The worker walks out to it with a calendar
    s.ground(540, 50, 1150, tufts=3)
    s.line(650, 540, 650, 118, w="h")
    _sock(s, 650, 150, -1, ghost=True)                          # where it pointed last time
    _sock(s, 650, 150, 1)
    s.worker(250, 339, look=(1, -0.6), arms=[None, (366, 372)], legs="walk")
    s.calendar(362, 300, 124, 124)
    s.stroke([(396, 372), (414, 392), (452, 346)], "aside", "h", amp=0.6)
    s.label(200, 110, "we changed|nothing", "aside")
    s.note(1000, 350, "the wind did", (872, 196), "point")
    s.label(520, 276, "every week", "path")
    s.route([(80, 586), (330, 578), (590, 586)], "path")


SKETCHES = [
    {"name": "the-wind-did",
     "idea": "a quiet failure follows no change of yours, so the check runs on a clock, not on a complaint",
     "verb": "walk out to read", "prop": "windsock",
     "alt": "A windsock points one way; a faint outline shows it pointed the other way before. A worker walks out to it "
            "carrying a calendar with a tick on it.",
     "caption": "Behaviour drifts with no deploy and no alarm. The check runs every week, even when nothing changed.",
     "draw": windsock},
]
