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
