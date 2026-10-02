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


SKETCHES = [
    {"name": "the-baton-on-the-track",
     "idea": "the work is fast; the time is lost in the waits between phases, and a wait nobody owns is the programme manager's",
     "verb": "pick up", "prop": "relay baton lying between two runners",
     "alt": "Two small machines stand on a running track, one that has finished its leg and one waiting and looking "
            "back. A red relay baton lies on the track between them. A worker bends over it and picks it up with both hands.",
     "caption": "Agents build a story in hours. The weeks go in the waits between phases, which belong to nobody unless they belong to you.",
     "draw": baton},
]
