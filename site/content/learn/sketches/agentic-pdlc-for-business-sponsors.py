"""Sketches for the lesson for business sponsors."""
from pages.sketch import Sk


def seedling(s: Sk, x: float, y: float, h: float = 70, pen: str = "ink", roots: bool = False):
    """A stem with two leaves, growing from ``x, y``. With ``roots`` it has been pulled up."""
    s.curve([(x, y), (x + 4, y - h * 0.5), (x, y - h)], pen)
    for k in (-1, 1):
        tip = (x + k * h * 0.78, y - h * 1.24)
        s.curve([(x, y - h), (x + k * h * 0.3, y - h * 1.36), tip], pen)
        s.curve([(x, y - h), (x + k * h * 0.44, y - h * 0.98), tip], pen)
    if roots:
        for dx in (-20, 2, 22):
            s.curve([(x, y), (x + dx * 0.6, y + 24), (x + dx, y + 46 + abs(dx) * 0.3)], pen, "t")


def pulled(s: Sk):
    # a row of seedlings in someone else's bed; the worker has stepped in and pulled one up to look at its roots
    s.ground(540, 50, 1150, tufts=1)
    s.curve([(520, 540), (580, 522), (720, 526), (880, 520), (1020, 526), (1120, 540)], "ink")   # the bed, heaped
    for x in (730, 850, 970, 1085):
        seedling(s, x, 524, 60)
    s.oval(610, 530, 26, 7, fill="ink")                      # the hole it came out of
    s.worker(300, 339, look=(1, -0.3), arms=[None, (510, 310)], lean=6)
    seedling(s, 510, 310, 74, roots=True)
    for dx, dy in ((-14, 76), (12, 96), (-4, 124), (26, 140)):
        s.oval(510 + dx, 310 + dy, 4, 4, fill="ink")         # soil falling off it
    s.note(740, 130, "pulled up to check", (560, 230), "point")
    s.label(900, 370, "delivery's bed", "ink")
    s.label(250, 130, "the sponsor", "aside")


def yoke(s: Sk):
    # a carrying pole across the worker's shoulders with a pail at each end: neither travels without the other
    s.ground(500, 50, 1150, tufts=2)
    for x in (300, 900):
        s.line(x, 232, x - 56, 372, w="t")
        s.line(x, 232, x + 56, 372, w="t")
        s.bucket(x, 482, 130, 110, level=0.7)
    s.worker(600, 298, look=(1, 0.1), arms=[(452, 232), (748, 232)], legs="walk")
    s.line(270, 232, 930, 232, w="h")                        # the pole
    s.label(250, 96, "43% fewer|person-days", "aside")
    s.label(950, 96, "$310|of tokens", "point")
    s.label(150, 566, "both from the team", "path", anchor="start")
    s.arrow(590, 552, 840, 552, "path", dash=True, w="h")


def brickwall(s: Sk, x: float, y: float, w: float, h: float):
    """A garden wall seen end on, its foot at ``x, y``: a cap, courses, and joints that do not line up."""
    s.rect(x, y - h, w, h, fill="p")
    s.rect(x - 10, y - h - 16, w + 20, 16, fill="p")
    n = int(h / 40)
    for i in range(1, n + 1):
        yy = y - h + i * h / (n + 1)
        s.stroke([(x, yy), (x + w, yy)], "ink", "t", amp=0.6)
        jx = x + w * (0.35 if i % 2 else 0.68)
        s.stroke([(jx, yy), (jx, yy - h / (n + 1))], "ink", "t", amp=0.4)


SKETCHES = [
    {"name": "pulled-up-to-see-the-roots",
     "idea": "a sponsor who reaches into delivery when a number disappoints loses the independent reading",
     "verb": "pull up", "prop": "seedling in someone else's bed",
     "alt": "A row of seedlings grows in a heaped bed. A worker has stepped up to the bed and holds one seedling in the air "
            "by its stem, roots dangling and soil falling off, with a hole where it stood.",
     "caption": "Reach into delivery when a number disappoints and you lose what only a sponsor has: an independent reading of whether it is working.",
     "draw": pulled},
    {"name": "two-pails-on-one-pole",
     "idea": "the saving and the spend arrive together, carried in by the team, or the programme does not survive cycle one",
     "verb": "carry", "prop": "yoke with two pails",
     "alt": "A worker walks with a pole across its shoulders and a pail hanging from each end. One pail is marked 43% fewer "
            "person-days and the other $310 of tokens.",
     "caption": "At day ninety the programme continued because both numbers came from the team, on one line.",
     "draw": yoke},
]
