"""Sketches for the SkyWays case study."""
from pages.sketch import Sk


def _case(s: Sk, x: float, y: float, w: float = 110, h: float = 80) -> None:
    """A shut suitcase standing on ``y``, its left side at ``x``."""
    s.rect(x, y - h, w, h, fill="p")
    s.curve([(x + w * 0.34, y - h), (x + w * 0.4, y - h - 17), (x + w * 0.6, y - h - 17), (x + w * 0.66, y - h)])
    s.line(x + w * 0.24, y - h + 5, x + w * 0.24, y - 5, w="t")
    s.line(x + w * 0.76, y - h + 5, x + w * 0.76, y - 5, w="t")


def belt(s: Sk):
    # a luggage belt out of a wall: two shut suitcases, and one that has burst. The worker does not lift
    # the burst one off; it ties a tag to it and lets it ride
    s.ground(540, 50, 1150, tufts=2)
    s.rect(60, 190, 62, 350, fill="p")                                         # the wall the belt comes out of
    s.hatch(60, 190, 62, 350, gap=26)
    s.conveyor(140, 740, 400)
    for px in (236, 650):
        s.line(px, 440, px, 540)
    _case(s, 180, 398, 110, 78)
    _case(s, 340, 398, 86, 112)
    s.poly([(506, 320), (492, 226), (628, 214), (642, 308)], fill="p")         # the burst one: its lid thrown back
    s.blob(574, 306, 62, 24, lumps=4, depth=0.2)                               # what was in it, coming out
    s.rect(500, 318, 150, 80, fill="p")
    s.curve([(600, 320), (616, 300), (640, 312), (646, 350), (628, 366), (636, 380)], "ink")   # a sleeve over the side
    s.burst(580, 268, 30, 4, "point", -150, -30)
    s.curve([(650, 352), (676, 376), (712, 344)], "ink", "t")                  # the string of the tag
    s.rect(708, 306, 104, 62, fill="p", tilt=-6)
    s.scribble(722, 320, 76, 36, 2)
    s.worker(950, 339, look=(-1, 0.1), arms=[(816, 338), None])
    s.label(268, 232, "13 episodes", "ink")
    s.note(430, 110, "failures stay in", (560, 200), "point")
    s.note(900, 168, "what it left behind", (770, 300), "aside")
    s.route([(150, 586), (450, 578), (760, 586)], "path")


def sizer(s: Sk):
    # a notice on a post says the limit; a metal frame is the limit. The worker shoves an oversized bag at the
    # frame, and one corner goes in and no more
    import math
    s.ground(540, 50, 1150, tufts=2)
    s.sign(180, 540, "max $400", "ink", post=150)
    for px in (620, 760):                                                       # the sizer: a rack the bag must fit
        s.line(px, 300, px, 540, w="h")
        s.line(px - 20, 540, px + 20, 540, w="h")
    s.line(620, 462, 760, 462, w="h")
    s.stroke([(642, 376), (738, 376), (738, 450), (642, 450)], "faint", "t", closed=True, dash=True)   # what would fit
    cx, cy, co, si = 762, 212, math.cos(math.radians(-25)), math.sin(math.radians(-25))

    def at(dx: float, dy: float) -> tuple[float, float]:
        return cx + dx * co - dy * si, cy + dx * si + dy * co

    s.rect(cx - 125, cy - 80, 250, 160, fill="p", tilt=-25)                     # the bag, one corner in the mouth
    s.curve([at(-32, -80), at(-24, -106), at(24, -106), at(32, -80)], "ink")
    for dx in (-92, 92):
        s.stroke([at(dx, -76), at(dx, 76)], "ink", "t")
    s.oval(*at(100, 92), 13, 13, fill="p")
    s.label(*at(0, 20), "$2,000", "ink", rot=-25, note=False)
    s.burst(690, 318, 26, 3, "point", 150, 230)
    s.worker(1040, 339, look=(-1, -0.4), arms=[(896, 190), None], lean=-9)
    s.note(200, 130, "written in|the prompt", (180, 290), "point")
    s.label(580, 480, "a cap in code", "aside", anchor="end")
    s.arrow(500, 430, 606, 404, "aside", bend=-14, w="t", head=15)


SKETCHES = [
    {"name": "failures-ride-the-belt",
     "idea": "the case keeps its failures in, because each one left a control behind that the next feature inherits",
     "verb": "tag", "prop": "burst suitcase on a luggage belt",
     "alt": "Suitcases ride a luggage belt out of a wall. One has burst open. A worker does not lift it off; it ties "
            "a tag to it and lets it ride on with the others.",
     "caption": "Each of the four failures left something behind that the next feature inherits, so the case keeps them in.",
     "draw": belt},
    {"name": "a-sign-or-a-sizer",
     "idea": "a limit written in a prompt is a notice; a limit in the tool's signature is a frame the amount must fit",
     "verb": "shove into", "prop": "bag sizer at the gate",
     "alt": "A notice on a post reads max $400. Beside it stands a metal bag sizer. A worker shoves a large bag marked "
            "$2,000 at the sizer and it will not go in.",
     "caption": "The $400 limit was a line in the prompt, and the refund tool accepted any amount. A sign asks; a frame "
                "the bag must fit refuses.",
     "draw": sizer},
]
