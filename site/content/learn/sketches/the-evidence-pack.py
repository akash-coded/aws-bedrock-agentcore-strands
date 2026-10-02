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
