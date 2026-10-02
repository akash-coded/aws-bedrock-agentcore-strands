"""Sketch for the AWS generative AI question bank."""
from pages.sketch import Sk


def lanyard(s: Sk, x: float, y: float, top: float, twist: bool = False) -> None:
    """The cord a badge hangs by: from a rail at ``top`` down to the clip at ``x, y``."""
    for k in (-1, 1):
        s.stroke([(x + k * 40, top), (x + (-k if twist else k) * 6, y - 16)], "ink", "t")
    s.rect(x - 12, y - 18, 24, 18, fill="p")


def flip(s: Sk):
    # two name badges on a rail: one shows the name a candidate can recite; the worker has turned the other
    # over with both hands, and the back is where the question is
    s.ground(560, 50, 1150, tufts=0)
    s.line(60, 96, 900, 100, w="h")
    lanyard(s, 235, 214, 98)
    s.rect(120, 214, 230, 206, fill="p")                                    # the front: a photo and a name
    s.rect(120, 214, 230, 30, fill="ink")
    s.rect(206, 258, 58, 62)
    s.oval(235, 280, 10, 11, w="t")
    s.curve([(214, 318), (235, 298), (256, 318)], "ink", "t")
    s.label(235, 392, "Runtime", "ink", size=56)
    lanyard(s, 680, 190, 100, twist=True)
    s.rect(516, 190, 336, 236, fill="p", tilt=-4, sw="h")                   # the back, turned to face us
    s.label(684, 300, "what bills|while idle?", "point", rot=-4)
    s.worker(1020, 345, look=(-1, -0.1), arms=[(856, 228), (852, 404)], lean=-6)
    s.label(300, 484, "interviews read|the back", "path")
    s.arrow(476, 500, 596, 440, "path", bend=-24, dash=True, w="h")


SKETCHES = [
    {"name": "the-back-of-the-name-badge",
     "idea": "naming the service is the front of the badge; the interview asks what is on the back",
     "verb": "turn over", "prop": "name badge",
     "alt": "Two name badges hang from a rail. One shows a photo and a service name, Runtime. A worker has turned the "
            "other over with both hands, and its back carries a question in red: what bills while idle?",
     "caption": "Naming the service is the front of the badge. The interview asks about the back: what bills "
                "while idle, what cannot be changed, where it stops.",
     "draw": flip},
]
