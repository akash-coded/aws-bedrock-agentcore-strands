"""The forward-deployed engineer guide: its hub, /forward-deployed-engineer/, and the framework picture.

A staged role (content/roles/forward-deployed-engineer.json, built by content/roles/_src/build_content.py) is
a guide of four pages: this hub, and one page per stage, Frame, Deliver and Evolve. ``render.render()`` hands
the role here. The hub's words are ``fde_hub.py``. Every quotation and source is a dated record in
``fde_sources.py``, and every fact about an AI tool is an id in content/tools/tools.json, so the page never
types a claim about the profession. Both files are checked on every build, and a problem stops it. The
guide's pages load theme/fde.css, and no other page does.

``figure(role, open_stage=None)`` draws the framework (council 10, verdict 2.4): the three stages down the
side in ink, the manual's four phases across in their hues, one step in each cell, and a rose signature at
the end of each row. It is read, not watched: nothing in it moves. On the hub every row is open and each
link goes down to its stage page. On a stage page its own row is open and the other two show their names
and four step names, as links across.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
_SRC = str(SITE / "content" / "roles" / "_src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
import fde_hub  # noqa: E402
import fde_sources  # noqa: E402

CSS = '<link rel="stylesheet" href="{up}theme/fde.css">'
NUM = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 12: "twelve"}


def E(s) -> str:
    return html.escape(str(s), quote=False)


def A(s) -> str:
    """Text for an attribute in double quotes."""
    return E(s).replace('"', "&quot;")


def _stage_name(st: dict) -> str:
    """A stage always carries its object, so Frame the stage never reads as P0's Frame."""
    return f'{st["name"]} {st["object"]}'


# ------------------------------------------------------------------------------------------- the picture
def figure(role: dict, open_stage: str | None = None) -> str:
    """The framework picture, for the hub (``open_stage`` None) or for the stage page of ``open_stage``.

    For a screen reader it is an ordered list of three stages, each an ordered list of four links that read
    "P0, step 1, Qualify: is this engagement worth taking? Discovery brief". The words are a label because
    hidden punctuation inside a link reads with stray spaces ("P0 , step 1 ,"). The header row repeats the
    phases each link already names, so it is hidden from a screen reader; the list's label says what the grid is."""
    import render
    f = fde_hub.FIGURE

    def at(stage: str) -> str:
        """A stage page's address from this page."""
        return "" if stage == open_stage else f"../{stage}/" if open_stage else f"{stage}/"

    head = "".join(f'<span class="p{p[1]}"><b>{p}</b>{render.PHASE_SHORT[p]}<em>{E(q)}</em></span>'
                   for p, q in f["phases"].items())
    rows = []
    for st in role["stages"]:
        full = open_stage in (None, st["id"])
        cells = []
        for s in (s for s in role["steps"] if s["stage"] == st["id"]):
            q, art = s["question"], s["artifact"]["short"]
            said = f'{s["pdlc"]}, step {s["n"]}, {s["phase"]}' + (f": {q[0].lower()}{q[1:]} {art}" if full else "")
            more = f'<span>{E(q)}</span><em>{E(art)}</em>' if full else ""
            cells.append(f'<li><a class="p{s["pdlc"][1]}" href="{at(st["id"])}#{s["id"]}" aria-label="{A(said)}">'
                         f'<i><b>{s["pdlc"]}</b>{s["n"]}</i><strong>{E(s["phase"])}</strong>{more}</a></li>')
        who = f'<b aria-hidden="true">{E(st["name"][0])}</b><strong>{E(st["name"])}</strong>'
        if full:
            who += f'<span>{E(st["object"])}</span><small>{E(st["span"])}. {E(st["people"])}</small>'
        # the row a stage page is about names it; it never links to the page it is on
        who = (f'<div class="fx-h">{who}</div>' if st["id"] == open_stage
               else f'<a class="fx-h" href="{at(st["id"])}">{who}</a>')
        sign = (f'<p class="fx-so"><b>{E(f["signed"])}</b> {E(st["signed"])}, by {E(st["signer"])}</p>' if full else "")
        rows.append(f'<li class="fx-r{"" if full else " fx-m"}">{who}<ol class="fx-s">{"".join(cells)}</ol>{sign}</li>')
    title = (f'<figcaption class="fx-t"><h2>{E(f["title"])}</h2><p>{E(f["caption"])}</p></figcaption>'
             if open_stage is None else "")
    return (f'<figure class="fx" id="framework">{title}<div class="fx-ph" aria-hidden="true">'
            f'<span class="fx-k">{E(f["corner"])}</span>{head}</div>'
            f'<ol class="fx-g" aria-label="{A(f["label"])}">{"".join(rows)}</ol>'
            f'<p class="fx-f">{E(f["foot"])}</p></figure>')


# --------------------------------------------------------------------------------------------- the hub
def _sketch(name: str) -> dict | None:
    """A lesson's sketch by its own name, or by its lesson's slug: a lesson has one sketch at most."""
    from pages import learn
    every = learn.sketches()
    return every.get(name) or next((s for s in every.values() if s["lesson"] == name), None)


def _table(head: list[str], rows: list[list[str]], cls: str = "", corner: bool = True, caption: str = "") -> str:
    """A table whose first cell in each row heads it. On a phone each row stacks, every cell under its
    column's name (fde.css, ``.fdt``)."""
    th = ("<td></td>" if corner else "") + "".join(f'<th scope="col">{h}</th>' for h in head)
    # each cell's column name, already escaped, without a head's small print
    names = [h.split("<", 1)[0].replace('"', "&quot;") for h in head][-(len(rows[0]) - 1):]
    body = "".join(
        f'<tr><th scope="row">{r[0]}</th>'
        + "".join(f'<td data-l="{n}">{c}</td>' for n, c in zip(names, r[1:])) + "</tr>"
        for r in rows)
    cap = f'<caption class="vh">{E(caption)}</caption>' if caption else ""
    return (f'<div class="tw" tabindex="0"><table class="fdt{" " + cls if cls else ""}">{cap}<thead><tr>{th}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def _sources(marks: "fde_sources.Marks") -> str:
    """The foot of a guide's page: its sources, numbered in the order the page first names them."""
    return (f'<section class="fx-src" id="sources" aria-labelledby="sources-h"><h2 class="h4" id="sources-h">'
            f'Where every claim on this page comes from</h2>'
            f'<p>Every claim about the profession is a posting, a page or an article, with the date it was checked. A date '
            f'turns amber once it is more than sixty days old.</p>{marks.foot()}</section>') if marks.order else ""


def hub(shell, role: dict) -> str:
    import render
    from pages import _kit as k, learn, sketch as sk_mod, tools

    H, S = fde_hub.HEAD, {s["id"]: s for s in fde_hub.SECTIONS}
    marks = fde_sources.Marks()
    _m, _t, lessons = learn.load()
    roles = {r["id"]: r for r in render.load_roles()}
    by_n = {s["n"]: s for s in role["steps"]}

    def T(text: str) -> str:
        """The hub's words: markdown-lite, then each quotation and source mark in place. A source's bare mark
        sits against the word before it, as a note's number does."""
        return marks.inline(render.md(re.sub(r"\s+(?=\[\[)", "", text)))

    def more(href: str, text: str) -> str:
        """A link on its own line, its arrow in place of the full stop."""
        return f'<p><a class="more" href="{href}">{E(text.rstrip("."))} <i aria-hidden="true">→</i></a></p>'

    def step(n: int) -> str:
        """A step of this guide, on its stage page."""
        s = by_n[n]
        return f'{s["stage"]}/#{s["id"]}'

    def lesson(slug: str) -> str:
        return f"../learn/{slug}/"

    def sec(sid: str, inner: str, cls: str = "") -> str:
        s = S[sid]
        lede = f'<p>{T(s["lede"])}</p>' if s.get("lede") else ""
        return f'<section class="sec{" " + cls if cls else ""}" id="{sid}"><h2>{E(s["h2"])}</h2>{lede}{inner}</section>'

    # 01 · what the job is, in three companies' words, and what you are judged on
    w = S["what"]
    quotes = "".join(f'<li>{fde_sources.quote(q)}{fde_sources.cite(fde_sources.QUOTES[q]["source"])}</li>' for q in w["quotes"])
    j = w["judged"]
    what = sec("what", f'<ul class="fq">{quotes}</ul><h3>{E(j["h3"])}</h3>'
                       f'<ol class="ticks">{"".join(f"<li>{T(x)}</li>" for x in j["items"])}</ol>'
                       f'<p class="fx-n">{T(j["source"])}</p>' + more(lesson(w["link"]["lesson"]), w["link"]["text"]))

    # 02 · six hats, with the hat stand beside the heading when F7's sketch is there
    h = S["hats"]
    hat_rows = []
    for r in h["rows"]:
        if r["role"] == role["id"]:
            href = step(r["steps"][0])
        else:
            first = next(s for s in roles[r["role"]]["steps"] if s["n"] == r["steps"][0])
            href = f'../{r["role"]}/#{first["id"]}'
        hat_rows.append([E(r["name"]), E(r["do"]), f'<a href="{href}">{E(r["borrow"])}</a>', E(r["theirs"])])
    side = ""
    spec = _sketch(h["sketch"])
    if spec:
        les = lessons[spec["lesson"]]
        side = (f'<div class="fx-sk">{sk_mod.render(spec)[0]}'
                + more(lesson(les.slug), f"From the lesson: {les.short}") + "</div>")
    hats = sec("hats", side + _table([E(x) for x in h["head"]], hat_rows, corner=False)
               + "".join(f"<p>{T(p)}</p>" for p in h["after"]), "fx-hs" if side else "")

    # 03 · the altitude table: what each kind of build asks of you
    a = S["altitude"]
    cols = [f'{E(c["name"])}<small>{E(c["when"])}</small>' for c in a["columns"]]
    alt = _table(cols, [[E(c) for c in r] for r in a["rows"]], "fx-al",
                 caption="Four altitudes, from a proof of concept to a deployment, compared on nine things")
    altitude = sec("altitude", alt + f'<p>{T(a["after"])}</p>')

    # 04 · a client inside your own company
    c = S["clients"]
    clients = sec("clients", _table([E(x) for x in c["head"]], [[E(x) for x in r] for r in c["rows"]])
                  + f'<p>{T(c["after"])}</p>')

    # 05 · two crafts, each move in the step that teaches it
    craft = sec("craft", '<div class="fx-cr">' + "".join(
        f'<div><h3>{E(col["h3"])}</h3><ol>'
        + "".join(f'<li>{T(t)} <a href="{step(n)}">step {n}</a></li>' for t, n in col["items"]) + "</ol></div>"
        for col in S["craft"]["columns"]) + "</div>")

    # 06 · AI tools in their building: dated facts from the Tool guides, then five rules
    t = S["tools"]
    by_id = tools.load()["by_id"]
    def dated(f: dict) -> str:
        """A fact's source and the day it was checked, in amber after sixty days, as the Tool guides show it."""
        old = ' class="stale"' if tools.is_stale(f) else ""
        return (f'<a href="{A(f["source"])}" target="_blank" rel="noopener">{E(tools._host(f["source"])[0])}</a> '
                f'<time{old} datetime="{f["checked"]}">checked {tools.short_date(f["checked"])}</time>')

    facts = [f'<li>{" ".join(tools._code(by_id[i]["fact"]) for i in group)}'
             f'<cite class="fsrc">{" · ".join(dated(by_id[i]) for i in group)}</cite></li>' for group in t["facts"]]
    toolsec = sec("tools", f'<h3>{NUM[len(facts)].capitalize()} dated facts</h3><ul class="ticks fx-tf">{"".join(facts)}</ul>'
                           f'<h3>{NUM[len(t["rules"])].capitalize()} rules</h3>'
                           f'<ol class="ticks">{"".join(f"<li>{T(x)}</li>" for x in t["rules"])}</ol>'
                           + more(f'../{t["link"]["page"]}', t["link"]["text"]) + f'<p>{T(t["after"])}</p>')

    # 07 · where people start from, the rungs, and ninety days to a first engagement
    cr = S["career"]
    ru, pl = cr["rungs"], cr["plan"]
    career = sec("career", _table([E(x) for x in cr["head"]], [[E(r[0])] + [T(x) for x in r[1:]] for r in cr["rows"]], corner=False)
                 + f'<h3>{E(ru["h3"])}</h3><ol class="ticks">{"".join(f"<li>{T(x)}</li>" for x in ru["items"])}</ol>'
                 f'<p>{T(ru["after"])}</p>'
                 f'<h3>{E(pl["h3"])}</h3><ol class="ticks">{"".join(f"<li>{T(x)}</li>" for x in pl["items"])}</ol>'
                 + more(lesson(pl["link"]["lesson"]), pl["link"]["text"]) + f'<p>{T(cr["hiring"])}</p>')

    # 08 · read next
    nx = S["next"]
    sim_a, sim_b = nx["sim"]["text"].split(". ", 1)
    # each lesson under the name the role's own reads give it (a tutorial name such as "For forward-deployed
    # engineers" says nothing on this page), with its level
    named = {h.rstrip("/").rsplit("/", 1)[-1]: l for l, h in role["reads"]}
    reads = "".join(f'<li><a href="{lesson(s)}">{E(named.get(s) or lessons[s].short)}<small>{E(lessons[s].level)}</small></a></li>'
                    for s in nx["lessons"])
    nextsec = sec("next", f'<ul class="readsg">{reads}</ul><p>{T(nx["line"])}</p>'
                          f'<p><a href="../{nx["sim"]["page"]}">{E(sim_a)}.</a> {E(sim_b)}</p>')
    first = next(st for st in role["stages"] if st["id"] == nx["next_up"]["stage"])
    foot = render.next_up(E(nx["next_up"]["line"]), f'{first["id"]}/', E(nx["next_up"]["text"]))

    sources = _sources(marks)

    # the page
    n_steps, n_prompts = len(role["steps"]), sum(len(s["prompts"]) for s in role["steps"])
    counts = "".join(f"<span>{c}</span>" for c in (
        f'{len(role["stages"])} stages', f"{n_steps} steps", f"{n_prompts} prompts"))
    guide = [(s["id"], s["rail"]) for s in fde_hub.SECTIONS]
    rail = (f'<aside class="rail wideonly" aria-label="The guide"><p class="railh">{E(fde_hub.RAIL["guide"])}</p><ol>'
            + "".join(f'<li><a class="rl" data-for="{i}" href="#{i}"><span class="rn">{n:02d}</span><span>{E(x)}</span></a></li>'
                      for n, (i, x) in enumerate(guide, 1))
            + f'</ol><p class="railh">{E(fde_hub.RAIL["stages"])}</p><ol>'
            + "".join(f'<li><a class="rl" href="{st["id"]}/"><span class="rn">{E(st["name"][0])}</span>'
                      f'<span>{E(_stage_name(st))}</span></a></li>' for st in role["stages"])
            + "</ol></aside>")
    contents = ('<details class="howto narrowonly"><summary>On this page</summary><ol class="hlist">'
                + "".join(f'<li><a href="#{i}">{E(x)}</a></li>' for i, x in guide) + "</ol></details>")
    orient = k.orient(T(H["for"]), T(H["use"]), [T(x) for x in H["how"]],
                      extra=f'<a class="btn" href="{lesson(render.ROLE_LESSON[role["id"]])}">The lesson for this role&nbsp;→</a>')
    tour = k.tour([
        {"sel": "#framework", "title": "The whole job in one picture",
         "body": "Three stages down the side, the manual's four phases across. Each box is a step, and opens its "
                 "template, its prompts and a worked example. Each row ends in a signature that opens the next."},
        {"sel": "#hats", "title": "Six hats",
         "body": "Each hat borrows the steps of another role's page, and names the decision that stays the client's."},
        {"sel": "#altitude", "title": "Think at the right altitude",
         "body": "Read this before your next proof of concept: what to build, what to skip and what never to skip, "
                 "from a POC to a deployment."},
        {"sel": "#sources", "title": "Every claim, dated",
         "body": "Each quotation and number about the profession leads here, to its posting or page and the day it "
                 "was checked. A date turns amber after sixty days."},
    ])
    body = (f'<div class="cols two-col">{rail}<main id="main" class="numbered fde">'
            f'<header class="phead in-col"><p class="eyebrow">{E(H["eyebrow"])}</p><h1>{E(H["h1"])}</h1>'
            f'<p class="lede">{E(H["lede"])}</p><p class="pmeta">{counts}</p></header>'
            f'{contents}{orient}{figure(role)}{what}{hats}{altitude}{clients}{craft}{toolsec}{career}{nextsec}'
            f'{sources}{foot}</main></div>')
    desc = (f"What a forward-deployed engineer does, end to end: {NUM[len(role['stages'])]} stages, Frame, Deliver and "
            f"Evolve, and {NUM[n_steps]} steps, each with a template, prompts and the words for the hard "
            f"conversations, sourced from the companies that run FDE teams.")
    return shell(title=f"{role['name']}: the guide to the job, end to end · The agentic manual", desc=desc, body=body,
                 depth=1, accent=role["accent"], nav_id=role["id"], canonical=f"{render.BASE_URL}{role['id']}/",
                 head_extra=CSS.format(up="../"), crumbs=[("Roles", "../#roles"), (role["name"], "")], tour=tour,
                 kind="fde", og=role["id"], ctx={"lesson": (lesson(render.ROLE_LESSON[role["id"]]), "The lesson")})


# ----------------------------------------------------------------------------------------- a stage page
# A stage page's own words (verdict 4.4, F6). Its name, object, question, brief and signature are the role's
# HEAD["stages"] and its steps are the role's steps, so only these are typed here; check() holds them to the
# house rules.
STAGE = {
    "eyebrow": "The FDE guide · stage {k} of {n}",
    "brief": {"long": "How long", "people": "The client's people", "think": "You think at",
              "ends": "It ends with", "wrong": "What goes wrong here"},
    "steps": "{n} steps to {signed}",
    "internal": "If your client is inside your own company",
    "say": "Say it like this",
    # the foot of a stage page: a line, then the next stage; after Evolve, Frame again, and the hub beside it
    "next": {"frame": "The go decision is signed. On day one the work moves into their building.",
             "deliver": "The handover is signed and the system is theirs. What it taught comes next.",
             "evolve": "Start the next engagement, with what this one taught."},
    "hub": "The guide",
}
HAT = {"qa": "QA"}      # a hat's chip is its id, but an initialism keeps its capitals


def _step(role: dict, s: dict, marks: "fde_sources.Marks", first: bool) -> str:
    """One step on its stage page: the role pages' step, with its hats and its altitude as chips in the head,
    and after its activities the two blocks a staged role adds (verdict 2.5). The first step on the page is
    open, as on a role page."""
    import render
    w = STAGE
    out = render.step_html(role, s)
    if first:
        out = out.replace(f'id="{s["id"]}">', f'id="{s["id"]}" open>', 1)
    # the hats are named on screen: two readers from outside took bare chips for a step's tags
    chips = ("<span>Hats</span>" + "".join(f"<i>{E(HAT.get(h, h))}</i>" for h in s["hats"])
             + (f'<b><span class="vh">Altitude: </span>{E(s["level"])}</b>' if s.get("level") else ""))
    out = out.replace('<span class="wh">', f'<span class="fhat">{chips}</span><span class="wh">', 1)
    out = out.replace("</ol></section>", (
        f'</ol></section><section><div class="lbl">{E(w["internal"])}</div><p class="fint">{render.md(s["internal"])}</p>'
        f'</section><section><div class="lbl">{E(w["say"])}</div><ul class="fsay">'
        + "".join(f'<li><b>{E(x["to"])}</b><q>{E(x["words"])}</q></li>' for x in s["say"]) + "</ul></section>"), 1)
    # Deliver's examples have two halves, the case as it happened and your move: a paragraph each
    out = out.replace(" <strong>Your move:</strong>", "</p><p><strong>Your move:</strong>", 1)
    # a source's bare mark sits against the word before it, then each quotation and mark goes in place
    return marks.inline(re.sub(r"\s+(?=\[\[)", "", out))


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:]


def stage(shell, role: dict, st: dict) -> str:
    """A stage page, /forward-deployed-engineer/<stage>/: a focused read of the stage's four steps, with the
    framework open at its own row, the stage in brief, and a rail of all twelve steps by stage."""
    import render
    w, stages = STAGE, role["stages"]
    k = [x["id"] for x in stages].index(st["id"])
    steps = [s for s in role["steps"] if s["stage"] == st["id"]]
    name = _cap(_stage_name(st))
    marks = fde_sources.Marks()

    brief = "".join(f'<tr><th scope="row">{E(label)}</th><td>{render.md(st["brief"][key].rstrip("."))}.</td></tr>'
                    for key, label in w["brief"].items())
    brief = (f'<table class="fx-b"><caption class="vh">{E(name)}, in brief</caption><tbody>{brief}</tbody></table>')
    body_steps = "".join(_step(role, s, marks, i == 0) for i, s in enumerate(steps))
    n_prompts = sum(len(s["prompts"]) for s in steps)
    counts = "".join(f"<span>{c}</span>" for c in (
        f"{len(steps)} steps", f"{n_prompts} prompts"))

    # the rail: all twelve steps by stage, this stage's four in the page and the rest on their own pages
    def rail_row(s: dict) -> str:
        here = s["stage"] == st["id"]
        at = f' data-for="{s["id"]}" href="#{s["id"]}"' if here else f' href="../{s["stage"]}/#{s["id"]}"'
        return f'<li><a class="rl"{at}><span class="rn">{s["n"]}</span><span>{E(s["phase"])}</span></a></li>'
    rail = ('<aside class="rail wideonly" aria-label="The twelve steps, by stage">' + "".join(
        f'<p class="railh">{E(_cap(_stage_name(x)))}</p><ol>'
        + "".join(rail_row(s) for s in role["steps"] if s["stage"] == x["id"]) + "</ol>" for x in stages)
        + "</aside>")

    sources = _sources(marks)
    if k + 1 < len(stages):
        nxt = stages[k + 1]
        foot = render.next_up(E(w["next"][st["id"]]), f'../{nxt["id"]}/', E(_cap(_stage_name(nxt))))
    else:
        foot = render.next_up(E(w["next"][st["id"]]), f'../{stages[0]["id"]}/', E(_cap(_stage_name(stages[0]))),
                              ("../", E(w["hub"])))

    head_steps = w["steps"].format(n=NUM[len(steps)].capitalize(), signed=st["signed"])
    body = (f'<div class="cols two-col">{rail}<main id="main" class="fx-st">'
            f'<header class="phead in-col"><p class="eyebrow">{E(w["eyebrow"].format(k=k + 1, n=len(stages)))}</p>'
            f'<h1>{E(name)}</h1><p class="lede">{E(st["question"])}</p><p class="pmeta">{counts}</p></header>'
            f'{figure(role, st["id"])}{brief}'
            f'<div class="rolehead"><h2>{E(head_steps)}</h2>'
            f'<button type="button" class="btn ghost sm" data-expand>Expand all</button></div>'
            f'{body_steps}{sources}{foot}</main></div>')
    names = [s["phase"] for s in steps]
    desc = (f"{name}, stage {k + 1} of the forward-deployed engineer's guide. {st['question']} "
            f"{NUM[len(steps)].capitalize()} steps, {', '.join(names[:-1])} and {names[-1]}, each with a template, "
            f"prompts and the words to say.")
    return shell(title=f"{name} · {role['name']} · The agentic manual", desc=desc, body=body, depth=2,
                 accent=role["accent"], nav_id=role["id"], canonical=f"{render.BASE_URL}{role['id']}/{st['id']}/",
                 head_extra=CSS.format(up="../../"),
                 crumbs=[("Roles", "../../#roles"), (role["name"], "../"), (name, "")],
                 kind="fde-stage", og=role["id"],
                 ctx={"lesson": (f'../../learn/{render.ROLE_LESSON[role["id"]]}/', "The lesson")})


# ------------------------------------------------------------------------------------------ the guide's pages
def check(role: dict) -> list[str]:
    """The records, the hub's words against the built guide, and the stage pages' own words. An empty list
    is a pass."""
    bad = fde_sources.check() + fde_hub.check(role)
    for where, text in (("eyebrow", STAGE["eyebrow"]), ("steps", STAGE["steps"]), ("internal", STAGE["internal"]),
                        ("say", STAGE["say"]), ("hub", STAGE["hub"]), *STAGE["brief"].items(),
                        *(("next." + i, t) for i, t in STAGE["next"].items())):
        bad += fde_sources.house(f"fde STAGE {where}", text, "plain", prices=True)
    if set(STAGE["next"]) != {st["id"] for st in role["stages"]}:
        bad.append("fde STAGE next: one line for each stage")
    return bad


def search_rows(role: dict) -> list[dict]:
    """The guide in the drawer's search (render.search_index): the hub, each stage with its question and its
    artefacts, and each step at its stage page's address, so a search for a statement of work lands on Frame."""
    rid, rows = role["id"], []
    tidy = lambda t: re.sub(r"[*`]", "", fde_sources.plain(t))  # noqa: E731
    rows.append({"t": role["name"], "d": f'{role["tagline"]}. A guide in three stages, '
                 f'{", ".join(st["name"] for st in role["stages"][:-1])} and {role["stages"][-1]["name"]}.',
                 "u": f"{rid}/", "k": "Role · the FDE guide"})
    for k, st in enumerate(role["stages"], 1):
        arts = ["the " + s["artifact"]["short"][:1].lower() + s["artifact"]["short"][1:]
                for s in role["steps"] if s["stage"] == st["id"]]
        rows.append({"t": _cap(_stage_name(st)), "u": f"{rid}/{st['id']}/", "k": "FDE stage",
                     "d": f"Stage {k} of {len(role['stages'])}. {st['question']} It makes {', '.join(arts[:-1])} "
                          f"and {arts[-1]}."})
    for s in role["steps"]:
        rows.append({"t": f"{s['n']} · {s['phase']}: {tidy(s['title'])}", "d": tidy(s["purpose"])[:160],
                     "u": f"{rid}/{s['stage']}/#{s['id']}", "k": f"FDE step · {s['stage'].capitalize()}"})
    return rows


def _pages(role: dict) -> list[tuple[str, object]]:
    """Every page of the guide: its address under the site's root, and what writes it. render() and urls()
    both read this list, so a page is written and listed in the sitemap together."""
    return [(f'{role["id"]}/', hub)] + [
        (f'{role["id"]}/{st["id"]}/', lambda shell, role, st=st: stage(shell, role, st)) for st in role["stages"]]


def render(put, shell, role: dict) -> None:
    errors = check(role)
    if errors:
        raise SystemExit("fde: " + "\n  fde: ".join([""] + errors))
    for w in fde_sources.warnings():
        print("  fde: warning:", w)
    for address, page in _pages(role):
        put(f"{address}index.html", page(shell, role))


def urls(base: str, role: dict) -> list[str]:
    return [base + address for address, _page in _pages(role)]
