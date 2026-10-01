---
name: SkyWays, the agentic manual
status: final
updated: 2026-10-01
form-factor: web, phone first, static HTML with progressive enhancement
visual-identity: DESIGN.md
---

# How the site works

`DESIGN.md` says how the pages look. This file says who arrives, what each page is for, and how the
pages behave. It records the decisions of the October 2026 restructure and the evidence behind them.

## Foundation

A static site, rendered by Python to plain HTML, one stylesheet and a few small scripts. Every page
reads without script. Light and dark follow the reader's system until they choose. The simulator is a
separate single file, published unchanged.

Readers arrive cold, from a search ("AI-DLC vs BMAD", "spec-driven development template") or from a
link a colleague sent. Most land on a deep page, not the home page, and most have never heard of
SkyWays. So every page has to say where the reader is, and the home page has three jobs only: say what
this is, show that it is real, and offer one way in.

## Information architecture

```
Home                      what this is, the four methods on one line, the roles, the simulator, the shelf
├─ Tutorial   /learn/     55 lessons in eight tracks
├─ Roles                  product manager, solution architect, engineering lead, QA, DevOps
├─ Method     /method/    the four boards: phases, loops, roles by phase, what a model may draft
├─ Library                templates, prompts, mental models, frameworks, picture pack
├─ Leadership /protocol/  for whoever funds the work
└─ Simulator  /simulator/ the worked case as a game
```

The top bar carries those five places and the simulator. The drawer (top left) still lists every page
by category and holds the search; on a phone it is the navigation.

The home page, top to bottom:

1. **Hero.** The headline, one sentence that says what the site is and that it is free, two buttons
   (start the tutorial, play the simulator), one line of counts and the author.
2. **Which agentic method should your team follow?** Answered in the heading, then drawn: four methods
   as bars along the four phases.
3. **Start from the job you do.** Six rows, five roles and the sponsor. The page's only routing device.
4. **Or play the ninety days yourself.** The simulator's own opening screen, three numbers, one button.
5. **Take what you need.** Six tiles: tutorial, templates, prompts, mental models, pictures, leadership.
6. **New to all this?** One lesson, eight minutes.

What left the home page went one click deeper, not away. The phase board, the eight loops, the role by
phase matrix and the delegation board are on `/method/` with their ids unchanged. Old links to
`/#pdlc`, `/#loops`, `/#by-role` and `/#delegation` are forwarded there by a script in the home page's
head, the same way the simulator's old `/#/…` routes are. The task table ("about to write a spec",
"about to launch") is on the tutorial's landing page as "Start where you are".

## Voice and tone

- A heading is a sentence the reader could say back: a question they came with, or a claim with a verb
  in it. Three to nine words. No category labels.
- One sentence under a page title, fifteen words or fewer where the page allows it.
- Plain words before house words. "P0 to P3" always appears beside the phase names, and the phase
  questions ("Is it worth building, and is it AI at all?") carry the meaning for a stranger.
- "Role", not "chair". "A fictional airline" on first mention of the case.
- No dashes in prose, no contrast staged for weight ("not X but Y"), no closing line that repeats the
  paragraph. The `humanizer` patterns are the checklist.
- Counts are stated as numbers and computed at build time.

## Component patterns

| Pattern | Behaviour |
| --- | --- |
| Top bar lists (Roles, Library) | Each is a `<details>`: opens on click or Enter without script. Script closes the other one, and closes on Esc, on a click elsewhere and when the focus tabs out. The parent is marked when a child page is current. |
| Drawer | Unchanged: `<details>`, Esc and scrim close it, `/` opens it on the search box. |
| Coverage table | Phase headers and method names are links to their lessons. Bars are cells with a visually hidden reading ("covers this phase"). Fits a 375px screen without scrolling. |
| Role rows | The whole row is the link. Hover tints the row in the role's colour and moves the arrow. |
| Simulator frame | The whole frame is one link to the simulator. |
| Folded how-to | Closed on arrival. Holds the audience, the use, the steps and the walkthrough button. |
| Walkthrough | Never offered by a popup, and nothing about it is stored. A small face sits bottom left on wide screens and names itself on hover; on a phone it is inside the folded how-to only. |
| Reveal | A band rises 18px into place the first time it is scrolled to. Without script, or with reduced motion, it is simply there. |

## State patterns

- **No script, or the home page's own script missing:** the globe is a shaded disc with the flight drawn
  over it; every band is visible, because the script that hides a band for its reveal is the one that
  reveals it; both top-bar lists open and close; the drawer works.
- **Reduced motion:** the globe is drawn once and does not turn, the plane holds its place between
  Frame and Design, nothing fades in.
- **Off screen or hidden tab:** the globe stops drawing.
- **Theme change:** the globe re-reads its colours and redraws; the simulator frame swaps its picture.
- **Old anchor on the home page:** forwarded to `/method/` before the page paints.

## Interaction primitives

Transitions sit on the site's scale (150, 250, 350, 400ms) with the one easing. Hover never carries
information that focus or the page itself does not. On a phone, buttons, navigation and list rows are
at least 44px tall; a link inside a sentence, and a checkbox in a self-check, keeps its text's height.

## Accessibility floor

- Text contrast is at least 4.5:1 in both themes, measured on every page type at 375 and 1280px. Two
  things sit under it by design: the grey continuation of a display heading, used only at 29px and above
  where it passes the 3:1 large-text bar, and a disabled button.
- The hero scene is `aria-hidden`: it repeats section two, which is real text and a real table.
- The coverage table has a caption, column and row headers, and a text reading in every cell.
- One `h1` per page; bands are labelled sections; the skip link, focus rings and breadcrumbs are kept.
- No page scrolls sideways at 375px.

## Key flows

Illustrative readers, used to test the pages. None of them is a real person.

**Meera, an engineering lead, on her phone between meetings.** She searched "AI-DLC vs BMAD" and
landed on the home page.
1. The first screen tells her it is a free manual for teams building with AI agents.
2. She scrolls once. The heading is her own question, and it answers: all four.
3. She reads the bars: BMAD stops before production, AIDD covers the build only.
4. *The moment:* she sees the methods are stretches of one line, not rivals, and taps "Compare the four methods".

**Daniel, a product manager, from a link a colleague posted.**
1. Home: he reads one sentence and scrolls to the roles.
2. He finds his row: "a vibe → a number you can defend".
3. The role page opens on his title, one line and the eight steps as a track.
4. *The moment:* he opens step one and copies the pain register template.

**Priyanka, who funds an agent programme, sent straight to `/protocol/`.**
1. The top bar says SkyWays, the agentic manual, with Leadership marked.
2. The title says what the page is, the line under it says it is for her.
3. *The moment:* she reaches "the four decisions only you can make" and takes them to her review.

**Tomás, a QA lead, who searched for a golden set template and landed on `/templates/`.**
1. Title, one line, "40 templates".
2. He picks QA lead in the left rail.
3. *The moment:* he presses Copy on the first block.

**Li Wei, who would rather play than read.**
1. Home: the second button in the hero says "Play the simulator".
2. *The moment:* the simulator opens on its own start screen, with a guided path through the case.

## Inspiration and anti-patterns

Two benchmarks were run before the restructure, from full-page screenshots and page text.

Ten product home pages (Linear, Stripe, Vercel, Raycast, Resend, Cursor, Tailwind, Claude, Framer,
PostHog): the median headline is five words, the subhead thirteen, there are two buttons in the hero,
five blocks in the first screen, five or six items in the top bar, about nine sections, and 120 to
128px above and below each one. Section headings are 40 to 56px on seven of the ten and a regular or
medium weight on eight, and five continue a white heading into a grey sentence at the same size. None has more than
three buttons in view, two paragraphs under one heading, or a sidebar beside the hero.

Seventeen manuals, courses, libraries and simulators (Shape Up, Linear Method, The Twelve-Factor App,
Thoughtworks Technology Radar, web.dev Learn, roadmap.sh, CSS for JS Developers, Full Stack Open,
Microsoft Learn, The Odin Project, Laws of UX, Refactoring.Guru, Untools, Brilliant, The Evolution of
Trust, ciechanow.ski, neal.fun): the median headline is three words, the subhead eleven, with one
button and at most two. Where a page routes readers it offers two to four doors. A section landing page
puts a title, one line and one count above its content, which starts within 370 to 560px. A manual's
landing page is its contents; a simulator's is its start screen; a work by one person is signed once,
by name, beside the title.

What the page was doing before, and no longer does: explaining the method five times, offering five
different ways to pick a role, listing its inventory three times, and opening every landing page with
an instruction strip, a contents box, a walkthrough button and a popup.

## Responsive and platform

- **Wide (over 1000px):** hero words left, scene right; the simulator band is two columns.
- **Tablet and phone:** the hero stacks, words first; the scene follows, centred and cropped by the
  band. The first phone screen holds the headline, the sentence, both buttons and the counts.
- **Under 860px:** the top bar keeps the mark, the simulator and the theme; the five places are in the
  drawer.
- **Under 760px:** the coverage table drops its questions and one-liners and fits the screen; role rows
  become two lines.

## Open items

- The home page's social card still carries the previous headline. It is drawn by `pages/ogcards.py`
  and rendered by `tools/ogshots.mjs`.
- The wiki's own pages still link to the old home anchors. They are forwarded, and the next
  `wiki_export.py` run rewrites them.
