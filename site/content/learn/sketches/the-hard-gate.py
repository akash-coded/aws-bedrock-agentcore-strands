"""Sketches for the lesson on the one hard gate."""
from pages.sketch import Sk


def tokens(s: Sk):
    # a turnstile that takes three tokens: two are in, the worker is patting itself down for the third
    s.ground(540, 50, 1150, tufts=3)
    arm = s.turnstile(620, 540, h=210)
    s.rect(470, 300, 90, 190, fill="p")                     # the coin box, three slots
    for i, filled in enumerate((True, True, False)):
        s.rect(486, 322 + i * 54, 58, 16, fill="ink" if filled else "p")
    s.ring(515, 438, 48, 26)
    s.worker(250, 339, look=(1, 0.4), arms=[(200, 390), (436, 430)])
    s.rect(900, 250, 220, 290, fill="p")                    # the workshop behind it, shuttered
    for i in range(1, 6):
        s.line(900, 250 + i * 48, 1120, 250 + i * 48, w="t")
    s.note(300, 110, "spec, bar,|budget", (500, 316), "ink")
    s.note(690, 140, "third one missing", (540, 420), "point")
    s.label(1010, 210, "build", "aside")
    s.route([(100, 590), (430, 578), (700, 588)], "path")


def standin(s: Sk):
    # a cardboard box standing where the oven will go, and the cabinet being built tight against it
    s.ground(540, 50, 1150, tufts=2)
    s.rect(120, 250, 200, 290, fill="p")                    # a finished cabinet
    s.line(120, 395, 320, 395, w="t")
    s.box(330, 340, 200, 200)                               # the stand-in, the right size
    s.tag(500, 344)
    s.rect(540, 250, 200, 290, fill="p")                    # the cabinet going in beside it
    s.line(540, 395, 740, 395, w="t")
    s.worker(890, 339, look=(-1, 0.1), arms=[(748, 330), None])
    s.stroke([(748, 330), (716, 300)], "ink", "h")          # a screwdriver, at the cabinet's edge
    s.doc(1030, 180, 96, 120, tilt=8, lines=2)              # the other kind of placeholder: a note taped to the air
    s.note(420, 150, "a stub with|an owner", (430, 330), "aside")
    s.note(1040, 120, "a sentence", (1078, 172), "point")
    s.route([(130, 590), (480, 580), (760, 590)], "path")


SKETCHES = [
    {"name": "three-tokens-one-way",
     "idea": "one crossing halts the build; it opens on three signed things",
     "verb": "feed tokens", "prop": "turnstile with a coin box",
     "alt": "A worker stands at a turnstile that takes three tokens. Two slots are filled and the third is ringed in red. "
            "The worker is patting itself down for the missing one. Behind the turnstile a workshop is shuttered.",
     "caption": "The build starts when all three are signed: the spec, the bar for each kind of case, and what the agent may do alone.",
     "draw": tokens},
    {"name": "a-stand-in-the-right-size",
     "idea": "a soft decision is safe only behind a real placeholder the build can be fitted around",
     "verb": "build around", "prop": "cardboard box in a kitchen",
     "alt": "A worker screws a cabinet tight against a cardboard box that stands where the oven will go. The box has a "
            "luggage tag on it. Further along, a note is taped to the air where another gap should be.",
     "caption": "A real placeholder is a working stub with an owner and a date. A sentence is not one.",
     "draw": standin},
]
