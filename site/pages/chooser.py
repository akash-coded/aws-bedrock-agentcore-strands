"""The home page's chooser band: which agentic methods should your team use? (verdict-home 1.3)

:func:`band` answers the heading's question on the same screen, in words: the pair every team needs, then three
yes-or-no questions, each adding one method when your work matches it. With nothing chosen both answers to every
question show, so the band is the whole rule for a reader who never touches it, on paper and without script. A
choice only hides the answer that does not apply, in plain CSS (``:has()``): no script, nothing stored, nothing
sent, no score.

The fourth question is the SkyWays PDLC's. Its rule is drawn in the four phase hues, so the lifecycle reads as the
frame round the methods and never as a fifth one. The names and their lessons come from
``content/library/frameworks.json`` through the map's checked loader (pages/spine.py), so the two bands always
name the same things; each rule's words rest on the lesson noted beside it.
"""
from __future__ import annotations

from html import escape as _E

# The pair every team needs, by the method's "name" in frameworks.json, with its one line. The data's "when":
# spec-driven development "Always. It is the backbone", AIDD "Every day, by everyone who writes code". The
# spec-driven lesson's FAQ: "A markdown file in the repository, read by path from the agent's context file, is
# spec-driven development". The AIDD lesson: a context file, a story file per unit of work, review set by risk.
PAIR = [
    ("SDD", "Keep one spec that people review and agents build from. Kiro, Spec Kit or a markdown file will do."),
    ("AIDD", "Give every coding agent a context file, a story file per task, and review by risk."),
]
# Three questions, each adding one method: (the radios' name, the question, the method, its Yes line, its No line).
ASK = [
    # what-is-the-bmad-method.md, "When BMAD pays": across several teams and on audited work "Worth it"; for one
    # team "Optional: Spec-driven development and the gates usually suffice"; "The trail is the evidence an auditor
    # asks for".
    ("q-bmad", "Does the work cross teams, or does an auditor read it?", "BMAD",
     "add its persona trail. Each hand-off is a versioned document, so decisions stay explicit and an auditor can "
     "read them.",
     "leave it out. For one team, spec-driven development and the gates usually suffice."),
    # The data's "when": "When the depth of a change is unknown up front"; what-is-ai-dlc.md: only the stages a change
    # needs, in bolts of hours or days; how-much-process-does-a-change-need.md: four questions about its risk.
    ("q-aidlc", "Is it hard to tell how deep a change goes before you start?", "AI-DLC",
     "add AI-DLC. Run only the stages each change needs, in bolts of hours or days.",
     'size each change yourself, by its risk, with <a href="learn/how-much-process-does-a-change-need/">four '
     'questions</a>.'),
    # The names lesson's FAQ: "Usually two of them ... the agentic PDLC for the product decisions those methods leave
    # open whenever the shipped software calls a model"; what-is-ai-dlc.md: "If your shipped software only runs
    # deterministic code that an agent wrote, AI-DLC may be most of what you need. If it calls a model, you need the
    # rest"; one-lifecycle-for-every-method.md, step 5: hold the phase exits, the hard gate above all.
    ("q-pdlc", "Does the product you ship call a model to rank, draft, decide or act?", "pdlc",
     "put the SkyWays PDLC around it. Decide what the agent may do alone, agree a pass mark for each kind of case, "
     "prove it before real users see it, and report what it saved and what it cost.",
     "a building method is most of what you need. Still sign the spec before anything is built."),
]


def band() -> str:
    """The home page's third band (verdict-home 1.3)."""
    from pages import spine
    d = spine.load()
    by = {m["name"]: m for m in d["methods"]} | {"pdlc": d["pdlc"]}

    def head(key: str) -> str:
        return f'<h3><a href="{by[key]["lesson"]}">{_E(by[key]["title"])}</a></h3>'

    cols = ['<div class="pk-c"><p class="pk-q">Every team that builds with coding agents, every day</p>'
            + "".join(f"{head(k)}<p>{line}</p>" for k, line in PAIR) + "</div>"]
    for name, q, key, yes, no in ASK:
        cols.append(f'<fieldset class="pk-c{" me" if key == "pdlc" else ""}"><legend class="pk-q">{q}</legend>'
                    f'<span class="yn"><label><input type="radio" name="{name}" value="y">Yes</label> '
                    f'<label><input type="radio" name="{name}" value="n">No</label></span>'
                    f'{head(key)}<p class="y"><b>Yes:</b> {yes}</p><p class="n"><b>No:</b> {no}</p></fieldset>')
    body = "\n    ".join(cols)
    return f"""<section class="band" id="choose" aria-labelledby="h-choose"><div class="wrap">
  <header class="sec-h split"><p class="eyebrow">Your team</p>
    <h2 id="h-choose">Which agentic methods should your team use?</h2>
    <p>Every team needs the first pair. Add each of the others when your work matches its question.</p></header>
  <div class="pk">
    {body}
  </div>
  <p class="links"><a class="more" href="learn/how-much-process-does-a-change-need/">How much process a change needs <i aria-hidden="true">→</i></a>
    <a class="more" href="method/">The four phases on one page <i aria-hidden="true">→</i></a></p>
</div></section>"""
