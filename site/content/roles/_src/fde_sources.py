"""The forward-deployed engineer guide's sources, as dated records, and the rules its own words keep.

Postings change in weeks, so the guide never types a claim about the profession. It names a record here.

- ``SOURCES``: the 29 sources of council 10's FDE paper, section 6, S1 to S28 with S6b, and S26b, the
  discovery page the paper's S26 named beside the alpha page. For each: who published it, its title, its
  address, how it was read and the date it was checked.
- ``QUOTES``: one record per quotation the paper shows, each with its source and its exact words, copied
  from the paper. A quotation with a long dash is cut shorter, never altered.

In the guide's words a quotation is a mark, never typed text. These are the Tool guides' marks:

    {{S24-ground}}   the quotation's words, in quotation marks, then its source's numbered mark
    [[S12]]          a source's mark alone, after a sentence that leans on it

``house()`` holds the guide's own words to the house rules of ``pages/tools.py``: no model name, no banned
word, no American spelling, no long dash. A quotation is exempt from those rules, because it is held to its
record instead. A mark that names no record fails. So does a quotation typed between quotation marks.
``build_content.py`` runs it over the role's HEAD and steps (fde_a.py, fde_b.py, fde_c.py), and
``fde_hub.check()`` runs it over the hub's words.

``cite()``, ``quote()``, ``Marks`` and ``plain()`` render the records, for pages/fde.py. A record checked
more than sixty days ago shows its date in amber, by the Tool guides' rule and clock (``STALE_DAYS``, and
``TOOLS_TODAY=2026-12-15`` to pretend it is that day). Every record below was checked on 2 October 2026, so
re-check them by 1 December 2026: open the address, compare the words, and change the date.
"""
from __future__ import annotations

import re
from datetime import date
from html import escape as _E

# The sources, in the paper's order. "read" is how the words were read: some careers pages draw their text
# with script, so the text came from the same job's record in the employer's public posting feed.
SOURCES = {
    "S1": {"company": "OpenAI", "title": "Forward Deployed Engineer (FDE), San Francisco",
           "url": "https://jobs.ashbyhq.com/openai/967f94aa-1706-4dba-ac89-bfbc2c38b688",
           "read": "WebFetch (title); text from OpenAI's Ashby feed, api.ashbyhq.com/posting-api/job-board/openai",
           "checked": "2026-10-02"},
    "S2": {"company": "OpenAI", "title": "Deployment Lead (DL), FDE, Tokyo",
           "url": "https://jobs.ashbyhq.com/openai/df514733-46ad-4777-be67-44667bc9fd45",
           "read": "WebFetch (title); text from OpenAI's Ashby feed, api.ashbyhq.com/posting-api/job-board/openai",
           "checked": "2026-10-02"},
    "S3": {"company": "OpenAI", "title": "Forward Deployed Software Engineer, San Francisco",
           "url": "https://jobs.ashbyhq.com/openai/00207abc-49b7-465c-a219-f7c1140f8047",
           "read": "WebFetch (title); text from OpenAI's Ashby feed, api.ashbyhq.com/posting-api/job-board/openai",
           "checked": "2026-10-02"},
    "S4": {"company": "OpenAI", "title": "Platform Engineering Manager, Forward Deployed Engineering",
           "url": "https://jobs.ashbyhq.com/openai/b073abb1-cf6c-4fd9-a318-732fdd2f1408",
           "read": "WebFetch (title); text from OpenAI's Ashby feed, api.ashbyhq.com/posting-api/job-board/openai",
           "checked": "2026-10-02"},
    "S5": {"company": "OpenAI", "title": "Manager, Forward Deployed Engineering, New York",
           "url": "https://jobs.ashbyhq.com/openai/5bbc43df-558a-4e4b-a0cf-83f185c664d7",
           "read": "WebFetch (title); text from OpenAI's Ashby feed, api.ashbyhq.com/posting-api/job-board/openai",
           "checked": "2026-10-02"},
    "S6": {"company": "Anthropic", "title": "Forward Deployed Engineer, London",
           "url": "https://job-boards.greenhouse.io/anthropic/jobs/5423029008",
           "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S6b": {"company": "Anthropic", "title": "Forward Deployed Engineer, Paris",
            "url": "https://job-boards.greenhouse.io/anthropic/jobs/5391021008",
            "read": "WebFetch, the experience line", "checked": "2026-10-02",
            "note": "The posting the lessons cite"},
    "S7": {"company": "Anthropic", "title": "Technical Deployment Lead",
           "url": "https://job-boards.greenhouse.io/anthropic/jobs/5017903008",
           "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S8": {"company": "Anthropic", "title": "Pre-Sales Program Lead, Forward Deployed Engineering",
           "url": "https://job-boards.greenhouse.io/anthropic/jobs/5391012008",
           "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S9": {"company": "Anthropic", "title": "Manager, Forward Deployed Engineering, New York",
           "url": "https://job-boards.greenhouse.io/anthropic/jobs/5099753008",
           "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S10": {"company": "Anthropic", "title": "Associate Applied AI, Rotational Program, London",
            "url": "https://job-boards.greenhouse.io/anthropic/jobs/5425724008",
            "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S11": {"company": "Palantir", "title": "Forward Deployed Software Engineer (Delta), New York",
            "url": "https://jobs.lever.co/palantir/dab396d4-2f14-4796-aac0-0d82883dccf0",
            "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S12": {"company": "Palantir", "title": "Deployment Strategist (Echo), New York",
            "url": "https://jobs.lever.co/palantir/e0ab8226-b928-4e3a-bf87-08fe7b1ea595",
            "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S13": {"company": "Palantir", "title": "Forward Deployed AI Engineer (Delta), New York",
            "url": "https://jobs.lever.co/palantir/636fc05c-d348-4a06-be51-597cb9e07488",
            "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S14": {"company": "Palantir", "title": "AIP Bootcamp",
            "url": "https://www.palantir.com/platforms/aip/bootcamp/",
            "read": "WebFetch (title); text from the page's own HTML", "checked": "2026-10-02"},
    "S15": {"company": "Databricks", "title": "Deployment Strategist",
            "url": "https://databricks.com/company/careers/open-positions/job?gh_jid=8463063002",
            "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S16": {"company": "Databricks", "title": "AI Engineer, Forward Deployed Engineering (AI FDE)",
            "url": "https://databricks.com/company/careers/open-positions/job?gh_jid=8546367002",
            "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S17": {"company": "Ramp", "title": "Software Engineer, Forward Deployed AI Solutions",
            "url": "https://jobs.ashbyhq.com/ramp/b614563f-3ce6-4dca-b5ba-0e5a6c8bda27",
            "read": "WebFetch (title); text from Ramp's Ashby feed", "checked": "2026-10-02"},
    "S18": {"company": "Ramp", "title": "Forward Deployed Engineering",
            "url": "https://engineering.ramp.com/post/forward-deployed-engineering",
            "read": "WebFetch, quoted sentences checked", "checked": "2026-10-02",
            "note": "Ramp Builders, undated"},
    "S19": {"company": "Scale AI", "title": "Forward Deployed Product Manager, Enterprise",
            "url": "https://job-boards.greenhouse.io/scaleai/jobs/4673051005",
            "read": "WebFetch, full text", "checked": "2026-10-02"},
    "S20": {"company": "AWS", "title": "AWS invests $1 billion to embed AI forward deployed engineers with customers",
            "url": "https://www.aboutamazon.com/news/aws/aws-1-billion-forward-deployed-ai-engineers",
            "read": "WebFetch", "checked": "2026-10-02", "author": "Francessca Vasquez"},
    "S21": {"company": "AWS", "title": "Sr Forward Deployed Engineer, AWS Forward Deployed Engineering",
            "url": "https://www.amazon.jobs/en/jobs/10517491/sr-forward-deployed-engineer-aws-forward-deployed-engineering",
            "read": "WebFetch", "checked": "2026-10-02"},
    "S22": {"company": "Anthropic",
            "title": "DXC will integrate Claude into the systems banks, airlines, and other regulated industries rely on",
            "url": "https://www.anthropic.com/news/dxc-anthropic-alliance",
            "read": "WebFetch", "checked": "2026-10-02", "published": "2026-06-11"},
    "S23": {"company": "SVPG", "title": "Forward Deployed Engineers",
            "url": "https://www.svpg.com/forward-deployed-engineers/",
            "read": "WebFetch", "checked": "2026-10-02", "author": "Marty Cagan", "published": "2025-09-17"},
    "S24": {"company": "The Pragmatic Engineer",
            "title": "What are Forward Deployed Engineers, and why are they so in demand?",
            "url": "https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers",
            "read": "WebFetch (part paywalled)", "checked": "2026-10-02", "author": "Gergely Orosz",
            "published": "2025-08-12", "note": "Quoting OpenAI's head of FDE, Colin Jarvis"},
    "S25": {"company": "Anthropic", "title": "Building effective agents",
            "url": "https://www.anthropic.com/engineering/building-effective-agents",
            "read": "WebFetch", "checked": "2026-10-02", "author": "Erik S. and Barry Zhang",
            "published": "2024-12-19"},
    # The paper's S26 named three pages of the Service Manual under one address. The guide cites two of them,
    # so each has its own record: S26, the alpha page, holds both quotations; S26b, the discovery page, holds
    # the sentence step 1 leans on (stopping at the end of discovery is not a failure).
    "S26": {"company": "GOV.UK", "title": "Service Manual: how the alpha phase works (updated 8 May 2019)",
            "url": "https://www.gov.uk/service-manual/agile-delivery/how-the-alpha-phase-works",
            "read": "WebFetch; both quotations checked again on 3 October 2026 against the saved page",
            "checked": "2026-10-02"},
    "S26b": {"company": "GOV.UK", "title": "Service Manual: how the discovery phase works (updated 21 June 2021)",
             "url": "https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works",
             "read": "WebFetch, the sentence on stopping at the end of discovery", "checked": "2026-10-03"},
    "S27": {"company": "The agentic manual", "title": "Tool guides",
            "url": "https://akash-coded.github.io/aws-bedrock-agentcore-strands/tools/",
            "read": "Read from the repository, site/content/tools/tools.json; each fact carries its own source and date",
            "checked": "2026-10-02"},
    "S28": {"company": "Glean", "title": "Founding Forward Deployed Engineer, New York",
            "url": "https://job-boards.greenhouse.io/gleanwork/jobs/4659412005",
            "read": "WebFetch, quoted sentence", "checked": "2026-10-02"},
}

# One record per quotation in the paper, word for word. The id is the source's, a hyphen and a short slug.
QUOTES = {
    # OpenAI
    "S1-own": {"source": "S1", "words": "You will own discovery, technical scoping, system design, build, and production rollout"},
    "S1-delivery": {"source": "S1", "words": "own technical delivery across multiple deployments from first prototype to stable production"},
    "S1-feedback": {"source": "S1", "words": "eval-driven feedback that changes product and model roadmaps"},
    "S1-codify": {"source": "S1", "words": "codify working patterns into tools, playbooks, or building blocks that others can use"},
    "S1-experience": {"source": "S1", "words": "5+ years of engineering or technical deployment experience that includes customer-facing work"},
    "S2-prototypes": {"source": "S2", "words": "drive 0→1 prototypes through MVP and scale"},
    "S2-measurement": {"source": "S2", "words": "run pre-/post-deployment measurement and report to exec sponsors"},
    "S2-experience": {"source": "S2", "words": "7+ years of customer-facing technical delivery leadership"},
    "S3-scopes": {"source": "S3", "words": "prepare detailed scopes of work and project plans for both proof-of-concept prototypes and full production deployments"},
    "S3-abstractions": {"source": "S3", "words": "design abstractions to solve customer problems, and then use them to scale our speed and quality of delivery across all Forward Deployed engagements"},
    "S4-handoff": {"source": "S4", "words": "ready for handoff"},
    "S5-codify": {"source": "S5", "words": "codify what works into tools, playbooks, and roadmap inputs"},
    # Anthropic
    "S6-codify": {"source": "S6", "words": "Identify and codify repeatable deployment patterns and contribute insights back to our Product and Engineering teams"},
    "S6-relationships": {"source": "S6", "words": "build long term relationships with customers and proactively identify new opportunities"},
    "S6-experience": {"source": "S6", "words": "4+ years"},
    "S6b-experience": {"source": "S6b", "words": "8+"},
    "S7-owns": {"source": "S7", "words": "product scoping, stakeholder management, value measurement"},
    "S7-build": {"source": "S7", "words": "build the technical solution"},
    "S7-scope": {"source": "S7", "words": "clear scope, milestones, dependencies, success criteria, and value hypotheses"},
    "S8-contract": {"source": "S8", "words": "from opportunity to a signed contract"},
    "S8-counterpart": {"source": "S8", "words": "a Post-Sale Program Lead counterpart who owns delivery from signature onward"},
    "S9-qualify": {"source": "S9", "words": "qualify engagements, scope work, and inform statements of work"},
    "S9-playbooks": {"source": "S9", "words": "repeatable playbooks, starter repositories, integration templates"},
    "S10-experience": {"source": "S10", "words": "0-2 years of software engineering, technical consulting, or solutions architecture experience"},
    # Palantir
    "S11-experience": {"source": "S11", "words": "1+ years of relevant, post-college work experience"},
    "S12-internal": {"source": "S12", "words": "may also be deployed to Palantir internal teams and problems"},
    "S13-cto": {"source": "S13", "words": "Forward Deployed AI Engineers' responsibilities look similar to those of a hands-on AI startup CTO"},
    "S14-use-cases": {"source": "S14", "words": "Develop initial use cases in the software"},
    "S14-five-days": {"source": "S14", "words": "an interactive workshop where customers go from 0 to use case in 5 days"},
    # Databricks
    "S15-embedded": {"source": "S15", "words": "embedded with our most strategic customers from the very first sales call, all the way through to a production-ready solution"},
    "S15-handoff": {"source": "S15", "words": "Strategic Handoff & Growth"},
    "S15-why": {"source": "S15", "words": "the 'product manager' for the customer's problem, responsible for the 'why' and 'what'"},
    "S15-how": {"source": "S15", "words": "responsible for the 'how'"},
    "S15-advisor": {"source": "S15", "words": "trusted advisor status to identify the next high-value FDE engagement"},
    "S16-rollouts": {"source": "S16", "words": "production rollouts of consumer and internally facing GenAI applications"},
    "S16-experts": {"source": "S16", "words": "support internal subject matter expert (SME) teams"},
    # Ramp
    "S17-co-lead": {"source": "S17", "words": "co-lead customer engagements with an AI Solutions Strategist"},
    "S18-lifecycle": {"source": "S18", "words": "through their entire lifecycle: from when they are prospects in the sales funnel, to implementation and rollout, to long-tail support"},
    "S18-pollute": {"source": "S18", "words": "ad-hoc customizations pollute the codebase"},
    "S18-tools": {"source": "S18", "words": "very heavy users of Cursor and Claude Code"},
    "S18-predictor": {"source": "S18", "words": "the single best predictor of real-world performance"},
    "S18-founders": {"source": "S18", "words": "of the 16 FDEs on the team, 7 of us are previous founders"},
    # Scale AI, AWS, DXC
    "S19-difference": {"source": "S19", "words": "can tell the difference between a customer's stated request, their actual problem, and what the platform should do"},
    "S20-operators": {"source": "S20", "words": "from observers to co-builders to autonomous operators"},
    "S20-consulting": {"source": "S20", "words": "assesses, recommends, and treats each deployment as a standalone project"},
    "S20-handover": {"source": "S20", "words": "deployed systems, knowledge graphs, runbooks, architectural documentation, and trained internal champions ready to operate independently"},
    "S21-agentic": {"source": "S21", "words": "experience leading agentic and spec-driven development at production scale"},
    "S22-recruit": {"source": "S22", "words": "DXC will recruit engineers from its existing development teams and certify them"},
    # Practitioners and public guidance
    "S24-ground": {"source": "S24", "words": "doesn't match the data/system reality on the ground"},
    "S25-simplest": {"source": "S25", "words": "finding the simplest solution possible, and only increasing complexity when needed"},
    "S26-complex": {"source": "S26", "words": "just complex enough to let you test different ideas, not production quality code"},
    "S26-throw-away": {"source": "S26", "words": "expect to throw away any code"},
    "S28-pod": {"source": "S28", "words": "in a pod with Forward Deployed PMs"},
}

SOURCE_ID = r"S\d{1,2}b?"
QUOTE_ID = SOURCE_ID + r"-[a-z0-9]+(?:-[a-z0-9]+)*"
MARK = re.compile(r"\{\{(" + QUOTE_ID + r")\}\}|\[\[(" + SOURCE_ID + r")\]\]")
# What is left of a mark that went wrong: doubled brackets, the paper's [S12], or a placeholder like {q:S14}.
_STRAY = re.compile(r"\{\{|\}\}|\[\[|\]\]|\[" + SOURCE_ID + r"\]|\{(?:[a-z]+:)?" + SOURCE_ID + r"[a-z0-9-]*\}")
_TYPED = re.compile("[\"\u201c\u201d\u201e\u00ab\u00bb]")   # a double quotation mark, straight or curly
_LONG_DASH = re.compile("[\u2013\u2014]")


def _tools():
    """pages/tools.py, for the Tool guides' clock, their sixty days and their house rules."""
    import sys
    from pathlib import Path
    site = str(Path(__file__).resolve().parents[3])
    if site not in sys.path:
        sys.path.insert(0, site)
    from pages import tools
    return tools


# --------------------------------------------------------------------------------------------- the words
# The extra words come from the house's list (no filler); "hero" and the game's title come from verdict 2.6:
# the guide never points at the home page's hero, and it calls the game the simulator.
_MORE_BANNED = re.compile(r"\b(holistic\w*|unlock\w*|transformation\w*|empower\w*|in conclusion|key takeaways)\b", re.I)
_HERO = re.compile(r"\bhero(es)?\b", re.I)
_GAME = re.compile(r"\bNinety Days\b")
_BULLET = re.compile(r"^(\s*)[-*+](?=\s)", re.M)


def _near(text: str, m: re.Match) -> str:
    a, b = max(0, m.start() - 28), min(len(text), m.end() + 28)
    return ("..." if a else "") + text[a:b].replace("\n", " ") + ("..." if b < len(text) else "")


def house(where: str, text: str, kind: str = "prose", prices: bool = False) -> list[str]:
    """One piece of the guide's own words against the house rules. An empty list is a pass.

    ``kind`` says how the words are shown. "prose" goes through render.md(), and marks belong there. "plain"
    is a title, a label or a line someone says: no marks. "code" is a prompt or a Markdown template, which a
    reader copies as it stands: no marks, quotation marks allowed, and a hyphen that opens a list line is not
    a dash. "source" is a template in a programming language, where a spaced hyphen is a minus sign: only a
    long dash counts. ``prices`` adds the price check, for words that carry no case (the hub's)."""
    t = _tools()
    bad = []
    copied = kind in ("code", "source")
    marks = MARK.findall(text)
    if marks and kind != "prose":
        what = "a template or a prompt, which is copied as it stands" if copied else "a title or a label"
        bad.append(f"{where}: a mark belongs in prose, and this is {what}")
    for q, s in marks:
        if q and q not in QUOTES:
            near = sorted(k for k in QUOTES if k.split("-")[0] == q.split("-")[0])
            bad.append(f"{where}: no quotation record {q} in fde_sources.py"
                       + (f" (records of {q.split('-')[0]}: {', '.join(near)})" if near else ""))
        if s and s not in SOURCES:
            bad.append(f"{where}: no source {s} in fde_sources.py")
    bare = MARK.sub("", text)     # a quotation is exempt from the house rules: it is held to its record
    if not copied:
        m = _STRAY.search(bare)
        if m:
            bad.append(f"{where}: a mark that is not {{{{quote-id}}}} or [[source-id]] ({_near(bare, m)!r})")
        m = _TYPED.search(bare)
        if m:
            bad.append(f"{where}: a quotation typed between quotation marks ({_near(bare, m)!r}); name its record "
                       f"as {{{{quote-id}}}}, or set a phrase in *italics*")
    words = _BULLET.sub(r"\1", bare) if kind == "code" else bare
    rules = [(t.MODEL_NAMES, "a model name"), (t.BANNED, "a banned word"), (_MORE_BANNED, "a banned word"),
             (re.compile(t.AMERICAN.pattern, re.I), "an American spelling"),
             (_LONG_DASH if kind == "source" else t.DASH, "a dash"),
             (_HERO, "the home page's hero, which the guide never names"),
             (_GAME, "the game's title; the guide calls it the simulator")]
    if prices:
        rules.append((t.PRICE, "a price"))
    for rx, why in rules:
        m = rx.search(words)
        if m:
            bad.append(f"{where}: {why} ({m.group(0)!r} in {_near(words, m)!r})")
    return bad


# ------------------------------------------------------------------------------------------ the records
def check() -> list[str]:
    """The records themselves. An empty list is a pass."""
    t = _tools()
    bad = []
    want = {f"S{i}" for i in range(1, 29)} | {"S6b", "S26b"}
    if set(SOURCES) != want:
        gone, extra = sorted(want - set(SOURCES)), sorted(set(SOURCES) - want)
        bad.append(f"fde_sources: the guide has 30 sources, the paper's S1 to S28 with S6b, and S26b "
                   f"(missing {gone}, unknown {extra})")
    for sid, s in SOURCES.items():
        where = f"fde_sources {sid}"
        for k in ("company", "title", "url", "read", "checked"):
            if not str(s.get(k) or "").strip():
                bad.append(f"{where}: no {k}")
        extra = set(s) - {"company", "title", "url", "read", "checked", "author", "published", "note"}
        if extra:
            bad.append(f"{where}: unknown fields {sorted(extra)}")
        if not str(s.get("url", "")).startswith("https://"):
            bad.append(f"{where}: a source carries the address it was read at")
        for k in ("checked", "published"):
            if k in s:
                try:
                    if date.fromisoformat(s[k]) > t.today():
                        bad.append(f"{where}: {k} on a date that has not happened")
                except (TypeError, ValueError):
                    bad.append(f"{where}: {k} is a date, 2026-10-02")
    for qid, q in QUOTES.items():
        where = f"fde_sources {qid}"
        if not re.fullmatch(QUOTE_ID, qid):
            bad.append(f"{where}: a quotation's id is its source's, a hyphen and a slug in lower case")
        if q.get("source") not in SOURCES:
            bad.append(f"{where}: no source {q.get('source')}")
        elif not qid.startswith(q["source"] + "-"):
            bad.append(f"{where}: the id starts with its source, {q['source']}-")
        if set(q) != {"source", "words"}:
            bad.append(f"{where}: a quotation is its source and its words, nothing else")
        w = q.get("words") or ""
        if not w.strip() or w != w.strip() or "\n" in w:
            bad.append(f"{where}: the words are one line, with no space at either end")
        if _LONG_DASH.search(w):
            bad.append(f"{where}: a long dash; cut the quotation shorter, never alter it")
        if _TYPED.match(w) or _TYPED.search(w[-1:] or " "):
            bad.append(f"{where}: the words without the quotation marks round them; the page adds those")
    return bad


def warnings() -> list[str]:
    """Each source past its sixty days, for the build to print."""
    t = _tools()
    return [f"fde_sources {sid}: checked {t.long_date(s['checked'])}, {t.age(s)} days ago; check it against "
            f"{s['url']} and update its date" for sid, s in SOURCES.items() if t.is_stale(s)]


# ----------------------------------------------------------------------------------------- rendering
def is_stale(sid: str) -> bool:
    return _tools().is_stale(SOURCES[sid])


def host(sid: str) -> str:
    return re.sub(r"^https://(www\.)?", "", SOURCES[sid]["url"]).split("/")[0]


def cite(sid: str) -> str:
    """One source as a page shows it: its company, its title linked to its address, the address's host, and
    the date it was checked, in amber (the class ``stale``) once that is more than sixty days ago."""
    t = _tools()
    s = SOURCES[sid]
    old = t.is_stale(s)
    cls = ' class="stale"' if old else ""
    tip = f' title="Checked more than {t.STALE_DAYS} days ago: the posting may have changed"' if old else ""
    when = f'<time{cls} datetime="{s["checked"]}"{tip}>checked {t.short_date(s["checked"])}</time>'
    return (f'<cite class="fsrc">{_E(s["company"])}, <a href="{_E(s["url"])}" target="_blank" rel="noopener">'
            f'{_E(s["title"])}</a> · <span class="fsrc-h">{_E(host(sid))}</span> · {when}</cite>')


def quote(qid: str) -> str:
    """A quotation's words, in quotation marks."""
    return f"<q>{_E(QUOTES[qid]['words'], quote=False)}</q>"


class Marks:
    """Numbers each source the first time a page names it, as the Tool guides number their facts.

    ``inline()`` takes HTML that render.md() or step_html() has already written and puts each quotation and
    mark in place; ``foot()`` lists the sources in the same order, each with its address and date."""

    def __init__(self) -> None:
        self.order: list[str] = []

    def n(self, sid: str) -> int:
        if sid not in self.order:
            self.order.append(sid)
        return self.order.index(sid) + 1

    def mark(self, sid: str) -> str:
        n = self.n(sid)
        return f'<a class="fn" href="#src-{sid}" aria-label="Source {n}: its address and the date it was checked">{n}</a>'

    def inline(self, html: str) -> str:
        def one(m: re.Match) -> str:
            q, s = m.group(1), m.group(2)
            return quote(q) + self.mark(QUOTES[q]["source"]) if q else self.mark(s)
        return MARK.sub(one, html)

    def foot(self) -> str:
        items = "".join(f'<li id="src-{sid}">{cite(sid)}</li>' for sid in self.order)
        return f'<ol class="fsrcs">{items}</ol>' if items else ""


def plain(text: str) -> str:
    """The words with each quotation in quotation marks and each bare mark dropped: for search rows, llms.txt
    and a page's description."""
    out = MARK.sub(lambda m: f"“{QUOTES[m.group(1)]['words']}”" if m.group(1) else "", text)
    out = re.sub(r"[ \t]{2,}", " ", out)
    return re.sub(r"\s+([.,;:!?])", r"\1", out).strip()
