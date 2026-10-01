"""The simulator's page: Ninety Days, the SkyWays case as a game.

The game itself is in ``site/play/``: ``days.json`` (every word and number), ``sim.js`` (the rules),
``art.js`` (the pictures, drawn in code) and ``game.js`` (the page). This module renders the page they
run in, through the site's own shell, and writes the thirteen days as a plain list underneath for a
reader without script.

The workbench used to live at this address. Its routes all begin ``#/``, and the game never uses a
hash, so the first script in the head forwards any such route to ``/workbench/`` before the page paints.
"""
from __future__ import annotations

import json
from html import escape as _E
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "play" / "days.json"

FORWARD = ('<script>(function(){function f(){var h=location.hash;if(h&&h.charAt(1)==="/")location.replace("../workbench/"+h)}'
           'f();addEventListener("hashchange",f)})();</script>')


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def _days(n: int) -> str:
    return "no days" if not n else "1 day" if n == 1 else f"{n} days"


def _plain(data: dict) -> str:
    """The thirteen days as text: the situation, the question, and each option with its price and what
    it did. This is what a reader without script gets, and what a search engine reads."""
    out = []
    for d in data["days"]:
        forms = list(d["variants"].values()) if "variants" in d else [d]
        out.append(f'<h2>Day {d["day"]}. {_E(d["title"])}</h2>')
        for f in forms:
            who = lambda k: data["cast"].get(k, {}).get("name", k)
            out.append("".join(f"<p><b>{_E(who(k))}:</b> {_E(line)}</p>" for k, line in f["scene"]))
            out.append(f'<p><b>{_E(f["ask"])}</b></p>')
            if d.get("task") == "slide":
                out.append("<ul><li>What was saved, in person-days and in money.</li><li>What it cost: the model bill and the "
                           "review time.</li><li>The net for the cycle, and one target for the next.</li><li>The score on the "
                           "test set.</li><li>Any money paid out in error.</li><li>How many documents are on file.</li></ul>"
                           "<p>Leave the cost off the slide and finance finds it three weeks later.</p>")
            if f.get("options"):
                out.append("<ul>" + "".join(
                    f'<li>{_E(o["label"])} ({_days(o["days"])}). {_E(o["now"])}'
                    + (f' Later: {_E(o["debt"]["text"])}' if o.get("debt") else "") + "</li>"
                    for o in f["options"]) + "</ul>")
    return "".join(out)


def build(shell, ctx: dict) -> str:
    data = load()
    body = f"""<div class="wrap"><main id="main" class="nd">
  <header class="nd-top">
    <p class="eyebrow">The simulator</p>
    <h1>{_E(data["title"])}</h1>
    <p class="lede">{_E(data["premise"])}</p>
    <a class="nd-quit" href="./">Leave this run</a>
  </header>
  <div id="nd" class="nd-app" data-up="../" hidden></div>
  <section class="nd-plain" aria-label="The thirteen days, as text">
    <p>The game needs script to run. Here are its thirteen days as text. The calculators and the case in
    depth are in <a href="../workbench/">the workbench</a>.</p>
    {_plain(data)}
  </section>
</main></div>
<script type="application/json" id="nd-data">{json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>"""
    return shell(
        title="Ninety Days · the SkyWays simulator · The agentic manual",
        desc="Play an airline's ninety-day build of an AI rebooking assistant: thirteen decisions, each with a "
             "price in days, and consequences that arrive later. As one role, the whole team, or the sponsor.",
        body=body, depth=1, nav_id="simulator", canonical=ctx["base"] + "simulator/",
        head_extra=(FORWARD + '<link rel="stylesheet" href="../play/game.css">'
                    '<script src="../play/sim.js" defer></script><script src="../play/art.js" defer></script>'
                    '<script src="../play/game.js" defer></script>'),
        kind="simulator", og="home")
