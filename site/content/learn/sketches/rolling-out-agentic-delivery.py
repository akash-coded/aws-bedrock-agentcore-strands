"""Sketches for the lesson on rolling out agentic delivery."""
from pages.sketch import Sk


def safe(s: Sk, x: float, y: float, w: float = 230, h: float = 260):
    """A bank safe standing with its bottom left at ``x, y``."""
    s.rect(x, y - h, w, h - 14, fill="p", sw="h")
    s.rect(x + 22, y - h + 22, w - 44, h - 58)
    s.oval(x + w * 0.42, y - h * 0.52, 30, 30)
    s.stroke([(x + w * 0.42, y - h * 0.52), (x + w * 0.42 + 16, y - h * 0.52 - 16)], "ink", "h", amp=0.3)
    s.stroke([(x + w * 0.7, y - h * 0.62), (x + w * 0.7, y - h * 0.4)], "ink", "h", amp=0.3)
    for fx in (x + 24, x + w - 24):
        s.stroke([(fx - 14, y), (fx - 14, y - 14), (fx + 14, y - 14), (fx + 14, y)], "ink")


def pennies(s: Sk):
    # a bank floor: the safe is roped off at one end; the worker walks the model past it to a table of small coins
    s.ground(540, 50, 1150, tufts=1)
    safe(s, 110, 540)
    for px in (70, 390):
        s.line(px, 540, px, 430, w="h")
        s.oval(px, 424, 9, 9, fill="p")
    s.string(70, 442, 390, 442, sag=40)
    s.worker(590, 339, look=(1, 0.2), arms=[None, (724, 440)], lean=6, legs="walk")
    s.bot(800, 453, 1.5, look=(1, 0))
    s.table(950, 440, w=180, h=100)
    s.stack(990, 432, 3, 46)
    s.stack(1046, 432, 5, 46)
    s.stack(1100, 432, 2, 46)
    s.route([(400, 578), (640, 586), (900, 574)], "path")
    s.label(225, 230, "the flagship", "point")
    s.label(840, 110, "high volume, low damage", "aside")
    s.note(1040, 250, "start here", (1046, 330), "path")


SKETCHES = [
    {"name": "past-the-safe-to-the-pennies",
     "idea": "the first feature is picked because it can be proven, not because it is worth the most",
     "verb": "steer past", "prop": "roped off safe and a table of pennies",
     "alt": "A bank safe stands roped off at one end. A worker walks a small machine with one eye past it, towards a "
            "table with small stacks of coins.",
     "caption": "Pick the first feature for provability, not value. The flagship has the highest bar, the least tolerance for a first attempt and the most spectators.",
     "draw": pennies},
]
