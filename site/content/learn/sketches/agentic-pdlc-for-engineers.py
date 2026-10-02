"""Sketches for the lesson for engineers."""
from pages.sketch import Sk


def rope(s: Sk):
    # backstage: a sandbag hangs from a pulley, over the money. The model was asked to keep hold of the
    # rope; the worker is tying the rope off on a cleat, so nobody has to remember to hold it.
    s.line(790, 40, 970, 40, w="h")                                        # a beam, and the pulley under it
    s.line(880, 40, 880, 64)
    s.line(902, 92, 902, 232)                                              # down to the sandbag
    s.blob(902, 322, 74, 86, lumps=3, depth=0.05)
    s.stroke([(876, 250), (902, 228), (928, 250)], "ink")
    s.line(878, 254, 926, 254, w="h")
    s.line(860, 96, 572, 484)                                              # and down to the cleat
    s.oval(880, 86, 23, 23, fill="p")
    s.curve([(540, 492), (440, 516), (310, 512), (250, 482), (226, 440)], "ink")           # the slack tail
    s.ground(520, 50, 1150, tufts=2)
    s.stack(902, 512, 3, 110)
    s.bot(140, 427, 1.6, look=(1, -0.4))
    s.oval(226, 438, 8, 8, "aside", fill="p")
    s.worker(400, 319, look=(1, 0.8), arms=[None, (540, 474)], lean=10)
    s.rect(520, 498, 96, 22, fill="p")                                     # the cleat
    s.line(500, 484, 636, 484, w="h")
    s.line(568, 484, 568, 498, w="h")
    s.stroke([(544, 476), (592, 492), (548, 492), (590, 476)], "ink", amp=0.5)             # the turns round it
    s.note(250, 100, "the prompt says:|hold on", (236, 426), "point")
    s.label(568, 596, "tied off in code", "ink", size=56)
    s.label(950, 596, "money, bookings", "ink", size=56)


def _dummy(s: Sk, x: float, y: float, foot: float):
    # a jacket on a tailor's dummy: x is its middle, y its shoulders, foot the floor
    s.line(x, y + 230, x, foot - 18, w="h")
    s.stroke([(x - 56, foot), (x, foot - 20), (x + 56, foot)], "ink", "h")
    s.oval(x, y - 20, 22, 15, fill="p")
    s.poly([(x - 74, y + 12), (x - 26, y), (x + 26, y), (x + 74, y + 12), (x + 90, y + 70), (x + 70, y + 226),
            (x - 78, y + 250), (x - 90, y + 70)], fill="p")
    s.stroke([(x - 26, y), (x - 2, y + 96), (x + 26, y)], "ink", "t")
    s.line(x - 2, y + 96, x - 6, y + 240, w="t")
    for i in range(3):
        s.oval(x + 12, y + 120 + i * 38, 6, 6, w="t")


def backwards(s: Sk):
    # a jacket already sewn, on the dummy. The worker holds a tape to it and writes what it reads on the
    # order form: the measurements are coming from the garment, not from the customer.
    s.ground(580, 60, 1140, tufts=2)
    _dummy(s, 770, 220, 580)
    s.doc(150, 300, 134, 172, lines=5)
    s.worker(470, 379, look=(-1, 0.2), arms=[(288, 392), (682, 240)])
    s.stroke([(288, 392), (262, 420)], "ink", "h")                         # the pencil
    s.line(682, 236, 676, 462, w="h")                                      # the tape, down the jacket's edge
    for i in range(1, 7):
        s.stroke([(679 - i * 0.8, 236 + i * 32), (692 - i * 0.8, 236 + i * 32)], "ink", "t", amp=0.3)
    s.route([(690, 196), (480, 142), (280, 190), (222, 284)], "path")
    s.label(480, 108, "written around it", "path")
    s.note(980, 130, "built in P0", (850, 226), "point")
    s.label(54, 542, "requirements", "ink", anchor="start")


SKETCHES = [
    {"name": "tie-off-the-rope",
     "idea": "a rule in a prompt is a request to keep holding; a cap in a signature is the rope tied off",
     "verb": "tie off", "prop": "sandbag rope on a cleat",
     "alt": "A sandbag hangs from a pulley. Its rope runs down to a cleat on the floor, where a worker is tying it "
            "off. The loose end trails away to a small machine that was asked to hold it and is looking elsewhere.",
     "caption": "A rule in a prompt asks the model to keep holding the rope. A cap in a tool's signature ties it off.",
     "h": 630, "draw": rope},
    {"name": "order-written-from-the-jacket",
     "idea": "build in P0 and the requirements get written around the prototype",
     "verb": "copy measurements from", "prop": "finished jacket on a tailor's dummy",
     "alt": "A finished, lopsided jacket hangs on a tailor's dummy. A worker holds a tape measure against it with one "
            "hand and writes on the order form with the other. A dashed arrow runs from the jacket to the form.",
     "caption": "Start building in P0 and the requirements get written around your prototype, like an order form copied from a jacket already sewn.",
     "h": 660, "draw": backwards},
]
