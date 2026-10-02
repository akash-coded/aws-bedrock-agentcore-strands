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


def seedling(s: Sk, x: float, y: float, h: float = 70, pen: str = "ink"):
    s.curve([(x, y), (x + 4, y - h * 0.5), (x, y - h)], pen)
    for k in (-1, 1):
        tip = (x + k * h * 0.78, y - h * 1.24)
        s.curve([(x, y - h), (x + k * h * 0.3, y - h * 1.36), tip], pen)
        s.curve([(x, y - h), (x + k * h * 0.44, y - h * 0.98), tip], pen)


def marker(s: Sk, x: float, y: float):
    """A plant label on a stick, with a name on it."""
    s.line(x, y, x, y - 84)
    s.rect(x - 30, y - 118, 60, 36, fill="p")
    s.stroke([(x - 18, y - 100), (x + 16, y - 101)], "aside", "t", amp=1.2)


def labels(s: Sk):
    # a row of seedlings, each with a name on a stick; the worker pushes in the next one. Further back along the
    # path, something nobody labelled has come up with thorns on
    s.ground(540, 50, 1150, tufts=1)
    s.curve([(240, 540), (226, 470), (262, 410), (236, 340), (256, 300)], "point", "h")      # the thorn
    for tx, ty, k in ((232, 500, -1), (238, 456, 1), (256, 412, -1), (246, 370, 1), (240, 334, -1)):
        s.stroke([(tx, ty), (tx + k * 40, ty - 22)], "point", amp=0.4)
    s.stroke([(200, 540), (220, 528), (240, 542), (262, 528), (282, 540)], "ink", "t", amp=0.4)
    for x in (760, 900, 1040):
        seedling(s, x, 540, 46)
    marker(s, 966, 540)
    marker(s, 1106, 540)
    s.worker(520, 339, look=(1, 0.4), arms=[None, (822, 436)], lean=5)
    marker(s, 826, 540)
    s.label(270, 190, "dropped in week one,", "ink")
    s.label(270, 250, "back in week five", "point")
    s.note(910, 230, "each credited by name", (968, 410), "aside")


SKETCHES = [
    {"name": "past-the-safe-to-the-pennies",
     "idea": "the first feature is picked because it can be proven, not because it is worth the most",
     "verb": "steer past", "prop": "roped off safe and a table of pennies",
     "alt": "A bank safe stands roped off at one end. A worker walks a small machine with one eye past it, towards a "
            "table with small stacks of coins.",
     "caption": "Pick the first feature for provability, not value. The flagship has the highest bar, the least tolerance for a first attempt and the most spectators.",
     "draw": pennies},
    {"name": "a-name-on-every-seedling",
     "idea": "a requirement nobody credited comes back later as a constraint",
     "verb": "label", "prop": "seedlings with name markers",
     "alt": "A worker pushes a name marker into the ground beside a seedling, in a row where every seedling has one. "
            "Further back, a thorny stem has come up through the path.",
     "caption": "Credit every requirement to the person who raised it, in writing. A voice dropped in week one comes back in week five as a constraint.",
     "draw": labels},
]
