"""The home page's tutorial band: four people from the game's team, each with one question.

:func:`band` builds the band (verdict-home 1.5). Priya, Arjun, Sam and Maya are the fictional airline's team
in the simulator (``play/days.json``), so a reader meets them again one band later. Each asks one real
question and gets the manual's answer in one sentence, beside a card-sized drawing of the sketches' small
worker, cut from a lesson's sketch. The whole card is one link, to the lesson that answers the question;
never to a role page, because the roles band above is the page's one routing device. Every number comes
from the lessons.

:func:`check` holds the band to its lessons when the site is built: each answer is lifted from a sentence
its lesson still says, word for word, and has 24 words or fewer; each drawing keeps the worker and two
labels of five words or fewer, written large enough for 13px on the narrowest card; the four drawings
together stay inside their bytes.
"""
from __future__ import annotations

import gzip
import json
import math
import re
from html import escape as _E

HAND = 64          # handwriting on a card, in sheet units: 15.5px on a 292px card at 1440, 14.9px on 280px at 320
HAND_MIN = 56      # 13px on the narrowest card (280px, on a 320px phone)
ANSWER_MAX = 24    # words


# ---------------------------------------------------------------------------------------------- the drawings
# Each is a card-sized cut of a lesson's sketch (content/learn/sketches/): the worker doing the verb, one
# prop, two labels at most, on a sheet 1200 by 500. A full lesson sketch on each card would cost about twice
# the bytes and carry labels that need their paragraph.

def _crow(s, x: float, y: float, k: float = 1.0) -> None:
    s.curve([(x - 34 * k, y - 6 * k), (x - 14 * k, y - 20 * k), (x, y)], "ink")
    s.curve([(x, y), (x + 16 * k, y - 22 * k), (x + 36 * k, y - 8 * k)], "ink")


def priya(s) -> None:
    """From the executives lesson's a-scarecrow-would-do: the worker plants a scarecrow, and the machine
    that was asked for flaps at the crow beside it."""
    s.ground(480, 60, 1140, tufts=0)
    s.worker(250, 279, look=(1, -0.1), arms=[None, (490, 340)], lean=4)      # her hand on the pole
    x, y = 500, 480
    s.line(x, y, x, y - 300, w="h")
    s.line(x - 104, y - 214, x + 104, y - 214, w="h")
    s.oval(x, y - 262, 36, 36, fill="p")
    s.stroke([(x - 56, y - 292), (x + 56, y - 292)], "ink", "h")
    s.poly([(x - 30, y - 292), (x - 20, y - 338), (x + 22, y - 338), (x + 30, y - 292)], fill="p")
    s.bot(930, 386, 1.5, look=(0.4, -0.8))
    for k in (-1, 1):
        s.stroke([(930 + k * 70, 380), (930 + k * 112, 324), (930 + k * 100, 270)], "aside")
    _crow(s, 1090, 110, 0.9)
    s.note(760, 78, "a rule does this better", (556, 138), "point", size=HAND)


def arjun(s) -> None:
    """From the architects' lesson's one-on-stage-the-rest-wait: one machine on the stage, two waiting at the
    steps, and the worker barring the way until one can name the limit it is there for."""
    s.ground(480, 50, 620, tufts=0)
    s.rect(612, 422, 68, 58)
    s.line(680, 360, 1150, 360, w="h")
    s.line(680, 360, 680, 480)
    for x in (120, 250):
        w, h = 84, 72
        s.rect(x - w / 2, 422 - h / 2, w, h, "aside", fill="p")
        s.oval(x + 7, 417, 13, 13, "aside")
        for dx in (-22, 22):
            s.stroke([(x + dx, 458), (x + dx, 478)], "aside")
    s.bot(930, 273, 1.5, look=(-1, 0.3))
    s.worker(486, 279, look=(-1, 0.3), arms=[(330, 262), (642, 266)], lean=-6)
    s.label(250, 80, "why a second one?", "point", size=HAND)
    s.label(1010, 96, "start with one", "ink", size=HAND)


def sam(s) -> None:
    """From the guardrails lesson's a-notice-where-the-valve-should-be: a notice says the limit where the
    valve should be, the worker's hands close on nothing, and the money runs out of the far end. The lesson's
    own label, "nothing here refuses", needs its paragraph; this one names the picture."""
    s.ground(480, 50, 1150, tufts=0)
    s.pipe([(60, 150), (880, 150), (912, 182), (912, 250)], r=20)
    ring = [(480 + 54 * math.cos(i * math.pi / 8), 148 + 54 * math.sin(i * math.pi / 8)) for i in range(16)]
    s.stroke(ring, "point", "", closed=True, dash=True, raw=True)
    s.line(646, 172, 652, 232, w="t")
    s.line(814, 172, 808, 232, w="t")
    s.rect(600, 232, 260, 96, fill="p", tilt=2)
    s.label(730, 298, "limit $400", "ink", rot=2, note=False, size=HAND)
    for x, y in ((910, 300), (902, 372)):
        s.coin(x, y, 22)
    s.stack(912, 470, 3, 110)
    s.worker(312, 297, 1.82, look=(1, -0.4), arms=[(428, 152), (488, 196)], lean=10)
    s.label(250, 64, "a notice, not a valve", "point", size=HAND, anchor="start")
    s.arrow(560, 76, 520, 102, "point", w="t", head=15)


def maya(s) -> None:
    """From the accuracy lesson's four-pebbles-one-rock: a plank over a log, a rock on one end, and the
    worker lowering the fourth pebble onto the other."""
    s.ground(480, 50, 1150, tufts=0)
    left, right = s.seesaw(640, 480, w=620, tip=0.0)
    s.rock(right[0] - 70, right[1], 150, 120)
    for i in range(3):
        s.pebble(left[0] + 50 + i * 52, left[1], 24)
    s.worker(200, 279, look=(1, 0.3), arms=[None, (left[0] + 206, left[1] - 40)])
    s.pebble(left[0] + 206, left[1] - 24, 24)
    s.note(1000, 120, "1 wrong: $36", (right[0] - 70, right[1] - 130), "point", size=HAND)
    s.note(560, 96, "4 right x $9", (left[0] + 110, left[1] - 50), "aside", size=HAND)


# ---------------------------------------------------------------------------------------------- the people
# In the lifecycle's order: a P0 question, a P1 question, then two from P2. ``who`` is the person's key in the
# game's cast, which gives the name and the job. ``answer`` is the card's sentence, at most 24 words, and
# ``source`` the sentence of ``lesson`` it is lifted from, which the build must find there. ``cut`` names the
# lesson sketch the drawing is cut from.
PEOPLE = (
    {"who": "priya", "ask": "Should this be an agent at all?",
     "answer": "Three questions settle it, cheapest first. Expect two or three of your top five requests to come "
               "back as rules, not agents.",
     "lesson": "p0-frame",
     "source": "Expect two or three of your top five requests to come back as rules.",
     "cut": "a-scarecrow-would-do", "draw": priya,
     "alt": "Priya plants a scarecrow in a field. Beside it a small machine with one eye flaps its arms at a crow."},
    {"who": "arjun", "ask": "One agent or several?",
     "answer": "Start with one. Add another only when you can name the limit that forces it.",
     "lesson": "agentic-pdlc-for-solution-architects",
     "source": "Start with a single agent and add another only when you can name the limit that forces it",
     "cut": "one-on-stage-the-rest-wait", "draw": arjun,
     "alt": "One small machine stands on a stage. Two more wait at the steps, and Arjun spreads both arms to bar "
            "the way."},
    {"who": "sam", "ask": "Can we put the refund limit in the prompt?",
     "answer": "Not on its own. A prompt only lowers the odds of crossing a limit; the tool's code closes the path.",
     "lesson": "ai-guardrails-that-hold",
     "source": "A limit an AI agent reads in its prompt only lowers the probability of crossing it; a limit "
               "enforced in the tool it calls closes the path entirely",
     "cut": "a-notice-where-the-valve-should-be", "draw": sam,
     "alt": "A notice reading limit $400 hangs from a pipe where a valve should be. Sam reaches for the valve "
            "that is not there, and coins pour out of the far end."},
    {"who": "maya", "ask": "How accurate does it need to be?",
     "answer": "As accurate as the money says. Where a wrong answer costs four times what a right one saves, the "
               "bar is 80%.",
     "lesson": "how-accurate-must-an-ai-agent-be",
     "source": "80% where it costs four times as much",
     "cut": "four-pebbles-one-rock", "draw": maya,
     "alt": "A plank balances on a log with a rock on one end. Maya lowers a fourth pebble onto the other end, "
            "and the plank comes level."},
)


def drawings() -> dict:
    """The four sheets, by person: ``{who: (Sk, svg)}``."""
    from pages.sketch import Sk
    out = {}
    for p in PEOPLE:
        s = Sk("home-" + p["who"], p["alt"], 500)
        p["draw"](s)
        out[p["who"]] = (s, s.svg())
    return out


def _flat(md: str) -> str:
    """A lesson's words on one line: no blockquote marks, every run of white space one space."""
    return " ".join(re.sub(r"(?m)^[ \t]*>[ \t]?", "", md).split())


def check(lessons: dict, cast: dict, pics: dict) -> list[str]:
    """What the band must keep to. Returns the problems; an empty list is a pass."""
    from pages import learn, sketch
    out = []
    for p in PEOPLE:
        who = p["who"]
        if who not in cast:
            out.append(f"{who}: not in the game's cast (play/days.json)")
        les = lessons.get(p["lesson"])
        if les is None:
            out.append(f"{who}: there is no lesson {p['lesson']}")
        elif " ".join(p["source"].split()) not in _flat(les.body):
            out.append(f"{who}: lessons/{p['lesson']}.md no longer says \"{p['source']}\", the sentence the "
                       f"card's answer is lifted from; change the answer with the lesson")
        n = len(p["answer"].split())
        if n > ANSWER_MAX:
            out.append(f"{who}: the answer has {n} words; {ANSWER_MAX} at most")
        if p["cut"] not in learn.sketches():
            out.append(f"{who}: the drawing is cut from {p['cut']}, which is no lesson's sketch")
        s, svg = pics[who]
        if len(s.words) > 2:
            out.append(f"{who}: the drawing has {len(s.words)} labels; two at most")
        for text, size in s.words:
            if len(sketch.WORD.findall(text)) > 5:
                out.append(f"{who}: the label '{text}' has more than five words")
            if size < HAND_MIN:
                out.append(f"{who}: the label '{text}' is written at {size}; {HAND_MIN} is 13px on a 280px card")
        if 'class="zB"' not in svg:
            out.append(f"{who}: the drawing has no worker; the worker does the thing it is about")
    # Bytes, gzipped together as the page carries them. 7 KB with path data written from the point before
    # (verdict-home H9); until that writer lands, the absolute paths are held to 10 KB.
    both = "".join(svg for _s, svg in pics.values())
    size = len(gzip.compress(both.encode("utf-8"), 9))
    cap = 7 if re.search(r'\sd="[^"]*[a-z]', both) else 10
    if size > cap * 1024:
        out.append(f"the four drawings are {size:,} bytes gzipped together; the budget is {cap} KB (fewer strokes)")
    return out


def _job(title: str) -> str:
    """The cast's job title as it reads after a name: "Product manager" becomes "product manager", and
    "QA lead" keeps its capitals."""
    return title[:1].lower() + title[1:] if title[1:2].islower() else title


def band() -> str:
    """The home page's fifth band (verdict-home 1.5)."""
    import render
    from pages import learn
    _meta, tracks, lessons = learn.load()
    cast = json.loads((learn.SITE / "play" / "days.json").read_text(encoding="utf-8"))["cast"]
    pics = drawings()
    problems = check(lessons, cast, pics)
    if problems:
        raise SystemExit("the home page's tutorial band (pages/people.py):\n  " + "\n  ".join(problems))
    first = tracks[0].lessons[0]                 # lesson one, where the band's button goes
    n_tracks = render.NUM.get(len(tracks), len(tracks))
    cards = []
    for p in PEOPLE:
        who, les = cast[p["who"]], lessons[p["lesson"]]
        cards.append(f'<li class="q"><div class="sk-paper">{pics[p["who"]][1]}</div>'
                     f'<p class="q-who">{_E(who["name"])}, {_E(_job(who["title"]))}</p>'
                     f'<h3>\u201c{_E(p["ask"])}\u201d</h3><p>{_E(p["answer"])}</p>'
                     f'<a href="learn/{les.slug}/"><small>The {learn.minutes(les.body)} minute lesson</small> '
                     f'{_E(les.short)}\u00a0<i aria-hidden="true">→</i></a></li>')
    return f"""<section class="band" id="tutorial" aria-labelledby="h-learn"><div class="wrap">
  <header class="sec-h split"><p class="eyebrow">The tutorial</p>
    <h2 id="h-learn">Learn to run agent projects one question at a time.</h2>
    <p>{len(lessons)} lessons in {n_tracks} tracks, each answering a question a team asks.
    These four come from the fictional airline the manual follows. Lesson one takes {learn.minutes(first.body)} minutes.</p></header>
  <ol class="qs">{''.join(cards)}</ol>
  <div class="ba"><a class="btn pri" href="learn/{first.slug}/">Start with lesson one</a>
    <a class="more" href="learn/">See all {n_tracks} tracks <i aria-hidden="true">→</i></a></div>
</div></section>"""
