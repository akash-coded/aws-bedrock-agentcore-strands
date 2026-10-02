"""The home page's library band: take the tools, templates and prompts with you.

:func:`band` builds the band (verdict-home 1.7): a three by three grid. Its first row is the three tools, each on the
material of what it opens: the workbench on its own navy panel, with its acceptance bar calculator set in real type;
the tutorial on the lessons' sketch paper, with its eight tracks in order; the simulator on the game's dusk, with the
boardroom on Day 90 drawn by the game's own code (``assets/pictures/sim-board.png``, made by ``tools/roomshot.mjs``).
Six shelves follow. Every number on a card is counted here, from what it counts, when the site is built.
"""
from __future__ import annotations

import json
import re
from html import escape as _E

# The calculator on the workbench's card shows the case's own acceptance bar, Maya's numbers in the tutorial band:
# a right answer saves $9 and a wrong one costs $36, so the bar is 36 / (36 + 9). The bar is worked out, never typed.
SAVES, COSTS = 9, 36
BOARD = "assets/pictures/sim-board.png"         # the boardroom on Day 90: node site/tools/roomshot.mjs board 90 <file>


def counts(tracks: list, lessons: dict) -> dict:
    """Every number the band shows, from the content it counts (verdict-home 1.9), and the name the workbench gives
    its acceptance bar calculator."""
    import render
    from pages import learn, models, pictures, tools
    roles = render.load_roles()
    workbench = (render.SITE / "app" / "SkyWays-Architect.html").read_text(encoding="utf-8")
    game = json.loads((render.SITE / "play" / "days.json").read_text(encoding="utf-8"))
    frameworks = json.loads((render.SITE / "content" / "library" / "frameworks.json").read_text(encoding="utf-8"))
    calc = re.search(r'TOOLS\.push\(\{id:"bar",name:"([^"]+)"', workbench)
    if not calc:
        raise SystemExit("homelib: the workbench has no acceptance bar calculator (TOOLS.push({id:\"bar\"...) to draw")
    return {
        "bar_name": calc.group(1),
        "calculators": len(re.findall(r"TOOLS\.push\(\{id:", workbench)),
        "lessons": len(lessons),
        "tracks": len(tracks),
        "hours": round(sum(learn.minutes(les.body) for les in lessons.values()) / 60),
        "decisions": len(game["days"]),
        "templates": sum(len(r["steps"]) for r in roles),
        "prompts": sum(len(s["prompts"]) for r in roles for s in r["steps"]),
        "models": len(models.MODELS),
        "jobs": len(tools.load()["jobs"]),
        "methods": len(frameworks["methods"]),
        "pictures": len(pictures.catalogue()),
    }


def _count(*parts: str) -> str:
    """A count line: a line may break only between its parts, so "about 7 hours" never splits."""
    return " · ".join(p.replace(" ", "\u00a0") for p in parts)


def _tool(kind: str, href: str, picture: str, count: str, name: str, line: str, go: str) -> str:
    """A flagship: the picture on its material, then a count, the name, one line and the action. One link."""
    return (f'<a class="fl fl-{kind}" href="{href}"><span class="fl-p">{picture}</span> '
            f'<span class="fl-b"><span class="lib-k">{count}</span> <b>{name}</b> <span class="lib-d">{line}</span> '
            f'<span class="fl-go">{go} <i aria-hidden="true">→</i></span></span></a>')


def band() -> str:
    """The home page's seventh band (verdict-home 1.7)."""
    from pages import learn
    _meta, tracks, lessons = learn.load()
    n = counts(tracks, lessons)
    bar = round(100 * COSTS / (COSTS + SAVES))
    # the workbench's calculator, by its name there: the two inputs, and the bar they set
    calc = (f'<span class="wbc" aria-hidden="true"><span class="wbc-h">{_E(n["bar_name"])}</span> '
            f'<span class="wbc-r">A right answer saves <b>${SAVES}</b></span> '
            f'<span class="wbc-r">A wrong one costs <b>${COSTS}</b></span> '
            f'<span class="wbc-r wbc-m">The bar <i style="--v:{bar}%"></i> <b>{bar}%</b></span></span>')
    # the tutorial's contents: every track, numbered; a phone shows each by its short name
    toc = " ".join(f'<span data-s="{_E(t.short)}"><i>{k:02d}</i> <span>{_E(t.title)}</span></span>'
                   for k, t in enumerate(tracks, 1))
    first = tracks[0].lessons[0]
    cards = [
        _tool("wb", "workbench/", calc, _count(f'{n["calculators"]} calculators', "a playbook for each role"), "The workbench",
              f"Run the numbers behind every decision, starting with the {bar}% bar.", "Open the workbench"),
        _tool("learn", f"learn/{first.slug}/", f'<span class="trk" aria-hidden="true">{toc}</span>',
              _count(f'{n["lessons"]} lessons', f'{n["tracks"]} tracks', f'about {n["hours"]} hours'), "The tutorial",
              "Every lesson in order, from the first question to interview answers.", "Start lesson one"),
        _tool("sim", "simulator/", f'<img src="{BOARD}" width="144" height="52" alt="" decoding="async">',
              _count(f'{n["decisions"]} decisions', "about fifteen minutes"), "The simulator",
              "Play one role, the whole team or the sponsor, from Day 1 or any later day.", "Enter the simulation"),
    ]
    # the shelves: a count (on a phone, only what comes before its dot), a name and one line
    shelves = [
        ("templates/", f'{n["templates"]} templates', "", "Templates", "One document to fill in for every step."),
        ("prompts/", f'{n["prompts"]} prompts', "", "Prompts", "Each states the job, the inputs and the shape of the answer."),
        ("models/", f'{n["models"]} rules of thumb', "", "Mental models", "Each one names the mistake it prevents."),
        ("tools/", f'{n["jobs"]} jobs', "every fact dated", "Tool guides",
         "Which AI tool does each job, with the source of every fact."),
        ("frameworks/", f'{n["methods"]} methods', "every acronym", "The methods, decoded",
         "Where AI-DLC, BMAD and the rest came from, and how they merge into one lifecycle."),
        ("pictures/", f'{n["pictures"]} pictures', "", "The picture pack", "Every diagram here, light and dark, free to reuse."),
    ]
    cards += [f'<a class="shf" href="{href}"><span class="lib-k">{count}{f"<span> · {more}</span>" if more else ""}</span> '
              f'<b>{name}</b> <span class="lib-d">{line}</span> <i aria-hidden="true">→</i></a>'
              for href, count, more, name, line in shelves]
    body = "\n    ".join(cards)
    return f"""<section class="band" id="library" aria-labelledby="h-lib"><div class="wrap">
  <header class="sec-h split"><p class="eyebrow">The library</p>
    <h2 id="h-lib">Take the tools, templates and prompts with you.</h2>
    <p>Start with one of the three tools, or copy what you need from the shelves. All of it is free to reuse under the MIT licence.</p></header>
  <div class="lib">
    {body}
  </div>
</div></section>"""
