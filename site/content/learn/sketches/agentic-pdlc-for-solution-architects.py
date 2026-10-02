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
    # one model on the stage, in the light; the rest queue at the steps, and the worker stands at the step
    # with both arms out, barring the way until one of them can say which limit it is there for
    s.ground(540, 50, 620, tufts=2)
    s.rect(612, 482, 68, 58)                                                               # a step, then the stage
    s.line(680, 420, 1150, 420, w="h")
    s.line(680, 420, 680, 540)
    s.hatch(692, 430, 130, 104, gap=24)
    s.rect(1086, 40, 50, 34, fill="p", tilt=-30)                                           # a lamp, and its light
    s.line(1090, 74, 840, 418, pen="faint", w="t")
    s.line(1118, 84, 1010, 418, pen="faint", w="t")
    for x in (110, 242):
        _small_bot(s, x, 482, 1.3)
    s.stroke([(34, 444), (34, 520)], "aside")                                               # and more, off the sheet
    s.bot(930, 333, 1.5, look=(-1, 0.3))
    s.worker(486, 339, look=(-1, 0.3), arms=[(330, 322), (642, 326)], lean=-6)
    s.note(60, 250, "fifteen agents", (160, 428), "aside", anchor="start")
    s.label(440, 140, "why a second one?", "point")
    s.label(812, 204, "start with one", "ink")


SKETCHES = [
    {"name": "one-on-stage-the-rest-wait",
     "idea": "start with one agent; another gets in only by naming the limit it is there for",
     "verb": "bar the steps to", "prop": "stage with a queue at the steps",
     "alt": "One small machine stands on a stage. More of them queue at the steps, and a worker spreads both arms to "
            "bar the way until one can name the limit it is there for.",
     "caption": "SkyWays' fifteen agents collapsed to one agent, a fan-out tool, a function and a checker. A second agent must name the limit it is there for.",
     "draw": audition},
]
