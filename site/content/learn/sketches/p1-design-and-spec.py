"""Sketches for the P1 Design & Spec lesson."""
from pages.sketch import Sk


def stones(s: Sk):
    # seven stepping stones across a stream: three flat slabs, two that wobble, two at the far end in red.
    # the worker stands on the last slab and prods the first wobbly one with a stick before stepping on it
    s.cliff(40, 430, 110, side="left", depth=130)
    s.cliff(1050, 430, 110, side="right", depth=130)
    for x in (220, 340, 460):                                                  # exact: the same every time
        s.rect(x - 48, 432, 96, 40, "ink", fill="p")
        s.hatch(x - 44, 436, 88, 32, gap=22)
    s.worker(400, 262, 1.6, look=(1, 0.7), arms=[None, (508, 300)])
    s.stroke([(498, 284), (588, 424)], "ink", "h")                             # the stick
    for x, tilt in ((600, -9), (720, 7)):                                      # best guess: they tip
        s.rect(x - 46, 432, 92, 36, "aside", fill="p", tilt=tilt)
    for x in (548, 652):
        s.curve([(x - 6, 418), (x, 408), (x - 4, 398)], "aside", "t")
    for x in (850, 970):                                                       # consequential: no way back
        s.rect(x - 48, 432, 96, 40, "point", fill="p", sw="h")
    for x0 in (170, 520, 780, 900):                                            # the water
        s.curve([(x0, 520), (x0 + 24, 512), (x0 + 48, 520), (x0 + 72, 512)], "faint", "t")
    s.label(340, 570, "3 exact: code", "ink")
    s.note(690, 190, "2 best guess:|the model", (662, 414), "aside")
    s.note(990, 190, "2 change|something real", (912, 418), "point")


def ledge(s: Sk):
    # the big sack sits on top of a tall rock; the machine at the foot can reach the small one and no more,
    # and the worker stands apart with the only ladder
    s.ground(540, 50, 1150, tufts=2)
    s.ladder(352, 540, h=330, w=70, rungs=5, lean=22)
    s.worker(220, 339, look=(1, 0.1), arms=[None, (368, 372)])
    s.sack(955, 250, 150, 150)                                                 # the larger amount, up top
    s.label(955, 204, "$2,000", "ink", size=54, rot=0)
    s.poly([(826, 540), (838, 304), (872, 254), (1042, 248), (1078, 312), (1092, 540)], "ink", fill="p")
    s.stroke([(872, 254), (896, 330), (880, 400)], "ink", "t")
    s.bot(712, 453, 1.5, look=(0.7, -1))
    s.sack(560, 540, 124, 124)                                                 # what it can reach
    s.label(560, 508, "$400", "ink", size=54, rot=0)
    s.label(690, 150, "out of reach", "point")
    s.arrow(700, 172, 760, 300, "point", bend=14, w="t", head=15)
    s.note(250, 100, "a person|keeps the ladder", (384, 204), "aside")


SKETCHES = [
    {"name": "seven-stones-three-kinds",
     "idea": "a feature's steps are three different kinds, and only some of them are the model's to guess",
     "verb": "prod", "prop": "seven stepping stones across a stream",
     "alt": "Seven stepping stones cross a stream: three flat slabs, two tilting stones drawn in blue and two drawn in "
            "red at the far side. A worker stands on the last slab and prods the first tilting stone with a stick.",
     "caption": "Seven steps, three kinds. Only two were the model's to guess. Three went to tested code, and the two that "
                "change something real need a gate.",
     "draw": stones},
    {"name": "the-ladder-stays-with-a-person",
     "idea": "a cap in the tool puts the larger amount out of the model's reach; only a person can go higher",
     "verb": "keep hold of", "prop": "ladder beside a tall rock",
     "alt": "A sack marked $2,000 sits on top of a tall rock. A small machine at the foot of the rock looks up at it; "
            "a sack marked $400 is on the ground within its reach. A worker stands apart, holding the only ladder.",
     "caption": "A cap in the tool puts the larger refund out of reach, whatever the model is told. Going higher takes a "
                "person with the ladder.",
     "draw": ledge},
]
