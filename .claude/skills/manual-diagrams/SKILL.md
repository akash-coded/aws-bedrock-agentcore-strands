---
name: manual-diagrams
description: Add or change an illustration on the agentic-manual site — a full-width board on the homepage or a per-step figure on a role page. Use when asked to draw, illustrate, visualise or restyle anything in site/, or to add a diagram to a wiki page. Covers the board primitives, the figure registry, the hue tokens, the placement hints and the verification the build does not do for you.
---

# Diagrams in this repo

Two systems, one grammar. Read the global `explainer-diagrams` skill first — it holds the
grammar itself. This one is where that grammar lives in this codebase.

## Boards — wide, text-heavy, HTML

`site/pages/dg.py` holds the primitives, `site/pages/boards.py` the content, and
`site/theme/base.css` (section `DIAGRAM SYSTEM · "boards"`) the styling.

| Primitive | Frame it builds |
| --- | --- |
| `board(kicker, title, sub, inner, note, bid)` | the outer frame every board shares |
| `flow(columns, gate_after)` | parallel comparison; `gate_after` marks one hard crossing |
| `column(hue, name, owner, icon, thesis, steps, takeaway)` | one column of a flow |
| `matrix(cols, rows, legend)` | two dimensions crossing |
| `band(...)` / `bands([...])` | left rail plus canvas, stacked |
| `returns(label)` | the dashed feedback line under a flow |
| `section_band(label)` / `dgt` | the near-black meta label |

Boards are HTML rather than SVG on purpose: they are 1100px wide and full of prose, and
SVG text does not wrap, theme, or read out to a screen reader. Add a new board as a
function in `boards.py` and call it from `home_page()` in `render.py`.

## Figures — small, geometric, SVG

`site/pages/figures.py`, fixed 560x190 frame, registered in the `FIGURES` dict. A step
earns a figure only when the shape of the thing is the lesson; most steps have none.

Placement is declarative, never hard-coded: `site/content/roles/_src/enrich.py` maps
`(role, step)` to a `figure` and/or `calc` name, and the build fails if a hint names
something that does not exist.

## Hues

`--dg-slate|indigo|teal|amber|green|violet|rose|sky`, with `--dg-fill` / `--dg-soft` /
`--dg-line` for tints and hairlines. Never write a hex inside a figure — dark mode
redefines every token and a literal will not follow.

`--dg-on` is the ink that sits **on** a solid hue. It is white in light mode and near-black
in dark, because dark mode lifts the hues so they read against a dark page.

## Two traps this repo has already fallen into

**`strong,b` sets colour directly** (base.css line ~116), which beats inherited colour
however specific the ancestor. Any bold word on a solid-hue background must set
`color:var(--dg-on)` itself or it renders at about 1.5:1. Measure contrast, do not look at
a screenshot — at small scale dark-on-hue reads as light-on-hue and you will pass it.

**Gutter grids.** A two-column grid whose first track is a narrow gutter for a `::before`
marker must send every real child to column two. See the `.gutter-grid` comment in
base.css; this has caused three separate layout bugs.

## Verifying

`python3 site/build.py`, then serve `site/_site` and look at it. Headless Chrome clamps
its window to about 485px, so a 390px `--window-size` crops a correctly laid-out page and
invents an overflow bug — use the browser pane's mobile preset for true narrow widths, and
compare `document.documentElement.scrollWidth` against `clientWidth` rather than eyeballing.

Always run: light, dark, 375px, the greyscale and thumbnail passes, and a contrast
measurement of every text-on-hue surface. Gates to pass before committing:
`python3 wiki/check.py`, `python3 site/content/roles/_src/build_content.py`,
`python3 site/build.py`.
