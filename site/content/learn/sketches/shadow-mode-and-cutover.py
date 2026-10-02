"""Sketches for the lesson on shadow mode and cut-over."""
from pages.sketch import Sk


def tracks(s: Sk):
    # two tracks across open ground: the desk's, and the agent's dashed one beside it. They part once, where
    # the desk walks round something that is not on any map; the worker plants a sign there
    s.curve([(60, 356), (300, 352), (480, 354), (600, 412), (720, 456), (840, 412), (960, 354), (1140, 348)], "ink", "h")
    s.curve([(60, 328), (400, 326), (720, 328), (1140, 322)], "aside", "h", True)
    s.sign(720, 330, "closed|after 18:00", "point", post=100, size=54)
    s.worker(1000, 220, look=(-1, 0.3), arms=[(726, 260), (732, 302)], lean=-7)
    s.label(70, 280, "the agent, in shadow", "aside", anchor="start")
    s.label(120, 424, "the desk", "ink", anchor="start")
    s.note(370, 516, "fourteen cases part here", (490, 374), "point")


def rain(s: Sk):
    # the machine has only ever been out under the roof; the worker wheels it out into the weather on purpose
    s.ground(540, 50, 1150, tufts=2)
    s.poly([(50, 222), (420, 192), (420, 176), (50, 206)], fill="p")             # the roof, and its posts
    s.hatch(60, 196, 350, 14, gap=30)
    s.line(88, 214, 88, 540)
    s.line(392, 192, 392, 540)
    s.worker(230, 339, look=(1, 0.1), arms=[(426, 424), (432, 398)], legs="walk", lean=8)
    s.stroke([(450, 496), (432, 396)], "ink", "h")           # the trolley
    s.rect(450, 490, 190, 14, fill="p")
    s.oval(484, 522, 16, 16, fill="p")
    s.oval(606, 522, 16, 16, fill="p")
    s.bot(545, 404, 1.45, look=(1, -0.3))
    s.cloud(970, 232, 300, 130, "ink")
    for x, y in ((896, 330), (960, 350), (1034, 326), (1094, 360), (920, 420), (996, 430), (1064, 446)):
        s.drop(x, y, 1.0)
    s.arrow(690, 446, 812, 446, "path", dash=True, w="h")
    s.label(756, 404, "on purpose", "path")
    s.label(262, 100, "a normal Tuesday,|many times", "ink")
    s.label(960, 70, "a storm day,|perhaps once", "point")


SKETCHES = [
    {"name": "where-the-two-tracks-part",
     "idea": "a shadow run lays the agent's decisions beside the desk's; where they part is a rule nobody wrote down",
     "verb": "plant a sign", "prop": "two tracks that part once",
     "alt": "Two tracks run side by side across open ground, one solid and one dashed. At one place the solid track "
            "swings wide and the dashed one goes straight on. A worker plants a sign there: closed after 18:00.",
     "caption": "The shadow run and the desk parted on fourteen cases, all for one rule nobody had written down. "
                "Finding it cost nothing.",
     "h": 560, "draw": tracks},
    {"name": "wheel-it-out-into-the-rain",
     "idea": "more of the same traffic is not new evidence; widen into the conditions the agent has not met",
     "verb": "wheel out", "prop": "trolley under a roof and a rain cloud",
     "alt": "A worker pushes a small machine on a trolley out from under a roof toward a rain cloud.",
     "caption": "Six weeks at 5% shows a normal Tuesday many times and a storm day perhaps once. Widen into the "
                "conditions you have not seen.",
     "draw": rain},
]
