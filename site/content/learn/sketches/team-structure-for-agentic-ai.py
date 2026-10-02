"""Sketches for the lesson on team structure."""
import math

from pages.sketch import Sk


def chart(s: Sk, x: float, y: float):
    """An org chart on a board on an easel, the board's top left at ``x, y``."""
    s.line(x + 60, y + 250, x + 30, 540)
    s.line(x + 260, y + 250, x + 290, 540)
    s.rect(x, y, 320, 250, fill="p")
    s.rect(x + 120, y + 30, 80, 46)
    s.stroke([(x + 160, y + 76), (x + 160, y + 112)], "ink", "t")
    s.stroke([(x + 56, y + 150), (x + 56, y + 112), (x + 264, y + 112), (x + 264, y + 150)], "ink", "t")
    s.stroke([(x + 160, y + 112), (x + 160, y + 150)], "ink", "t")
    for i in range(3):
        s.rect(x + 20 + i * 104, y + 150, 72, 46)


def conway(s: Sk):
    # the org chart on an easel, and the agents set out on the floor to match it, one under each box
    s.ground(540, 50, 1150, tufts=2)
    chart(s, 60, 120)
    s.worker(530, 339, look=(-1, -0.2), arms=[(384, 300), (704, 446)])
    for i in range(3):
        s.bot(770 + i * 160, 472, 1.15, look=(1 if i < 2 else -1, 0))
    for x in (850, 1010):                                    # where one hands to the next
        s.stroke([(x - 16, 450), (x + 8, 464), (x - 10, 480), (x + 14, 494)], "point", "h", amp=0.5)
    s.label(220, 86, "the org chart", "ink")
    s.label(930, 110, "one agent|per department", "aside")
    s.label(900, 310, "breaks at the hand-offs", "point")
    s.arrow(860, 330, 852, 430, "point", w="t", head=15)
    s.arrow(990, 330, 1008, 430, "point", w="t", head=15)


def _tf(x: float, y: float, deg: float):
    co, si = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return lambda px, py: (x + px * co - py * si, y + px * si + py * co)


def can(s: Sk, x: float, y: float, deg: float = 0):
    """A watering can centred at ``x, y``, its spout to the right, tipped by ``deg``, with a name stuck on its side.
    Returns the rose it pours from and the back of its handle."""
    t = _tf(x, y, deg)
    s.poly([t(-62, -54), t(62, -54), t(68, 54), t(-68, 54)], fill="p")
    s.stroke([t(64, 30), t(170, -60)], "ink", "h")
    s.poly([t(156, -82), t(192, -48), t(182, -38), t(146, -68)], fill="p")
    s.curve([t(-62, -44), t(-126, -10), t(-66, 44)], "ink", "h")
    s.poly([t(-40, -22), t(40, -22), t(40, 20), t(-40, 20)], "aside")
    s.stroke([t(-26, 0), t(24, -2)], "aside", "t", amp=1.2)
    return t(184, -52), t(-122, -10)


def named(s: Sk):
    # a plant everyone is supposed to water, drooping; the worker waters it from a can with one name on it
    s.ground(540, 50, 1150, tufts=2)
    s.poly([(652, 462), (792, 462), (770, 540), (674, 540)], fill="p")        # the pot
    s.rect(640, 440, 164, 24, fill="p")
    s.curve([(722, 440), (716, 360), (730, 290), (778, 262), (812, 300)], "ink", "h")   # the plant, bent over
    s.oval(816, 326, 20, 20, fill="p")
    s.burst(816, 326, 22, 6, "ink", 0, 180)
    for k, ly in ((-1, 392), (1, 372)):                      # two limp leaves
        lx = 718 if k < 0 else 716
        tip = (lx + k * 50, ly + 42)
        s.curve([(lx, ly), (lx + k * 40, ly), tip], "ink")
        s.curve([(lx, ly), (lx + k * 14, ly + 30), tip], "ink")
    s.worker(200, 339, look=(1, 0.2), arms=[None, (334, 252)])
    rose, grip = can(s, 440, 300, 22)
    for dx, dy in ((4, 30), (26, 62), (-2, 92)):
        s.drop(rose[0] + dx, rose[1] + dy, 0.9)
    s.sign(1004, 540, "we all do", "point", post=120)
    s.label(900, 130, "who owns governance?", "ink")
    s.note(300, 100, "one name on the can", (436, 250), "aside")


SKETCHES = [
    {"name": "the-org-chart-set-out-on-the-floor",
     "idea": "agent boundaries copy team boundaries unless someone decides them",
     "verb": "copy from", "prop": "org chart on an easel",
     "alt": "An org chart stands on an easel. A worker looks at it with one hand on the chart and the other placing the "
            "first of three small machines, which stand in a row to match the chart's three boxes. Red marks sit "
            "between the machines.",
     "caption": "One agent per department is often an org chart, not a design. Decide the seams on purpose, and give each hand-off a named limit.",
     "draw": conway},
    {"name": "one-name-on-the-watering-can",
     "idea": "a job that belongs to everyone gets done by nobody, so one name goes on it",
     "verb": "water", "prop": "watering can with a name on it",
     "alt": "A drooping plant in a pot stands beside a sign that reads we all do. A worker waters it from a can with a "
            "name written on its side.",
     "caption": "Governance belongs to no delivery role, so name the one sponsor who owns it. If the answer is \"we all do\", nobody does.",
     "draw": named},
]
