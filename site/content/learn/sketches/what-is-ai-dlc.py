"""Sketches for the lesson on AWS's AI-DLC."""
from pages.sketch import Sk


def trays(s: Sk):
    # the machine keeps a pile of drafts coming along the bench; the worker holds the next one over two
    # trays, one ticked and one crossed, and chooses
    s.ground(540, 50, 1150, tufts=2)
    s.bot(180, 447, 1.6, look=(1, -0.2))
    s.table(340, 400, w=520, h=140)
    for i in range(5):                                         # the pile it has drafted
        s.rect(372 + (i % 2) * 8, 388 - i * 13, 130, 12, fill="p")
    for x in (580, 724):                                       # two trays, seen from the side
        s.stroke([(x, 346), (x + 8, 400), (x + 122, 400), (x + 130, 346)], "ink")
    s.stroke([(624, 372), (638, 388), (668, 356)], "aside", "h", amp=0.5)
    s.stroke([(772, 358), (806, 390)], "point", "h", amp=0.5)
    s.stroke([(806, 358), (772, 390)], "point", "h", amp=0.5)
    s.doc(672, 188, 96, 122, tilt=10, lines=3)                 # the one being decided
    s.worker(1010, 339, look=(-1, 0.1), arms=[(778, 296), None])
    s.route([(516, 368), (570, 286), (656, 252)], "path")
    s.label(185, 262, "AI proposes", "aside")
    s.note(430, 120, "plans, questions,|code", (436, 318), "ink")
    s.note(890, 150, "people decide", (790, 214), "point")


def parcel(s: Sk, x: float, y: float, w: float = 120, h: float = 90):
    """A parcel tied with string, its top left at ``x, y``."""
    s.rect(x, y, w, h, fill="p")
    s.line(x + w * 0.5, y, x + w * 0.5, y + h, w="t")
    for k in (-1, 1):
        s.curve([(x + w * 0.5, y), (x + w * 0.5 + k * 22, y - 20), (x + w * 0.5 + k * 30, y - 4), (x + w * 0.5, y)], "ink", "t")


def clock(s: Sk):
    # the machine sits beside a parcel it finished long ago; the worker lifts the fortnight's calendar
    # off its post and brings a clock to hang there
    s.ground(540, 50, 1150, tufts=2)
    s.bot(160, 453, 1.5, look=(1, -0.6))
    parcel(s, 262, 440, 130, 100)
    s.line(625, 352, 625, 540, w="h")
    s.calendar(550, 200, 150, 152)
    s.worker(880, 339, look=(-1, -0.2), arms=[(704, 300), (1030, 306)])
    s.clock(1040, 244, 60, hour=2)
    s.note(300, 170, "built in|an afternoon", (328, 412), "aside")
    s.label(625, 96, "sprint:|two weeks", "point")
    s.label(1000, 88, "a bolt: hours|or days", "path")


SKETCHES = [
    {"name": "the-machine-drafts-a-person-decides",
     "idea": "AI-DLC inverts who starts: the AI drafts the plans, questions and code, and people keep the decision",
     "verb": "sort", "prop": "yes tray and no tray at the end of a bench",
     "alt": "A small machine stands at one end of a bench with a pile of drafts. At the other end a worker holds one "
            "sheet over two trays, one marked with a tick and one with a cross.",
     "caption": "In AI-DLC the AI starts the work: plans, questions, code. People validate what it proposes and "
                "make the decisions.",
     "draw": trays},
    {"name": "a-clock-where-the-calendar-hung",
     "idea": "an agent builds in an afternoon and then waits out a two-week sprint; a bolt plans at the speed it builds",
     "verb": "swap", "prop": "wall calendar for a clock",
     "alt": "A small machine sits idle beside a finished parcel. A worker lifts a calendar off its post with one hand "
            "and holds a clock ready in the other.",
     "caption": "An agent that builds a story in an afternoon sits idle for most of a two-week sprint. A bolt plans "
                "in hours or days.",
     "draw": clock},
]
