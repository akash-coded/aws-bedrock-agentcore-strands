"""The words of the forward-deployed engineer guide's hub, /forward-deployed-engineer/, as data.

Council 10's verdict, section 2.6, sets the sections and their headings. The words are the FDE paper's section
2.4, with the verdict's changes: no reference to the home page's hero, the game called the simulator, and "some
weeks you are the whole team", never "always". pages/fde.py renders them, and ``check()`` holds them to the
house rules. build_content.py runs it on every build of the roles, and the renderer can run it too.

How the words name things, so that a page never types a fact:
- a quotation is ``{{S1-own}}`` and a source's mark alone is ``[[S12]]``, both records in fde_sources.py;
- a fact about an AI tool is its id in content/tools/tools.json, rendered with its own source and date;
- a step of this guide is its number, 1 to 12; another role's steps are its id and step numbers;
- a lesson is its slug in content/learn/lessons/; a page of the site is its address from the site's root.

Text is the role sources' markdown-lite (render.md(): ``**bold**``, ``*italics*``, `` `code` ``), with the marks
above. Counts the role already knows are left out: the head's "3 stages, 12 steps, 12 templates, 30 prompts" is
computed from the role's JSON. A count written in the words, such as "Six dated facts", is checked against
the list it counts.
"""
from __future__ import annotations

HEAD = {
    "eyebrow": "Your role, end to end",
    "h1": "Forward-deployed engineer",
    "lede": "From a customer's pain to a system they run after you leave.",
    # the folded how-to, as on every role page: who it is for, what to use it for, how
    "for": ("Engineers who build inside a customer's organisation, or inside another team in their own company, "
            "and anyone who hires, manages or works beside one."),
    "use": "Run an engagement end to end, with a template, prompts and the words to say at every step.",
    "how": ["Read the picture: it is the whole job.",
            "Read the altitude table before your next proof of concept.",
            "Open the stage you are in."],
}

# The framework picture's own words (verdict 2.4). The stage column and the signatures come from the role's
# HEAD["stages"]; the steps' short names, questions and artefacts from its steps.
FIGURE = {
    "title": "Frame, deliver, evolve: the same four questions, three times",
    "caption": "Rows are an engagement's three stages, in order. Columns are the manual's four phases, P0 to P3.",
    "corner": "Across: the order. Down: one question, three scales.",
    "phases": {"P0": "Is it worth doing?", "P1": "What exactly, who signs?",
               "P2": "Does it meet the bar?", "P3": "Is it working, at what cost?"},
    "signed": "Signed",
    "foot": "Every box opens its step: template, prompts, a worked example. After the review, Frame starts again.",
    "label": ("The FDE framework: three stages, Frame, Deliver and Evolve, each asking the four questions P0 to P3 "
              "about a different thing, and each ending in a signature"),
}

RAIL = {"guide": "The guide", "stages": "The stages"}

SECTIONS = [
    {"id": "what", "rail": "What an FDE does",
     "h2": "What does a forward-deployed engineer do?",
     "lede": ("An engineer who works inside a customer's organisation and owns the outcome there, then carries what "
              "they learnt back home. The job runs in three stages that are its own initials: Frame, Deliver, "
              "Evolve. In the words of three companies that run FDE teams:"),
     "quotes": ["S1-own", "S13-cto", "S6-codify"],
     "judged": {
         "h3": "You are judged on five things",
         "items": ["**Impact**: value against the customer's goals, and the system becomes part of their work.",
                   "**Delivery**: milestones hit, little reopened.",
                   "**Reuse**: patterns of yours that other deployments use.",
                   "**Judgement** under pressure.",
                   "**Product**: field signal that changes a roadmap."],
         "source": "OpenAI's measures for a Deployment Lead in its FDE team [[S2]].",
     },
     "link": {"lesson": "what-is-a-forward-deployed-engineer", "text": "The lesson: What is an FDE?"}},

    {"id": "hats", "rail": "Six hats",
     "h2": "One person, six hats, and the decisions stay theirs.",
     "lede": ("Some weeks you are the whole team. Each hat has a role page here: borrow its steps. What the last "
              "column names, you draft and they sign."),
     # beside the heading on a wide screen, after the paragraph on a phone; its caption is the sketch's own
     "sketch": "what-is-a-forward-deployed-engineer",
     "head": ["The hat", "What you do in it", "Borrow these steps", "What stays theirs"],
     "rows": [
         {"hat": "product", "name": "Product manager", "do": "Measure the pain, size the value, cut the first slice",
          "role": "product-manager", "steps": [1, 2, 3], "borrow": "PM steps 1 to 3",
          "theirs": "Which pain is worth paying for"},
         {"hat": "architect", "name": "Solution architect", "do": "Map the steps, draft the authority budget",
          "role": "solution-architect", "steps": [3, 6], "borrow": "Architect steps 3 and 6",
          "theirs": "Every limit, and who approves above it"},
         {"hat": "engineer", "name": "Engineer", "do": "Build in their repository, with their engineers",
          "role": "engineering", "steps": [1, 2, 3, 4, 5], "borrow": "Engineering steps 1 to 5",
          "theirs": "Merge rights, and who owns the code"},
         {"hat": "qa", "name": "QA lead", "do": "Build the golden set, the harness and the shadow",
          "role": "qa", "steps": [2, 4, 7], "borrow": "QA steps 2, 4 and 7",
          "theirs": "What counts as a right answer"},
         {"hat": "platform", "name": "Platform", "do": "Access, environments, the rollback",
          "role": "devops", "steps": [2, 3, 8], "borrow": "DevOps steps 2, 3 and 8",
          "theirs": "Who runs it after you leave"},
         {"hat": "consultant", "name": "Consultant", "do": "Discovery, the statement of work, the readout, the review",
          "role": "forward-deployed-engineer", "steps": [1, 2, 4, 12], "borrow": "This guide, steps 1, 2, 4 and 12",
          "theirs": "The decision to buy, and to continue"},
     ],
     "after": [
         ("At a larger vendor the work is split in two. Palantir pairs its engineers with Deployment Strategists "
          "[[S12]], and Databricks does the same [[S15]]. Anthropic adds a Technical Deployment Lead [[S7]], and "
          "Ramp an AI Solutions Strategist [[S17]]. Glean puts its founding FDEs {{S28-pod}}. Learn both halves: "
          "when the pair is one short, you are both."),
         ("Wear the consultant's hat as a craft. AWS sets its FDEs against consulting that {{S20-consulting}}: you "
          "build, and you stay until it runs."),
     ]},

    {"id": "altitude", "rail": "Altitude",
     "h2": "Think at the altitude the step needs.",
     "lede": ("Most FDE mistakes are a right answer at the wrong altitude: a proof built like production, or "
              "production built like a proof."),
     # each column names the guide's steps that think at its altitude; a step's own chip is its "level"
     "columns": [
         {"name": "POC", "steps": [3], "when": "step 3 · days"},
         {"name": "MVP", "steps": [5, 6, 7], "when": "steps 5 to 7, one slice · weeks"},
         {"name": "Build", "steps": [7], "when": "step 7, every slice · weeks"},
         {"name": "Deploy", "steps": [8], "when": "step 8 · until handover"},
     ],
     "rows": [
         ["The question", "Can it work at all, on their data?",
          "Will one group of real users get value from the thinnest version?",
          "Will it hold on every slice, at full volume, when things go wrong?", "Will it keep working without you?"],
         ["You think about", "One hypothesis", "One workflow and one slice",
          "The system: every slice, every failure, the cost", "The organisation: owners, operations, the contract"],
         ["Code", "Throwaway, in a sandbox", "Their repository, their identity, the floor tested",
          "Caps in tool signatures, the harness blocking the merge, traces", "Runbooks, timed switches, alerts with owners"],
         ["Evidence", "A number with its sample size, and what it does not prove",
          "A pass mark for the slice, and agreement in shadow",
          "The lower bound above the pass mark, per slice, and cost per case",
          "The saving and the spend on one line, and drift watched"],
         ["You may skip", "Hardening, scale, the interface", "Other slices, and any autonomy above drafting",
          "Nothing in scope", "Nothing"],
         ["Never skip", "Writing down what it does not prove", "Their risk owner's signature",
          "A harness the merge cannot pass", "The person on their side who will run it"],
         ["Your AI tools", "A coding agent writes most of it. You read the evaluation, line by line",
          "The agent builds from a story file. You review every change that touches their systems",
          "The agent writes and the harness proves. Two people read anything that moves money",
          "The agent drafts the runbooks. People rehearse them with a stopwatch"],
         ["Ends with", "Go, go with conditions, change course, or stop", "A shadow report", "The pass mark met, slice by slice",
          "A handover signed by their operator"],
         ["The trap", "The demo becomes the success criterion",
          "The first slice becomes the product without a pass mark", "Polishing slices nobody uses",
          "Leaving with nobody owning it"],
     ],
     "after": ("The proof column follows GOV.UK's service manual on alpha: build things {{S26-complex}}, and "
               "{{S26-throw-away}}. Anthropic's own advice on agents points the same way: {{S25-simplest}}.")},

    {"id": "clients", "rail": "Internal or external",
     "h2": "Your client may sit in your own company.",
     "lede": "The twelve steps do not change. Five things do.",
     "head": ["External client", "Internal client"],
     "rows": [
         ["The agreement", "A statement of work, signed by both companies", "A charter, signed by the business unit's head"],
         ["Saying no", "A change request, sized in days", "A trade-off put to the sponsor you share"],
         ["Where learning goes", "Your product team, or your practice's library", "Your platform's backlog"],
         ["How it ends", "Handover, then the contract closes",
          "Handover on the charter's date, or you become their team for good"],
         ["What failure costs", "The renewal", "Their trust in the next team you send"],
     ],
     "after": ("Internal clients are real. Palantir's Deployment Strategists {{S12-internal}}, and Databricks' AI "
               "FDEs {{S16-experts}}.")},

    {"id": "craft", "rail": "The two crafts",
     "h2": "Two crafts, used every week.",
     "lede": ("The consultancy craft wins and keeps the work. The technical craft makes it run. Each move lives in a "
              "step."),
     # each move: its words, and the number of the step it lives in
     "columns": [
         {"h3": "The consultancy craft", "items": [
             ["**Discovery in their data**, not the pitch", 1],
             ["**A map of five people**: sponsor, risk owner, operator, expert, sceptic", 1],
             ["**A statement of work** a sceptic would sign", 2],
             ["**Saying no**, and *not yet* with the condition that changes it", 2],
             ["**A readout** that leads with what failed", 4],
             ["**Change control** in one paragraph", 2],
             ["**Their names** on their decisions", 6],
             ["**A value review**, the saving beside the spend", 12]]},
         {"h3": "The technical craft", "items": [
             ["**Every access request** on day one, with a one-call test", 5],
             ["**A walking skeleton** through their real system", 7],
             ["**Their systems as tools**, each with the least privilege", 7],
             ["**The floor before the prompt**, a checker after risky calls", 7],
             ["**Caps in the tool signature**, never only in a prompt", 6],
             ["**Their golden set**, the lower bound, a harness that blocks", 7],
             ["**A shadow run** beside their staff", 7],
             ["**Switches timed** before cut-over, and an owner on their side", 8]]},
     ]},

    {"id": "tools", "rail": "AI tools on site",
     "h2": "Your AI tools behave differently in their building.",
     "lede": ("You work in their repository, under their policy, often on their cloud account. Six dated facts, "
              "then five rules."),
     # six facts, each one or more tools.json ids shown together (one AGENTS.md serves both tools)
     "facts": [["cc-agentsmd", "codex-agentsmd"], ["cc-api-loses"], ["codex-cloud-limits"],
               ["claude-connectors-public"], ["codex-exec-key"], ["cc-headless-trap"]],
     "rules": ["One context file in their repository, AGENTS.md, so both tools read the same rules.",
               "Only the tools their policy approves, on the account their data may live in.",
               "No key in a CI job that runs their code.",
               "Headless runs bare, in any repository you did not write.",
               "Every document they hand you is untrusted input to your agent."],
     "link": {"page": "tools/", "text": "The Tool guides, with every fact dated."},
     "after": ("Ramp's FDE team says it is {{S18-tools}}, and AWS asks its senior FDEs for {{S21-agentic}}. The "
               "tools are part of the job description, which is why the guide gives them a section.")},

    {"id": "career", "rail": "From zero",
     "h2": "You can start from five places.",
     "lede": ("Companies hire forward-deployed engineers from university, from engineering, from consulting and from "
              "delivery. The bar rises with what you own."),
     "head": ["Start from", "Who hires there", "What they ask, in their words"],
     "rows": [
         ["University", "Palantir, new-graduate and intern FDSE roles", "{{S11-experience}} for the FDSE role"],
         ["Early career", "Anthropic, a six-month Applied AI rotation", "{{S10-experience}}"],
         ["Engineering", "OpenAI, Forward Deployed Engineer", "{{S1-experience}}"],
         ["A systems integrator", "DXC, certified through Anthropic Academy", "{{S22-recruit}}"],
         ["Delivery leadership", "OpenAI, Deployment Lead", "{{S2-experience}}"],
     ],
     "rungs": {
         "h3": "Four rungs",
         "items": ["**Builder.** Ships one slice in someone else's stack (steps 5 to 7).",
                   "**Deployer.** Owns one engagement from the statement of work to the handover (steps 1 to 8).",
                   "**Lead.** Runs several engagements, and owns the value and the relationship (all twelve, across "
                   "accounts).",
                   "**Practice lead.** Turns patterns into product and playbooks, and hires (steps 10 to 12, for the "
                   "practice)."],
         "after": ("The top two rungs are in the managers' postings. OpenAI's FDE manager must {{S5-codify}}. "
                   "Anthropic's must {{S9-qualify}}, and build {{S9-playbooks}}."),
     },
     "plan": {
         "h3": "Ninety days to your first engagement",
         "items": ["**Days 1 to 30, build.** A rebooking agent over a public flight dataset, with one tool as an MCP "
                   "server, a refund cap in the tool's signature with its test, 200 labelled cases and a lower bound.",
                   "**Days 31 to 60, frame.** Write its discovery brief, statement of work and proof sheet as if for a "
                   "real sponsor, and have a stranger red-team the statement.",
                   "**Days 61 to 90, deliver and evolve.** Shadow it against your own labels, time the rollback, and "
                   "write the handover pack and one pattern entry. Then play the simulator from Day 1 as the whole "
                   "team: you make all thirteen calls."],
         "link": {"lesson": "forward-deployed-engineer-interview-questions", "text": "Ten interview questions, by stage."},
     },
     "hiring": ("Ramp finds drive and work ethic {{S18-predictor}}, and {{S18-founders}}. Scale wants people who "
                "{{S19-difference}}.")},

    {"id": "next", "rail": "Read next",
     "h2": "Read next.",
     # the three lessons, each shown with its title and level from the tutorial
     "lessons": ["what-is-a-forward-deployed-engineer", "ai-dlc-for-forward-deployed-engineers",
                 "forward-deployed-engineer-interview-questions"],
     "line": "Every lesson in the tutorial ends with a row for you: what a forward-deployed engineer does with it.",
     "sim": {"page": "simulator/", "text": ("Play the simulator from Day 1. You make all thirteen calls as the whole "
                                             "team: an FDE's ninety days in fifteen minutes.")},
     "next_up": {"line": "Start where every engagement starts.", "text": "Frame the engagement", "stage": "frame"}},
]

# Keys whose values name things rather than say them: they are checked as names, not as words.
NAMES = {"id", "quotes", "facts", "lesson", "lessons", "role", "page", "sketch", "hat", "stage"}


def words():
    """Every piece of the hub's own words, with where it sits."""
    def walk(where, v):
        if isinstance(v, str):
            yield where, v
        elif isinstance(v, dict):
            for k, x in v.items():
                if k not in NAMES:
                    yield from walk(f"{where}.{k}", x)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                yield from walk(f"{where}[{i}]", x)
    yield from walk("HEAD", HEAD)
    yield from walk("FIGURE", FIGURE)
    yield from walk("RAIL", RAIL)
    for s in SECTIONS:
        yield from walk(s["id"], s)


_NUMBER = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
           "ten": 10, "eleven": 11, "twelve": 12}


def _steps_in(label: str) -> list[int]:
    """The step numbers a label names: "steps 5 to 7" is 5, 6 and 7; "steps 1, 2, 4 and 12" is those four."""
    import re
    m = re.search(r"(\d+) to (\d+)", label)
    return list(range(int(m.group(1)), int(m.group(2)) + 1)) if m else [int(x) for x in re.findall(r"\d+", label)]


def _counted(text: str, noun: str) -> int | None:
    import re
    m = re.search(r"\b(\w+) " + noun, text, re.I)
    return _NUMBER.get(m.group(1).lower()) if m else None


def check(fde: dict | None = None) -> list[str]:
    """An empty list is a pass. Every record, tool fact, lesson and step the hub names exists; every count it
    writes in words matches the list it counts; the words keep the house rules.

    ``fde`` is the built guide (forward-deployed-engineer.json as a dict); without it the file is read if it
    exists, and step numbers are held to 1 to 12 until it does."""
    import importlib
    import json
    import sys
    from pathlib import Path

    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    fs = importlib.import_module("fde_sources")
    roles_dir, site = here.parent, here.parents[2]
    bad = []
    for where, text in words():
        bad += fs.house(f"fde_hub {where}", text, "prose", prices=True)

    sec = {s["id"]: s for s in SECTIONS}
    if [s["id"] for s in SECTIONS] != ["what", "hats", "altitude", "clients", "craft", "tools", "career", "next"]:
        bad.append("fde_hub: the eight sections run what, hats, altitude, clients, craft, tools, career, next (verdict 2.6)")
        return bad
    for q in sec["what"]["quotes"]:
        if q not in fs.QUOTES:
            bad.append(f"fde_hub what.quotes: no quotation record {q} in fde_sources.py")

    # counts written in words
    for text, noun, n in ((sec["what"]["lede"], "companies", len(sec["what"]["quotes"])),
                          (sec["what"]["judged"]["h3"], "things", len(sec["what"]["judged"]["items"])),
                          (sec["hats"]["h2"], "hats", len(sec["hats"]["rows"])),
                          (sec["clients"]["lede"], "things do", len(sec["clients"]["rows"])),
                          (sec["tools"]["lede"], "dated facts", len(sec["tools"]["facts"])),
                          (sec["tools"]["lede"], "rules", len(sec["tools"]["rules"])),
                          (sec["career"]["h2"], "places", len(sec["career"]["rows"])),
                          (sec["career"]["rungs"]["h3"], "rungs", len(sec["career"]["rungs"]["items"]))):
        said = _counted(text, noun)
        if said != n:
            bad.append(f"fde_hub: {text!r} says {said} {noun}, and the list holds {n}")

    # tool facts, by their id in tools.json
    facts = {f["id"] for f in json.loads((site / "content" / "tools" / "tools.json").read_text(encoding="utf-8"))["facts"]}
    for group in sec["tools"]["facts"]:
        for fid in group:
            if fid not in facts:
                bad.append(f"fde_hub tools.facts: no fact {fid} in content/tools/tools.json")

    # lessons, by slug
    named = [sec["what"]["link"]["lesson"], sec["career"]["plan"]["link"]["lesson"], *sec["next"]["lessons"]]
    for slug in named:
        if not (site / "content" / "learn" / "lessons" / f"{slug}.md").exists():
            bad.append(f"fde_hub: no lesson {slug} in content/learn/lessons/")

    # the guide itself
    if fde is None and (roles_dir / "forward-deployed-engineer.json").exists():
        fde = json.loads((roles_dir / "forward-deployed-engineer.json").read_text(encoding="utf-8"))
    by_n = {s["n"]: s for s in fde["steps"]} if fde else {}

    def own(where: str, n: int) -> None:
        if not (isinstance(n, int) and 1 <= n <= 12) or (by_n and n not in by_n):
            bad.append(f"fde_hub {where}: the guide has no step {n}")

    # the hats: the six, once each, and each row's borrowed steps exist where they point
    hats = [r["hat"] for r in sec["hats"]["rows"]]
    if sorted(hats) != sorted(["product", "architect", "engineer", "qa", "platform", "consultant"]):
        bad.append(f"fde_hub hats: the six hats once each, product, architect, engineer, qa, platform and consultant ({hats})")
    for r in sec["hats"]["rows"]:
        where = f"hats.{r['hat']}"
        if _steps_in(r["borrow"]) != r["steps"]:
            bad.append(f"fde_hub {where}: {r['borrow']!r} does not say steps {r['steps']}")
        if r["role"] == "forward-deployed-engineer":
            for n in r["steps"]:
                own(where, n)
            continue
        path = roles_dir / f"{r['role']}.json"
        if not path.exists():
            bad.append(f"fde_hub {where}: no role {r['role']}")
            continue
        have = {s["n"] for s in json.loads(path.read_text(encoding="utf-8"))["steps"]}
        for n in r["steps"]:
            if n not in have:
                bad.append(f"fde_hub {where}: {r['role']} has no step {n}")

    # the altitudes: each column's steps exist, its label says them, and the steps carry that level
    for c in sec["altitude"]["columns"]:
        where = f"altitude.{c['name']}"
        if _steps_in(c["when"]) != c["steps"]:
            bad.append(f"fde_hub {where}: {c['when']!r} does not say steps {c['steps']}")
        for n in c["steps"]:
            own(where, n)
            level = (by_n.get(n) or {}).get("level")
            if by_n and n in by_n and c["name"].lower() not in str(level).lower():
                bad.append(f"fde_hub {where}: step {n}'s level is {level!r}, and the table puts it at {c['name']}")
    if len({len(r) for r in sec["altitude"]["rows"]} | {len(sec["altitude"]["columns"]) + 1}) != 1:
        bad.append("fde_hub altitude: every row has a head and one cell per column")
    if len({len(r) for r in sec["clients"]["rows"]} | {len(sec["clients"]["head"]) + 1}) != 1:
        bad.append("fde_hub clients: every row has a head and one cell per column")
    if len({len(r) for r in sec["career"]["rows"]} | {len(sec["career"]["head"])}) != 1:
        bad.append("fde_hub career: every row has one cell per column")

    # the crafts: eight moves each, each in a step that exists
    for col in sec["craft"]["columns"]:
        if len(col["items"]) != 8:
            bad.append(f"fde_hub craft: {col['h3']!r} has {len(col['items'])} moves, and the verdict gives eight")
        for text, n in col["items"]:
            own(f"craft {text[:30]!r}", n)

    if sec["next"]["next_up"]["stage"] not in ("frame", "deliver", "evolve"):
        bad.append("fde_hub next.next_up: a stage is frame, deliver or evolve")
    return bad
