"""Sketches for the lesson for executives."""
from pages.sketch import Sk


def scarecrow(s: Sk, x: float, y: float):
    """Two sticks, a sack for a head, a hat and a ragged shirt, planted at ``x, y``."""
    s.line(x, y, x, y - 300, w="h")
    s.line(x - 112, y - 214, x + 112, y - 214, w="h")
    s.stroke([(x - 100, y - 214), (x - 88, y - 150), (x - 56, y - 176), (x - 44, y - 112), (x - 14, y - 136),
              (x + 6, y - 104), (x + 30, y - 138), (x + 54, y - 116), (x + 62, y - 180), (x + 90, y - 154),
              (x + 100, y - 214)], "ink", amp=0.8)
    s.oval(x, y - 262, 36, 36, fill="p")
    s.stroke([(x - 56, y - 292), (x + 56, y - 292)], "ink", "h")
    s.poly([(x - 30, y - 292), (x - 20, y - 338), (x + 22, y - 338), (x + 30, y - 292)], fill="p")
    for dx in (-13, 13):
        s.oval(x + dx, y - 266, 3, 3, fill="ink")


def crow(s: Sk, x: float, y: float, k: float = 1.0):
    s.curve([(x - 34 * k, y - 6 * k), (x - 14 * k, y - 20 * k), (x, y)], "ink")
    s.curve([(x, y), (x + 16 * k, y - 22 * k), (x + 36 * k, y - 8 * k)], "ink")


def rule(s: Sk):
    # a field: the model stands in it waving at the crows because agents were asked for; the worker is planting
    # the thing that does this job without being told twice
    s.ground(540, 50, 1150, tufts=3)
    s.worker(250, 339, look=(1, -0.1), arms=[None, (470, 400)], lean=4)
    scarecrow(s, 480, 540)
    s.bot(930, 446, 1.6, look=(0.4, -0.8))
    for k in (-1, 1):                                        # its arms, up and flapping
        s.stroke([(930 + k * 74, 440), (930 + k * 120, 380), (930 + k * 108, 322)], "aside")
        s.burst(930 + k * 108, 310, 8, 3, "aside", -130 if k < 0 else -90, -90 if k < 0 else -50)
    crow(s, 760, 150)
    crow(s, 1100, 120, 0.8)
    s.note(600, 110, "a rule does this better", (520, 196), "point")
    s.label(940, 250, "an agent, as asked", "aside")


def pumpkin(s: Sk, x: float, y: float, r: float = 60, pen: str = "ink"):
    """A pumpkin centred at ``x, y``."""
    s.oval(x, y, r, r * 0.78, pen, fill="p")
    for k in (-1, 1):
        s.curve([(x + k * r * 0.3, y - r * 0.7), (x + k * r * 0.46, y), (x + k * r * 0.3, y + r * 0.7)], pen, "t")
    s.stroke([(x, y - r * 0.78), (x + 7, y - r * 0.78 - 18)], pen, "h", amp=0.4)


def barrow(s: Sk, x: float, y: float):
    """A wheelbarrow facing right, its wheel standing at ``x, y``."""
    s.poly([(x - 230, y - 140), (x + 10, y - 140), (x - 30, y - 62), (x - 190, y - 62)], fill="p")
    s.stroke([(x - 222, y - 126), (x - 330, y - 150)], "ink", "h")
    s.stroke([(x - 180, y - 62), (x - 186, y)], "ink")
    s.stroke([(x - 40, y - 62), (x, y - 28)], "ink")
    s.oval(x, y - 28, 28, 28, fill="p", w="h")


def prize(s: Sk):
    # a show table with the one pumpkin the grower chose; the worker pins a rosette on it with its back to the barrow
    s.ground(540, 50, 1150, tufts=2)
    s.table(120, 410, w=300, h=130)
    pumpkin(s, 270, 346, 82)
    s.worker(610, 339, look=(-1, 0.2), arms=[(366, 330), None], lean=-5)
    s.oval(350, 330, 24, 24, "aside", fill="p")              # the rosette
    s.oval(350, 330, 9, 9, "aside")
    s.stroke([(340, 352), (330, 398)], "aside")
    s.stroke([(360, 352), (368, 398)], "aside")
    for px, py, r in ((860, 372, 34), (930, 356, 46), (1010, 374, 36), (890, 322, 28), (968, 310, 30)):
        pumpkin(s, px, py, r)
    s.stroke([(916, 340), (944, 372)], "point", "h", amp=0.4)     # one of them is bad
    s.stroke([(944, 340), (916, 372)], "point", "h", amp=0.4)
    barrow(s, 1080, 540)
    s.note(250, 130, "the demo: one, chosen", (262, 250), "aside")
    s.note(900, 150, "the rest, never weighed", (936, 270), "point")


SKETCHES = [
    {"name": "a-scarecrow-would-do",
     "idea": "ask for agents and you get agents, even for work a rule does better",
     "verb": "plant", "prop": "scarecrow in a field",
     "alt": "In a field a small machine with one eye waves its arms at two crows. Beside it a worker is planting a "
            "scarecrow, which would do the same job.",
     "caption": "Ask for agents and you get agents, even where a rule does the job better. Expect two or three of your top five to be rules.",
     "draw": rule},
    {"name": "a-rosette-on-the-chosen-pumpkin",
     "idea": "accept a demo as evidence and the cases nobody chose are never looked at",
     "verb": "pin a rosette on", "prop": "show pumpkin beside a full barrow",
     "alt": "One large pumpkin sits on a show table and a worker pins a rosette to it. Behind the worker stands a "
            "wheelbarrow heaped with other pumpkins, one of them marked with a red cross.",
     "caption": "Accept a demo and you will be shown demos. Ask instead for a score for each kind of case, against its pass mark.",
     "draw": prize},
]
