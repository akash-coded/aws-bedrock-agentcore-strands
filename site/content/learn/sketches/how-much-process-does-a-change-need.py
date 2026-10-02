"""Sketches for the lesson on how much process a change needs."""
from pages.sketch import Sk


def sieve(s: Sk):
    # a kitchen sieve sorts by size: the big harmless lumps stay in it, the one small hot thing falls through
    s.ground(540, 50, 1150, tufts=2)
    s.worker(250, 339, look=(1, 0.2), arms=[None, (452, 262)])
    s.line(452, 262, 520, 256, w="h")                           # the handle
    for t in (0.35, 0.68):                                      # the mesh
        s.curve([(520 + 130 * t * 0.6, 262 + 80 * t), (650, 262 + 100 * t), (780 - 130 * t * 0.6, 262 + 80 * t)], "faint", "t")
    for dx in (-60, 0, 60):
        s.curve([(650 + dx, 270), (650 + dx * 0.8, 320), (650 + dx * 0.5, 350)], "faint", "t")
    s.curve([(520, 258), (560, 330), (650, 356), (740, 330), (780, 258)], "ink", "h")
    for dx, r in ((-70, 34), (4, 42), (76, 32)):                # what stays in it
        s.pebble(650 + dx, 268, r)
    s.oval(650, 262, 130, 14)
    s.marble(650, 430, 13, "point", fill="point")               # what does not
    s.line(640, 376, 640, 402, "point", "t")
    s.line(660, 372, 660, 400, "point", "t")
    s.curve([(540, 474), (566, 534), (650, 540), (734, 534), (760, 474)], "ink", "h")     # the bowl underneath
    s.oval(650, 474, 110, 12)
    s.label(300, 120, "sorted by size", "aside")
    s.note(960, 150, "big refactor:|caught", (742, 236), "ink")
    s.label(960, 400, "one line:|the refund cap", "point")
    s.arrow(820, 424, 682, 430, "point", bend=-10, w="t", head=15)


def mitten(s: Sk, x: float, y: float, k: int = 1):
    """An oven glove lying on the floor, its fingers toward ``k``."""
    pts = [(-58, -24), (-18, -26), (-8, -46), (14, -48), (20, -28), (44, -26), (62, -6), (60, 14), (40, 24), (-58, 22)]
    s.stroke([(x + k * a, y + b) for a, b in pts], closed=True, amp=1.0)
    s.line(x - k * 34, y - 24, x - k * 34, y + 22, w="t")


def gloves(s: Sk):
    # the oven gloves lie on the floor where they were thrown, and the worker reaches for the one hot dish bare-handed
    s.ground(540, 50, 1150, tufts=2)
    mitten(s, 150, 512)
    mitten(s, 300, 514, -1)
    s.table(690, 400, w=380, h=140)
    s.rect(800, 336, 190, 64, fill="p")                         # a casserole, straight from the oven
    s.curve([(796, 336), (840, 306), (950, 306), (994, 336)], "ink", "h")
    s.oval(895, 298, 12, 8, fill="p")
    s.line(772, 352, 800, 352, w="h")
    s.line(990, 352, 1018, 352, w="h")
    for dx in (-52, 0, 52):
        s.curve([(895 + dx, 276), (883 + dx, 256), (905 + dx, 238), (893 + dx, 218)], "point", "t")
    s.worker(500, 339, look=(1, 0.2), arms=[None, (766, 352)])
    s.burst(760, 338, 18, 4, a0=-210, a1=-90)
    s.note(240, 320, "too heavy for|most jobs", (226, 468), "aside")
    s.note(900, 96, "the one that|needed them", (895, 204), "point")


SKETCHES = [
    {"name": "small-falls-through-the-sieve",
     "idea": "sizing process by the size of the change catches the big harmless ones and lets the small dangerous one through",
     "verb": "sift", "prop": "a kitchen sieve over a bowl",
     "alt": "A worker holds a kitchen sieve over a bowl. Three big lumps sit caught in the sieve. One small red thing "
            "has fallen straight through the mesh toward the bowl.",
     "caption": "Size the process to the size of the change and the big, harmless ones are caught. The one-line "
                "change to a refund cap falls straight through.",
     "draw": sieve},
    {"name": "gloves-off-for-the-hot-one",
     "idea": "a process too heavy for most changes gets abandoned, and the dangerous few lose it first",
     "verb": "grab bare-handed", "prop": "a hot casserole, oven gloves on the floor",
     "alt": "A pair of oven gloves lies thrown on the floor. A worker reaches bare-handed for a steaming casserole "
            "on the table.",
     "caption": "A process that is too heavy for most changes gets dropped, and the dangerous few are the first to go without it.",
     "draw": gloves},
]
