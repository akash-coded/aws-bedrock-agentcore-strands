"""Sketches for the P0 Frame lesson."""
from pages.sketch import Sk


def downhill(s: Sk):
    # a meeting table up on a ledge, a gutter running down from it over the engineer's head, and the engineer
    # bent over an open box with both hands in the works, back to the slope, as the question drops in
    s.cliff(40, 200, 250, side="left", depth=350)
    s.table(70, 136, w=150, h=62)
    s.marble(142, 110, 24)
    s.ground(560, 290, 1160, tufts=2)
    s.pipe([(292, 190), (620, 240), (962, 290)], r=15)
    s.marble(470, 193, 22)
    s.box(850, 440, 220, 120, open_=True)
    s.worker(676, 392, 1.58, look=(0.7, 1), arms=[(852, 442), (912, 418)], lean=27)
    s.stroke([(912, 418), (940, 486)], "ink", "h")               # the screwdriver, already in the works
    s.marble(992, 368, 22)                                       # the next one, dropping in
    for dx in (-14, 14):
        s.stroke([(992 + dx, 318), (992 + dx, 336)], "ink", "t", amp=0.4)
    s.label(262, 96, "nobody decided", "point", anchor="start")
    s.arrow(254, 82, 178, 100, "point", bend=8, w="t", head=15)
    s.arrow(330, 262, 580, 302, "path", dash=True, w="h")
    s.label(452, 360, "weeks pass", "path", rot=9)
    s.note(1000, 110, "decided here,|by accident", (1004, 330), "point")


SKETCHES = [
    {"name": "decisions-roll-downhill",
     "idea": "a decision nobody makes in P0 still gets made, later, by accident, by whoever wires the first tool",
     "verb": "roll downhill", "prop": "gutter from a meeting table",
     "alt": "A gutter runs down from a meeting table on a ledge, over a worker's head, to an open box on the floor. "
            "The worker bends over the box with a screwdriver in the works, back to the slope, as a marble drops in.",
     "caption": "A decision nobody makes in P0 gets made later, in code, by whoever wires the first tool.",
     "h": 620, "draw": downhill},
]
