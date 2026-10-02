"""Sketches for the lesson on the maturity model."""
from pages.sketch import Sk


def rake(s: Sk, x: float, y0: float, y1: float):
    s.line(x, y0, x, y1, w="h")
    s.stroke([(x - 36, y1), (x + 36, y1)], "ink", "h", amp=0.5)
    for dx in (-36, -18, 0, 18, 36):
        s.stroke([(x + dx, y1), (x + dx, y1 - 22)], "ink", amp=0.3)


def spade(s: Sk, x: float, y0: float, y1: float):
    s.line(x, y0, x, y1 + 60, w="h")
    s.poly([(x - 26, y1 + 60), (x + 26, y1 + 60), (x + 22, y1 + 12), (x, y1 - 6), (x - 22, y1 + 12)], fill="p")


def hurdle(s: Sk, x: float, y: float, w: float = 110, h: float = 150, last: bool = False):
    """One panel of a farm fence, its left post standing at ``x, y``."""
    s.line(x, y, x, y - h, w="h")
    if last:
        s.line(x + w, y, x + w, y - h, w="h")
    s.line(x, y - h + 26, x + w, y - h + 26)
    s.line(x, y - 44, x + w, y - 44)
    s.line(x, y - 44, x + w, y - h + 26, w="t")


def tools(s: Sk):
    # the worker holds up a rake and a spade, with more behind; along the field the fence has a panel missing
    # and the model is standing in the gap
    s.ground(540, 50, 1150, tufts=2)
    rake(s, 60, 540, 250)
    spade(s, 400, 540, 230)
    s.worker(230, 339, look=(1, -0.2), arms=[(116, 250), (344, 250)])
    rake(s, 116, 420, 130)
    spade(s, 344, 420, 110)
    for i in range(6):
        if i != 3:
            hurdle(s, 480 + i * 110, 540, last=i in (2, 5))
    s.bot(865, 482, 1.0, look=(1, 0))
    s.route([(880, 552), (960, 572), (1090, 566)], "path")
    s.label(230, 84, "many tools", "ink")
    s.note(690, 150, "count what is enforced", (620, 380), "point")
    s.note(1000, 270, "the agent,|through the gap", (880, 410), "aside")


SKETCHES = [
    {"name": "tools-in-hand-and-a-gap-in-the-fence",
     "idea": "maturity is the controls that hold, not the tools bought",
     "verb": "hold up", "prop": "garden tools beside a gapped fence",
     "alt": "A worker holds up a rake and a spade, with more tools standing behind. Along the field runs a fence with one "
            "panel missing, and a small machine with one eye stands in the gap, about to walk out.",
     "caption": "A team with many AI tools and no gates is less mature than a team with one tool and tight control. Count the controls.",
     "draw": tools},
]
