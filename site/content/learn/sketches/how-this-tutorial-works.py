"""Sketches for the lesson on how the tutorial is built."""
from pages.sketch import Sk


def pole(s: Sk, x: float, top: float, foot: float):
    """A telegraph pole: a post, a crossbar and two insulators."""
    s.stroke([(x, foot), (x, top)], "ink", "h")
    s.stroke([(x - 38, top + 22), (x + 38, top + 22)], "ink", "h", amp=0.5)
    for dx in (-30, 30):
        s.oval(x + dx, top + 12, 6, 8, "ink", fill="p", w="t")


def telegraph(s: Sk):
    # a line between two poles with sheets pegged along it; the line has parted in the middle, and only
    # the first sheet reached the far pole, where the worker takes it down
    s.ground(540, 50, 1150, tufts=3)
    pole(s, 130, 150, 540)
    pole(s, 700, 150, 540)
    s.doc(186, 222, 84, 104, tilt=26, lines=3)                                # what was still on its way
    s.doc(272, 306, 84, 104, tilt=40, lines=3)
    s.curve([(130, 172), (236, 232), (330, 322), (366, 436)], "ink")          # the dead half, hanging
    s.curve([(700, 172), (600, 226), (520, 300), (500, 378)], "ink")          # the live half, hanging
    s.burst(432, 336, 26, 5, "point", a0=-160, a1=-20)
    s.worker(990, 339, look=(-1, -0.2), arms=[(866, 290), None])
    s.doc(766, 204, 96, 122, tilt=-6, lines=3)                                # the one that got through
    s.note(1000, 96, "the answer", (862, 206), "ink")
    s.note(440, 150, "cut here", (432, 296), "point")
    s.label(250, 506, "the rest", "aside")


def fork(s: Sk):
    # the path splits; the worker points up one branch with the folded map held shut behind its back
    s.curve([(50, 520), (200, 522), (380, 518), (540, 520)], "ink")
    s.curve([(540, 520), (700, 470), (860, 362), (1150, 250)], "ink")
    s.curve([(540, 520), (760, 548), (960, 590), (1150, 612)], "ink")
    s.worker(360, 319, look=(1, -0.3), arms=[(232, 398), (530, 300)])
    s.poly([(120, 372), (150, 356), (182, 374), (214, 356), (244, 372), (244, 440), (214, 424), (182, 442),
            (150, 424), (120, 440)], "ink", fill="p")                         # the map, folded shut
    s.stroke([(150, 356), (150, 424)], "ink", "t")
    s.stroke([(182, 374), (182, 442)], "ink", "t")
    s.stroke([(214, 356), (214, 424)], "ink", "t")
    s.arrow(600, 452, 790, 352, "path", dash=True, w="h")
    s.note(640, 130, "guess first", (548, 284), "point")
    s.note(180, 170, "map shut|till you do", (182, 346), "ink")
    s.label(985, 468, "a wrong guess|still helps", "aside")


SKETCHES = [
    {"name": "the-line-went-dead",
     "idea": "a reader can stop at any point, as a telegraph line could, so the answer travels first",
     "verb": "take down", "prop": "telegraph line that parted mid-story",
     "alt": "A line runs between two telegraph poles with sheets pegged along it. The line has parted in the middle. "
            "A worker at the far pole takes down the one sheet that arrived; the others hang on the dead half.",
     "caption": "A telegraphed story could be cut off at any point, and a reader can stop after one paragraph. So the "
                "first paragraph is the whole answer.",
     "draw": telegraph},
    {"name": "guess-the-fork-first",
     "idea": "trying before you look fixes an idea better than rereading, even when the try is wrong",
     "verb": "point the way", "prop": "folded map behind the back at a fork",
     "alt": "A path splits in two. A worker stands at the split and points up one branch, holding a folded map shut "
            "behind its back.",
     "caption": "Trying the problem before you open the answer fixes the idea in memory better than reading it again, "
                "even when the first try is wrong.",
     "h": 640, "draw": fork},
]
