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
    # one long counter: the calls queue along it as letters, and every one passes the open ledger, where the
    # worker writes it down before it goes on to the model
    s.ground(540, 50, 1150, tufts=2)
    s.table(70, 410, w=570, h=130)
    for x, y, tilt in ((90, 338, -5), (214, 342, 4), (336, 336, -3)):      # the calls, waiting their turn
        s.envelope(x, y, 104, 68, tilt=tilt)
    s.poly([(560, 404), (452, 396), (466, 336), (564, 350)], fill="p")      # the ledger, open
    s.poly([(560, 404), (672, 396), (660, 336), (564, 350)], fill="p")
    s.scribble(476, 350, 74, 42, 3)
    s.scribble(576, 350, 70, 24, 2)
    s.worker(780, 339, look=(-1, 0.6), arms=[(668, 352), (628, 384)], lean=-11)
    s.stroke([(628, 384), (606, 352)], "ink", "h")           # the pen
    s.bot(1040, 453, 1.5, look=(-1, 0))
    s.arrow(100, 300, 410, 300, "path", dash=True, w="h")
    s.arrow(892, 456, 950, 456, "path", dash=True, w="h")
    s.label(250, 270, "one way in", "path")
    s.note(560, 150, "every call, written down", (570, 330), "point")
    s.label(1040, 318, "the model", "aside")


def stopwatch(s: Sk, x: float, y: float, r: float = 40):
    s.rect(x - 8, y - r - 15, 16, 14, fill="p")
    s.clock(x, y, r, hour=2)


def levers(s: Sk):
    # four switches in a row, each with the time it took to throw; the worker throws the first with a stopwatch up
    s.ground(480, 50, 1150, tufts=2)
    times = ("40|seconds", "", "", "11|minutes")              # the fastest and the slowest of the four
    knobs = []
    for i, t in enumerate(times):
        x = 470 + i * 190
        knobs.append(s.lever(x, 480, on=False))
        if t:
            s.label(x, 246, t, "point" if i == 3 else "ink")
    s.worker(210, 279, look=(1, 0.2), arms=[(96, 240), knobs[0]], lean=6)
    stopwatch(s, 92, 198)
    s.label(760, 110, "timed in advance", "aside")


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
     "alt": "Letters queue along one counter. At its end a worker bends over an open ledger and writes each one "
            "down. Beyond the counter stands a small machine with one eye.",
     "caption": "One gateway with a log for every call. Without the log, the only evidence of a quality drop is the complaint.",
     "draw": ledger},
    {"name": "four-switches-and-a-stopwatch",
     "idea": "a rollback is only real once it has been thrown and timed, and the four times are far apart",
     "verb": "time", "prop": "row of four switches",
     "alt": "Four switches stand in a row. The first has 40 seconds written above it and the last has 11 minutes. "
            "A worker throws the first one while holding up a stopwatch.",
     "caption": "SkyWays threw every switch with a stopwatch before cut-over. The slowest took 11 minutes, and they knew it in advance.",
     "h": 540, "draw": levers},
]
