"""Posters: pictures drawn for sharing rather than for a lesson. Each is plain HTML in the ByteByteGo
grammar (one hue per concept, parallel slots, a takeaway strip), so it renders live on a page and is
captured for the picture pack like every other visual.

    prompt_anatomy()     the five parts of a prompt template, with one prompt taken apart
    prompts_by_role()    every role's eight steps with the prompt each step ships with
"""
from __future__ import annotations

import json
from html import escape as E
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
ROLES_DIR = SITE / "content" / "roles"

# Journey order, and the accent each role carries on its own page and on the boards. A role's
# colour is the role's: the phase hues (slate, indigo, teal, amber) are kept for P0 to P3, which is
# what the small phase chip in every cell wears. The forward-deployed engineer is left out on purpose: a staged
# role (pages/fde.py) has twelve steps in three stages, so it would draw a sixth column twelve tall. Its prompts
# are on its own stage pages.
ROLE_HUE = [("product-manager", "slate"), ("solution-architect", "ochre"), ("engineering", "sage"),
            ("qa", "plum"), ("devops", "violet")]

PARTS = [
    ("1", "The job", "You are …", "Who the model is, for whom, and on what. One sentence; the rest of the "
     "prompt inherits it.", "indigo"),
    ("2", "The inputs", "Inputs: …", "What it may use: pasted, attached or named. Nothing outside the list "
     "counts as evidence.", "teal"),
    ("3", "Do", "Do: …", "The verb and its scope. Deduplicate, sort, draft, check: one job, not a "
     "conversation.", "amber"),
    ("4", "The output shape", "Output: …", "A table, a list, a file with named columns: the shape the next "
     "step can consume without editing.", "violet"),
    ("5", "Then, the check", "Then: flag …", "What it must test, mark or refuse before it stops, so that "
     "the output carries its own caveat.", "rose"),
]

EXAMPLE = [
    ("indigo", "You are a product analyst at SkyWays."),
    ("teal", "Inputs: the pasted tickets and transcripts."),
    ("amber", "Do: list every distinct pain, with the exact sentence that evidences it and how many times it appears."),
    ("violet", "Output: a table of pain, evidence, count."),
    ("rose", "Then: flag any pain with fewer than three occurrences as anecdotal."),
]


def _roles() -> list[dict]:
    out = []
    for rid, hue in ROLE_HUE:
        p = ROLES_DIR / f"{rid}.json"
        if p.exists():
            r = json.loads(p.read_text(encoding="utf-8"))
            r["_hue"] = hue
            out.append(r)
    return out


def prompt_anatomy() -> str:
    cards = "".join(
        f'<div class="pa-c" style="--c:var(--dg-{hue})"><span class="pa-n">{n}</span><b>{E(name)}</b>'
        f'<code>{E(cue)}</code><p>{E(what)}</p></div>'
        + ('<i class="pa-arrow" aria-hidden="true"></i>' if n != "5" else "")
        for n, name, cue, what, hue in PARTS)
    ex = "".join(f'<span style="--c:var(--dg-{hue})">{E(line)}</span>' for hue, line in EXAMPLE)
    return (f'<figure class="poster pa" id="poster-prompt-anatomy" aria-label="The anatomy of a prompt template: '
            f'the job, the inputs, do, the output shape, then the check">'
            f'<figcaption><span class="bk">Prompt templates</span><span class="bt">The anatomy of a prompt template</span>'
            f'<span class="bs">Five parts, in this order. A prompt that skips one gets a different answer every time.</span></figcaption>'
            f'<div class="pa-row">{cards}</div>'
            f'<div class="pa-ex"><span class="pa-exl">One prompt, taken apart</span><p>{ex}</p></div>'
            f'<p class="pa-tk"><b>The rule.</b> Say the shape you want, or you get a different shape every time. '
            f'Every template in the library is written this way: replace the angle brackets and keep the five parts.</p>'
            f'</figure>')


def prompts_by_role() -> str:
    """Five roles, eight steps each. Written role by role, so that on a phone each role is its own
    list; on a wide screen base.css lays the same cells out as a grid, one column a role, one row a
    step (``--k`` is the column, ``--r`` the row)."""
    roles = _roles()
    n_prompts = sum(len(s["prompts"]) for r in roles for s in r["steps"])
    n_steps = max(len(r["steps"]) for r in roles) if roles else 8
    nums = "".join(f'<span class="pr-n" style="--r:{i + 2}">{i + 1}</span>' for i in range(n_steps))
    cols = []
    for k, r in enumerate(roles):
        cells = [f'<div class="pr-h"><b>{E(r["name"])}</b>'
                 f'<span>{sum(len(s["prompts"]) for s in r["steps"])} prompts</span></div>']
        for i in range(n_steps):
            s = r["steps"][i] if i < len(r["steps"]) else None
            if not s:
                cells.append(f'<div class="pr-c empty" style="--r:{i + 2}"></div>')
                continue
            first = s["prompts"][0]["title"] if s["prompts"] else "no prompt at this step"
            more = len(s["prompts"]) - 1
            cells.append(f'<div class="pr-c" style="--r:{i + 2}"><span class="pr-s"><i class="pr-i">{i + 1}</i>{E(s["phase"])}'
                         f'<em class="{E(s["pdlc"]).lower()}">{E(s["pdlc"])}</em></span><b>{E(first)}</b>'
                         + (f'<small>+{more} more</small>' if more > 0 else "") + "</div>")
        cols.append(f'<div class="pr-col" style="--c:var(--{r["_hue"]});--k:{k + 2}">{"".join(cells)}</div>')
    return (f'<figure class="poster pr" id="poster-prompts-by-role" aria-label="{n_prompts} prompt templates across '
            f'five roles: for each role, the eight steps in order and the prompt each step ships with">'
            f'<figcaption><span class="bk">Prompt templates</span><span class="bt">{n_prompts} prompt templates, '
            f'five roles, one glance</span><span class="bs">Each role\'s steps in journey order, and the first prompt '
            f'each step ships with. Every one has a copy button on the prompts page.</span></figcaption>'
            f'<div class="pr-grid">{nums}{"".join(cols)}</div>'
            f'<p class="pa-tk"><b>How to read it.</b> One role\'s list is its ninety days. The same step number in '
            f'another role is the same moment seen by that role, which is why the prompts hand each other their '
            f'outputs. The small chip is the phase: P0 to P3.</p>'
            f'</figure>')


POSTERS = {
    "prompt_anatomy": (prompt_anatomy, "The anatomy of a prompt template: the job, the inputs, do, the output "
                       "shape, then the check, with one prompt taken apart", "prompts/"),
    "prompts_by_role": (prompts_by_role, "Every role's eight steps in journey order, with the prompt template "
                        "each step ships with", "prompts/"),
}
