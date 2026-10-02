"""Sketches for the lesson on how accurate an agent must be."""
from pages.sketch import Sk


def pebbles(s: Sk):
    # a plank over a log: one rock on one end, the worker lowering the fourth pebble onto the other
    s.ground(540, 50, 1150, tufts=3)
    l, r = s.seesaw(640, 540, w=620, tip=0.0)
    s.rock(r[0] - 70, r[1], 150, 120)
    for i in range(3):
        s.pebble(l[0] + 50 + i * 52, l[1], 24)
    s.worker(200, 339, look=(1, 0.3), arms=[None, (l[0] + 206, l[1] - 40)])
    s.pebble(l[0] + 206, l[1] - 24, 24)
    s.note(940, 190, "1 wrong: $36", (r[0] - 70, r[1] - 130), "point")
    s.note(500, 150, "4 right x $9", (l[0] + 110, l[1] - 50), "aside")
    s.label(660, 330, "level at 80%", "ink")


def mattress(s: Sk):
    # the model walks on with a tall stack of plates, one sliding off; a person has shoved a mattress under the fall
    s.ground(540, 50, 1150, tufts=2)
    s.bot(330, 420, 1.6, look=(1, 0))
    s.stack(330, 318, 6, 120)
    s.oval(470, 330, 60, 12, fill="p")                      # the plate that is going
    s.curve([(420, 250), (470, 280), (480, 316)], "faint", "t")
    s.mattress(420, 482, 360, 58)
    s.worker(930, 339, look=(-1, 0.5), arms=[(784, 500), None], lean=-6)
    s.note(260, 110, "same model", (300, 190), "aside")
    s.note(640, 250, "the hold", (600, 470), "point")
    s.label(900, 110, "$600 becomes $30", "ink")
    s.label(900, 170, "bar: 98 to 71", "path")


SKETCHES = [
    {"name": "four-pebbles-one-rock",
     "idea": "the bar is where right answers just pay for wrong ones",
     "verb": "balance", "prop": "plank over a log",
     "alt": "A plank balances on a log. A rock sits on one end. A worker lowers a fourth pebble onto the other end, and the "
            "plank comes level.",
     "caption": "The bar for partner flights is 80% because one wrong answer weighs as much as four right ones.",
     "draw": pebbles},
]
