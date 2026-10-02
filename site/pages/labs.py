"""The labs: hands-on simulations, one engine and one script per lab.

A lab is a bench. The reader assembles a prompt from parts, runs it, reads the recorded reply, marks what is
wrong in it and makes the calls a person has to make, while the document they are making grows beside the
work. Each lab makes one document, and the next lab starts from it.

Where things are:

- ``site/content/labs/<slug>.py``: one lab's script, a ``LAB`` dict (its words, prompts, recorded replies,
  the document's sections and the beats in order). ``README.md`` beside them is the authoring guide.
- ``site/labs/lab.js`` and ``lab.css``: the engine and its look, loaded only on lab pages.
- this module: loads the scripts, checks them, and renders the front page (``/labs/``) and one page per lab,
  each with a reading version underneath for a page without script.

A recorded reply is a real model's answer to the exact prompt shown, saved when the lab was written. The
check refuses a reply that does not say which model and on what date: a lab never passes off a written
example as a recording.
"""
from __future__ import annotations

import importlib.util
import json
import re
from html import escape as _E
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DIR = SITE / "content" / "labs"
PHASES = [("P0", "Frame", "slate"), ("P1", "Design &amp; Spec", "indigo"), ("P2", "Build &amp; Prove", "teal"), ("P3", "Run &amp; Learn", "amber")]
KINDS = {"note", "compose", "run", "mark", "choose", "compare", "file"}
_LABS: list[dict] | None = None


def load() -> list[dict]:
    """Every lab that has a script, in order. ``PLANNED`` in ``_set.py`` lists the ones still to come."""
    global _LABS
    if _LABS is None:
        _LABS = []
        for f in sorted(DIR.glob("*.py")):
            if f.name.startswith("_"):
                continue
            spec = importlib.util.spec_from_file_location(f"lab_{f.stem.replace('-', '_')}", f)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            lab = prepare(dict(mod.LAB, slug=f.stem))
            _LABS.append(lab)
        _LABS.sort(key=lambda x: x["n"])
    return _LABS


def planned() -> list[dict]:
    f = DIR / "_set.py"
    if not f.exists():
        return []
    spec = importlib.util.spec_from_file_location("lab_set", f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(mod.PLANNED)


def _lines(text: str) -> list[dict]:
    """A recorded reply as lines. A line that starts with ``#`` or is wholly bold is a heading."""
    out = []
    for raw in text.strip("\n").split("\n"):
        t = raw.rstrip()
        out.append({"t": t, **({"h": 1} if re.match(r"^(#{1,4} |\*\*[^*]+\*\*:?$)", t.strip()) else {})})
    return out


def prepare(lab: dict) -> dict:
    """Turn the script's convenient forms into the ones the engine reads: a reply's ``text`` becomes
    ``lines``, and each ``flags`` entry (the start of a line, and why it is a fault) is attached to its line."""
    for rid, r in lab["replies"].items():
        if "lines" not in r:
            r["lines"] = _lines(r.pop("text"))
        for start, why in r.pop("flags", []):
            hit = [ln for ln in r["lines"] if ln["t"].strip().startswith(start)]
            if len(hit) != 1:
                raise SystemExit(f"labs/{lab['slug']}: reply {rid}: the flag {start!r} matches {len(hit)} lines; it must match one")
            hit[0].update(flag=1, why=why)
        for start, why in r.pop("sound", []):          # a line a careful reader might mark, and why it is sound
            hit = [ln for ln in r["lines"] if ln["t"].strip().startswith(start)]
            if len(hit) != 1:
                raise SystemExit(f"labs/{lab['slug']}: reply {rid}: the note {start!r} matches {len(hit)} lines; it must match one")
            hit[0].update(why=why)
    return lab


def check(labs: list[dict]) -> list[str]:
    """What every lab must keep to. An empty list is a pass."""
    err = []
    for lab in labs:
        s = f"labs/{lab['slug']}"
        for k in ("n", "title", "does", "who", "phase", "minutes", "makes", "tool", "artefact", "replies", "beats", "debrief"):
            if k not in lab:
                err.append(f"{s}: missing {k}")
        ids = [b.get("id") for b in lab.get("beats", [])]
        if len(ids) != len(set(ids)) or None in ids:
            err.append(f"{s}: every beat needs its own id")
        secs = {x["id"] for x in lab["artefact"]["sections"]}
        marks = 0
        for b in lab.get("beats", []):
            if b.get("kind") not in KINDS:
                err.append(f"{s}: beat {b.get('id')}: unknown kind {b.get('kind')!r}")
            if b.get("kind") in ("run", "mark") and "reply" in b:
                refs = [b["reply"]] if isinstance(b["reply"], str) else list(b["reply"].values())
                err += [f"{s}: beat {b['id']}: no reply called {r!r}" for r in refs if r not in lab["replies"]]
                if isinstance(b["reply"], dict) and "*" not in b["reply"]:
                    err.append(f"{s}: beat {b['id']}: the reply map needs a '*' entry for any other prompt")
            if b.get("kind") == "mark":
                marks += 1
                refs = [b["doc"]] if b.get("doc") else ([b["reply"]] if isinstance(b.get("reply"), str) else list((b.get("reply") or {}).values()))
                for r in refs:
                    if r in lab["replies"] and not any(ln.get("flag") for ln in lab["replies"][r]["lines"]):
                        err.append(f"{s}: beat {b['id']}: reply {r!r} has nothing to mark")
            patches = list(b.get("patch", [])) + [p for o in b.get("options", []) + b.get("cols", []) for p in o.get("patch", [])]
            err += [f"{s}: beat {b['id']}: no section called {p['id']!r}" for p in patches if "id" in p and p["id"] not in secs]
            if b.get("kind") in ("choose", "compare") and not any(o.get("right") for o in b.get("options", []) + b.get("cols", [])):
                err.append(f"{s}: beat {b['id']}: no option is marked as the book's")
        if not marks:
            err.append(f"{s}: a lab without a reply to mark is a slideshow; add a mark beat")
        if not lab["beats"] or lab["beats"][-1].get("kind") != "file":
            err.append(f"{s}: the last beat files the document")
        for rid, r in lab["replies"].items():
            if not (r.get("model") and re.fullmatch(r"\d{1,2} [A-Z][a-z]+ \d{4}", r.get("date", ""))):
                err.append(f"{s}: reply {rid}: a recording says which model and on what date (for example '2 October 2026')")
            err += [f"{s}: reply {rid}: no section called {p['id']!r}" for p in r.get("patch", []) if "id" in p and p["id"] not in secs]
        blob = json.dumps({k: v for k, v in lab.items() if k != "replies"}, ensure_ascii=False)
        if "—" in blob or "–" in blob:
            err.append(f"{s}: a dash in the lab's own words (recorded replies are left as the model wrote them)")
    return err


def _phase(lab: dict) -> tuple[str, str, str]:
    return PHASES[lab["phase"]]


def _rich(text: str) -> str:
    def inline(t: str) -> str:
        t = _E(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        return re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    out = []
    for block in re.split(r"\n\s*\n", (text or "").strip()):
        lines = block.split("\n")
        if all(ln.startswith("- ") for ln in lines):
            out.append("<ul>" + "".join(f"<li>{inline(ln[2:])}</li>" for ln in lines) + "</ul>")
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "".join(out)


def _reply_text(r: dict) -> str:
    return "\n".join(ln["t"] for ln in r["lines"])


def _book(lab: dict) -> dict:
    """The lab played by the book: the first prompt option marked ``book`` in each slot, the option marked
    ``right`` at each call. Used for the reading version and to hand the document to the next lab."""
    picks: dict = {}
    for b in lab["beats"]:
        if b["kind"] == "compose":
            picks[b["id"]] = {p["id"]: next((o["id"] for o in p["options"] if o.get("book")), p["options"][-1]["id"])
                              for p in b["parts"] if "options" in p}
        elif b["kind"] in ("choose", "compare"):
            opts = b.get("options") or b.get("cols")
            picks[b["id"]] = next(o["id"] for o in opts if o.get("right"))
    return picks


def _holds(when: dict | None, picks: dict) -> bool:
    if not when:
        return True
    for k, want in when.items():
        bid, _, part = k.partition(".")
        v = picks.get(bid)
        if part and isinstance(v, dict):
            v = v.get(part)
        if (v not in want) if isinstance(want, list) else (v != want):
            return False
    return True


def _reply_for(b: dict, picks: dict) -> str:
    if isinstance(b["reply"], str):
        return b["reply"]
    c = picks.get(b["of"], {})
    for k, rid in b["reply"].items():
        if k != "*" and all(c.get(kv.split("=")[0]) == kv.split("=")[1] for kv in k.split(",")):
            return rid
    return b["reply"]["*"]


def book_document(lab: dict) -> str:
    """The lab's document as it stands when the lab is played by the book, as markdown text."""
    picks = _book(lab)
    secs = {x["id"]: dict(x) for x in lab["artefact"]["sections"]}

    def apply(patches):
        for p in patches or []:
            if "id" in p and "body" in p:
                secs[p["id"]]["body"] = p["body"]

    for b in lab["beats"]:
        if not _holds(b.get("when"), picks):
            continue
        apply(b.get("patch"))
        if b["kind"] in ("choose", "compare"):
            apply(next(o for o in (b.get("options") or b.get("cols")) if o["id"] == picks[b["id"]]).get("patch"))
        if b["kind"] in ("run", "mark") and "reply" in b:
            apply(lab["replies"][_reply_for(b, picks)].get("patch"))
    return "\n\n".join((x["head"] + "\n" if x.get("head") else "") + x["body"] for x in secs.values() if x.get("body")) + "\n"


def _plain(lab: dict) -> str:
    """The lab as a document to read: each step, the prompt the book uses, the recorded reply, what to notice."""
    picks = _book(lab)
    out = ['<p>This lab is played with script. Here it is as a document: each step, the prompt the book uses, '
           "the recorded reply, and what to notice in it.</p>"]
    for f in lab.get("files", []):
        out.append(f'<h2>On the desk: {_E(f["name"])}</h2><pre>{_E(f["body"])}</pre>')
    for b in lab["beats"]:
        if not _holds(b.get("when"), picks):
            continue
        if b.get("move"):
            out.append(f'<h2>{_E(b["move"])}</h2>')
        if b.get("say"):
            out.append(_rich(b["say"]))
        if b["kind"] == "compose":
            text = "\n\n".join(p["text"] if "text" in p else next(o["text"] for o in p["options"] if o["id"] == picks[b["id"]][p["id"]])
                               for p in b["parts"])
            out.append(f'<p><b>The prompt:</b></p><pre>{_E(text)}</pre>')
        elif b["kind"] in ("run", "mark"):
            r = lab["replies"][b.get("doc") or _reply_for(b, picks)]
            out.append(f'<p><b>Recorded reply</b> ({_E(r["model"])}, {_E(r["date"])}; yours will differ):</p><pre>{_E(_reply_text(r))}</pre>')
            if b["kind"] == "mark":
                faults = [ln for ln in r["lines"] if ln.get("flag")]
                out.append(f'<p><b>{_E(b["ask"])}</b></p><ul>' + "".join(f'<li><code>{_E(ln["t"].strip())}</code> {_E(ln["why"])}</li>' for ln in faults) + "</ul>")
        elif b["kind"] in ("choose", "compare"):
            opts = b.get("options") or b.get("cols")
            o = next(x for x in opts if x.get("right"))
            out.append(f'<p><b>{_E(b["ask"])}</b></p><ul>' + "".join(f'<li>{_E(x["label"])}</li>' for x in opts) + "</ul>")
            out.append(f'<p>The book chooses: <b>{_E(o["label"])}</b>.</p>' + _rich(o.get("after", "")))
    d = lab["debrief"]
    out.append(f'<h2>{_E(d["title"])}</h2>' + _rich(d["trap"]) + "<h2>The habit to keep</h2>" + _rich(d["habit"]))
    out.append(f'<h2>The document, by the book: {_E(lab["artefact"]["name"])}</h2><pre>{_E(book_document(lab))}</pre>')
    return "".join(out)


def lab_page(lab: dict, labs: list[dict], shell, ctx: dict) -> str:
    key, name, hue = _phase(lab)
    script = {k: lab[k] for k in ("slug", "title", "artefact", "files", "replies", "beats", "debrief") if k in lab}
    script["v"] = lab.get("v", 1)
    nxt = next((x for x in labs if x["n"] == lab["n"] + 1), None)
    links = [("All the labs", "../")] if not nxt else [(f'Next lab: {nxt["title"]}', f'../{nxt["slug"]}/'), ("All the labs", "../")]
    script["debrief"] = dict(lab["debrief"], links=links + [tuple(x) for x in lab["debrief"].get("links", [])])
    body = f"""<div class="wrap"><main id="main" class="page labpage">
  <header class="lab-head"><p class="eyebrow" style="--c:var(--dg-{hue})">Lab {lab["n"]} · {key} {name} · {_E(lab["who"])}</p>
    <h1>{_E(lab["title"])}</h1>
    <p class="lede">{_E(lab["does"])}</p>
    <ul class="lab-facts"><li><b>{lab["minutes"]} minutes</b></li><li>You leave with <b>{_E(lab["makes"])}</b></li>
      <li>On the bench: <b>{_E(lab["tool"]["name"])}</b></li><li>Replies are recordings of a real model, dated</li></ul></header>
  <div id="lab" class="lab" hidden></div>
  <section class="lab-plain prose" aria-label="This lab, as a document to read">{_plain(lab)}</section>
</main></div>
<script type="application/json" id="lab-data">{json.dumps(script, ensure_ascii=False).replace("</", "<\\/")}</script>"""
    return shell(title=f'{lab["title"]} · a hands-on lab · The agentic manual',
                 desc=f'{lab["does"]} A hands-on lab: {lab["minutes"]} minutes, real recorded model replies, and you leave with {lab["makes"]}.',
                 body=body, depth=2, nav_id="labs", canonical=f'{ctx["base"]}labs/{lab["slug"]}/',
                 head_extra='<link rel="stylesheet" href="../../labs/lab.css"><script src="../../labs/lab.js" defer></script>',
                 crumbs=[("Labs", "../"), (lab["title"], "")], kind="simulator", og="home")


def hub(labs: list[dict], shell, ctx: dict) -> str:
    rows = []
    for item in sorted(labs + planned(), key=lambda x: x["n"]):
        key, name, hue = PHASES[item["phase"]]
        inner = (f'<span class="l-n">Lab {item["n"]} · {key}</span>'
                 f'<span class="l-t">{_E(item["title"])}<small>{_E(item["does"])}</small></span>'
                 f'<span class="l-m"><b>{_E(item["who"])}</b>You leave with {_E(item["makes"])}</span>')
        if "beats" in item:
            rows.append(f'<li style="--c:var(--dg-{hue})"><a href="{item["slug"]}/">{inner}<span class="l-go">{item["minutes"]} min →</span></a></li>')
        else:
            rows.append(f'<li style="--c:var(--dg-{hue})"><div class="soon">{inner}<span class="l-go">being built</span></div></li>')
    body = f"""<div class="wrap"><main id="main" class="page">
  <header class="phead"><p class="eyebrow">The labs</p>
    <h1>Do the work of an AI project with your own hands</h1>
    <p class="lede">Each lab is ten to fifteen minutes on one real job from the airline case: you assemble the prompt, run it,
    read what a real model said, catch what is wrong, and make the calls only a person can make. You leave each one
    with a document, and the next lab starts from it.</p></header>
  <ol class="labs-how">
    <li><b>You assemble the prompt</b><span>From parts, the way a practised hand builds one. Every part is a choice, and the choice changes the reply.</span></li>
    <li><b>The reply is a recording</b><span>A real model's answer to that exact prompt, with its name and the date on it. Yours will differ; copy the prompt and try it.</span></li>
    <li><b>You leave with the document</b><span>It grows beside your work and shows what a person decided and what a model guessed. Download it, or carry it into the next lab.</span></li>
  </ol>
  <ol class="labs-list">{"".join(rows)}</ol>
  <div class="next"><a class="btn pri" href="{labs[0]["slug"]}/">Start with {_E(labs[0]["title"])}</a>
    <a class="btn" href="../simulator/">Or play the whole project as a game</a></div>
</main></div>"""
    return shell(title="The labs: do the work of an AI project with your own hands · The agentic manual",
                 desc="Hands-on labs on one airline case: assemble a prompt, read a real model's recorded reply, catch what is wrong, "
                      "and leave each lab with the document it makes, from the spec to the system prompt to the architecture.",
                 body=body, depth=1, nav_id="labs", canonical=f'{ctx["base"]}labs/',
                 head_extra='<link rel="stylesheet" href="../labs/lab.css">', crumbs=[("Labs", "")], kind="simulator", og="home")


def render(put, shell, ctx: dict) -> None:
    labs = load()
    errors = check(labs)
    if errors:
        raise SystemExit("labs: " + "\n  labs: ".join([""] + errors))
    if not labs:
        return
    put("labs/index.html", hub(labs, shell, ctx))
    for lab in labs:
        put(f'labs/{lab["slug"]}/index.html', lab_page(lab, labs, shell, ctx))


def urls(base: str) -> list[str]:
    return [f"{base}labs/"] + [f'{base}labs/{lab["slug"]}/' for lab in load()]
