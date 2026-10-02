---
name: Ninety Days, the SkyWays simulator
status: second release (round six: days that open cold, a sixth task, colour, a link to each day; council 9: the ninety days as one line, Day 1 on the title, a safeguard on every press, the building's key, a row for each role, the day on the card's metrics, a loop that rests and a byte budget)
updated: 2026-10-02
form-factor: web, one page, canvas for the picture and plain HTML for every word and control
lives-at: /simulator/ (the earlier tool is the workbench, at /workbench/)
---

# Ninety Days

The simulator is a game. This file says what it is for, how it plays, what its rules are and how it
is drawn and tested. `DESIGN.md` and `EXPERIENCE.md` still govern everything around it: the
type, the tokens, the motion rules, the voice.

## Why it exists

The tool that used to sit at `/simulator/` is a reference: nineteen routes, about seventy thousand
words, seventeen calculators. It teaches by being read. The owner asked for a simulation: little text,
pixel art, an enterprise to move around in, depth on both the consultancy side and the technical side,
and three ways in (one role, the whole team, the organisation as its sponsor sees it).

What only a simulation can teach is a cost paid now against a larger one that arrives later with your
name on it, under a budget too small to do everything. So the game is built on that, and the old tool
stays behind it as the workbench: every day of the game links to the calculator or the lesson that
holds the depth.

## Who plays

- **A newcomer with ten minutes** who has never run an agent project. They must make a call inside
  twenty seconds, and no acronym may reach them before the thing it names has happened. Words such as
  NFR and ADR are given after the document is filed, as something earned.
- **A practitioner in one role** who wants to feel what their seat owns, and what it has to ask of
  the others.
- **A sponsor or team lead** who wants to see where a programme breaks, without playing thirteen days.

## The loop

Thirteen dated days stand for the ninety: 1, 4, 6, 9, 12, 15, 20, 30, 45, 60, 75, 82, 90. One day is:

1. **The head of the day**, written for someone who has seen no other day (see "Every day opens cold").
2. **What arrived.** A debt from an earlier day comes due, with the player's own choice quoted back.
3. **The scene.** Forty words at most, spoken by the people in the room.
4. **The call.** Two or three options. Each shows its price in days before it is chosen. What it will
   cost later is not shown.
5. **A hands-on task**, on six of the days: say which limits can move (Day 6), set the bar from two costs
   (15), read a score one kind of case at a time (45), route nine changes for review (60), find the leak
   in the bill (75), build the slide (90). The first five open only behind the method's option; a
   shortcut skips the task with it.
6. **What it did.** A document goes on file, or something is pinned to a later day.

A full run is ten to fifteen minutes. A save is the list of actions taken, replayed on load.

## Every day opens cold

A save reopens on Day 45 a week later, and a lesson links straight to its day. So each day screen
stands alone. From the top:

- **Kicker**: `Day 45 of 90 · Build and prove · QA room`. The day, the phase in words, the room.
- **Headline** (`head`, the `h2` that takes the focus): a sentence with the number and the stake,
  never a noun, in a newcomer's words. It names what it is about (the AI assistant, the project, or
  people by their role) and points at no one it has not named. "Day 45. On its first test the AI
  assistant got 82.4 percent of 500 real cases right. The team promised 80 percent." Day 82 has one per
  variant.
- **Premise and context**: one paragraph. The premise (`short`) is the same twelve words every day
  ("SkyWays is a fictional airline building an assistant that rebooks stranded passengers."), set
  quieter. The context (`context`) is one fixed sentence, true on every path, that says where the
  project is.
- **So far**, computed in `sim.soFar`: the earlier call that today leans on, quoted. The day itself says
  which call that is. Every day after the first has a `leans` entry: `day`, the id of the earlier day to
  quote; `doc`, the document whose state says what that call left; and, where the document's own
  sentence would say nothing about today, an `on` or `off` sentence of its own. It is not always the day
  that files what the rules need today (`needs`): one option on Day 20 costs two more days without the
  signed quality targets from Day 9, and the day quotes Day 12's decision records, because the third
  decision, the framework, is due today. `tools/sim.test.mjs` checks that every `leans` names an earlier
  day and a document an earlier day files. Every option carries a `recap`: past tense, ten words at most,
  no pronoun pointing back. Then what that call left: the document is on file (each document has an `on`
  and an `off` sentence), something is pinned to a later day, or today a choice comes back. "You" in
  whole-team mode, on the player's own days and on a call the player challenged; otherwise the
  colleague's name. Never "yesterday": the days jump. Day 1 says there is nothing yet, and how many of
  the ninety days are spare.

The premise and "So far" exist only for the cold reader, and together stay under forty words on any
path (twelve, and twenty-five at most). With the context the three lines come to 48 words at most on
the method's line. The end screen's table and the no-script list use the same headlines.

The page is written for the same reader before the first day. Its heading says what this is before it
says its name: `what` ("A game: run a ninety-day AI project."), large, then "Ninety Days, the SkyWays
simulator", small. Under it, `premise` is the opening lines: a fictional airline, an AI assistant that
rebooks stranded passengers, ninety days, and thirteen decisions that each cost days. Under them, once,
at 16px, `pitch` gives the facts: a game takes ten to fifteen minutes, and every decision shows its price
in days before it is chosen. `pages/play.py` renders the heading and the opening lines, and `game.js`
the pitch. `tools/sim.test.mjs` holds all three to the same plain words as a day, checks that `what`
says it is a game without giving the name, and that `premise` names each of those things.

### The title

From the top, at 1440 by 900: the heading and the opening lines side by side, on the same grid as the
building and the panel under them (594px, then the rest), so the opening lines keep to 46 to 56
characters a line. Then the ninety days as one line, the full width of the page. Then the building on
the left, with its caption over it and its key under it, and on the right Day 1 as the home page shows a
day. Then, the width of both, the two other ways to play: a row for each role and one for the sponsor.
At 1240 and under the order is the line, Day 1, the rows, the building; on a phone the same.

**The line of the ninety days** answers what a newcomer asks first: what are the ninety days, where
do the thirteen fall, what are the milestones, and can I start later. It is drawn to time: an 8px bar
in the four phase hues with each phase's name over its run, the seams halfway between the last day of
one phase and the first of the next (10.5, 25 and 67.5), and each of the thirteen at (day − 1) / 89 of
the width, numbered under. The four milestones are larger and ringed in ink, each with its word from
`line.milestones` in `days.json`: Day 15 "Sign-off", in rose, because rose is the sign-off; Day 45
"First test"; Day 75 "First bill"; Day 90 "Sponsor's slide". The caption under it, `line.caption`, is
"Start at Day 1, or at any day: the days before it are played by the book." Start sits at its right.

Every stop is a link to its day (`#day-45`; see "A link to each day"). Pointing at a stop, or focusing
it, puts that day's headline in the caption and makes the button "Start at Day 45"; pressing it opens
Day 45 by the book on a fresh run, saved, as "Open Day 45 on a fresh run" does. The choice stays until
another stop is pointed at, so the hand can travel from the stop to the button. The stops are one stop
for Tab, and the arrow keys move along them, so Tab goes on to Start with the day chosen. With a run
saved, "Carry on from Day 9" stands beside Start, and following a stop's link offers the same choice as
any link to a day. The line is page markup, a list of thirteen links whose text is the day, so it reads
without the canvas and without sight. On a phone only Day 1 and the four milestones are links, each a
44px target; the other eight are marks.

**Day 1 on the title** is the home page's day card, borrowed whole (`theme/base.css`, `.daycard`): 578
wide, a 20px corner and one long shadow, the boardroom at four times its size bled to the edges (three
times and cropped on a phone), one 26px inset, the kicker "Day 1 of 90 · Boardroom", the headline, the
context, the question, and the two answers with their price in days. Pressing an answer starts a
whole-team run and makes that call, as if on the day. Its answers are the game's own answer
component, the one every day uses.

**The building on the title** shows the day Start would open: Day 1, the boardroom lit and framed, the
other rooms turned down, the build floors shuttered, and under it "Day 1: the boardroom, top floor".
Pointing at a stop on the line shows that day instead, as the book would leave it (the shutters lifted
after the sign-off), at once and without motion.

**The role rows.** "One role" is five rows, then "The organisation" is a sixth, for the sponsor. A row
is one press: its button ("Play as Maya", the person's name; "Set the rules" for the sponsor, which
opens the rules screen) covers the whole row. At 1440 a row is 64px and reads across: the role and the
person with the number of their calls ("QA lead", "Maya · 2 calls"); one line of what you decide and
under it "Pick this if ..."; the player's days lit as ink marks on a 180px copy of the ninety-day line,
with the days under it; what you leave with; the button. Narrower, the same parts stack. The words are
each role's `card` in `days.json` (`decide`, `leave`, `pick`; the sponsor's is `org.card`), under
seventy words a role; the person, the days and the count come from the days' owners. There is no "Or
start at Day 45" in a row: `sim.book` plays the days before a later day as a whole-team run, and a role
run that starts later would need the rules to play the colleagues' days in a role run, which they do
not, so a role always starts at Day 1.

In play the strip of the thirteen days stays a carriage map of equal cells. Over it, each phase's name
spans its run; under it one line names the next milestone from today ("Next: the sign-off, Day 15",
and "Today: the sign-off" on the day); in one role the player's own days wear a ring. Beside the
building at 1440 that line and the meters share a row, unless there are four meters (one role, the
sponsor), which then take a row of their own.

### The day's card

In play the day, from its kicker to its answers and what follows them on the day, is one card on the
home page's day card's metrics: the paper surface, a 20px corner, one 26px inset that every line and
answer shares, and three sizes: the 12.5px mono kicker (and the book line, the names, a price), the
headline at up to 25px in balanced lines, and 15.5px for everything read, the question included, in
its card weight. Inside a group things stand 8px apart and groups stand 20px apart. Answers are 48px
tall with a plain mono price at the right, the same component as Day 1's card on the title. A task or
the sign-off is part of the card, under a hairline, not a box in it. Reading text keeps to 75
characters a line (33.5em); a tinted box keeps the card's width and its words the same measure, and
every tinted box is inset 16px. Who the player is and the strip stand over the card; the debts, the
date and the way out under it. The building is the one object with depth: the card's corner and its
long shadow.

On a phone the card runs to the screen's edges, its inset the page's own, so its words keep the width
they had, and the call comes first: under the news stand the question and its answers, and then the people in the room, the day's
figure and the line about the book. The kicker drops the phase (the strip above names it). So the first
answer of every day is on a 390 by 844 screen: Day 20, the longest, ends it at 828.

## A link to each day

`/simulator/#day-45` opens Day 45 on a fresh whole-team run, with the earlier days played by the book
(`sim.book`): the method's option each day, each task done well, the limit typed into the tool on the
first day that is possible, and the date moved once if the runway has run out. The screen says so in
one line. Nothing is saved until the player makes a move, and the link is cleared from the address
then. With a run already saved, the title offers both ("Carry on from Day 9", "Open Day 45 on a fresh
run") and only the second replaces the save. The stops on the title's line of the ninety days are these
links. A day that is not one of the thirteen falls back to the title. Hashes that begin with a slash are the old workbench routes, and are forwarded as before.

The site header's pill on this page follows the day: on a day whose `deeper` list has a lesson it
reads "Read the lesson" and points there; otherwise it goes back to the tutorial.

## The rules (`play/sim.js`)

Two meters. **Runway** is days of slack before Day 90. **Trust** is the sponsor's, out of six, and it
moves only on surprise: bad news told early costs nothing.

- **Pay or owe.** Doing a day properly costs days and files a document. A shortcut costs less and
  leaves a sealed debt on the day the case itself names: a dot vote on Day 9 comes back on Day 75. A
  debt always costs more than the shortcut saved, in days or in trust.
- **The way back.** A sealed debt can be repaired before it fires, at twice the price.
- **The budget does not fit.** The runway is eighteen days (twenty in one role). Doing all thirteen
  days properly takes eighteen or nineteen, and on one of three days, set by the run, a vendor's freeze
  takes two more. The date can be moved once, by four days. With four documents on file the sponsor
  agrees without a question; without them it costs three of her six points of trust. That is the first
  claim of the method: a phase ends on evidence, not on a date.
- **The price is not a tell.** On some days the method's option is the dearer one, on some the cheaper,
  on some the middle of three. Over-doing loses too: forty decision records, a halt on all eleven open
  questions, two senior readers on every change. Each of those is in the manual's own lessons.
- **One sign-off.** Day 15 needs three signed documents: the spec, the bar per slice, the authority
  budget. Short of them, the player holds the build and writes what is missing, or starts it anyway.
  Everything a player reads calls this the sign-off. The lessons call it the hard gate, and the code
  keeps `gate` as its name.
- **What cannot be ranked comes out first.** Day 6's method option opens the sixth task: six lines were
  all called a must, three are limits nobody in the building can change in ninety days (the law, the
  booking system, a partner contract) and three are wishes. A limit left unticked goes to the workshop
  as if it could be traded and comes back from its owner: the law stops the Day 15 sign-off (2 days,
  trust 1), the booking system reruns the Day 9 workshop (the same 3 days as skipping the day), the
  partners' cap cuts off the first build on Day 30 (2 days). A wish ticked as a limit costs Day 9 one
  day, however many are ticked. Done right it costs nothing beyond the day, so the budget is unchanged.
  One trip back to a day repairs everything that day left sealed.
- **Something nobody asks about.** From Day 30 the refund limit is in the prompt and not in the tool.
  No day prompts the player to check. Looking in on the Platform room shows it, and one day moves the
  limit into the tool. On Day 82 the refund is refused, or paid.
- **The ending.** Funded needs trust of five and the date met. Then funded with conditions, paused,
  stopped. Trust starts at four and rises twice at most: when the tool refuses the refund on Day 82, and
  when the slide carries both numbers and the loss. The slide on Day 90 is built from the run's own
  numbers; leave the cost off it and finance finds it.

The runway, the trust scale, the price of every option and the size of every debt, the limits task's
included, are in `play/days.json`. The verdict's thresholds, the ledger and a few debts that depend on how a task was done
are in `play/sim.js`. The case's own figures (82.4 and 79.1, the $400 limit and the $2,000 refund, 4.4
times as 1.6 × 1.5 × 1.3 × 1.41, the bars of 50, 80, 98 and 71, a first cycle of 31.2 person-days saved,
a $4,200 model bill and $6,912 of review time, net minus $1,128) come from the lessons and the workbench.
Where the manual disagrees with itself the game follows the lessons: the bars use the lesson's costs
($9 and $36), and Day 1 gives 12 requirements and 9 quality targets. The split of the 500 cases into
three kinds (400, 55 and 45) and the ledger away from the canonical line are the game's own, and
illustrative. A score on fewer than a hundred cases takes Wilson's lower bound, as the lesson says.

## Three ways to play

One engine, three controllers.

- **The whole team** (the default, with no choice before Day 1, and what a link to a day opens): every
  call is the player's.
- **One role**: the player makes their own role's calls. On every other day they see what a colleague
  plans to do and its price, and may ask to see the evidence four times in a run. A colleague does the day
  properly when the document they lean on is on file and it is not one of their habits. Nothing is
  random. Every role can reach the best ending; none can reach it by leaving colleagues alone.
- **The organisation**: the player is the sponsor. They pick up to three rules to enforce out of six,
  then watch the days run with the same colleagues, and may ask a question twice. The best three rules
  alone are funded with conditions; with the two questions well spent they are funded; no rules at all
  is stopped.

A question works the same way in both. "Ask to see the evidence" is offered on every plan while
questions are left, sound or not, so being offered tells the player nothing. Asking (`ask` in `sim.js`)
costs one question, whatever it shows, and shows the evidence and nothing more: the document the plan
works from and whether it is on file, and what the plan would put on file. On Day 90 it is the slide as
planned. It never says what the plan costs later; the player still has to judge. Then the player lets
the plan stand or asks for another option (on Day 90, builds the slide), at no further cost; the sponsor
chooses what to send the team back to do. In one role a call asked for becomes the player's own, task
and all. The sponsor only asks, and the team then does the day the way it was chosen.

## The picture (`play/art.js`)

SkyWays' head office, cut open: seven rooms and a lobby on four floors, drawn at one logical pixel per
unit and scaled by whole numbers. Everything is drawn in code; there are no image files.

Colour comes from light and material, never from bright paint:

- **Walls.** Each room takes about a third of its owner's jacket into its walls, capped at a quarter
  saturation: Product from Priya, Architecture from Arjun, Engineering from Sam, QA from Maya, Platform
  from Lena. The boardroom is walnut. The contact centre and the lobby belong to nobody on the team and
  stay grey. The room chips on the page carry the same hue as a swatch.
- **Sky.** One still sky per phase, the same in both themes: dawn for Frame, morning for Design and
  spec, afternoon for Build and prove, golden hour for Run and learn. Day 90 is dusk, or night if the
  run is late. It shows above the roof, through the windows of six rooms and through the lobby doors.
  Stars only at dusk and at night. The apron and its runway lights follow it. Lamps stay warm against it.
- **State.** The lobby's day board draws its digits and its thirteen dots in each day's phase hue, with
  a white core on today and a rose pixel under a day that has something due.

- The room where today happens is lit and framed in white, and the others are turned down by half, so
  their walls keep their hue. The same room is shown close up at the head of the day.
- Every canvas is drawn at a whole number of screen pixels to an art pixel and never resampled. The
  building's picture fills its column: twice its size wherever the column holds 594px, once on a phone,
  with the sky and the apron running on either side of the building where the column is wider than it,
  and cropped by its frame on the smallest phone (297 in 280). The close-up is always twice its size.
- Above 1240 wide the building stands beside the day and the close-up is not shown. In play it stays in
  view as the page scrolls; where it is taller than the window it scrolls until its foot is in view and
  stays there, so the key is never out of reach. On the title it scrolls with the page. At 1240 and under
  the building moves below the day, and the close-up sits beside the day strip and the meters. Between
  900 and 1240 wide, during play, the close-up, the day strip and the meters form a rail to the left of
  the day (`play/game.css`), so a day that also brings news (Day 20's freeze, Day 82's refund) still has
  its question and its first option on the first screen; under the day the building starts on the
  rail's edge and its key stands beside it, ending on the card's edge. On a phone the close-up is
  cropped to its column and its ceiling, with the three meters stacked beside it.
- Room names are drawn on the canvas at twice its size and up. On a phone, at one to one, a name would
  be five pixels tall, under the site's 11px floor, so there they are in the key only.
- The walls show the state: the notes wall, the whiteboard, the build wall, the score against its bar,
  the bill, the departures board, the day board in the lobby.
- People are 10 by 22, about four heads tall, with no faces at that size: a jacket in the muted hue of
  the role, a light shirt, the role's accent on the lanyard. Faces appear only as 24 by 24 portraits
  beside what is said.
- The only lettering on the canvas is room names and the day board. Every sentence is page text.

### The building's key

Over the building, a caption (`building.caption`): "SkyWays head office. Each day happens in one room,
lit. The days start at the top, work down to the passengers, and end in the boardroom." Under it, one
line: where today is ("Today: the boardroom, top floor"; on the title, "Day 1: ..."), beside the pause
control. Then the key, headed "Who works where, and their days": a button for each room, which is its
line of the key, in two columns where the column holds them (both ending on the building's edges) and
one on a phone. Each reads room, person, days: "QA · Maya · Days 45, 82". The days are the days the
room is lit and the days its person makes the call, wherever that is; the person is whoever on the
team, or the sponsor, sits there, and the contact centre has nobody ("Contact centre · Day 82"). A
room's button opens its card, on the title as in play, and the card opens on its person: "Maya, QA
lead, makes the calls on Days 45 and 82. Day 82 is held in the contact centre." In a run the card goes
on to what the room shows today, and the platform room's action. Last, the three marks the picture
uses, each beside a scrap of the building drawn by `art.js` at twice its size: a white frame, today's
room; a steel shutter, shut until the sign-off; a rose square, something is due there. No tour, no
popup: the key is page text that is there for whoever reads it.
- The plane is drawn side on, nose to the right, and only ever flies to the right.
- Rose means the sign-off and what is owed, and nothing else: the shutters on the build floors, the bar
  the sign-off set, a pin, the flash when the incident lands. It is not used for decoration.

Motion, under the site's rules: people walk into the day's room once; the build floors stay shuttered
until the sign-off has been dealt with and then lift; one plane crosses per day; the incident lands with
a short rose flash. Monitors and the roof beacon keep blinking, so the picture carries the site's pause
control. With reduced motion nothing is animated at all and each state is drawn once.

## Four small simulations (`play/game.js`, `play/game.css`)

Page elements, not canvas. Each shows one idea the words carry badly, plays once per day in true steps
(no number counts up), lasts between 0.6 and 1.6 seconds, ends on the whole picture, and is skipped
under reduced motion, where the whole picture is simply shown. Only transform, opacity and clip-path
move, on the site's own curves and durations.

- **Day 45, the score splits.** One bar at 82.4 breaks into three columns, as wide as their share of the
  500 cases, each with its own bar line and the margin under its score. The smallest sample has the
  longest whisker.
- **Day 75, the bill multiplies.** The estimate, then a segment for each habit: 1.6, 1.5, 1.3, 1.41, to
  4.4. Ticking a fix takes its segment out and everything after it shrinks.
- **A debt is pinned.** A rose pin leaves the outcome line and lands on its day on the day strip, which
  keeps it. When the debt fires, that day's text quotes it.
- **Day 82, paper or wall.** The $2,000 refund meets the $400 limit as a sheet of paper (a sentence in
  the prompt) and goes through, or as a wall (the tool) and stops. The figure follows the call, below the
  options, and stays on the day once the call is made.

## Access

- The canvases are hidden from a screen reader. The game is the panel: a heading that takes the focus
  on each new day, the scene, a group of real buttons with the question as its legend, the outcome.
- Keys 1 to 3 choose an option while the focus is inside the group.
- Meter changes are announced in one polite status line. A debt coming due is in the day's own text.
- Tasks are radios, checkboxes and buttons. Nothing is dragged. A form submitted empty says what is
  missing in a status line.
- The figures in the small simulations are hidden from a screen reader; each has a caption or a status
  line in real text that says the same thing.
- The line of the ninety days is a list of links named "Day 15 Sign-off" and so on. Tab reaches the
  chosen stop, the arrow keys move along the line, and the caption that follows the stop is a polite
  status line.
- Every press runs inside one safeguard. The next screen is built before the panel is emptied, and a
  run is saved only once its screen exists, so a press that throws leaves the page as it was and saves
  nothing. The panel then says "This page is out of date. Reload to play." with a Reload button, and
  the console gives the error. It is for a browser that holds an old `sim.js` under a new `game.js`:
  the title calls nothing in the rules, Start is the first call, and before this a stale file made
  Start do nothing visible.
- "Undo today" returns to the start of the day. Nothing sealed has been opened by then, so it gives
  nothing away.
- A role row is one button, "Play as Maya", described by the row's own words; the key's rooms are
  buttons that say pressed, and a card that opens takes the focus.
- Without script the page is the thirteen days as text, each under its own headline and context. With
  script, one line in the page's head (`pages/play.py`) marks the page `nd-js` before it paints, and the
  style sheet hides that text, so it never flashes up while the game loads on a slow phone. If the game
  cannot start (the rules or the pictures never came, or the first screen throws) `game.js` takes the
  mark off and the text comes back.

## Weight and the loop

The building is the only thing that loops, and the loop rests whenever no canvas it would change is on
the screen: an observer watches the building's canvas and the close-up of today's room, and the loop
runs while the building is in view, or while the close-up is in view and its people are still walking
in. On a phone on Day 1 the building is far down the page, so after the walk-in nothing is drawn until
the building is scrolled to. Nothing starts because it came into view; it goes on from where it was.

The game's weight has a budget, held by `tools/accept.mjs`: its three scripts under 45 KB gzipped
(44.8), the site's `base.css` under 40 KB (39.5), the page's HTML under 25 KB (16.4), and no font but
the four the site has. Council 9's first parcel had taken the scripts to 46.8 KB and this one added the
key and the rows, so the comments in `game.js` and `art.js` were cut to a line of why each, leaving the
reasons to this file; no rule and no number of the game changed.

## Tests

- `tools/sim.test.mjs` plays every combination of choices in whole-team mode (each task done well or
  badly), every role and every set of rules, without a browser. It asserts that no path dead-ends, that
  no shortcut is free, that the method's line is funded only when the date is moved on evidence, and
  that always-cheapest and always-most-careful both lose. It checks the limits task's debts one by one,
  that the book reaches every day with nothing owed, that a document goes on file only when its task is
  done, and that a stopped or late run never reports the saving of the method's line. A question can be
  asked of a sound plan as well as an unsound one, costs one, shows only the evidence (on Day 90, the
  slide as planned) and makes asking for something else free. It also lints the words: no dash, no
  "gate", no word the player has not been given yet, no sentence over twenty words, nothing that points
  at someone it has not named; a headline with a verb or a number that names what it is about, a
  one-sentence context, a question that says who is to act, a recap of ten words with no pronoun, and a
  heading that says it is a game before its name. The line's caption and the note on Day 1's card are
  held to the same plain words, and its four milestones must be days of the game, in order, the first
  of them the sign-off's. Every day after the first leans on an earlier day and
  on a document an earlier day files, and its "So far" quotes that day, never joins two and runs to
  twenty-five words at most whatever was chosen.
- `tools/playtest.mjs` plays each mode by real clicks to the verdict in headless Chrome, at laptop and
  phone widths, and checks focus, saves and the forwarding of old workbench links. It does the sixth
  task by its controls, opens `#day-45` with and without a save, opens all thirteen links, reads the
  header pill, and checks that every headline it saw is a sentence. Its eleventh section keeps what an
  audit found by looking, as checks run with motion allowed: the title's first screen says what the game
  is and how to start, at 1440 and 390 wide, with the opening lines at 46 to 56 characters a line and
  every button on the title as tall as Start; a day's question and its first option are on the first
  screen at 1440 by 900 and 1024 by 768, on Days 20 and 82 as well as 1, 9 and 45, and at 390 by 844 on
  Day 1; the header does not
  move between days; on Day 75 only the labels of what is left are shown, none on another; on Day 82
  nothing sits on anything else down to 320 wide; a figure plays only as the answer to a press, and only
  on screen; a pin flies only to a day strip that can be seen; a document goes on file when its task is
  done; Day 15's three documents line up; the sponsor is offered a question on a sound plan and on an
  unsound one, and in one role the evidence comes before the other options; and a day offers one way to
  leave the run. Its twelfth section is the title: the line is thirteen links drawn to time with the
  four milestones named, on the first screen; focusing Day 45 puts its headline in the caption, the
  arrow keys move along the line, and "Start at Day 45" opens it by the book, saved; pointing at a stop
  does the same, and the stop's own link opens its day unsaved; on a phone the five links are 44px
  targets and the other eight are marks; Day 1's card starts a whole-team run with the call that was
  pressed; in play the strip names its phases, says the next milestone and rings a role's own days.
  Every mode's first press, and every move after it, must leave no "This page is out of date" on the
  page. And with `sim.soFar` deleted in the page, as an old `sim.js` would lack it, Start must leave the
  title as it was, save nothing, and say so with a Reload button. The first-screen check of section 11
  runs every one of its days at 390 by 844 too. Its thirteenth section is the building and the rows: the
  caption, the key of seven rooms in two columns on the building's edges reading "QA · Maya · Days 45,
  82", the line under the building, the three marks drawn at twice their size, and a room's card opening
  on its person; five role rows of 64px at 1440 and the sponsor's, each one press, with the role's own
  days lit on a 180px line and its words under seventy with no dash; the day's card at 20px, 26px,
  12.5, 25 and 15.5px with answers of 48px and a plain price, the same component as Day 1's card; the
  faults council 9 measured, each measured again (the context's measure, a tinted box's inset, the
  building on the rail's edge at 1024, the building at a whole scale on a phone, faces at twice their
  size, strip numbers at 11px); and, at 390 on Day 1, no frame drawn while the building is off the
  screen until it is scrolled to.
- `tools/accept.mjs` includes the page, and asks the canvas how many frames it drew. Its first pass
  checks that without script the thirteen days are shown as text. Its sixteenth holds `game.js` back and
  checks that the page paints with that text hidden, that the game comes up once the script arrives,
  and that the text comes back when `sim.js` cannot be fetched. Its seventeenth is the byte budget,
  read from the built site.

## What the council decided

Five advisors and five reviewers. All ten agreed on the frame: a game as the front door, the old tool
kept as the workbench at its own address, words as page text, rules before art. The reviews changed
four things. The economist's: two meters, and a budget that does not fit, so the date has to move. The
learning designer's: an over-do option only where the manual teaches against it, and one thing nobody
prompts the player to check. The owner's advocate's: portraits, people who move, a plane that reads as
a plane, and a verdict worth beating. The phone reviewer's: native controls, and undo for a slipped tap.

Refused for this release: sound, walking between floors, points and ranks, a pixel font for sentences,
random events. Not yet built: a short link that reopens a finished run, and a picture of the Day 90
building to share.

Round six, a second council of five and five. The owner's words: more colour, more simulations, and
"somebody who is seeing it should not have to know the beginning of the story to know what is going on
in Day 45". The verdict: fix the day screen first, then spend colour and motion only on state the words
cannot carry. Rooms take their owner's hue and the sky takes the phase, because rooms are not phases.
The recap quotes the day today leans on, because the day before often says nothing about today. The
sixth task takes out what cannot be ranked before anything is ranked, which none of the other five
teaches. "The gate" became "the sign-off". Refused: thirteen skies, a stamp that bounces, daylight that
moves, rooms tinted by phase.

## Open items

- "Lena" (platform lead) and "Ines" (sponsor) are names the game adds; the case has four named people.
  The case gives Day 75, the bill, to the architect. The game gives it to the platform lead, so that
  role has a day of its own.
- A link to a day always opens whole-team mode on seed 0, so the vendor's freeze falls on Day 20.
- A role cannot start at a later day: `sim.book` plays the earlier days for a whole-team run only. A
  role row could offer "Or start at Day 45" once the rules can play a role run's colleagues by the book.
