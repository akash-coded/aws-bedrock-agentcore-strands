"""Sketches for the lesson on how the lifecycle evolved."""
from pages.sketch import Sk


def log(s: Sk, x: float, y: float, tilt: float, w: float = 84):
    """A log floating in the stream, seen from above."""
    s.rect(x - w / 2, y - 10, w, 20, "ink", fill="p", tilt=tilt)


def jam(s: Sk):
    # a stream seen from above, pinched at two places; the worker has poled the logs through the first
    # pinch, and they are piling up at the second
    top = [(40, 150), (230, 152), (360, 196), (410, 206), (460, 196), (620, 152), (790, 170), (880, 206), (930, 196), (1160, 156)]
    bot = [(40, 300), (230, 298), (360, 254), (410, 246), (460, 254), (620, 298), (790, 282), (880, 248), (930, 258), (1160, 296)]
    s.curve(top, "ink")
    s.curve(bot, "ink")
    for x, y in ((398, 196), (426, 258), (868, 196), (896, 258)):               # the rocks that make each pinch
        s.blob(x, y, 30, 22, "ink", lumps=4, depth=0.1)
    log(s, 476, 224, 8, 70)                                                    # the one being poled through
    log(s, 590, 228, 4)                                                        # through, and on their way
    log(s, 700, 214, -8)
    for x, y, tilt in ((800, 200, 62), (812, 232, -40), (790, 258, 18), (838, 214, -74), (846, 246, 80)):
        log(s, x, y, tilt, 78)                                                 # the next jam
    for x0, y0 in ((90, 226), (180, 204), (1010, 228), (1080, 250)):             # the water
        s.curve([(x0, y0), (x0 + 22, y0 - 7), (x0 + 44, y0), (x0 + 66, y0 - 7)], "faint", "t")
    s.ground(562, 60, 450, tufts=2)
    s.worker(250, 392, 1.6, look=(1, -0.6), arms=[None, (352, 322)])
    s.stroke([(300, 384), (446, 228)], "ink", "h")                             # the pole
    s.arrow(520, 110, 730, 110, "path", dash=True, w="h")
    s.label(625, 84, "the jam moves", "path")
    s.note(580, 420, "cleared:|typing the code", (436, 262), "ink")
    s.note(960, 420, "now: is it|right enough?", (826, 276), "point")


def case(s: Sk):
    # an open suitcase already full of the old kit; the worker lowers three new things in on top
    s.ground(540, 50, 1150, tufts=3)
    s.rect(410, 268, 312, 152, "ink", fill="p", tilt=-2)                       # the lid, standing open
    for x in (468, 664):
        s.stroke([(x, 272), (x, 418)], "ink", "t")
    for x in (480, 566, 652):                                                  # the old kit, showing over the rim
        s.oval(x, 412, 42, 24, "ink", fill="p", w="t")
    s.rect(400, 420, 332, 120, fill="p")                                       # the case
    for x in (460, 672):
        s.stroke([(x, 420), (x, 540)], "ink", "t")                             # its straps
    s.curve([(532, 476), (538, 456), (594, 456), (600, 476)], "ink", "h")      # its handle
    s.worker(170, 339, look=(1, 0.3), arms=[(330, 366), (332, 290)])
    for i in range(3):                                                         # three new things, going in
        s.rect(318 + i * 8, 318 - i * 44, 84, 40, "point", fill="p", tilt=-5 + i * 5)
    s.note(600, 120, "the old kit stays", (566, 228), "ink")
    s.label(790, 300, "add: a pass mark", "point", anchor="start", size=56)
    s.label(790, 370, "a limit on actions", "point", anchor="start", size=56)
    s.label(790, 440, "a watch for drift", "point", anchor="start", size=56)


SKETCHES = [
    {"name": "the-jam-moves-downstream",
     "idea": "each lifecycle cleared the bottleneck of its day, and the work piled up at the next narrow place",
     "verb": "pole through", "prop": "log jam in a stream",
     "alt": "A stream seen from above narrows at two places. A worker on the bank has poled the logs through the first "
            "narrow place, and they are piling up at the second.",
     "caption": "Each lifecycle cleared the jam of its day, and the work piled up at the next narrow place. Which jam "
                "does a new method move?",
     "draw": jam},
    {"name": "repack-and-add-three",
     "idea": "agentic delivery keeps almost all of the old discipline and adds three specific things",
     "verb": "pack on top", "prop": "open suitcase of old kit",
     "alt": "An open suitcase is already full. A worker presses three small new parcels in on top of what is there.",
     "caption": "Keep the gates, tests, flags and postmortems you have. Add three: a pass mark, a limit on what the "
                "agent may do, a watch for drift.",
     "draw": case},
]
