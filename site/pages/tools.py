"""The tool guides: /tools/, the AI tools a team uses sorted by job, and one manual per way of working.

Where things are:

- ``site/content/tools/tools.json``: every fact, each with its source address and the date it was checked.
  ``README.md`` beside it is the authoring guide. Nothing on these pages states a fact about a tool that is
  not a sentence in that file.
- this module: loads and checks the facts, holds the two manuals' words, and renders the index
  (``/tools/``) and one page per manual (``/tools/<slug>/``).

A manual's text marks each fact it uses. ``{{id}}`` puts the fact's own sentence on the page, followed by a
numbered mark that links to the fact's row in the dated table at the foot; ``[[id]]`` puts the mark alone,
after a sentence that leans on the fact. Each manual lists its facts in ``facts``, and the check below
refuses a manual whose marks and list disagree, so the table at the foot is every fact the page used.

A fact goes stale sixty days after it was checked. The build then prints a warning naming the page and the
fact, and the page shows its "Last checked" date in amber. ``TOOLS_TODAY=2026-12-15`` pretends it is that
day, to see both.
"""
from __future__ import annotations

import json
import os
import re
from datetime import date
from html import escape as _E
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "content" / "tools" / "tools.json"
STALE_DAYS = 60
FAMILIES = ("claude", "openai", "google")
STATUS = {"GA", "beta", "public beta", "preview", "research preview", "experimental"}
PHASE_HUE = {"P0": "slate", "P1": "indigo", "P2": "teal", "P3": "amber"}
LAB = "../../labs/grow-the-spec/"

# What a fact or a manual must never say. Prices and model names move monthly, so the pages link to the
# vendor's own page for them; the house style bans a few words and every long dash.
MODEL_NAMES = re.compile(r"\b(Opus|Sonnet|Haiku|Fable|Mythos|GPT-?\d[\w.]*|Gemini \d[\w.]*|Astra|Luna|Terra|Sol|"
                         r"o[134](-mini|-pro)?|Nano Banana|Veo|Lyria)\b")
PRICE = re.compile(r"\$\s?\d|\bUSD\b|\b\d[\d,.]*\s?(dollars|cents)\b|\bper (month|seat)\b|\ba month\b")
BANNED = re.compile(r"\b(comprehensive|robust\w*|ensur\w+|seamless\w*|leverag\w+)\b", re.I)
AMERICAN = re.compile(r"\b(organiz\w+|behavior\w*|colors?|analyz\w+|center|catalog|prioritiz\w+|"
                      r"summariz\w+|optimiz\w+|recogniz\w+|customiz\w+)\b")
DASH = re.compile("[\u2013\u2014]|\\s-\\s")
MARK = re.compile(r"\{\{([a-z0-9-]+)\}\}|\[\[([a-z0-9-]+)\]\]")

_DATA: dict | None = None


def load() -> dict:
    global _DATA
    if _DATA is None:
        _DATA = json.loads(DATA.read_text(encoding="utf-8"))
        _DATA["by_id"] = {f["id"]: f for f in _DATA["facts"]}
    return _DATA


def today() -> date:
    v = os.environ.get("TOOLS_TODAY")
    return date.fromisoformat(v) if v else date.today()


def age(f: dict) -> int:
    return (today() - date.fromisoformat(f["checked"])).days


def is_stale(f: dict) -> bool:
    return age(f) > STALE_DAYS


def long_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def short_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


# ------------------------------------------------------------------------------------------------ the manuals
# Each manual: what it is in one paragraph, when not to use it, five moves with the real prompt or command,
# what it is poor at, three settings, its traps, and every fact it used in a dated table. The words are the
# site's (DESIGN.md, EXPERIENCE.md); every sentence that states a fact about a tool is a fact from the file.

def _lab_prompts() -> dict[str, str]:
    """The two prompts the manuals borrow from the lab Grow the spec, read from the lab itself, so the words on
    the page are the words the lab's recordings answer."""
    from pages import labs
    lab = next(x for x in labs.load() if x["slug"] == "grow-the-spec")
    beats = {b["id"]: b for b in lab["beats"]}
    ask = next(o["text"] for p in beats["ask"]["parts"] if "options" in p for o in p["options"] if o["id"] == "ask")
    hand = next(c["body"] for c in beats["hand"]["cols"] if c["id"] == "struct").split("\n\nDOCUMENT:")[0]
    return {"ask": ask, "hand": hand + "\n\nDOCUMENT:\n<the signed spec: fields 3, 7 and 8>"}


SECTIONS = [("what", "What it is"), ("not", "When not to use it"), ("moves", "Five moves"),
            ("poor", "Where it falls short"), ("settings", "Three settings"), ("traps", "Its traps"),
            ("facts", "The facts, dated")]

DESK = {
    "slug": "claude-at-the-desk", "n": 1, "name": "Claude at the desk",
    "kicker": "Tool guide 1 · the Claude apps",
    "h1": "How the airline's team uses Claude at the desk",
    "lede": "Chat, Projects, skills, connectors and scheduled tasks, for the people who write the spec.",
    "card": "Chat, Projects, skills, connectors and scheduled tasks, as the people who write the spec use them.",
    "what": {"h2": "What the Claude apps do for a team", "body": (
        "Claude at the desk means the Claude apps, on the web, the desktop and the phone. {{claude-chat-one}} "
        "{{claude-chat-rollout}} Around the chat sit the four things this manual covers: projects, skills, "
        "connectors and scheduled tasks. At the fictional airline, this is where Priya, the product manager, "
        "writes the rebooking assistant's spec, and where Maya, the QA lead, reads the 500 past cases.")},
    "not": {"h2": "When to reach for something else", "items": [
        "When the work is code in a repository. That is [Claude in the repo](../claude-in-the-repo/), the second manual.",
        "When a rule must hold every time. {{claude-projects-advice}} The $400 refund limit belongs in the refund "
        "tool's code, never in a project's instructions.",
        "When you are tuning the rebooking assistant's own system prompt. {{claude-playground}} Keep that prompt "
        "in git, beside the tests that judge it.",
        "When the system you need sits inside the airline's network. {{claude-connectors-public}}",
    ]},
    "moves": {"h2": "Five moves the airline's team makes with it",
              "lead": "Each move names who makes it, in which phase, and the words they use. Copy one and change the nouns.",
              "items": [
        {"phase": "P1", "who": "Priya, product manager", "title": "Keep the whole case in one project",
         "say": "Priya opens a project for the rebooking assistant and loads the PRD-lite, the interview notes and "
                "the glossary. {{claude-projects}} She writes its instructions once, so no chat starts cold.",
         "code": ("Project instructions", "This project is SkyWays' rebooking assistant. Owner: Priya (product).\n"
                  "Read the PRD in the project knowledge before you answer.\n"
                  "Take every number from the PRD: the 38-minute wait, the 240 cases a day, the $400 refund limit.\n"
                  "Never supply a number yourself.\n"
                  "Where the PRD is silent, write NOT DECIDED, the question, and who answers it."),
         "after": "Then she shares it with Arjun, the architect, and Maya. {{claude-projects-sharing}}"},
        {"phase": "P1", "who": "Priya, product manager", "title": "Ask for the questions before the draft",
         "say": "A draft fills every gap with a guess that reads like a decision. So Priya first asks what her one "
                "page leaves open, and who owns each answer.",
         "code": ("Prompt A, from the lab", "lab:ask"),
         "lab": "The lab Grow the spec opens on this prompt, with a real model's recorded reply"},
        {"phase": "P1", "who": "Arjun, architect", "title": "Write the spec's rules down once, as a skill",
         "say": "The eight-field spec is a procedure, and a procedure retyped into every chat drifts. "
                "{{claude-skills}} Arjun writes one for the whole team.",
         "code": ("SKILL.md", "---\nname: eight-field-spec\n"
                  "description: Turn a PRD into SkyWays' eight-field agent spec. Use when someone asks for a spec, "
                  "or for the fields a spec still lacks.\n---\n"
                  "Write exactly eight fields: Title, Value, Acceptance criteria, The model's role, Autonomy, "
                  "The bar, Fallback, Records.\n"
                  "For fields 4 to 8, where the PRD does not say, write NOT DECIDED, the question, and who "
                  "should answer it.\n"
                  "Never fill a gap with a sensible default. The gaps are what the review is for."),
         "after": "{{claude-skills-code}} Arjun reads a skill from outside the team before he switches it on, as he "
                  "would any software.",
         "lab": "The lab's second prompt teaches the same rule, and shows what a model writes without it"},
        {"phase": "P2", "who": "Maya, QA lead", "title": "Turn the 500 past cases into a workbook",
         "say": "Maya has the 500 past cases as an export: the kind of case, the old outcome, and whether it was "
                "right. {{claude-files}}",
         "code": ("Prompt, with the CSV attached", "The attached CSV holds 500 past rebooking cases, one row each.\n"
                  "Make an Excel workbook with one sheet per kind of case: same-day SkyWays, partner "
                  "(codeshare), refund, hand-over to an agent.\n"
                  "On each sheet show the count, the share handled right, and the formula behind every number.\n"
                  "Keep codeshare as its own group.\n"
                  "Do not drop or repair any row. List the rows you could not read."),
         "after": "She checks three totals by hand before any number goes near the bar. {{claude-files-warning}} "
                  "So she works from the airline's own export, never from a file a stranger sent."},
        {"phase": "P1", "who": "Priya, product manager", "title": "Chase the open questions every morning",
         "say": "A spec waits on its owners, and chasing them is a daily chore. {{claude-scheduled}} "
                "{{claude-connectors}}",
         "code": ("Scheduled task, weekdays at 08:00", "Read the rebooking assistant's board in Jira and the "
                  "#rebooking channel in Slack.\nList every spec field still marked NOT DECIDED, its owner, and the "
                  "days it has been open, oldest first.\n"
                  "Do not answer any of them. Do not post anywhere. Send the list to me."),
         "after": "{{claude-scheduled-approval}} Priya's task may read, and may not post."},
    ]},
    "poor": {"h2": "Where the apps let you down", "items": [
        "It advises and does not enforce. A project's instructions tailor what Claude "
        "writes[[claude-projects-advice]], so a limit that matters lives in code.",
        "Its memory is not a record. {{claude-memory}} Put a decision in the project's files, with a name and a "
        "date beside it.",
        "A citation shows where to look and proves nothing on its own. {{claude-research}} Open the sources that "
        "carry a decision before you quote the report.",
    ]},
    "settings": {"h2": "Three settings decide how it behaves", "items": [
        ("Memory: what it keeps between chats", "{{claude-memory-default}} {{claude-incognito}}"),
        ("Permissions: what it may touch", "{{claude-connectors-owner}} {{claude-connectors-perms}} "
                                           "{{claude-files-network}}"),
        ("Context: what every chat starts from", "{{claude-projects-rag}} Load the PRD and the decisions, and "
                                                 "leave the email threads out."),
    ]},
    "traps": {"h2": "The traps that catch a team", "items": [
        "{{claude-memory-wipe}} Keep decisions in files, where that switch cannot reach them.",
        "{{claude-chat-missing}}",
        "{{claude-cloud-beta}}",
        "{{claude-connectors-injection}}",
        "Two of Anthropic's own pages disagree on who can share a skill. {{claude-skills-platform}} "
        "{{claude-skills-org}}",
        "{{claude-scheduled-local}}",
        "{{claude-projects-chats}} So a decision reached in one member's chat belongs in the project's files, "
        "where the others can read it.",
        "For now, two things share one name. {{claude-projects-not-code}}",
    ]},
    "facts": ["claude-chat-one", "claude-chat-rollout", "claude-projects-advice", "claude-playground",
              "claude-connectors-public", "claude-projects", "claude-projects-sharing", "claude-skills",
              "claude-skills-code", "claude-files", "claude-files-warning", "claude-scheduled", "claude-connectors",
              "claude-scheduled-approval", "claude-memory", "claude-research",
              "claude-memory-default", "claude-incognito", "claude-connectors-owner", "claude-connectors-perms",
              "claude-files-network", "claude-projects-rag", "claude-memory-wipe", "claude-chat-missing",
              "claude-cloud-beta", "claude-connectors-injection", "claude-skills-platform", "claude-skills-org",
              "claude-scheduled-local", "claude-projects-chats", "claude-projects-not-code"],
    "next": ("The same team, in the code: the second manual.", "../claude-in-the-repo/", "Claude in the repo"),
}

REPO = {
    "slug": "claude-in-the-repo", "n": 2, "name": "Claude in the repo",
    "kicker": "Tool guide 2 · Claude Code",
    "h1": "How the airline's engineers use Claude in the repo",
    "lede": "Claude Code in the terminal, VS Code, the cloud and Chrome, for the people who build.",
    "card": "Claude Code in the terminal, VS Code, the cloud and Chrome, as the people who build use it.",
    "what": {"h2": "What Claude Code does for the engineers", "body": (
        "{{cc-what}} {{cc-surfaces}} At the fictional airline it builds the rebooking assistant from the signed "
        "spec: the refund tool with the $400 limit in code, its tests, and the evaluation on the 500 past cases. "
        "Arjun, the architect, owns the instructions it reads. Maya, the QA lead, owns the tests that judge what "
        "it writes.")},
    "not": {"h2": "When to reach for something else", "items": [
        "Before the spec is signed. A coding agent builds what the document says, gaps included, and the lab "
        "[Grow the spec](" + LAB + ") shows what one guesses from a paragraph.",
        "When the airline reaches Claude only through its AWS account or an API key. {{cc-api-loses}}",
        "When the job is a document, a workbook or a chase. That is [Claude at the desk](../claude-at-the-desk/), "
        "the first manual.",
    ]},
    "moves": {"h2": "Five moves the airline's engineers make with it",
              "lead": "Each move names who makes it, in which phase, and the words they type. Copy one and change the nouns.",
              "items": [
        {"phase": "P1", "who": "Arjun, architect", "title": "Write the file every session reads",
         "say": "{{cc-claudemd}} Arjun writes the project's file before the first session, and reviews changes to "
                "it like code.",
         "code": ("CLAUDE.md", "# Rebooking service\n\n"
                  "The spec is docs/spec.md. Read fields 3, 5 and 7 before you change behaviour.\n"
                  "The $400 refund limit is one constant in refund_tool.py. Never copy it into a prompt.\n"
                  "Every limit in the spec's field 5 is enforced in code, with a test below, at and above it.\n"
                  "Never book on a stale fare: when the fare engine is down, the case queues for an agent.\n"
                  "Run the tests before you call a change done."),
         "after": "{{cc-agentsmd}}"},
        {"phase": "P2", "who": "an engineer", "title": "Ask for the plan before the code",
         "say": "{{cc-modes}} Before the refund tool is touched, the engineer asks what Claude Code would build, and "
                "what it would have to guess.",
         "code": ("The hand-off prompt, from the lab", "lab:hand"),
         "after": "Every guess on the third list goes back to its owner before an edit is approved.",
         "lab": "The lab's last step runs this prompt on a paragraph and on the spec, with recorded replies"},
        {"phase": "P2", "who": "Maya, QA lead", "title": "Review the branch against the file",
         "say": "{{cc-code-review}} Maya runs it, then asks the question a review rarely asks.",
         "code": ("In the session", "/code-review\n\n"
                  "List every number in this branch that also appears in docs/spec.md.\n"
                  "For each, say whether it is read from one constant or typed again.\n"
                  "The $400 refund limit must appear once, in refund_tool.py."),
         "after": "{{cc-review-varies}} So the review is a second reader, and the test at $400.01 is the gate."},
        {"phase": "P2", "who": "an engineer", "title": "Hand the evaluation run to a cloud session",
         "say": "{{cc-cloud}} The run on the 500 past cases takes a while, so the engineer sends it away.",
         "code": ("Terminal", "git push\n"
                  "claude --cloud \"Run the evaluation on the 500 past cases in eval/cases.csv. Report the share "
                  "handled right for each kind of case, codeshare as its own group, against the bar in "
                  "docs/spec.md field 6. Open a pull request with the report. Change no code.\""),
         "after": "The push comes first. {{cc-cloud-clone}}"},
        {"phase": "P2", "who": "Maya, QA lead", "title": "Walk the agent's screen in Chrome",
         "say": "{{cc-chrome}} Maya checks what a contact-centre agent sees when the refund path runs.",
         "code": ("Terminal, then the prompt", "claude --chrome\n\n"
                  "Open the rebooking screen on the local build as the test agent.\n"
                  "Cancel booking TEST-104 and take the refund path with a $399 fare, then with a $401 fare.\n"
                  "Report what the screen shows at each step, and every console error."),
         "after": "{{cc-chrome-risk}} So Maya runs it in a browser profile signed in to the test site and nothing "
                  "else."},
    ]},
    "poor": {"h2": "Where Claude Code lets you down", "items": [
        "Its undo is partial. {{cc-checkpoints}} Commit before every long run.",
        "Auto mode is a convenience. {{cc-auto-safety}}",
        "A helper does not hear the conversation. {{cc-subagents}} {{cc-subagent-brief}} Write the brief as you would for a "
        "contractor on their first day.",
        "Its sandbox has edges. {{cc-sandbox}}",
    ]},
    "settings": {"h2": "Three settings decide how it behaves", "items": [
        ("The memory file: CLAUDE.md", "{{cc-claudemd-context}} {{cc-prompt-audit}}"),
        ("Permissions: what it may do alone", "{{cc-auto}} {{cc-deny}} {{cc-hooks}} Guard the push to main and "
                                              "the refund limit's line with a rule or a hook."),
        ("Context: what each session carries", "{{cc-skills-context}} {{cc-chrome-cli}} Switch on what this task "
                                               "needs and leave the rest off."),
    ]},
    "traps": {"h2": "The traps that catch a team", "items": [
        "A one-line job in CI can run more than you meant. {{cc-headless}} {{cc-headless-trap}}",
        "{{cc-routines}} {{cc-routines-green}} Read the pull request, not the tick.",
        "{{cc-cloud-autofix}}",
        "{{cc-worktrees}}",
        "Steering from the phone still needs your own machine. {{cc-remote}}",
    ]},
    "facts": ["cc-what", "cc-surfaces", "cc-api-loses", "cc-claudemd", "cc-agentsmd", "cc-modes", "cc-code-review",
              "cc-review-varies", "cc-cloud", "cc-cloud-clone", "cc-chrome", "cc-chrome-risk", "cc-checkpoints",
              "cc-auto-safety", "cc-subagents", "cc-subagent-brief", "cc-sandbox", "cc-claudemd-context",
              "cc-prompt-audit", "cc-auto", "cc-deny", "cc-hooks", "cc-skills-context", "cc-chrome-cli",
              "cc-headless", "cc-headless-trap", "cc-routines", "cc-routines-green", "cc-cloud-autofix",
              "cc-worktrees", "cc-remote"],
    "next": ("Back to the table: the same jobs, in every family of tools.", "../", "All the tool guides"),
}

MANUALS = [DESK, REPO]
NEXT_UP = "ChatGPT with Codex, and Google AI Studio with Jules, are next."


def _texts(m: dict) -> list[str]:
    """Every piece of a manual's own words, in the order the page shows them."""
    out = [m["lede"], m["what"]["h2"], m["what"]["body"], m["not"]["h2"], *m["not"]["items"], m["moves"]["h2"],
           m["moves"]["lead"]]
    for mv in m["moves"]["items"]:
        out += [mv["title"], mv["say"], mv.get("after", ""), mv.get("lab", "")]
    out += [m["poor"]["h2"], *m["poor"]["items"], m["settings"]["h2"]]
    out += [x for pair in m["settings"]["items"] for x in pair]
    out += [m["traps"]["h2"], *m["traps"]["items"]]
    return [t for t in out if t]


def _codes(m: dict) -> list[str]:
    lab = _lab_prompts()
    return [lab[mv["code"][1][4:]] if mv["code"][1].startswith("lab:") else mv["code"][1] for mv in m["moves"]["items"]]


# ------------------------------------------------------------------------------------------------ the check
def check(d: dict) -> list[str]:
    """What the facts and the manuals must keep to. An empty list is a pass."""
    err = []
    jobs = [j["name"] for j in d["jobs"]]
    seen = set()
    for f in d["facts"]:
        s = f"tools.json: {f.get('id', '?')}"
        for k in ("id", "family", "surface", "job", "fact", "status", "source", "checked"):
            if k not in f:
                err.append(f"{s}: missing {k}")
        if f["id"] in seen or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", f["id"]):
            err.append(f"{s}: an id is unique, in lower case with hyphens")
        seen.add(f["id"])
        if f["family"] not in FAMILIES + ("other",):
            err.append(f"{s}: family is one of {', '.join(FAMILIES)} or other")
        if f["job"] not in jobs:
            err.append(f"{s}: the job {f['job']!r} is not one of the seven")
        if f["status"] is not None and f["status"] not in STATUS:
            err.append(f"{s}: status {f['status']!r} is not a word the vendors use ({', '.join(sorted(STATUS))})")
        if not str(f["source"]).startswith("https://"):
            err.append(f"{s}: a fact carries the address of the page it came from")
        try:
            if date.fromisoformat(f["checked"]) > today():
                err.append(f"{s}: checked on a date that has not happened")
        except ValueError:
            err.append(f"{s}: checked is a date, 2026-10-02")
        t = f["fact"]
        if not t.endswith(".") or re.search(r"[.!?] +[A-Z]", t.replace("e.g. ", "")):
            err.append(f"{s}: a fact is one sentence, ending in a full stop")
        for rx, why in ((MODEL_NAMES, "a model name"), (PRICE, "a price"), (BANNED, "a banned word"),
                        (AMERICAN, "an American spelling"), (DASH, "a dash")):
            if rx.search(t):
                err.append(f"{s}: {why} ({rx.search(t).group(0)!r}); link to the vendor's page instead" if rx in (MODEL_NAMES, PRICE)
                           else f"{s}: {why} ({rx.search(t).group(0)!r})")
    cells = {}
    for f in d["facts"]:
        if f.get("cell"):
            key = (f["job"], f["family"])
            if key in cells:
                err.append(f"tools.json: two facts claim the cell {key}: {cells[key]} and {f['id']}")
            cells[key] = f["id"]
    for j in jobs:
        for fam in FAMILIES:
            if (j, fam) not in cells:
                err.append(f"tools.json: no fact names the {fam} tool for {j!r} (mark one with \"cell\": true)")
    by_id = d["by_id"]
    slugs = set()
    for m in MANUALS:
        s = f"tools/{m['slug']}"
        if m["slug"] in slugs:
            err.append(f"{s}: two manuals share a slug")
        slugs.add(m["slug"])
        if len(m["moves"]["items"]) != 5:
            err.append(f"{s}: a manual has five moves")
        if len(m["settings"]["items"]) != 3:
            err.append(f"{s}: a manual has three settings")
        texts = _texts(m)
        used = [a or b for t in texts for a, b in MARK.findall(t)]
        listed = m["facts"]
        if len(listed) != len(set(listed)):
            err.append(f"{s}: a fact is listed twice in facts")
        for i in sorted(set(used) - set(listed)):
            err.append(f"{s}: the text uses {i} and facts does not list it")
        for i in sorted(set(listed) - set(used)):
            err.append(f"{s}: facts lists {i} and the text never uses it")
        for i in sorted(set(used) | set(listed)):
            if i not in by_id:
                err.append(f"{s}: no fact called {i} in tools.json")
        for t in texts + _codes(m):
            for rx, why in ((MODEL_NAMES, "a model name"), (BANNED, "a banned word"), (AMERICAN, "an American spelling"),
                            (DASH, "a dash")):
                bare = MARK.sub("", t)
                if rx.search(bare):
                    err.append(f"{s}: {why} ({rx.search(bare).group(0)!r}) in {bare[:60]!r}")
        for t in texts:
            if re.search(r"[{}\[\]]{2}", MARK.sub("", t)):
                err.append(f"{s}: a mark that is not {{{{id}}}} or [[id]] in {t[:60]!r}")
    return err


def page_facts() -> dict[str, list[dict]]:
    """Each page and the facts it uses: the index uses every cell and every row below the families."""
    d = load()
    out = {"tools/": [f for f in d["facts"] if f.get("cell") or f["family"] == "other"]}
    for m in MANUALS:
        out[f"tools/{m['slug']}/"] = [d["by_id"][i] for i in m["facts"]]
    return out


def warnings() -> list[str]:
    out = []
    for page, facts in page_facts().items():
        for f in facts:
            if is_stale(f):
                out.append(f"{page}: fact {f['id']} was last checked {long_date(f['checked'])}, {age(f)} days ago; "
                           f"check it against {f['source']} and update its date")
    return out


# ------------------------------------------------------------------------------------------------ rendering
_TOKEN = re.compile(r"\{\{([a-z0-9-]+)\}\}|\[\[([a-z0-9-]+)\]\]|`([^`]+)`|\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)\s]+)\)")


def _code(text: str) -> str:
    """Escape, and set `code` in code."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", _E(text, quote=False))


class _Marks:
    """Numbers each fact the first time the page uses it; the table at the foot follows the same numbers."""

    def __init__(self, by_id: dict):
        self.by_id, self.order = by_id, []

    def n(self, fid: str) -> int:
        if fid not in self.order:
            self.order.append(fid)
        return self.order.index(fid) + 1

    def mark(self, fid: str) -> str:
        n = self.n(fid)
        return f'<a class="fn" href="#f-{fid}" aria-label="Fact {n}: its source and date">{n}</a>'

    def inline(self, text: str) -> str:
        out, last = [], 0
        for m in _TOKEN.finditer(text):
            out.append(_E(text[last:m.start()], quote=False))
            ins, mark, code, bold, ltext, href = m.groups()
            if ins:
                out.append(_code(self.by_id[ins]["fact"]) + self.mark(ins))
            elif mark:
                out.append(self.mark(mark))
            elif code:
                out.append(f"<code>{_E(code, quote=False)}</code>")
            elif bold:
                out.append(f"<b>{_E(bold, quote=False)}</b>")
            else:
                out.append(f'<a href="{_E(href)}">{_E(ltext, quote=False)}</a>')
            last = m.end()
        out.append(_E(text[last:], quote=False))
        return "".join(out)


def _ext(href: str, text: str, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{_E(href)}" target="_blank" rel="noopener">{text}</a>'


def _checked(facts: list[dict]) -> str:
    """The page's own "Last checked": the oldest date among its facts, in amber once any is past sixty days."""
    oldest = min(f["checked"] for f in facts)
    stale = any(is_stale(f) for f in facts)
    title = (f' title="{sum(is_stale(f) for f in facts)} of its facts are more than {STALE_DAYS} days old"' if stale else "")
    return (f'<span class="tg-ck{" stale" if stale else ""}"{title}>Last checked '
            f'<time datetime="{oldest}">{long_date(oldest)}</time></span>')


def _status(f: dict) -> str:
    return f' <span class="tg-st">{_E(f["status"])}</span>' if f.get("status") else ""


def _cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def _host(url: str) -> tuple[str, str]:
    m = re.match(r"https://([^/]+)(/.*)?", url)
    host, path = m.group(1), (m.group(2) or "/").rstrip("/")
    tail = path.rsplit("/", 1)[-1] if path else ""
    return host.removeprefix("www."), tail


def index_page(shell, ctx: dict) -> str:
    from pages import _kit as k
    import render
    d = load()
    fams = {f["id"]: f for f in d["families"]}
    in_manual = {fid: m for m in MANUALS for fid in m["facts"]}
    cells = {(f["job"], f["family"]): f for f in d["facts"] if f.get("cell")}
    rows = []
    for j in d["jobs"]:
        tds = []
        for fam in FAMILIES:
            f = cells[(j["name"], fam)]
            old = (f'<span class="tg-old stale">checked {short_date(f["checked"])}</span>' if is_stale(f) else "")
            man = in_manual.get(f["id"])
            more = (f'<a class="tg-in" href="{man["slug"]}/">In the manual {_E(man["name"])}</a>' if man else "")
            tds.append(f'<td data-f="{_E(fams[fam]["name"])}">'
                       f'{_ext(f["source"], _E(f["surface"]), "tg-t")}{_status(f)}'
                       f'<p>{_code(f["fact"])}</p>{old}{more}</td>')
        rows.append(f'<tr><th scope="row"><b>{_E(_cap(j["name"]))}</b><span>{_E(j["line"])}</span></th>{"".join(tds)}</tr>')
    others = [f for f in d["facts"] if f["family"] == "other"]
    more_rows = "".join(
        f'<tr><th scope="row"><b>{_E(f["surface"])}</b><span>{_E(_cap(f["job"]))}</span></th>'
        f'<td colspan="3">{_ext(f["source"], _E(_host(f["source"])[0]), "tg-t")}{_status(f)}'
        f'<p>{_code(f["fact"])}</p>'
        + (f'<span class="tg-old stale">checked {short_date(f["checked"])}</span>' if is_stale(f) else "")
        + "</td></tr>" for f in others)
    used = page_facts()["tools/"]
    vendor_row = ('<tbody class="tg-src"><tr><th scope="row"><b>Prices, limits and models</b>'
                  '<span>They change every month, so none is printed here</span></th>'
                  + "".join(f'<td data-f="{_E(fams[x]["name"])}">{_ext(fams[x]["pricing"], "Plans and prices")}'
                            f'{_ext(fams[x]["models"], "Models")}</td>' for x in FAMILIES) + "</tr></tbody>")
    table = f"""<section class="tg-map" id="by-job" aria-label="The tools, by job">
<div class="tw" tabindex="0"><table>
<caption class="vh">Seven jobs a team does with AI, down the side, and the tool each of three families offers for it, across. Each cell names the tool, its status in the vendor's own word where it gives one, and links to the vendor's page.</caption>
<colgroup><col class="j"><col><col><col></colgroup>
<thead><tr><th scope="col"><span class="vh">The job</span></th>{"".join(f'<th scope="col">{_E(fams[x]["name"])}</th>' for x in FAMILIES)}</tr></thead>
<tbody>{"".join(rows)}</tbody>
{vendor_row}
<tbody class="tg-more"><tr class="tg-grp"><th scope="rowgroup" colspan="4">Four more names a team meets, beyond the three families</th></tr>{more_rows}</tbody>
</table></div>
<div class="tg-key"><p>The tag is the vendor's own word for how finished a thing is, and it changes what you can promise a team. No tag means the vendor's page gave none.</p>
<p>A tool's name links to the vendor's own page, the one its fact was checked against. The number beside a fact in a manual leads to the same page and its date.</p></div>
</section>"""
    tiles = "".join(
        f'<a class="tile" href="{m["slug"]}/"><span class="tile-k">5 moves · {len(m["facts"])} dated facts</span>'
        f'<b>{_E(m["name"])}</b><span class="tile-d">{_E(m["card"])}</span>'
        f'<span class="tile-go" aria-hidden="true">→</span></a>' for m in MANUALS)
    counts = "".join(f"<span>{c}</span>" for c in (
        f"{len(d['jobs'])} jobs", f"{len(FAMILIES)} families of tools", f"{len(used)} dated facts",
        f"{len(MANUALS)} manuals")) + _checked(used)
    orient = k.orient(
        "Anyone about to hand a job to an AI tool, and anyone asked which one the team should use.",
        "Find the tool each vendor offers for a job, see how finished it is, and open the vendor's own page.",
        ["Find the <b>job</b> down the side: drafting, holding the case, testing a prompt, building, handing off, "
         "browsing or a scheduled check.",
         "Read across. Each cell names the tool, its status tag and one fact, and links to the page the fact came from.",
         "For the tools in a manual, the cell links to it: five moves with the real prompt, three settings and the traps."])
    tour = k.tour([
        {"sel": ".tg-map", "title": "Jobs down the side, vendors across",
         "body": "Seven jobs a team does with AI. Each cell names the tool that vendor offers for it, with its status and one dated fact."},
        {"sel": ".tg-map td .tg-t", "title": "Every fact has a source",
         "body": "The tool's name links to the vendor's own page, the one the fact was checked against."},
        {"sel": ".tg-shelf .shelf", "title": "The manuals",
         "body": "Five moves at the airline, each with the real prompt, then the settings, the traps and every fact with its date."},
    ])
    body = f"""<div class="wrap"><main id="main" class="page tg">
<header class="phead"><p class="eyebrow">Tool guides</p>
  <h1>Which AI tool does each job?</h1>
  <p class="lede">Seven jobs a team does with AI, and the tool each vendor offers for it.</p>
  <p class="pmeta">{counts}</p>
</header>
{orient}
{table}
<section class="tg-shelf" id="manuals" aria-labelledby="manuals-h">
  <div class="tg-sh"><h2 id="manuals-h">Two manuals put Claude in the airline team's hands</h2>
    <p>Each one is five moves with the real prompt or command, the three settings that matter, its traps, and every fact
    it used with its source and date.</p></div>
  <div class="shelf">{tiles}</div>
  <p class="tg-soon">{_E(NEXT_UP)}</p>
</section>
{render.next_up("Start where the spec gets written, at the desk.", MANUALS[0]["slug"] + "/", "Claude at the desk",
                ("../labs/grow-the-spec/", "Or grow the spec in the lab"))}
</main></div>"""
    return shell(title="Tool guides: which AI tool does each job · The agentic manual",
                 desc="Seven jobs a team does with AI, and the tool Claude, ChatGPT and Codex, and Google each offer for it, "
                      "with its status and a dated fact linked to the vendor's own page.",
                 body=body, depth=1, nav_id="tools", canonical=f'{ctx["base"]}tools/',
                 crumbs=[("Libraries", ""), ("Tool guides", "")], tour=tour, kind="tools", og="home")


def _rail() -> str:
    items = "".join(f'<li><a class="rl" data-for="{i}" href="#{i}"><span class="rn">{n}</span><span>{_E(t)}</span></a></li>'
                    for n, (i, t) in enumerate(SECTIONS, 1))
    return f'<aside class="rail wideonly" aria-label="Sections of this page"><p class="railh">On this page</p><ol>{items}</ol></aside>'


def _contents() -> str:
    items = "".join(f'<li><a href="#{i}">{_E(t)}</a></li>' for i, t in SECTIONS)
    return f'<details class="howto narrowonly"><summary>On this page</summary><ol class="hlist">{items}</ol></details>'


def manual_page(m: dict, shell, ctx: dict) -> str:
    import render
    d = load()
    marks = _Marks(d["by_id"])
    lab = _lab_prompts()

    def sec(sid: str, h2: str, inner: str) -> str:
        return f'<section class="sec" id="{sid}"><h2>{marks.inline(h2)}</h2>{inner}</section>'

    what = sec("what", m["what"]["h2"], f'<p class="tg-what">{marks.inline(m["what"]["body"])}</p>')
    not_ = sec("not", m["not"]["h2"], '<ul class="tg-list">' + "".join(f"<li>{marks.inline(t)}</li>" for t in m["not"]["items"]) + "</ul>")
    moves = []
    for n, mv in enumerate(m["moves"]["items"], 1):
        title, body = mv["code"]
        body = lab[body[4:]] if body.startswith("lab:") else body
        hue = PHASE_HUE[mv["phase"]]
        labline = (f'<p class="tg-lab"><a href="{LAB}">{_E(mv["lab"])} <i aria-hidden="true">→</i></a></p>' if mv.get("lab") else "")
        moves.append(
            f'<li class="tg-move" id="move-{n}"><div class="tg-mt">'
            f'<p class="tg-mw"><span class="tg-mn">Move {n}</span><span class="tg-ph" style="--c:var(--dg-{hue})">{mv["phase"]}</span>'
            f'<span>{_E(_cap(mv["who"]))}</span></p>'
            f'<h3>{marks.inline(mv["title"])}</h3><p>{marks.inline(mv["say"])}</p>'
            + (f'<p>{marks.inline(mv["after"])}</p>' if mv.get("after") else "") + labline
            + '</div><div class="tg-mc">' + render.block("prompt", title, "", body, m["slug"] + "-" + str(n)) + "</div></li>")
    moves_html = sec("moves", m["moves"]["h2"], f'<p>{marks.inline(m["moves"]["lead"])}</p><ol class="tg-moves">{"".join(moves)}</ol>')
    poor = sec("poor", m["poor"]["h2"], '<ul class="tg-list">' + "".join(f"<li>{marks.inline(t)}</li>" for t in m["poor"]["items"]) + "</ul>")
    settings = sec("settings", m["settings"]["h2"], '<div class="three tg-set">' + "".join(
        f'<div class="card"><p class="tg-sn">{n}</p><h3>{marks.inline(h)}</h3><p>{marks.inline(t)}</p></div>'
        for n, (h, t) in enumerate(m["settings"]["items"], 1)) + "</div>")
    traps = sec("traps", m["traps"]["h2"], '<ul class="tg-list">' + "".join(f"<li>{marks.inline(t)}</li>" for t in m["traps"]["items"]) + "</ul>")
    facts = [d["by_id"][i] for i in marks.order]
    frows = []
    for n, f in enumerate(facts, 1):
        host, tail = _host(f["source"])
        frows.append(
            f'<tr id="f-{f["id"]}"><td class="n">{n}</td><td>{_code(f["fact"])}{_status(f)}</td>'
            f'<td class="s">{_ext(f["source"], f"<b>{_E(host)}</b>" + (f"<span>/{_E(tail)}</span>" if tail else ""))}'
            f'<time class="{"stale" if is_stale(f) else ""}" datetime="{f["checked"]}">checked {short_date(f["checked"])}</time></td></tr>')
    fam = next(x for x in d["families"] if x["id"] == "claude")
    prices, models = _ext(fam["pricing"], "Claude's plans and prices"), _ext(fam["models"], "the models overview")
    facts_html = (f'<section class="sec" id="facts"><h2>Where every fact on this page comes from</h2>'
                  f'<p>Each numbered mark above points to a row here: the fact, the vendor\'s page it was checked against, and '
                  f'the date. A date turns amber once it is more than {STALE_DAYS} days old. Prices, usage limits and model '
                  f'names change too often to print: read them on {prices} and {models}.</p>'
                  f'<div class="tw tg-facts" tabindex="0"><table><caption class="vh">Every fact this page uses, with its source and the date it was checked</caption>'
                  f'<thead><tr><th scope="col">No.</th><th scope="col">The fact</th><th scope="col">Source, and when it was checked</th></tr></thead>'
                  f'<tbody>{"".join(frows)}</tbody></table></div></section>')
    counts = "".join(f"<span>{c}</span>" for c in (
        f"{len(m['moves']['items'])} moves", f"{len(m['settings']['items'])} settings", f"{len(m['traps']['items'])} traps",
        f"{len(facts)} dated facts")) + _checked(facts)
    nx = m["next"]
    body = f"""<div class="cols two-col">{_rail()}<main id="main" class="numbered tg tg-man">
<header class="phead in-col"><p class="kicker">{_E(m["kicker"])}</p>
  <h1>{_E(m["h1"])}</h1>
  <p class="lede">{marks.inline(m["lede"])}</p>
  <p class="pmeta">{counts}</p>
</header>
{_contents()}
{what}{not_}{moves_html}{poor}{settings}{traps}{facts_html}
{render.next_up(nx[0], nx[1], nx[2], ("../", "All the tool guides") if nx[1] != "../" else (LAB, "Grow the spec in the lab"))}
</main></div>"""
    return shell(title=f'{m["name"]}: a tool guide · The agentic manual',
                 desc=f'{m["lede"]} Five moves at a fictional airline with the real prompt, three settings, the traps, '
                      f'and every fact with its source and date.',
                 body=body, depth=2, nav_id="tools", canonical=f'{ctx["base"]}tools/{m["slug"]}/',
                 crumbs=[("Libraries", ""), ("Tool guides", "../"), (m["name"], "")], kind="tools", og="home",
                 ctx={"lesson": (LAB, "The lab")})


def words(m: dict) -> dict[str, int]:
    """How long a manual reads: its prose, with each fact's sentence in place, and its prompts."""
    d = load()
    prose = " ".join(MARK.sub(lambda x: d["by_id"][x.group(1)]["fact"] if x.group(1) else "", t) for t in _texts(m))
    prose = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", prose)
    return {"prose": len(prose.split()), "prompts": sum(len(c.split()) for c in _codes(m))}


def search_rows() -> list[dict]:
    rows = [{"t": "Tool guides: which AI tool does each job", "u": "tools/", "k": "Library",
             "d": "Seven jobs a team does with AI, and the tool Claude, ChatGPT and Codex, and Google each offer for it, with dated facts."}]
    rows += [{"t": f'{m["name"]}: a tool guide', "d": m["card"], "u": f'tools/{m["slug"]}/', "k": "Tool guide"} for m in MANUALS]
    return rows


def render(put, shell, ctx: dict) -> None:
    d = load()
    errors = check(d)
    if errors:
        raise SystemExit("tools: " + "\n  tools: ".join([""] + errors))
    for w in warnings():
        print("  tools: warning:", w)
    put("tools/index.html", index_page(shell, ctx))
    for m in MANUALS:
        put(f'tools/{m["slug"]}/index.html', manual_page(m, shell, ctx))


def urls(base: str) -> list[str]:
    return [f"{base}tools/"] + [f'{base}tools/{m["slug"]}/' for m in MANUALS]
