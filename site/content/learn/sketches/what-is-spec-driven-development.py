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


SKETCHES = [
    {"name": "the-drawing-goes-back-on-the-wall",
     "idea": "spec-first throws the spec away when the code is done; spec-anchored keeps it, and it outlives the code",
     "verb": "pin back up", "prop": "drawing above the workbench",
     "alt": "A finished birdhouse stands on a bench. One drawing of it lies crumpled in a bin. A worker pins another "
            "copy back on the wall above the bench.",
     "caption": "Spec-first throws the spec away when the task is done. Spec-anchored keeps it and changes it with "
                "the feature, on every change.",
     "draw": pinned},
]
