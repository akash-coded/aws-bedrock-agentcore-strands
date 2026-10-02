"""Sketches for the lesson on proving an agent meets its bar."""
from pages.sketch import Sk


def lens(s: Sk):
    # a thermometer whose reading sits a hair above the mark; the worker has dropped the small lens and is
    # heaving up one big enough to show the gap
    s.ground(540, 50, 1150, tufts=2)
    s.oval(868, 492, 40, 40, w="h")                          # the small lens, dropped
    s.stroke([(838, 520), (800, 536)], "ink", "h", amp=0.5)
    s.rect(710, 96, 40, 356, fill="p")                       # the thermometer
    s.rect(721, 380, 18, 80, "aside", fill="aside")
    s.oval(730, 488, 42, 42, "aside", fill="aside")
    for i in range(3):
        s.line(750, 392 + i * 22, 766, 392 + i * 22, w="t")
    s.oval(730, 255, 122, 122, fill="p", w="h")              # the big lens, and what it shows
    s.line(682, 166, 682, 346)
    s.line(778, 166, 778, 346)
    s.rect(694, 232, 72, 112, "aside", fill="aside")
    s.stroke([(658, 290), (810, 290)], "ink", "h", amp=0.6)
    s.stroke([(822, 236), (822, 286)], "point", "h", amp=0.4)
    s.stroke([(644, 342), (522, 436)], "ink", "h", amp=0.6)  # its handle
    s.worker(340, 339, look=(1, -0.5), arms=[(514, 440), (550, 414)], lean=-6, squash=0.95)
    s.label(876, 240, "score 82.4%", "aside", anchor="start")
    s.label(876, 312, "bar 80%", "ink", anchor="start")
    s.note(470, 100, "968 cases", (626, 178), "point")
    s.label(1040, 446, "500 was|not enough", "ink")


def pick(s: Sk):
    # a jar of plain marbles with a red one or two in it; the worker lifts the red ones out one at a time
    # and puts them in a tray of their own
    s.ground(540, 50, 1150, tufts=2)
    s.stroke([(170, 320), (184, 540), (436, 540), (450, 320)], "ink", "h")       # the jar
    for i, (x, y) in enumerate(((222, 514), (274, 516), (326, 514), (378, 516), (248, 470), (300, 472),
                                (352, 470), (404, 474), (222, 428), (274, 428), (326, 430), (378, 428),
                                (248, 386), (300, 384), (352, 386), (404, 388))):
        s.oval(x, y, 24, 24, fill="point" if i == 5 else "p")
    s.stroke([(800, 478), (814, 540), (1006, 540), (1020, 478)], "ink", "h")     # the tray
    for x in (856, 910, 964):
        s.oval(x, 512, 24, 24, "point", fill="point")
    s.worker(610, 339, look=(1, 0.5), arms=[(450, 262), (800, 420)])
    s.oval(432, 250, 24, 24, "point", fill="point")
    s.oval(818, 430, 24, 24, "point", fill="point")
    s.label(300, 200, "everyday cases", "ink")
    s.note(640, 110, "rare, costly", (452, 226), "point")
    s.note(960, 300, "take extra|of these", (930, 470), "aside")


SKETCHES = [
    {"name": "a-hair-above-the-mark",
     "idea": "the closer the score sits to the bar, the more cases it takes to tell them apart",
     "verb": "heave up", "prop": "giant lens at a thermometer",
     "alt": "A thermometer reads a hair above its mark. A worker strains to hold up a lens as big as itself to show "
            "the gap, and a much smaller lens lies dropped on the floor behind.",
     "caption": "Codeshare scored 82.4% against a bar of 80%. A gap that small takes 968 cases to prove, and half "
                "the gap takes four times as many.",
     "draw": lens},
    {"name": "pick-the-rare-ones-by-hand",
     "idea": "a sample that looks like traffic holds almost none of the rare, costly cases, so those are drawn on purpose",
     "verb": "pick out one by one", "prop": "jar of marbles and a tray",
     "alt": "A jar is full of plain marbles with one red one among them. A worker lifts a red marble out with one hand "
            "and sets another in a tray that holds only red ones.",
     "caption": "A sample that looks like traffic holds few of the rare, costly cases. Draw each kind separately and "
                "take extra of those.",
     "draw": pick},
]
