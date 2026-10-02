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


def blanket(s: Sk):
    # a dust sheet over three lumps; the worker lifts one corner, and one of the lumps is spiky
    s.ground(540, 50, 1150, tufts=3)
    s.stroke([(820, 540), (850, 430), (880, 500), (910, 400), (945, 500), (975, 440), (1000, 540)], "point", "h")
    s.sheet(330, 540, [(60, 150), (270, 190), (470, 120)])
    s.worker(200, 339, look=(1, 0.6), arms=[None, (300, 500)])
    s.stroke([(300, 500), (330, 470), (372, 480)], "ink")   # the corner, lifted
    s.label(600, 300, "91% overall", "ink")
    s.note(1000, 250, "refunds", (912, 388), "point")
    s.label(600, 110, "a bar for each", "path")


SKETCHES = [
    {"name": "four-pebbles-one-rock",
     "idea": "the bar is where right answers just pay for wrong ones",
     "verb": "balance", "prop": "plank over a log",
     "alt": "A plank balances on a log. A rock sits on one end. A worker lowers a fourth pebble onto the other end, and the "
            "plank comes level.",
     "caption": "The bar for partner flights is 80% because one wrong answer weighs as much as four right ones.",
     "draw": pebbles},
    {"name": "something-soft-underneath",
     "idea": "a hold does not make the agent better; it makes a mistake cheaper, so the bar drops",
     "verb": "catch", "prop": "mattress under a stack of plates",
     "alt": "A small machine walks along carrying a tall stack of plates, and one plate is sliding off. A worker has shoved a "
            "mattress under where it will land and holds the corner.",
     "caption": "A person checking refunds cuts the damage from $600 to $30, so the bar falls from 98% to 71%. The model is the same.",
     "draw": mattress},
    {"name": "lift-the-blanket",
     "idea": "one accuracy number covers kinds of case that fail very differently",
     "verb": "lift", "prop": "dust sheet over three lumps",
     "alt": "A dust sheet covers three lumps and carries one number, 91% overall. A worker lifts a corner. Beside it, "
            "uncovered, one lump is spiky and drawn in red.",
     "caption": "One accuracy number for the whole feature hides the refunds.",
     "draw": blanket},
]
