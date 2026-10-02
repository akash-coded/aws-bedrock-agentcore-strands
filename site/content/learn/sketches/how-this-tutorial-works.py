"""Sketches for the lesson on how the tutorial is built."""
from pages.sketch import Sk


def fork(s: Sk):
    # a road that splits in two at a blank signpost; the worker leans and points up one branch, with the
    # folded map held shut behind its back
    s.curve([(50, 462), (300, 460), (520, 450), (760, 372), (960, 276), (1150, 214)], "ink")      # the road
    s.curve([(50, 544), (300, 546), (560, 552), (800, 572), (1000, 598), (1150, 612)], "ink")
    s.curve([(1150, 268), (980, 328), (800, 412), (668, 474), (820, 496), (1000, 528), (1150, 546)], "ink")
    s.line(676, 470, 676, 330, w="h")                                         # the signpost, both arms blank
    s.poly([(676, 336), (770, 318), (790, 330), (774, 346), (676, 364)], fill="p")
    s.poly([(676, 376), (770, 392), (788, 408), (768, 420), (676, 404)], fill="p")
    s.worker(390, 322, 1.8, look=(1, -0.4), arms=[(246, 392), (566, 300)], lean=9)
    s.poly([(122, 366), (152, 350), (184, 368), (216, 350), (246, 366), (246, 434), (216, 418), (184, 436),
            (152, 418), (122, 434)], "ink", fill="p")                         # the map, folded shut
    for x, y in ((152, 350), (184, 368), (216, 350)):
        s.stroke([(x, y), (x, y + 68)], "ink", "t")
    s.arrow(820, 372, 1010, 286, "path", dash=True, w="h")
    s.note(640, 130, "guess first", (574, 284), "point")
    s.label(170, 300, "map shut", "ink")
    s.label(1010, 418, "wrong guess|still helps", "aside")


SKETCHES = [
    {"name": "guess-the-fork-first",
     "idea": "trying before you look fixes an idea better than rereading, even when the try is wrong",
     "verb": "point the way", "prop": "folded map behind the back at a fork",
     "alt": "A road splits in two at a signpost with nothing written on it. A worker leans and points up one branch, "
            "holding a folded map shut behind its back.",
     "caption": "Trying the problem before you open the answer fixes the idea in memory better than reading it again, "
                "even when the first try is wrong.",
     "h": 640, "draw": fork},
]
