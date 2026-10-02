---
name: SkyWays, the agentic manual
status: final
updated: 2026-10-02
form-factor: web, phone first, static HTML with progressive enhancement
visual-identity: DESIGN.md
---

# How the site works

`DESIGN.md` says how the pages look. This file says who arrives, what each page is for, and how the
pages behave. It records the decisions of the October 2026 restructure and the evidence behind them.

## Foundation

A static site, rendered by Python to plain HTML, one stylesheet and a few small scripts. Every page
reads without script. Every page opens dark. Light is the reader's choice, made with the toggle in the
top bar and remembered; paper is always printed light. The simulator is a game, Ninety Days, with its
own spine in `GAME.md`. The tool that used to be the simulator is the workbench: a separate single file,
published unchanged, with its own day and night switch.

Readers arrive cold, from a search ("AI-DLC vs BMAD", "spec-driven development template") or from a
link a colleague sent. Most land on a deep page, not the home page, and most have never heard of
SkyWays. So every page has to say where the reader is, and the home page has three jobs only: say what
this is, show that it is real, and offer one way in.

## Information architecture

```
Home                      what this is, why a spine, the methods on it, the roles, the simulator, the tutorial, the shelf
├─ Tutorial   /learn/     55 lessons in eight tracks
├─ Roles                  product manager, solution architect, engineering lead, QA, DevOps
├─ Method     /method/    the four boards: phases, loops, roles by phase, what a model may draft
├─ Library                templates, prompts, mental models, frameworks, picture pack
├─ Leadership /protocol/  for whoever funds the work
├─ Simulator  /simulator/ Ninety Days: the worked case as a game
├─ Labs       /labs/      one job of the project by hand, with a real model's recorded replies
└─ Workbench  /workbench/ the earlier tool: episodes in depth, calculators, role playbooks
```

The top bar carries those five places and one slot that changes with where the reader is. The slot never
points at the page it is on. In the manual it is one pill, "Simulator". In a lesson the pill is "Play this
day" when the game has a day that lesson is the reading for, and a quiet link beside it jumps to the
lesson's own "Apply it in your role". In the game the pill is "Read the lesson" for the day on screen, and
the quiet link goes back to the manual. On a phone the pill stays and the quiet link is left to the drawer.
The drawer (top left) still lists every page by category and holds the search; on a phone it is the navigation.

The home page, top to bottom:

1. **Hero.** The headline, two sentences that say what the site is, the three ways to take it and that
   it is free, two buttons (start the tutorial, play the simulator), one line of counts and the author.
2. **Agent projects go wrong in four places.** The reason to care, then the lifecycle: four methods give
   it one idea each, their lines meet in one point, and out of it comes one line that closes into a loop,
   the question each phase asks above it, and under it the line a team hears when the question was skipped.
3. **Which agentic method should your team use?** Any of the four works, says the paragraph; the table
   shows which phases each covers, and its last row what no method decides for you. One link below it
   sorts the other names a reader may have heard.
4. **Start from the job you do.** Seven rows: five roles, the forward-deployed engineer and the sponsor.
   The page's only routing device, with one quiet link to the tutorial's nineteen starting points for
   anyone not on the list.
5. **Play a ninety-day AI project in fifteen minutes.** One button, a line with the number of decisions
   and the time a game takes, and a quiet link to the labs. Beside them, one real day of the game as a
   card: Day 45, its room drawn in pixels, its headline, its context, its question and its three answers
   with their price in days, each of which opens that day in the game.
6. **Read the lessons in order.** The eight tracks, numbered, one sketch from a lesson as a sample, and
   one button to lesson one.
7. **Copy the templates and prompts you need.** Four tiles: templates, prompts, mental models, pictures.

Every band's heading stands alone. The three ways in are named once, in the hero's second sentence, so
no heading has to begin with "Or" and a reader who lands mid-page is not left asking "or what?".

What left the home page went one click deeper, not away. The phase board, the eight loops, the role by
phase matrix and the delegation board are on `/method/` with their ids unchanged. Old links to
`/#pdlc`, `/#loops`, `/#by-role` and `/#delegation` are forwarded there by a script in the home page's
head, the same way the workbench's old `/#/…` routes are. The task table ("about to write a spec",
"about to launch") is on the tutorial's landing page as "Start where you are".

## Voice and tone

- A heading is a sentence the reader could say back: a question they came with, or a claim with a verb
  in it. Three to nine words. No category labels.
- One sentence under a page title, fifteen words or fewer where the page allows it.
- Plain words before house words. "P0 to P3" always appears beside the phase names, and the phase
  questions ("Is it worth building, and is it AI at all?") carry the meaning for a stranger. On a landing
  page and in the game a house word appears only beside the plain one: "sign-off" for the hard gate, "pass
  mark" for the bar, "kind of case" for a slice. "Spine" is not used on the home page.
- One idea to a sentence, twenty words at most, and say the thing rather than a saying about it. A
  sentence the owner flagged, kept here as the pattern to avoid: "The spine keeps the part each does best
  and adds what none of them decides."
- Every screen can be read cold. A heading names what the screen is about to someone who has seen no other
  screen; a step in a sequence carries one line of what came before. In the game that line is "So far".
- "Role", not "chair". "A fictional airline" on first mention of the case.
- No dashes in prose, no contrast staged for weight ("not X but Y"), no closing line that repeats the
  paragraph. The `humanizer` patterns are the checklist.
- Counts are stated as numbers and computed at build time.

## Component patterns

| Pattern | Behaviour |
| --- | --- |
| Top bar lists (Roles, Library) | Each is a `<details>`: opens on click or Enter without script. Script closes the other one, and closes on Esc, on a click elsewhere and when the focus tabs out. The parent is marked when a child page is current. |
| Drawer | Unchanged: `<details>`, Esc and scrim close it, `/` opens it on the search box. |
| Top bar slot | Chosen by the page when it is built, never by script, except inside the game, which points the pill at the lesson behind the day on screen. Between pages, where the browser can, the pill's shape travels and resizes on the spring and its words swap with a short blur; elsewhere the page simply changes. |
| Lifecycle figure | One piece of markup, two layouts. Over 1000px the four methods stack on the left, their lines run into one point, the name sits on the line that leaves it, the four questions sit inside the loop and the four symptoms hang under it. At 1000px and under the methods are a row of chips, then the line, then each phase with its question and its symptom. Methods and phases link to their lessons. The drawing is hidden from a screen reader; a sentence says the lifecycle keeps one idea from each of four methods, and each symptom is prefixed with "Skip it, and you hear". |
| Sketch | A `<figure>`: the drawing is one image with a description of the scene, and the caption under it is real text that makes the point alone. Its notes arrive once, in order, when first scrolled to; without script, in print and under reduced motion it is simply complete. It prints on white, never across a page break. |
| Method table | Phase headers and method names link to their lessons. Bars are cells with a hidden reading ("covers this phase", "extended in this manual"). Fits a 375px screen without scrolling; there, the spine's row becomes a list under the table. |
| Role rows | The whole row is the link. Hover tints the row in the role's colour and moves the arrow. Two rows are not role journeys and say so in their counts: the forward-deployed engineer's field guide and the sponsor's page. |
| Track list | Eight links, numbered in order, each with its lesson count. |
| Simulator frame | The whole frame is one link to the simulator. |
| Folded how-to | Closed on arrival. Holds the audience, the use, the steps and the walkthrough button. |
| Section rail | On a wide screen the role pages and the leadership page list their sections down the left and mark the one being read (`aria-current`): the last one whose top has passed the upper third of the window. On a narrow screen a role page relies on its step track, and the leadership page folds the list under its title. |
| Role step | The step's head links to its template and its prompts; a tap opens the step if it is shut and lands on the block. "Expand all" sits beside the steps' heading. On a wide screen in a browser that can, a step opens to its height in 250ms; elsewhere it is simply open. |
| Copy | The button turns green, draws a tick and says "Copied"; a polite live region says so to a screen reader. |
| Pause control | A checkbox in the corner of the hero and of the tower figure. Ticked, the flight, the globe and the tower hold still. It works without script for everything but the globe, which needs script to turn at all. |
| Figures | A drawn figure fades in part by part, in drawing order, the first time it is scrolled to. Nothing is hidden beforehand: a figure the observer never reaches is simply there. |
| Page to page | Where the browser supports it, one page cross-fades into the next with the top bar held still, and a title on both pages (a lesson in its track list, a role in its home-page row) travels to its new place. |
| Next up | Templates, prompts, mental models, frameworks and the picture pack each end on one sentence, one button and one quiet link. |
| Walkthrough | Never offered by a popup, and nothing about it is stored. Two ways in, on every screen width: "Show me around this page" in the drawer, shown only on a page that has a walkthrough, and "Show me around" in the folded how-to. Nothing floats over the page for it. The card highlights one element at a time and carries a plain label, "The walkthrough", the step count, the step's title and text, and Back and Next; it has no face and no name. Esc, the arrow keys and the close button work. |
| Reveal | A band rises 18px into place the first time it is scrolled to. Without script, or with reduced motion, it is simply there. |

## State patterns

- **No script, or the home page's own script missing:** the globe is a shaded disc with the flight drawn
  over it; every band is visible, because the script that hides a band for its reveal is the one that
  reveals it; both top-bar lists open and close; the drawer works.
- **Reduced motion:** the globe is drawn once and does not turn, one aircraft is parked at each phase,
  nothing fades in, pages do not cross-fade, connectors do not move, and the pause control is not shown
  because there is nothing to pause.
- **Paused:** the flight, the aircraft's shape, the sign-off's bar and the tower hold together, and the
  globe stops turning.
- **A second visit to the home page in one sitting:** the hero is already drawn; its entrance played once.
- **A browser that cannot ease one path into another (Safari):** the aircraft is four drawings that take
  turns on the same clock.
- **A browser without scroll timelines, view transitions or animatable `auto` height:** connectors are
  still, pages change at once, steps snap open. Nothing is missing, only the movement.
- **Off screen or hidden tab:** the globe stops drawing.
- **Theme:** dark until the reader chooses light. The choice is kept in `localStorage` and applied before
  the page paints. Without script the page stays dark. The browser's own chrome follows the page.
- **Theme change:** the globe re-reads its colours and redraws; the simulator frame swaps its picture.
- **Print:** always the light tokens, whatever the screen shows.
- **Old anchor on the home page:** forwarded to `/method/` before the page paints.
- **Old workbench route:** a link to `/simulator/#/…` or `/#/…` is forwarded to `/workbench/#/…` before
  the page paints. The game never uses a hash that begins with a slash.

## Interaction primitives

Motion has three permitted jobs and two classes; `DESIGN.md` states them. Transitions sit on the site's
scale (150, 250, 350, 400ms) with the one easing. Hover never carries
information that focus or the page itself does not. On a phone, buttons, navigation and list rows are
at least 44px tall; a link inside a sentence, and a checkbox in a self-check, keeps its text's height.

## Accessibility floor

- Text contrast is at least 4.5:1 in both themes, measured on every page type at 375 and 1280px. Two
  things sit under it by design: the grey continuation of a display heading, used only at 29px and above
  where it passes the 3:1 large-text bar, and a disabled button.
- The hero scene is `aria-hidden`: it repeats the spine band, which is real text.
- The spine's drawing is hidden from a screen reader. What it says is in the markup: a list of the four
  phases, each with its question and its symptom. The method table has a caption, column and row
  headers, and a text reading in every cell.
- Nothing moves on its own for more than five seconds without a control to stop it (WCAG 2.2.2): the
  three things that do, the hero's flight, the tower and the game's picture, each carry one.
- Handwriting in a sketch is 13px or more on a 320px phone and meets 4.5:1 on its paper. A sketch's meaning
  never rests on the pen's colour alone: the caption says it.
- "Copied" is announced through a polite live region; the rail marks the current section with `aria-current`.
- One `h1` per page; bands are labelled sections; the skip link, focus rings and breadcrumbs are kept.
- No page scrolls sideways at 375px.

## Key flows

Illustrative readers, used to test the pages. None of them is a real person.

**Meera, an engineering lead, on her phone between meetings.** She searched "AI-DLC vs BMAD" and
landed on the home page.
1. The first screen tells her it is a free manual for teams building with AI agents.
2. She scrolls once and recognises a line under Build & Prove: the score went up, and so did the complaints.
3. She scrolls again. The heading is her own question. She reads the bars, each beside its name: AIDD
   covers the build only, BMAD reaches Run & Learn only as extended here.
4. *The moment:* she reads the last row, what the spine adds that no method carries, and taps AI-DLC.

**Daniel, a product manager, from a link a colleague posted.**
1. Home: he reads one sentence and scrolls to the roles.
2. He finds his row: "a vibe → a number you can defend". His title travels with him to the next page.
3. The role page opens on his title, one line and the eight steps as a track, arriving in order.
4. He taps the first stop, then "The template" in the step's head.
5. *The moment:* he presses Copy on the pain register, and the button says so.

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
2. The first button on the game's first screen is "Start at Day 1". No role or mode has to be picked first.
3. Twenty seconds in, a call with a price on it. On Day 9 a choice from Day 6 comes back, quoted.
4. *The moment:* the verdict on Day 90, and the wish to play the other path.

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
- **1000px and under:** the spine band becomes the line first, then each phase with its question and its
  symptom. Under 600px the gate on the line is a rose bar before P2.
- **Under 760px:** the method table drops its one-liners and fits the screen, and the spine's row becomes
  a list under it.
- **Under 760px:** role rows become two lines.

## The second council: the inner pages, and motion

Asked whether to bring the other pages up to the front page's standard and how much motion to add, the
council (five advisors, five anonymous reviews) agreed on four things: take the text out of its boxes;
give long pages numbers and air; fix the words a stranger trips on before adding anything that moves;
and stop the site's own perpetual motion, which broke its duration rule and had no pause.

It split on how much motion. One advisor wanted every figure animated; three wanted almost none. The
resolution is the test now written in `DESIGN.md`: motion must answer the reader, say where they are, or
show a sequence. That shipped the page-to-page cross-fade, the ordered arrivals (the hero's words, a
role's steps, the method bars, the parts of a figure), the opening step and the copy tick. It refused
numbers that count up, cursor spotlights and glows, a circular theme reveal, hub cities on the globe,
text that slides in on reading pages, and a second drawing of the role route.

What the peer review added: nobody had defined "done". So there is a gate, `tools/accept.mjs`, that
checks five things on a page of every kind: nothing hidden without script; nothing hidden or running
under reduced motion; nothing still moving after four seconds except what follows the scroll or sits on a
page with a pause control; nothing left hidden once the page has been scrolled through; and on a phone no
sideways scroll and the title inside the first screen.

Not done, and why: stacked forms of the four-column tables on a phone (they scroll sideways inside their
own box, which is honest if not pretty); a legend defining "bar", "slice" and "gate" at first use on every
page (the lessons define them; the role pages still assume them); longer animated explanations of single
figures, which would each need a still frame, a start control and a pause.

## The third council: many names, one spine

The owner asked for a new home section: the names a reader has heard (agentic PDLC, agentic STLC, BMAD,
AIDD, AI-DLC) resolving into one roadmap, the SkyWays PDLC, with a picture that carries it and few words;
and a reason to care, tied to the three ways of taking the manual. Five advisors and five reviewers.

All five advisors said the same thing first: do not add a band. A second band about the method would
explain it twice, which the first council removed. Rebuild section two instead. They split on the
picture: three kept the table and added to it, two replaced it with strands running into one line.

The reviews settled it. Three findings changed the design. The table's own data undid its claim: AI-DLC
had the same bar as the SkyWays PDLC, so a sceptic would read "just follow AI-DLC". The lessons sort
these names by kind (a method says how to build; the lifecycle asks whether a product with a model in it
is right), and both the table and the strands sorted them by length. And at 1440 by 900 the question and
its answer never shared a screen. So the spine and a method now have different marks, the answer is the
figure's largest thing, and the heading and paragraph sit side by side to bring the whole band into one
screen.

Kept from the owner's brief: the names in the picture, one connected spine from idea to production and
back, the loop drawn as a loop, the three ways in as one sentence down the page, dark as the default.
One thing from the brief was reworded to what the manual can back: "the best parts of all of them" is in
the paragraph as "it keeps the part each method does best", which is the frameworks page's own claim
(merged, not stacked). Refused, with the reason: "agentic STLC" as a strand (the manual has no lesson on
it, so it is named in the link under the figure and answered in the terms lesson's FAQ, which points to
the QA lead's eight steps); a pinned scroll sequence; a three-doors band (a second routing device); a
list of audiences (the forward-deployed engineer got a row, everyone else the link to the nineteen
starting points).

## After the third council: the owner's correction

The strands figure shipped and the owner found it harder to read than the table it replaced, and asked
for both to be kept, each in a better form, with a reason for the visitor to care. So the page now has
the two pictures the third council's advisors had argued over, each doing one job. The spine lost its
strands and gained the reason it exists: under each phase, the line a team hears when that phase's
question went unasked, taken from the phase's own lesson. The table came back with its bars in the phase
hues, and with the reviews' finding kept: the SkyWays PDLC is not a fifth bar. Its row is words, what it
adds in each phase that no method carries. BMAD's Run & Learn cell is hollow: a stage this manual adds,
called extended BMAD and described in the BMAD lesson.

The first council's rule against explaining the method twice still stands in spirit: two pictures, two
different questions (why a spine, and where your method sits on it), and neither repeats the other's text.

## The fifth council: more motion, more pictures, and screens that explain themselves

The owner asked for motion graphics and stylised transitions "without overdoing", a coloured, smoother
globe, an aircraft that changes from P0 to P3, a loop that reads as a spiral, a funnel that shows the
SkyWays PDLC taking in the other methods, a plainer word than "hard gate", simpler sentences, hand-drawn
illustrations through the tutorial, a more colourful game whose days explain themselves, and top-bar
buttons that change with where the reader is. Five advisors and five reviewers.

**Where the council agreed.** Copy first: every animated label comes from the plain-words deck, because
animated jargon is still jargon. Design each moving thing from its still last frame. "Sign-off" for the
gate. The funnel borrows ideas, it does not swallow methods: each method's chip names the idea kept, the
chips stay in the last frame, and the caption says you still choose the method. In the game, rooms take
their owner's hue and the sky tells the phase; the recap quotes the earlier call today depends on.

**Where it clashed, and how it was settled.** The sceptic refused globe colour, the jet, a second button
and room colour; four reviewers overruled, because each was asked for in the owner's own words, and the
built hero showed a blue globe spends no phase hue. One pill or two in the top bar: one filled pill to the
twin of the page plus one quiet link, which gives the owner two without repeating a word already in the
bar. Sketches on the page colour or on paper: paper in both themes, four reviewers to one, because on the
dark page the black worker became a pale egg. The sketch's pens: the skill's red, orange and blue, three
to two, because on their own sheet they cannot be mistaken for phase hues. Path morph or cross-fade for the
aircraft: both, on one clock, since Safari takes the cross-fade.

**What every advisor missed, caught in review.** Nobody had looked at a phone: sketch labels were 10px
there, so handwriting now has a 13px floor that the build checks. A change no single frame shows teaches
nothing: each phase's label carries its aircraft, and reduced motion parks one at each phase. The first
sketches had the worker standing beside the picture: it now does the verb, at a third of the sheet. The
gate tested the build and never the pause: it now checks that one switch holds every looping animation.

**Refused, with the reason.** Night lights on the globe (decoration in P3's hue). Scroll-driven drawing
(half a figure if the reader stops). An animation library (the vocabulary of layout morphs, presence and
springs is here in CSS, the Web Animations API and view transitions). A quota of sketches per lesson
(quotas make filler). Moving daylight in the game. A lanyard to tell a person from the agent in sketches
(two pixels on a phone): the worker is a person, the model is a box with one eye.

## After the fifth council: the labs, and plain words in the game

The labs are new, at `/labs/`: one job of the airline's project done by hand, ten to fifteen minutes each,
on the same case as the game. One is open, Grow the spec, and three more are listed as being built; each
starts from the document the one before it filed. The drawer lists them under Play, and the home page's
simulator band has a quiet link to them.

Every lab keeps the same rules. It is a bench: the work on the left, one beat after another (assemble a
prompt from parts, run it, read the reply, mark what is wrong in it, make a call), and on the right the
document the work makes, which shows what a person decided and what a model guessed; on a phone the two sit
one above the other. Every reply is a recording, never a live model call: a real model's answer to the
exact prompt on the screen, with the model's name and the date on every reply, and the build refuses one
whose prompt is not what the parts join into. A gap in the document is written in capitals, NOT DECIDED
with an owner's name beside it, so a reviewer cannot mistake it for finished. Every call tells the player
what the book does and why, in two or three sentences, and a wrong call is told what it costs. Without
script the page reads as a document: each step, the prompt the book uses, every recording, and the
document as the book leaves it.

The game's words were rewritten for a newcomer. Every headline and context line names what it is
about (the AI assistant, six airline managers, the project team) and points at no one it has not named,
and every question says who is to act. Each day after the first says which earlier day and which document
it leans on, so "So far" quotes the call today depends on, which is often not the day before. The page's
heading says what the game is before its name. `GAME.md` has the fields.

Other changes went with them. Every local stylesheet and script is asked for by its content's version,
so a page never meets an old file from a browser's cache. Each sketch carries its own paint, so it
survives a missing stylesheet, and the sketches were cut from 98 to 77 by their own two tests of removal.
The hero is one canvas on one clock: a turning Earth, a fine spiral around it, and one aircraft climbing
it. The home page's bands no longer rise into place, and pages change without the cross-fade the second
council shipped. The workbench opens dark like the manual, shares its theme setting, and carries the way
back in its own top bar, so the frame's strip above it is gone. In the game, a question about a
colleague's plan now shows the evidence behind it, and costs the question whatever it shows.

## After the fifth council: four decisions, and labels that read

The leadership page is rebuilt on the role pages' pattern, under four rules. Its first screen says what it
is for: four decisions only you can make, twenty minutes, four questions for the next review. It has one
picture, the P0 to P3 line with a pin where each decision falls, and each decision's card carries one
control: a sort, a ladder or a calculator. Nothing was deleted: the sections it cut are folded at its foot
under their old ids, so an old link still lands on its words.

A label drawn in a hue is mixed toward the ink by a token in `base.css`, `--dg-text` in the figures and
`--mg-text` where a mental-model glyph's label sits on a heavier tint, so it reads at 4.5:1 or more and
the tints stay as they are.

## The ninth council: a simulator a newcomer can read

The owner had pressed "Start at Day 1" and seen nothing happen. As a newcomer they could not tell what
their days were, where they could start or where the milestones fell, and asked "where's a 10000 ft
view"; the building on the simulator page was not explained, "There is no mental map of that." They asked
for a role picker with meaning, the tutorial finished, every alignment fault fixed, more speed, and a
simulator as refined as the home page's day card, which they liked. Five advisors (an information
designer, a game designer, a product and usability advisor, an art director and a sceptic) and the
chair's verdict.

**Where the council agreed.** One picture for the ninety days, on the title: a line with the four phases,
the thirteen days and the four milestones (the sign-off before the build, the first test, the first bill,
the sponsor's slide), every stop a way in. The building explained in page text, not on the canvas: a
caption, a key of who works where and their days, and the three marks beside scraps of the drawing. The
roles as rows that say what each decides, which days are theirs and what they leave with, because the roles
are unequal: the architect makes six of the thirteen calls, the platform lead one. The home page's day card
as the one component the title and play share, borrowed exactly: its paper, its corner, its one inset, its
three sizes and its 48px answers. And "fix all alignment issues" read as a list of faults, each measured
and each held by a check, never as a sweep by eye.

**Where it clashed, and how it was settled.** Equal stops or a line drawn to time: the game designer kept
equal stops, since the player moves by decisions and a line true to the calendar puts Days 1 to 9 in 31px
on a phone; the information designer and the art director drew it to time, so that Days 1 to 4 stop looking
as long as Days 30 to 45. Each where it does its job: to time on the title, where the question is when
things happen, and equal cells in play, where the strip is the map of where you are and a line to scale has
no room. Where the Start button sits: the game designer put the line under it, the information designer put
it under the line, and the sceptic, finding the first screen already full, had the line replace the pitch.
Start sits at the line's foot beside its caption, so pointing at a stop changes both, and Day 1's card took
the pitch's place. The building under the fold at 1440: it ended 129px under the fold before the line went
above it, and it cannot fit under the line at a whole-pixel scale, so it still starts on the first screen
and ends under the fold. Accepted, because the council's own rule is a whole-pixel scale, never resampled.

**What review caught.** No paper had reproduced the dead button: Start worked in Chrome and in WebKit, and
the game designer asked which browser the owner had used. The sceptic's paper, read in after the first
verdict, did. The title calls nothing in the rules script, so Start is the first call into it, and before
the files were versioned that morning a new page script could meet a rules script ten minutes old, which
threw a TypeError, left the title, collapsed its heading and saved an empty run. Removing one function from
the rules reproduces it, so the playtest does that and expects the notice every press now gives. The review
of the lesson pass found the drawn boards still too tall: the hard gate's map runs to 89% of a 1440 by 900
screen against the council's cap of 70%, and its layout lives in the map engine, so it was left for a parcel
of its own.

**Refused, with the reason.** A guided tour or coach marks (Day 1 is the tutorial, and a key that stays on
the page teaches without stopping play). Tilt or parallax for the "3d-like" card (it reads as deep through
one long shadow and a room drawn in perspective, and tilt on the game's canvas breaks whole pixels).
Splitting `base.css` by kind of page (it saves 30 KB once and reopens the fault of a page meeting an old
stylesheet). A service worker (it turns ten minutes of stale cache into weeks).

**Performance, before and after.** The sceptic measured the site before the round: the bytes of
everything a page asks for, raw and gzipped, its first paint at 1440, and a phone on slow 4G with the
processor slowed four times. The after is the gate's seventeenth pass (gzip at level 9) and the playtest.
Where nothing was measured again, the before stands.

| What | Before the round | After |
| --- | --- | --- |
| Home page: raw, gzipped, first paint at 1440, phone | 382 KB, 172 KB, 0.27 to 0.61 s, 0.9 to 1.5 s | Stands |
| A lesson | 365 KB, 154 KB, 0.14 to 0.21 s, 1.3 to 1.4 s | Stands |
| The simulator | 537 KB, 206 KB, 0.11 s, 1.0 s (the title at 1.5 to 1.7 s) | Stands; the page's own HTML is 16.4 KB gzipped |
| The workbench | 1,949 KB, 833 KB, 0.52 to 0.58 s, largest paint at 5.6 s | Stands; the build keeps its bytes as they are |
| `base.css`, gzipped | 37.6 KB (163 KB raw) | 39.5 KB, under the gate's 40 KB |
| The game's three scripts, gzipped | 42.9 KB | 44.8 KB, under the gate's 45 KB |
| The game's loop with the building off the screen, on a phone | Drawing: 34% of the main thread with the processor slowed four times, against 5% paused | 0 frames until the building is scrolled to |
| The line for a reader without script, on a slow phone | Shown for 0.5 to 0.7 s before the title | Hidden from the first paint |
| The game's drawing | 7.3 frames a second at 1.3 to 2 ms each (5.4 to 9 ms with the processor slowed four times) | Stands |
| The title's relayout | 3 to 6 ms | Stands: nothing to chase |

`base.css` grew with the lessons' measure and margin column, and the game's scripts with this round's title
and day; both hold under the budgets the gate now enforces.

## Open items

- The workbench names a different set of methods on its opening screen (it adds Spec Kit and Kiro).
- "Agentic STLC" has an FAQ entry and no lesson. If it earns one, it is built from the QA lead's journey.
- The product manager's row and the QA lead's row both end on "a number you can defend".
- Three labs are listed as being built: the system prompt from the spec, proving the bar, and reviewing a
  change a coding agent wrote.
- The labs have one set of recordings, from one model on one date. A second model's replies to the same
  prompts would let a lab show what its debrief claims: the numbers a model invents differ, and the places
  it invents them do not.
- A role run cannot start from a later day: `sim.book` stops at the first day a colleague owns, so a role
  always starts at Day 1 and the role rows offer no "Or start at Day 45".
- 20 of the 44 lesson maps run over 70% of a 1440 by 900 screen, the evolution of the PDLC's at 103% and
  the hard gate's at 89%. Their layout lives in the map engine (`pages/maps.py`) and belongs to a parcel of
  its own.
- The home page's sample sketch keeps the old paper tone in the dark theme: the toned paper is set on the
  lesson pages only.
- help.openai.com refuses the session's proxy, so five OpenAI facts in the Tool guides stand as the
  research sheet had them, unchecked against their pages.

- The wiki on GitHub is a copy of `wiki/`. After a deploy, `wiki/sync.sh` pushes the copy; until it runs,
  the live wiki keeps its older links, which the home page forwards.
