"""Sketches for the lesson that introduces the agentic PDLC."""
from pages.sketch import Sk


def compass(s: Sk):
    # a walker with both hands on a big compass, eyes on the needle, one step from the edge of the ground:
    # the needle is as steady when it is wrong as when it is right
    s.cliff(50, 470, 750, side="left", depth=125)
    s.route([(80, 436), (190, 428), (290, 438)], "path")
    s.worker(450, 269, 1.9, look=(1, 0.5), arms=[(598, 322), (602, 228)], legs="walk")
    cx, cy = 684, 274
    s.oval(cx, cy, 86, 86, fill="p", w="h")                      # the compass, held out in front
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        s.stroke([(cx + dx * 66, cy + dy * 66), (cx + dx * 80, cy + dy * 80)], "ink", "t", amp=0.3)
    s.poly([(cx, cy - 13), (cx + 66, cy), (cx, cy + 13)], "aside", fill="aside")      # the needle, pointing on
    s.poly([(cx, cy - 13), (cx - 66, cy), (cx, cy + 13)], "aside")
    s.note(650, 84, "right most days", (680, 176), "aside")
    s.label(990, 300, "wrong today,|just as steady", "point")
    s.arrow(900, 232, 784, 258, "point", bend=-16, w="t", head=15)
    s.label(1000, 548, "no alarm rings", "ink")


SKETCHES = [
    {"name": "the-needle-never-shakes",
     "idea": "a model is right most of the time and exactly as sure of itself when it is wrong, so nothing warns you",
     "verb": "follow", "prop": "compass at a cliff edge",
     "alt": "A worker walks with both hands on a large compass and its eyes on the needle. The needle points straight "
            "ahead, and one step ahead the ground ends in a drop.",
     "caption": "A model is right most of the time and sounds sure all of the time. When it is wrong, nothing shakes "
                "and no alarm rings.",
     "draw": compass},
]
