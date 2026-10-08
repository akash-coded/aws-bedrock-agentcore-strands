---
name: SkyWays, the agentic manual
status: final
updated: 2026-10-03
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
SkyWays. So every page has to say where the reader is, and the home page has four jobs only: say what
this is, show that it is real, offer one way in, and, at its foot, say who can help apply it.

## Information architecture

```
Home                      what this is, how the methods fit, which to use, the roles, the tutorial,
                          the simulator, the library, the consultancy
├─ Tutorial   /learn/     55 lessons in eight tracks
├─ Roles                  product manager, solution architect, engineering lead, QA, DevOps,
│                         and the forward-deployed engineer's guide:
│  └─ /forward-deployed-engineer/   its hub, and frame/, deliver/ and evolve/, one page a stage
├─ Method     /method/    the four boards: phases, loops, roles by phase, what a model may draft
├─ Library                templates, prompts, mental models, frameworks, Tool guides, picture pack
├─ Leadership /protocol/  for whoever funds the work
├─ Simulator  /simulator/ Ninety Days: the worked case as a game
├─ Labs       /labs/      one job of the project by hand, with a real model's recorded replies
└─ Workbench  /workbench/ the earlier tool: episodes in depth, calculators, role playbooks
```

The top bar carries those five places and one slot that changes with where the reader is. The slot never
points at the page it is on. In the manual it is one pill, "Simulator". In a lesson the pill is "Play this
day" when the game has a day that lesson is the reading for, and a quiet link beside it jumps to the
lesson's own "Apply it in your role". In the game the pill is "Read the lesson" for the day on screen, and
the quiet link goes back to the manual. On the FDE guide's pages the quiet link is "The lesson", the field
guide. On a phone the pill stays and the quiet link is left to the drawer. The drawer (top left) still lists
every page by category and holds the search; on a phone it is the navigation.

The forward-deployed engineer's guide is a role in three stages, so it is four pages, not one: a hub that
draws the whole job in one picture and says what the role is, and one page for each stage, Frame the
engagement, Deliver the system and Evolve the relationship, each a focused read of four steps. The top bar's
Roles list and the drawer name it with the other roles; its stage pages are in the sitemap, the search finds
each step at its stage page, and `/templates/` and `/prompts/` end their role sections with one line to the
stage pages, where its 12 templates and 30 prompts live. A count of the whole manual counts the guide too: the
home page and the leadership page say 52 templates and 146 prompts, and the libraries' own heads give that
total and where each part is ("52 templates · 40 here, for 5 roles · 12 in the FDE guide", and 146 prompts, 116
here and 30 in the guide), the guide named and linked.

The home page, top to bottom:

1. **Hero.** The headline, two sentences that say what the site is, the three ways to take it and that
   it is free, two buttons (start the tutorial, play the simulator), one line of counts and the author,
   whose name links to the close. Beside them the flight: a dart round the Earth that becomes a drawing, a
   built airliner and a jet, stops at the sign-off before it is built, and comes to rest.
2. **How AI-DLC, BMAD and the rest fit together.** One map on the SkyWays PDLC: each of the five names a
   reader has heard is a shape as long as the phases it covers, with a handwritten note on who made it and
   when; all five meet in the build; under them, the four questions no method reaches.
3. **Which agentic methods should your team use?** The pair every team needs, then three yes-or-no
   questions, each adding one method. Nothing to decode, and nothing to choose for the answer to be there.
4. **Start from the job you do.** Seven rows: six roles, the forward-deployed engineer's guide among them,
   and the sponsor. The page's only routing device, with one quiet link to the tutorial's nineteen starting
   points for anyone not on the list.
5. **Learn to run agent projects one question at a time.** Four people from the game's team (Priya, Arjun,
   Sam and Maya) each ask one question and get the manual's answer in one sentence, beside a drawing of the
   worker; each card is a link to the lesson that answers it. Then one button to lesson one.
6. **Play a ninety-day AI project in fifteen minutes.** It says the game is for learning the method; one
   button, "Enter the simulation", a line with the number of decisions and the time a game takes, and a quiet
   link to the labs. Beside them one real day of the game as a card, labelled "Example day" and standing in
   perspective on a wide screen: Day 45, its room drawn in pixels, its headline, its context, its question
   and its three answers with their price in days, each of which opens that day in the game.
7. **Take the tools, templates and prompts with you.** Three tools first, each on the material of what it
   opens (the workbench, the tutorial, the simulator), then six shelves (templates, prompts, mental models,
   the Tool guides, the methods decoded, the picture pack). Every count is counted when the site is built.
8. **Work with the consultancy that wrote this manual.** SkyWays Consultancy's four offers, each ending in
   what a buyer leaves with, and one button, "Write to Akash Das", with "Say what you want to change, and by
   when." beside it.

Every band's heading stands alone. The three ways in are named once, in the hero's second sentence, and the
hero's buttons and the bands below run in the same order: lessons, then the game.

What left the home page went one click deeper, not away. The phase board, the eight loops, the role by
phase matrix and the delegation board are on `/method/` with their ids unchanged. Old links to
`/#pdlc`, `/#loops`, `/#by-role` and `/#delegation` are forwarded there by a script in the home page's
head, the same way the workbench's old `/#/…` routes are; `/#why` goes to the methods band and `/#method`
to the chooser. The lifecycle figure and the method table left in council 10: the funnel of four methods
into one point is the frameworks page's "How they merge", and the bars and their key are its plug board.
The task table ("about to write a spec", "about to launch") is on the tutorial's landing page as "Start
where you are".

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
- "Role", not "chair". "A fictional airline" on first mention of the case. "SkyWays Consultancy" in full,
  every time, so it is never taken for the airline; the consultancy never enters the game's fiction.
- No dashes in prose, no contrast staged for weight ("not X but Y"), no closing line that repeats the
  paragraph. The `humanizer` patterns are the checklist. On the home page the build enforces part of it: a
  dash, a brochure word ("seamless", "end-to-end", "solutions", "gamified" and the like) or an American
  spelling in what a reader meets stops the build.
- Counts are stated as numbers and computed at build time.

## Component patterns

| Pattern | Behaviour |
| --- | --- |
| Top bar lists (Roles, Library) | Each is a `<details>`: opens on click or Enter without script. Script closes the other one, and closes on Esc, on a click elsewhere and when the focus tabs out. The parent is marked when a child page is current. |
| Drawer | `<details>`, Esc and scrim close it, `/` opens it on the search box. Its contact form's first topic, "Work with SkyWays Consultancy", is chosen only by the close's button (`data-sw-open="consultancy"`), and a message sent with it is headed "[SkyWays Consultancy] enquiry from ...". Every other way in (the footer, the mail pill, `?contact`) opens it on "An idea or suggestion", as before, and puts that back if the close chose the consultancy and the reader did not change it. |
| Top bar slot | Chosen by the page when it is built, never by script, except inside the game, which points the pill at the lesson behind the day on screen. |
| Method map | One grid, three layouts: over 1180px the notes sit in a margin column with their arrows; from 761 to 1280px the author's line drops under the name; at 1180px and under each note moves into its shape; at 760px and under each method is its name, its note and a strip across the four columns. The shapes are a list of links, each read as its name, who made it and the phases it covers, built from the same data as the shape and the strip; the frame, the wash, the arrows and the ends are hidden from a screen reader. In print it keeps to one A4 page. |
| Chooser | Three fieldsets, each a legend and two radios. With nothing chosen both lines show, which is the whole rule; Yes hides No, and No hides Yes and greys the method's name. Plain CSS (`:has()`): no script, nothing stored, nothing sent. On paper, and in a browser without `:has()`, there are no toggles and both lines show. |
| Sketch | A `<figure>`: the drawing is one image with a description of the scene, and the caption under it is real text that makes the point alone. It is complete when the reader reaches it. It prints on white, never across a page break. |
| Role rows | The whole row is the link. Hover tints the row in the role's colour, past its column, and moves only the arrow. One row is not a role journey and says so in its counts: the sponsor's page. |
| People card | The whole card is one link, to the lesson that answers its question; a screen reader meets a picture, a name, a heading, an answer and one short link. Hover moves the arrow and darkens the foot's rule; focus rings the whole card. The build refuses an answer whose source sentence its lesson no longer says. |
| Day card | One real day of the game, its question and its answers as links: each answer is a link to that day in the game, and the note under them says each has a price in days, now or later, and that any of them opens the day in the game, where the reader makes the call. Plain links, so they work without script. Over 1000px it stands at a tilt and turns to face the reader on hover or on keyboard focus inside it, in 400ms, at once under reduced motion; flat at 1000px and under, and on paper. |
| Library cards | Each of the nine is one link. Flat at rest; hover moves the border to ink and lifts the card 3px in 250ms. In print every card's words are ink on paper, whatever its ground. |
| Close | One button. With script it opens the drawer on the consultancy's topic; without script it is a link to the repository's discussions page, and a reader who asks for a new tab gets that page in one. No form, no logo, no testimonial. |
| Folded how-to | Closed on arrival. Holds the audience, the use, the steps and the walkthrough button. |
| Section rail | On a wide screen the role pages, the leadership page, the libraries, the Tool guides' manuals and the FDE guide list their sections down the left and mark the one being read (`aria-current`): the last one whose top has passed the upper third of the window. A stage page of the FDE guide lists all twelve steps by stage, its own four marked as you read and the other eight linking their pages. On a narrow screen a role page relies on its step track, and the leadership page and the FDE hub fold the list under their titles. |
| Lesson guide | From 1280px wide, on the right of every lesson: the track, the lesson's place in it, the previous and next, the sections with the one being read marked by the same rule as a rail (with the first marked before any heading has passed), and the course folded, opened at the current lesson. On a short screen a long guide scrolls itself to keep the mark in view; the page never moves. Without script the list is there and nothing is marked. Under 1280px its two lists are two folds side by side under the meta line, closed under 1280px with script and open without it. |
| FDE framework | Twelve step links, each landing on the step's own block on its stage page; the stage heads link the stage pages. For a screen reader, an ordered list of three stages, each an ordered list of four links that read like "P0, step 1, Qualify: is this engagement worth taking? Discovery brief". Without script, under reduced motion and in print it is the same picture. |
| Role step | The step's head links to its template and its prompts; a tap opens the step if it is shut and lands on the block. "Expand all" sits beside the steps' heading. On a wide screen in a browser that can, a step opens to its height in 250ms; elsewhere it is simply open. The first step of each FDE stage page is open. |
| Copy | The button turns green, draws a tick and says "Copied"; a polite live region says so to a screen reader. It copies the text exactly as written; a code box wraps, so nothing is hidden off its side. |
| Pause control | A checkbox in the corner of the hero's stage and of the tower figure. Ticked, the flight, the globe and the tower hold still. It works without script for everything but the globe, which needs script to turn at all. |
| Next up | Templates, prompts, mental models, frameworks and the picture pack each end on one sentence, one button and one quiet link. The FDE stage pages end on the next stage, and Evolve's on Frame, "the next engagement", with the hub beside it. |
| Walkthrough | Never offered by a popup, and nothing about it is stored. Two ways in, on every screen width: "Show me around this page" in the drawer, shown only on a page that has a walkthrough, and "Show me around" in the folded how-to. Nothing floats over the page for it. The card highlights one element at a time and carries a plain label, "The walkthrough", the step count, the step's title and text, and Back and Next; it has no face and no name. Esc, the arrow keys and the close button work. On a lesson its first steps show the guide on a wide screen and the folds on a narrow one. |

## State patterns

- **No script, or the home page's own script missing:** the globe is a shaded disc with the line of names
  under it; every band is visible; the chooser shows both lines of every question; the close's button is a
  link to the repository's discussions page, and no page prints the contact address; a lesson's guide lists
  its sections with nothing marked, and its folds are open on a narrow screen; both top-bar lists open and
  close; the drawer works.
- **Reduced motion:** the hero draws its rest frame once (the four forms parked in their phases, each named)
  and shows no pause control, because there is nothing to pause; the day card keeps its tilt and turns at
  once; nothing fades in, and connectors do not move.
- **Paused:** the flight, the camera, the forms and the tag hold together, and the Earth stops turning.
- **At rest:** in its second round on a first visit (about 50 seconds in) the hero settles into its rest frame
  and draws nothing more; the pause control shows play; pressed, the flight goes on and does not rest again.
- **A second visit to the home page in one sitting:** no camera move and no spring-in: one round from Frame
  at the whole view, resting in the middle of Run & Learn about 21 seconds in.
- **A browser without scroll timelines or animatable `auto` height:** connectors are still and steps snap
  open. Nothing is missing, only the movement.
- **Off screen or hidden tab:** the globe stops drawing, and goes on from where it was.
- **Theme:** dark until the reader chooses light. The choice is kept in `localStorage` and applied before
  the page paints. Without script the page stays dark. The browser's own chrome follows the page. A sketch's
  paper is toned in the dark theme, on every page.
- **Theme change:** the globe re-reads its colours and redraws.
- **Print:** always the light tokens, whatever the screen shows. The method map keeps to one A4 page with its
  notes in ink; the chooser prints both lines; the day card is flat with no shadow and its pill prints as it
  shows; the close's button prints in ink with its address after it; a lesson's guide and folds do not print.
- **Old anchor on the home page:** `#pdlc`, `#loops`, `#by-role` and `#delegation` go to `/method/`; `#why`
  goes to the methods band and `#method` to the chooser; all before the page paints.
- **Old workbench route:** a link to `/simulator/#/…` or `/#/…` is forwarded to `/workbench/#/…` before
  the page paints. The game never uses a hash that begins with a slash.

## Interaction primitives

Motion has three permitted jobs and two classes; `DESIGN.md` states them. Transitions sit on the site's
scale (150, 250, 350, 400ms) with the one easing. Hover never carries information that focus or the page
itself does not. On a phone, buttons, navigation, list rows, the footer's button and the hero's pause control are at least 44px tall;
in a lesson every fold's whole closed box is its control, 44px or taller ("Show the answer", "What a strong
answer covers"). A link inside a sentence, and a checkbox in a self-check, keeps its text's height. The
leadership stepper's dots are the one exception: 24px apart, each with a 24px touch square, beside 44px Back
and Next. A line of links that wraps on a phone sets its rows 26px apart.

## Accessibility floor

- Text contrast is at least 4.5:1 in both themes, measured from the page's own pixels where a gradient or a
  picture sits behind it (`tools/ui.test.mjs`, at 1440, 1024, 390 and 320). Two things sit under it by
  design: the grey continuation of a display heading or a lesson's title, used only at 29px and above where
  it passes the 3:1 large-text bar, and a disabled button.
- A focus ring is never cut by the box it sits in. Where a box clips its overflow (a step's rounded corner, a
  code box, a picture card, a rail, the drawer's list), the ring is drawn 3px inside it; a ring on a code
  box takes the dark theme's slate in both themes, 3:1 or more on the code.
- The hero's stage is an image with one sentence: "A paper dart flies round the Earth through four phases
  and becomes, in turn, a drawing, a built airliner and a jet. It stops at a sign-off before it is built.
  Then it comes back to Frame, one level higher."
- The method map is a list of five links, each read as its name, who made it and the phases it covers; the
  questions no method reaches are an ordered list. The chooser's questions are fieldsets with legends; a
  radio reached by the keyboard rings its label. The FDE framework is three ordered lists of four links.
- Nothing moves on its own for more than five seconds without a control to stop it (WCAG 2.2.2): the
  three things that do, the hero's flight, the tower and the game's picture, each carry one, and the hero's
  flight also stops by itself after about 50 seconds.
- Handwriting in a sketch is 13px or more on a 320px phone and meets 4.5:1 on its paper; on the home page's
  map it is 16px or more. A sketch's meaning never rests on the pen's colour alone: the caption says it.
- "Copied" is announced through a polite live region; the rail and the lesson's guide mark the current
  section with `aria-current`.
- One `h1` per page; bands are labelled sections; the skip link, focus rings and breadcrumbs are kept. A
  breadcrumb is a link or the page itself: only the last is current, and on a phone the one before it is a
  link.
- No page scrolls sideways at 320px, and no table hides a column on a phone: a table that does not fit stacks,
  one block a row, each value under its column's name.

## Key flows

Illustrative readers, used to test the pages. None of them is a real person.

**Meera, an engineering lead, on her phone between meetings.** She searched "AI-DLC vs BMAD" and
landed on the home page.
1. The first screen tells her it is a free manual for teams building with AI agents.
2. She scrolls once. The map puts AI-DLC and BMAD on the same four phases and says who made each and when,
   and under Build & Prove she recognises a line: the score went up, and so did the complaints.
3. She scrolls again. The heading is her own question.
4. *The moment:* she answers three questions and reads her team's set: spec-driven development and AIDD,
   and BMAD, because an auditor reads their work. She taps BMAD.

**Helen, chief technology officer of an insurer, sent the link by her head of engineering.**
1. The first screen tells her it is a free manual for building software with AI agents, by Akash Das.
2. She reads the method map: five names she has heard, one frame, and a row no method reaches.
3. She stops at Maya's card: the bar comes from what a mistake costs.
4. *The moment:* at the foot she finds the consultancy that wrote it, and four offers that each end in
   something she can check. She writes to Akash Das with what she wants to change, and by when.

**Daniel, a product manager, from a link a colleague posted.**
1. Home: he reads one sentence and scrolls to the roles.
2. He finds his row: "a vibe → a number you can defend".
3. The role page opens on his title, one line and the eight steps as a track.
4. He taps the first stop, then "The template" in the step's head.
5. *The moment:* he presses Copy on the pain register, and the button says so.

**Priyanka, who funds an agent programme, sent straight to `/protocol/`.**
1. The top bar says SkyWays, the agentic manual, with Leadership marked.
2. The title says what the page is, the line under it says it is for her.
3. *The moment:* she reaches "the four decisions only you can make" and takes them to her review.

**Tomás, a QA lead, who searched for a golden set template and landed on `/templates/`.**
1. Title, one line, and the counts: "52 templates", 40 of them here for five roles.
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

- **Wide (over 1000px):** hero words left, scene right; the simulator band is two columns, its day card in
  perspective.
- **Tablet and phone:** the hero stacks, words first; the scene follows. The first phone screen holds the
  headline, the sentence, both buttons and the picture, which ends inside it; under the picture the meta line
  keeps the licence and the author, and the counts show only over 1000px. The hero's two buttons stay side by
  side on a phone: stacked, they pushed its picture below a 390 by 844 screen.
- **Under 860px:** the top bar keeps the mark, the simulator and the theme; the five places are in the
  drawer. On a phone it sits on the page's 20px column.
- **The method map:** over 1180px the notes sit in a margin column with their arrows; from 761 to 1280px the
  author's line drops under each name; at 1180px and under each note moves into its shape; at 760px and under
  each method is a row with a strip across the four columns, and the four questions stack.
- **The chooser:** four columns over 1000px, two by two from 601 to 1000px, one column at 600px and under;
  Yes and No are 46px tall at 820px and under.
- **The tutorial's people:** four across from 1181px, two by two from 601 to 1180px, one column at 600px and
  under, the picture on top.
- **The library:** three columns over 1000px; two from 561 to 1000px, each tool spanning both with its picture
  on the left; at 560px and under each tool keeps its picture in a 112px strip on top, and each shelf is a
  count and a name, two to a row.
- **The close:** four offers over 1000px, two from 601, one at 600px and under, where the panel is 20px inside.
- **At 900px and under:** role rows become two lines.
- **A lesson:** from 1280px the column on the page's left edge and the guide on the right; from 901 to 1279px
  one centred column with the guide's two lists as folds under the meta line; at 900px and under a phone's
  column, the body at 17px, with the same two folds.
- **The FDE framework:** on a phone the stages stack and each stage's four steps sit two by two, so across is
  still the order; the artefact line drops.
- **The libraries:** on a phone the templates and prompts pages fold their five roles under the title ("By
  role"), as the leadership page folds its sections.

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

## After the ninth council: the owner's eight answers

The owner answered the ninth council's open questions on 2 October. The labs stay at `/labs/`. A key for
Amazon Bedrock was added, and later any call there to any model was allowed; the account reaches models
from several makers, though not the newest from Anthropic, OpenAI or xAI. Of the content helper's six
wording questions, the three changes already made stay (the frameworks decoder's five "From" cells, the
workbench lesson's new title and the workbench line in the wiki's sidebar), and three are new: the
summary box keeps its "In short" label and loses the bold lead that said it again, a summary runs to
three sentences at most, and an empty template cell reads "none". The tall lesson maps and a role run
from a later day each get a parcel. The building at 1440 stays as the ninth council left it, starting on
the first screen and ending under the fold. The sketches are cut to about thirty by council 7's test,
with four pebbles and a rock as the home page's sample. The five OpenAI facts in the Tool guides that
could not be checked stand, with no action.

**Summaries.** All 55 summaries opened with a bold lead under a box already labelled "In short", and 52
of the leads said "in short" again. The leads are gone. In six lessons a lead carried a term the sentence
needed, and the term moved into the first sentence, so every summary still stands alone. The 29 that ran
to four to eight sentences now run to three, each rewritten from its lesson's body with the same facts,
numbers and bold terms, no sentence over 35 words and the median length unchanged. Two outside models
from different makers read every rewrite beside the old text; two of the losses they listed were real,
and both were restored after a check against the bodies. The build refuses a summary over three
sentences or one that opens with a bold lead, and on the lessons as they were it flags exactly the 29 and
the 55 leads. The guide no longer asks for 40 to 70 words: 20 summaries were already over 70, and the
owner's rule is about sentences. Every empty cell in the role templates reads "none": seven cells, and
the architect's list of allowed values.

**Sketches.** The sketches went from 77 in 48 lessons to 30, one each in 30 lessons. Each drawing was
read blind, then shown with its caption covered to three vision models from three makers, and each answer
was judged against the real caption. A sketch stayed when at least two of the three got its point, its
labels were the lesson's own nouns and numbers, and its lesson needed it: 20 were read by all three and 10
by two. Of the 47 cut, 14 were missed by all three, and 8 that all three read were cut anyway, 7 because
their lesson kept a stronger one and 1 because it sat in a question bank. Most misses came from a label
only the lesson explains: "thirteen points" read as story points, and "$2,000" on a high rock as an
opportunity. The 48 lesson pages that had sketches weigh 17% less gzipped, and 11 lessons read a minute
shorter.

**Maps.** Twenty of the 44 lesson maps ran over the ninth council's cap of 70% of a 1440 by 900 screen,
the evolution of the PDLC's at 928px. In most of them the label column set a band's height, and the cells
needed less. The engine now tightens only a map that is over, one step at a time, and draws the first
layout that fits, so the 24 that fitted, the leadership page's map and the wiki's 40 pictures are drawn as
before. Every step moves things or takes out air, and the smallest label stays 13.9px at 1440. The tallest
map is now 628px. The evolution of the PDLC and the evidence pack read as sequences, so they became cards
read left to right. Even as cards, evolution's six eras fit only without the second line in each cell, so
it lost twelve lines that its own steps already say. At 1024, 390 and 320 every map keeps its text version
and none is taller. The gate's eighteenth pass measures every lesson's map at 1440 by 900.

**A later start.** A role can start at its own later day: each role row's days are links, and a role
whose first call comes after Day 1 also offers "Or start at Day 45, your first call". The links are the
day numbers under the row's small line, at least 24px tall, because the architect's six marks on that
line sit 4 to 6px apart. The four rows with that link are 93px tall at 1440, where they were 64px, so
the link has a band of its own. The book that plays the earlier days uses only the moves a player has and
adds no rule. The game's three scripts are 44.95 KB gzipped, 52 bytes under their budget, after five fixed
sentences moved word for word into `days.json`; the simulator's own HTML is 16.8 KB gzipped, up from 16.4.
Three outside models from three makers reviewed the rule change. One ran out of room before it answered.
Of the faults the other two raised, one held, and it predates this round (see the open items); the rest
did not, because a day without options is handled and no plan is ever pending in a whole-team run.

**The lab's claim.** Grow the spec's debrief said that the numbers a model invents differ and the places
it invents them do not, and it now shows that. Two of its prompts went word for word to three models from
other makers: Kimi K3 (Moonshot AI), GLM-5 (Z.ai) and DeepSeek V3.2. Asked for the full PRD, all four put
a number on "much faster", "most" and "rare", and the numbers differ; all four left the refund cap to
Finance, the one gap the page gave an owner. Told where to stop, all four wrote NOT DECIDED at least once
in each of the five open fields, and one still let the assistant act alone on a refund up to $400, which
the closing line says. Each table cell quotes the words of its reply it is built from, and the build
holds it to them. Inline, the six replies would have taken the lab page near 40 KB against its 34 KB
hold, so they have a page of their own, 13.96 KB gzipped, which the fold reads in when first opened. The
lab page ends at 33.38 KB, 634 bytes under its hold.

**The role book's questions.** When a role starts late, the book plays the days before it. On a
colleague's day it plays as a player who knows the method: a sound plan stands, and one that is not is
questioned and the recommended option asked for, while a question is spare. The first book, never
shipped, questioned every such plan while questions lasted. A search over every move a player has, from each start the rows
offer, showed what that left: four late starts opened with no question left, and from none of them could
the player reach funded with conditions. A player who knows the method keeps a question for the
sponsor's slide, so the book does: when Day 90 is a colleague's, the last question is kept for it, and
those four starts now open with one. The product manager's book is unchanged, because Day 90 is theirs.
The rules test holds the property, not the table: from each of the 28 starts the rows offer, some line
must still end funded with conditions or better.

| Start | Best reachable, first book | Best reachable, as shipped | Played on by the book, first book | Played on by the book, as shipped |
| --- | --- | --- | --- | --- |
| Product manager, Day 15 | Funded | Funded | Funded, with conditions | Funded, with conditions |
| Product manager, Day 90 | Funded, with conditions | Funded, with conditions | Funded, with conditions | Funded, with conditions |
| Architect, Days 1 to 12 | Funded, by argument | Funded, by argument | Paused | Funded, with conditions |
| Architect, Day 20 | Funded | Funded | Paused | Funded, with conditions |
| Engineering lead, Day 30 | Funded, with conditions | Funded, with conditions | Paused | Funded, with conditions |
| Engineering lead, Day 60 | Paused | Funded, with conditions | Paused | Funded, with conditions |
| QA lead, Day 45 | Paused | Funded, with conditions | Stopped | Funded, with conditions |
| QA lead, Day 82 | Paused | Funded, with conditions | Stopped | Funded, with conditions |
| Platform lead, Day 75 | Stopped, whatever the player does | Funded, with conditions | Stopped | Funded, with conditions |
| Whole team, any day | | | Funded | Funded, unchanged |

All starts are on seed 0, as the rows' links are. The architect's starts from Days 1 to 12 take over five
minutes each to search, so they stand on an argument: the book's line from each passes through the Day 20
start, from which the search finds a funded ending.

**The newcomer test.** Three outside models from three makers were shown only the simulator's first
screen, at 1440 and at 390, and asked seven questions as a newcomer. All six answers understood the game,
and all six missed that the line's stops can be pressed: each read the caption's promise of a start at
any day and found no way to choose one. One also asked what "by the book" meant, one found the building's
caption at odds with its drawing (the days "end in the boardroom", which is at the top), and one could
not tell whether Day 1's card was a preview. Those became the title's four fixes. Shown the new build, all
three models, at both widths, said to press a day on the line to start later. What they still flagged:
four of the six answers asked what "the method" was, so after the test "the method's way" became "the
recommended way"; two found the line's smaller dots unexplained; and at 1440 one saw Day 1's question
with no answers, because they sit below the fold. Shown the role rows, all three would press "Or start at
Day 45, your first call" to play the QA lead late. Two said the rows' small timelines have no key, and two
found the sponsor row's "Every day, watched" and "2 questions" cryptic.

**Around the parcels.** All 266 pictures the wiki and the markdown twins embed were shot again from the
current build, because they dated from before the map engine's rewrite; 178 changed, and the thirty
sketches were shot for the first time, so each lesson's markdown twin shows its sketch as a picture. The
wiki's tutorial and course pages carry the new reading times. The home sample's source line wraps at 1024
with the longer lesson title, so its arrow is now held to the last word. The picture pack gained the thirty
sketches and the leadership page's map, each with its card and its image data, and its page grew from 29 to
37 KB gzipped. The gate's hold for that page was raised to 38 KB, the one hold raised on purpose; trimming
the image data each picture carries for search would bring it back down, and is the owner's call.

## Round eleven: late starts that show their work, a second lab, two more manuals

The owner answered on 2 October, in these words: "yes to wiki sync. late starts should already just assume
what would have done by then and present with evidence, artefacts and process recap. mental models wiki
pages: take the right call. For next parcels, take your best call and build." So the wiki gained a
workflow that seeds it from GitHub's side, a late start now assumes the work was done and shows it, and the
wiki's mental models page is generated from the site again. The round also opened a second lab, added two
tool manuals and fixed the four faults an outside design review agreed on.

**A late start that shows its work.** A late start in one role used to play a colleague's earlier day as
the colleague would: an unsound plan was questioned while questions lasted, and one question was kept for
Day 90. So the player could begin with fewer questions and a debt falling due, and six late starts could
reach funded with conditions at best. Now every day before the run's start is played the recommended way,
in one role as in the whole team, by one condition in the rules: a colleague's plan waits for the player
only from the run's start. The player begins with all four questions and nothing owed, and the rule for
keeping a question for Day 90 is gone. The whole-team book is proven unchanged across 56 histories, and
5,700 random runs from Day 1 give identical states under the old and new rules. All 42 starts the title's
line and the role rows offer can now reach Funded, and the rules test asserts it for each. Before the day
opens, a briefing recaps the calls with their people and prices, the documents with the day each was
filed, and where the run stands; one press opens the day, and the day can open the briefing again. Three
outside models from three makers read its first version as newcomers and all understood it. Two misread
the numbers, so trust now shows its number beside its pips and a sentence gives the spare days used. Maya's
first answer on Day 45 now ends at 836px of a 900px screen at 1440, where it ended at 969 under a debt's
news, and at 839 of 844 at 390. From about Day 20 the briefing is taller than a laptop's window, so its
button's row sticks to the window's foot: on Day 45 at 1440 the button ended at 1,140px and now sits at 818
to 900. The briefing took the game's three scripts from 44.95 to 45.97 KB gzipped after the savings
`GAME.md` lists, so their budget in the gate rose from 45 to 46 KB, the measured size rounded up to the next
half KB, with the reason beside the line. A late role start saved under the previous rules no longer
replays, and the game drops it.

**Lab 2: the system prompt from the spec.** The second lab is open, twelve minutes in P1, for the engineer
with the architect. It starts from the spec Lab 1 files, and the build holds its desk copy to that document
byte for byte. Sam, the engineer, asks a model for the assistant's system prompt, with or without a spec
line on every rule, marks the six rules that ask the model to keep a limit code should keep, and decides
where the limits live. Then Arjun's refund case runs with the draft as a real system prompt and the tools
as text: a note a partner desk typed into the booking says Finance approved a $1,240.00 refund. With the
limits in the prompt, the lab's own model, Claude Opus 4.6, called the refund tool for $1,240.00. With the
same prompt and the limits in the tools' signatures, it sent the refund to Finance and still told the
passenger it was approved, which is the lab's second call: what the prompt is still for. The lab files the
prompt, every rule ending in its spec line, seven limits moved into code across four tools, each with a
test, and two items still open, one with operations and one with compliance. Every reply was recorded
once, on 2 October 2026, through Amazon Bedrock. Three more models had the same case: Kimi K3 (Moonshot
AI), GLM-5 (Z.ai) and DeepSeek V3.2 (DeepSeek). Told the cap in words, all four called the refund tool for
$1,240.00. With the cap in the signatures none did: three sent the refund to Finance and one looked for a
flight first, and three of the four still took the note's word. The lab page is 18.5 KB gzipped and its
page of the six replies 7.8 KB.

**Two more tool manuals.** The Tool guides have four manuals. ChatGPT and Codex carries 36 dated facts and
Google AI Studio and Jules 32, in the form of the two Claude manuals. The 61 new facts, 33 about OpenAI's
tools and 28 about Google's, come from 37 pages opened on 2 October 2026, each fact with its address and
date in `tools.json`, and the build's checks pass on all 141. help.openai.com and openai.com refuse the
session's proxy, so the OpenAI facts come from learn.chatgpt.com and developers.openai.com. What no
official page could confirm was left out: that a shared project uses project-only memory, that a scheduled
task in a project cannot read the project's files, that deep research lets you edit its plan, that Work
replaced agent mode, custom GPTs' retirement, canvas's withdrawal, file and upload limits, Record and the
Meetings plugin, AI Studio's Compare mode as it is today, where AI Studio keeps saved prompts, which
languages Get code offers, and which model Jules uses. The five older help-centre facts stand as the owner
decided, and the new manual does not use them. Two outside models from two makers read every new fact
against its quoted sentence; eleven whose wording had drifted from their page were corrected after the page
was read again. Sixteen of the table's twenty-one cells now link a manual, and each new page is under 11 KB
gzipped. ChatGPT and Codex teaches one AGENTS.md for every agent: Codex reads it, Jules looks for it at
the repository's root, and Claude Code reads it when there is no CLAUDE.md or CLAUDE.local.md. Google AI
Studio and Jules has the team test with made-up cases until the account is on Google's paid terms.

**The mental models page.** The wiki's page had drifted from the site: the models had been renamed, their
words revised and a link had died. `site/export_models.py` could not be run, because it would have deleted
the page's hand-written sections, "Where each one bites" with its picture and "The three that get
resisted". The call was to keep the site canonical and give those words a source of their own,
`site/content/library/mental-models-wiki.md`, from which the generator puts the region back byte for byte,
2,608 bytes in 34 lines. The picture is drawn with the same helper the journey pages use. The site's twelve
names and words win, and each renamed model keeps its old name as an anchor, so all 17 anchors of the old
page still resolve and the six links in five lessons still land. The page now opens with the repository's
generated-page marker, the generator refuses rather than drop words, and `--check` says whether the page is
current. Regenerated, the page lost 22 of its 25 em dashes (the three left are in the hand-written words),
says "manual" where it said "playbook", and its dead link now leads to the workbench's bar calculator. Two
sentences on the site's models page that an earlier dash sweep had broken were mended first, so the wiki
copies them whole.

**Four faults an outside review agreed on.** Three vision models from three makers reviewed six lesson
screens as senior designers. Four faults were named by at least two of them and confirmed by measurement,
and exactly those were fixed. The tutorial rail's current lesson started its highlight at 104px at 1440,
10px left of its track heading at 114; every row's box now starts on the heading's edge. The theme
button's "◐" was set in a font without the glyph, so a fallback drew a small dot; it is now drawn in SVG on
the menu icon's rule, in the header and in the workbench's top bar. Lesson tables set money, counts and
percentages left with ragged edges; fourteen numeric columns in six lessons now read down their right edge
in figures of one width. The tightened funnels set "yes" as plain text beside "no" pills; both are pills
now, and no funnel grew taller. Of the 266 pictures shot again from the new build, exactly the six images
of those funnels changed, and only they were replaced. `base.css` grew by 164 bytes to 39.66 KB gzipped,
350 bytes under its 40 KB budget. Shown the same screens after the fix, two of the three found all four
fixed and nothing worse; the third called the rail not fixed in a close-up, which the measurement settles.

**The wiki, synced from GitHub's side.** `wiki/sync.sh` could not run from a cloud session: the wiki is a
git repository of its own, and the session's git proxy will not carry a credential for it. A workflow,
`.github/workflows/wiki-sync.yml`, runs the same script unchanged with GitHub's own token, as the Pulse
workflow does for the scoreboard. It runs only when started by hand (Actions, Wiki sync, Run workflow),
because a sync overwrites the wiki, and the script still refuses to run over a page someone edited in the
browser since the last seed. It ran twice on 2 October 2026 and pushed 82 pages each time: once with the
workflow's own commit, and again after the mental models page was regenerated. The live wiki now matches
`wiki/`.

## Round twelve: council 10, the home page, the lessons and the FDE guide

On 2 October the owner asked for a home page that shows what changes from phase to phase (a rocket entering
each phase and shedding a stage, leaving the atmosphere at the sign-off), a Venn of AI-DLC, BMAD,
spec-driven development, AIDD and the agentic SDLC coming together in the SkyWays PDLC, four people with their
own questions in place of the track list, a three by three library with the workbench, the simulator and the
tutorial as flagships, a call to SkyWays Consultancy at the foot, lesson pages that look finished, and a full
guide for the forward-deployed engineer built on Frame, Deliver and Evolve. Council 10 sat in two rooms. The
home room (a motion designer, an information designer, a narrative strategist and a sceptic) ruled on the home
page; a second room ruled on the lessons, the FDE guide and an audit of the site's parts. Each chair wrote a
verdict, and each verdict's parcels were built by their own builders. The owner answered both verdicts'
questions with their defaults: the lesson guide on the right; the libraries keep their byte holds, with one
line pointing to the FDE stage pages; no consultancy line on the FDE guide; "Check yourself" next round; the
map's credit "SkyWays PDLC, by Akash Das, SkyWays Consultancy, 2026"; the four offers in the verdict's order;
no proof line; and the drawer as it is, the discussions page without script, and no delivery line.

**Room first.** `base.css`, which every page loads, stood at 39.66 KB gzipped under a 40 KB ceiling, and a
quarter of it was comments. The build now ships every stylesheet without them (`build.py`, `lean()`), which
took the file to 29.28 KB as shipped with the same rules, and the ceiling came down to 32 KB so the room is
kept for work. Both rooms' parts were then built inside it: it ships at 30.54 KB (31,272 bytes) at the round's end.

**The home page: what was decided.** The page runs in eight bands, and its headings read as one sentence of
intent: what it is, how the methods fit, which to use, start, learn, play, take, get help. The hero is staged
like a launch rather than drawn as a rocket (below). The methods band is a map, not a Venn. The chooser answers
its own question in words. The roles band stays, without "eight" in its sentence, because the FDE guide has
twelve steps. The tutorial moved above the simulator and became four people from the game's team. The
simulator band keeps its heading, says plainly that it is a game for learning, labels its day card "Example
day" and stands it in perspective: the "3D pop-out" the owner remembered from council 9's tilted frame. The
library is three tools and six shelves, and the page closes on SkyWays Consultancy. Every count on the page is
computed, and the build refuses a dash, a brochure word or an American spelling in what a reader meets there.

**Clashes, and how they were settled.**
- *A rocket.* No seat argued for one. The motion designer built a launch first: the climb out of the atmosphere
  curled into a hook at the Earth's edge and read as a dive. Shedding stages also teaches the opposite of the
  method, since at a gate nothing is thrown away and each phase leaves a record the next is held to, and a
  rocket goes one way while the method loops. All four of the owner's points survive in the staged flight: a
  boundary nobody can miss, the sign-off as the dramatic moment, a thing that gets better and ends up shipped,
  and a start close to the Earth that pulls back. "Shed one thing" is kept the right way round: each form
  leaves a trace on the path.
- *A Venn.* Its middle would say the SkyWays PDLC is what every method shares, the reverse of the manual's own
  claim, and five sets make 31 regions no source describes. What the methods share is phases, and phases have
  an order a set loses. So each method is a shape as long as the phases it covers, inside one frame, and every
  overlap is true: all five meet in the build. Every element the owner named is kept, the handwritten notes on
  who made each and when among them. A zoomed P0 to P3 panel beside it would have drawn the phases twice.
- *The order of the tutorial and the simulator.* The owner described the simulator first. The tutorial comes
  first: the hero's sentence and buttons already put lessons before the game, it teaches the model before the
  practice (Maya's 80% bar one band before the Day 45 card that tests it), and two of three outside readers,
  asked only whether anything was out of order, proposed the move unprompted.
- *Tilt.* The ninth council refused tilt "on the game's canvas" because it breaks whole pixels. The day card is
  a still picture in a card; at its angles the cost is one stepped diagonal and the type stays sharp. The game's
  own canvas, and its own Day 1 card, are never tilted.
- *The library's order.* Workbench, tutorial, simulator: the workbench is the one tool the page has not shown,
  and its calculator carries Maya's numbers, so the 80% bar runs through three bands.
- *Heights.* The sceptic wanted one drawing on a phone and the close inside one phone screen. The owner asked
  for the four workers, and two sketches side by side would put the handwriting under 13px; the four offers
  need about 1,300px at 390 to stay whole.
- *The hero's budget.* The sceptic showed the script is about a fifth of a frame's cost and today's hero kept a
  slowed phone's main thread busy for 69.8 of 70 seconds. So the rest became a condition of shipping, with a
  sixty-frame cap and four drawing rules.

**Refused, on the home page.** A rocket, an atmosphere shell, plumes and particles; WebGL, an animation
library, video or a second canvas; a camera that moves every round or follows the scroll; a Venn, the SkyWays
PDLC as a sixth shape, phase colours on the methods, and motion on the map; a score or a stored answer in the
chooser; a fifth person (the FDE has its row in the roles band); "gamified" in the copy; badges, a 4 by 4 grid,
tilt on the library cards, raster screenshots; logos, testimonials, counts of clients, a popup or a sticky
"Book a call", and the owner's service words hidden in structured data; inline style blocks, a home-only
stylesheet, and a base.css ceiling above 32 KB.

**The lessons.** Measured, the "50%" the owner saw was true both ways: a 248px rail of 64 links left of a
508px column of 16.5px text, a 300px margin column that held something for 8 to 15% of a lesson's height,
nothing right of the text on 60% of its rows, a right edge that jumped twelve times, and 54 of 55 titles in
three lines. A lesson now reads in one column from the page's left edge, text at 584px and 19px, pictures to
944px, and a 240px guide on the right holds navigation and nothing else; the sketches came into the text at its
width (handwriting from 14.5px to about 28px), and "Try it" sits where the lesson reaches it. The title is the
whole search title in two lines with its second half in grey, and six gaps replaced eleven. The hard gate grew
from 7,614 to 8,601px at 1440; its reading time is unchanged. Ten lessons gained a picture already drawn, each
after the sentence it shows, and three new figures draw what three lessons' prose could not, from numbers
written into those lessons first: a drift of thirteen points in eight weeks that never trips a weekly alarm
and trips the baseline alarm in week 5, a $2,000 refund through five claimed defences, and four ways back from
40 seconds to 11 minutes. Lessons whose only picture was their opener went from 18 to 7: the exercise sheet,
four interview banks, the interview guide and the tutorial's own manual. Refused: text across the whole page
(107 characters a line), one centred column (scored lowest of seven layouts, for its empty flanks), a repaired
margin column (a 944px map scrolling under a sticky 300px column collides with it), a quota of pictures,
motion on a lesson, and the guide's bars as links (14px targets). "Check yourself" in every lesson waits for
the next round.

**The forward-deployed engineer's guide.** The FDE became the sixth role, as a guide of four pages: a hub and one
page for each stage. Each stage asks P0 to P3 of its own object (the engagement, the system, the relationship), so
the job is twelve steps, twelve artefacts and three signatures: the go decision, signed by the client's sponsor;
the handover, signed by the person who will run it; the next frame or a clean close. One correction to the owner:
"an FDE is a whole team in one person" ships as "some weeks you are the whole team", because at scale the work is
a pair, and Anthropic, Palantir, Databricks and Ramp say so in their postings. Every claim about the profession is
a dated record (31 sources and 54 quotations, 28 read on 2 October 2026 and three on the 3rd), and a page never types a
quotation. The case runs on: Frame is the three weeks before day 1, Deliver is days 1 to 97 with the canon
unchanged beside "Your move", and Evolve is the guide's own. The joins: the top bar, the drawer and the home
page's roles band list it; the search finds every step at its stage page; `llms.txt` lists it; `/templates/` and
`/prompts/` point to its stage pages; *What is an FDE?*, the field guide lesson and the FDE interview bank teach
the three stages, and the first gained the 31st sketch, a hat stand. Refused: one page of about 60 KB, a spiral, a
rocket or any motion in the framework, a colour for each stage or dimmed rows on a stage page, a new named
character, the FDE's 12 templates and 30 prompts in full on the libraries (both stand near their holds), and
copies of the other roles' steps (the hats table links to them).

**The parts.** The audit measured 24 faults across the site and put each in a parcel by file; six were moot
under the redesigns. Focus rings are drawn inside the boxes that clip them, rings on code boxes read 3:1, the
lab's "(empty)" reads, the toned sketch paper is on every dark page, and every phone control is 44px tall, the
stepper's dots excepted at 24px apart. Prompts and templates wrap instead of hiding half their lines on a phone
(116 of 116 prompts scrolled sideways at 390), role rows and rails sit on their column, and the top bar sits on
the page's 20px column on a phone. The audit had found eight corner radii for one kind of box, five buttons off
any scale, inner h2s in five sizes and two weights, and capitals with wide tracking; now three corners are three
tokens, buttons come in three heights (36, 43 and 51px at 1440), an inner page has one h2 scale, and no text is
set in capitals. The light amber reads 4.69:1 on a calculator's panel, where it read 4.39. Every landing page
opens on one page head from one helper, with one eyebrow in the page's accent; 15 of 90 pages had marked two
crumbs as the page, and a category in the crumbs is now a link, so the one crumb a phone shows leads back; and
tables that hid columns on a phone (the leadership page's eight ran 212 to 364px past their box at 390) stack.
The libraries' heads now count the whole manual and say where the FDE guide's part is. Two choices went against
the audit's letter: the hero's two buttons stay side by side on a phone, because stacked they pushed its
picture below a 390 by 844 screen, and the game keeps its own buttons and chips. The workbench meets the same
floor in its own file: no label under 11px (4.6px on a phone before), a sign-off at 6.7:1 (2.88), the control
tower's links at 12.3:1 (2.86), every focus ring 3:1 or more (1.6 and 1.9), and Menu on screen at 320px with
44px controls. `tools/ui.test.mjs` keeps the audit's measurer as a test: seventeen checks over 21 page states,
four widths and both themes.

**Outside readers.** Models from other makers, through Amazon Bedrock, read the built parts cold with the
councils' own questions. On the method map, in three runs, at least two of three answered each of five factual
questions; from the chooser, all three answered both team scenarios, and none needed a key. On the people band
two of three named a specific thing they had learned. On the close all three stated every offer's output, none
quoted a phrase the council had cut, and all three said one named client with one number would most make them
write: the owner's to give. Shown six stills of the staged hero, two of three described the aircraft changing
form and all three stated the sign-off's rule, where two of three could not see today's aircraft change at
all. Three decoded the FDE framework cold, the hat stand's point came through for two makers with its caption
covered, and two stated each new figure's point; their notes changed three labels.

**The gate.** The acceptance gate grew with the round and has twenty passes. Pass 18 now holds every lesson's
frame and type, not only its map: the measure, one left edge and two right ones, the guide on screen marking the
section being read, two-line titles with their grey at 3:1 or more, the six gaps, and at 390 no table that
scrolls and no fold under 44px. Pass 19 holds the home page: the home verdict's order, eyebrows and headings,
its height (8,700px at most at 1440, 13,200px at 390), a first visit that asks for nothing the byte count leaves
out, then each band's own checks. Pass 20 holds the FDE guide's four pages at four widths in both themes. Pass 13
was rewritten to see the hero's words, its fit and its whole cost, not only its script: thirteen checks, every
moment read from the hero's own times, and the rest held as a condition of shipping (a first visit still by its
rest time plus two seconds, a later one within 30 seconds). On 3 October the machine under the gate changed and
the same code lost a third of its frames, so an absolute floor measured the host, not the hero. The hero's cost
is now judged against a frozen copy of the hero before the round (`tools/reference/hero-2026-10-02.js`), served
in its place in the same run; in a gate that shares the machine that check is a screen, and pass 13 alone under
the exclusive lock is the judge. Pass 17 holds `theme/hero.js` under 10 KB, `frame/frame.js` (every page loads
it) under 6 KB, the home page's HTML under 21 KB with no `<style>` block, everything a first visit to the home
page asks for under 176 KB, `fde.css` under 2 KB and the FDE hub under 22 KB, beside its older budgets. Passes 1
to 4 and 8 fail when one of the home page's parts is no longer found there, so a renamed class cannot leave
nothing checked, and pass 1 reads the close's button without script. Each new check was shown to fail on a build
with its fault put in. CI now runs the role builder's tests before every build, and the tools that drive Chrome,
but for `ui.test.mjs`, ask the system for a free port, so two runs never drive one browser.

**Fixed forward.** A last parcel took the round's reports' loose ends. AIDDLC's seven phases and BMAD's unit,
six documents (its own reference installs five agents in its current release, where "twelve personas" came from
an older one), now agree in every lesson, map, library entry and role page. The leadership page sends people to
the FDE guide's twelve steps and counts five delivery roles and the FDE. The QA lead's line is its own ("from
'it works' to proof that it works") everywhere but its social card. The start page's box opens with its answer.
The picture pack names the three new figures. Two sketches' labels clear 13px at 320. The library's room keeps
its screen whole from 561 to 1000px, and its shelf names start level on a small phone. The contact relay files a
consultancy enquiry as one. The workbench's menu sheet, role tabs and rows and footer links are 44px on a phone
with their rings whole, and its loop map, gate pictures and concept map read 4.5:1. The Mental Models picture
names the twelve models as the site does, and the stale copy of the workbench is gone.

**Reviewed, then fixed.** After the merge, four reviewers, four seats of one model, read the lessons, the home
page, the FDE guide and the site's facts cold, and a sceptic on the same model tried to refute each finding: 35
were confirmed and 7 refuted. The 35 were fixed in two parcels. The FDE guide's statement of work carries who
keeps what is built (section 8) and the support period after handover (section 9), the clauses steps 8, 10 and
11 rely on; the career table's university row quotes Palantir's new-graduate posting, recorded and dated (31
sources and 54 quotations now); the field guide lesson walks Deliver as eight moves and says which guide step
each belongs to, with the lead-time items back on day one; two worked examples, four source records and two
lessons' citations were corrected. In the lessons, pictures and numbers now say what the words say: P0 Frame's
autonomy table replaced a figure that contradicted its veto window, lesson one opens on its own map and sends the
boards to `/method/`, the postmortem's layers read "a request" where they read "absent from the code", a
quarter's drift is twenty-six points (two a week for thirteen weeks), the QA lead's level alert is over 6pp
against the frozen baseline, and the methods and loops boards are drawn with larger type in a lesson. On the home
page the day card's note says each answer has a price in days, a wrapped link keeps its arrow after its last
word, a route that does not fit breaks between its two ends, the close's four offers start their "You leave
with" level, and the hero's pause control is 44px on a phone. The templates page's filled-in register carries the
case's pain line word for word, the search index and `llms.txt` say the FDE's artefacts are on the guide's stage
pages, and the loop count is right everywhere: two loops run backwards (cost P3 to P1, incident P3 to P0) and
three have nobody waiting, governance among them.

**The last pass.** Five final readers, each on one part of the site, fixed what they found rather than
reporting it. On the FDE guide, step 5 now opens the pattern log that step 10 relies on, the handover pack
gives the desk's overrides an owner, and the field guide lesson's map draws the shadow run in Build and
Prove, as step 7 does. The social cards were shot again from the content: the home card counts six roles,
55 lessons, 52 templates and 146 prompts, the library cards say where their counts live, and the guide, the
simulator, the workbench, the labs, the tool guides and the picture pack each have a card of their own, 82
in all, set in the site's own fonts. The drawer's slide-in, declared on the closed menu, had kept Chrome
drawing a frame on every tick after the hero rested; it now belongs to the open menu, so a resting page
draws nothing, and a later visit's seventy seconds on a slowed phone cost 22.6 s of main thread against
24.3 s. The hero's pause control is 44px at every width, the roles band reads the leadership page's
reading time from the built page (25 minutes), the engineering lead's line is the same plain line
everywhere, the method page counts five delivery roles, and three lessons' summaries, pictures and FAQ say
what their steps say.

**Bytes.** Sketch paths are written from the point before: the 31 pages with a sketch went from 547.6 to 511.1
KB gzipped, 1.18 KB a page, and every sketch draws the same pixels. The home page's HTML grew from 13.0 to 19.1
KB with its four drawings, the map, the chooser, the library and the close, under the 21 KB it is held to, and
no longer asks for `engine.js`; everything a first visit to it asks for, scrolled to the end, went from 177.3 to
174.0 KB. The page is 8,550px tall at 1440 (7,085 before) and 12,914px at 390 (9,742). The hero's script went
from 7.1 to 9.9 KB, under its 10 KB budget, and it stops drawing once it rests. The FDE hub is 17.8 KB, and
Frame 22.4, Deliver 23.5 and Evolve 21.5 KB. The picture pack is 37.88 KB of its 38 KB hold. The sizes are the
round's last build read with node's zlib at level 9, a KB 1,024 bytes.

**Performance, before and after.** Measured with `tools/perf.mjs` on 3bdb076, the last commit before the round,
and b91e196, the round's pages as merged before the content review's fixes and this record, on one machine, each
build served as GitHub Pages serves it, before and after taking turns. The machine was slower than when the
council set its bars (the old hero took 1.17 ms of script a frame unthrottled, where it took 0.92 when the
council measured it), so no bar is an absolute number: every bar is judged against the build before the round,
measured on the same machine in the same run, at the council's ratio, with the absolute numbers beside it. Every
bar was met, the two minute bars by 0.3 and 0.2 seconds. The table is the sheet's own, before 3bdb076 and after
b91e196, Chrome 154 on four cores.

| What | Before | After | The bar | Met |
| --- | --- | --- | --- | --- |
| The home page's HTML, gzipped | 13.0 KB | 19.0 KB (1.46 of before) | under 21 KB | met |
| A first visit to the home page, scrolled to the end, at 1440 and at 390: everything it asks for, gzipped (raw) | 177.3 and 177.2 KB (394.0 KB raw; 15 and 14 files) | 174.0 and 173.8 KB (389.8 KB raw; 15 and 14 files; 0.98 of before) | under 176 KB | met |
| A lesson: a first visit at 1440, scrolled to the end, gzipped (raw) | 156.3 KB (374.4 KB raw), 12 files | 147.9 KB (362.9 KB raw), 12 files (0.95 of before) | information |  |
| The simulator: a first visit at 1440, scrolled to the end, gzipped (raw) | 216.9 KB (579.4 KB raw), 15 files | 203.5 KB (550.7 KB raw), 15 files (0.94 of before) | information |  |
| The workbench: a first visit at 1440, scrolled to the end, gzipped (raw) | 832.1 KB (1,949.8 KB raw), 4 files | 833.2 KB (1,953.8 KB raw), 4 files (1.00 of before) | information |  |
| The FDE guide: a first visit at 1440, scrolled to the end, gzipped (raw) | 172.8 KB (394.4 KB raw), 13 files, /learn/ai-dlc-for-forward-deployed-engineers/ | 165.7 KB (376.7 KB raw), 13 files (0.96 of before) | information |  |
| A role page: a first visit at 1440, scrolled to the end, gzipped (raw) | 174.5 KB (438.1 KB raw), 11 files | 165.7 KB (420.4 KB raw), 11 files (0.95 of before) | information |  |
| A lab: a first visit at 1440, scrolled to the end, gzipped (raw) | 187.0 KB (482.4 KB raw), 13 files | 177.3 KB (462.0 KB raw), 13 files (0.95 of before) | information |  |
| First paint, then the hero's first frame, 1440 x 900, full speed: medians of 5 | 0.32 s (0.28 to 0.33), then 0.21 s | 0.31 s (0.28 to 0.35; 0.97 of before), then 0.21 s | information |  |
| Largest paint and its element, 1440 x 900, full speed: median of 5 | 0.32 s (0.28 to 0.33), the h1 in 5 of 5 | 0.31 s (0.28 to 0.35; -0.01 s, 0.97 of before), the h1 in 5 of 5 | the h1 | met |
| First paint, then the hero's first frame, 390 x 844 at 3x, council 9's slow 4G, processor 4x: medians of 5 | 1.34 s (0.96 to 1.42), then 1.55 s | 1.14 s (0.87 to 1.31; 0.85 of before), then 1.54 s | information |  |
| Largest paint and its element, 390 x 844 at 3x, council 9's slow 4G, processor 4x: median of 5 | 1.34 s (1.16 to 1.42), the h1 in 5 of 5 | 1.26 s (1.14 to 1.31; -0.08 s, 0.94 of before), the h1 in 5 of 5 | the h1 | met |
| First paint, then the hero's first frame, 390 x 844 at 3x, DevTools' Slow 4G, processor 4x: medians of 5 | 2.08 s (1.84 to 2.26), then 2.47 s | 1.95 s (1.77 to 2.01; 0.94 of before), then 2.61 s | information |  |
| Largest paint and its element, 390 x 844 at 3x, DevTools' Slow 4G, processor 4x: median of 5 | 2.08 s (2.03 to 2.26), the h1 in 5 of 5 | 2.01 s (1.95 to 2.26; -0.08 s, 0.96 of before), the h1 in 5 of 5 | the h1, and no later than before's median plus 0.15 s (2.23 s) | met |
| The hero at 1280 x 800, processor 4x, the first seconds: script a frame, frames in 3 s (a second), the worst gap and the worst tap (3 loads) | 6.59 ms, 96 (32), 83 ms, 41 ms | 4.91 ms (0.74 of before), 101 (34; 1.06 of before), 83 ms, 39 ms | information: pass 13 holds the hero |  |
| The hero at 1280 x 800, processor 4x, steady flight: script a frame, frames in 3 s (a second), the worst gap and the worst tap (3 loads) | 7.13 ms, 89 (30), 50 ms, 51 ms | 7.21 ms (1.01 of before), 96 (32; 1.07 of before), 50 ms, 35 ms | information: pass 13 holds the hero |  |
| The hero at 390 x 844 at 3x, processor 4x, the first seconds: script a frame, frames in 3 s (a second), the worst gap and the worst tap (3 loads) | 7.08 ms, 69 (23), 83 ms, 67 ms | 5.01 ms (0.71 of before), 78 (26; 1.14 of before), 83 ms, 54 ms | information: pass 13 holds the hero |  |
| The hero at 390 x 844 at 3x, processor 4x, steady flight: script a frame, frames in 3 s (a second), the worst gap and the worst tap (3 loads) | 7.17 ms, 68 (23), 67 ms, 55 ms | 7.29 ms (1.02 of before), 71 (24; 1.04 of before), 67 ms, 48 ms | information: pass 13 holds the hero |  |
| 70 seconds on a phone's first screen (390 x 844 at 3x, processor 4x), a first visit: main-thread time, and the hero's frames | 69.4 s; 1,992 frames, still drawing at the end | 51.4 s (0.740 of before); 1,384 frames, the last at 51 s | at most 0.745 of before's main-thread time (51.7 s) | met |
| 70 seconds on a phone's first screen (390 x 844 at 3x, processor 4x), a later visit: main-thread time, and the hero's frames | 69.0 s; 2,155 frames, still drawing at the end | 24.5 s (0.355 of before); 509 frames, the last at 23 s | at most 0.358 of before's main-thread time (24.7 s) | met |
| A flick down the home page at 390 x 844 at 3x, processor 4x, 5 flicks: the median and the worst gap between frames, frames over 50 ms, the most layout shift | 16.7 ms, 66.7 ms, 4 of 1,060, 0.000 | 16.7 ms, 83.4 ms, 4 of 1,446, 0.000 | before misses 16.7 ms and 50 ms here too, so after is held to before: a median no longer, and no more frames over 50 ms a flick; layout shift at most 0.05 | met |
| The same flicks at 390 x 844 at 3x, once the hero has left the screen: the median and the worst gap, frames over 50 ms | 16.7 ms, 66.6 ms, 1 of 1,005 | 16.7 ms, 50.1 ms, 0 of 1,391 | before misses 16.7 ms and 50 ms here too, so after is held to before: a median no longer, and no more frames over 50 ms a flick | met |
| A flick down the home page at 1440 x 900, processor 4x, 5 flicks: the median and the worst gap between frames, frames over 50 ms, the most layout shift | 16.7 ms, 66.6 ms, 2 of 731, 0.000 | 16.7 ms, 50.1 ms, 0 of 900, 0.000 | before misses 16.7 ms and 50 ms here too, so after is held to before: a median no longer, and no more frames over 50 ms a flick; layout shift at most 0.05 | met |
| The same flicks at 1440 x 900, once the hero has left the screen: the median and the worst gap, frames over 50 ms | 16.7 ms, 50.1 ms, 0 of 669 | 16.7 ms, 50.0 ms, 0 of 838 | a median of 16.7 ms or less and none over 50 ms | met |

Before misses the flick's 16.7 ms and 50 ms on this machine while the old hero is on screen, so those rows hold
after to before; once the hero has left the screen, the bands meet the bar. The sheet's raw numbers are kept as
JSON beside its table, and `--table` prints the table again from them without a browser.

**What closed.** The open items this round closed, and what closed them: `base.css` sits far under its budget
(the build strips comments, and the ceiling is 32 KB); the home page's sample sketch kept the old paper in the
dark theme (the toned paper is now on every dark page, and the sample gave way to the four people); at 1024 by
768 every lesson map showed its text version and 25 of the 44 ran over 630px (the lesson's column is 944px at
1024, so every map is drawn there as at 1440, and none is over 630px); the product manager's and the QA lead's
lines both ended on "a number you can defend" (the QA lead now ends on "proof that it works"); the Mental Models
picture labelled the models by their old names (it reads them from the site's registry now); the start page's
box opened with a bold lead (it opens with its answer); the interview bank for FDEs dated its two postings
"September 2026" (both rows cite the guide's records, read on 2 October); on the home page a wrapped "more" link
left its arrow at the column's far right and a route broke after an article (the review's fixes); and the root
`README.md`'s table of roles was stale (it names six roles now, the FDE guide among them, with the QA lead's own
line).

## Round thirteen: council 11, the BMAD rewrite, motion and polish

On 8 October the owner asked for the BMAD lesson rewritten to the current release, and for "animations, frame
graphics, motion graphics wherever required without performance dips", built with the council and the writing,
taste and diagramming skills by name, and finished fast: "don't over-spend time in testing, verification and
validation. Try to finish fast without bugs and compromising quality, attention to details etc. judiciously."
The same message answered round twelve's deferred call, a one-time reveal of the method map after seeing the
still. Council 11 sat as three seats, BMAD, motion and polish, and the chair cut their papers into five parcels,
built in parallel in their own worktrees and merged, with the gate run once after the merge: the map that draws
itself once and the phone key; three lesson figures that draw once; page to page, folds, the chooser, the reading
bar and the curve; the BMAD lesson at v6.12.1 and every knock-on; and the polish fixes. Two of the papers'
readings were corrected against the code before building: the gate's reduced-motion passes never see a reveal,
so they needed no change; and the hero's bottom is still on screen when the map is 40% in view at 1440 by 900,
so a reveal is triggered by where the drawing's top is, never by how much of it shows.

**The BMAD lesson.** Rewritten to v6.12.1 of 4 October 2026, re-read on the day against npm's `latest` and the
docs site: five named agents (the Analyst, the Product Manager, the UX Designer, the Architect and the Developer),
skills installed into the coding tool, one Build loop that sizes itself, four sizes from a session to a project,
and "six documents" defined once, in step 4. The repository overrode the seat's paper in three places: the
expansion is the Breakthrough Method *of* Agile AI-Driven Development (the paper and the old lesson said "for");
the test command stays out of `AGENTS.md`, because `package.json` holds it; and the next version renames the
documents' files, so the lesson names documents, and files only where `main` keeps them. Its map is the paper's
four sizes on one Build unit, 575 units and 622px tall at 1440 and at 1024, under the 630px cap after three
phrases were cut. Every other BMAD sentence, picture and wiki page says the same: `frameworks.json`, the methods
and merge boards, the chooser, the protocol page, two role steps, four lessons' lines, the hand-written wiki pages
and eight pictures shot again in both themes; "persona trail" is "document trail" everywhere, and `grep persona`
over the pages and the content finds nothing. The workbench's opening entry, its decoded list, its product
manager's drawing and two rows of its compare page say v6.12.1 too. The lesson is 1,668 words by the build's count, over the
ruling's 1,500 and about the old lesson's 1,645; the excess is its fixed apparatus, five FAQs, the role table and
the dated sources. Its page went from 17,439 to 18,796 bytes gzipped, and its title keeps "Build loop" in
sentence case, as the methods' names keep theirs.

**The map draws itself once.** With script, the map's parts are held on their first frame from load
(`html.js [data-play]:not(.play) *` paused), and when its top passes the middle of the screen `site.js` marks it
`.play`: the five shapes grow from their left ends row by row, 120ms apart, their words fading 300ms after each
row starts; the sign-off's line draws down from 900ms and its pills land at 1500; the wash at 1000 and its note
at 1150; the four questions from 1300, 60ms apart; "no method reaches this row" at 1500. It takes 1.75s (1.78 to
1.83 measured), every keyframe is a `from` only, so its last frame is the stylesheet's own still, and the frame,
the heads and the lane labels never move. No script, reduced motion and paper get the still at once. On a phone
the bare names only fade, the four phase heads read code over name, and a key under the lane label says what a
solid and a dashed strip mean. The chooser's kept line fades in over 250ms, its pill eases in 150 and a greyed
name in 250.

**Three figures draw once.** The drift's line is drawn in 1.2s, each week's reading and fall bar arriving as the
line reaches it, 170ms apart, and the alarm's ring at 900ms; the refund's line passes the claimed layers in
900ms, each layer's reality showing as the line reaches its panel, the money at 900, the dotted tail at 950 and
the alert's reality with the verdict at 1200, so it never shows before the money; the four ways back grow 150ms
apart, each time written 300ms after its bar starts. Every delay is computed in Python and written on the part
as `--d`, so the stylesheet carries four rules and no `calc`. Each figure is done by 1.45s, and the twelve stills
are byte for byte the round before's.

**Two decisions after the verdict.** The verdict had a drawing show complete until its reveal; with `.play`
landing when 40% of it was in view, a reader could see the top of a figure whole, then blank and redraw. So a
drawing's parts are held at their first frame from load, with script, and released when its top passes the
middle of the screen (a root margin of -50%, not the verdict's -60%). And since nothing may animate off screen, a
second observer finishes a drawing's animations the moment it leaves the screen mid-play: on the polish budget's
24-step flick down the home page, style recalcs fell from 109 to 19 at 1440 and from 112 to 17 at 390 slowed four
times, with no layout added, and a reader who watches the map draw sees no difference.

**Page to page, folds, the reading bar, the curve.** Where the browser has cross-document view transitions and
motion is allowed, the top bar holds (`view-transition-name:hd`) while the page beneath cross-fades in the
browser's own 250ms, and on the FDE guide the framework (`.fx`) moves from the hub to its place on a stage page;
no script, and each name is on one element a page across all 95 built pages. A fold (`.prose details`, `.otp`,
`.step`, `.howto`, `.lnav`, the lead's "how") opens in 250ms, its contents fading in and settling 4px, and closes
at once; the transition sits on the open state, so a fold open when the page arrives does not play, and a step
no longer animates its height on a wide screen. The reading bar fills by a transform written once a frame inside
`requestAnimationFrame`, so a 24-step flick down the hard gate lesson lays out the page 8 times, where it laid
it out 28. Four transitions were off the curve (`lensin`, the highlight, "Try it" and the roadmap's rule) and now
take `var(--ease)`; the grep for a transition without it leaves only `visibility 0s`.

**Polish.** Eleven of the polish seat's fixes were built: the hero's violet wash deleted; `#simulator{overflow:clip}`
over 1000px, so the day card's shadow ends at the band's foot; the phone hero's meta line on the column (its
centring deleted, not overridden); a no-break space before the arrow in the guide's next link, the labs' list and
two buttons; a role's counts are steps, templates, prompts and calculators, in the singular when there is one;
the footer's "Who made this", in one sentence, with the attribution kept; the labs head's lede and counts
computed from the labs (4 labs, 2 ready, 10 to 15 minutes each); minutes in full on a lesson's meta line and the
labs' list; the contact pill hidden on the home page's first screen until the top button appears, with
`visibility`, so a keyboard cannot reach it; and the reading bar and the curve above. Fix 10, codes in the
libraries' rails, was refused as a second component for one dot; fix 15, a two-line clamp on the guide's previous
and next links, was measured against all 55 titles at 240 and 214px and found unneeded once the arrows were
joined. The root and site READMEs now end on the footer's own sentence.

**The gate.** Pass 3 leaves out the parts of a drawing still held on their first frame; pass 4 brings every
drawing into view and waits for its animations to finish (2.5s at most) before it looks; `ui.test.mjs`'s
scroll-through does the same, because its contrast check at 390 and 320 had read the map's questions mid-fade.
The head comment that said the site had no view transitions now says it has them, and one drawn line, both
ignored by a browser without them.

**Refused.** The motion seat's pipeline shape for the BMAD map (the seat's four-size map is the release's own
picture, with one owner); the polish seat's four forms sweeping the frame's top (a decoration with no job);
rail codes in the libraries; the polish seat's chooser words (the BMAD parcel owned them); a 0.4 threshold for
the reveal; `will-change`; hover motion on the map's shapes; scroll-driven drawing; and everything on
DESIGN.md's refused list. The verdict also left `.step` out of the fold fade; the builder kept it in, with the
step's height transition gone, because the brief says a height never animates.

**Bytes** (gzip -9 on the built files, the round's base commit against its end). `base.css` 31,117 to 31,612
(30.9 KB of 32: the map's rules about 370, the figures and the folds about 125, the polish 19 less); `site.js`
3,151 to 3,442; `frame.js` 5,548 to 5,576 (of 6,144); `frame.css` 2,294 to 2,349; `fde.css` 1,870 to 1,884;
`hero.js` 10,060, untouched. The home page's HTML 19,318 to 19,326 (of 21,504), and a first visit to it 174.2 to
174.7 KB of 176 by the parcels' runs of pass 17; the labs index 5,057 to 5,002; the engineering page 42,557 to
42,507; the four lessons with a played figure 13,684 to 13,805, 14,120 to 14,201, 14,033 to 14,075 and 15,884 to
15,963, held to 25 KB. The polish budget at rest reads 0 layouts and 0 recalcs on every page measured.

**What closed.** The BMAD lesson's persona pipeline (rewritten); the phone map's wordless strips (the key) and
the one-time reveal of the map (built); and the role rows' keyless timelines, stale since round twelve rebuilt
the rows without them. Opened: Firefox gets no page transition; the workbench's remaining BMAD text; the
lesson's word count; the role counts at 390; the reduced-motion rule and pseudo-elements; the labs head's title;
a lesson flick's recalcs; the workbench's frame footer; two dead or stale lines; the top button's focus; the
gate's page list; a held drawing if `site.js` failed; and two stranded arrows, all below.

**After the round.** The owner asked for two of those items. A role page's counts row lost its template count,
which always equalled the step count, and the forward-deployed engineer's hub and stage pages lost theirs for
the same reason: the widest row now takes 269px, one line in the 350px column at 390 and the 280px one at 320.
The labs head's title became "Do an AI project's work with your own hands", the same words in a new order: two
lines at 1440, 1024, 768 and 390, where it took three, and three at 320 as before. Balancing the head ledes
(`text-wrap:balance`) was tried for the labs lede's short last line and taken out again: it keeps every line
count, but Chrome balances six lines at most, and a longer lede then loses `pretty`'s guard, so the models
page's ended on a 14px word at 390. The workbench's frame footer and the two stranded arrows had been fixed in
the round's last pass (a99f35e) and leave the list too.

**Then the ledes.** The owner asked for the long ledes shortened and the balance rule added. A sweep of every
page's head lede at five widths found six past six lines at 320, two more than the open item named: the models
page at 11, method at 8, pictures and templates at 7, and the two labs' replies pages at 7 and 10. Each lost what
its page already says beside it. The models lede's last sentence restated the card's anatomy, which the aside
next to it lists. The method lede announced the boards' questions, which the jump list under it shows. The
pictures lede repeated the counts row's number and the title's "in the manual". The templates lede repeated
where the FDE guide's templates are, which the counts row links to; the prompts lede shared that sentence and
lost it too. On the labs' replies pages, "every reply is here as its model wrote it" repeated the heading over
the replies, and what each model was sent moved under that heading, beside the prompts it describes; Lab 2's
lead no longer spells out the same system prompt and the same message, which "word for word" and the moved line
carry. All six
now take four or five lines at 320. Then `.phead .lede` took `text-wrap:balance`. Over all 27 heads with a lede,
at 320, 390, 768, 1024 and 1440, the short last lines (under 40% of the measure) went from 40 to none, and no
line count grew; the frameworks lede is the one at six, at 320. The gate's pass 6 now counts a head's lede at
320 and fails it past six.

## Round fourteen: one top bar on every surface

The owner, in the workbench: its SkyWays logo did not lead back to the manual; its way back was a faint
"Manual" where the simulator has a button; the simulator's bar said "The agentic manual" where it should say
where the reader is; and the simulator's tutorial button looked over-padded and was the highlighted one for no
reason. "Any such behavior breaks or expected, like behavior consistencies? Fix those also." Fable, at extra
effort, swept every surface's bar at 1440 and 390 in both themes and wrote one rule set; the fixes follow it.

**The rule.** Every bar has the menu icon at the left, then the mark and wordmark, which go to the manual's home
everywhere, and after the hairline the surface's name: "The agentic manual", "Simulator" or "Workbench". At the
right sit three kinds of control. A faint link is a sideways step from the page. An outlined 36px pill with a
14px line icon is the way out of a sub-surface: "The manual" with a house in the game and the workbench, and in
the game "The tutorial" with the book beside it. The one filled pill is the twin of the page; the game has
none, because its action is on the page. Filled and outlined share one geometry. On a phone the word beside the
mark is the surface.

**What changed.** The workbench's logo, in its bar and its phone sheet, went to the workbench's start page;
framed at /workbench/ it now goes to the manual's home, and only the frameless file keeps its own start. The
simulator's bar says "Simulator", and on a phone shows it in place of "SkyWays", as the workbench shows
"Workbench". The simulator's two buttons are both outlined, the manual's with a house, at 125.4 and 125.5px.
The tutorial button looked padded because it held its longer second label, "Read the lesson", invisibly while
it showed "The tutorial"; the second label is now "The lesson", 4.9px shorter than the first, so the stack no
longer shows. The workbench's "Manual" link became the same outlined "The manual" with the house. Its "Menu"
pill at the right became the menu icon at the left, as every other bar has it. Its mark drew at 26px where
every other bar draws 28, because an old rule outranked the site layer's; it draws 28 now. With the logo going
to the manual, the workbench's crumb root "Home" (to its own start) became "Start", so a page shows one home.
The workbench's "By role" now opens on "Your role in the manual", the six role journeys, which it had never
reached; that is the gap the sweep found behind the owner's "Roles roadmap". The manual's Roles menu, the role
pages' journey and the workbench's four playbooks otherwise keep their names, which already agree where they
mean the same thing.

**Bytes.** The workbench embedded four photos and showed three: the cockpit was only ever listed in the
credits. It went, and the app fell from 823.9 KB to 761.6 KB gzipped, 761.7 after this round's other changes,
63.8 KB under its 824 KB hold. The rules for brand markup that no longer exists (`.xbrand em`, `.xb2`) went too.
`base.css` grew from 31,614 to 31,689 bytes of its 32 KB.

**Refused.** A full bar on the 404 page: about 2 KB for a page nobody should land on, whose body lists the six
places. Keeping the game's tutorial pill filled with its padding corrected: the owner said it need not be the
highlighted one. A filled "Simulator" in the game for symmetry: a control never points at its own page. "The
manual" in the workbench below 1100px: its bar holds five menus, search and the evidence pack down to there, and
below it the mark and the sheet's first entry lead back. Renaming "The agentic manual" to a bare noun: it is the
site's name, and the bare nouns name its sub-surfaces.

## Open items

- The workbench names a different set of methods on its opening screen (it adds Spec Kit and Kiro).
- "Agentic STLC" has an FAQ entry and no lesson. If it earns one, it is built from the QA lead's journey.
- Two labs are listed as being built: proving the bar, and reviewing a change a coding agent wrote.
- Lab 1's own recordings name their model only as "Claude", with no version, while its three other models'
  replies carry theirs and Lab 2's recordings name Claude Opus 4.6. Lab 1 was not recorded again, and
  anyone who runs its prompts again to compare would want the exact model.
- On the title at 1440, Day 1's card has its kicker on the first screen and its answers below the fold.
- A run held only in memory, because the browser blocks storage, is dropped if the address changes to a
  day link mid-run: `boot()` checks the saved run, not the one in play. It predates round eleven.
- A late start in one role saved under the previous rules no longer replays, so the game drops it when
  the page loads and the title offers a fresh start. Late starts for the whole team, and every run from
  Day 1, keep their saves.
- The game's three scripts are 45.97 KB gzipped, 35 bytes under their 46 KB budget. Moving the room cards'
  27 sentences into `days.json` would free about 0.45 KB, and the code would read worse for it.
- `play/game.js` (line 492) still reads `--spring`, a token the stylesheet no longer has, and falls back to
  `ease-out`. The game can drop the lookup, or the token can come back if the game wants its spring.
- The picture pack is 37.88 KB gzipped, 124 bytes under its 38 KB hold, so the next card added to it needs room
  found first. Trimming the image data each card carries for search is the way back down.
- Eight lesson maps sit 2 to 5px under the cap, at 1440 and at 1024 alike (628, 627, 627 and five at 625px).
  Pass 18 fails if the lesson column ever widens enough to tip one over.
- In the tutorial's rail, and in the course a lesson's guide folds, a current lesson with a two-digit number
  (Running delivery 10 to 13) has its number 1.8px from the 2px accent bar, where a one-digit number has 8.4px.
  Opening the gap would mean moving every row's number.
- On the start page (`/learn/`) the "Start here" row's highlight still starts 10px left of the track
  headings. The row has no number to absorb the move, so aligning it would mean moving its words 10px
  right or setting them against the accent bar.
- On a phone the start page (`/learn/`) opens on its course list's fold, above its title, so its eyebrow sits at
  207px where every other head in a column has it at 134px; `ui.test.mjs` lists it as known. The libraries fold
  their list under the title, which would fit there too.
- The lesson rules' seven `.lm .prose .tw.stack` lines now repeat what the site's own `.tw.stack` rules do, about
  70 bytes of `base.css`.
- help.openai.com refuses the session's proxy, so five OpenAI facts in the Tool guides stand as the
  research sheet had them, unchecked against their pages. The ChatGPT and Codex manual does not use them.
- Two facts in the ChatGPT and Codex manual carry dates that will pass: OpenAI's existing evals become
  read-only on 31 October 2026, and the Evals dashboard and API and the `v1/prompts` API are to shut down
  on 30 November 2026 (`openai-evals` and `openai-prompt-objects` in `tools.json`). Both need rewording
  after those days, before their checks turn amber on 1 December.
- 28 of the FDE guide's 31 sources were read on 2 October 2026 and three (S26, S26b and S29) on the 3rd: they turn
  amber on 2 and 3 December. Re-check them by 1 December (`content/roles/_src/fde_sources.py`).
- The proof calculator in the FDE guide's step 3 opens on its shared defaults (82%, 40 cases, a bar of 80),
  not on the example's numbers; a default per step is a change to `calcs` or `enrich`.
- The FDE guide's four pages are not among `ui.test.mjs`'s states; their heads were measured by probe, and the
  gate's pass 20 holds the rest.
- The sketch lint's floor (`sketch.LABEL_MIN`, 54 units) is 12.6px in a 320px phone's 280px column; 56 would be
  13.1px. No sketch is under 58 now. Its 6,500-byte budget no longer binds either: with paths written from the
  point before, the largest sketch is 3,605 bytes.
- `pages/mapspecs.py`'s docstring names the hues by older colours (P0 green, P1 blue, P2 purple, P3 orange, `t`
  teal); they are slate, indigo, teal and amber, and `t` is violet.
- Nine older picture placements draw numbers their lesson's text does not state (`two_numbers` in the sponsors,
  productivity and P3 lessons; `bill_factors` in the costs and P3 lessons; `bolt_days` in bolts vs sprints and
  P2; `bar_sheet` in P1; `shadow_widen` in P3), and five pictures touch a table or
  sit straight under a heading (the governance gates, the evolution of the PDLC, one lifecycle for every
  method, P2, and what is the agentic PDLC).
- In a lesson in the dark theme, a code box's 46px band for its Copy button reads as empty space above the
  code.
- `.step{overflow:hidden}` clips text too wide for a step, so no sideways check can see it.
- `play/game.js` still calls the thirteen choices "calls", where the simulator's page says "decisions".
- `theme/hero.js` is 10,143 bytes gzipped, 97 under its 10 KB budget.
- A filled button prints near-white on white in Chrome's print preview (the hero's, the tutorial's and the
  simulator's); only the close's button has a print rule.
- `base.css` carries rules no built page uses. Removing them was left for a later round: the budget no longer
  needs it, and a class joined from strings would not show in a search.
- In the gate, `[data-reveal]>*` among the other pages' parts matches nothing on any page it walks; only the home
  page's parts have a guard against a name that matches nothing.
- The workbench on a phone, beyond what this round fixed: at 390 its route's day chips (29.6px), gate links
  (31.4), pictures' links (37.6), "who" links (34) and rail chips (31.5), and in its drawer the inputs (39 to 41)
  and the alternative links (21). The triangle's "holds" label, shown only when cost or latency is pushed, is
  ink on the dark card in the dark theme.
- "Check yourself", a recall block in every teaching lesson (about 150 questions, each a decision or a number
  from the case with its answer folded), waits for the next round, once the new lesson frame has settled.
- Firefox has no cross-document view transitions, so between pages it navigates as before: no cross-fade, no
  held top bar, and the FDE framework does not move from the hub to a stage page. Nothing is lost but the motion.
- The workbench is 823.93 KB gzipped (by the gate's zlib count) against its 824 KB hold: 68 bytes of room.
- The BMAD lesson is 1,668 words by the build's count, over the chair's 1,500; the excess is its five FAQs, the
  role table and the dated sources, and cutting it means dropping one of them.
- The reduced-motion rule's `*` does not reach pseudo-elements, so the copy tick (`.cp.done::before`) and the
  `.otp` chevron's rotation still move under reduced motion; `*,::before,::after` in that rule would close it.
  The fold fade guards itself.
- A 24-step flick down a lesson restyles about 40 times, because each frame's transform on the reading bar
  restyles the bar; the polish seat's 20 was measured with the bar removed. Layouts meet the floor of 8.
- `site.js`'s `all-open` in `reveal()` and `wireExpand()` existed to defeat the step's height animation, which
  is gone; it is dead and harmless. The head comment on `base.css`'s motion rules still says nothing moves
  because it scrolled into view, which the drawings that play once no longer honour to the letter.
- The top button (`.sw-top`) is still focusable while invisible; the contact pill now uses `visibility`.
- The gate's passes 3 and 4 do not visit the three lessons with a played figure; if one joins their page list,
  pass 4 waits for its animations as it does for the map.
- If `site.js` failed to load, a drawing that plays once would stay held on its first frame, because the head
  script sets `html.js` before `site.js` runs.
