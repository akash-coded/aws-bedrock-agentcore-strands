"""Sketches for the lesson on measuring AI productivity."""
from pages.sketch import Sk


def apple(s: Sk, x: float, y: float, r: float = 21):
    s.oval(x, y, r, r, fill="p")
    s.stroke([(x, y - r), (x + 5, y - r - 11)], "ink", "t", amp=0.3)


def barrow(s: Sk, x: float, y: float):
    """A wheelbarrow facing right, its wheel standing at ``x, y``."""
    s.poly([(x - 230, y - 140), (x + 10, y - 140), (x - 30, y - 62), (x - 190, y - 62)], fill="p")
    s.stroke([(x - 222, y - 126), (x - 300, y - 146)], "ink", "h")
    s.stroke([(x - 180, y - 62), (x - 186, y)], "ink")
    s.stroke([(x - 40, y - 62), (x, y - 28)], "ink")
    s.oval(x, y - 28, 28, 28, fill="p", w="h")


def sorting(s: Sk):
    # the model wheels in apples by the barrow; one worker still looks at each apple, one at a time
    s.ground(540, 50, 1150, tufts=2)
    s.bot(112, 453, 1.45, look=(1, 0))
    for ax, ay in ((250, 380), (296, 384), (342, 380), (388, 386), (272, 346), (320, 340), (366, 348), (318, 304)):
        apple(s, ax, ay)
    barrow(s, 420, 540)
    for ax, ay in ((520, 518), (566, 518), (612, 518), (543, 480), (589, 480), (566, 442)):
        apple(s, ax, ay)
    s.worker(800, 339, look=(-1, -0.3), arms=[(664, 300), (946, 452)])
    apple(s, 652, 286)
    apple(s, 980, 456)
    apple(s, 1040, 460)
    s.box(940, 466, 170, 74)
    s.note(270, 150, "98% more arrive", (310, 270), "aside")
    s.label(850, 120, "same readers, same pace", "point")
    s.label(1040, 330, "delivery|stays flat", "ink")


SKETCHES = [
    {"name": "one-apple-at-a-time",
     "idea": "a model raises how much is produced; the same people still read it, so delivery does not move",
     "verb": "check one at a time", "prop": "wheelbarrow of apples",
     "alt": "A small machine with one eye has wheeled in a barrow heaped with apples, and more lie in a pile. One worker "
            "holds a single apple up to look at it and puts the checked ones in a crate.",
     "caption": "Faros AI measured 98% more pull requests merged per developer and flat delivery: more changes were produced, and the same number of people read them.",
     "draw": sorting},
]
