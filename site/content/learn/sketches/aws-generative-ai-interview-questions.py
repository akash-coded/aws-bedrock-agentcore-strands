"""Sketch for the AWS generative AI question bank."""
from pages.sketch import Sk


def badge(s: Sk, x: float, y: float, w: float, h: float, front: bool = True, tilt: float = 0.0) -> None:
    """A name badge hanging from the line above it, its top left at ``x, y``."""
    s.line(x + w / 2, y - 62, x + w / 2, y, w="t")
    s.rect(x, y, w, h, fill="p", tilt=tilt)
    if front:
        s.rect(x, y, w, 30, fill="ink", tilt=tilt)


def flip(s: Sk):
    # three name badges on a line: two show the names a candidate can recite; the worker has turned the
    # third one over, and the back is where the question is
    s.ground(540, 50, 1150, tufts=0)
    s.string(50, 120, 980, 124, sag=22)
    badge(s, 66, 196, 222, 170)
    badge(s, 326, 200, 222, 170)
    badge(s, 596, 196, 322, 190, front=False, tilt=-3)
    s.worker(1066, 339, look=(-1, -0.1), arms=[(922, 318), None])
    s.label(177, 316, "Runtime", "ink")
    s.label(437, 320, "Gateway", "ink")
    s.label(757, 284, "what bills|while idle?", "point")
    s.label(400, 462, "the interview|reads the back", "path")
    s.arrow(616, 470, 726, 404, "path", bend=-30, dash=True, w="h")


SKETCHES = [
    {"name": "the-back-of-the-name-badge",
     "idea": "naming the service is the front of the badge; the interview asks what is on the back",
     "verb": "turn over", "prop": "name badge",
     "alt": "Three name badges hang on a line. Two show service names, Runtime and Gateway. A worker has turned the "
            "third one over, and its back carries a question in red: what bills while idle?",
     "caption": "Naming the service is the front of the badge. The interview asks about the back: what bills "
                "while idle, what cannot be changed, where it stops.",
     "draw": flip},
]
