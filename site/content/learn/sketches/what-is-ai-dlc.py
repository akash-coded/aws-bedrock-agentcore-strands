"""Sketches for the lesson on AWS's AI-DLC."""

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


SKETCHES = [
    {"name": "the-machine-drafts-a-person-decides",
     "idea": "AI-DLC inverts who starts: the AI drafts the plans, questions and code, and people keep the decision",
     "verb": "sort", "prop": "yes tray and no tray at the end of a bench",
     "alt": "A small machine pushes a pile of drafts along a bench. At the other end a worker leans in and holds one "
            "sheet in both hands over two trays, one marked with a tick and one with a cross.",
     "caption": "In AI-DLC the AI starts the work: plans, questions, code. People validate what it proposes and "
                "make the decisions.",
     "draw": trays},
]
