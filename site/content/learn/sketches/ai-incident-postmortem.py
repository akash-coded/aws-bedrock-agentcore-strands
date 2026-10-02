"""Sketches for the lesson on postmortems for AI incidents."""
from pages.sketch import Sk


def fuses(s: Sk):
    # the fuse box, opened: five places for a fuse, two empty and three with a rolled-up note in them
    s.ground(540, 50, 520, tufts=2)
    s.rect(540, 170, 480, 300, fill="p", sw="h")             # the box
    s.poly([(540, 170), (436, 204), (436, 504), (540, 470)], fill="p")           # its door, open
    for i in range(5):
        x = 596 + i * 92
        s.rect(x - 16, 232, 32, 14, fill="ink")
        s.rect(x - 16, 370, 32, 14, fill="ink")
        if i in (1, 2, 3):
            s.doc(x - 24, 254, 48, 108, tilt=5, lines=3)     # a note where the fuse should be
        else:
            s.stroke([(x - 13, 252), (x + 13, 252), (x + 13, 364), (x - 13, 364)], "faint", "t", closed=True)
    s.worker(250, 339, look=(1, 0), arms=[None, (438, 350)])
    s.label(780, 130, "five layers claimed", "ink")
    s.label(690, 442, "none enforced", "point", size=54)
    s.note(880, 548, "a sentence in a prompt", (886, 372), "aside")


def steps(s: Sk):
    # two steps: the machine stood on the upper one, and the worker has set it down on the lower. A dashed
    # outline shows where it was, and an arrow the way back up
    s.ground(540, 50, 1150, tufts=2)
    s.line(560, 540, 560, 440, w="h")                        # the steps
    s.line(560, 440, 830, 440, w="h")
    s.line(830, 440, 830, 340, w="h")
    s.line(830, 340, 1140, 340, w="h")
    s.line(1140, 340, 1140, 540, w="h")
    was = ((900, 216), (1040, 216), (1040, 334), (900, 334))
    for i in range(4):                                       # where it stood
        s.stroke([was[i], was[(i + 1) % 4]], "faint", dash=True)
    s.bot(690, 353, 1.5, look=(-1, 0))
    s.worker(380, 339, look=(1, 0), arms=[(616, 396), (620, 344)])
    s.arrow(780, 316, 890, 262, "path", bend=22, dash=True, w="h")
    s.label(970, 180, "acts alone", "ink")
    s.label(620, 212, "needs an approver", "aside")
    s.label(986, 426, "fourteen days|of shadow", "path", size=54)


SKETCHES = [
    {"name": "notes-where-the-fuses-go",
     "idea": "most controls that failed were never enforced; they were sentences where a mechanism should be",
     "verb": "open up", "prop": "fuse box with notes for fuses",
     "alt": "A worker holds open the door of a fuse box. Of five places for a fuse, two are empty and three hold a "
            "rolled-up note.",
     "caption": "Five layers of defence were claimed and none was enforced. The cap and the approver were sentences in "
                "a prompt.",
     "draw": fuses},
    {"name": "down-one-step",
     "idea": "after an incident the action drops one autonomy level, and evidence, not a date, moves it back",
     "verb": "set down one step", "prop": "two steps and the machine",
     "alt": "A worker sets a small machine down on the lower of two steps. A dashed outline on the upper step shows "
            "where it stood, and a dashed arrow leads back up to it.",
     "caption": "After the incident refunds drop one level, from acting alone to needing an approver, until a "
                "fourteen-day shadow run earns the level back.",
     "draw": steps},
]
