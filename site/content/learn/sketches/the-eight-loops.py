"""Sketches for the lesson on the eight loops."""
from pages.sketch import Sk


def parcel(s: Sk, x: float, y: float, w: float = 120, h: float = 90):
    """A parcel tied with string, its top left at ``x, y``."""
    s.rect(x, y, w, h, fill="p")
    s.line(x + w * 0.5, y, x + w * 0.5, y + h, w="t")
    for k in (-1, 1):                                         # the bow
        s.curve([(x + w * 0.5, y), (x + w * 0.5 + k * 22, y - 20), (x + w * 0.5 + k * 30, y - 4), (x + w * 0.5, y)], "ink", "t")


def collect(s: Sk):
    # a post office shelf where three parcels were never collected; the desk they are owed to is empty,
    # so a person lifts one down and walks it back
    s.ground(500, 50, 1150, tufts=3)
    s.table(90, 360, w=220, h=140)
    s.rect(150, 345, 100, 14, fill="p")                       # the design, lying on the desk
    s.shelf(830, 300, w=310)
    parcel(s, 850, 212, 120, 88)
    parcel(s, 1000, 212, 120, 88)
    s.worker(600, 299, look=(-1, 0.1), arms=[(470, 350), (420, 350)], legs="walk", lean=-5)
    parcel(s, 372, 252, 132, 96)
    s.note(230, 120, "nobody waiting", (200, 336), "point")
    s.note(960, 80, "cost, incident,|governance", (985, 204), "ink")
    s.label(610, 140, "a named person", "aside")
    s.route([(720, 548), (500, 540), (300, 548)], "path")


def readdress(s: Sk):
    # the bill arrives in an envelope addressed to finance; the worker strikes that out and writes
    # design, and the route runs back to the decision record on its post
    s.ground(540, 50, 1150, tufts=2)
    s.line(160, 440, 160, 540, w="h")
    s.doc(100, 292, 120, 150, lines=4)
    s.table(400, 420, w=470, h=120)
    s.rect(430, 190, 400, 230, fill="p", tilt=-2)             # the envelope, standing on the desk
    s.rect(752, 204, 52, 62, sw="t", tilt=-2)                 # its stamp
    s.label(600, 300, "to: finance", "ink", rot=-2)
    s.stroke([(478, 288), (724, 278)], "point", "h", note=True)
    s.label(600, 380, "to: design", "point", rot=-2)
    s.worker(1010, 339, look=(-1, 0.2), arms=[(796, 368), None])
    s.stroke([(796, 368), (742, 382)], "ink", "h")            # the pen
    s.route([(420, 326), (330, 312), (236, 346)], "path")
    s.note(930, 84, "bill: 4.4 times|the estimate", (812, 192), "ink")
    s.label(215, 180, "decision record:|second version", "aside")


SKETCHES = [
    {"name": "nobody-comes-to-collect",
     "idea": "five loops close because someone downstream is waiting; three have nobody waiting, so a named person "
             "has to carry them back",
     "verb": "carry back", "prop": "uncollected parcels on a post office shelf",
     "alt": "Two parcels sit uncollected on a shelf. A worker has lifted a third down and walks it back to a desk "
            "where nobody is waiting.",
     "caption": "Five loops close because someone downstream is waiting. Cost, incident and governance close only "
                "when a named person carries them back.",
     "h": 590, "draw": collect},
    {"name": "the-bill-readdressed-to-design",
     "idea": "a bill over its estimate is a design question, not a finance question; it closes in a decision record",
     "verb": "re-address", "prop": "envelope with the bill in it",
     "alt": "A large envelope stands on a desk. The address to finance is struck out in red and a worker writes "
            "to design beneath it. A dashed route runs from the envelope back to a document on a post.",
     "caption": "A bill that left its estimate goes to design, not to finance. The cost loop closes when a decision "
                "record has a new version.",
     "draw": readdress},
]
