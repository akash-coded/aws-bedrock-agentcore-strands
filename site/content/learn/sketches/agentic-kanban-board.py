"""Sketches for the lesson on a board for agentic work."""
from pages.sketch import Sk


def sink(s: Sk):
    # a sink that drains slowly: the worker turns the tap down to what the drain can clear
    s.ground(540, 50, 1150, tufts=2)
    s.stroke([(400, 290), (424, 450), (716, 450), (740, 290)], "ink", "h")        # the basin
    s.line(440, 450, 436, 540)
    s.line(700, 450, 704, 540)
    s.curve([(406, 314), (500, 320), (640, 310), (734, 314)], "aside")            # nearly full
    s.curve([(450, 340), (520, 346), (590, 338)], "aside", "t")
    s.stroke([(760, 292), (760, 170), (620, 170), (620, 204)], "ink", "h")        # the tap
    s.line(760, 170, 760, 148, w="h")
    s.line(728, 146, 792, 146, w="h")
    s.line(612, 210, 612, 304, "aside", "h")                    # what it pours
    s.line(628, 210, 628, 304, "aside", "h")
    s.line(560, 450, 560, 484)                                  # the drain
    s.line(582, 450, 582, 484)
    s.drop(571, 512, 0.7)
    s.worker(960, 339, look=(-1, -0.5), arms=[(792, 146), (764, 262)], lean=-8)
    s.note(430, 110, "building", (598, 250), "aside")
    s.note(210, 400, "review:|4.5 a day", (544, 492), "ink")
    s.note(900, 76, "the limit goes here", (770, 122), "point", bend=-10)


SKETCHES = [
    {"name": "tap-turned-down-to-the-drain",
     "idea": "work-in-progress limits come from what review can clear, not from how fast the building is",
     "verb": "turn down the tap over", "prop": "a sink that drains slowly",
     "alt": "A sink is nearly full. Its tap pours fast and its drain lets out one drop at a time. A worker steadies the pipe with one hand "
            "and turns the tap down with the other.",
     "caption": "Review cleared 4.5 slots a day at SkyWays. The limit goes on what enters the build, to match what review can clear.",
     "draw": sink},
]
