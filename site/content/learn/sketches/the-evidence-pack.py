"""Sketches for the lesson on the evidence pack."""
from pages.sketch import Sk


def outline(s: Sk):
    # the document is there, and ticked; the thing it describes has moved along, and the worker is
    # about to set a crate down on the outline it left behind
    s.ground(540, 50, 1150, tufts=2)
    s.line(135, 392, 135, 540, w="h")
    s.doc(80, 250, 110, 142, mark="tick")
    s.stroke([(530, 540), (530, 420), (720, 420), (720, 540)], "faint", dash=True)
    s.worker(370, 339, look=(1, 0.3), arms=[(540, 344), (540, 386)])
    s.box(536, 292, 130, 98)
    s.rect(975, 420, 170, 120, fill="p")                      # the system, where it is now
    s.hatch(975, 420, 170, 120, gap=24)
    s.arrow(742, 486, 958, 486, "path", dash=True, w="h")
    s.label(860, 372, "the system|moved", "path")
    s.note(700, 120, "builds on a fiction", (712, 408), "point")
    s.label(150, 206, "it exists", "aside")


def lid(s: Sk):
    # a cash box whose padlock is a drawing taped to the front; the worker tries the lid and it lifts.
    # The pack's one page stands beside it with the result stamped across it in capitals
    s.ground(540, 50, 1150, tufts=2)
    s.line(230, 440, 230, 540, w="h")
    s.rect(60, 222, 340, 218, fill="p", tilt=-1)              # the pack: one index page
    s.scribble(88, 244, 284, 84, 3)
    s.rect(72, 348, 316, 74, "point", sw="h", tilt=-5)        # what the check leaves on it
    s.label(230, 404, "NOT ENFORCED", "point", size=54, rot=-5)
    s.table(470, 420, w=380, h=120)
    s.stroke([(520, 304), (520, 420), (770, 420), (770, 304)], "ink")     # the cash box, open at the top
    s.poly([(516, 300), (522, 280), (772, 232), (770, 254)], "ink", fill="p")   # its lid, lifting on the hinge
    for dx in (0, 34):                                        # what is in it
        s.oval(700 + dx, 300, 15, 7)
    s.rect(592, 316, 104, 94, fill="p", tilt=4)               # the padlock, on paper
    s.lock(644, 372, 0.75)
    s.worker(1000, 339, look=(-1, 0.1), arms=[(776, 240), None])
    s.note(810, 120, "the check you run", (780, 222), "aside")
    s.label(660, 500, "$400 cap", "ink")
    s.label(230, 186, "the pack", "ink")


SKETCHES = [
    {"name": "set-down-on-an-outline",
     "idea": "a stale document passes every check for existence, and the next phase builds on what it says",
     "verb": "build on", "prop": "outline where the block used to stand",
     "alt": "A ticked document hangs on a post. A worker lowers a crate onto a dashed outline on the ground. The "
            "solid block that used to stand there is further along.",
     "caption": "A stale document passes every check that asks whether it exists. The next phase starts, then "
                "builds on a fiction.",
     "draw": outline},
]
