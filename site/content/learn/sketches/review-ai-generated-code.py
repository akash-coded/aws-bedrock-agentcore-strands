"""Sketches for the lesson on reviewing by risk."""
from pages.sketch import Sk


def mushroom(s: Sk, x: float, y: float, r: float = 26):
    s.line(x - 7, y, x - 9, y + 30, "point")
    s.line(x + 7, y, x + 9, y + 30, "point")
    s.stroke([(x - r, y), (x - r * 0.6, y - r * 0.8), (x, y - r * 1.1), (x + r * 0.6, y - r * 0.8), (x + r, y), (x - r, y)],
             "point", raw=True)


def tagged(s: Sk):
    # a scaffold with one foot on a pile of bricks, and the worker who built it tying a "low risk" tag to it
    s.ground(540, 50, 1150, tufts=2)
    s.rect(716, 508, 62, 32, fill="p")                          # the bricks under one foot
    s.line(520, 540, 556, 130, w="h")                           # two uprights, not quite upright
    s.line(746, 508, 776, 130, w="h")
    for y0 in (176, 340):                                       # two platforms
        s.rect(530 - (y0 - 340) * 0.09, y0, 250, 16, fill="p", tilt=-2)
    s.line(540, 334, 766, 196, w="t")
    s.line(554, 196, 758, 334, w="t")
    s.line(526, 500, 756, 360, w="t")
    for x0, y0 in ((800, 130), (806, 300)):                     # it sways
        s.curve([(x0, y0), (x0 + 14, y0 + 18), (x0, y0 + 38)], "point", "t")
    s.worker(220, 339, look=(1, 0.2), arms=[None, (452, 392)])
    s.curve([(452, 392), (494, 380), (532, 388)], "ink", "t")   # the string
    s.rect(360, 406, 200, 84, fill="p", tilt=-5)
    s.oval(380, 448, 6, 6, w="t")
    s.label(468, 466, "low risk", "ink", size=54, rot=-5)
    s.note(340, 110, "says its author", (452, 396), "point")
    s.sign(990, 540, "money:|two readers", "ink", post=150, size=54)
    s.label(990, 196, "the path decides", "aside", size=54)


SKETCHES = [
    {"name": "tagging-your-own-scaffold",
     "idea": "self-assessed risk is not a control: the path a change touches sets its band, not its author",
     "verb": "tie a low-risk tag to", "prop": "a scaffold with one foot on bricks",
     "alt": "A scaffold stands with one foot propped on bricks and sways. The worker who built it ties a tag to it "
            "that reads low risk. A fixed sign beside it reads money: two readers.",
     "caption": "Self-assessed risk is not a control. The paths a change touches decide its band, from a rule file nobody sets for their own work.",
     "draw": tagged},
]
