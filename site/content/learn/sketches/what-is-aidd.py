"""Sketches for the lesson on AI-driven development, the daily craft."""
from pages.sketch import Sk


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


SKETCHES = [
    {"name": "eighty-said-sixty-two-counted",
     "idea": "a model doing arithmetic fails fluently; a number the feature acts on is counted by tested code",
     "verb": "count on", "prop": "abacus on the bench",
     "alt": "A small machine says a total out loud, $80. A worker moves the beads of an abacus on a bench, and the "
            "abacus comes to $62.",
     "caption": "The agent returned $80 where the ledger said $62, with no error. A number the feature acts on comes "
                "from tested code, never from a prompt.",
     "draw": count},
]
