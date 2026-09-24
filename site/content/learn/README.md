# Writing a lesson

The tutorial is written once, here, and published twice: as indexed pages under `/learn/` on the
site (canonical), and as wiki pages (a mirror — GitHub does not let search engines index a wiki
with fewer than 500 stars or open editing). `python3 site/build.py` renders and validates the site
copy; `python3 site/learn_export.py` writes the wiki copy.

The build refuses a lesson that breaks the rules marked **must**. The rest are warnings.

## The map at the top of a lesson

Every lesson opens with a picture drawn in the site's illustration grammar, not a mermaid fence. The
lesson embeds it with `{{map:<slug>}}` on a line of its own (the slug is the lesson's), and the picture
itself is a short spec in [`site/pages/mapspecs.py`](../../pages/mapspecs.py): a title row, then one of
five shapes — `bands` (rows per phase or theme), `flow` (a chain, with an optional gate, terminal or
decision), `pairs` (two panels, row-aligned), `funnel` (a ladder of questions) or `fan` (one question,
its outcomes) — with a callout that says what the picture proves. Change the spec, not the lesson, to
change the picture. The wiki shows a screenshot of it (`python3 site/build.py --shots`, then
`node site/tools/shoot.mjs`). Mermaid still works anywhere else in a lesson.

## Anatomy — every lesson, same slots, same order

Parallel slots are what let a reader skim twelve lessons and know where the answer is in each.

```markdown
---
title:       the H1 and the <title>. The query a practitioner types, made specific. ≤ 60 characters.
short:       the sidebar label. ≤ 34 characters.
wiki:        the wiki page name. Letters, digits, hyphens. Must not collide with a hand-written page.
description: 120–160 characters. Contains the main term and promises the payoff.
dek:         one line under the H1: the promise, in plain words.
level:       Beginner | Intermediate | Advanced
keywords:    the main query first, then variants people also type
updated:     YYYY-MM-DD
---

> [!TIP]
> **<Term> in one sentence.** The answer, 40–70 words, first. This is the paragraph a search engine
> or an assistant lifts, so it must stand alone and must not start with "In this lesson".

<the hero picture: {{map:<slug>}} — its spec in site/pages/mapspecs.py — or a {{board:…}}, {{figure:…}}, {{frameworks:…}}, {{model:…}} directive>

**In this lesson** you'll learn:
- three outcomes, each a verb phrase

## Sound familiar?
Three symptoms, *stated* not asked. Then one line saying which one this lesson fixes.

## <What is it?>            question-shaped H2s — they match what people ask
## <How it works, step by step>
### Step 1 · …              short steps, one idea each, a picture where the step has a shape
## Where you'll use it       (concept lessons) — or "When to use it" (how-to lessons)
## Why it matters
## Try it                    one problem; the answer in <details><summary>Show the answer</summary>
## Key takeaways             must — three, parallel, short
## FAQ                       3–5 questions people actually ask; 2–4 sentence answers
## Apply it in your role     must — a three-row table (forward-deployed engineer · product manager or
                             FDPM · GenAI or agentic AI engineer) × (Do this · The AI-augmented
                             shortcut), then "Across the enterprise" in two or three sentences, then
                             "The ten-minute workflow": one copyable prompt in a text block
## Sources and credits       must — a table of Idea · Origin · Source
```

## Rules

- **Must:** no H1 in the body; `## Key takeaways`, `## Apply it in your role` and `## Sources and credits` present; at least one
  picture; every `lesson:`, `track:`, `wiki:` and `#anchor` link resolves.
- **One idea per paragraph.** Two to four sentences. If a paragraph needs a sub-heading, it is two.
- **Answer first, everywhere.** The first sentence under a heading answers the heading.
- **Numbers carry their source.** A SkyWays number is a worked example from a fictional airline and
  says so the first time it appears. An outside number carries its author and year in the sources
  table. Never a statistic without a source.
- **Credit precisely.** In the sources table, *Original* means this playbook constructed it;
  *Adapted* means an outside idea changed here; *Borrowed* means used as published. When unsure,
  check [Sources and Confidence](../../../wiki/Sources-and-Confidence.md) and the primary source.
- **No fluff.** Delete any sentence that would survive unchanged in a lesson about a different topic.
- **British spelling** in prose, as the rest of the playbook. Put American variants in `keywords`.
- **Length:** 900–1,500 words, and up to about 3,000 for an interview bank; the build warns above 14 minutes.
- **Prompts** in "The ten-minute workflow" ask the model to question you rather than invent your numbers, and
  say what output shape you want. A prompt that would work unchanged for any lesson is not specific enough.
- **Edit here, never on the wiki.** Every wiki copy of a lesson is regenerated; an edit made on the wiki
  opens an issue (the Wiki edits workflow) and `wiki/sync.sh` refuses to overwrite it until it comes home.

## Links and pictures

| Write | For |
| --- | --- |
| `[text](lesson:slug#anchor)` | another lesson |
| `[text](track:id)` | a track page |
| `[text](wiki:Page-Name#anchor)` | a hand-written wiki page |
| `[text](site:qa/#measure)` | a page on the site |
| `[text](repo:docs/START-HERE.md)` · `repo:labs/` | a file or folder in the repo |
| `[text](sim:#/toolkit/aifit)` | the simulator |
| `{{board:pdlc}}` on its own line | a live board on the site, a screenshot on the wiki |

Visuals available: `board:` pdlc, loops, by_role, delegation · `figure:` bar_sheet, chain,
cache_prefix, bolt_days, shadow_widen, bill_factors, authority_ladder, two_numbers · `model:` g_decay,
g_doors, g_lever, g_wall, g_average, g_bound, g_funnel, g_multiply, g_fanout, g_dial, g_baton,
g_drift · `frameworks:` ring, ladder, chain. New ones are registered in `_visuals()` in
`site/pages/learn.py`, then screenshotted with `site/tools/shoot.mjs`.

## Mermaid on both targets

GitHub renders the wiki's mermaid in the reader's colour mode; the site renders it with the page's.
A hex cannot follow a theme, so use only these, which clear 3:1 on white and on near-black:

| Concept | Stroke | Tint fill | Band fill |
| --- | --- | --- | --- |
| P0 · slate | `#516981` | `#5169811A` | `#5169810D` |
| P1 · indigo | `#4B5CC8` | `#4B5CC81A` | `#4B5CC80D` |
| P2 · teal | `#0E7F7C` | `#0E7F7C1A` | `#0E7F7C0D` |
| P3 · amber | `#9C6803` | `#9C68031A` | `#9C68030D` |
| backwards / risk · rose | `#A93F3F` | `#A93F3F1A` | — |
| governance · violet | `#7455B3` | `#7455B31A` | — |
| yours / evidence · green | `#2C7A4B` | `#2C7A4B1A` | — |
| meta / questions · grey | `#6E6E6E` | `#6E6E6E14` | — |

Keep each label line short enough not to wrap — mermaid breaks any line wider than about 200px, so
about 22 characters bold and 25 italic; put a `<br/>` where the phrase breaks instead. Never set
`color:` on a node. Style every `subgraph` band with `style <id> fill:…0D,stroke:…`.
Never point an edge back at an earlier node inside a banded diagram — end on a terminal node. Count
the invisible `~~~` links when numbering `linkStyle`. Keep a diagram's intrinsic width under ~700px:
stack bands vertically, two nodes across. `site/tools/check_diagrams.py` renders every block in both
themes and fails on small text, low contrast and bands out of order, and warns on wrapped lines and
drawings wider than 720px.

## Screenshots

A screenshot of the simulator goes on its own line as `![alt](site:assets/learn/name.webp)`.
Capture it with `node site/tools/simshots.mjs <simulator url> site/assets/learn` — at 2x, as WebP,
clipped to one element — and the renderer reads its size from the file, so a narrow one stays narrow
on the site and on the wiki. Write the alt text as the sentence the screenshot proves. Never capture
the simulator's photographs; clip to the part of the page that is the playbook's own work.
