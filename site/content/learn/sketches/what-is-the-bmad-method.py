"""Sketches for the lesson on the BMAD Method."""
from pages.sketch import Sk


def spools(s: Sk):
    # a knot of yarn on the left; the worker draws one thread out of it and winds it onto the next spool in a row
    s.ground(540, 50, 1150, tufts=2)
    s.tangle(215, 420, 125)
    s.spool(790, 540, 1.25, wound=False)
    s.spool(930, 540, 1.25)
    s.spool(1070, 540, 1.25)
    s.worker(540, 339, look=(1, 0.5), arms=[(418, 402), (700, 414)], lean=6)
    s.curve([(306, 446), (360, 404), (418, 402)], "path")       # the thread, out of the knot
    s.curve([(700, 414), (734, 440), (760, 478)], "path")       # and onto the spool
    for i in range(2):
        s.stroke([(753, 500 - i * 20), (827, 508 - i * 20)], "path", "t", amp=0.5)
    s.label(56, 150, "who decided that?", "point", anchor="start")
    s.label(70, 268, "one long chat", "aside", anchor="start")
    s.note(930, 200, "one document each", (930, 380), "ink")


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
    # the trail used to end at a line on the ground; past it, the worker reaches up and posts one more
    # envelope, and the route runs back under the ground to the first document
    g = 500
    s.ground(g, 50, 1150, tufts=2)
    s.line(176, 420, 176, g, w="h")                             # where the trail starts: the brief, on its post
    s.doc(116, 270, 120, 150, lines=4)
    s.stroke([(560, g - 30), (560, g + 18)], "point", "h")     # where it used to end
    s.hatch(566, g - 26, 34, 40, gap=12, pen="point")
    s.line(1065, 410, 1065, g, w="h")
    s.letterbox(980, 190)
    s.envelope(880, 220, 138, 84, tilt=-8)
    s.worker(742, 299, look=(1, -0.3), arms=[(884, 300), (896, 240)], lean=9)
    s.note(1000, 70, "the incident,|written up", (962, 210), "ink")
    s.note(430, 250, "used to|stop here", (552, 462), "point")
    s.route([(1065, 524), (720, 622), (330, 610), (196, 440)], "path")
    s.label(690, 580, "the next brief", "path")


SKETCHES = [
    {"name": "wind-the-chat-onto-spools",
     "idea": "BMAD takes decisions out of one long conversation and puts each on its own document",
     "verb": "wind", "prop": "knot of yarn and a row of spools",
     "alt": "A worker pulls one thread out of a big knot of yarn and winds it onto a spool. Two more spools beside it "
            "are already neatly wound.",
     "caption": "Each decision sits in its own document, so it can be found.",
     "draw": spools},
    {"name": "six-binders-one-small-hatch",
     "idea": "the persona trail is right for audited work and dead weight on a one-line fix",
     "verb": "squeeze through", "prop": "six binders at a small hatch",
     "alt": "A worker carries a pile of six binders up to a wall. The only way through is a hatch the size of a postcard.",
     "caption": "Six documents suit an audited feature. They do not suit a typo fix.",
     "draw": hatch},
    {"name": "post-it-back-to-the-start",
     "idea": "one more hand-off after launch: what production teaches goes back in writing as the next brief",
     "verb": "post", "prop": "letterbox past the finish line",
     "alt": "A red line on the ground marks where the trail used to end. Beyond it, a worker reaches up with both "
            "hands and posts an envelope into a letterbox, and a dashed route runs back to the first document.",
     "caption": "After launch, the incident is written up and becomes the next brief.",
     "h": 650, "draw": post},
]
