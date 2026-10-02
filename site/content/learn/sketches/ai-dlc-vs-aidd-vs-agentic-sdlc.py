"""Sketches for the lesson that sorts AI-DLC, AIDD, the agentic SDLC and the PDLC."""
from pages.sketch import Sk


def inside(s: Sk):
    # one machine nails the crate shut from outside; a second one is looking out of it. The worker
    # holds a magnifying glass over the one inside, which is the one nobody has checked
    s.ground(540, 50, 1150, tufts=2)
    s.bot(215, 447, 1.6, look=(1, 0))
    s.stroke([(290, 436), (436, 386)], "aside")                # its arm, and a hammer on the crate's side
    s.rect(428, 356, 24, 58, "aside", fill="p", tilt=-18)
    s.bot(600, 372, 1.25, look=(1, -0.3))
    s.rect(460, 392, 280, 148, fill="p")                       # the crate, over the one inside
    s.line(460, 442, 740, 442, w="t")
    s.line(460, 492, 740, 492, w="t")
    hx, hy = s.magnifier(612, 360, 58)
    s.worker(950, 339, look=(-1, 0.1), arms=[(hx, hy), None])
    s.note(215, 190, "AI builds it", (220, 312), "aside")
    s.note(590, 110, "AI is inside it", (600, 270), "aside")
    s.note(960, 100, "how right|must it be?", (690, 318), "point")


SKETCHES = [
    {"name": "the-builder-and-the-one-inside",
     "idea": "most projects have AI twice: one builds the product, one is inside it; a building method covers only the first",
     "verb": "inspect", "prop": "crate with a second machine inside",
     "alt": "A small machine nails a crate shut from the outside. A second machine looks out of the crate. A worker "
            "holds a magnifying glass over the one inside.",
     "caption": "Most projects are both: a coding agent builds the product, and the product calls a model. A "
                "building method covers only the first.",
     "draw": inside},
]
