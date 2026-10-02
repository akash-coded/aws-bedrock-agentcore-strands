"""Sketches for the lesson on guardrails that hold."""
import math

from pages.sketch import Sk


def novalve(s: Sk):
    # a notice hangs from the pipe and says what the limit is; where the valve should be there is only pipe,
    # and the worker's hands close on nothing while the money runs out of the far end
    s.ground(540, 50, 1150, tufts=2)
    s.pipe([(60, 160), (880, 160), (912, 192), (912, 280)], r=20)
    ring = [(480 + 54 * math.cos(i * math.pi / 8), 158 + 54 * math.sin(i * math.pi / 8)) for i in range(16)]
    s.stroke(ring, "point", "", closed=True, dash=True, raw=True)                # the valve that is not there
    s.line(646, 182, 652, 262, w="t")                        # the notice, on its strings
    s.line(814, 182, 808, 262, w="t")
    s.rect(600, 262, 260, 104, fill="p", tilt=2)
    s.label(730, 334, "limit $400", "ink", rot=2, note=False)
    for x, y in ((910, 318), (922, 384), (902, 446)):        # what comes out of the far end
        s.coin(x, y, 22)
    s.stack(912, 530, 4, 110)
    s.worker(312, 347, 1.82, look=(1, -0.4), arms=[(428, 162), (488, 212)], lean=10)
    s.note(770, 76, "nothing here refuses", (548, 124), "point", bend=-14)
    s.label(990, 470, "$2,000", "point", anchor="start")


SKETCHES = [
    {"name": "a-notice-where-the-valve-should-be",
     "idea": "a limit that is only written down reads like a limit and stops nothing",
     "verb": "reach for the valve on", "prop": "pipe with a notice and no valve",
     "alt": "A notice reading limit $400 hangs from a pipe. A worker leans in and reaches up with both hands for a valve that is not there, and "
            "coins marked $2,000 pour out of the far end of the pipe.",
     "caption": "A limit written in a prompt reads like a limit and refuses nothing. Ask to see the line of code that "
                "says no.",
     "draw": novalve},
]
