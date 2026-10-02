"""Sketches for the SkyWays case study."""
from pages.sketch import Sk


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
    {"name": "a-sign-or-a-sizer",
     "idea": "a limit written in a prompt is a notice; a limit in the tool's signature is a frame the amount must fit",
     "verb": "shove into", "prop": "bag sizer at the gate",
     "alt": "A notice on a post reads max $400. Beside it stands a metal bag sizer. A worker shoves a large bag marked "
            "$2,000 at the sizer and it will not go in.",
     "caption": "The $400 limit was a line in the prompt, and the refund tool accepted any amount. A sign asks; a frame "
                "the bag must fit refuses.",
     "draw": sizer},
]
