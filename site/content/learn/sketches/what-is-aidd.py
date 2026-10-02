"""Sketches for the lesson on AI-driven development, the daily craft."""
from pages.sketch import Sk


def door(s: Sk):
    # a notice goes up on a post by the workshop door; every machine in the queue reads it on the way in
    s.ground(540, 50, 1150, tufts=2)
    s.bot(120, 459, 1.4, look=(1, -0.5))
    s.bot(300, 459, 1.4, look=(1, -0.5))
    s.sign(505, 540, "context|file", "ink", post=120)
    s.worker(800, 339, look=(-1, -0.1), arms=[(652, 300), None])
    s.stroke([(652, 300), (634, 262)], "ink", "h")             # the hammer
    s.rect(606, 240, 46, 22, fill="ink", tilt=-25)
    s.door(980, 540, w=140, h=270, ajar=True)
    s.route([(60, 584), (500, 574), (1010, 584)], "path")
    s.note(215, 150, "every session|reads it", (290, 348), "aside")
    s.note(830, 120, "an hour of work", (672, 236), "point")


def count(s: Sk):
    # the machine names a total out loud; the worker moves the beads on an abacus, which says another
    s.ground(540, 50, 1150, tufts=2)
    s.bot(200, 447, 1.6, look=(1, -0.2))
    s.table(420, 420, w=400, h=120)
    s.rect(486, 222, 250, 198, fill="p", sw="h")              # the abacus
    for i, (left, right) in enumerate(((2, 2), (1, 3), (2, 1), (3, 1))):
        y = 222 + 198 * (i + 0.5) / 4
        s.stroke([(486, y), (736, y)], "ink", "t", amp=0.4)
        for k in range(left):
            s.oval(504 + k * 24, y, 10, 16, fill="ink")
        for k in range(right):
            s.oval(718 - k * 24, y, 10, 16, fill="ink")
    s.worker(990, 339, look=(-1, -0.1), arms=[(746, 296), None])
    s.label(215, 282, "model says $80", "aside")
    s.label(215, 204, "no error", "point")
    s.squiggle(132, 218, 166, "point")
    s.label(812, 398, "$62", "ink", size=66)
    s.label(620, 498, "tested code", "ink")


def mirror(s: Sk):
    # one machine checks its work in a mirror, which ticks it; the worker pushes in a second machine to look instead
    s.ground(540, 50, 1150, tufts=2)
    s.bot(160, 453, 1.5, look=(1, 0))
    s.oval(360, 396, 58, 120, w="h")                           # a mirror on a stand
    s.line(360, 516, 360, 540, w="h")
    s.line(318, 540, 402, 540, w="h")
    s.oval(352, 366, 20, 20, "faint")                          # its own eye, looking back
    s.oval(346, 366, 7, 7, "faint", fill="faint")
    s.stroke([(338, 436), (352, 452), (384, 414)], "aside", "h", amp=0.6)
    s.bot(650, 441, 1.7, look=(-1, 0.1))
    s.stroke([(620, 375), (606, 336)], "aside")               # a second aerial: not the same machine
    s.oval(604, 326, 9, 9, "aside")
    s.worker(950, 339, look=(-1, 0.2), arms=[(736, 420), None])
    s.note(285, 140, "agrees with itself", (352, 268), "point")
    s.note(760, 150, "a different model", (665, 312), "aside")
    s.route([(900, 584), (700, 576), (500, 584)], "path")


SKETCHES = [
    {"name": "the-rule-by-the-door",
     "idea": "a rule typed in chat reaches one session; a rule in the context file is read by every session on the way in",
     "verb": "nail up", "prop": "notice on a post by the workshop door",
     "alt": "A worker hammers a notice onto a post beside a workshop door. Two small machines queue in front of it, "
            "both looking up at the notice.",
     "caption": "A rule typed into a chat reaches one session. A rule in the context file is read by every session "
                "before it starts.",
     "h": 620, "draw": door},
    {"name": "eighty-said-sixty-two-counted",
     "idea": "a model doing arithmetic fails fluently; a number the feature acts on is counted by tested code",
     "verb": "count on", "prop": "abacus on the bench",
     "alt": "A small machine says a total out loud, $80. A worker moves the beads of an abacus on a bench, and the "
            "abacus comes to $62.",
     "caption": "The agent returned $80 where the ledger said $62, with no error. A number the feature acts on comes "
                "from tested code, never from a prompt.",
     "draw": count},
    {"name": "the-mirror-always-agrees",
     "idea": "a review step in the same context agrees with its own reasoning; an independent checker is a different model",
     "verb": "wheel in", "prop": "mirror in front of the machine",
     "alt": "A small machine looks into a mirror on a stand, and the mirror shows a tick. A worker pushes a second "
            "machine in from the other side to look instead.",
     "caption": "Asking a model to review its own answer in the same context changes nothing. An independent "
                "checker is a different model or a fresh context.",
     "h": 620, "draw": mirror},
]
