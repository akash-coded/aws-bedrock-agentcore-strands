"""Sketches for the lesson on DevOps and platform teams."""
from pages.sketch import Sk


def tap(s: Sk):
    # a garden tap left running into a bed with nothing in it; the meter on the hose has been turning all along,
    # and the worker has only now got a hand to the tap
    s.ground(530, 50, 1150, tufts=2)
    s.rect(80, 468, 380, 62, fill="p")                       # the raised bed, bare
    s.curve([(88, 466), (150, 452), (230, 462), (310, 450), (390, 462), (452, 456)], "ink", "t")
    s.line(680, 530, 680, 290, w="h")                        # the standpipe
    s.stroke([(680, 312), (610, 312), (610, 346)], "ink", "h")
    s.line(652, 284, 720, 284, w="h")                        # its handle
    s.curve([(610, 346), (606, 430), (570, 486)], "ink")     # the hose, down to the meter
    s.curve([(520, 470), (480, 446), (440, 436)], "ink")     # and on to the bed
    s.oval(548, 484, 42, 42, fill="p")                       # the meter, on the hose
    s.stroke([(548, 484), (572, 460)], "point", "h", amp=0.4)
    for dx, dy in ((0, 0), (-24, 16), (-8, -22)):
        s.drop(420 + dx, 436 + dy, 0.8)
    s.worker(900, 328, look=(-1, 0.3), arms=[(724, 284), None], lean=-5)
    s.label(222, 404, "nothing planted", "ink")
    s.note(440, 130, "meter already running", (544, 432), "point")
    s.note(930, 110, "on since week two", (700, 268), "aside")


def ledger(s: Sk):
    # four doors used to lead to the model; now every call comes past one desk, and the worker writes each one down
    s.ground(540, 50, 1150, tufts=2)
    for i in range(4):
        s.rect(70, 150 + i * 92, 96, 62, fill="p")
    s.route([(176, 180), (300, 230), (410, 330), (470, 372)], "path")
    s.curve([(176, 272), (330, 300), (460, 366)], "path", "h", True, True)
    s.curve([(176, 364), (320, 372), (456, 380)], "path", "h", True, True)
    s.curve([(176, 456), (330, 440), (456, 394)], "path", "h", True, True)
    s.table(480, 410, w=250, h=130)
    s.poly([(600, 404), (492, 396), (506, 340), (604, 352)], fill="p")      # the ledger, open
    s.poly([(600, 404), (712, 396), (700, 340), (604, 352)], fill="p")
    s.scribble(516, 352, 74, 40, 3)
    s.scribble(616, 352, 70, 22, 2)
    s.worker(850, 339, look=(-1, 0.5), arms=[(668, 384), None], lean=-6)
    s.stroke([(668, 384), (690, 350)], "ink", "h")           # the pen
    s.bot(1070, 440, 1.25, look=(-1, 0))
    s.label(120, 110, "four codebases", "ink", anchor="start")
    s.note(560, 190, "every call, written down", (600, 336), "point")
    s.label(1070, 330, "the model", "aside")
    s.label(330, 500, "one way in", "path")


def stopwatch(s: Sk, x: float, y: float, r: float = 40):
    s.rect(x - 8, y - r - 15, 16, 14, fill="p")
    s.clock(x, y, r, hour=2)


def levers(s: Sk):
    # four switches in a row, each with the time it took to throw; the worker throws the first with a stopwatch up
    s.ground(480, 50, 1150, tufts=2)
    times = ("40|seconds", "2|minutes", "3|minutes", "11|minutes")
    knobs = []
    for i, t in enumerate(times):
        x = 470 + i * 190
        knobs.append(s.lever(x, 480, on=False))
        s.label(x, 246, t, "point" if i == 3 else "ink")
    s.worker(210, 279, look=(1, 0.2), arms=[(96, 240), knobs[0]])
    stopwatch(s, 92, 198)
    s.label(760, 96, "timed before anyone needs them", "aside")


SKETCHES = [
    {"name": "a-tap-left-on-over-bare-soil",
     "idea": "some of what this workload needs bills for existing, so the cost starts before the feature does",
     "verb": "shut off", "prop": "garden tap running onto a bare bed",
     "alt": "A garden tap runs through a hose onto a raised bed with nothing planted in it. A meter on the hose is "
            "turning. A worker has just got a hand to the tap.",
     "caption": "Some services bill for existing, not for use. The meter starts before a single line of the feature is written.",
     "draw": tap},
    {"name": "every-call-past-one-desk",
     "idea": "a model call scattered over four codebases leaves no record; one gateway writes every call down",
     "verb": "write down", "prop": "ledger on one desk",
     "alt": "Dashed paths from four small boxes meet at one desk. A worker at the desk writes in an open ledger. "
            "Beyond the desk stands a small machine with one eye.",
     "caption": "One gateway with a log for every call. Without the log, the only evidence of a quality drop is the complaint.",
     "draw": ledger},
    {"name": "four-switches-and-a-stopwatch",
     "idea": "a rollback is only real once it has been thrown and timed, and the four times are far apart",
     "verb": "time", "prop": "row of four switches",
     "alt": "Four switches stand in a row, each with a time written above it: 40 seconds, 2 minutes, 3 minutes, 11 minutes. "
            "A worker throws the first one while holding up a stopwatch.",
     "caption": "SkyWays threw every switch with a stopwatch before cut-over. The slowest took 11 minutes, and they knew it in advance.",
     "h": 540, "draw": levers},
]
