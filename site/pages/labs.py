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
example as a recording. Where a compose beat sends a system prompt (its parts marked ``user`` are the
message, the rest the system prompt), the recording carries both, and the check holds both.
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
DATE = r"\d{1,2} [A-Z][a-z]+ \d{4}"                  # the date on a recording: 2 October 2026
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
    ``lines``, each ``flags`` entry (the start of a line, and why it is a fault) is attached to its line,
    and at a call every option that is not the book's is marked so."""
    for b in lab["beats"]:
        for o in b.get("options", []) + b.get("cols", []):
            if b["kind"] in ("choose", "compare"):
                o.setdefault("right", False)
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
    for r in lab.get("debrief", {}).get("others", {}).get("replies", []):      # other models' replies, read like the lab's own
        if "lines" not in r:
            r["lines"] = _lines(r.pop("text"))
    return lab


def _files(lab: dict) -> dict[str, dict]:
    out = {f["id"]: f for f in lab.get("files", [])}
    for b in lab["beats"]:
        out.update({f["id"]: f for f in b.get("gives", [])})
    return out


def _joined(lab: dict, beat: dict, picks: dict | None, user: bool) -> str:
    files, picks, out = _files(lab), picks or {}, []
    for p in beat["parts"]:
        if bool(p.get("user")) != user:
            continue
        if "file" in p:
            out.append(p.get("lead", "") + files[p["file"]]["body"])
        elif "text" in p:
            out.append(p["text"])
        else:
            want = picks.get(p["id"], p["options"][0]["id"])
            out.append(next(o["text"] for o in p["options"] if o["id"] == want))
    return "\n\n".join(t for t in out if t)


def prompt_text(lab: dict, beat: dict, picks: dict | None = None) -> str:
    """The prompt a compose beat assembles, given the option picked in each slot (the first option where
    none is given). The same joining as lab.js promptText, so the check below is the engine's own truth.
    Where the beat sends a message with it (parts marked ``user``), this is the system prompt."""
    return _joined(lab, beat, picks, False)


def message_text(lab: dict, beat: dict, picks: dict | None = None) -> str:
    """The message a compose beat sends with its system prompt: its parts marked ``user``, joined the same way.
    Empty for a beat whose prompt is the whole message."""
    return _joined(lab, beat, picks, True)


def _sent(lab: dict, beat: dict, picks: dict | None = None) -> tuple[str | None, str]:
    """What a compose beat sends, as (system prompt, message): (None, the prompt) where the prompt is the whole message."""
    msg = message_text(lab, beat, picks)
    return (prompt_text(lab, beat, picks), msg) if msg else (None, prompt_text(lab, beat, picks))


def _picks_for(key: str) -> dict:
    return {} if key == "*" else dict(kv.split("=") for kv in key.split(","))


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
        if lab.get("starts"):                           # a lab starts from the document the one before it filed
            prev, desk = next((x for x in labs if x["n"] == lab["n"] - 1), None), _files(lab).get(lab["starts"])
            if not prev or not desk:
                err.append(f"{s}: 'starts' names the desk file that the lab before it filed; there is no such lab or file")
            elif desk["body"] != book_document(prev).rstrip("\n"):
                err.append(f"{s}: the desk file {lab['starts']!r} is not the document Lab {prev['n']} files; copy it again, and record again")
        shown: dict[str, set] = {}                      # reply id -> what the lab shows it was sent: (system prompt or None, prompt)
        for b in lab.get("beats", []):
            comp = next((x for x in lab["beats"] if x["id"] == b.get("of")), None) if b.get("of") else None
            if b.get("kind") in ("run", "mark") and comp and comp.get("kind") == "compose":
                if b.get("doc"):
                    cond = b.get("when", {}).get(f"{comp['id']}.{next((p['id'] for p in comp['parts'] if 'options' in p), '')}")
                    keys = [cond] if isinstance(cond, str) else ["*"]
                    for k in keys:
                        slot = next((p["id"] for p in comp["parts"] if "options" in p), None)
                        shown.setdefault(b["doc"], set()).add(_sent(lab, comp, {slot: k} if slot and k != "*" else {}))
                elif isinstance(b.get("reply"), dict):
                    for k, rid in b["reply"].items():
                        if k != "*":
                            shown.setdefault(rid, set()).add(_sent(lab, comp, _picks_for(k)))
                elif isinstance(b.get("reply"), str):
                    shown.setdefault(b["reply"], set()).add(_sent(lab, comp))
            if b.get("kind") == "compare":
                for c in b.get("cols", []):
                    if c.get("reply"):
                        shown.setdefault(c["reply"], set()).add((None, c["body"]))
        for rid, r in lab["replies"].items():
            if not (r.get("model") and re.fullmatch(DATE, r.get("date", ""))):
                err.append(f"{s}: reply {rid}: a recording says which model and on what date (for example '2 October 2026')")
            if "prompt" not in r:
                err.append(f"{s}: reply {rid}: a recording carries the exact prompt it answers")
            elif rid in shown and (r.get("system"), r["prompt"]) not in shown[rid]:
                err.append(f"{s}: reply {rid}: the prompt the lab shows (or the system prompt sent with it) is not the one that was recorded")
            err += [f"{s}: reply {rid}: no section called {p['id']!r}" for p in r.get("patch", []) if "id" in p and p["id"] not in secs]
        err += _check_others(lab, s, shown)
        blob = json.dumps(_own_words(lab), ensure_ascii=False)
        if "—" in blob or "–" in blob:
            err.append(f"{s}: a dash in the lab's own words (recorded replies, and the words a table quotes from them, are left as the model wrote them)")
    return err


def _check_others(lab: dict, s: str, shown: dict[str, set]) -> list[str]:
    """The debrief's part on other models. Each of their replies is held to the lab's own rule (a model, its maker, a
    date, and the exact prompt the lab shows for the recording it stands beside), and each table is built from the
    replies alone: no cell is empty, each cell's ``quote`` is in its reply word for word, every number in a cell is in
    the words it quotes, and a ``count`` cell is the count."""
    o = lab.get("debrief", {}).get("others")
    if not o:
        return []
    err = [f"{s}: debrief.others: missing {k}" for k in ("title", "lead", "tables", "close", "fold", "replies") if not o.get(k)]
    ids = [r.get("id") for r in o.get("replies", [])]
    if len(ids) != len(set(ids)) or None in ids:
        err.append(f"{s}: debrief.others: every reply needs its own id")
    for r in o.get("replies", []):
        rid = f"others/{r.get('id')}"
        if not (r.get("model") and r.get("maker") and re.fullmatch(DATE, r.get("date", ""))):
            err.append(f"{s}: {rid}: a recording says which model, whose it is, and on what date (for example '2 October 2026')")
        if r.get("of") not in shown:
            err.append(f"{s}: {rid}: 'of' must name a recording whose prompt the lab shows, not {r.get('of')!r}")
        elif "prompt" not in r:
            err.append(f"{s}: {rid}: a recording carries the exact prompt it answers")
        elif (r.get("system"), r["prompt"]) not in shown[r["of"]]:
            err.append(f"{s}: {rid}: its prompt (or the system prompt sent with it) is not the one the lab shows for {r['of']!r}")
    for t in o.get("tables", []):
        name = f"{s}: debrief.others, the table {t.get('caption')!r}"
        cols = _columns(lab, t.get("of"))
        if len(cols) < 2:
            err.append(f"{name}: 'of' must name one of the lab's recordings that other models answered")
            continue
        if not (str(t.get("caption", "")).strip() and str(t.get("corner", "")).strip()):
            err.append(f"{name}: a table needs a caption and a name for its first column")
        texts = ["\n".join(ln["t"] for ln in c["lines"]) for c in cols]
        for row in t.get("rows", []):
            where, cells = f"{name}, row {row.get('h')!r}", row.get("cells", [])
            if not str(row.get("h", "")).strip():
                err.append(f"{name}: a row with no head")
            if len(cells) != len(cols):
                err.append(f"{where}: {len(cells)} cells for {len(cols)} columns")
                continue
            if any(not str(c).strip() for c in cells):
                err.append(f"{where}: a cell is empty")
            if row.get("count"):
                err += [f"{where}: {c['model']} writes {row['count']!r} {tx.count(row['count'])} times, not {v}"
                        for v, tx, c in zip(cells, texts, cols) if str(v) != str(tx.count(row["count"]))]
                continue
            quotes = row.get("quote") or []
            if len(quotes) != len(cols):
                err.append(f"{where}: each cell needs the words of its reply it is built from ({len(quotes)} for {len(cols)} cells)")
                continue
            for v, q, tx, c in zip(cells, quotes, texts, cols):
                qs = [] if q is None else [q] if isinstance(q, str) else list(q)
                err += [f"{where}: {c['model']}'s reply does not say {x!r}" for x in qs if x not in tx]
                err += [f"{where}: {c['model']}: {n} is not in the words the cell quotes" for n in re.findall(r"\d+(?:\.\d+)?", str(v))
                        if not any(re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", x) for x in qs)]     # 1 is not found in 11
    return err


def _own_words(lab: dict) -> dict:
    """The lab's own words, for the dash rule: everything but the recorded replies and the words a table quotes."""
    out = {k: v for k, v in lab.items() if k != "replies"}
    o = lab.get("debrief", {}).get("others")
    if o:
        o = {k: v for k, v in o.items() if k != "replies"}
        o["tables"] = [dict(t, rows=[{k: v for k, v in r.items() if k != "quote"} for r in t.get("rows", [])]) for t in o.get("tables", [])]
        out["debrief"] = dict(lab["debrief"], others=o)
    return out


def _columns(lab: dict, of: str | None) -> list[dict]:
    """A table's columns: the lab's own recording, then each other model's reply to the same prompt, in script order."""
    if of not in lab["replies"]:
        return []
    return [lab["replies"][of]] + [r for r in lab["debrief"].get("others", {}).get("replies", []) if r.get("of") == of]


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
        if b["kind"] in ("run", "mark") and ("reply" in b or b.get("doc")):      # as lab.js: a mark beat's reply is its doc
            apply(lab["replies"][b.get("doc") or _reply_for(b, picks)].get("patch"))
    return "\n\n".join((x["head"] + "\n" if x.get("head") else "") + x["body"] for x in secs.values() if x.get("body")) + "\n"


# ---------------------------------------------------------------------------------------------- other models
# A debrief may show its point holds beyond one model: ``debrief.others`` holds other models' replies to the lab's
# own prompts and the tables built from them. The part is drawn once, in the reading version; lab.js copies it into
# the debrief. The replies themselves have a page of their own (``labs/<slug>/others/``), which the fold reads in
# when it is opened, so the lab's page keeps to its byte budget.
def _asked(lab: dict, rid: str) -> tuple[dict, dict] | None:
    """Where the lab shows the prompt a recording answers: its compose beat, and the option picked in its slot."""
    for b in lab["beats"]:
        comp = next((x for x in lab["beats"] if x["id"] == b.get("of") and x.get("kind") == "compose"), None)
        if b.get("kind") not in ("run", "mark") or not comp:
            continue
        slot = next((p["id"] for p in comp["parts"] if "options" in p), None)
        if b.get("doc") == rid:
            k = (b.get("when") or {}).get(f"{comp['id']}.{slot}")
            return comp, ({slot: k} if slot and isinstance(k, str) else {})
        if isinstance(b.get("reply"), dict):
            k = next((k for k, r in b["reply"].items() if r == rid and k != "*"), None)
            if k:
                return comp, _picks_for(k)
        elif b.get("reply") == rid:
            return comp, {}
    return None


TO = ("System prompt", "Message")                    # where a beat sends a message with its prompt, the two halves' labels


def _prompt_box(lab: dict, comp: dict, picks: dict) -> str:
    """A prompt as its compose beat shows it once run: each part, the option picked, the desk files by name."""
    files, parts, label, was = _files(lab), [], "", None
    two = any(p.get("user") for p in comp["parts"])
    for p in comp["parts"]:
        if two and bool(p.get("user")) != was:
            was = bool(p.get("user"))
            parts.append(f'<p class="lab-to">{TO[was]}</p>')
        if "file" in p:
            lead = p.get("lead", "").strip()
            parts.append(f'<pre class="lab-part file">{_E(lead + " " if lead else "")}[ {_E(files[p["file"]]["name"])}, in full ]</pre>')
        elif "text" in p:
            parts.append(f'<pre class="lab-part">{_E(p["text"])}</pre>')
        else:
            o = next(x for x in p["options"] if x["id"] == picks.get(p["id"], p["options"][0]["id"]))
            label = o["label"]
            parts.append(f'<pre class="lab-part pick">{_E(o["text"] or "(nothing added)")}</pre>')
    return f'<div class="lab-prompt"><p class="lab-ph">{_E(comp["title"])}<span>{_E(label)}</span></p>{"".join(parts)}</div>'


def _reply_box(r: dict, to: str, rid: str = "") -> str:
    """A recorded reply in the lab's own look: the stamp, then the reply line by line, as the model wrote it."""
    who = " · ".join(_E(x) for x in (r["model"], r.get("maker"), r["date"]) if x)
    anchor = f' id="{_E(rid)}"' if rid else ""
    lines = "".join(f'<div class="lab-ln{" h" if ln.get("h") else ""}{" gap" if ln["t"] == "" else ""}">{_E(ln["t"])}</div>' for ln in r["lines"])
    return (f'<div class="lab-reply"{anchor}><p class="lab-stamp">Recorded reply · {who} · to {_E(to)}</p>'
            f'<div class="lab-lines">{lines}</div></div>')


def _others(lab: dict, page: bool = False) -> str:
    """The part: the lead, the tables, the closing line and, on the lab's page, the fold for the replies."""
    o, t_ = lab["debrief"]["others"], (lambda s: _E(str(s), quote=False))     # t_: text between tags needs no quote escaped
    out = [] if page else [_rich(o["lead"])]
    for t in o["tables"]:
        cols = _columns(lab, t["of"])
        head = f'<th scope="col">{t_(t["corner"])}</th>' + "".join(f'<th scope="col">{t_(c["model"])}</th>' for c in cols)
        rows = "".join(f'<tr><th scope="row">{t_(row["h"])}' + (f'<small>{t_(row["note"])}</small>' if row.get("note") else "") + "</th>"
                       + "".join(f'<td data-h="{_E(c["model"])}">{t_(v)}</td>' for c, v in zip(cols, row["cells"])) + "</tr>"
                       for row in t["rows"])
        out.append(f'<div class="tw lab-tw"><table class="lab-t"><caption>{t_(t["caption"])}</caption>'
                   f'<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
    out.append(f'<p class="lab-close">{_E(o["close"], quote=False)}</p>')
    if not page:                                     # with script, lab.js reads the replies in from their page when this opens
        out.append(f'<details class="lab-fold" data-src="others/"><summary>{_E(o["fold"], quote=False)}</summary><div class="lab-others-list">'
                   f'<p>They are on <a href="others/">a page of their own</a>, each as its model wrote it, under the prompt it answers.</p>'
                   f'</div></details>')
    return f'<div class="lab-others">{"".join(out)}</div>'


def others_page(lab: dict, shell, ctx: dict) -> str:
    """The replies behind the debrief's tables: each prompt as the lab shows it, then every other model's reply to it,
    and the lab's own two recordings for the tables' first column."""
    o = lab["debrief"]["others"]
    groups, own, two = [], [], False
    for t in o["tables"]:
        comp, picks = _asked(lab, t["of"])
        two = two or any(p.get("user") for p in comp["parts"])
        groups.append(_prompt_box(lab, comp, picks) + "".join(_reply_box(r, comp["title"], r["id"]) for r in o["replies"] if r["of"] == t["of"]))
        own.append(_reply_box(lab["replies"][t["of"]], comp["title"], t["of"]))
    sent = "Each system prompt went with its message and nothing else." if two else "Each prompt was the whole message."
    import render
    head = render.page_head(f'Lab {lab["n"]} · {_E(lab["title"])} · the replies behind its debrief', _E(o["title"]),
                            _E(o["lead"]), cls="lab-head")
    body = f"""<div class="wrap"><main id="main" class="page labpage">
  {head}
  <section class="lab-otherspage" aria-label="The tables and the replies">{_others(lab, page=True)}
    <h2>The replies, as the models wrote them</h2>
    <p>{sent}</p>
    <div class="lab-others-replies">{"".join(groups)}</div>
    <h2>The lab's own recordings, for the first column</h2>
    <div class="lab-others-own">{"".join(own)}</div>
    <p class="lab-next"><a class="btn pri" href="../">Back to the lab</a></p></section>
</main></div>"""
    return shell(title=f'{o["title"]} · {lab["title"]}, a hands-on lab · The agentic manual',
                 desc=f'{o["lead"]} Each prompt as the lab shows it, every reply as its model wrote it, and the tables built from them.',
                 body=body, depth=3, nav_id="labs", canonical=f'{ctx["base"]}labs/{lab["slug"]}/others/',
                 head_extra='<link rel="stylesheet" href="../../../labs/lab.css">',
                 crumbs=[("Labs", "../../"), (lab["title"], "../"), (o["title"], "")], kind="lab", og="labs")


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
            system, msg = _sent(lab, b, picks.get(b["id"]))
            out.append((f'<p><b>The system prompt:</b></p><pre>{_E(system)}</pre><p><b>The message sent with it:</b></p>'
                        if system is not None else "<p><b>The prompt:</b></p>") + f"<pre>{_E(msg)}</pre>")
        elif b["kind"] in ("run", "mark"):
            r = lab["replies"][b.get("doc") or _reply_for(b, picks)]
            out.append(f'<p><b>Recorded reply</b> ({_E(r["model"])}, {_E(r["date"])}; yours will differ):</p><pre>{_E(_reply_text(r))}</pre>')
            if b["kind"] == "mark":
                faults = [ln for ln in r["lines"] if ln.get("flag")]
                out.append(f'<p><b>{_E(b["ask"])}</b></p><ul>' + "".join(f'<li><code>{_E(ln["t"].strip())}</code> {_E(ln["why"])}</li>' for ln in faults) + "</ul>")
        elif b["kind"] in ("choose", "compare"):
            opts = b.get("options") or b.get("cols")
            o = next(x for x in opts if x.get("right"))
            if b["kind"] == "compare":
                for c in opts:
                    r = lab["replies"][c["reply"]]
                    out.append(f'<h3>{_E(c["label"])}</h3><pre>{_E(c["body"])}</pre>'
                               f'<p><b>Recorded reply</b> ({_E(r["model"])}, {_E(r["date"])}; yours will differ):</p><pre>{_E(_reply_text(r))}</pre>')
            out.append(f'<p><b>{_E(b["ask"])}</b></p><ul>' + "".join(f'<li>{_E(x["label"])}</li>' for x in opts) + "</ul>")
            out.append(f'<p>The book chooses: <b>{_E(o["label"])}</b>.</p>' + _rich(o.get("after", "")))
    d = lab["debrief"]
    out.append(f'<h2>{_E(d["title"])}</h2>' + _rich(d["trap"]) + "<h2>The habit to keep</h2>" + _rich(d["habit"]))
    if d.get("tool"):
        out.append(f'<h2>{_E(d["tool"]["title"])}</h2>' + _rich(d["tool"]["body"]))
    if d.get("others"):
        out.append(f'<h2>{_E(d["others"]["title"])}</h2>' + _others(lab))
    out.append(f'<h2>The document, by the book: {_E(lab["artefact"]["name"])}</h2><pre>{_E(book_document(lab))}</pre>')
    return "".join(out)


def lab_page(lab: dict, labs: list[dict], shell, ctx: dict) -> str:
    key, name = _phase(lab)[:2]
    script = {k: lab[k] for k in ("slug", "title", "artefact", "files", "replies", "beats", "debrief") if k in lab}
    script["replies"] = {rid: {k: v for k, v in r.items() if k not in ("prompt", "system")} for rid, r in lab["replies"].items()}
    script["v"] = lab.get("v", 1)
    nxt = next((x for x in labs if x["n"] == lab["n"] + 1), None)
    links = [("All the labs", "../")] if not nxt else [(f'Next lab: {nxt["title"]}', f'../{nxt["slug"]}/'), ("All the labs", "../")]
    lesson = [(f'The lesson behind this lab', f'../../learn/{lab["lesson"][0]}/')] if lab.get("lesson") else []
    script["debrief"] = dict(lab["debrief"], links=lesson + links + [tuple(x) for x in lab["debrief"].get("links", [])])
    if lab["debrief"].get("others"):                 # the part is copied from the reading version; the script needs its title
        script["debrief"]["others"] = {"title": lab["debrief"]["others"]["title"]}
    import render
    head = render.page_head(
        f'Lab {lab["n"]} · {key} {name} · {_E(lab["who"])}', _E(lab["title"]), _E(lab["does"]),
        f'<ul class="lab-facts"><li><b>{lab["minutes"]} minutes</b></li><li>You leave with <b>{_E(lab["makes"])}</b></li>'
        f'<li>On the bench: <b>{_E(lab["tool"]["name"])}</b></li><li>Replies are recordings of a real model, dated</li></ul>',
        cls="lab-head")
    body = f"""<div class="wrap"><main id="main" class="page labpage">
  {head}
  <div id="lab" class="lab" hidden></div>
  <section class="lab-plain prose" aria-label="This lab, as a document to read">{_plain(lab)}</section>
</main></div>
<script type="application/json" id="lab-data">{json.dumps(script, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")}</script>"""
    return shell(title=f'{lab["title"]} · a hands-on lab · The agentic manual',
                 desc=f'{lab["does"]} A hands-on lab: {lab["minutes"]} minutes, real recorded model replies, and you leave with {lab["makes"]}.',
                 body=body, depth=2, nav_id="labs", canonical=f'{ctx["base"]}labs/{lab["slug"]}/',
                 head_extra='<link rel="stylesheet" href="../../labs/lab.css"><script src="../../labs/lab.js" defer></script>',
                 crumbs=[("Labs", "../"), (lab["title"], "")], kind="lab", og="labs",
                 ctx={"lesson": (f'../../learn/{lab["lesson"][0]}/', lab["lesson"][1])} if lab.get("lesson") else None)


def hub(labs: list[dict], shell, ctx: dict) -> str:
    rows, every = [], sorted(labs + planned(), key=lambda x: x["n"])
    for item in every:
        key, name, hue = PHASES[item["phase"]]
        inner = (f'<span class="l-n">Lab {item["n"]} · {key}</span>'
                 f'<span class="l-t">{_E(item["title"])}<small>{_E(item["does"])}</small></span>'
                 f'<span class="l-m"><b>{_E(item["who"])}</b>You leave with {_E(item["makes"])}</span>')
        if "beats" in item:
            rows.append(f'<li style="--c:var(--dg-{hue})"><a href="{item["slug"]}/">{inner}<span class="l-go">{item["minutes"]} minutes&nbsp;→</span></a></li>')
        else:
            rows.append(f'<li style="--c:var(--dg-{hue})"><div class="soon">{inner}<span class="l-go">being built</span></div></li>')
    import render
    head = render.page_head(
        "The labs", "Do an AI project's work with your own hands",
        "Ten to fifteen minutes on one real job from the airline case, and you keep the document.",
        f'<p class="pmeta"><span>{len(every)} labs</span><span>{len(labs)} ready</span><span>10 to 15 minutes each</span></p>')
    body = f"""<div class="wrap"><main id="main" class="page">
  {head}
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
                      "and leave each lab with the document it makes, from the spec to the system prompt to the evidence pack.",
                 body=body, depth=1, nav_id="labs", canonical=f'{ctx["base"]}labs/',
                 head_extra='<link rel="stylesheet" href="../labs/lab.css">', crumbs=[("Labs", "")], kind="labs", og="labs")


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
        if lab["debrief"].get("others"):
            put(f'labs/{lab["slug"]}/others/index.html', others_page(lab, shell, ctx))


def urls(base: str) -> list[str]:
    return [f"{base}labs/"] + [u for lab in load() for u in [f'{base}labs/{lab["slug"]}/']
                               + ([f'{base}labs/{lab["slug"]}/others/'] if lab["debrief"].get("others") else [])]
