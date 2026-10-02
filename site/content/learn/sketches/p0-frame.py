"""Sketches for the P0 Frame lesson."""
from pages.sketch import Sk


def downhill(s: Sk):
    # a meeting table up on a ledge, a gutter running down from it, and an engineer at the bottom,
    # head down in an open box, who never sees the question arrive
    s.cliff(40, 262, 280, side="left", depth=300)
    s.table(80, 190, w=170, h=72)
    s.marble(150, 162, 26)
    s.ground(560, 300, 1160, tufts=2)
    s.pipe([(318, 250), (540, 340), (770, 420)], r=17)
    s.marble(500, 296, 26)
    s.worker(1010, 359, look=(-1, 0.7), arms=[(900, 470), None], lean=-10)
    s.box(740, 440, 220, 120, open_=True)
    s.marble(812, 412, 26)
    s.stroke([(900, 470), (856, 520)], "ink", "h")               # the screwdriver, already in the works
    s.note(250, 76, "nobody decided", (160, 128), "point")
    s.label(500, 470, "weeks pass", "path", rot=21)
    s.arrow(400, 366, 620, 452, "path", dash=True, w="h")
    s.note(840, 96, "decided here,|by accident", (826, 376), "point")


def wring(s: Sk):
    # a cloud twisted like a wet towel over a measuring jug: what drips out has numbers on it
    s.ground(540, 60, 1140, tufts=3)
    s.worker(360, 339, look=(1, -0.2), arms=[(520, 216), (640, 250)])
    s.cloud(590, 222, 250, 112, "aside")
    s.stroke([(520, 216), (560, 240), (600, 208), (640, 250)], "aside", "t")      # the twist in it
    for dx, dy in ((0, 0), (18, 44), (-10, 86)):
        s.drop(596 + dx, 330 + dy, 1.2)
    s.jug(600, 540, 170, 190, level=0.5, marks=4)
    s.note(610, 80, "make it smarter", (600, 164), "aside")
    s.label(760, 400, "38 minutes", "ink", anchor="start")
    s.label(760, 460, "240 a day", "ink", anchor="start")
    s.label(760, 520, "$9.40 a case", "ink", anchor="start")


SKETCHES = [
    {"name": "decisions-roll-downhill",
     "idea": "a decision nobody makes in P0 still gets made, later, by accident, by whoever wires the first tool",
     "verb": "roll downhill", "prop": "gutter from a meeting table",
     "alt": "A gutter runs down from a meeting table to an open box on the floor. Marbles roll along it. A worker has "
            "their head in the box and a screwdriver in the works, and does not see the next marble arrive.",
     "caption": "A decision nobody makes in P0 gets made later, in code, by whoever wires the first tool.",
     "h": 620, "draw": downhill},
    {"name": "wring-the-vibe",
     "idea": "a vibe cannot be sized; squeeze it until numbers come out",
     "verb": "wring out", "prop": "cloud over a measuring jug",
     "alt": "A worker twists a small cloud like a wet towel. Drops fall from it into a measuring jug. Beside the jug "
            "are three numbers: 38 minutes, 240 a day, $9.40 a case.",
     "caption": "Two days of work turned \"make rebooking smarter\" into one line with numbers in it.",
     "draw": wring},
]
