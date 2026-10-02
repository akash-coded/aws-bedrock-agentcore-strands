"""Sketches for the lesson on a board for agentic work."""
from pages.sketch import Sk


def skewer(s: Sk):
    # a cake with a "done" flag stuck in it, and the worker drawing a skewer out of it, wet
    s.ground(540, 50, 1150, tufts=2)
    s.table(380, 420, w=420, h=120)
    s.rect(470, 330, 240, 90, fill="p")                         # the cake
    s.curve([(470, 358), (510, 374), (550, 356), (590, 374), (630, 356), (670, 374), (710, 358)], "ink", "t")
    s.sign(548, 330, "done", "aside", post=40)
    s.worker(940, 339, look=(-1, -0.2), arms=[(800, 232), None])
    s.oval(690, 331, 7, 3, fill="ink")                          # the hole it left
    s.line(800, 232, 700, 318)                                  # the skewer
    s.line(730, 292, 700, 318, "point", "h")                    # what came out on it
    s.drop(694, 300, 0.8, "point")
    s.note(250, 150, "someone|said so", (452, 240), "aside")
    s.note(930, 96, "the skewer|says not yet", (742, 280), "point")


def fish(s: Sk, x: float, y: float):
    """A raw fish held up by its tail at ``x, y``, head down."""
    s.oval(x, y + 104, 40, 84, "point", fill="p")
    s.poly([(x, y + 26), (x - 30, y - 8), (x + 30, y - 8)], "point", fill="p")
    s.oval(x + 12, y + 156, 5, 5, "point")
    s.curve([(x - 26, y + 124), (x, y + 138), (x + 26, y + 124)], "point", "t")


def boards(s: Sk):
    # the raw fish comes off the board it shared with the salad and goes onto a board of its own
    s.ground(540, 50, 1150, tufts=2)
    s.table(140, 430, w=680, h=110)
    s.rect(190, 408, 250, 22, fill="p")                         # two chopping boards
    s.rect(540, 408, 250, 22, fill="p")
    s.blob(280, 384, 56, 24, "ink", lumps=7, depth=0.16)        # the salad: leaves and a tomato
    s.blob(318, 372, 44, 22, "ink", lumps=6, depth=0.18)
    s.oval(378, 392, 15, 15, fill="p")
    s.arrow(440, 372, 596, 290, "path", bend=44, dash=True, w="h")
    s.worker(970, 339, look=(-1, 0.1), arms=[(668, 180), None])
    fish(s, 664, 188)
    s.label(270, 290, "a label change", "ink")
    s.note(450, 116, "a money change", (616, 250), "point")
    s.label(640, 506, "its own board", "path", size=54)


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
    s.worker(980, 339, look=(-1, -0.3), arms=[(796, 146), None])
    s.note(440, 110, "building", (598, 250), "aside")
    s.note(206, 400, "review clears|4.5 a day", (544, 492), "ink")
    s.note(960, 84, "the limit goes here", (800, 128), "point")


SKETCHES = [
    {"name": "the-skewer-says-not-yet",
     "idea": "a card moves on evidence, not on someone saying it is done",
     "verb": "draw a skewer out of", "prop": "a cake with a done flag in it",
     "alt": "A cake on a table has a little sign stuck in it that reads done. A worker draws a skewer out of the cake "
            "and it comes out wet.",
     "caption": "\"Done\" because someone said so is status. A card on an agentic board moves on evidence.",
     "draw": skewer},
    {"name": "raw-fish-gets-its-own-board",
     "idea": "lanes are risk bands: a money change never shares a lane with a label change",
     "verb": "lift the raw fish onto", "prop": "a chopping board of its own",
     "alt": "Two chopping boards lie on a table. A salad sits on the first. A worker lifts a raw fish by the tail off "
            "that board and carries it over to the second.",
     "caption": "A card takes the lane of the most dangerous thing it touches, so a money change never shares one with a label change.",
     "draw": boards},
    {"name": "tap-turned-down-to-the-drain",
     "idea": "work-in-progress limits come from what review can clear, not from how fast the building is",
     "verb": "turn down the tap over", "prop": "a sink that drains slowly",
     "alt": "A sink is nearly full. Its tap pours fast and its drain lets out one drop at a time. A worker has a hand on "
            "the tap, turning it down.",
     "caption": "Review cleared 4.5 slots a day at SkyWays. The limit goes on what enters the build, to match what review can clear.",
     "draw": sink},
]
