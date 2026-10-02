#!/usr/bin/env python3
"""Dump the authored Python role content to JSON for the renderer.

Authoring happens in Python because templates and prompts are multi-line strings with quotes in
them, and hand-escaping those into JSON is how mistakes get in. Run this after editing any
``<role>_*.py`` here; commit both the source and the generated JSON.

    python site/content/roles/_src/build_content.py

A role whose HEAD has ``stages`` is staged: the forward-deployed engineer's guide, twelve steps in three
stages, Frame, Deliver and Evolve. Inside each stage its phases run P0 to P3 once, so the check that the
phases never go back holds inside a stage, not along all twelve steps. Its steps carry what the guide's
pages draw (``check_staged``), and its words are held to the house rules and to its dated records in
``fde_sources.py``. The guide's sources and its hub's words (``fde_hub.py``) are checked on every run,
whether or not its steps exist yet. ``test_build_content.py`` feeds the checks a role that keeps every
rule and the same role broken one way at a time.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent

REQUIRED_STEP = {"n", "id", "phase", "title", "when", "purpose", "activities", "ai",
                 "artifact", "template", "prompts", "example", "pitfalls", "done_when"}
REQUIRED_ROLE = {"id", "name", "short", "accent", "tagline", "arc", "intro", "owns",
                 "not_yours", "ai_stance", "reads"}

# What a staged role carries beyond the role format (verdict 2.8). HEAD["stages"] is the framework as
# data: each stage's id, name, object, question, span, the client's people, and what is signed by whom at
# its end, with an optional "brief" for its stage page. Each step names its stage, its altitude ("level",
# None where it has none), the hats it wears, a note for a client inside your own company, the words to
# say, the question it answers, and its artefact's short name, which the framework picture draws.
STAGES = ("frame", "deliver", "evolve")
STAGE_KEYS = {"id", "name", "object", "question", "span", "people", "signed", "signer"}
STAGE_BRIEF = {"long", "people", "think", "ends", "wrong"}
REQUIRED_STAGED_STEP = {"stage", "level", "hats", "internal", "say", "question"}
HATS = ("product", "architect", "engineer", "qa", "platform", "consultant")
# Each altitude and the stage it lives in: a proof of concept in Frame, the rest in Deliver (verdict 2.3).
LEVELS = {"POC": "frame", "MVP": "deliver", "Build": "deliver", "Deploy": "deliver", "MVP, then build": "deliver"}

# role id -> module stem. A role is built when all three of <stem>_a/_b/_c.py exist, so a role in
# progress simply does not appear on the site until its three files land.
STEMS = {
    "product-manager": "product_manager",
    "solution-architect": "solution_architect",
    "engineering": "engineering",
    "qa": "qa",
    "devops": "devops",
    "forward-deployed-engineer": "fde",
}


def discover() -> dict[str, tuple[str, list[str]]]:
    found = {}
    for rid, stem in STEMS.items():
        mods = [f"{stem}_{suffix}" for suffix in ("a", "b", "c")]
        if all((SRC / f"{m}.py").exists() for m in mods):
            found[rid] = (mods[0], mods)
    return found


def in_progress() -> dict[str, list[str]]:
    """Roles with one or two of their three files. None is built; a staged one is checked, so whoever
    writes one of its files hears about its problems before the other two land."""
    found = {}
    for rid, stem in STEMS.items():
        have = [f"{stem}_{suffix}" for suffix in ("a", "b", "c") if (SRC / f"{stem}_{suffix}.py").exists()]
        if 0 < len(have) < 3:
            found[rid] = have
    return found


def load(mod: str) -> dict:
    ns: dict = {}
    exec((SRC / f"{mod}.py").read_text(encoding="utf-8"), ns)  # noqa: S102 - our own authored content
    return ns


def assemble(head_mod: str | None, step_mods: list[str], rid: str | None = None) -> dict:
    """A role as the renderer reads it: the HEAD, then every step of its files in number order."""
    role = dict(load(head_mod)["HEAD"]) if head_mod else {"id": rid}
    steps: list[dict] = []
    for m in step_mods:
        ns = load(m)
        for key in sorted(k for k in ns if k.startswith("STEPS")):
            steps.extend(ns[key])
    role["steps"] = sorted(steps, key=lambda s: s.get("n") or 0)
    return role


def code_problem(body: str, lang: str) -> str | None:
    """A template that says it is code must be code. Angle-bracket placeholders stand in for values."""
    probe = re.sub(r"<[^>\n]{1,60}>", "PLACEHOLDER", body)
    try:
        if lang == "python":
            ast.parse(probe)
        elif lang == "json":
            json.loads(probe)
        elif lang in ("yaml", "yml"):
            try:
                import yaml  # optional; skipped where it is not installed
            except ImportError:
                return None
            yaml.safe_load(probe)
    except Exception as exc:  # noqa: BLE001 - any parse failure is the finding
        return f"{lang} template does not parse: {str(exc).splitlines()[0][:110]}"
    return None


def check(role: dict, partial: bool = False, head: bool = True) -> list[str]:
    """What every role must keep to. An empty list is a pass.

    ``partial`` checks one or two files of a role in progress: each step, and each stage whose steps are
    all there, but not the numbering of the whole. ``head`` says whether the role's HEAD is among them."""
    bad = []
    missing = REQUIRED_ROLE - set(role)
    if missing and head:
        bad.append(f"role {role.get('id')}: missing {sorted(missing)}")
    seen_ids, seen_n = set(), set()
    for s in role["steps"]:
        where = f"{role['id']} step {s.get('n')}"
        m = REQUIRED_STEP - set(s)
        if m:
            bad.append(f"{where}: missing {sorted(m)}")
        if s.get("id") in seen_ids:
            bad.append(f"{where}: duplicate id {s.get('id')}")
        if s.get("n") in seen_n:
            bad.append(f"{where}: duplicate number")
        seen_ids.add(s.get("id")); seen_n.add(s.get("n"))
        if not s.get("activities"):
            bad.append(f"{where}: no activities")
        template = s.get("template") or {}
        if not template.get("body", "").strip():
            bad.append(f"{where}: empty template")
        else:
            problem = code_problem(template["body"], template.get("lang", ""))
            if problem:
                bad.append(f"{where}: {problem}")
        if not s.get("prompts"):
            bad.append(f"{where}: no prompts")
        for p in s.get("prompts") or []:
            if not {"title", "when", "body"} <= set(p):
                bad.append(f"{where}: prompt missing a field")
        if not str(s.get("done_when") or "").strip():
            bad.append(f"{where}: no done_when")
    if not partial:
        if [s.get("n") for s in role["steps"]] != list(range(1, len(role["steps"]) + 1)):
            bad.append(f"{role['id']}: steps are not numbered 1..n in order")
        if len(role.get("arc", [])) != len(role["steps"]):
            bad.append(f"{role['id']}: arc has {len(role.get('arc', []))} labels for {len(role['steps'])} steps")
    if "stages" in role or (not head and any("stage" in s for s in role["steps"])):
        bad += check_staged(role, partial)
    elif any("stage" in s for s in role["steps"]):
        bad.append(f"{role['id']}: its steps name a stage, and its HEAD has no stages")
    return bad


# ------------------------------------------------------------------------------------- staged roles
def _sentences(text: str) -> int:
    """How many sentences: each full stop, question or exclamation mark that ends one, and an unpunctuated
    tail counts as one more."""
    t = text.strip()
    ends = re.findall(r"[.!?][\"'’”)\]]*(?=\s+[A-Z0-9\"'‘“(\[{*]|\Z)", t)
    return len(ends) + (0 if re.search(r"[.!?][\"'’”)\]]*\Z", t) else 1) if t else 0


def _head_words(role: dict) -> list[tuple[str, str, str]]:
    """Every piece of a staged role's HEAD that a page shows, and how: prose (through md(), where marks
    belong) or plain (a name, a label, a line in the framework picture)."""
    out = []
    for k in ("intro", "owns", "not_yours"):
        out += [(f"{k}[{i}]", "prose", t) for i, t in enumerate(role.get(k) or []) if isinstance(t, str)]
    if isinstance(role.get("ai_stance"), str):
        out.append(("ai_stance", "prose", role["ai_stance"]))
    out += [(k, "plain", role[k]) for k in ("name", "short", "tagline") if isinstance(role.get(k), str)]
    out += [(f"arc[{i}]", "plain", t) for i, t in enumerate(role.get("arc") or []) if isinstance(t, str)]
    out += [(f"reads[{i}]", "plain", r[0]) for i, r in enumerate(role.get("reads") or [])
            if isinstance(r, (list, tuple)) and r and isinstance(r[0], str)]
    return out


def _step_words(s: dict) -> list[tuple[str, str, str]]:
    """Every piece of a staged step's words, and how a page shows it: prose (through md(), where marks
    belong), plain (a title, a label, a line someone says), code (a prompt or a Markdown template, copied
    as it stands) or source (a template in a programming language)."""
    out = []

    def add(where: str, kind: str, v) -> None:
        if isinstance(v, str) and v:
            out.append((where, kind, v))

    for k in ("when", "purpose", "internal", "done_when"):
        add(k, "prose", s.get(k))
    for k in ("title", "phase", "question"):
        add(k, "plain", s.get(k))
    for i, a in enumerate(s.get("activities") or [], 1):
        if isinstance(a, dict):
            add(f"activity {i}", "prose", a.get("do"))
            add(f"activity {i} detail", "prose", a.get("detail"))
    for i, a in enumerate(s.get("ai") or [], 1):
        if isinstance(a, dict):
            add(f"ai {i} tool", "plain", a.get("tool"))
            add(f"ai {i}", "prose", a.get("use"))
            add(f"ai {i} caution", "prose", a.get("caution"))
    art = s.get("artifact") if isinstance(s.get("artifact"), dict) else {}
    for k, kind in (("name", "plain"), ("good", "prose"), ("owner", "plain"), ("short", "plain")):
        add(f"artifact {k}", kind, art.get(k))
    template = s.get("template") if isinstance(s.get("template"), dict) else {}
    add("template title", "plain", template.get("title"))
    lang = str(template.get("lang") or "").lower()
    add("template", "code" if lang in ("", "markdown", "md", "text", "txt") else "source", template.get("body"))
    for i, p in enumerate(s.get("prompts") or [], 1):
        if isinstance(p, dict):
            add(f"prompt {i} title", "plain", p.get("title"))
            add(f"prompt {i} when", "plain", p.get("when"))
            add(f"prompt {i}", "code", p.get("body"))
    example = s.get("example") if isinstance(s.get("example"), dict) else {}
    add("example title", "plain", example.get("title"))
    add("example", "prose", example.get("body"))
    for i, p in enumerate(s.get("pitfalls") or [], 1):
        add(f"pitfall {i}", "prose", p)
    for i, x in enumerate(s.get("say") or [], 1):
        if isinstance(x, dict):
            add(f"say {i} to", "plain", x.get("to"))
            add(f"say {i}", "plain", x.get("words"))
    return out


def check_staged(role: dict, partial: bool = False) -> list[str]:
    """What a role in stages owes beyond the role format (verdict 2.8): the stages in order, the phases P0
    to P3 once each inside every stage, the fields its pages draw, and its words held to the house rules
    and to its records. The only staged role is the forward-deployed engineer's guide, so its words are
    held to fde_sources.py."""
    import fde_sources as fs  # noqa: PLC0415 - local so the module stays importable alone

    rid = role["id"]
    bad = []
    steps = sorted(role["steps"], key=lambda s: s.get("n") or 0)

    if "stages" in role:
        stages = role["stages"] if isinstance(role["stages"], list) else []
        ids = [st.get("id") if isinstance(st, dict) else None for st in stages]
        if ids != list(STAGES):
            bad.append(f"{rid}: HEAD stages run {', '.join(STAGES)}, in that order (it has {ids})")
        for st in stages:
            if not isinstance(st, dict):
                continue
            where = f"{rid} stage {st.get('id')}"
            if STAGE_KEYS - set(st):
                bad.append(f"{where}: missing {sorted(STAGE_KEYS - set(st))}")
            if set(st) - STAGE_KEYS - {"brief"}:
                bad.append(f"{where}: unknown fields {sorted(set(st) - STAGE_KEYS - {'brief'})}")
            for k in sorted(STAGE_KEYS - {"id"}):
                if isinstance(st.get(k), str):
                    bad += fs.house(f"{where} {k}", st[k], "plain")
            if "brief" in st:
                brief = st["brief"]
                if not isinstance(brief, dict) or set(brief) != STAGE_BRIEF:
                    bad.append(f"{where}: brief holds exactly {', '.join(sorted(STAGE_BRIEF))}")
                for k, v in (brief.items() if isinstance(brief, dict) else []):
                    if not isinstance(v, str) or not v.strip():
                        bad.append(f"{where} brief {k}: words, not empty")
                    else:
                        bad += fs.house(f"{where} brief {k}", v, "plain")
        arc = role.get("arc") or []
        if partial:
            wrong = [s.get("n") for s in steps if isinstance(s.get("n"), int) and 0 < s["n"] <= len(arc)
                     and arc[s["n"] - 1] != s.get("phase")]
            if wrong:
                bad.append(f"{rid}: arc names steps {wrong} differently from their phase (the short name)")
        elif arc != [s.get("phase") for s in steps]:
            bad.append(f"{rid}: arc is each step's phase (its short name), in step order")
        for where, kind, text in _head_words(role):
            bad += fs.house(f"{rid} {where}", text, kind)

    for s in steps:
        where = f"{rid} step {s.get('n')}"
        missing = REQUIRED_STAGED_STEP - set(s)
        if missing:
            bad.append(f"{where}: missing {sorted(missing)}, which every step of a staged role carries")
        art = s.get("artifact") if isinstance(s.get("artifact"), dict) else {}
        if not isinstance(art.get("short"), str) or not art["short"].strip():
            bad.append(f"{where}: the artifact has no short name, which the framework picture draws")
        if "stage" in s and s["stage"] not in STAGES:
            bad.append(f"{where}: stage {s['stage']!r} is not one of {', '.join(STAGES)}")
        if "level" in s:
            level = s["level"]
            if level is not None and level not in LEVELS:
                bad.append(f"{where}: level {level!r} is None or one of {', '.join(map(repr, LEVELS))}")
            elif level is not None and s.get("stage") in STAGES and LEVELS[level] != s["stage"]:
                bad.append(f"{where}: level {level!r} is an altitude of {LEVELS[level]}, and the step is in {s['stage']}")
        if "hats" in s:
            hats = s["hats"]
            if (not isinstance(hats, list) or not hats or len(set(map(str, hats))) != len(hats)
                    or not set(hats) <= set(HATS)):
                bad.append(f"{where}: hats is one or more of {', '.join(HATS)}, each once (it has {hats!r})")
        if "internal" in s:
            n = _sentences(s["internal"]) if isinstance(s["internal"], str) else 0
            if not 2 <= n <= 4:
                bad.append(f"{where}: internal is two to four sentences (it has {n})")
        if "say" in s:
            say = s["say"]
            if not (isinstance(say, list) and 2 <= len(say) <= 3 and all(
                    isinstance(x, dict) and set(x) == {"to", "words"}
                    and all(isinstance(x[k], str) and x[k].strip() for k in ("to", "words")) for x in say)):
                bad.append(f"{where}: say is two or three entries, each {{'to': ..., 'words': ...}}")
        if "question" in s and not (isinstance(s["question"], str) and s["question"].strip().endswith("?")):
            bad.append(f"{where}: question is the one the step answers, ending in a question mark")
        for part, kind, text in _step_words(s):
            bad += fs.house(f"{where} {part}", text, kind)

    # Inside each stage the phases run P0 to P3, once each, and stage k holds steps 4k-3 to 4k. A phase
    # comes from enrich.PDLC through apply_pdlc; a step it could not place has been reported there.
    by_stage: dict[str, list[dict]] = {}
    for s in steps:
        if s.get("stage") in STAGES:
            by_stage.setdefault(s["stage"], []).append(s)
    for i, stage in enumerate(STAGES):
        got = by_stage.get(stage, [])
        if not got:
            if not partial:
                bad.append(f"{rid}: no step in the stage {stage}")
            continue
        phases = [s.get("pdlc") for s in got]
        if all(p in PHASES for p in phases) and phases != list(PHASES):
            bad.append(f"{rid}: inside {stage} the phases run {' '.join(phases)}; a stage runs P0, P1, P2, P3, "
                       f"once each and in that order")
        numbers = [s.get("n") for s in got]
        want = list(range(4 * i + 1, 4 * i + 5))
        if numbers != want:
            bad.append(f"{rid}: {stage} holds steps {numbers}; stage {i + 1} of {len(STAGES)} holds steps "
                       f"{want[0]} to {want[-1]}")
    order = [STAGES.index(s["stage"]) for s in steps if s.get("stage") in STAGES]
    if any(b < a for a, b in zip(order, order[1:])):
        bad.append(f"{rid}: the stages go backwards along the steps ({' '.join(str(s.get('stage')) for s in steps)}); "
                   f"they run {', '.join(STAGES)}")
    return bad


PHASES = ("P0", "P1", "P2", "P3")


def apply_enrichment(role: dict) -> tuple[int, list[str]]:
    """Attach presentation hints. A hint naming a step that does not exist is a build error."""
    from enrich import ENRICH  # noqa: PLC0415 - local so the module stays importable alone

    ids = {s["id"] for s in role["steps"]}
    bad = [f"{role['id']}: enrichment names step '{sid}', which does not exist"
           for (rid, sid) in ENRICH if rid == role["id"] and sid not in ids]
    n = 0
    for s in role["steps"]:
        hint = ENRICH.get((role["id"], s["id"]))
        if hint:
            s.update(hint)
            n += 1
    return n, bad


def apply_pdlc(role: dict, partial: bool = False) -> list[str]:
    """Join each step to its PDLC phase, exhaustively.

    Partial coverage is the failure that matters here: a step with no phase would
    silently vanish from the journey's arc diagram, and the reader would never know a
    step was missing. So every step must be named exactly once, and every name must be
    a step that exists. A staged role runs the phases once inside each stage, so its
    order is checked stage by stage (check_staged), not here. ``partial`` places the
    steps of a role in progress and stops there.
    """
    from enrich import PDLC, PDLC_ABSENT  # noqa: PLC0415

    rid = role["id"]
    table = PDLC.get(rid)
    if table is None:
        return [f"{rid}: no PDLC phase mapping"]

    staged = "stages" in role or any("stage" in s for s in role["steps"])
    ids = [s.get("id") for s in role["steps"]]
    bad = [] if partial else [f"{rid}: PDLC names step '{sid}', which does not exist"
                              for sid in table if sid not in ids]
    bad += [f"{rid}: step '{sid}' has no PDLC phase" for sid in ids if sid not in table]
    bad += [f"{rid}: step '{sid}' has phase '{ph}', which is not one of {PHASES}"
            for sid, ph in table.items() if ph not in PHASES]
    if bad:
        if staged:
            bad.append(f"{rid}: enrich.PDLC places the steps {', '.join(table)}")
        return bad

    # The journey is read top to bottom, so the phases have to advance and never go
    # back. A non-monotonic mapping would put a P0 step after a P2 one and the phase
    # bands in the walk would read as nonsense.
    if not staged:
        order = {ph: i for i, ph in enumerate(PHASES)}
        seq = [order[table[s["id"]]] for s in role["steps"]]
        if any(b < a for a, b in zip(seq, seq[1:])):
            names = " ".join(table[s["id"]] for s in role["steps"])
            return [f"{rid}: PDLC phases go backwards along the step order: {names}"]

    for s in role["steps"]:
        s["pdlc"] = table[s["id"]]
    if partial:
        return []
    covered = {s["pdlc"] for s in role["steps"]}
    role["pdlc_absent"] = {ph: PDLC_ABSENT.get((rid, ph), "")
                           for ph in PHASES if ph not in covered}
    missing_copy = [ph for ph, txt in role["pdlc_absent"].items() if not txt]
    return [f"{rid}: phase {ph} has no step and no line saying what happens there instead"
            for ph in missing_copy]


def check_guide(fde: dict | None = None) -> tuple[list[str], list[str]]:
    """The FDE guide's dated records and its hub's words: problems, then warnings (a record past its
    sixty days). ``fde`` is the guide's role when this run built it."""
    import fde_hub  # noqa: PLC0415
    import fde_sources  # noqa: PLC0415

    return fde_sources.check() + fde_hub.check(fde), fde_sources.warnings()


def main() -> int:
    problems, built, checked = [], [], []
    roles = discover()
    started = in_progress()
    skipped = sorted(set(STEMS) - set(roles) - set(started))
    fde = None
    for rid, (head_mod, step_mods) in roles.items():
        role = assemble(head_mod, step_mods)
        n_hint, hint_problems = apply_enrichment(role)
        problems += hint_problems
        problems += apply_pdlc(role)
        problems += check(role)
        if problems:
            continue
        path = OUT / f"{rid}.json"
        path.write_text(json.dumps(role, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        n_p = sum(len(s["prompts"]) for s in role["steps"])
        n_a = sum(len(s["activities"]) for s in role["steps"])
        n_fig = sum(1 for s in role["steps"] if s.get("figure"))
        n_cal = sum(1 for s in role["steps"] if s.get("calc"))
        built.append(f"  {rid}.json — {len(role['steps'])} steps, {n_a} activities, "
                     f"{n_p} prompts, {len(role['steps'])} templates, "
                     f"{n_fig} figures, {n_cal} calculators ({path.stat().st_size:,} bytes)")
        if "stages" in role:
            fde = role if rid == "forward-deployed-engineer" else fde
            built.append("    stages: " + " · ".join(
                f"{st} {sum(1 for s in role['steps'] if s['stage'] == st)} steps, "
                f"{sum(len(s['prompts']) for s in role['steps'] if s['stage'] == st)} prompts" for st in STAGES))
    for rid, mods in started.items():
        stem = STEMS[rid]
        head_mod = f"{stem}_a" if f"{stem}_a" in mods else None
        role = assemble(head_mod, [m for m in mods], rid)
        if not ("stages" in role or any("stage" in s for s in role["steps"])):
            skipped.append(rid)        # an unstaged role in progress waits unchecked, as before
            continue
        found = apply_pdlc(role, partial=True) + check(role, partial=True, head=head_mod is not None)
        problems += found
        numbers = [s.get("n") for s in role["steps"] if isinstance(s.get("n"), int)]
        span = f"steps {min(numbers)} to {max(numbers)}" if numbers else "no steps"
        waiting = [f"{stem}_{x}" for x in ("a", "b", "c") if f"{stem}_{x}" not in mods]
        checked.append(f"  {rid}: {', '.join(mods)}, {span}, {len(found)} problems; "
                       f"built when {' and '.join(waiting)} land")
    guide_problems, guide_warnings = check_guide(fde)
    problems += guide_problems
    if problems:
        print("content problems:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1
    print("\n".join(["built:"] + built))
    if checked:
        print("\n".join(["checked, not built yet:"] + checked))
    if skipped:
        print("not yet authored: " + ", ".join(sorted(skipped)))
    from fde_sources import QUOTES, SOURCES  # noqa: PLC0415
    print(f"the FDE guide: {len(SOURCES)} sources and {len(QUOTES)} quotations on record; the hub's words checked")
    for w in guide_warnings:
        print("  warning: " + w)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
