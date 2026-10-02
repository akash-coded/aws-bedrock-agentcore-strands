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


def poster(s: Sk):
    # the board of things the checkpoint knows to look for: three, each ticked. The worker pins up a fourth,
    # which is the only way the board ever learns it
    s.ground(540, 50, 1150, tufts=2)
    s.rect(110, 196, 660, 232, fill="p")
    for px in (190, 690):
        s.line(px, 428, px, 540)
    s.oval(196, 262, 13, 13, w="t")                              # scissors
    s.oval(232, 262, 13, 13, w="t")
    s.stroke([(202, 274), (236, 336)], "ink")
    s.stroke([(226, 274), (192, 336)], "ink")
    s.rect(350, 276, 44, 62, fill="p")                           # a bottle
    s.rect(362, 250, 20, 26, fill="p")
    s.oval(530, 302, 34, 34, fill="p")                           # a round thing with a fuse
    s.curve([(548, 272), (562, 252), (580, 256)], "ink", "t")
    for cx in (214, 372, 530):
        s.stroke([(cx - 20, 384), (cx - 5, 400), (cx + 26, 360)], "aside", "h", amp=0.6)
    star = [(690, 250), (704, 290), (744, 282), (716, 314), (742, 350), (700, 340), (684, 380), (670, 338), (628, 346), (654, 314),
            (630, 280), (672, 290)]
    s.poly(star, "point", fill="p")                              # the new one, going up
    s.worker(940, 339, look=(-1, -0.1), arms=[(748, 316), None])
    s.label(400, 160, "last quarter's attacks", "ink")
    s.label(440, 500, "all tests pass", "aside")
    s.note(930, 130, "this quarter's", (722, 262), "point")


def arrivals(s: Sk):
    # the arrivals door, and the worker already there holding up a card with the name of what is coming
    s.ground(540, 50, 1150, tufts=2)
    s.door(930, 540, w=160, h=290, ajar=True)
    s.rect(240, 92, 330, 100, fill="p", tilt=-2)
    s.label(405, 162, "surprise bill", "point", rot=-2, note=False)
    s.worker(405, 339, look=(1, 0.1), arms=[(262, 196), (548, 190)])
    s.label(1010, 226, "arrivals", "ink")
    s.label(590, 336, "named before|it lands", "aside", anchor="start")
    s.arrow(578, 350, 516, 344, "aside", bend=10, w="t", head=15)
    s.route([(900, 584), (720, 578), (540, 586)], "path")


SKETCHES = [
    {"name": "the-wind-did",
     "idea": "a quiet failure follows no change of yours, so the check runs on a clock, not on a complaint",
     "verb": "walk out to read", "prop": "windsock",
     "alt": "A windsock points one way; a faint outline shows it pointed the other way before. A worker walks out to it "
            "carrying a calendar with a tick on it.",
     "caption": "Behaviour drifts with no deploy and no alarm. The check runs every week, even when nothing changed.",
     "draw": windsock},
    {"name": "pin-up-this-quarters",
     "idea": "a suite that stops growing keeps passing, because it only tests the attacks it already knows",
     "verb": "pin up", "prop": "board of known shapes at a checkpoint",
     "alt": "A board shows three known items, each with a tick under it. A worker pins a fourth, spiky shape drawn in "
            "red onto the end of the board.",
     "caption": "A suite that has not grown in three months tests last quarter's attacks and reports green. Extend it every quarter.",
     "draw": poster},
    {"name": "someone-meets-the-bill",
     "idea": "nobody waits for a bill or an incident to come back, so the person who meets it is named before it lands",
     "verb": "wait for", "prop": "name card at the arrivals door",
     "alt": "A worker stands facing an arrivals door and holds a name card above its head. The card reads surprise bill.",
     "caption": "Nobody downstream is waiting for a bill, an incident or a governance check. Each needs a named owner before the event, not after it.",
     "draw": arrivals},
]
