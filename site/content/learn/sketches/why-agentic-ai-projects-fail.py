"""Sketches for the lesson on why agentic projects fail."""
import math

from pages.sketch import Sk


def leak(s: Sk):
    # a walker with its eyes on a ticked checklist and a sack on its back; the sack has a hole, and what
    # was in it lies along the road behind
    s.ground(540, 50, 1150, tufts=2)
    s.blob(560, 300, 84, 104, "ink", lumps=4, depth=0.05)                      # the rucksack on its back
    s.curve([(488, 262), (556, 284), (632, 256)], "ink")                       # its flap
    s.rect(506, 318, 70, 52, "ink", fill="p", sw="t")                          # its pocket
    s.worker(700, 339, look=(1, 0.1), arms=[(856, 346), (852, 290)], legs="walk", lean=4)
    s.doc(850, 236, 104, 134, tilt=6, lines=2, mark="tick")
    for x, y in ((512, 430), (498, 482)):                                      # falling
        s.coin(x, y, 15)
    for x in (120, 215, 300, 392, 470):                                        # fallen
        s.oval(x, 530, 17, 8, "ink", fill="p")
    s.ring(505, 398, 30, 20)
    s.note(880, 110, "every check passes", (908, 226), "aside")
    s.note(290, 250, "no error|for this", (478, 396), "point")
    s.label(250, 478, "the value", "ink")


def snowball(s: Sk):
    # a snowball that started small rolls down a hill, bigger at each of four bumps, and arrives against
    # the worker at the bottom
    ux, uy = 0.866, 0.5
    x0, y0 = 60, 170
    foot = (x0 + 760 * ux, y0 + 760 * uy)
    s.curve([(x0, y0), (x0 + 380 * ux, y0 + 380 * uy), foot, (900, 556), (1150, 560)], "ink")
    for t, r, pen in ((40, 14, "ink"), (250, 30, "faint"), (460, 50, "faint")):
        px, py = x0 + t * ux, y0 + t * uy
        s.oval(px + 0.5 * r, py - 0.866 * r, r, r, pen, fill="p")
    s.oval(812, 452, 104, 104, "ink", fill="p", w="h")                         # the bill, arrived
    s.curve([(760, 400), (790, 372), (832, 366)], "ink", "t")
    s.worker(1040, 359, look=(-1, -0.1), arms=[(908, 400), (900, 480)], lean=9, squash=0.94)
    for t in (130, 280, 430, 580):                                             # four habits, one after another
        px, py = x0 + t * ux, y0 + t * uy
        s.stroke([(px - 0.5 * 10, py + 0.866 * 10), (px - 0.5 * 34, py + 0.866 * 34)], "path", "h", amp=0.3)
    px, py = x0 + 330 * ux, y0 + 330 * uy
    s.label(px - 0.5 * 96, py + 0.866 * 96, "four habits, multiplied", "path", rot=30)
    s.note(880, 120, "4.4 times|the estimate", (830, 340), "point")


SKETCHES = [
    {"name": "leaking-on-schedule",
     "idea": "these failures raise no error, so the checks a team already has stay green while the value drains away",
     "verb": "leak", "prop": "rucksack with a split seam",
     "alt": "A worker walks along with its eyes on a ticked checklist. The rucksack on its back has split, and what was in "
            "it lies in a line along the road behind.",
     "caption": "None of these failures throws an error. The checks you already have stay green while the value runs "
                "out behind you.",
     "draw": leak},
    {"name": "four-habits-one-snowball",
     "idea": "ordinary habits multiply rather than add, so a bill grows fourfold with nothing running away",
     "verb": "brace against", "prop": "snowball down a hill",
     "alt": "A small snowball at the top of a hill has rolled down past four marks, growing at each. At the bottom it is "
            "taller than the worker, who braces against it with both hands.",
     "caption": "Nothing ran away. Four ordinary habits multiplied, and by day 75 the bill was 4.4 times its estimate "
                "with traffic flat.",
     "h": 640, "draw": snowball},
]
