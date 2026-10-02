"""Sketches for the lesson on the BMAD Method."""
from pages.sketch import Sk


def spools(s: Sk):
    # a knot of yarn on the left; the worker draws one thread out of it and winds it onto the next spool in a row
    s.ground(540, 50, 1150, tufts=2)
    s.tangle(205, 420, 125)
    s.spool(790, 540, 1.25, wound=False)
    s.spool(930, 540, 1.25)
    s.spool(1070, 540, 1.25)
    s.worker(530, 339, look=(1, 0.3), arms=[(408, 402), (690, 414)])
    s.curve([(296, 446), (350, 404), (408, 402)], "path")       # the thread, out of the knot
    s.curve([(690, 414), (730, 440), (760, 478)], "path")       # and onto the spool
    for i in range(2):
        s.stroke([(753, 500 - i * 20), (827, 508 - i * 20)], "path", "t", amp=0.5)
    s.note(255, 140, "who decided that?", (215, 300), "point")
    s.label(205, 600, "one long chat", "aside")
    s.note(900, 180, "brief, requirements,|architecture", (930, 380), "ink")


def hatch(s: Sk):
    # a pile of six binders in the worker's arms, and a hatch in the wall the size of a postcard
    s.ground(540, 50, 1150, tufts=2)
    s.rect(880, 170, 290, 370, fill="p")                        # the wall
    s.hatchway(965, 330, 120, 84)
    s.worker(400, 339, look=(1, 0.1), arms=[(650, 436), (612, 436)], lean=5)
    for i in range(6):
        s.binder(610 + (i % 2) * 8, 392 - i * 42, 200, 40)
    s.burst(850, 300, r=14, n=3, a0=-40, a1=40)
    s.label(1025, 288, "a typo fix", "ink")
    s.note(715, 124, "six documents", (715, 176), "point")
    s.note(250, 88, "\"we are a|BMAD shop\"", (385, 214), "aside")


def post(s: Sk):
    # a washing line of pegged documents ends in a frayed string; past the end, the worker reaches up
    # and posts one more envelope, and the route runs back to the first sheet on the line
    g = 500
    s.ground(g, 50, 1150, tufts=2)
    s.string(60, 122, 470, 150, sag=14)
    for i, x in enumerate((90, 210, 330)):
        s.doc(x, 142 + i * 6, 84, 104, lines=3)
        s.line(x + 42, 126 + i * 6, x + 42, 150 + i * 6, w="h")
    for dy in (-14, 0, 14):                                     # the frayed end
        s.stroke([(470, 150), (500, 150 + dy)], "ink", "t", amp=0.6)
    s.line(1065, 410, 1065, g, w="h")
    s.letterbox(980, 190)
    s.envelope(900, 224, 130, 80, tilt=-8)
    s.worker(770, 299, look=(1, -0.3), arms=[None, (916, 276)])
    s.note(990, 62, "the incident,|written up", (962, 214), "ink")
    s.note(470, 366, "trail used to|stop here", (480, 170), "point")
    s.route([(1065, 524), (700, 606), (260, 590), (128, 270)], "path")
    s.label(600, 570, "the next brief", "path")


SKETCHES = [
    {"name": "wind-the-chat-onto-spools",
     "idea": "BMAD takes decisions out of one long conversation and puts each on its own document",
     "verb": "wind", "prop": "knot of yarn and a row of spools",
     "alt": "A worker pulls one thread out of a big knot of yarn and winds it onto a spool. Two more spools beside it "
            "are already neatly wound.",
     "caption": "Each decision sits in its own document, so it can be found.",
     "h": 640, "draw": spools},
    {"name": "six-binders-one-small-hatch",
     "idea": "the persona trail is right for audited work and dead weight on a one-line fix",
     "verb": "squeeze through", "prop": "six binders at a small hatch",
     "alt": "A worker carries a pile of six binders up to a wall. The only way through is a hatch the size of a postcard.",
     "caption": "Six documents suit an audited feature. They do not suit a typo fix.",
     "draw": hatch},
    {"name": "post-it-back-to-the-start",
     "idea": "one more hand-off after launch: what production teaches goes back in writing as the next brief",
     "verb": "post", "prop": "letterbox past the end of a washing line",
     "alt": "Documents hang pegged on a line that ends in a frayed string. Beyond the end, a worker reaches up and "
            "posts an envelope into a letterbox, and a dashed route runs back to the first document.",
     "caption": "After launch, the incident is written up and becomes the next brief.",
     "h": 650, "draw": post},
]
