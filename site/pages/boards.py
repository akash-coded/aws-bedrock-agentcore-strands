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
                         "A ceiling, in writing"]),
     "learn/p0-frame/",
     "Decide whether to build it at all, and whether it is AI at all. The product manager "
     "owns it. You leave with a pain that is a measurement, an AI-fit verdict and a ceiling "
     "in writing. Open the lesson."),
    ("indigo", "P1 · Design & Spec", "solution architect", "blueprint",
     "Decide exactly what, and under whose authority.",
     [("Eight-field spec", "what a machine can build from"),
      ("A bar per slice", "derived from damage over saving"),
      ("Authority budget", "what it may do unasked, and where it stops")],
     ("You leave with", ["A signed spec", "A bar per slice, not one bar",
                         "A named approver per gate"]),
     "learn/p1-design-and-spec/",
     "Decide exactly what, and under whose authority. The solution architect owns it. You "
     "leave with a signed spec, a bar per slice and a named approver per gate. Open the lesson."),
    ("teal", "P2 · Build & Prove", "engineering lead", "prove",
     "Prove it meets the bar, slice by slice.",
     [("Bolts, not sprints", "ten days, one owner, one artefact"),
      ("Golden set in CI", "a required check, run in cost order"),
      ("Shadow run", "beside the desk, not instead of it")],
     ("You leave with", ["Evidence at the bar",
                         "A lower bound, never a score",
                         "A shadow run that agrees"]),
     "learn/p2-build-and-prove/",
     "Prove it meets the bar, slice by slice. The engineering lead owns it. You leave with "
     "evidence at the bar, a lower bound and a shadow run that agrees. Open the lesson."),
    ("amber", "P3 · Run & Learn", "the sponsor", "gauge",
     "Watch it, cost it, and feed the next frame.",
     [("Trace and drift", "the three signals a normal stack lacks"),
      ("The bill, by factor", "context, tier, cache, attempts"),
      ("Two-number report", "and the brief the next P0 starts from")],
     ("You leave with", ["Two numbers, not a dashboard",
                         "A drift readout",
                         "The next P0 brief, with an owner"]),
     "learn/p3-run-and-learn/",
     "Watch it, cost it and feed the next frame. The sponsor owns it. You leave with two "
     "numbers, a drift readout and the next P0 brief. Open the lesson."),
]


def pdlc() -> str:
    cols = [dg.column(h, n, b, i, t, s, k, href=u, tip=tp) for h, n, b, i, t, s, k, u, tp in PHASES]
    inner = dg.flow(cols, gate_after=1) + dg.returns(
        "production is where the next frame comes from: incident, drift, cost")
    return dg.board(
        "The spine", "P0 to P3: the SkyWays PDLC loop",
        "Four phases that run as a spiral rather than a line. Each pass takes an idea a step "
        "closer to production, and what production teaches starts the next pass. Click a "
        "phase to open its lesson.",
        inner,
        aside_title="What the hard gate is",
        aside="<p>The one hand-off nobody may skip. The spec, the bar per slice and the "
              "authority budget are signed before a line of the agent is written.</p>"
              "<p>It sits between P1 and P2 because paper is cheap to change and production "
              "is not. The other three crossings are soft: they check evidence and let the "
              "line move.</p>"
              '<p><a href="learn/what-is-the-agentic-pdlc/">The four phases in one lesson</a></p>',
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
        "By role", "Your role across P0 to P3",
        "One row per role, one column per phase. Read across for your own arc; read down "
        "to see who else is in the room when yours is the hard part. Every cell opens the "
        "step it names.",
        m,
        aside_title="How to read it",
        aside="<ul><li><b>The bar</b> marks the phase a role is accountable for.</li>"
              "<li><b>Dashed cells</b> are on purpose. An engineering lead who starts building "
              "in P0, or a QA lead who arrives in P2, are the two most expensive habits in "
              "agentic delivery.</li>"
              '<li><b>P3</b> belongs to the sponsor, which is why it has <a href="protocol/">its '
              "own page</a>.</li></ul>",
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
        "The machine took the drafting. It did not take the judgement; it concentrated it. "
        "Every step in this manual names a tool, a use, a caution, and exactly one thing "
        "that is never delegated.",
        b,
        aside_title="Read the red column first",
        aside="<p>Forty steps across five roles each name one thing that is never delegated, "
              "and the forty have a shape: every one is a fact about your business, your "
              "regulator or your ledger that no context window makes knowable from outside.</p>"
              "<p>The job did not shrink. It is the same judgement, concentrated into fewer "
              "and larger decisions, each with a name on it.</p>",
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
        "The feedback", "Eight loops that run every team's workflow, P0 to P3",
        "Five loops carry work forward, from requirements to trust. Three bring production "
        "back to the phase that must answer for it: cost, incident and governance.",
        inner,
        aside_title="The eight, as drawn",
        aside='<div class="bxg"><span class="bxk">Forward, five</span>'
              + "".join(f"<i>{n}</i>" for n in ("Requirements P0 → P1", "Spec P1 → P2", "Trust P2 → P3",
                                                 "Decision P1 → P1", "Delivery P2 → P2"))
              + '</div><div class="bxg" style="--c:var(--dg-rose)"><span class="bxk">Back from '
                'production, three</span><i>Cost P3 → P1</i><i>Incident P3 → P0</i>'
                '<i style="--c:var(--dg-violet)">Governance P0 → P3</i></div>'
                "<p>Nobody downstream is waiting for the three, so they have to be built on "
                "purpose. Name the person who owns each; if you cannot, the loop is absent.</p>",
        bid="loops")
