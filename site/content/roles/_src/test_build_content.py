#!/usr/bin/env python3
"""Offline tests for the role builder's staged mode, the FDE guide's records and its hub's words.

    python3.12 site/content/roles/_src/test_build_content.py

A staged role built here in code keeps every rule. The same role, broken one way at a time, must fail with
its own message: its phases going backwards inside a stage, a quotation that is not a record, a quotation
typed between quotation marks, a missing staged field, a word the house does not use. The five existing roles
must rebuild to their JSON files byte for byte. Nothing here writes a file.
"""
from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_content as bc  # noqa: E402
import enrich  # noqa: E402
import fde_hub  # noqa: E402
import fde_sources as fs  # noqa: E402

SHORT = {"qualify": "Qualify", "scope": "Scope", "prove": "Prove", "decide": "Decide",
         "mobilise": "Mobilise", "sign": "Sign", "build": "Build", "hand-over": "Hand over",
         "reframe": "Reframe", "codify": "Codify", "reuse": "Reuse", "review": "Review"}
LEVEL = {3: "POC", 5: "MVP", 6: "MVP", 7: "MVP, then build", 8: "Deploy"}


def step(n: int, sid: str) -> dict:
    stage = bc.STAGES[(n - 1) // 4]
    return {
        "n": n, "id": sid, "phase": SHORT[sid], "stage": stage, "level": LEVEL.get(n), "hats": ["consultant", "qa"],
        "title": f"Do the work of step {n}", "when": f"{stage.title()}, in its own week",
        "purpose": "A purpose in plain words, citing a source [[S12]] and quoting one: {{S24-ground}}.",
        "activities": [{"do": "Do one thing", "detail": "Why it matters, in one sentence."}],
        "ai": [{"tool": "Do not delegate", "use": "The decision that is theirs.", "caution": None}],
        "artifact": {"name": f"{SHORT[sid]} sheet", "good": "One page a stranger can read.",
                     "owner": "Forward-deployed engineer", "short": f"{SHORT[sid]} sheet"},
        "template": {"title": f"{SHORT[sid]} sheet", "lang": "markdown",
                     "body": "# <title>\n- **Out:** <...>\n| Item | Owner |\n|------|-------|\n"},
        "prompts": [{"title": "Draft it", "when": "Before the meeting",
                     "body": 'Draft the sheet from my notes.\n- list every "assumed" number\n<paste>'}],
        "example": {"title": "SkyWays, three weeks before day 1", "body": "The desk agreed on 184 of 200 cases."},
        "pitfalls": ["Writing it after the meeting."],
        "done_when": "A colleague can read it cold.",
        "internal": "Inside your own company the sponsor is often your manager's peer. Write the noes down first.",
        "say": [{"to": "A date the scope cannot meet", "words": "We can meet that date with the first slice."},
                {"to": "A decision that is theirs", "words": "Your compliance officer signs it, because it is your risk."}],
        "question": f"Is step {n} worth doing?",
    }


def staged_role() -> dict:
    """The guide's shape, every rule kept: three stages, four steps each, P0 to P3 inside each."""
    ids = list(enrich.PDLC["forward-deployed-engineer"])
    stage = lambda sid, name, obj: {"id": sid, "name": name, "object": obj, "question": "What is it for?",
                                    "span": "Days", "people": "The client's people watch.",
                                    "signed": "the go decision", "signer": "the client's sponsor"}
    return {
        "id": "forward-deployed-engineer", "name": "Forward-deployed engineer", "short": "FDE", "accent": "#1E7FA8",
        "tagline": "From a customer's pain to a system they run after you leave",
        "arc": [SHORT[i] for i in ids],
        "stages": [stage("frame", "Frame", "the engagement"), stage("deliver", "Deliver", "the system"),
                   dict(stage("evolve", "Evolve", "the relationship"),
                        brief={"long": "Months.", "people": "Run it.", "think": "The portfolio.",
                               "ends": "The next frame.", "wrong": "The review nobody holds."})],
        "intro": ["You are an engineer who works inside someone else's organisation."],
        "owns": ["The **engagement's spec**"], "not_yours": ["**Their limits**"],
        "ai_stance": "Use a model to go faster through the work that is yours.",
        "reads": [["The lesson: what is an FDE?", "../learn/what-is-a-forward-deployed-engineer/"]],
        "steps": [step(n, sid) for n, sid in enumerate(ids, 1)],
    }


def build(role: dict) -> list[str]:
    """What main() does to a role, without writing it."""
    _n, bad = bc.apply_enrichment(role)
    return bad + bc.apply_pdlc(role) + bc.check(role)


def fails(role: dict, *words: str) -> None:
    bad = build(role)
    text = "\n".join(bad)
    assert bad, "expected a problem, found none"
    for w in words:
        assert w in text, f"expected {w!r} in:\n{text}"


# ------------------------------------------------------------------------------------- the staged role
def test_a_staged_role_that_keeps_every_rule_passes():
    role = staged_role()
    assert build(role) == [], build(role)
    assert [s["pdlc"] for s in role["steps"]] == ["P0", "P1", "P2", "P3"] * 3
    assert role["pdlc_absent"] == {}
    hint = {s["id"]: (s.get("calc"), s.get("figure")) for s in role["steps"]}
    assert hint["prove"] == ("proof", None) and hint["decide"] == ("value", None)
    assert hint["hand-over"] == (None, "shadow_widen")


def test_phases_going_backwards_inside_a_stage_fail():
    role = staged_role()                       # the writer numbers Scope before Qualify
    role["steps"][0]["n"], role["steps"][1]["n"] = 2, 1
    role["steps"].sort(key=lambda s: s["n"])
    role["arc"][0], role["arc"][1] = role["arc"][1], role["arc"][0]
    fails(role, "inside frame the phases run P1 P0 P2 P3")


def test_phases_going_backwards_fail_in_check_alone():
    role = staged_role()
    assert build(role) == []
    role["steps"][5]["pdlc"], role["steps"][6]["pdlc"] = "P2", "P1"
    assert any("inside deliver the phases run P0 P2 P1 P3" in p for p in bc.check(role)), bc.check(role)


def test_stages_out_of_order_fail():
    role = staged_role()
    role["stages"][0], role["stages"][1] = role["stages"][1], role["stages"][0]
    fails(role, "HEAD stages run frame, deliver, evolve")
    role = staged_role()
    for s in role["steps"][:4]:
        s["stage"] = "deliver"
    for s in role["steps"][4:8]:
        s["stage"] = "frame"
    fails(role, "the stages go backwards", "frame holds steps [5, 6, 7, 8]")


def test_a_quotation_that_is_not_a_record_fails():
    role = staged_role()
    role["steps"][4]["example"]["body"] += " Their head of FDE said {{S24-made-up}}."
    fails(role, "no quotation record S24-made-up", "records of S24: S24-ground")
    role = staged_role()
    role["steps"][0]["purpose"] = "Claims about the profession are cited [[S99]]."
    fails(role, "no source S99")


def test_a_typed_quotation_fails():
    role = staged_role()
    role["steps"][2]["purpose"] = "Palantir's bootcamp is the model: “Develop initial use cases in the software”."
    fails(role, "a quotation typed between quotation marks")
    role = staged_role()
    role["steps"][2]["say"][0]["words"] = 'I would say "not yet".'
    fails(role, "step 3 say 1: a quotation typed")


def test_marks_in_the_papers_form_or_the_wrong_place_fail():
    for bad_mark in ("[S12]", "{q:S14-use-cases}", "{{S12}}", "[[S24-ground]]"):
        role = staged_role()
        role["steps"][0]["purpose"] = f"A claim {bad_mark}."
        fails(role, "a mark that is not")
    role = staged_role()
    role["steps"][0]["question"] = "Is {{S4-handoff}} met?"
    fails(role, "a mark belongs in prose")
    role = staged_role()
    role["steps"][0]["template"]["body"] += "\nSee [[S12]].\n"
    fails(role, "copied as it stands")


def test_the_house_rules_hold_and_a_quotation_is_exempt():
    role = staged_role()                      # the record's American spelling is the source's own
    role["steps"][9]["purpose"] = "Ramp names the cost: {{S18-pollute}}."
    assert build(role) == []
    for words, why in (("A customization nobody asked for.", "an American spelling"),
                       ("Leverage the harness.", "a banned word"), ("A holistic review.", "a banned word"),
                       ("The proof \u2014 and its limits.", "a dash"), ("The proof - and its limits.", "a dash"),
                       ("Ask Sonnet to draft it.", "a model name"), ("As the hero's flight shows.", "hero"),
                       ("Then play Ninety Days.", "the game's title")):
        role = staged_role()
        role["steps"][3]["pitfalls"] = [words]
        fails(role, why)
    role = staged_role()                      # a hyphen opening a template's list line is not a dash
    role["steps"][3]["template"]["body"] = "# Readout\n- **Go:** <...>\n  - nested <...>\n"
    assert build(role) == []
    role["steps"][3]["template"]["body"] = "# Readout\nGo - or stop.\n"     # one between words is
    fails(role, "step 4 template: a dash")
    role = staged_role()                      # in a template that is code, a spaced hyphen is a minus sign
    role["steps"][2]["template"] = {"title": "Lower bound", "lang": "python",
                                    "body": "low = p - 1.96 * (p * (1 - p) / n) ** 0.5\n"}
    assert build(role) == []
    role["steps"][2]["template"]["body"] += "# the bound \u2014 per slice\n"
    fails(role, "step 3 template: a dash")
    role = staged_role()                      # the case's own dollar figures are the case
    role["steps"][5]["example"]["body"] = "On day 6 compliance signed a named approver for every refund over $400."
    assert build(role) == []


def test_the_staged_fields_are_required_and_shaped():
    for change, why in ((lambda s: s.pop("say"), "missing ['say']"),
                        (lambda s: s.pop("level"), "missing ['level']"),
                        (lambda s: s["artifact"].pop("short"), "no short name"),
                        (lambda s: s.update(hats=["QA"]), "hats is one or more of"),
                        (lambda s: s.update(hats=[]), "hats is one or more of"),
                        (lambda s: s.update(level="Deploy"), "is an altitude of deliver, and the step is in frame"),
                        (lambda s: s.update(level="Prototype"), "is None or one of"),
                        (lambda s: s.update(stage="build"), "is not one of frame, deliver, evolve"),
                        (lambda s: s.update(internal="One sentence only."), "two to four sentences (it has 1)"),
                        (lambda s: s.update(internal="One. Two. Three. Four. Five."), "two to four sentences (it has 5)"),
                        (lambda s: s.update(say=s["say"][:1]), "say is two or three entries"),
                        (lambda s: s.update(say=[{"to": "x", "said": "y"}] * 2), "say is two or three entries"),
                        (lambda s: s.update(question="Is it worth doing"), "ending in a question mark")):
        role = staged_role()
        change(role["steps"][0])
        fails(role, why)
    role = staged_role()
    role["stages"][2]["brief"].pop("wrong")
    fails(role, "brief holds exactly")
    role = staged_role()
    role["arc"][7] = "Handover"
    fails(role, "arc is each step's phase")
    role = staged_role()
    role.pop("stages")
    fails(role, "its steps name a stage, and its HEAD has no stages")


def test_one_file_of_a_role_in_progress_is_checked_alone():
    deliver = [copy.deepcopy(s) for s in staged_role()["steps"][4:8]]
    role = {"id": "forward-deployed-engineer", "steps": deliver}
    assert bc.apply_pdlc(role, partial=True) + bc.check(role, partial=True, head=False) == []
    role = {"id": "forward-deployed-engineer", "steps": copy.deepcopy(deliver)}
    role["steps"][3]["id"] = "handover"        # not the id enrich.PDLC places
    bad = bc.apply_pdlc(role, partial=True)
    assert any("step 'handover' has no PDLC phase" in p for p in bad), bad
    role = {"id": "forward-deployed-engineer", "steps": copy.deepcopy(deliver)}
    for s, n in zip(role["steps"], (1, 2, 3, 4)):
        s["n"] = n                             # Deliver's steps numbered as if they were Frame's
    bc.apply_pdlc(role, partial=True)
    assert any("deliver holds steps [1, 2, 3, 4]" in p for p in bc.check(role, partial=True, head=False))


# ------------------------------------------------------------------------------------- the five roles
def test_the_five_roles_rebuild_byte_for_byte():
    for rid, (head_mod, step_mods) in bc.discover().items():
        if rid == "forward-deployed-engineer":
            continue
        role = bc.assemble(head_mod, step_mods)
        assert build(role) == [], (rid, build(role))
        made = json.dumps(role, indent=1, ensure_ascii=False) + "\n"
        assert made == (bc.OUT / f"{rid}.json").read_text(encoding="utf-8"), f"{rid}.json would change"


def test_a_stem_without_files_is_skipped():
    if not any((HERE / f"fde_{x}.py").exists() for x in "abc"):
        assert "forward-deployed-engineer" not in bc.discover()
        assert "forward-deployed-engineer" not in bc.in_progress()


# ------------------------------------------------------------------------------------- records and hub
def test_the_records_and_the_hub_keep_their_rules():
    assert fs.check() == [], fs.check()
    assert fde_hub.check() == [], fde_hub.check()
    assert len(fs.SOURCES) == 29 and all(q["source"] in fs.SOURCES for q in fs.QUOTES.values())


def test_the_hub_refuses_what_does_not_exist():
    keep = copy.deepcopy(fde_hub.SECTIONS)
    try:
        fde_hub.SECTIONS[0]["quotes"].append("S1-made-up")
        fde_hub.SECTIONS[5]["facts"].append(["no-such-fact"])
        fde_hub.SECTIONS[1]["rows"][0]["steps"] = [1, 2, 9]
        fde_hub.SECTIONS[2]["after"] += " A robust proof."
        bad = "\n".join(fde_hub.check())
        for w in ("no quotation record S1-made-up", "no fact no-such-fact", "product-manager has no step 9",
                  "does not say steps [1, 2, 9]", "a banned word", "says 6 dated facts, and the list holds 7"):
            assert w in bad, f"expected {w!r} in:\n{bad}"
    finally:
        fde_hub.SECTIONS[:] = keep


def test_the_hub_agrees_with_the_built_guide():
    role = staged_role()
    assert build(role) == []
    assert fde_hub.check(role) == [], fde_hub.check(role)
    role["steps"][6]["level"] = "MVP"           # step 7 sits in the Build column too
    assert any("step 7's level is 'MVP'" in p for p in fde_hub.check(role))


def test_marks_render_with_their_dated_sources():
    marks = fs.Marks()
    html = marks.inline("<p>As they put it {{S24-ground}}, and as Palantir does [[S12]]. Again [[S24]].</p>")
    assert "<q>doesn&#x27;t match" not in html and "<q>doesn't match the data/system reality on the ground</q>" in html
    assert 'href="#src-S24"' in html and ">1</a>" in html and ">2</a>" in html and html.count(">1</a>") == 2
    foot = marks.foot()
    assert foot.index('id="src-S24"') < foot.index('id="src-S12"')
    assert fs.plain("It {{S4-handoff}} [[S4]].") == "It “ready for handoff”."


def test_a_date_turns_amber_after_sixty_days():
    keep = os.environ.get("TOOLS_TODAY")
    try:
        os.environ["TOOLS_TODAY"] = "2026-12-01"            # sixty days after the check
        assert 'class="stale"' not in fs.cite("S1") and not fs.warnings()
        os.environ["TOOLS_TODAY"] = "2026-12-02"            # sixty-one
        cite = fs.cite("S1")
        assert 'class="stale"' in cite and "checked 2 Oct 2026" in cite and "jobs.ashbyhq.com" in cite
        assert "OpenAI" in cite and 'href="https://jobs.ashbyhq.com/openai/' in cite
        assert len(fs.warnings()) == 29
    finally:
        if keep is None:
            os.environ.pop("TOOLS_TODAY", None)
        else:
            os.environ["TOOLS_TODAY"] = keep


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} tests passed")
