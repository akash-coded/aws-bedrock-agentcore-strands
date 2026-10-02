"""Sketches for the lesson on spec-driven development."""
from pages.sketch import Sk


def birdhouse(s: Sk, x: float, y: float, w: float, h: float, wt: str = ""):
    """A birdhouse standing at ``x, y`` (its bottom left): the thing that got built."""
    s.poly([(x, y), (x, y - h * 0.62), (x + w / 2, y - h), (x + w, y - h * 0.62), (x + w, y)], "ink", fill="p", w=wt)
    s.oval(x + w / 2, y - h * 0.42, w * 0.13, w * 0.13, "ink", w=wt)


def pinned(s: Sk):
    # the thing is built and on the bench; one drawing of it is in the bin, and the worker pins the other
    # back on the wall above the bench
    s.ground(540, 50, 1150, tufts=2)
    s.bucket(170, 540, 130, 130)
    s.blob(172, 404, 46, 30, lumps=6, depth=0.22)               # a crumpled sheet
    s.table(400, 420, w=400, h=120)
    birdhouse(s, 440, 420, 124, 150)
    s.rect(590, 120, 150, 180, fill="p", tilt=2)                # the drawing, on the wall
    birdhouse(s, 630, 268, 70, 92, "t")
    s.oval(665, 134, 6, 6, "point", fill="point")               # the pin
    s.worker(950, 339, look=(-1, -0.4), arms=[(744, 142), None])
    s.note(190, 250, "spec first:|thrown away", (172, 362), "ink")
    s.label(380, 104, "spec anchored:|kept", "aside")
    s.label(905, 92, "survives|the code", "point")
    s.arrow(806, 118, 752, 150, "point", w="t", head=15)


def form(s: Sk):
    # the tool has printed a tall form; the top of it is filled, and five boxes lower down are empty.
    # The worker writes in one of them
    s.ground(540, 50, 1150, tufts=2)
    s.bot(200, 447, 1.6, look=(1, -0.3))
    s.rect(440, 80, 320, 460, fill="p", tilt=-1)
    s.scribble(470, 104, 260, 110, 3)
    for i in range(5):
        s.rect(470, 240 + i * 56, 260, 40, "point", sw="t")
    s.scribble(482, 362, 150, 20, 1, pen="ink")                 # the first words going in
    s.worker(960, 339, look=(-1, 0.2), arms=[(784, 388), None])
    s.stroke([(784, 388), (694, 374)], "ink", "h")              # the pencil
    s.route([(290, 430), (360, 404), (428, 412)], "path")
    s.label(225, 180, "the tool gives|the boxes", "aside")
    s.label(965, 120, "five are yours", "point")
    s.arrow(880, 142, 748, 246, "point", w="t", head=15, bend=-16)


SKETCHES = [
    {"name": "the-drawing-goes-back-on-the-wall",
     "idea": "spec-first throws the spec away when the code is done; spec-anchored keeps it, and it outlives the code",
     "verb": "pin back up", "prop": "drawing above the workbench",
     "alt": "A finished birdhouse stands on a bench. One drawing of it lies crumpled in a bin. A worker pins another "
            "copy back on the wall above the bench.",
     "caption": "Spec-first throws the spec away when the task is done. Spec-anchored keeps it and changes it with "
                "the feature, on every change.",
     "draw": pinned},
    {"name": "the-tool-prints-the-boxes",
     "idea": "a spec tool gives you places to write; the five agentic fields are blanks only the team can fill",
     "verb": "fill in", "prop": "printed form with five empty boxes",
     "alt": "A small machine has printed a tall form. Its top lines are filled in and five boxes below are empty. "
            "A worker writes in one of the empty boxes with a long pencil.",
     "caption": "A spec tool gives you the places to write things down. The model's role, autonomy, the bar, the "
                "fallback and the records are yours to fill.",
     "draw": form},
]
