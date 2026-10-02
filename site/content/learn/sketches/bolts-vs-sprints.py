"""Sketches for the lesson on bolts and sprints."""
from pages.sketch import Sk


def shaker(s: Sk, x: float, y: float, k: int):
    """A shaker held upside down at ``x, y``, pouring; ``k`` leans it toward the bowl."""
    s.rect(x - 24, y - 44, 48, 80, fill="p", tilt=k * 8)
    s.line(x - 30 - k * 4, y + 38, x + 30 - k * 4, y + 38, w="h")       # its cap, underneath
    for i in range(5):
        gx = x - k * 4 + (9 if i % 2 else -8)
        s.line(gx, y + 58 + i * 38, gx + 1, y + 72 + i * 38, w="t")


def two_shakers(s: Sk):
    # two new things shaken into one bowl at once: when it goes wrong, nothing says which did it
    s.worker(600, 256, look=(0, 0.9), arms=[(432, 150), (768, 150)], legs="none")
    shaker(s, 418, 136, 1)
    shaker(s, 782, 136, -1)
    s.poly([(330, 396), (870, 396), (800, 560), (400, 560)], fill="p")            # the bowl, in front
    s.oval(600, 396, 270, 20, fill="p")
    s.label(232, 250, "one unknown", "ink")
    s.label(980, 250, "and a second", "ink")
    s.label(600, 506, "which one failed?", "point")


SKETCHES = [
    {"name": "two-shakers-one-bowl",
     "idea": "a bolt with two unknowns cannot tell you which one failed",
     "verb": "shake in two at once", "prop": "two shakers over one mixing bowl",
     "alt": "A worker stands behind a big mixing bowl with a shaker in each raised hand, tipping both in at once. "
            "On the bowl is written: which one failed?",
     "caption": "Put two unknowns in one bolt and a failure cannot tell you which of them it was.",
     "draw": two_shakers},
]
