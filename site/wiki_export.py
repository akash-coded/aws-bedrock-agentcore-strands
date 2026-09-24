#!/usr/bin/env python3
"""Export each role journey to a wiki page, from the same JSON the site renders.

The site and the wiki say the same thing because they are generated from one source. The wiki page
is the reading copy: no collapsing, no copy buttons, everything on the page, so it can be read in a
browser tab, printed, or pasted into a document.

    python site/wiki_export.py          # writes ../wiki/Journey-<Role>.md

Existing hand-written ``Role-*.md`` pages are left alone. They are the standing definition of each
job — what it is accountable for, what it may settle alone, what crosses its desk and how it fails.
These are the day-to-day walk. Each links to the other, and neither repeats the other.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "pages"))

SITE = Path(__file__).resolve().parent
CONTENT = SITE / "content" / "roles"
WIKI = SITE.parent / "wiki"
LIVE = "https://akash-coded.github.io/aws-bedrock-agentcore-strands/"

# role id -> (wiki page for the day-to-day journey, wiki page for the standing definition)
PAGES = {
    "product-manager": ("Journey-Product-Manager", "Role-Product-Manager"),
    "solution-architect": ("Journey-Solution-Architect", "Role-Solution-Architect"),
    "engineering": ("Journey-Engineering-Lead", "Role-Engineering-Lead"),
    "qa": ("Journey-QA-Lead", "Role-QA-Lead"),
    "devops": ("Journey-DevOps", "Role-DevOps"),
}


def live(href: str) -> str:
    """A site-relative href as a live URL. A role page sits one level below the root, so ``../x`` is ``x``."""
    return LIVE + re.sub(r"^(\.\./)+", "", href)


def unmd(s: str) -> str:
    """Site markdown-lite is already markdown; only relative hrefs need absolutising. A role page sits
    one level below the site root, so a ``../x`` from it is ``x`` at the root."""
    return re.sub(r"\]\((?!https?:|#)([^)]+)\)", lambda m: f"]({live(re.sub(r'^(\.\./)+', '', m.group(1)))})", s)


def fence(body: str, lang: str) -> str:
    lang = {"markdown": "markdown", "md": "markdown"}.get(lang, lang or "text")
    ticks = "````" if "```" in body else "```"
    return f"{ticks}{lang}\n{body.rstrip()}\n{ticks}"


# The phase names and the question each answers are canonical on the wiki's
# The-Agentic-PDLC page; the step-to-phase join lives in the content source, so this is
# a label table and nothing more.
PHASE_NAME = {"P0": "P0 · Frame", "P1": "P1 · Design & Spec",
              "P2": "P2 · Build & Prove", "P3": "P3 · Run & Learn"}
PHASE_ASKS = {
    "P0": "is this worth doing, is it AI at all, and how much may the machine do?",
    "P1": "what exactly is being built, and under whose authority?",
    "P2": "does it meet the bar, slice by slice?",
    "P3": "is it still doing what we launched, and what did it cost?",
}
# GitHub draws the wiki in the reader's colour mode, so each hue must clear 3:1 on white and on
# near-black; these are the lifted values site/content/learn/README.md lists.
PHASE_HUE = {"P0": "#516981", "P1": "#4B5CC8", "P2": "#0E7F7C", "P3": "#9C6803"}
ORDER = ("P0", "P1", "P2", "P3")


def by_phase(role: dict) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {ph: [] for ph in ORDER}
    for s in role["steps"]:
        out[s["pdlc"]].append(s)
    return out


def _wrap(text: str, width: int = 26) -> str:
    """Break a label at word boundaries before mermaid does: it wraps any line over ~200px itself."""
    lines, cur = [], ""
    for word in text.split():
        seen = len(re.sub(r"<[^>]+>", "", f"{cur} {word}".strip()))
        if cur and seen > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return "<br/>".join(lines + [cur])


def arc_diagram(role: dict) -> str:
    """The role's eight steps, grouped into the four phases they actually belong to.

    The arc table says what each step produces. This says where each step sits on the
    spine — which is the thing a reader cannot get from a numbered list, and the reason
    the hard gate lands in a different place for each role.
    """
    groups = by_phase(role)
    # Phases stack as bands, two steps to a row, so the drawing stays narrow enough for a phone; the
    # step numbers carry the order. Invisible ~~~ links count in linkStyle numbering, so count them.
    L, classes, links = ["```mermaid", "flowchart TB"], {ph: [] for ph in ORDER}, 0
    absent = []
    for ph in ORDER:
        L += [f'  subgraph {ph}["{PHASE_NAME[ph]}"]', "    direction LR"]
        steps = groups[ph]
        if steps:
            ids = []
            for st in steps:
                nid = f"S{st['n']}"
                ids.append(nid)
                classes[ph].append(nid)
            label = {f"S{st['n']}": f'{st["n"]} · {st["phase"]}' for st in steps}
            for k in range(0, len(ids), 2):
                row = ids[k:k + 2]
                L.append("    " + " ~~~ ".join(f'{n}["{label[n]}"]' for n in row))
                links += len(row) - 1
        else:
            nid = f"{ph}X"
            absent.append(nid)
            L.append(f'    {nid}["{_wrap(role["pdlc_absent"][ph])}"]')
        L.append("  end")

    L += ["  P0 --> P1", '  P1 -->|"HARD GATE"| P2', "  P2 --> P3"]
    for ph in ORDER:
        hue = PHASE_HUE[ph]
        L.append(f"  classDef {ph.lower()} fill:{hue}1A,stroke:{hue},stroke-width:1.5px")
        if classes[ph]:
            L.append(f"  class {','.join(classes[ph])} {ph.lower()}")
        L.append(f"  style {ph} fill:{hue}0D,stroke:{hue},stroke-width:1.5px")
    if absent:
        # no color: — no fixed grey clears 4.5:1 for text in both modes; the dash carries "absent"
        L.append("  classDef absent fill:none,stroke:#8A8A8A,stroke-width:1.2px,stroke-dasharray:4 3")
        L.append(f"  class {','.join(absent)} absent")
    # the three phase links follow every invisible one, so the gate is the second of them
    L.append(f"  linkStyle {links + 1} stroke:{PHASE_HUE['P2']},stroke-width:3px")
    L.append("```")
    return "\n".join(L)


def page(role: dict) -> str:
    slug, role_page = PAGES[role["id"]]
    live_url = f"{live(role['id'])}/"
    n_p = sum(len(s["prompts"]) for s in role["steps"])
    n_a = sum(len(s["activities"]) for s in role["steps"])

    L = [f"# {role['name']} · the journey, end to end", "",
         f"**{unmd(role['tagline'])}**", "",
         f"{len(role['steps'])} steps · {n_a} sub-steps · {len(role['steps'])} templates · {n_p} prompts",
         "",
         f"This is the reading copy. The [interactive version]({live_url}) has a copy button on every "
         f"template and prompt, which is what you want when you are actually doing the work."]
    if role_page:
        L += ["", f"This page is the walk. For the standing definition of the job — what you own, "
                  f"what you may settle alone, what crosses your desk and how the role fails — see "
                  f"[{role_page.replace('-', ' ')}]({role_page})."]
    L += ["", "---", ""]
    for para in role["intro"]:
        L += [unmd(para), ""]
    import wiki_pictures
    L += ["## The arc", "",
          "Eight steps, and the four phases they sit in. Where the hard gate falls on your own "
          "arc is the thing worth noticing: it is a different place for every role.", "",
          wiki_pictures.picture(wiki_pictures.JOURNEYS[role["id"]]), "",
          "| # | Phase | Step | What it produces |", "| --- | --- | --- | --- |"]
    groups = by_phase(role)
    for ph in ORDER:
        if not groups[ph]:
            L.append(f"| — | {ph} | *{role['pdlc_absent'][ph]}* | — |")
            continue
        for s in groups[ph]:
            L.append(f"| {s['n']} | {ph} | [**{s['phase']}** — {unmd(s['title'])}](#{s['n']}--"
                     f"{re.sub(r'[^a-z0-9]+', '-', s['phase'].lower()).strip('-')}) | "
                     f"{unmd(s['artifact']['name'])} |")

    L += ["", "## What is yours, and what is not", "",
          "| Yours to own | Not yours — stop signing these |", "| --- | --- |"]
    owns, nots = role["owns"], role["not_yours"]
    for i in range(max(len(owns), len(nots))):
        a = unmd(owns[i]) if i < len(owns) else ""
        b = unmd(nots[i]) if i < len(nots) else ""
        L.append(f"| {a} | {b} |")

    L += ["", "## How to use a model in this role", "", f"> {unmd(role['ai_stance'])}", "", "---", ""]

    seen: set[str] = set()
    gated = False
    has = {st["pdlc"] for st in role["steps"]}
    for s in role["steps"]:
        if s["pdlc"] not in seen:
            seen.add(s["pdlc"])
            L += [f"> **{PHASE_NAME[s['pdlc']]} begins here** — *{PHASE_ASKS[s['pdlc']]}*", ""]
            # The gate belongs where this role's walk LEAVES P1, which is not always at a
            # P2 step: the architect has no P2 step at all and still signs it.
            if "P1" in has and ORDER.index(s["pdlc"]) > ORDER.index("P1") and not gated:
                gated = True
                L += ["> ⛔ **The hard gate — P1 to P2.** Everything past this point depends on "
                      "the spec, the acceptance bar per slice and the authority budget being "
                      "signed. It is the one crossing nothing downstream survives without — "
                      "[why](The-Agentic-PDLC).", ""]
        L += [f"## {s['n']} · {s['phase']}", "",
              f"### {unmd(s['title'])}", "",
              f"*{unmd(s['when'])}*", "",
              unmd(s["purpose"]), "",
              "**What you actually do**", ""]
        for i, a in enumerate(s["activities"], 1):
            L.append(f"{i}. **{unmd(a['do'])}** — {unmd(a['detail'])}")
        L += ["", "**Where a model helps, and where it must not**", "",
              "| Tool | Use it for |", "| --- | --- |"]
        for a in s["ai"]:
            cell = unmd(a["use"])
            if a.get("caution"):
                cell += f"<br>⚠ {unmd(a['caution'])}"
            L.append(f"| **{unmd(a['tool'])}** | {cell} |")
        L += ["", "**The artefact**", "",
              f"| | |", "| --- | --- |",
              f"| Produces | **{unmd(s['artifact']['name'])}** |",
              f"| Good looks like | {unmd(s['artifact']['good'])} |",
              f"| Owner | {unmd(s['artifact']['owner'])} |",
              "", f"<details><summary><b>Template · {s['template']['title']}</b></summary>", "",
              fence(s["template"]["body"], s["template"].get("lang", "markdown")), "", "</details>", ""]
        for p in s["prompts"]:
            L += [f"<details><summary><b>Prompt · {p['title']}</b> — {unmd(p['when'])}</summary>", "",
                  fence(p["body"], "text"), "", "</details>", ""]
        L += [f"**Worked example · {unmd(s['example']['title'])}**", "",
              f"> {unmd(s['example']['body'])}", "", "**Pitfalls**", ""]
        L += [f"- {unmd(p)}" for p in s["pitfalls"]]
        L += ["", f"**Done when** — {unmd(s['done_when'])}", "", "---", ""]

    L += ["## Read next", ""]
    L += [f"- [{l}]({h if h.startswith('http') else live(h)})" for l, h in role["reads"]]
    others = [f"[{PAGES[r][0].replace('-', ' ').replace('Journey ', '')}]({PAGES[r][0]})"
              for r in PAGES if r != role["id"] and (CONTENT / f"{r}.json").exists()]
    if others:
        L += ["", "**Other roles:** " + " · ".join(others)]
    L += ["", f"- [The manual, interactive]({LIVE}) · [every template]({LIVE}templates/) · "
              f"[every prompt]({LIVE}prompts/) · [frameworks and acronyms]({LIVE}frameworks/)", ""]
    return "\n".join(L)


def main() -> int:
    written = []
    for rid, (slug, _m) in PAGES.items():
        src = CONTENT / f"{rid}.json"
        if not src.exists():
            continue
        role = json.loads(src.read_text(encoding="utf-8"))
        out = WIKI / f"{slug}.md"
        out.write_text(page(role) + "\n", encoding="utf-8")
        written.append(f"  {out.name} ({out.stat().st_size:,} bytes)")
    print("\n".join(["wiki pages written:"] + written) if written else "no role JSON found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
