"""Sketches for the lesson on AWS's AI-DLC."""
import math

from pages.sketch import Sk


def trays(s: Sk):
    # the machine pushes a pile of drafts along the bench; the worker leans in with the next one in both
    # hands, over two trays, one ticked and one crossed, and chooses
    s.ground(540, 50, 1150, tufts=2)
    s.bot(170, 447, 1.6, look=(1, -0.2))
    s.table(330, 400, w=510, h=140)
    for i in range(5):                                         # the pile it has drafted
        s.rect(362 + (i % 2) * 8, 388 - i * 13, 130, 12, fill="p")
    s.stroke([(246, 440), (300, 400), (360, 372)], "aside")    # its arm, pushing the pile along
    for x in (540, 690):                                       # two trays, seen from the side
        s.stroke([(x, 346), (x + 8, 400), (x + 122, 400), (x + 130, 346)], "ink")
    s.stroke([(584, 372), (598, 388), (628, 356)], "aside", "h", amp=0.5)
    s.stroke([(738, 358), (772, 390)], "point", "h", amp=0.5)
    s.stroke([(772, 358), (738, 390)], "point", "h", amp=0.5)
    s.doc(566, 196, 100, 126, tilt=9, lines=3)                 # the one being decided, over the yes tray
    s.worker(956, 339, look=(-1, 0.3), arms=[(672, 232), (668, 318)], lean=-10)
    s.route([(470, 316), (500, 262), (548, 244)], "path")
    s.label(175, 262, "AI proposes", "aside")
    s.note(400, 120, "plans, questions,|code", (430, 318), "ink")
    s.note(870, 130, "people decide", (690, 208), "point")


def parcel(s: Sk, x: float, y: float, w: float = 120, h: float = 90):
    """A parcel tied with string, its top left at ``x, y``."""
    s.rect(x, y, w, h, fill="p")
    s.line(x + w * 0.5, y, x + w * 0.5, y + h, w="t")
    for k in (-1, 1):
        s.curve([(x + w * 0.5, y), (x + w * 0.5 + k * 22, y - 20), (x + w * 0.5 + k * 30, y - 4), (x + w * 0.5, y)], "ink", "t")


def _fallen_calendar(s: Sk, cx: float, cy: float, w: float, h: float, tilt: float):
    """A tear-off calendar taken down and left leaning, its middle at ``cx, cy``."""
    co, si = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))

    def t(u: float, v: float) -> tuple[float, float]:
        return cx + u * co - v * si, cy + u * si + v * co

    s.poly([t(-w / 2, -h / 2), t(w / 2, -h / 2), t(w / 2, h / 2), t(-w / 2, h / 2)], fill="p")
    s.poly([t(-w / 2, -h / 2), t(w / 2, -h / 2), t(w / 2, -h / 2 + 26), t(-w / 2, -h / 2 + 26)], fill="ink")
    for u in (-w * 0.24, w * 0.24):
        s.stroke([t(u, -h / 2 - 11), t(u, -h / 2 + 11)], "ink", "h", amp=0.3)
    for i in range(3):                                         # the days, in rows
        v = -h / 2 + 52 + i * 26
        s.stroke([t(-w / 2 + 18, v), t(w / 2 - 18, v)], "faint", "t", amp=0.6)


def clock(s: Sk):
    # the machine sits beside a parcel it finished long ago; the fortnight's calendar is down on the floor,
    # and the worker hangs a clock on the post where it used to be
    s.ground(540, 50, 1150, tufts=2)
    s.bot(150, 453, 1.5, look=(1, -0.6))
    parcel(s, 250, 440, 130, 100)
    s.line(640, 300, 640, 540, w="h")                          # the post
    _fallen_calendar(s, 552, 462, 136, 146, -17)               # what hung on it, down against its foot
    s.clock(640, 232, 70, hour=2)
    s.worker(868, 339, look=(-1, -0.5), arms=[(704, 210), (648, 344)], lean=-9)
    s.note(270, 150, "built in|an afternoon", (316, 412), "aside")
    s.note(476, 306, "sprint:|two weeks", (524, 388), "point", bend=-10)
    s.note(1000, 96, "bolt: hours|or days", (716, 190), "path")


SKETCHES = [
    {"name": "the-machine-drafts-a-person-decides",
     "idea": "AI-DLC inverts who starts: the AI drafts the plans, questions and code, and people keep the decision",
     "verb": "sort", "prop": "yes tray and no tray at the end of a bench",
     "alt": "A small machine pushes a pile of drafts along a bench. At the other end a worker leans in and holds one "
            "sheet in both hands over two trays, one marked with a tick and one with a cross.",
     "caption": "In AI-DLC the AI starts the work: plans, questions, code. People validate what it proposes and "
                "make the decisions.",
     "draw": trays},
    {"name": "a-clock-where-the-calendar-hung",
     "idea": "an agent builds in an afternoon and then waits out a two-week sprint; a bolt plans at the speed it builds",
     "verb": "swap", "prop": "wall calendar for a clock",
     "alt": "A small machine sits idle beside a finished parcel. A calendar has been taken down and leans against the "
            "foot of a post. A worker steadies the post with one hand and hangs a clock on it with the other.",
     "caption": "An agent that builds a story in an afternoon sits idle for most of a two-week sprint. A bolt plans "
                "in hours or days.",
     "draw": clock},
]
