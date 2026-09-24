"""Pictures for the hand-written wiki pages, in the same grammar as the lessons' maps.

The wiki has no site twin for these pages, so each picture is drawn here, screenshotted by the
shots pipeline and embedded by ``site/wiki_pictures.py`` in place of the mermaid fence it replaces.
Keys are short slugs; the registry name is ``wikimap:<slug>`` and the screenshot ``wikimap-<slug>``.

The five journey arcs (``journey-<role>``) are built from the roles JSON, so they cannot drift from
the journey pages they sit on.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import maps
from .mapspecs import _c, _q, P0, P1, P2, P3

ROLES = Path(__file__).resolve().parents[1] / "content" / "roles"

SPECS: dict[str, dict] = {}

# ============================================================================ the spine pages
SPECS["anti-patterns"] = dict(
    kind="flow", title=[("Eighteen anti-patterns", "k"), ("and where each one lives",)], hue="k", numbered=True, gap=26,
    nodes=[_c("In requirements", "P0 · four: the record says more than the room did", "users"),
           _c("In design", "P1 · four: a choice nobody can point at", "layers"),
           _c("In building", "P2 · four: a control that is not one", "code"),
           _c("In proving", "P2 · three: a number that cannot carry its claim", "chart"),
           _c("In running", "P3 · three: a report with nothing to compare", "trend")],
    back=("whatever is left here arrives as next cycle's requirement",),
    callout=("An anti-pattern is a sensible decision by a careful person that the next phase pays for. Each one is caught cheapest where it lives.", "k", 40),
    alt="Eighteen anti-patterns across five stages, from requirements to running, with what is left over returning as the next cycle's requirement",
)

SPECS["depth-of-change"] = dict(
    kind="fan", title=[("What kind of change?", P2), ("four answers",)], start="A change",
    q="What kind of change is it?",
    outs=[_c("One-line fix", "a spec update and a single agent; skip discovery and most design", "pen", P0),
          _c("A feature", "SDD with the five gates: chat to spec, an editor agent to build", "spec", P1),
          _c("Audited, multi-team", "SDD with the BMAD persona trail; keep the versioned artefacts", "users", "k"),
          _c("Depth unknown", "AI-DLC: start shallow, escalate on evidence", "ladder", P3)],
    callout=("The question worth arguing about is not which method but how deep this change needs to go.", P2, 40),
    alt="Four kinds of change and the depth of process each one needs",
)

SPECS["eight-loops-workshop"] = dict(
    kind="flow", title=[("The requirements loop", P0), ("two meetings to a ratified list",)], hue=P0, numbered=True, per_row=4, gap=26,
    nodes=[_c("Discover", "two meetings", "users"), _c("Credit", "every line, by name", "pen"),
           _c("Consolidate", "in the email, not the room", "mail"), _c("Constrain", "technical, regulatory, commercial", "scale"),
           _c("Candidates", "as six-part scenarios", "doc"), _c("Utility trees", "one per stakeholder", "layers"),
           _c("Workshop", "uncontested first", "calendar"), _c("Ratify", "and name the sensitivity points", "check")],
    callout=("The loop closes when the architect can design without asking. Every line still carries the name of who said it.", P0, 40),
    alt="The requirements loop in eight moves, from discovery to a ratified list",
)

SPECS["eight-loops-proof"] = dict(
    kind="funnel", title=[("The trust loop", P2), ("from a golden set to live traffic",)], start="A golden set per slice, scored with its lower bound",
    steps=[
        {"q": "Lower bound at or above the bar?", "exit": "no", "out": _c("More cases, or fix the slice", "then score again", "loop", "o")},
        {"q": "The shadow run agrees with the desk?", "exit": "no", "out": _c("You learned for free", "the shadow decides, never acts", "eye", "o")},
    ],
    end=_c("Five percent of traffic", "then widen on live evidence", "plane", P0),
    aside=("The two tests", ["A score is not proof: the lower bound is", "A shadow that disagrees cost nothing", "Widen on evidence, never on a date"], P2),
    alt="The trust loop: score against the bar, shadow beside the desk, then five percent and widen",
)

SPECS["formulas"] = dict(
    kind="bands", title=[("Fourteen formulas", "n"), ("each answers one question",)],
    bands=[
        {"hue": P0, "key": "P0", "name": "Frame", "cells": [_c("The value line", "worth building?", "money")], "to_label": "a number that says go"},
        {"hue": P1, "key": "P1", "name": "Design & Spec", "cells": [_c("Acceptance bar", "how right?", "scale"), _c("Utility tree", "which NFR first?", "layers"),
                                                                  _c("Hand-off count", "how many agents?", "robot"), _c("Chained p", "will it hold?", "wave")], "to_label": "a number to hit"},
        {"hue": P2, "key": "P2", "name": "Build & Prove", "cells": [_c("Lower bound", "proven, or not?", "chart"), _c("Cases needed", "how many more?", "table"),
                                                                  _c("Days of evidence", "how long at 5%?", "calendar"), _c("Queue time", "why four days?", "clock"),
                                                                  _c("Cache break-even", "does it pay?", "db")], "to_label": "a number that was hit"},
        {"hue": P3, "key": "P3", "name": "Run & Learn", "cells": [_c("Four bill factors", "why 4.4 times?", "bill"), _c("Fix order", "what first?", "steps"),
                                                                _c("Maturity level", "getting better?", "ladder")]},
    ],
    terminal=_c("The next value line", "a bill at 4.4 times is a value line that was wrong", h="n"),
    callout=("Every formula on this page is worked once on the SkyWays numbers and carries a note on when it misleads.", "n", 40),
    alt="Fourteen formulas placed on the four phases, each with the question it answers",
)

SPECS["mental-models"] = dict(
    kind="bands", title=[("Twelve mental models", "n"), ("where each one does its work",)],
    bands=[
        {"hue": P0, "key": "P0", "name": "Frame", "cells": [_c("2 · Reversibility is the hinge", "", "undo")], "to_label": "11 · the brief crosses"},
        {"hue": P1, "key": "P1", "name": "Design & Spec", "cells": [_c("1 · Length is the enemy", "", "wave"), _c("3 · A hold is a lever", "", "users"),
                                                                  _c("9 · Parallelism is a tool property", "", "tool"), _c("10 · Depth is a dial", "", "ladder")], "to_label": "11 · the signed spec crosses the hard gate"},
        {"hue": P2, "key": "P2", "name": "Build & Prove", "cells": [_c("4 · A prompt asks, a signature closes", "", "lock"), _c("5 · The average hides the slice", "", "chart"),
                                                                  _c("6 · A score is not proof", "", "scale"), _c("7 · Evidence at the speed of traffic", "", "clock")], "to_label": "11 · the evidence pack crosses"},
        {"hue": P3, "key": "P3", "name": "Run & Learn", "cells": [_c("8 · Cost is a product of habits", "", "bill"), _c("12 · Drift has no error message", "", "trend")]},
    ],
    terminal=_c("The next P0", "8 and 12 are what reopen a frame somebody had closed", h="n"),
    callout=("11 · A phase ends on an artefact, not a date: it is the model that moves the others across.", "n", 40),
    alt="Twelve mental models placed on the four phases",
)

# ============================================================================ decision trees
SPECS["dt-exact"] = dict(
    kind="funnel", title=[("Exact, consequential or best-guess?", P1), ("one step at a time",)], start="One step of the feature",
    steps=[
        {"q": "Must it be right every single time?", "exit": "yes", "out": _c("EXACT", "a function, proven by a unit test", "code", P0), "go": "no"},
        {"q": "Does it change something real?", "exit": "yes", "out": _c("CONSEQUENTIAL", "a tool and a gate, proven by a confirmation", "lock", "k"), "go": "no"},
    ],
    end=_c("BEST-GUESS", "a model call, proven by a measured share", "brain", P1),
    aside=("Why it matters", ["Exact steps stay in code: no tokens, no bar", "Consequential steps get a gate before they act", "Only best-guess steps carry a bar per slice"], P1),
    alt="Two questions sort a step into exact, consequential or best-guess",
)

SPECS["dt-autonomy"] = dict(
    kind="funnel", title=[("How much may it do alone?", "k"), ("per action, never per product",)], start="One action",
    steps=[
        {"q": "Irreversible, or safety-critical?", "exit": "yes", "out": _c("Not delegated", "a person does it", "stop", "n"), "go": "no"},
        {"q": "Real money, identity or policy?", "exit": "yes", "out": _c("A named approver, every time", "and a cap in the tool signature", "lock", "k"), "go": "no"},
        {"q": "Reversible without effort?", "exit": "with effort", "out": _c("Acts, monitored", "or inside a veto window", "eye", P3), "go": "yes"},
    ],
    end=_c("Acts alone", "the cost of one wrong action is nothing", "check", P0),
    aside=("The rule", ["Autonomy follows reversibility, not capability", "Decided per action and written into the record", "A level only ever moves on evidence"], "k"),
    alt="Three questions set the autonomy level of one action, from not delegated to acts alone",
)

SPECS["dt-agents"] = dict(
    kind="funnel", title=[("One agent, or many?", P1), ("start single, escalate on a named limit",)], start="A feature: one agent with its tools",
    steps=[
        {"q": "Does one context genuinely overload?", "exit": "yes", "out": _c("Orchestrator and workers", "each hand-off with a named limit", "users", P2), "go": "no"},
        {"q": "Parallel sub-tasks a fan-out tool cannot express?", "exit": "yes", "out": _c("Orchestrator and workers", "each hand-off with a named limit", "users", P2), "go": "no"},
        {"q": "Complex, multi-team and audited?", "exit": "yes", "out": _c("A full agent team", "with the persona trail kept", "layers", "k"), "go": "no"},
    ],
    end=_c("Stay single", "one agent, its tools, zero hand-offs", "robot", P0),
    aside=("Hand-offs multiply", ["Five agents have ten possible hand-offs", "A fan-out tool runs in parallel with none", "Escalate only on a limit written in the record"], P1),
    alt="Three questions decide whether a feature needs one agent, an orchestrator with workers, or a full team",
)

SPECS["dt-prompt-or-signature"] = dict(
    kind="funnel", title=[("Prompt, or signature?", "k"), ("where a rule lives",)], start="A rule",
    steps=[
        {"q": "If the model were talked past it, would it cost money, expose data or be irreversible?", "exit": "yes",
         "out": _c("The tool signature", "typed, bounded, raises; keep the sentence in the prompt as policy", "lock", "k"), "go": "no"},
    ],
    end=_c("The prompt", "it is policy, and policy is fine there", "doc", P0),
    aside=("The distinction", ["A prompt is a request a model can be argued past", "A signature raises and cannot be", "Both can be right, for different rules"], "k"),
    alt="One question decides whether a rule belongs in the prompt or in the tool signature",
)

SPECS["dt-review-band"] = dict(
    kind="fan", title=[("Review by band", "k"), ("what is the most dangerous tool it touches?",)], start="A change",
    q="The most dangerous tool it touches? Not: how large is it",
    outs=[_c("R1", "the harness, review at the end", "check", P0) | {"via": "reads only"},
          _c("R2", "one reader before merge", "eye", "t") | {"via": "a reversible write"},
          _c("R3", "approve first", "users", P3) | {"via": "hard to reverse"},
          _c("R4", "two readers, every time", "lock", "k") | {"via": "money, identity, policy"},
          _c("R5", "not delegated", "stop", "n") | {"via": "irreversible"}],
    callout=("A change inherits the band of whatever it touches. The diff size never enters the decision.", "k", 40),
    alt="One question routes a change into one of five review bands",
)

SPECS["dt-cache"] = dict(
    kind="funnel", title=[("Cache it?", P3), ("and for how long",)], start="A prompt prefix",
    steps=[
        {"q": "Will it be reused more than once?", "exit": "no", "out": _c("No", "a write costs more than the call", "stop", "n")},
        {"q": "At least about 1,024 cacheable tokens?", "exit": "no", "out": _c("No", "below the minimum, nothing is stored", "stop", "n")},
        {"q": "Gap between calls: seconds to minutes?", "exit": "yes", "out": _c("Five-minute cache", "write 1.25×, refreshes free on each hit", "clock", P3), "go": "longer than five minutes"},
    ],
    end=_c("One-hour cache", "write 2× once; beats paying 1.25× every call", "db", P1),
    aside=("The arithmetic", ["A write is priced above a read", "A hit is a tenth of a read", "The gap decides which window pays"], P3),
    alt="Three questions decide whether to cache a prompt prefix, and for five minutes or an hour",
)

SPECS["dt-tier"] = dict(
    kind="fan", title=[("Which tier?", P3), ("route by the reasoning it needs",)], start="A request",
    q="What reasoning does it actually need?",
    outs=[_c("Cheap tier", "a lookup, a format, a classification", "bolt", P0) | {"via": "a lookup"},
          _c("Mid tier", "a policy question with a known shape", "scale", P1) | {"via": "a policy question"},
          _c("Frontier", "genuinely multi-constraint judgement", "brain", "k") | {"via": "genuinely multi-constraint"}],
    callout=("Every loop gets MAX_LOOPS = 5 and a per-transaction token cap, whichever tier answered.", P3, 40),
    alt="A request is routed to a cheap, mid or frontier tier by the reasoning it needs; every loop keeps a cap",
)

SPECS["dt-ship"] = dict(
    kind="funnel", title=[("Ship it?", P2), ("four checks, in order",)], start="A change",
    steps=[
        {"q": "Exact checks green?", "exit": "no", "out": _c("Reject", "exact work is exact", "stop", "k")},
        {"q": "Every slice at or above its bar?", "exit": "no", "out": _c("Reject", "the average hides the slice", "stop", "k")},
        {"q": "The lower bound clears the bar, not just the estimate?", "exit": "no", "out": _c("Cases owed", "not a rejection: more evidence", "table", P3)},
        {"q": "Money actions still gated?", "exit": "no", "out": _c("Reject", "a cap that moved is a stop", "stop", "k")},
    ],
    end=_c("Ship to 5%", "and widen on live evidence", "plane", P0),
    alt="Four checks in order decide whether a change ships to five percent",
)

# ============================================================================ how-to pages
def _steps(slug, title, hue, items, callout, alt, per_row=None, back=None, gate=None):
    d = dict(kind="flow", title=title, hue=hue, numbered=True, gap=24,
             nodes=[_c(t, s, i) for t, s, i in items], callout=(callout, hue, 40), alt=alt)
    if per_row:
        d["per_row"] = per_row
    if back:
        d["back"] = back
    if gate:
        d["gate_after"], d["gate_soft"], d["edge_labels"] = gate
    SPECS[slug] = d

_steps("choose", [("Build, buy or borrow", P1), ("five moves",)], P1,
       [("Frame", "whole product, three years, the exit", "target"), ("Criteria and weights", "six, from the ratified NFRs", "scale"),
        ("Rate the options", "score = Σ weight × rating", "table"), ("Three-year cost, and the door", "count the people; one-way or two", "money"),
        ("The decision record", "an ADR, with the rejections", "doc")],
       "A door that closes is priced like a door: month twelve is when the criteria are read again.",
       "Five moves from framing the choice to the decision record, with a review at month twelve", back=("month twelve", 1))

_steps("control-bill", [("Control the token bill", P3), ("six moves",)], P3,
       [("The per-call log", "four signatures, baseline vs now", "bill"), ("Multiply, then order", "4.40, and (factor − 1) ÷ days", "chart"),
        ("Context and routing", "the two half-day fixes", "swap"), ("Make the cache pay", "prefix, window, break-even", "db"),
        ("Breaker, and the trap", "MAX_LOOPS, and mark cache hits", "warn"), ("Guards, then P1", "a watched ratio and an amended record", "shield")],
       "A surprise bill is four ordinary habits multiplying. Fix in order of multiplier removed per day of work, not by what feels urgent.",
       "Six moves from the per-call log to a watched ratio and an amended design record")

_steps("cut-sprints", [("Cut sprints into bolts", P2), ("six moves",)], P2,
       [("Set the cadence", "how often evidence arrives", "calendar"), ("Cut by dependency", "not by priority", "layers"),
        ("Change the ceremonies", "one question at standup", "users"), ("Write the story file", "six parts, one file", "spec"),
        ("Measure exposure", "in unknown-days", "clock"), ("Re-cut, out loud", "before the day is spent", "undo")],
       "A bolt is one unknown, one owner, one artefact, integrated the same day. A bolt that cannot be built alone was cut wrong.",
       "Six moves for cutting sprints into bolts, with a re-cut when the cut was wrong", back=("the cut was wrong", 1))

_steps("design-agent", [("Design an agent on paper", P1), ("seven moves",)], P1,
       [("Is it an agent at all?", "three questions, in order", "ask"), ("The two planes", "what may happen · what does", "layers"),
        ("The agent PRD", "eight fields, one screen", "spec"), ("High-level design", "count the hand-offs first", "robot"),
        ("Low-level design", "behaviours, never knobs", "gear"), ("Prompts as policy", "tools as enforcement", "lock"),
        ("The design review", "four artefacts, then a signature", "check")],
       "Everything on paper is cheaper than it will ever be again. The review signs four artefacts, not a deck.",
       "Seven moves for designing an agent on paper, ending in a design review")

_steps("review-band", [("Review by risk band", "k"), ("six moves",)], "k",
       [("Read the queue", "slots needed ÷ slots per day", "clock"), ("Band by what it touches", "R1 to R5, never by size", "ladder"),
        ("Put the band in a path rule", "from the authority budget", "code"), ("Route the readers", "two, one, none", "users"),
        ("The harness-only lane", "open it, and count the escapes", "check"), ("Measure the policy", "three numbers, or it is repealed", "chart")],
       "A four-day queue is two of nine changes touching money. Band them, route the readers, count the escapes.",
       "Six moves for reviewing by risk band, from reading the queue to measuring the policy")

_steps("nfr-workshop", [("The NFR workshop", P0), ("nine days",)], P0,
       [("Day 1 · Discovery one", "the three closest to the work", "users"), ("Day 2 · Discovery two", "read back, credited", "pen"),
        ("Day 4 · The email", "all lines, every name, duplicates kept", "mail"), ("Day 6 · Constraints by type", "technical, regulatory, commercial", "scale"),
        ("Day 7 · Candidates", "as six-part scenarios", "doc"), ("Day 8 · Utility trees", "one per stakeholder", "layers"),
        ("Day 9 · The workshop", "uncontested first, then the conflicts", "calendar"), ("Ratify", "and name the sensitivity points", "check")],
       "Nine days from the first conversation to nine ratified NFRs, with every line still carrying the name of who said it.",
       "The NFR workshop over nine days, from discovery to ratification", per_row=4)

_steps("prove-bar", [("Prove the bar", P2), ("seven moves and one test",)], P2,
       [("Set the bar", "per slice, from cost", "scale"), ("Build the golden set", "real cases, by slice", "table"),
        ("Score it", "checks, then the judge", "chart"), ("Report the lower bound", "not the estimate", "check"),
        ("Shadow run", "decides, never acts", "eye"), ("Cut over at 5%", "twelve cases a day", "plane"), ("Widen on evidence", "never on a date", "trend")],
       "The gate between four and five: the lower bound clears the bar, or cases are owed and the slice is fixed and scored again.",
       "Seven moves for proving the bar, with the lower-bound test as a gate before the shadow run", gate=(3, True, ["", "", "", "lower bound ≥ bar? else cases owed"]))

SPECS["postmortem"] = dict(
    kind="flow", title=[("The missing-control postmortem", "k"), ("day 82 at SkyWays",)], hue="k", numbered=True, gap=24, per_row=4,
    nodes=[_c("The incident", "a $2,000 refund, not owed", "warn", "n"), _c("The question", "which enforced control would have made this impossible?", "ask"),
           _c("Classify every layer", "enforced, a request, absent", "layers"), _c("Choose the fix", "closes the path, not lowers the odds", "lock"),
           _c("Drop the autonomy level", "2 to 1, until a 14-day shadow passes", "ladder"), _c("Feed it forward", "golden cases, an ADR, the record, the brief", "loop")],
    terminal=_c("The next P0", "refunds as their own slice", h="n"),
    callout=("The counterfactual is the finding. A postmortem that produced a name has not finished; one that produced a control has.", "k", 40),
    alt="The missing-control postmortem from the incident to the next P0 brief",
)

SPECS["hold-boundary"] = dict(
    kind="flow", title=[("The security boundary", "k"), ("six controls, in the order text meets them",)], hue="k", numbered=True, gap=24, per_row=4,
    nodes=[_c("Text arrives", "passenger, partner API, document, booking field, knowledge chunk", "mail", "n"),
           _c("Injection defence", "tagged at ingest, read as data", "shield"),
           _c("The model decides", "the prompt's policy is a request", "brain", "n"),
           _c("Least authority", "may it call this tool at all?", "lock"),
           _c("Bounded tools", "over the cap: raises", "stop"),
           _c("Human gate on money", "no valid token: raises", "users"),
           _c("The money moves", "within $400, with a named approver", "money", "n"),
           _c("Traceability", "one redacted row, attempts included", "eye")],
    callout=("The sixth control is the rule in the system: every layer classified as enforced, a request, or absent — and audited as such.", "k", 40),
    alt="Text arriving, the injection defence, the model deciding, least authority, bounded tools, the human gate, the money moving, and the trace",
)

SPECS["agent-topology"] = dict(
    kind="bands", title=[("One agent", P1), ("its tools, and what sits behind the server",)], flow=True,
    bands=[
        {"hue": P1, "key": "One agent", "name": "Four tools", "sub": "a passenger request comes in", "cells": [
            _c("Fan-out search tool", "four partners in parallel", "search"), _c("fare_difference()", "exact, in code", "code"),
            _c("MCP server", "reads open, writes gated", "server"), _c("Independent checker", "a different model, an adversarial brief", "scale")],
         "to_label": "writes go through the server"},
        {"hue": "k", "key": "Behind the server", "name": "Gated writes", "sub": "each with its band", "cells": [
            _c("rebook()", "R3: approve first", "handoff"), _c("issue_refund(≤400)", "R4: a named approver, every time", "lock")]},
    ],
    callout=("Start single. One agent with a fan-out tool searches four partners in parallel with zero hand-offs and nothing to get wrong between them.", P1, 40),
    alt="One agent with four tools; behind the MCP server, two gated writes with their bands",
)

# ============================================================================ role pages: what crosses the desk
def _role(slug, name, sub, hue, icon, into, out, callout):
    SPECS[slug] = dict(
        kind="pairs", title=[(name, hue), ("what crosses the desk",)], centre=(name, sub, hue, icon),
        left={"hue": "s", "name": "Arrives from", "cells": [_c(a, b, i) for a, b, i in into]},
        right={"hue": hue, "name": "Goes to", "cells": [_c(a, b, i) for a, b, i in out]},
        callout=(callout, hue, 40),
        alt=f"What arrives on the {name.lower()}'s desk, from whom, and what leaves it, to whom",
    )

_role("role-product-manager", "Product manager", "owns the pain, the autonomy and the bar", P0, "target",
      [("The sponsor", "the request", "person"), ("The solution architect", "constraints, ratified NFRs, the map", "layers"), ("The QA lead", "a lower bound, the shadow run", "chart")],
      [("The solution architect", "pain register, AI-fit, the ceiling", "target"), ("The engineering lead", "spec, a bar per slice, bolt plan", "spec"), ("The sponsor", "two numbers, the next P0 brief", "trend")],
      "The product manager decides what and why; the machine downstream cannot ask what was meant, so every hand-off is a written artefact.")

_role("role-solution-architect", "Solution architect", "decides which steps may guess, and where the caps live", P1, "layers",
      [("The product manager", "pain register, AI-fit, the ceiling", "target"), ("The engineering lead", "questions against the map", "ask"), ("The platform team", "the bill, by factor", "bill")],
      [("The product manager", "constraints, ratified NFRs, the map", "layers"), ("The engineering lead", "ADRs, authority budget, gate map", "lock"), ("The platform team", "caching and routing changes", "swap")],
      "The architect owns the map: exact, best-guess or consequential per step, and the authority budget before a token is spent.")

_role("role-engineering-lead", "Engineering lead", "floor first, then the model, then the checker", P2, "code",
      [("The solution architect", "the map, ADRs, authority budget", "layers"), ("The product manager", "spec, a bar per slice, bolt plan", "spec"), ("The QA lead", "the golden set, what must block", "table")],
      [("The QA lead", "context file, the boundary line", "shield"), ("The product manager", "bolts, a required check, the ledger", "bolt"), ("The solution architect", "caching and routing changes", "swap")],
      "The engineering lead turns the map into bolts, the limit into a signature, and the bar into a required check.")

_role("role-qa-lead", "QA lead", "the arithmetic veto", "k", "scale",
      [("The solution architect", "the map's tags", "layers"), ("The product manager", "spec, a bar per slice", "spec"), ("The engineering lead", "builds, bolt by bolt", "bolt")],
      [("The engineering lead", "proof map, golden set, checker map", "table"), ("The product manager", "a lower bound, the shadow comparison", "chart"), ("The solution architect", "the missing-control finding", "shield")],
      "QA's veto is arithmetic, not opinion: a slice whose lower bound is below its bar does not pass.")

_role("role-devops", "Platform", "the floor under all four phases", "t", "server",
      [("The solution architect", "authority budget, gate map", "lock"), ("The QA lead", "what the harness must block", "check")],
      [("The engineering lead", "one gateway, pinned environments, a required check", "server"), ("The product manager", "cost per case, attempts, drift", "trend"), ("The solution architect", "the bill, by factor", "bill")],
      "One gateway every call passes through, a harness nobody can bypass, and a rollback that has been rehearsed.")

_role("role-sponsor", "Sponsor", "funding, the ceiling, what counts as proof", "n", "flag",
      [("The product manager", "AI-fit records, the two numbers", "trend"), ("The QA lead", "a slice called unproven", "warn"), ("The solution architect", "the missing-control finding", "shield")],
      [("The product manager", "the autonomy ceiling", "ladder"), ("The QA lead", "what counts as evidence", "scale"), ("The product manager", "cycle-two funding", "money")],
      "Four decisions nobody below the sponsor can make: what is AI work, what it does alone, what counts as evidence, what gets funded.")

# ============================================================================ finding your way
SPECS["scenario-library"] = dict(
    kind="fan", title=[("Thirty-seven scenarios", P1), ("start from what went wrong",)], start="Last three times",
    q="What went wrong the last three times?",
    outs=[_c("We built the wrong thing", "scenarios 1, 4, 6, 11: framing and the spec", "target", P0),
          _c("We could not say whether it worked", "scenarios 14 to 17: proof and the bar", "chart", P2),
          _c("It worked, then the bill arrived", "scenarios 18 to 20: the bill, by factor", "bill", P3),
          _c("Something got through that should not have", "scenarios 21, 22, 12, 13: boundary and review", "shield", "k"),
          _c("Leadership lost confidence", "scenarios 23, 24, 10: governance and the two numbers", "flag", "n")],
    alt="Five kinds of past failure, each pointing to the scenarios that rehearse it",
)

SPECS["where-do-i-find-it"] = dict(
    kind="fan", title=[("Where do I find it?", "t"), ("start from what is going wrong",)], start="Right now",
    q="What is going wrong right now?",
    outs=[_c("Nobody has written down what the thing may do", "Design an Agent on Paper · Run an NFR Workshop", "spec", P1),
          _c("We cannot say whether it works", "Prove the Bar", "chart", P2),
          _c("The bill left its estimate", "Control the Token Bill", "bill", P3),
          _c("Work is stuck, or arriving in one lump", "Cut Sprints into Bolts · Review by Risk Band", "bolt", P2),
          _c("Something got through", "Hold the Security Boundary · Run a Missing-Control Postmortem", "shield", "k"),
          _c("A decision keeps being re-opened", "Choose Build, Buy or Borrow", "doc", "n")],
    alt="Six symptoms, each pointing to the how-to page that treats it",
)

SPECS["error-index"] = dict(
    kind="fan", title=[("The error index", "k"), ("start from the exact string",)], start="The string",
    q="The exact string in front of you",
    outs=[_c("Access and identity", "aws sts get-caller-identity", "lock", "k") | {"via": "denied, or an empty list"},
          _c("Model IDs and invocation", "aws bedrock list-inference-profiles", "brain", P1) | {"via": "ValidationException, AttributeError"},
          _c("The agent loop", "print the message roles", "loop", P2) | {"via": "the same call twice, or forever"},
          _c("Agents and action groups", "open the trace, not the response", "robot", P2) | {"via": "nothing threw, nothing happened"},
          _c("Retrieval", "read five cited passages yourself", "search", "t") | {"via": "an answer you do not trust"},
          _c("Cost and platform", "the per-call log, and who answered", "bill", P3) | {"via": "a number moved with no deploy"},
          _c("Labs and local environment", "check the Python version", "code", "s") | {"via": "labctl, or a SyntaxError"}],
    alt="Seven kinds of error string, each pointing to the section that explains it",
)

SPECS["study-plans"] = dict(
    kind="funnel", title=[("Which study plan?", "t"), ("five questions",)], start="Who is reading?",
    steps=[
        {"q": "A team, reading together?", "exit": "yes", "out": _c("Twelve weeks, reading group", "90 minutes a week", "users", "t"), "go": "just me"},
        {"q": "Is there a date?", "exit": "an interview in a fortnight", "out": _c("Interview in two weeks", "four labs and two guides", "calendar", "k"), "go": "no date"},
        {"q": "Will you write code?", "exit": "no, I need the method", "out": _c("One week, no code", "about four hours", "book", P0), "go": "yes"},
        {"q": "Do you have AWS?", "exit": "not yet, or never", "out": _c("No AWS account yet", "about twenty hours, zero cost", "cloud", P1), "go": "yes"},
        {"q": "What shape is the time?", "exit": "an hour most evenings", "out": _c("Four weeks, evenings", "about six hours a week", "clock", P2), "go": "one clear block"},
    ],
    end=_c("One weekend", "about twelve hours", "bolt", P3),
    alt="Five questions pick one of six study plans",
)

SPECS["sources"] = dict(
    kind="flow", title=[("A default becomes evidence", "n"), ("only by being measured",)], hue="n", numbered=True, gap=26,
    nodes=[_c("Adopt", "a default, labelled as a default", "doc"), _c("Measure", "on your own traffic", "chart")],
    decision={"q": "Your traffic agrees?", "yes": ("Keep it, and set the next review date", P0, "check"), "no": ("Change it, and record what you saw", P3, "pen")},
    callout=("Either way it is now yours, and it is evidence. A default nobody looked at for a year is not confirmation: it is a number with a plausible shape.", "n", 52),
    alt="Adopt a default, measure it on your own traffic, then keep it or change it; either way it becomes evidence",
)


# ============================================================================ journeys, from the roles JSON
ROLE_STYLE = {"product-manager": ("Product manager", P0), "solution-architect": ("Solution architect", P1),
              "engineering": ("Engineering lead", P2), "qa": ("QA lead", "k"), "devops": ("DevOps and platform", "t")}
STEP_ICON = {"discover": "search", "qualify": "ask", "frame": "target", "specify": "spec", "plan": "calendar", "gate": "gate",
             "launch": "plane", "learn": "chart", "elicit": "users", "constrain": "scale", "map": "layers", "shape": "robot",
             "decide": "doc", "bound": "lock", "detail": "server", "evolve": "loop", "prepare": "doc", "slice": "spec",
             "floor": "code", "layer": "brain", "harness": "check", "ship": "bolt", "operate": "server", "define": "clipboard",
             "curate": "table", "check": "check", "measure": "chart", "attack": "shield", "shadow": "eye", "watch": "trend",
             "baseline": "cloud", "access": "server", "environments": "layers", "pipeline": "gear", "deploy": "flag",
             "observe": "eye", "protect": "shield", "recover": "undo"}


def journey(role_id: str) -> dict:
    role = json.loads((ROLES / f"{role_id}.json").read_text(encoding="utf-8"))
    name, hue = ROLE_STYLE[role_id]
    by = {ph: [] for ph in ("P0", "P1", "P2", "P3")}
    for st in role["steps"]:
        by[st["pdlc"]].append(st)
    names = [("P0", "Frame", P0), ("P1", "Design & Spec", P1), ("P2", "Build & Prove", P2), ("P3", "Run & Learn", P3)]
    bands = []
    for key, pname, phue in names:
        steps = by[key]
        if steps:
            cells = [_c(f"{s['n']} · {s['phase']}", s["artifact"]["name"], STEP_ICON.get(s["phase"].lower(), "doc")) for s in steps]
        else:
            cells = [_q(role["pdlc_absent"].get(key, "nothing owed in this phase"))]
        b = {"hue": phue, "key": key, "name": pname, "cells": cells}
        if len(steps) >= 3 or (steps and len(steps) == max(len(v) for v in by.values())):
            b["sub"] = "where the hard gate lands for you" if key == "P1" and role_id == "solution-architect" else ""
        bands.append(b)
    return dict(kind="bands", title=[(name, hue), ("the eight steps, on the spine",)], bands=bands,
                callout=(role["tagline"], hue, 40),
                alt=f"The {name.lower()}'s eight steps placed on the four phases, with the artefact each one produces")


for _rid in ROLE_STYLE:
    SPECS[f"journey-{_rid}"] = journey(_rid)


def keys() -> list[str]:
    return list(SPECS)


def draw(slug: str) -> str:
    spec = SPECS[slug]
    return maps.KINDS[spec["kind"]](spec)


def alt(slug: str) -> str:
    return SPECS[slug]["alt"]
