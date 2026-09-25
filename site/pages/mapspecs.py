"""One map per lesson, as data. ``maps.py`` draws them; a lesson embeds its own with ``{{map:<slug>}}``.

Hues: P0 green ``g``, P1 blue ``b``, P2 purple ``p``, P3 orange ``o``; teal ``t`` and pink ``k`` for
themes that are not phases; navy ``n`` for the manual's own devices; slate ``s`` for the neutral.
A cell is ``{"t": title, "s": subtitle, "i": icon}``; ``{"t": ..., "quiet": True}`` is the dashed
empty-by-design cell.
"""
from __future__ import annotations

P0, P1, P2, P3 = "g", "b", "p", "o"


def _c(t, s="", i="", h=None):
    d = {"t": t}
    if s:
        d["s"] = s
    if i:
        d["i"] = i
    if h:
        d["h"] = h
    return d


def _q(t):
    return {"t": t, "quiet": True}


def _phase_bands(rows, leads=()):
    """The four phases as bands; ``rows`` is four lists of cells, ``leads`` the phases this role leads."""
    names = [("P0", "Frame", P0), ("P1", "Design & Spec", P1), ("P2", "Build & Prove", P2), ("P3", "Run & Learn", P3)]
    out = []
    for (key, name, hue), cells in zip(names, rows):
        b = {"hue": hue, "key": key, "name": name, "cells": cells}
        if key in leads:
            b["sub"] = "yours to lead"
        out.append(b)
    return out


MAPS: dict[str, dict] = {}

# ============================================================================ by role
MAPS["agentic-pdlc-for-product-managers"] = dict(
    kind="bands", title=[("The product manager", P0), ("across the four phases",)],
    bands=_phase_bands([
        [_c("1 · Discover", "the vibe, measured", "search"), _c("2 · Qualify", "is it AI at all?", "ask"),
         _c("3 · Frame", "value and autonomy", "target")],
        [_c("4 · Specify", "eight fields, one screen", "spec"), _c("5 · Plan", "bolts, not sprints", "calendar")],
        [_c("6 · Gate", "your three gates", "gate")],
        [_c("7 · Launch", "shadow, 5%, widen", "plane"), _c("8 · Learn", "two numbers, next frame", "chart")],
    ], leads=("P0",)),
    callout=("The product manager leads P0 and holds three gates in P2. What and why stay yours; how right it must be becomes a number per slice.", P0, 52),
    alt="The product manager's eight steps laid across the four phases, leading P0",
)

MAPS["agentic-pdlc-for-solution-architects"] = dict(
    kind="bands", title=[("The solution architect", P1), ("across the four phases",)],
    bands=_phase_bands([
        [_c("1 · Elicit", "every line credited", "users"), _c("2 · Constrain", "typed, before any target", "scale")],
        [_c("3 · Map", "exact, best-guess, consequential", "layers"), _c("4 · Shape", "how many agents", "robot"),
         _c("5 · Decide", "only ADRs that earn one", "doc"), _c("6 · Bound", "authority before tokens", "lock"),
         _c("7 · Detail", "context, server, checker", "server")],
        [_q("Answers against the map; does not re-open it")],
        [_c("8 · Evolve", "bill, trace, incident ADR", "loop")],
    ], leads=("P1",)),
    callout=("Five of eight steps sit in P1: the architect decides which steps may guess, and where the caps live, before a token is spent.", P1, 52),
    alt="The solution architect's eight steps across the four phases, five of them in P1",
)

MAPS["agentic-pdlc-for-engineers"] = dict(
    kind="bands", title=[("The engineer", P2), ("across the four phases",)],
    bands=_phase_bands([
        [_q("Not on the clock: reads the brief, starts nothing")],
        [_c("1 · Prepare", "the context file", "doc")],
        [_c("2 · Slice", "a story file per bolt", "spec"), _c("3 · Floor", "exact code first", "code"),
         _c("4 · Layer", "model calls, a checker", "brain"), _c("5 · Gate", "the limit in the signature", "lock"),
         _c("6 · Harness", "in CI, in cost order", "check"), _c("7 · Ship", "a bolt a day, behind a flag", "bolt")],
        [_c("8 · Operate", "cache, route, trace, ledger", "server")],
    ], leads=("P2",)),
    callout=("An engineer who opens a branch in P0 is the most expensive habit in agentic delivery. The work is P2: floor first, then the model, then the checker.", P2, 52),
    alt="The engineer's eight steps across the four phases, six of them in P2",
)

MAPS["agentic-pdlc-for-qa"] = dict(
    kind="bands", title=[("The QA lead", P2), ("across the four phases",)],
    bands=_phase_bands([
        [_q("One question: what will right mean, and who says so?")],
        [_c("1 · Define", "the proof each step owes", "clipboard"), _c("2 · Curate", "the golden set, by slice", "table")],
        [_c("3 · Check", "the checker fits the work", "check"), _c("4 · Harness", "every change, in CI", "gear"),
         _c("5 · Measure", "lower bound, not score", "chart"), _c("6 · Attack", "injection, as a regression", "shield"),
         _c("7 · Shadow", "beside the desk", "eye")],
        [_c("8 · Watch", "drift, and incidents into controls", "trend")],
    ], leads=("P2",)),
    callout=("QA gains a veto that is arithmetic rather than opinion: a slice whose lower bound is below its bar does not pass.", P2, 52),
    alt="The QA lead's eight steps across the four phases, leading P2",
)

MAPS["agentic-pdlc-for-devops"] = dict(
    kind="bands", title=[("DevOps and platform", P3), ("across the four phases",)],
    bands=_phase_bands([
        [_c("1 · Baseline", "account, tags, budget", "cloud")],
        [_c("2 · Access", "per region, one gateway", "server"), _c("3 · Environments", "model version pinned", "layers")],
        [_c("4 · Pipeline", "the harness is required", "gear"), _c("5 · Deploy", "a flag per action", "flag")],
        [_c("6 · Observe", "cost, trace, drift", "eye"), _c("7 · Protect", "the smallest identity", "shield"),
         _c("8 · Recover", "rehearsed, and timed", "undo")],
    ], leads=("P3",)),
    callout=("The floor under all four phases: one gateway every call passes through, a harness nobody can bypass, and a rollback that has been rehearsed.", P3, 52),
    alt="DevOps and platform's eight steps across the four phases, leading P3",
)

MAPS["agentic-pdlc-for-program-managers"] = dict(
    kind="bands", title=[("The programme manager", "t"), ("across the four phases",)],
    bands=_phase_bands([
        [_c("1 · Board and baseline", "person-days per story, now", "board"), _c("2 · Lead times", "requested in week one", "clock")],
        [_c("3 · Decision log", "hard or soft, owner, date", "doc"), _c("4 · Cadence", "and an integration date", "calendar")],
        [_c("5 · Daily rhythm", "one question at standup", "users"), _c("6 · Review queue", "slots, not tickets", "table")],
        [_c("7 · Gate conditions", "evidence, never dates", "gate"), _c("8 · Two numbers", "and the maturity check", "chart")],
    ]),
    callout=("The programme manager owns the board, the cadence and the review queue, and reports evidence, never dates.", "t", 44),
    alt="The programme manager's eight steps across the four phases",
)

MAPS["agentic-ai-for-executives"] = dict(
    kind="flow", title=[("Four decisions", "n"), ("only you can make",)], hue="n", numbered=True,
    nodes=[_c("What is AI work?", "ask for: AI-fit records", "ask"), _c("What it does alone", "ask: show me the cap", "lock"),
           _c("What is evidence?", "ask for: a lower bound", "chart"), _c("What gets funded", "ask for: two numbers", "money")],
    terminal=_c("Every cycle · 10 min", "the four questions", h="n"),
    callout=("Each trades a business risk against a business return, which is why nobody below you can make it. Keep them true with four questions asked every cycle.", "n", 52),
    alt="The four executive decisions in order, closing on the four questions asked every cycle",
)

MAPS["agentic-pdlc-for-business-sponsors"] = None  # this lesson has no map

MAPS["ai-dlc-for-forward-deployed-engineers"] = dict(
    kind="bands", title=[("The forward-deployed engineer", "t"), ("on a customer's site",)],
    bands=[
        {"hue": P0, "key": "P0", "name": "Frame", "sub": "on site", "cells": [
            _c("Measure the pain", "in their data, not the pitch", "search"), _c("Name their risk owner", "before any design", "person")]},
        {"hue": P1, "key": "P1", "name": "Design & Spec", "sub": "as a mob", "cells": [
            _c("Mob elaboration", "with their team, recorded", "users"), _c("Authority budget", "signed by their owner", "lock")]},
        {"hue": P2, "key": "P2", "name": "Build & Prove", "sub": "in their stack", "cells": [
            _c("Skeleton on day one", "against their real system", "bolt"), _c("Their cases, their CI", "a golden set they recognise", "check")]},
        {"hue": P3, "key": "P3", "name": "Run & Learn", "sub": "then leave", "cells": [
            _c("Shadow their staff", "find the unwritten rules", "eye"), _c("Hand over the evidence", "and a named operator", "handoff")]},
    ],
    callout=("Their pain, their risk owner, their stack, their people. The FDE leaves an evidence pack and a named operator, not a dependency.", "t", 44),
    alt="AI-DLC and AIDD applied by a forward-deployed engineer across the four phases on a customer's site",
)

# ============================================================================ fundamentals
MAPS["what-is-the-agentic-pdlc"] = dict(
    kind="flow", title=[("Four phases", P1), ("one hard gate, one loop back",)], gap=34,
    nodes=[_c("P0 · Frame", "worth it, AI at all, how much may it do?", "flag", P0),
           _c("P1 · Design & Spec", "what exactly, and under whose authority?", "spec", P1),
           _c("P2 · Build & Prove", "does it meet the bar, slice by slice?", "bolt", P2),
           _c("P3 · Run & Learn", "still true, and what did it cost?", "chart", P3)],
    edge_labels=["soft · the brief", "signed spec, bar, guardrails", "soft · the evidence pack", "what you learned"],
    gate_after=1, tall=True,
    terminal=_c("The next P0", "an incident, drift or a bill", h="n"),
    callout=("Three crossings are soft and can cross with a placeholder, a named owner and a date. One is hard: nothing downstream survives without the spec, the bar and the guardrails.", "k", 52),
    alt="The agentic PDLC: P0 Frame, P1 Design and Spec, the hard gate, P2 Build and Prove, P3 Run and Learn, and the next P0",
)

MAPS["evolution-of-the-pdlc"] = dict(
    kind="bands", title=[("Six lifecycles", "s"), ("one bottleneck at a time",)], flow=True,
    bands=[
        {"hue": "s", "key": "1970s", "name": "Plan-driven", "cells": [_c("Bottleneck: change cost", "a decision was expensive to revisit", "money"), _c("Answer: decide up front", "the whole design before a line of code", "doc")]},
        {"hue": "s", "key": "1988 · 90", "name": "Spiral and stage-gate", "cells": [_c("Bottleneck: the wrong thing", "built well, wanted by nobody", "warn"), _c("Answer: evidence gates", "a review before each round of spend", "gate")]},
        {"hue": "s", "key": "2001", "name": "Agile", "cells": [_c("Bottleneck: late learning", "feedback arrived after the release", "clock"), _c("Answer: short cycles", "working software every few weeks", "loop")]},
        {"hue": "s", "key": "2009 on", "name": "DevOps", "cells": [_c("Bottleneck: the release", "the hand-off to operations", "server"), _c("Answer: continuous delivery, measured", "deploy often, watch the four keys", "trend")]},
        {"hue": "t", "key": "2021 on", "name": "AI-assisted", "cells": [_c("Bottleneck: typing code", "the keyboard was the slow part", "code"), _c("Answer: a model writes, a person reviews", "the same lifecycle, faster inside", "brain")]},
        {"hue": P0, "key": "2024 on", "name": "Agentic", "cells": [_c("Bottleneck: mostly right", "part of the product is right a share of the time", "wave"), _c("Answer: a measured bar, authority per action", "and one hard gate before the build", "target")]},
    ],
    callout=("Each lifecycle answered the bottleneck of its day and kept everything before it. The agentic one keeps all five and adds the arithmetic.", P0, 44),
    alt="Six lifecycles from plan-driven to agentic, each row naming its bottleneck and its answer",
)

MAPS["why-agentic-ai-projects-fail"] = dict(
    kind="bands", title=[("Seven failure modes", "k"), ("and the phase that catches each",)],
    bands=[
        {"hue": P0, "key": "P0", "name": "Frame", "sub": "catches", "cells": [_c("1 · Nobody measured the pain", "", "search", "k")]},
        {"hue": P1, "key": "P1", "name": "Design & Spec", "sub": "catches", "cells": [_c("2 · A model doing a rule's job", "", "robot", "k"), _c("3 · A limit that lives only in the prompt", "", "lock", "k")]},
        {"hue": P2, "key": "P2", "name": "Build & Prove", "sub": "catches", "cells": [_c("4 · The average hides the slice", "", "chart", "k"), _c("5 · A score with no sample size", "", "scale", "k")]},
        {"hue": P3, "key": "P3", "name": "Run & Learn", "sub": "catches", "cells": [_c("6 · A bill that multiplies", "", "bill", "k"), _c("7 · Drift with no deploy", "", "wave", "k")]},
    ],
    callout=("None of these throws an error. Each is caught by a specific phase, which is the argument for having the phases.", "k", 44),
    alt="Seven failure modes of agentic AI projects, placed on the phase that catches each",
)

MAPS["p0-frame"] = dict(
    kind="funnel", title=[("P0 · Frame", P0), ("is this worth doing, and is it AI at all?",)], start="A request",
    steps=[
        {"q": "A genuine judgement call?", "exit": "no", "out": _c("A rule", "code does it", "code", "s")},
        {"q": "Enough volume for a probabilistic system?", "exit": "no", "out": _c("A person", "is cheaper", "person", "s")},
        {"q": "Is a wrong answer recoverable?", "exit": "no", "out": _c("A person in the loop", "assisted and gated", "users", "o"), "go": "yes, or partly"},
    ],
    end=_c("Agentic", "unrecoverable steps gated", "robot", P0),
    aside=("The first no ends it", ["Most of a roadmap comes back as rules", "A person is cheaper below the volume line", "Recoverability sets the autonomy, not capability"], P0),
    callout=("Four decisions on paper, before anything is built, each cheaper now than it will ever be again.", P0, 40),
    alt="The AI-fit funnel: judgement call, volume, recoverability; each no exits to a rule, a person, or a person in the loop",
)

MAPS["p1-design-and-spec"] = dict(
    kind="bands", title=[("The eight-field spec", P1), ("three classical, five agentic",)], flow=True,
    bands=[
        {"hue": "s", "key": "Fields 1 to 3", "name": "Classical", "sub": "usually already written", "cells": [
            _c("1 · Title", "one line", "pen"), _c("2 · Value", "the net, and its pain", "money"), _c("3 · Acceptance", "in EARS, with boundaries", "check")]},
        {"hue": P1, "key": "Fields 4 to 8", "name": "Agentic", "sub": "usually undecided", "cells": [
            _c("4 · The model's role", "which steps it decides", "brain"), _c("5 · Autonomy", "a level per action", "ladder"),
            _c("6 · The bar", "per slice, from cost", "scale"), _c("7 · Fallback", "when it cannot decide", "undo"),
            _c("8 · Records", "what every action logs", "doc")]},
    ],
    callout=("A spec a coding agent, or an engineer who was not in the room, can build from without asking. The five agentic fields are the ones a PRD leaves blank.", P1, 44),
    alt="The eight-field spec: three classical fields and five agentic ones",
)

MAPS["the-hard-gate"] = dict(
    kind="funnel", title=[("Hard or soft?", "k"), ("the test for any open decision",)], start="An open decision",
    steps=[
        {"q": "Cheap to reverse once building starts?", "exit": "no"},
        {"q": "Can the build proceed behind a placeholder?", "exit": "no"},
        {"q": "A named owner and a date?", "exit": "no"},
        {"q": "Does downstream work survive a change?", "exit": "no"},
    ],
    shared=_c("HARD", "settle it before the phase closes", "lock", "k"),
    end=_c("SOFT", "runs beside the build, behind a placeholder", "handoff", P0),
    aside=("Only one crossing is hard", ["P1 to P2: the spec, the bar and the guardrails", "Soft gates cross with a placeholder, an owner, a date", "Treating all four as hard is its own failure"], "k"),
    alt="Four questions decide whether an open decision is a hard gate or a soft one",
)

MAPS["p2-build-and-prove"] = dict(
    kind="flow", title=[("P2 · Build & Prove", P2), ("every change, per slice",)], hue=P2, gap=26,
    nodes=[_c("Build", "a bolt, one unknown", "bolt"), _c("Exact checks", "unit tests, schema, rules", "code"),
           _c("Golden slice", "the slices it touched", "table"), _c("Judge", "independent, by rubric", "scale"),
           _c("Score per slice", "n, score and lower bound", "chart")],
    decision={"q": "Any touched slice below its bar?", "yes": ("Reject the merge", "k", "stop"), "no": ("Merge", P0, "check")},
    callout=("Report per slice, never overall. The lower bound is the number; the score is an estimate with a width.", P2, 40),
    alt="The P2 harness: build, exact checks, golden slice, judge, score per slice, then merge or reject",
)

MAPS["the-evidence-pack"] = dict(
    kind="bands", title=[("The evidence pack", "n"), ("what must exist before each hand-off",)],
    bands=[
        {"hue": P0, "key": "P0 → P1", "name": "Soft · 7 owed", "sub": "test: can the architect design without asking?", "cells": [
            _c("Pain, AI-fit, value", "", "target"), _c("Autonomy", "", "ladder"), _c("Requirements, constraints, NFRs", "", "doc")]},
        {"hue": P1, "key": "P1 → P2", "name": "HARD · 9 owed", "sub": "test: can an outsider build bolt one alone?", "cells": [
            _c("Spec, bar sheet, ADRs", "", "spec"), _c("Step map, authority", "", "lock"), _c("Topology, context", "", "layers"), _c("Story files, 50 cases", "", "table")]},
        {"hue": P2, "key": "P2 → P3", "name": "Soft · 8 owed", "sub": "test: is the bar a running check?", "cells": [
            _c("Bolt plan, lower bound", "", "chart"), _c("Review lanes, harness", "", "gear"), _c("Checkers, gated tools", "", "shield"), _c("Shadow, cut-over", "", "eye")]},
        {"hue": P3, "key": "P3 → P0", "name": "Soft · 6 owed", "sub": "test: does the next brief have an owner?", "cells": [
            _c("Two numbers, drift", "", "trend"), _c("Redacted trace, bill", "", "bill"), _c("Incident, maturity", "", "loop")]},
    ],
    callout=("A phase ends on an artefact, not a date. Each hand-off has a test; an empty line reads as a blocked merge.", "n", 40),
    alt="The evidence pack: what each of the four hand-offs owes, with the test for each",
)

MAPS["the-eight-loops"] = None
MAPS["p3-run-and-learn"] = None

# ============================================================================ methods decoded
MAPS["ai-dlc-vs-aidd-vs-agentic-sdlc"] = dict(
    kind="bands", title=[("Six terms", "t"), ("two questions",)], flow=True,
    bands=[
        {"hue": "t", "key": "AI builds the software", "name": "Methods for building with AI", "cells": [
            _c("AWS AI-DLC", "AI proposes, people decide", "users"), _c("AIDDLC", "a seven-phase standard", "layers"),
            _c("AIDD", "the everyday craft", "code"), _c("Agentic SDLC", "agents in every phase", "robot"),
            _c("Spec-driven dev", "the spec comes first", "spec"), _c("BMAD Method", "agile personas as agents", "users")],
         "to_label": "and then"},
        {"hue": "n", "key": "AI is inside the software", "name": "A lifecycle for the product", "cells": [
            _c("The agentic PDLC", "how right, who may act, when it stops being true", "loop", "n")]},
    ],
    callout=("The six on top answer how to build with AI. The one below answers what changes when the product itself decides. You need both.", "n", 44),
    alt="Six building methods above, the agentic PDLC below: methods for building with AI against a lifecycle for a product that contains AI",
)

MAPS["what-is-ai-dlc"] = dict(
    kind="bands", title=[("AWS AI-DLC", P3), ("three phases, bolts, a mob",)],
    bands=[
        {"hue": P0, "key": "Inception", "name": "Mob Elaboration", "cells": [
            _c("Intent", "the business goal", "flag"), _c("Requirements and stories", "AI asks, the team answers", "users"), _c("Units of work", "in place of epics", "layers")]},
        {"hue": P2, "key": "Construction", "name": "Mob Construction", "cells": [
            _c("Architecture and models", "AI proposes, team decides", "gear"), _c("Code and tests", "in bolts of hours or days", "bolt")]},
        {"hue": P3, "key": "Operations", "name": "Run it", "cells": [
            _c("Infrastructure", "and deploy, from context", "cloud"), _c("Run it", "with the team overseeing", "eye")]},
    ],
    callout=("AI proposes, people decide, at every boundary. Inception is P0 and P1, Construction is P2, Operations is P3.", P3, 40),
    alt="AI-DLC's three phases: Inception with mob elaboration, Construction with mob construction, Operations",
)

MAPS["what-is-aidd"] = dict(
    kind="flow", title=[("AIDD", P2), ("the daily craft, in five moves",)], hue=P2, numbered=True,
    nodes=[_c("Context file", "read by every session", "doc"), _c("Story file", "one per bolt, not a chat", "spec"),
           _c("Exact floor", "functions and tests first", "code"), _c("Model layer", "an independent checker", "brain"),
           _c("Harness and review", "per slice, by risk band", "check")],
    terminal=_c("Merge", "the same day", h=P0),
    callout=("How an engineer works with a coding agent day to day, whichever method frames it: context, story, floor, model, harness, merge.", P2, 40),
    alt="AIDD in five moves from context file to a same-day merge",
)

MAPS["what-is-the-bmad-method"] = dict(
    kind="bands", title=[("The BMAD Method", "k"), ("agile personas as agents",)],
    bands=[
        {"hue": P0, "key": "Mostly P0", "name": "Framing the work", "cells": [_c("Analyst", "a brief", "search", "k")]},
        {"hue": P1, "key": "Mostly P1", "name": "Specifying it", "cells": [_c("Product manager", "a requirements document", "doc", "k"), _c("Architect", "an architecture", "gear", "k")]},
        {"hue": P2, "key": "Mostly P2", "name": "Building it", "cells": [_c("Scrum master", "stories, sharded small", "board", "k"), _c("Developer", "code, story by story", "code", "k"), _c("QA", "review against the story", "check", "k")]},
    ],
    callout=("Each persona hands a versioned document to the next. On a one-line change it is twelve personas between you and the change.", "k", 40),
    alt="BMAD's personas from analyst to QA, placed on the phases they mostly serve",
)

MAPS["what-is-spec-driven-development"] = dict(
    kind="bands", title=[("Spec-driven development", P1), ("Kiro and Spec Kit",)], flow=True,
    bands=[
        {"hue": "n", "key": "You decide", "name": "What no tool decides for you", "cells": [
            _c("The bar per slice", "from what a mistake costs", "scale", "n"), _c("The authority budget", "limits in signatures", "lock", "n")],
         "to_label": "you write these into the spec"},
        {"hue": P1, "key": "P1", "name": "What a tool keeps", "cells": [
            _c("Kiro", "requirements.md in EARS, design.md", "spec"), _c("Spec Kit", "constitution, specify, plan, tasks", "doc")]},
        {"hue": P2, "key": "P2", "name": "What the agent does", "cells": [
            _c("Kiro", "tasks.md, run task by task", "code"), _c("Spec Kit", "implement, to checklists", "check")]},
    ],
    callout=("The spec, not the code, is what you maintain. The tools keep it and build from it; the bar and the authority budget are yours to write in.", P1, 40),
    alt="Spec-driven development: what you decide, what Kiro and Spec Kit keep in P1, and what the agent does in P2",
)

MAPS["one-lifecycle-for-every-method"] = dict(
    kind="bands", title=[("Every method", P1), ("on one lifecycle",)],
    bands=_phase_bands([
        [_c("AI-DLC · intent", "", "flag"), _c("BMAD · analyst's brief", "", "search"), _c("Shape Up · shaping, betting", "", "target")],
        [_c("AI-DLC · Mob Elaboration", "", "users"), _c("Kiro · requirements, design", "", "spec"), _c("Spec Kit · specify, plan", "", "doc"), _c("BMAD · PRD, architecture", "", "gear")],
        [_c("AI-DLC · Construction, bolts", "", "bolt"), _c("Kiro · tasks", "", "code"), _c("Spec Kit · implement", "", "check"), _c("BMAD · stories, dev, QA", "", "board"), _c("Scrum · sprints become bolts", "", "loop")],
        [_c("AI-DLC · Operations", "", "server"), _c("AIDDLC · operate, evolve", "", "trend")],
    ]),
    callout=("The methods mostly agree on the shape. What none of them settles is the bar, the authority and who watches the agent after launch.", P1, 40),
    alt="AI-DLC, BMAD, Kiro, Spec Kit, Scrum and Shape Up placed on the four phases",
)

MAPS["how-much-process-does-a-change-need"] = dict(
    kind="funnel", title=[("Shallow, standard or deep?", P2), ("sizing a change",)], start="The change, in one sentence",
    steps=[
        {"q": "Touches money, identity or policy?", "exit": "yes", "out": _c("Standard, at least", "spec-driven, with the five gates", "gate", P2), "go": "no"},
        {"q": "Cheap to undo once it is live?", "exit": "no", "out": _c("Standard, at least", "spec-driven, with the five gates", "gate", P2)},
        {"q": "More than one team, or an auditor, reads it?", "exit": "yes", "out": _c("Deep", "spec, the gates and a persona trail, kept", "layers", "k"), "go": "no"},
    ],
    end=_c("Shallow", "a spec update and one coding agent", "code", P0),
    aside=("Depth is a dial", ["Standard goes deep when more than one team, or an auditor, reads it", "The spec stays everywhere; what flexes is around it", "Per change, judged by the architect"], P2),
    alt="Three questions size a change as shallow, standard or deep",
)

# ============================================================================ running delivery
MAPS["how-to-run-an-agentic-ai-project"] = None
MAPS["bolts-vs-sprints"] = None

MAPS["agentic-kanban-board"] = dict(
    kind="bands", title=[("Nine columns", P2), ("each with an exit criterion",)],
    bands=_phase_bands([
        [_c("Framed", "exit: pain measured, AI-fit recorded", "target")],
        [_c("Specified", "exit: spec, bar and band signed", "spec"), _c("Bolt ready", "exit: story file, one unknown", "doc")],
        [_c("Building", "exit: integrated the same day", "bolt"), _c("Harness green", "exit: every touched slice at its bar", "check"),
         _c("Reviewed", "exit: readers set by the band", "eye"), _c("In shadow", "exit: agreement per slice, window closed", "users")],
        [_c("Live", "exit: widened on evidence", "plane"), _c("Watching", "drift and the two numbers", "trend")],
    ]),
    callout=("A card moves on evidence, never on a date. The exit criterion is the column's whole definition.", P2, 40),
    alt="A kanban board for agentic delivery: nine columns across the four phases, each with its exit criterion",
)

MAPS["cut-delivery-time"] = dict(
    kind="bands", title=[("What compresses", P0), ("and what will not",)], flow=False,
    bands=[
        {"hue": P0, "key": "Compresses", "name": "When AI builds", "cells": [_c("Writing code and tests", "hours, not days", "code"), _c("Drafting specs and docs", "it drafts, you check", "pen")]},
        {"hue": P1, "key": "Compresses", "name": "Only by redesign", "cells": [_c("Decisions", "per action, not per system", "ladder"), _c("Review", "routed by risk band", "eye"),
                                                                                 _c("Integration", "cut by dependency, daily", "bolt"), _c("Lead times", "started on day one", "clock")]},
        {"hue": "k", "key": "Does not", "name": "Compress", "cells": [_c("Live evidence", "arrives at traffic speed", "wave"), _c("A shadow window", "fixed in advance", "calendar")]},
    ],
    callout=("Months become weeks by redesigning the four things in the middle. Evidence arrives at the speed of traffic, whatever the model.", "k", 40),
    alt="Three bands: what compresses when AI builds, what compresses only by redesign, what does not compress",
)

MAPS["review-ai-generated-code"] = dict(
    kind="fan", title=[("Review by risk", "k"), ("never by diff size",)], start="A change",
    q="The most dangerous tool or path it touches?",
    outs=[_c("R4 · R5", "two named readers, every time", "lock", "k") | {"via": "money, identity, policy, irreversible"},
          _c("R2 · R3", "one reader, after the harness", "users", P3) | {"via": "a write, reversible or hard to reverse"},
          _c("R1", "the harness alone, escapes counted", "check", P0) | {"via": "reads only"}],
    callout=("Four hundred lines of help text cannot move money; three lines in a refund cap can. The band decides the readers.", "k", 40),
    alt="One question routes a change to R4-R5 with two readers, R2-R3 with one, or R1 with the harness alone",
)

MAPS["how-accurate-must-an-ai-agent-be"] = None
MAPS["prove-ai-accuracy"] = None
MAPS["shadow-mode-and-cutover"] = None
MAPS["ai-agent-costs"] = None
MAPS["ai-guardrails-that-hold"] = None

MAPS["ai-governance-gates"] = dict(
    kind="flow", title=[("Five gates", "k"), ("that do not slow delivery",)], hue="k", numbered=True, gap=26,
    nodes=[_c("Intent", "product manager · pain, AI-fit, value line", "flag"), _c("Plan", "PM and architect · bolts, authority, gates", "calendar"),
           _c("Behaviour", "QA lead · per slice, lower bound", "chart"), _c("Release", "product manager · shadow run, rollback", "plane"),
           _c("Expansion", "QA lead · live evidence, drift", "trend")],
    terminal=_c("While live", "a drift alert re-opens release", h="o"),
    callout=("A gate is defined by a name on it and the evidence it needs, never by a meeting. The last one re-opens itself.", "k", 40),
    alt="The five governance gates in order, each with its owner, and the drift alert that re-opens release",
)

MAPS["ai-drift-monitoring"] = None

MAPS["ai-incident-postmortem"] = dict(
    kind="flow", title=[("The postmortem", "k"), ("finds the missing control",)], hue="k", numbered=True, gap=26,
    nodes=[_c("Ask one question", "the missing control?", "ask"), _c("Classify layers", "enforced, asked, absent", "layers"),
           _c("Close the path", "in code, with tests", "code"), _c("Lower the autonomy", "and name what restores it", "ladder")],
    terminal=_c("Feed it forward", "golden cases, an ADR, the next P0 brief", h="n"),
    callout=("A postmortem that produced a name has not finished. The finding is the control that would have made the incident impossible.", "k", 40),
    alt="The AI incident postmortem in five moves, from the one question to the next P0 brief",
)

MAPS["agentic-delivery-cadence"] = dict(
    kind="bands", title=[("The cadence", "t"), ("what runs when",)], flow=False,
    bands=[
        {"hue": P2, "key": "Every day", "name": "Build", "cells": [_c("One bolt, integrated", "one unknown, same day", "bolt"), _c("Review by band", "from the path rule", "eye")]},
        {"hue": P1, "key": "Every change", "name": "Prove", "cells": [_c("The harness", "per slice, required", "check"), _c("The injection suite", "every entry, every tool", "shield")]},
        {"hue": P3, "key": "Every week", "name": "Watch", "cells": [_c("Drift readout", "mix, two thresholds", "wave"), _c("The board", "queue, integration, live", "board")]},
        {"hue": "n", "key": "Cycle and quarter", "name": "Report", "cells": [_c("Two numbers", "saving beside spend", "chart"), _c("The maturity check", "six tests, run again", "clipboard")]},
        {"hue": "k", "key": "On an event", "name": "Respond", "cells": [_c("An incident", "the missing control", "warn"), _c("A surprise bill", "which signature", "bill")]},
    ],
    callout=("Daily, per change, weekly, per cycle, and on an event. Nothing here needs a ceremony that did not exist already.", "t", 40),
    alt="The delivery cadence: what runs every day, every change, every week, every cycle, and on an event",
)

MAPS["measure-ai-productivity"] = dict(
    kind="pairs", title=[("What AI inflates", "k"), ("vs",), ("what you report", P0)], arrows=False,
    left={"hue": "k", "name": "What AI inflates", "cells": [
        _c("PRs per developer", "up; delivery flat", "trend"), _c("Code generated", "volume, not value", "code"),
        _c("Suggestions accepted", "habit, not outcome", "check"), _c("Surveyed speed-up", "a belief, not a fact", "ask")]},
    right={"hue": P0, "name": "What you report", "cells": [
        _c("Person-days per story", "vs the baseline", "clock"), _c("Token spend per story", "on the same line", "bill"),
        _c("Review hours added", "high early, then falls", "eye"), _c("Re-runs per story", "where leaks show first", "loop")]},
    callout=("Two numbers on one line, and two rows that keep them honest. Everything on the left goes up whether or not delivery does.", P0, 40),
    alt="Four metrics AI inflates beside the four you report",
)

MAPS["ai-delivery-maturity-model"] = dict(
    kind="bands", title=[("Six controls", "n"), ("you can test in ten minutes",)], flow=True,
    bands=[
        {"hue": P1, "key": "P1", "name": "Written down", "cells": [_c("1 · A context file", "test: it is current", "doc"), _c("2 · Spec, bar, owner", "test: pick any story", "spec")]},
        {"hue": P2, "key": "P2", "name": "Enforced in code", "cells": [_c("3 · A merge gate", "test: lower a bar, push", "gate"), _c("4 · Caps in signatures", "test: grep the prompts", "lock")]},
        {"hue": P3, "key": "P3", "name": "Seen in production", "cells": [_c("5 · A redacting trace", "test: find no passports", "shield"), _c("6 · Drift watched", "test: the gate re-opens", "wave")]},
    ],
    terminal=_c("Level = the count", "next: the first missing control", h="n"),
    callout=("Maturity is control, not tool count. A team with nine AI tools and no gates is less mature than one with one tool and six controls.", "n", 40),
    alt="Six controls in three bands, each with its ten-minute test; the level is the count",
)

MAPS["rolling-out-agentic-delivery"] = dict(
    kind="flow", title=[("Ninety days", P0), ("one feature, five stages, one trap each",)], hue=P0, tall=True, gap=26,
    nodes=[_c("Days 1 to 15 · Choose", "for provability, not value · trap: the flagship", "target"),
           _c("Days 15 to 30 · Specify", "spec, bars, authority · trap: the persuasive demo", "spec"),
           _c("Days 30 to 60 · Build", "a slice a day, in CI · signal: merges most days", "bolt"),
           _c("Days 60 to 90 · Shadow", "beside the people, then 5% · rule: widen on evidence", "eye")],
    terminal=_c("Day 90 on · Report", "two numbers, every cycle", h="n"),
    callout=("Feature two needs less of you than feature one did. That, not the demo, is the signal the method has landed.", P0, 40),
    alt="A ninety-day rollout in five stages from choosing the feature to reporting two numbers every cycle",
)

MAPS["team-structure-for-agentic-ai"] = dict(
    kind="bands", title=[("Three layers", "n"), ("governance, product, platform",)], flow=True,
    bands=[
        {"hue": "n", "key": "Governance", "name": "A sponsor", "cells": [_c("Sponsor", "funding, the ceiling, what counts as proof", "person", "n")]},
        {"hue": P1, "key": "Product team", "name": "P0 to P3", "sub": "owns one product end to end", "cells": [
            _c("Product manager", "pain, autonomy, bar", "target"), _c("Solution architect", "map, authority, ADRs", "layers"),
            _c("Engineering lead", "floor and boundary", "code"), _c("QA lead", "the arithmetic veto", "scale")]},
        {"hue": "t", "key": "Platform team", "name": "Shared", "sub": "what every team needs", "cells": [
            _c("Gateway and log", "every call, per case", "server"), _c("Harness template", "gates every merge", "gear"), _c("Landing zone", "accounts, tags, traces", "cloud")]},
    ],
    callout=("No new roles, none disappears. Two boundaries move: the PM stops approving code, and QA's veto becomes arithmetic.", "n", 40),
    alt="Three layers: a sponsor for governance, a product team of four owning P0 to P3, and a shared platform team",
)

# ============================================================================ practice, case, careers
MAPS["skyways-case-study"] = dict(
    kind="bands", title=[("SkyWays", P1), ("ninety days, thirteen episodes",)],
    bands=[
        {"hue": P0, "key": "P0 · days 1 to 9", "name": "Frame", "cells": [
            _c("Day 1 · Requirements", "31, four the same", "doc"), _c("Day 4 · The email", "every line credited", "mail"),
            _c("Day 6 · A $400 limit", "reshapes three NFRs", "money"), _c("Day 9 · NFR workshop", "nine ratified", "users")]},
        {"hue": P1, "key": "P1 · days 12 to 20", "name": "Spec", "cells": [
            _c("Day 12 · Two ADRs", "one per tension", "scale"), _c("Day 15 · Eight fields", "from a 30-page PRD", "spec"), _c("Day 20 · Buy or build", "fast start, closed door", "swap")]},
        {"hue": P2, "key": "P2 · days 30 to 60", "name": "Build", "cells": [
            _c("Day 30 · First bolt", "on screen by 4 pm", "bolt"), _c("Day 45 · 82.4% vs 80", "a score, not a proof", "chart"), _c("Day 60 · A 4-day queue", "two of nine touch money", "clock")]},
        {"hue": P3, "key": "P3 · days 75 to 90", "name": "Run", "cells": [
            _c("Day 75 · A 4.4× bill", "flat traffic, cold cache", "bill"), _c("Day 82 · A refund", "$2,000, not owed", "warn"), _c("Day 90 · Both numbers", "time saved, money spent", "trend")]},
    ],
    callout=("Failures left in: the score that was not a proof, the queue that was money, the bill that was habits. Each closed a loop.", P1, 40),
    alt="The SkyWays case: thirteen dated episodes across the four phases",
)

MAPS["agentic-pdlc-exercises"] = dict(
    kind="bands", title=[("Twelve exercises", P2), ("three per phase",)],
    bands=_phase_bands([
        [_c("1 · AI or rule?", "", "ask"), _c("2 · Value", "", "money"), _c("3 · Hard or soft?", "", "gate")],
        [_c("4 · The bar", "", "scale"), _c("5 · Chains", "", "layers"), _c("6 · Agents", "", "robot")],
        [_c("7 · Proven?", "", "chart"), _c("8 · Cases, days", "", "clock"), _c("9 · The queue", "", "table")],
        [_c("10 · The bill", "", "bill"), _c("11 · Drift", "", "wave"), _c("12 · A control?", "", "shield")],
    ]),
    callout=("Commit to an answer before you open the worked one. Each exercise is the arithmetic of its phase.", P2, 40),
    alt="Twelve exercises, three per phase",
)

MAPS["agentic-delivery-simulator"] = dict(
    kind="flow", title=[("The playbook", "n"), ("how to practise with it",)], hue="n", numbered=True,
    nodes=[_c("Read an episode", "each one closes a loop", "book"), _c("Run it twice", "loop-closing path first", "loop"),
           _c("Use your numbers", "17 tools, formulas shown", "chart"), _c("Add the artefact", "to the evidence pack", "clipboard")],
    terminal=_c("Download the pack", "one markdown file", h=P0),
    callout=("Thirteen dated episodes, nine simulations, seventeen calculators. Run each episode once as written and once your way.", "n", 40),
    alt="Five moves for practising with the SkyWays playbook, ending with the downloaded evidence pack",
)

MAPS["how-this-tutorial-works"] = dict(
    kind="flow", title=[("Every lesson", "t"), ("the same seven parts",)], hue="t", numbered=True, gap=22,
    nodes=[_c("The answer", "one paragraph, first", "check"), _c("A picture", "the idea as a shape", "layers"),
           _c("Sound familiar?", "the problem, stated", "ask"), _c("Step by step", "one idea per step", "steps"),
           _c("Try it", "commit before you look", "pen"), _c("Three takeaways", "what to keep", "target"),
           _c("Sources", "each idea credited", "book")],
    callout=("Same shape every time, so you can read only the part you need. The answer comes first; the argument follows.", "t", 40),
    alt="The seven parts every lesson has, in order",
)

MAPS["what-is-a-forward-deployed-engineer"] = dict(
    kind="bands", title=[("Product engineer", "s"), ("vs",), ("forward-deployed engineer", "t")], flow=False,
    bands=[
        {"hue": "s", "key": "A product engineer", "name": "One capability, many customers", "cells": [
            _c("One capability", "built once", "gear"), _c("Many customers", "use it as shipped", "users")]},
        {"hue": "t", "key": "A forward-deployed engineer", "name": "One customer, many capabilities", "cells": [
            _c("One customer", "embedded with them", "person"), _c("Many capabilities", "made to work there", "tool")]},
    ],
    terminal=_c("Back into the product", "patterns, codified, for the next customer", h="t") | {"label": "patterns, codified"},
    callout=("The FDE's output is not only the deployment: it is the pattern that goes back into the product for the next customer.", "t", 40),
    alt="A product engineer builds one capability for many customers; a forward-deployed engineer makes many capabilities work for one, and codifies the patterns back",
)

MAPS["how-to-answer-ai-interview-questions"] = dict(
    kind="pairs", title=[("If they ask…", "s"), ("reach for",), ("the framework", P1)], arrows=True,
    left={"hue": "s", "name": "If they ask…", "cells": [
        _c("Design an AI product", "", "target"), _c("Is 92% good enough?", "", "scale"), _c("Why is it wrong?", "", "ask"),
        _c("Why did cost jump?", "", "bill"), _c("It caused harm. Now?", "", "warn"), _c("Tell me about a time", "", "person")]},
    right={"hue": P1, "name": "…reach for", "cells": [
        _c("The P0 to P3 answer", "", "layers"), _c("The bar in three lines", "", "chart"), _c("The grounding triangle", "", "search"),
        _c("The four signatures", "", "lock"), _c("The missing control", "", "shield"), _c("STAR, number, change", "", "trend")]},
    callout=("Six question shapes, six frameworks. Each framework is a structure the interviewer can follow and a number they can check.", P1, 40),
    alt="Six kinds of AI interview question, each matched to the framework for answering it",
)

MAPS["ai-product-manager-interview-questions"] = dict(
    kind="pairs", title=[("The round", "s"), ("and",), ("the AI twist", P0)], arrows=True,
    left={"hue": "s", "name": "The round", "cells": [
        _c("Product sense", "", "target"), _c("Analytics", "", "chart"), _c("Strategy", "", "flag"), _c("Technical", "", "code"), _c("Leadership", "", "users")]},
    right={"hue": P0, "name": "The AI twist", "cells": [
        _c("Is it AI work at all?", "", "ask"), _c("Good enough, per slice", "", "scale"), _c("Where the moat is", "", "shield"),
        _c("Retrieval or model?", "", "db"), _c("Evidence over hype", "", "check")]},
    callout=("The classic PM round, and the question inside each that only an AI product manager can answer.", P0, 40),
    alt="The five parts of a product manager interview round, each with its AI twist",
)

def _bank(slug, title, hue, groups, callout):
    MAPS[slug] = dict(
        kind="bands", title=title, flow=True,
        bands=[{"hue": h, "key": k, "name": n, "cells": [_c(t, "", i) for t, i in cells]} for h, k, n, cells in groups],
        callout=(callout, hue, 40),
        alt=f"The ten questions in this bank, grouped: " + "; ".join(n for _h, _k, n, _c_ in groups),
    )

_bank("agentic-ai-engineer-interview-questions", [("Agentic AI engineer", P2), ("ten questions",)], P2, [
    (P0, "1 to 2", "The loop and the rung", [("1 · Walk the loop", "loop"), ("2 · Not an agent", "code")]),
    (P1, "3 to 5", "Authority and tools", [("3 · The refund cap", "lock"), ("4 · A good tool", "tool"), ("5 · MCP security", "shield")]),
    (P2, "6 to 7", "Topology and evaluation", [("6 · One agent or many", "robot"), ("7 · Evaluate an agent", "chart")]),
    (P3, "8 to 10", "Running it", [("8 · Runaways", "warn"), ("9 · People in the loop", "users"), ("10 · Your failure", "person")]),
], "Each question tests one thing. The strong answer names the cap, the checker or the number; the weak one names a framework.")

_bank("genai-engineer-interview-questions", [("GenAI engineer", P1), ("ten questions",)], P1, [
    (P1, "1 to 3", "Quality", [("1 · RAG is wrong", "search"), ("2 · Evaluate it", "chart"), ("3 · Fine-tune?", "brain")]),
    (P3, "4 to 6", "Performance and cost", [("4 · 8 s to 2 s", "clock"), ("5 · The bill doubled", "bill"), ("6 · Pick a model", "swap")]),
    (P2, "7 to 8", "Safety and structure", [("7 · Injection", "shield"), ("8 · Reliable JSON", "code")]),
    ("n", "9 to 10", "State and story", [("9 · Memory", "db"), ("10 · Your system", "person")]),
], "Retrieval, evaluation, cost, safety, state: the five things a GenAI engineer is really being asked about.")

_bank("forward-deployed-engineer-interview-questions", [("Forward-deployed engineer", "t"), ("ten questions",)], "t", [
    (P0, "1 to 3", "Discover and scope", [("1 · The first two weeks", "calendar"), ("2 · A demo in three days", "clock"), ("3 · Build, buy or no", "swap")]),
    (P2, "4 to 6", "Build and prove", [("4 · An eval in a week", "chart"), ("5 · Works here, not there", "warn"), ("6 · Design for a bank", "shield")]),
    (P3, "7 to 10", "Hand over and feed back", [("7 · What you leave", "handoff"), ("8 · More autonomy, now", "ladder"), ("9 · The sceptic", "person"), ("10 · A pattern, codified", "book")]),
], "The FDE is judged on what they leave behind: evidence a customer can run, and a pattern the product can absorb.")

_bank("aws-generative-ai-interview-questions", [("AWS generative AI", P3), ("ten questions",)], P3, [
    (P1, "1 to 2", "Architecture", [("1 · A regulated agent", "shield"), ("2 · Which framework", "layers")]),
    ("n", "3 to 5", "Access, security and data", [("3 · Access denied", "lock"), ("4 · Enterprise access", "users"), ("5 · RAG on Bedrock", "db")]),
    (P3, "6 to 7", "Cost and resilience", [("6 · Cost at scale", "bill"), ("7 · Throttling", "clock")]),
    (P2, "8 to 10", "Operate", [("8 · Observe it", "eye"), ("9 · Deploy it", "cloud"), ("10 · Well-Architected", "check")]),
], "Bedrock, AgentCore, Guardrails, Knowledge Bases: the questions test whether you know what the service decides for you and what it does not.")

MAPS = {k: v for k, v in MAPS.items() if v is not None}
