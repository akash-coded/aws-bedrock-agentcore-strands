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

## Four traps this repo has already fallen into

**`strong,b` sets colour directly** (base.css line ~116), which beats inherited colour
however specific the ancestor. Any bold word on a solid-hue background must set
`color:var(--dg-on)` itself or it renders at about 1.5:1. Measure contrast, do not look at
a screenshot — at small scale dark-on-hue reads as light-on-hue and you will pass it.

**Gutter grids.** A two-column grid whose first track is a narrow gutter for a `::before`
marker must send every real child to column two. See the `.gutter-grid` comment in
base.css; this has caused three separate layout bugs.

**`--accent` is redefined per page** (render.py sets it from the role's colour). A figure
that draws with it renders in a different hue on every page that shows it, which means its
colour carries no information. Figures use `--dg-*` only.

**Mermaid on the wiki is a different medium.** Wiki diagrams are rendered by GitHub in an
iframe using *the reader's* colour mode, and a `classDef` hex cannot follow a theme. Four
things follow, all of which cost a round trip once:

- A `subgraph` with no `style` line gets mermaid-dark's own **#474949** band fill, and
  every hued node border inside it falls to about 1.4:1. Always give a band
  `style <id> fill:#HHHHHH0D,stroke:#HHHHHH,stroke-width:1.5px` so its nodes sit on the
  canvas and the band carries its own hue.
- A stroke hue must clear 3:1 against **both** `#FFFFFF` and `#0D1117`. The window is
  roughly L 0.12–0.30, which is wide; the site's light `--dg-*` values are too dark for it
  and the wiki uses lifted variants (`#516981`, `#4B5CC8`, `#7455B3`, `#78589B`).
- No fixed grey clears 4.5:1 for **text** against both white and near-black — the two
  windows do not overlap. Never set `color:` on a muted node; let the theme pick it and
  let a dashed border carry "muted".
- A back edge to an earlier node makes a cycle, and dagre breaks it by reversing a
  *forward* edge — so `A-->B-->C-->D; D-.->A` can render D first. `<-.-` does not help
  when the endpoints are clusters; mermaid ignores it and draws the arrow forward. End the
  chain on a terminal node instead, or drop the edge. Also count `~~~` invisible links
  when numbering `linkStyle`: they are declared first, so styling index 1 usually reveals
  an invisible link rather than the arrow you meant, and a `linkStyle` stroke override
  silently drops the dash that carries dashed-means-flow.

## Verifying

`python3 site/build.py`, then serve `site/_site` and look at it. Headless Chrome clamps
its window to about 485px, so a 390px `--window-size` crops a correctly laid-out page and
invents an overflow bug — use the browser pane's mobile preset for true narrow widths, and
compare `document.documentElement.scrollWidth` against `clientWidth` rather than eyeballing.

Check collisions by measurement, not by looking. In the page, walk every `<text>` in a
figure, take `getBBox()`, and test each pair for rectangle intersection — also test each
label against the viewBox so nothing escapes its frame. Two label collisions in the loops
board and the whole text-on-hue contrast class of bug were found this way after passing a
visual inspection twice.

Always run: light, dark, 375px, the greyscale and thumbnail passes, and a contrast
measurement of every text-on-hue surface. Gates to pass before committing:
`python3 wiki/check.py`, `python3 site/content/roles/_src/build_content.py`,
`python3 site/build.py`.

For wiki mermaid, `wiki/check.py` only checks that the fence declares a diagram type — it
never renders. Render every block with mermaid 11 in headless Chrome under **both**
`theme:"dark"` and `theme:"default"`, and assert three things numerically: no node label
below 11px once the SVG is scaled to a 896px column (GitHub's wiki content width), stroke
vs its *composited* surface at 3:1 and label vs its composited fill at 4.5:1, and cluster
order along the true layout axis. Two harness errors to avoid, both of which produced
confident wrong answers here: `getBBox()` on a `g.cluster` ignores the element's own
transform and returns (8,8) for everything — use `getBoundingClientRect()`; and a cluster
is a **sibling** of the nodes it contains, not their ancestor, so `closest("g.cluster")`
finds nothing and every node looks like it sits on the page background. Resolve the
surface geometrically, by which cluster rect contains the node's centre.
