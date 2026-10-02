"""Sketches for the lesson for solution architects."""
from pages.sketch import Sk


def _small_bot(s: Sk, x: float, y: float, k: float = 1.2):
    # a model in the queue: fewer strokes than the engine's bot, same blue box with one eye
    w, h = 70 * k, 60 * k
    s.rect(x - w / 2, y - h / 2, w, h, "aside", fill="p")
    s.oval(x + 6 * k, y - 4 * k, 11 * k, 11 * k, "aside")
    s.oval(x + 10 * k, y - 4 * k, 4 * k, 4 * k, "aside", fill="aside")
    for dx in (-18, 18):
        s.stroke([(x + dx * k, y + h / 2), (x + dx * k, y + h / 2 + 16 * k)], "aside")


def audition(s: Sk):
    # one model on the stage, in the light; the rest queue at the steps, and the worker bars the way
    # until one of them can say which limit it is there for
    s.ground(540, 50, 660, tufts=2)
    s.rect(612, 482, 68, 58)                                                               # a step, then the stage
    s.line(680, 420, 1150, 420, w="h")
    s.line(680, 420, 680, 540)
    s.rect(1086, 40, 50, 34, fill="p", tilt=-30)                                           # a lamp, and its light
    s.line(1090, 74, 820, 418, pen="faint", w="t")
    s.line(1118, 84, 990, 418, pen="faint", w="t")
    for x in (100, 232):
        _small_bot(s, x, 482, 1.3)
    s.stroke([(24, 444), (24, 520)], "aside")                                               # and more, off the sheet
    s.bot(900, 333, 1.5, look=(-1, 0.3))
    s.worker(500, 339, look=(-1, 0.3), arms=[(340, 340), None])
    s.note(60, 250, "fifteen agents", (150, 428), "aside", anchor="start")
    s.label(520, 130, "name your limit", "point")
    s.label(850, 176, "start with one", "ink")


def prompter(s: Sk):
    # the prompt box at the front of a stage: the worker is in it up to the waist with the script open,
    # and the model on the stage has turned to ask
    s.stroke([(172, 440), (180, 310), (240, 214), (340, 180), (440, 180)], "ink", "h")      # the hood of the box
    s.worker(330, 370, look=(1, -0.2), arms=[None, (478, 386)], legs="none")
    s.rect(50, 440, 1100, 100, fill="p")                                                   # the front of the stage
    s.line(50, 440, 1150, 440, w="h")
    s.doc(468, 282, 98, 122, tilt=9, lines=4)
    s.bot(1000, 347, 1.6, look=(-1, 0.2))
    s.label(1112, 262, "?", "aside", size=96, rot=8)
    s.arrow(596, 344, 902, 352, "path", dash=True, w="h")
    s.label(748, 312, "answer from it", "path")
    s.note(430, 100, "the signed design", (510, 272), "ink")
    s.label(930, 120, "no quiet rewrites", "point")


SKETCHES = [
    {"name": "one-on-stage-the-rest-wait",
     "idea": "start with one agent; another gets in only by naming the limit it is there for",
     "verb": "bar the steps to", "prop": "stage with a queue at the steps",
     "alt": "One small machine stands on a stage. More of them queue at the steps, and a worker holds out an arm to "
            "stop them until one can name the limit it is there for.",
     "caption": "SkyWays' fifteen agents collapsed to one agent, a fan-out tool, a function and a checker. A second agent must name the limit it is there for.",
     "draw": audition},
    {"name": "the-prompter-in-the-box",
     "idea": "in P2 the architect answers from the signed design and does not quietly rewrite it while the build is on",
     "verb": "prompt from", "prop": "prompt box at the front of a stage",
     "alt": "A worker sits waist deep in the prompt box at the front of a stage, holding the script open. A small "
            "machine on the stage has turned to ask a question, and a dashed arrow carries the answer from the script.",
     "caption": "In P2 the architect answers from the signed design, like a prompter with the script. If the design is wrong, re-cut in the open, never quietly.",
     "h": 580, "draw": prompter},
]
