# Writing a lesson

The tutorial is written once, here, and published under `/learn/` on the site, which is the only
copy (GitHub does not let search engines index a wiki with fewer than 500 stars or open editing).
`python3 site/build.py` renders and validates it; `python3 site/learn_export.py` puts a thin index on
the wiki (Start Here and one page per track, each linking the lessons here) and a pointer line on
the reference pages a lesson introduces.

The build refuses a lesson that breaks the rules marked **must**. The rest are warnings.

## The map at the top of a lesson

Every lesson opens with a picture drawn in the site's illustration grammar, not a mermaid fence. The
lesson embeds it with `{{map:<slug>}}` on a line of its own (the slug is the lesson's), and the picture
itself is a short spec in [`site/pages/mapspecs.py`](../../pages/mapspecs.py): a title row, one of
five shapes, and a callout that says what the picture proves. The shapes are `bands` (rows per phase or
theme), `flow` (a chain, with an optional gate, terminal or decision), `pairs` (two panels,
row-aligned), `funnel` (a ladder of questions) and `fan` (one question, its outcomes). Change the spec,
not the lesson, to change the picture. The wiki shows a screenshot of it
(`python3 site/build.py --shots`, then `node site/tools/shoot.mjs`). Mermaid still works anywhere
else in a lesson.

## Anatomy: every lesson, same slots, same order

Parallel slots are what let a reader skim twelve lessons and know where the answer is in each.

```markdown
---
title:       the <title> and the H1. The query a practitioner types, made specific. ≤ 60 characters.
             Write it in title case for search; the H1 shows it in sentence case (see Rules).
short:       the sidebar label. ≤ 34 characters.
wiki:        the wiki page name. Letters, digits, hyphens. Must not collide with a hand-written page.
description: 120 to 160 characters. Contains the main term and promises the payoff.
dek:         one line under the H1: the promise, in plain words.
level:       Beginner | Intermediate | Advanced
keywords:    the main query first, then variants people also type
updated:     YYYY-MM-DD
---

> [!TIP]
> The answer first, in at most three short sentences. No bold lead: the page already labels this box
> "In short". It is the paragraph a search engine or an assistant lifts, so it must stand alone and
> must not start with "In this lesson".

<the hero picture: {{map:<slug>}} (its spec in site/pages/mapspecs.py) or a {{board:…}}, {{figure:…}}, {{frameworks:…}}, {{model:…}} directive>

**In this lesson** you'll learn:
- three outcomes, each a verb phrase

## Sound familiar?
Three symptoms, *stated* not asked. Then one line saying which one this lesson fixes.

## <What is it?>            question-shaped H2s: they match what people ask
## <How it works, step by step>
### Step 1 · …              short steps, one idea each, a picture where the step has a shape
## Where you'll use it       (concept lessons), or "When to use it" (how-to lessons)
## Why it matters
## Try it                    one problem; the answer in <details><summary>Show the answer</summary>
## Key takeaways             must: three, parallel, short
## FAQ                       3 to 5 questions people actually ask; answers of 2 to 4 sentences
## Apply it in your role     must: a table of three rows (forward-deployed engineer · product manager
                             or FDPM · GenAI or agentic AI engineer) × (Do this · The AI-augmented
                             shortcut), plus a row for any role the home page sends here (below),
                             then "Across the enterprise" in two or three sentences, then
                             "The ten-minute workflow": one copyable prompt in a text block
## Sources and credits       must: a table of Idea · Origin · Source
```

## Rules

- **Must:** no H1 in the body; `## Key takeaways`, `## Apply it in your role` and `## Sources and credits` present; at least one
  picture; every `lesson:`, `track:`, `wiki:` and `#anchor` link resolves; the summary at most three sentences, with no
  bold lead (the box is labelled "In short", and the markdown twin writes that label once).
- **One idea per paragraph.** Two to four sentences. If a paragraph needs a sub-heading, it is two.
- **Answer first, everywhere.** The first sentence under a heading answers the heading.
- **Numbers carry their source.** A SkyWays number is a worked example from a fictional airline and
  says so the first time it appears. An outside number carries its author and year in the sources
  table. Never a statistic without a source.
- **Credit precisely.** In the sources table, *Original* means this manual constructed it;
  *Adapted* means an outside idea changed here; *Borrowed* means used as published. When unsure,
  check [Sources and Confidence](../../../wiki/Sources-and-Confidence.md) and the primary source.
- **No fluff.** Delete any sentence that would survive unchanged in a lesson about a different topic.
- **British spelling** in prose, as the rest of the manual. Put American variants in `keywords`.
- **Length:** 900 to 1,500 words, and up to about 3,000 for an interview bank; the build warns above 14 minutes.
- **Prompts** in "The ten-minute workflow" ask the model to question you rather than invent your numbers, and
  say what output shape you want. A prompt that would work unchanged for any lesson is not specific enough.
- **Titles in sentence case on the page.** The renderer sets the H1 and the track's list in sentence case and
  keeps the `<title>` as written. A word with a capital past its first letter (AI, PDLC, DevOps) or a digit keeps
  its own; a name that has neither (Kanban, Spec Kit, P1 Design & Spec) goes in `KEEP_CASE` in
  `site/pages/learn.py`, or it is lowered. The H1 is the whole title, in two lines on a wide screen: the part
  before the first ": " or "? " in ink, the rest in the grey continuation, and a hyphenated word (hand-off,
  AI-DLC) never breaks across a line. So write the title as the lesson's name, then what it promises.
- **The page sets the measure.** A lesson reads in one column, in the order it is written, and nothing floats
  beside it: the guide on the right holds only navigation. Prose, the lede, "In short", a two-column table, the
  sketch and "Try it" stop at one measure (584px, about 75 characters of the 19px body); boards, drawn figures,
  code and tables of three columns or more run to the column's edge, 944px, and so does the title from 1280px
  wide. So a lesson has one left edge and two right ones, and `site/tools/accept.mjs` holds them on every
  lesson. Put a sketch straight after the paragraph it draws, where it is drawn at the text's width, and keep
  "Try it" to the problem and its folded answer: no table or code block in it.
- **A picture follows its sentence.** It goes on the line after the paragraph that says what it shows, never
  touching a table or another picture, and it draws no number its lesson's text does not state. A small figure
  (a few bars, no notes) is marked `fig sm` in `site/pages/figures.py` and keeps to the text's width.
- **A lesson the home page links to answers its card.** Four lessons are the home page's tutorial band (P0
  Frame, For solution architects, Guardrails that hold, How accurate must an agent be?). Each asks its card's
  question in its title or lede, answers it in the first two sentences of "In short", and has a row in "Apply it
  in your role" for the card's role, ending with a link to that role's steps (the table's first row, unless the
  role is one of the three already there). The four sentences the band quotes are checked by the build
  (`site/pages/people.py`): change them only with the band.
- **A table stacks on a phone.** Three or more columns become one block per row, its first cell as the row's
  name and each other cell under its column's heading. Make the first column the thing the row is about.
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
| `[text](sim:#/toolkit/aifit)` | a page of the workbench |
| `{{board:pdlc}}` on its own line | a live board on the site, a screenshot on the wiki |

Visuals available: `board:` pdlc, loops, by_role, delegation · `figure:` bar_sheet, chain,
cache_prefix, bolt_days, shadow_widen, bill_factors, authority_ladder, two_numbers, drift_slide,
postmortem_layers, rollback_times · `model:` g_decay, g_doors, g_lever, g_wall, g_average, g_bound,
g_funnel, g_multiply, g_fanout, g_dial, g_baton, g_drift · `frameworks:` spine, pdlc_vs, ladder, chain,
methods, merge. New ones are registered in `_visuals()` in `site/pages/learn.py`, then screenshotted with
`site/tools/shoot.mjs`.

## Mermaid on both targets

GitHub renders the wiki's mermaid in the reader's colour mode; the site renders it with the page's.
A hex cannot follow a theme, so use only these, which clear 3:1 on white and on near-black:

| Concept | Stroke | Tint fill | Band fill |
| --- | --- | --- | --- |
| P0 · slate | `#516981` | `#5169811A` | `#5169810D` |
| P1 · indigo | `#4B5CC8` | `#4B5CC81A` | `#4B5CC80D` |
| P2 · teal | `#0E7F7C` | `#0E7F7C1A` | `#0E7F7C0D` |
| P3 · amber | `#9C6803` | `#9C68031A` | `#9C68030D` |
| backwards / risk · rose | `#A93F3F` | `#A93F3F1A` | n/a |
| governance · violet | `#7455B3` | `#7455B31A` | n/a |
| yours / evidence · green | `#2C7A4B` | `#2C7A4B1A` | n/a |
| meta / questions · grey | `#6E6E6E` | `#6E6E6E14` | n/a |

Keep each label line short enough not to wrap: mermaid breaks any line wider than about 200px, so
about 22 characters bold and 25 italic; put a `<br/>` where the phrase breaks instead. Never set
`color:` on a node. Style every `subgraph` band with `style <id> fill:…0D,stroke:…`.
Never point an edge back at an earlier node inside a banded diagram. End on a terminal node. Count
the invisible `~~~` links when numbering `linkStyle`. Keep a diagram's intrinsic width under ~700px:
stack bands vertically, two nodes across. `site/tools/check_diagrams.py` renders every block in both
themes and fails on small text, low contrast and bands out of order, and warns on wrapped lines and
drawings wider than 720px.

## Screenshots

A screenshot of the workbench goes on its own line as `![alt](site:assets/learn/name.webp)`.
Capture it with `node site/tools/simshots.mjs <workbench url> site/assets/pictures` (at 2x, as WebP,
clipped to one element) and the renderer reads its size from the file, so a narrow one stays narrow
on the site and on the wiki. Write the alt text as the sentence the screenshot proves. Never capture
the workbench's photographs; clip to the part of the page that is the manual's own work.
