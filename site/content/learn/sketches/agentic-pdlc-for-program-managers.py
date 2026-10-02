"""Sketches for the lesson for programme managers."""
from pages.sketch import Sk


def baton(s: Sk):
    # a relay: one runner has finished its leg, the next is waiting and looking back, and the baton lies
    # on the track between them. The worker bends over it with both hands.
    s.ground(540, 50, 1150, tufts=1)
    for x in range(120, 1100, 150):                                        # the lane, marked on the track
        s.stroke([(x, 566), (x + 70, 566)], "faint", "t", amp=0.6)
    for i in range(3):                                                     # the first runner came in fast
        s.stroke([(52, 430 + i * 22), (90, 430 + i * 22)], "aside", "t", amp=0.5)
    s.bot(170, 459, 1.4, look=(1, 0.4))
    s.bot(1040, 459, 1.4, look=(-1, 0.4))
    s.rect(596, 506, 190, 30, "point", fill="point", tilt=-3)             # the baton, dropped
    s.oval(596, 526, 9, 15, "point", fill="p")
    s.burst(692, 492, 22, 5)
    s.worker(516, 339, look=(0.8, 1), arms=[(634, 512), (698, 508)], lean=24)
    s.label(50, 312, "the work: hours", "aside", anchor="start")
    s.note(900, 200, "the wait: weeks", (774, 492), "point")
    s.label(590, 110, "nobody's, so yours", "ink")


def _coat(s: Sk, cx: float, y: float):
    s.curve([(cx - 4, y - 34), (cx + 10, y - 24), (cx, y - 2)], "ink", "t")              # the hanger's hook
    s.poly([(cx - 20, y), (cx + 20, y), (cx + 56, y + 16), (cx + 70, y + 200), (cx - 70, y + 200), (cx - 56, y + 16)], fill="p")
    s.stroke([(cx - 20, y), (cx, y + 56), (cx + 20, y)], "ink", "t")
    s.line(cx, y + 56, cx, y + 198, w="t")


def ticket(s: Sk):
    # a tailor's rail of coats, each with a ticket that says whose it is and when it is due.
    # One coat has no ticket. The worker is writing one for it.
    s.ground(540, 60, 1140, tufts=2)
    s.line(420, 40, 420, 176, w="t")
    s.line(1070, 40, 1070, 176, w="t")
    s.line(396, 178, 1094, 178, w="h")
    for i, cx in enumerate((510, 670, 830, 990)):
        _coat(s, cx, 212)
        if i:
            s.tag(cx + 34, 180, 62, 40, tilt=-6)
    s.worker(220, 339, look=(1, -0.1), arms=[None, (424, 300)])
    s.rect(420, 274, 70, 46, fill="p", tilt=-8)                            # the blank ticket in its hand
    s.ring(520, 300, 62, 78)
    s.note(250, 86, "no owner:|the best find", (470, 236), "point")
    s.note(800, 96, "owner, date", (860, 216), "aside")
    s.label(750, 504, "open decisions", "ink")


SKETCHES = [
    {"name": "the-baton-on-the-track",
     "idea": "the work is fast; the time is lost in the waits between phases, and a wait nobody owns is the programme manager's",
     "verb": "pick up", "prop": "relay baton lying between two runners",
     "alt": "Two small machines stand on a running track, one that has finished its leg and one waiting and looking "
            "back. A red relay baton lies on the track between them. A worker bends over it and picks it up with both hands.",
     "caption": "Agents build a story in hours. The weeks go in the waits between phases, which belong to nobody unless they belong to you.",
     "draw": baton},
    {"name": "the-coat-with-no-ticket",
     "idea": "an open decision with no owner is the find; give it a name and a date",
     "verb": "write a ticket for", "prop": "tailor's rail of coats",
     "alt": "Four coats hang on a tailor's rail. Three carry a ticket. The fourth has none and is ringed in red, and a "
            "worker holds a blank ticket up to it.",
     "caption": "Every open decision gets an owner and a date. The one with neither is the most useful thing you can find.",
     "draw": ticket},
]
