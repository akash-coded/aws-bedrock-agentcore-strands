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


SKETCHES = [
    {"name": "a-scarecrow-would-do",
     "idea": "ask for agents and you get agents, even for work a rule does better",
     "verb": "plant", "prop": "scarecrow in a field",
     "alt": "In a field a small machine with one eye waves its arms at two crows. Beside it a worker is planting a "
            "scarecrow, which would do the same job.",
     "caption": "Ask for agents and you get agents, even where a rule does the job better. Expect two or three of your top five to be rules.",
     "draw": rule},
]
