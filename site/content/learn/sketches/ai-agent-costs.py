"""Sketches for the lesson on why the bill is four times the estimate."""
from pages.sketch import Sk


def trap(s: Sk):
    # an alarm bell rings on top of the cache because its answers come back too fast; the worker has a hand
    # on the plug
    s.ground(540, 50, 1150, tufts=2)
    s.curve([(60, 534), (330, 530), (590, 530), (660, 480), (690, 416)], "ink")   # the flex
    s.rect(770, 320, 240, 220, fill="p")                     # the cache
    s.rect(752, 380, 18, 60, fill="p")
    s.rect(690, 392, 40, 36, fill="ink")                     # its plug, half out
    s.line(730, 402, 748, 402)
    s.line(730, 418, 748, 418)
    s.stroke([(840, 318), (846, 262), (890, 236), (934, 262), (940, 318)], "ink", "h")   # the bell
    s.line(826, 318, 954, 318, w="h")
    s.burst(890, 256, r=60, n=5, pen="point")
    s.worker(440, 339, look=(1, 0.2), arms=[None, (694, 408)], lean=-6)
    s.label(890, 448, "cache,|working", "aside")
    s.note(1150, 150, "suspiciously fast", (950, 236), "point", anchor="end")
    s.note(520, 96, "bill up about a third", (702, 380), "point")


SKETCHES = [
    {"name": "the-alarm-was-the-cache",
     "idea": "a cache hit looks like a fault to a latency alarm, and switching the cache off puts the bill up",
     "verb": "pull the plug on", "prop": "alarm bell on top of the cache",
     "alt": "A box marked cache has an alarm bell ringing on top of it. A worker has a hand on its plug and is pulling "
            "it out of the socket.",
     "caption": "Cache hits come back fast, so a latency alarm flags them as failures. Switch the cache off and the "
                "bill rises by about a third.",
     "draw": trap},
]
