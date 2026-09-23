"""The homepage boards.

Three illustrations, in the order a newcomer needs them: the lifecycle itself, the same
lifecycle seen from each chair, and the division of labour between a person and a model
inside it. Content here is the wiki's canonical spine and the roles' own step data, so
the pictures cannot drift from the prose.
"""
from __future__ import annotations

from . import dg

# --------------------------------------------------------------------------- A · the spine
PHASES = [
    ("slate", "P0 · Frame", "product manager", "frame", "Decide whether to build it at all.",
     [("Pain register", "one line, a count, a cost"),
      ("AI-fit verdict", "naming what was rejected, and why"),
      ("Autonomy ceiling", "how much the machine may do")],
     ("You leave with", ["A pain that is a measurement",
                         "A verdict with an alternative named",
                         "A ceiling, in writing"])),
    ("indigo", "P1 · Design & Spec", "solution architect", "blueprint",
     "Decide exactly what, and under whose authority.",
     [("Eight-field spec", "what a machine can build from"),
      ("A bar per slice", "derived from damage over saving"),
      ("Authority budget", "what it may do unasked, and where it stops")],
     ("You leave with", ["A signed spec", "A bar per slice, not one bar",
                         "A named approver per gate"])),
    ("teal", "P2 · Build & Prove", "engineering lead", "prove",
     "Prove it meets the bar, slice by slice.",
     [("Bolts, not sprints", "ten days, one owner, one artefact"),
      ("Golden set in CI", "a required check, run in cost order"),
      ("Shadow run", "beside the desk, not instead of it")],
     ("You leave with", ["Evidence at the bar",
                         "A lower bound, never a score",
                         "A shadow run that agrees"])),
    ("amber", "P3 · Run & Learn", "the sponsor", "gauge",
     "Watch it, cost it, and feed the next frame.",
     [("Trace and drift", "the three signals a normal stack lacks"),
      ("The bill, by factor", "context, tier, cache, attempts"),
      ("Two-number report", "and the brief the next P0 starts from")],
     ("You leave with", ["Two numbers, not a dashboard",
                         "A drift readout",
                         "The next P0 brief, with an owner"])),
]


def pdlc() -> str:
    cols = [dg.column(h, n, b, i, t, s, k) for h, n, b, i, t, s, k in PHASES]
    inner = dg.flow(cols, gate_after=1) + dg.returns(
        "production is where the next frame comes from: incident, drift, cost")
    return dg.board(
        "The spine", "The agentic PDLC",
        "Four phases, one hard gate, and a line that comes back. Everything else on this "
        "site hangs off this picture.",
        inner,
        note="<b>Why the gate sits there.</b> P0 and P1 are cheap to get wrong on paper and "
             "expensive to get wrong in production. That asymmetry is the whole argument for "
             "the phases. P1 to P2 is the one crossing nothing downstream survives without: "
             "the spec, the bar per slice and the authority budget are signed before a line "
             "of the agent is written. The other three crossings are soft, and the dashed "
             "return line at the bottom is the one teams forget to build.",
        bid="pdlc")


# --------------------------------------------------------------------------- B · by role
COLS = [("slate", "P0 · Frame", "Is this worth doing, and is it AI at all?"),
        ("indigo", "P1 · Design & Spec", "What exactly, and under whose authority?"),
        ("teal", "P2 · Build & Prove", "Does it meet the bar, slice by slice?"),
        ("amber", "P3 · Run & Learn", "Is it still doing it, and what did it cost?")]

ROWS = [
    {"name": "Product manager", "note": "accountable for P0", "accent": "var(--slate)", "cells": [
        {"own": True, "head": "Measure the pain, rule on AI-fit",
         "sub": "Pain register · AI-fit record · autonomy ceiling", "href": "product-manager/#discover"},
        {"head": "Write the spec, set the bar",
         "sub": "Eight fields, and a bar derived per slice", "href": "product-manager/#specify"},
        {"head": "Hold the three gates that are yours",
         "sub": "A gate is defined by a name on it", "href": "product-manager/#gate"},
        {"head": "Shadow, five percent, then widen",
         "sub": "Then two numbers and the next brief", "href": "product-manager/#launch"}]},
    {"name": "Solution architect", "note": "accountable for P1", "accent": "var(--ochre)", "cells": [
        {"head": "Credit every line back to a person",
         "sub": "Constraint register, sorted by type", "href": "solution-architect/#elicit"},
        {"own": True, "head": "Map the chain, bound the authority",
         "sub": "Exact / best-guess / consequential · ADRs · gate map",
         "href": "solution-architect/#map"},
        {"head": "Answer against the map",
         "sub": "Decisions here are read, not re-opened", "href": "solution-architect/#decide"},
        {"head": "Make it cheap, auditable, redesignable",
         "sub": "Caching, routing, the missing-control finding",
         "href": "solution-architect/#evolve"}]},
    {"name": "Engineering lead", "note": "accountable for P2", "accent": "var(--sage)", "cells": [
        {"quiet": True, "head": "Deliberately not yet on the clock",
         "sub": "Reads the brief, sizes the unknowns, starts nothing"},
        {"head": "Context file, then the boundary line",
         "sub": "The never-touch list and what it must refuse", "href": "engineering/#prepare"},
        {"own": True, "head": "Floor first, then model, then checker",
         "sub": "Bolts · harness in CI · shadow behind a flag", "href": "engineering/#floor"},
        {"head": "Cache, route, trace, keep the ledger",
         "sub": "And the injection suite that never stops running", "href": "engineering/#operate"}]},
    {"name": "QA lead", "note": "proof, throughout", "accent": "var(--plum)", "cells": [
        {"quiet": True, "head": "Asks the one question early",
         "sub": "What will right mean, and who says so?"},
        {"head": "Decide what proof each step owes",
         "sub": "Proof map · bar sheet · the golden set", "href": "qa/#define"},
        {"head": "Wire the proof in so it cannot be skipped",
         "sub": "A required check, and a lower bound not a score", "href": "qa/#harness"},
        {"head": "Watch drift, turn incidents into controls",
         "sub": "The postmortem that names the missing control", "href": "qa/#watch"}]},
    {"name": "DevOps and platform", "note": "the floor under all four", "accent": "var(--violet)",
     "cells": [
        {"head": "Account, tags and budget before the first call",
         "sub": "Landing zone and a cost baseline", "href": "devops/#baseline"},
        {"head": "One gateway, comparable environments",
         "sub": "Model access matrix, version pinned", "href": "devops/#access"},
        {"head": "Make the harness unbypassable",
         "sub": "A required status check, and a flag to ship behind", "href": "devops/#pipeline"},
        {"head": "Three signals, smallest identity, rehearsed rollback",
         "sub": "Trace · cost record · alarms · containment", "href": "devops/#observe"}]},
]


def by_role() -> str:
    m = dg.matrix(COLS, ROWS, legend="the bar marks the phase this role is accountable for")
    return dg.board(
        "The same ninety days, five chairs", "Your role, across the four phases",
        "One row per role, one column per phase. Read across to see your own arc; read "
        "down to see who else is in the room when yours is the hard part.",
        m,
        note="<b>Two things this chart is honest about.</b> The dashed cells are not gaps in "
             "the manual, they are the point: an engineering lead who opens a branch in P0 and "
             "a QA lead who arrives in P2 are the two most expensive habits in agentic "
             "delivery. And P3 is accountable to nobody on this chart — it belongs to the "
             "sponsor, which is why it has its own page.",
        bid="by-role")


# --------------------------------------------------------------------------- C · the split
LANES = [
    ("slate", "P0", "Frame", "Pain, AI-fit and the ceiling", [
        ("green", "The model drafts", [
            "Distinct pains from six transcripts, deduplicated",
            "Counts from a ticket export, with the script it ran",
            "Cost-per-case arithmetic, assumptions in named cells"], False),
        ("indigo", "You check", [
            "Every line still carries the name of who said it",
            "The script counted the right date column",
            "A sceptic can move one cell and watch the answer move"], False),
        ("rose", "Never delegated", [
            "Which pain is worth solving",
            "Whether a wrong action can be undone",
            "The autonomy level itself"], True)]),
    ("indigo", "P1", "Design & Spec", "Spec, bar and authority", [
        ("green", "The model drafts", [
            "The constraint register, sorted by type",
            "A first pass at the agent map, every step tagged",
            "The eight-field spec from the brief and the notes"], False),
        ("indigo", "You check", [
            "The register separates real constraints from habits",
            "A $400 threshold is policy, not folklore",
            "Each bar was derived from two money figures, not chosen"], False),
        ("rose", "Never delegated", [
            "The read-back, to the person who said it",
            "What counts as money",
            "The bar and the autonomy fields"], True)]),
    ("teal", "P2", "Build & Prove", "Floor, harness and shadow", [
        ("green", "The model drafts", [
            "The deterministic floor from the exact-code inventory",
            "Checker implementations and a first judge rubric",
            "Golden-set candidates pulled from real traffic"], False),
        ("indigo", "You check", [
            "The boundary line says what the system must refuse",
            "The judge agrees with human labels on a fresh sample",
            "The harness runs in cost order and blocks the merge"], False),
        ("rose", "Never delegated", [
            "The never-touch list",
            "The expected outcome on every golden case",
            "The verdict: proven, failed or unproven"], True)]),
    ("amber", "P3", "Run & Learn", "Trace, bill and the next brief", [
        ("green", "The model drafts", [
            "The trace schema and a starting alarm set",
            "The bill decomposed into its four factors",
            "A draft of the two-number report"], False),
        ("indigo", "You check", [
            "The factors multiply back to the bill you were sent",
            "The blast radius of each new permission is named",
            "Drift is measured against the launch set, not last week"], False),
        ("rose", "Never delegated", [
            "What is masked and what is kept",
            "Declaring the incident over",
            "What the sponsor sees"], True)]),
]


def delegation() -> str:
    b = dg.bands([dg.band(h, k, n, s, lanes) for h, k, n, s, lanes in LANES])
    return dg.board(
        "What actually changed", "Where the model helps, and where it must not",
        "The machine took the drafting. It did not take the judgement — it concentrated "
        "it. Every step in this manual names a tool, a use, a caution, and exactly one "
        "thing that is never delegated.",
        b,
        note="<b>Read the red column first.</b> Forty steps across five roles produce forty "
             "of those lines, and they have a shape: every one is a fact about your business, "
             "your regulator or your ledger that no amount of context makes knowable from "
             "outside. That is the job now — not less judgement, the same judgement "
             "concentrated into fewer and larger decisions, each with a name on it.",
        bid="delegation")


# --------------------------------------------------------------------------- D · the loops
# Geometry, stated once so the drawing below is readable. Four phase nodes on a spine;
# forward loops arc over it, loops that close inside a phase dip just under it, and the
# three that run backwards swing deep below — which is the whole point of the picture.
_PX = [("slate", "P0", "Frame", 150), ("indigo", "P1", "Design & Spec", 420),
       ("teal", "P2", "Build & Prove", 690), ("amber", "P3", "Run & Learn", 960)]
_NW, _TOP, _BOT = 190, 150, 212


def _tag(x: float, y: float, text: str, colour: str, weight: int = 600,
         anchor: str = "middle") -> str:
    """A label that has to survive sitting on top of a curve: it carries its own backing."""
    w = len(text) * 5.7 + 14
    x0 = x - w / 2 if anchor == "middle" else (x - 7 if anchor == "start" else x - w + 7)
    return (f'<rect x="{x0:.0f}" y="{y - 10:.0f}" width="{w:.0f}" height="14" rx="4" '
            f'fill="var(--bone)"/>'
            f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-size="10.5" '
            f'font-weight="{weight}" fill="{colour}">{dg.E(text)}</text>')


def _loops_svg() -> str:
    ink, rose, violet = "var(--soft)", "var(--dg-rose)", "var(--dg-violet)"
    o = ['<defs>']
    for name, col in (("ai", ink), ("ar", rose), ("av", violet)):
        o.append(f'<marker id="{name}" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" '
                 f'orient="auto"><path d="M0 0.5 L8.5 4.5 L0 8.5 z" fill="{col}"/></marker>')
    o.append("</defs>")

    # governance spans the whole line and belongs to nobody who builds
    o.append('<g data-loop="governance">'
             f'<path d="M150 46 V32 H960 V46" fill="none" stroke="{violet}" stroke-width="1.6" '
             f'stroke-dasharray="5 4" marker-end="url(#av)"/>'
             + _tag(555, 36, "Governance  ·  P0 → P3  ·  the sponsor's", violet, 700) + "</g>")

    # the phases
    for hue, key, name, cx in _PX:
        c = f"var(--dg-{hue})"
        o.append(f'<rect x="{cx - _NW // 2}" y="{_TOP}" width="{_NW}" height="{_BOT - _TOP}" '
                 f'rx="12" fill="{c}"/>')
        o.append(f'<text x="{cx}" y="{_TOP + 26}" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="var(--dg-on)">{key}</text>')
        o.append(f'<text x="{cx}" y="{_TOP + 45}" text-anchor="middle" font-size="12" '
                 f'fill="var(--dg-on)" opacity=".96">{dg.E(name)}</text>')

    # forward: they close on their own, because somebody downstream is waiting
    for (a, b), name in zip([(150, 420), (420, 690), (690, 960)],
                            ["Requirements · P0 → P1", "Spec · P1 → P2", "Trust · P2 → P3"]):
        o.append(f'<path d="M{a} {_TOP} C{a} 66 {b} 66 {b} {_TOP}" fill="none" stroke="{ink}" '
                 f'stroke-width="1.6" marker-end="url(#ai)"/>')
        o.append(_tag((a + b) / 2, 80, name, "var(--ink2)"))

    # closes inside its own phase
    for cx, name in ((420, "Decision · P1 → P1"), (690, "Delivery · P2 → P2")):
        o.append(f'<path d="M{cx - 34} {_BOT} C{cx - 34} 250 {cx + 34} 250 {cx + 34} {_BOT}" '
                 f'fill="none" stroke="{ink}" stroke-width="1.6" marker-end="url(#ai)"/>')
        o.append(_tag(cx + 46, 245, name, "var(--ink2)", anchor="start"))

    # backwards: the three teams forget, drawn deep and kept moving
    o.append('<g data-loop="cost">'
             f'<path class="fl" d="M960 {_BOT} C960 312 366 312 366 {_BOT}" fill="none" '
             f'stroke="{rose}" stroke-width="1.9" marker-end="url(#ar)"/>'
             + _tag(600, 292, "Cost · P3 → P1", rose, 700) + "</g>")
    o.append('<g data-loop="incident">'
             f'<path class="fl" d="M960 {_BOT} C960 356 150 356 150 {_BOT}" fill="none" '
             f'stroke="{rose}" stroke-width="1.9" marker-end="url(#ar)"/>'
             + _tag(555, 336, "Incident · P3 → P0", rose, 700) + "</g>")
    return dg.svg(1120, 372, "".join(o),
                  "Four phases on a line. Five loops close forwards or inside a phase; cost, "
                  "incident and governance run backwards across it.")


BACKWARD = [
    {"hue": "rose", "key": "P3 → P1", "name": "Cost", "loop": "cost",
     "body": "A bill that left its estimate is a design question, not a finance question. "
             "It closes when an architecture decision record changes, not when a budget does.",
     "meta": [("Owner", "Solution architect"), ("Closed when", "An ADR has a v2 with a diff"),
              ("Confidence", "documented")]},
    {"hue": "rose", "key": "P3 → P0", "name": "Incident", "loop": "incident",
     "body": "A postmortem that does not produce a brief has not finished. The finding is the "
             "control that would have made the incident impossible, named.",
     "meta": [("Owner", "Every role"), ("Closed when", "A next-P0 brief exists, with an owner"),
              ("Confidence", "established")]},
    {"hue": "violet", "key": "P0 → P3", "name": "Governance", "loop": "governance",
     "body": "Spans the whole line and belongs to the sponsor, not to any delivery role. It is "
             "the only loop with nobody downstream waiting, which is why it is the one most "
             "often absent.",
     "meta": [("Owner", "Sponsor"), ("Closed when", "The four leadership decisions are dated"),
              ("Confidence", "working method")]},
]


def loops() -> str:
    inner = (_loops_svg()
             + dg.section_band("The three that run backwards")
             + dg.cards(BACKWARD))
    return dg.board(
        "The spine, continued", "Eight loops make the line a ring",
        "Each loop opens in one phase and closes in a later one. Five close forwards or "
        "inside a phase and look after themselves, because somebody downstream is waiting "
        "and will chase. Three run backwards, and nobody is waiting.",
        inner,
        note="<b>The test for a loop that exists.</b> For each of the three backwards loops, "
             "name the person. Not the team, the person. If you cannot, the loop is absent — "
             "and absent is the honest word, not <em>informal</em>. A loop is closed when an "
             "artefact in the opening phase has changed because of evidence from the closing "
             "one, and you can show the diff.",
        bid="loops")
