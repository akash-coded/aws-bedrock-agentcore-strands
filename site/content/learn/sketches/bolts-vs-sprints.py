"""Sketches for the lesson on bolts and sprints."""
from pages.sketch import Sk


def hang(s: Sk):
    # a door is not a door until it hangs in its frame: the worker carries today's door to the empty doorway
    s.ground(540, 50, 1150, tufts=2)
    s.stroke([(900, 540), (900, 230), (1070, 230), (1070, 540)], "ink", "h")      # the doorway, empty
    s.oval(906, 300, 5, 9)                                      # its hinges, waiting
    s.oval(906, 470, 5, 9)
    s.worker(250, 339, look=(1, 0), arms=[None, (420, 360)], legs="walk")
    s.rect(420, 252, 150, 282, fill="p", tilt=7)                # the door, on its way
    s.oval(538, 392, 7, 7, fill="ink")
    s.arrow(630, 380, 872, 380, "path", dash=True, w="h")
    s.note(520, 110, "built today", (500, 244), "ink")
    s.note(960, 100, "not in:|not happened", (986, 300), "point")
    s.label(750, 446, "in by|tonight", "path")


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


def pipes(s: Sk):
    # the bare pipes, joined end to end before any wall goes up: the worker pours a bucket through, and the joint that leaks shows now
    s.ground(540, 50, 1150, tufts=2)
    s.worker(190, 339, look=(1, -0.2), arms=[None, (340, 196)])
    s.poly([(318, 140), (336, 226), (402, 212), (398, 124)], fill="p", w="h")     # a bucket, tipped
    s.drop(418, 240, 1.0)
    s.drop(426, 284, 1.0)
    s.stroke([(380, 300), (420, 340), (460, 300)], "ink", "h")  # the mouth of the pipe
    s.pipe([(420, 340), (420, 440), (930, 440), (930, 486)], r=17)
    s.rect(640, 416, 30, 48, fill="p")                          # the joint
    s.curve([(655, 414), (670, 344), (716, 318)], "point")      # and its leak
    s.drop(738, 330, 0.9, "point")
    s.drop(712, 368, 0.8, "point")
    s.bucket(930, 540, 110, 44, level=0.5)
    s.drop(930, 500, 0.7)
    s.label(470, 130, "just the pipes", "ink", anchor="start")
    s.label(800, 204, "found on day one", "point")
    s.arrow(670, 222, 712, 300, "point", bend=-12, w="t", head=15)
    s.label(1140, 292, "not day fourteen", "aside", anchor="end")


SKETCHES = [
    {"name": "a-door-is-not-a-door-until-hung",
     "idea": "a bolt that is built but not integrated has not happened",
     "verb": "carry to its frame", "prop": "a door built today and an empty doorway",
     "alt": "A worker carries a finished door toward an empty doorway whose hinges are waiting. Until the door hangs "
            "there, the doorway is a hole.",
     "caption": "A bolt that is built but not integrated has not happened. The integration deadline is part of the cadence.",
     "draw": hang},
    {"name": "two-shakers-one-bowl",
     "idea": "a bolt with two unknowns cannot tell you which one failed",
     "verb": "shake in two at once", "prop": "two shakers over one mixing bowl",
     "alt": "A worker stands behind a big mixing bowl with a shaker in each raised hand, tipping both in at once. "
            "On the bowl is written: which one failed?",
     "caption": "Put two unknowns in one bolt and a failure cannot tell you which of them it was.",
     "draw": two_shakers},
    {"name": "water-through-the-bare-pipes",
     "idea": "the walking skeleton proves the pieces connect on day one, before anything is built round them",
     "verb": "pour a bucket through", "prop": "bare pipes before the walls go up",
     "alt": "A worker tips a bucket of water into a run of bare pipe with no walls around it. Water comes out of the "
            "far end into a bucket, and one joint in the middle squirts a leak.",
     "caption": "The walking skeleton is the pipes with no walls: run something through on day one and the joint that leaks shows now.",
     "draw": pipes},
]
