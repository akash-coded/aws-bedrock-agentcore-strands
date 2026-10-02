---
name: Ninety Days, the SkyWays simulator
status: second release (round six: days that open cold, a sixth task, colour, a link to each day; council 9: the ninety days as one line, Day 1 on the title, a safeguard on every press, the building's key, a row for each role, the day on the card's metrics, a loop that rests and a byte budget; round ten: a role can start at any of its own days, the stops on the line look pressable, and the title says what playing by the book means; round eleven: a late start assumes every earlier day was done the recommended way, in one role as in the whole team, and opens on a briefing of the calls, the documents and where the run stands)
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
"Start at Day 1, or press a day on the line to start there. The days before that day are played for you, the
recommended way." Start sits at its right.

Every stop is a link to its day (`#day-45`; see "A link to each day"), and its number is underlined, as a
link in text is, so it reads as something to press before any pointer reaches it. Pointing at a stop, or focusing
it, puts that day's headline in the caption and makes the button "Start at Day 45"; pressing it opens
Day 45's briefing on a fresh run, saved, as "Open Day 45 on a fresh run" does (see "A link to each day"). The choice stays until
another stop is pointed at, so the hand can travel from the stop to the button. The stops are one stop
for Tab, and the arrow keys move along them, so Tab goes on to Start with the day chosen. With a run
saved, "Carry on from Day 9" stands beside Start, and following a stop's link offers the same choice as
any link to a day. The line is page markup, a list of thirteen links whose text is the day, so it reads
without the canvas and without sight. On a phone only Day 1 and the four milestones are links, each a
44px target with its number underlined; the other eight are marks, with no number. So the caption says "press a
day", never "any day".

**Day 1 on the title** is the home page's day card, borrowed whole (`theme/base.css`, `.daycard`): 578
wide, a 20px corner and one long shadow, the boardroom at four times its size bled to the edges (three
times and cropped on a phone), one 26px inset, the kicker "Day 1 of 90 · Boardroom · Your answer starts the
game" (its last part is `line.card`), the headline, the context, the question, and the two answers with their
price in days. Pressing an answer starts a whole-team run and makes that call, as if on the day. The kicker
says so because at 1440 it is on the first screen and the answers are not, and a newcomer could not tell a
preview from a game already running. Its answers are the game's own answer
component, the one every day uses.

**The building on the title** shows the day Start would open: Day 1, the boardroom lit and framed, the
other rooms turned down, the build floors shuttered, and under it "Day 1: the boardroom, top floor".
Pointing at a stop on the line shows that day instead, as the book would leave it (the shutters lifted
after the sign-off), at once and without motion.

**The role rows.** "One role" is five rows, then "The organisation" is a sixth, for the sponsor. A row
is one press: its button ("Play as Maya", the person's name; "Set the rules" for the sponsor, which
opens the rules screen) covers the whole row and plays from Day 1. At 1440 a row is 64px and reads across:
the role and the person with the number of their calls ("QA lead", "Maya · 2 calls"); one line of what you
decide and under it "Pick this if ..."; the player's days lit as ink marks on a 180px copy of the
ninety-day line, with the days under it; what you leave with; the button. Narrower, the same parts stack.
The words are each role's `card` in `days.json` (`decide`, `leave`, `pick`; the sponsor's is `org.card`),
under seventy words a role; the person, the days and the count come from the days' owners.

The days under the line are links that start the role on that day (`#day-45-qa`, see "A link to each
day"), and a role whose first call comes after Day 1 has one more, in words: "Or start at Day 45, your
first call" (`line.first`), on the product manager's Day 15, the engineering lead's 30, the QA lead's 45
and the platform lead's 75. They are underlined, as links in text are, and lie over the button's cover, so
the rest of the row is still one press. At 1440 a row with a first call is 93px: its link takes a second
line under the days and what you leave with. Narrower it has a line of its own. On a phone every link is
at least 24px tall, the days stand beside the line where they fit and under it where they do not, and they
are spaced so that no two targets touch. The sponsor's row has no days to start from: the sponsor still
starts at the rules.

In play the strip of the thirteen days stays a carriage map of equal cells. Over it, each phase's name
spans its run; under it one line names the next milestone from today ("Next: the sign-off, Day 15",
and "Today: the sign-off" on the day); in one role the player's own days wear a ring. Beside the
building at 1440 that line and the meters share a row, unless there are four meters (one role, the
sponsor), which then take a row of their own.

### The day's card

In play the day, from its kicker to its answers and what follows them on the day, is one card on the
home page's day card's metrics: the paper surface, a 20px corner, one 26px inset that every line and
answer shares, and three sizes: the 12.5px mono kicker (and the link back to a late start's briefing, the names, a price), the
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
figure and the link back to a late start's briefing. The kicker drops the phase (the strip above names it). So the first
answer of every day is on a 390 by 844 screen: Day 20, the longest, ends it at 828.

## A link to each day

`/simulator/#day-45` opens Day 45 on a fresh whole-team run, and `/simulator/#day-45-qa` opens it in one role,
the QA lead's. Either way a late start assumes that every earlier day was done the recommended way
(`sim.book`): each call the recommended option, each task done well, the limit typed into the tool on the
first day that is possible, and the date moved once if the runway runs out. In one role those days are
played as the whole team would play them, by the same moves: no colleague's plan waits on a day before the
run's start (see "The rules"), so the player starts with all four questions and nothing owed, on the role's
runway, two days longer. A run from Day 1 is as it was, in every mode.

Before the day, a short briefing says what that assumption amounts to, from the rules' own record: the run is
replayed to that day, and each earlier day is read as it stood before "On to". Its heading is the line the
day used to carry, "Days 1 to 30 were played for you the recommended way." (It said "played by the book",
which a newcomer could not read, and then "the method's way", a phrase the page had not explained.) Under it
are three parts. The calls: each earlier day on one line with the day, who made the call, the call (the
option's own label) and its price in days; under a day, anything else that moved the runway or trust that
day (the vendor's freeze, the limit typed into the tool, the date moved, the refund the tool refused), so
the days spent add up to the runway left. On file: the documents on file by then, each with the day that
filed it. Where the run stands: the meters, as the day shows them (runway, trust, documents on file and, in
one role, questions left), with trust's number beside its pips; "The project began with 18 spare days. The
days before used 14 days.", because a player who starts late never saw Day 1 say how many of the ninety are
spare; the document the day works from, in the words the evidence box uses ("Working from. A pass mark per
kind of case is on file."); and "Nothing comes due from the days before." One press,
"Start Day 45", opens the day as it always opens: at the top, its headline focused, its people walking in,
its first answer where it always is. Where the line about the book stood, the day then offers "What was
done before Day 45", which opens the briefing again, its button now "Back to Day 45". The whole team and a
role get the same briefing but for who the player is and the questions. At 1440 it stands beside the
building; from 1240 down it is one column of 640px, as the verdict is; on a phone the calls stack (the day,
who and the price over the call) and the documents take one column. From about Day 20 the briefing is
taller than a laptop's window, so the row of its one button sticks to the window's foot, on the card's
paper under a hairline, while the recap scrolls beneath it, and rests at the card's end once the reader
reaches it: on Day 45 at 1440 by 900 the button sits at 818 to 900px, where it had ended at 1,140. On a
phone the row spans the card's full width. Its fixed sentences are `brief` in `days.json`.

Nothing is saved while the briefing is open, and the link stays in the address, so a reload opens the
briefing again. "Start Day 45" saves the run and clears the link, so a reload after it resumes past the
briefing: the title offers "Carry on from Day 45", which opens the day. With a run already saved, the title
offers both ("Carry on from Day 9", "Open Day 45 on a fresh run"; for a role it says "This link opens Day 45
as Maya.") and only the second replaces the save, saving the fresh run and opening its briefing. A save the
rules can no longer replay to its end is dropped, as a damaged one is: a late start in one role saved
before round eleven, when the book still questioned colleagues' plans before the start, is one. The stops on
the title's line of the ninety days and the days on a role's row are these links. A day that is not one of
the thirteen, or a role the game does not have, falls back to the title. Hashes that begin with a slash are
the old workbench routes, and are forwarded as before.

What a start can reach, measured by a search over every move a player has: from every start the page offers,
funded. That is the whole team from each of the thirteen stops on the title's line (seed 0, as the links open
them), each role from each of its own later days on its row (seed 0), and the whole team and each role from
Day 1, on each of the three days the vendor's freeze can fall. Before this round six late starts in one role
could reach funded with conditions at best (the engineering lead from Days 30 and 60, the QA lead from 45 and
82, the platform lead from 75, the product manager from 90), because the book had spent their questions on the
days before the start and let some shortcuts stand. Now a late start keeps its four questions for the
colleagues' days still to come, and finds nothing owed.

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
- **A late start.** A run that starts at a later day (`from`, which a link to a day sets) assumes every
  earlier day was done the recommended way. In the rules that is one condition in `openDay`: a colleague's
  plan waits for the player only from the run's start. So in one role a day before the start is the
  player's to play, and the book plays it as the whole team would, with the moves any player has; the role
  keeps all its questions and starts with nothing owed. From Day 1 the condition never applies, so a run
  that starts there is played as before.

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
  random. Every role can reach the best ending; none can reach it by leaving colleagues alone. A role
  can also start at any of its own days, with every day before it done the recommended way, as the whole
  team would have done it, and a briefing of what was done (see "A link to each day").
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
lit. Day 1 is in the boardroom at the top. The days work down the floors to the passengers, and come back
to the boardroom on Day 90." (Before, it said the days start at the top, work down and end in the
boardroom; a newcomer who could see the boardroom at the top read that as a contradiction.) Under it, one
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
- A late start's briefing is a heading that takes the focus, three parts each under its own heading, and
  one button. The calls are a table whose rows are headed by their day; a line under a day (the freeze, the
  limit) carries that day too, for a screen reader, and the columns have names only a screen reader hears.
  "What was done before Day 45" on the day is a button that looks like a link, a 24px target on one 19px line.
- A role row is one button, "Play as Maya", described by the row's own words; its days and its first
  call are links over that press, a day named "Day 45 as Maya" and the first call by its own words. The
  key's rooms are buttons that say pressed, and a card that opens takes the focus.
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

The game's weight has a budget, held by `tools/accept.mjs`: its three scripts under 46 KB gzipped
(45.97), the site's `base.css` under 40 KB (39.66), the page's HTML under 25 KB (16.9), and no font but
the four the site has. Council 9's first parcel had taken the scripts to 46.8 KB and this one added the
key and the rows, so the comments in `game.js` and `art.js` were cut to a line of why each, leaving the
reasons to this file; no rule and no number of the game changed. Round ten's role start took them to 45.3
KB, and it fits because the last fixed sentences in `game.js` (the sign-off's opening line, the sponsor's
two lines, Day 82's figure captions, the three questions for Monday) moved into `days.json` with every other
word of the game, where the tests lint them; the page's HTML carries them instead. One list of number words
now serves two places, and `sim.owner`, which nothing called, is gone. Round eleven's briefing took them from
44.95 KB to 45.97, over the 45 they had. The honest savings came first: the role book's rules for questions left
`sim.js`, which is now smaller than it was; the briefing shows the run's numbers with the meters the day uses,
and the evidence line and the trust wording are each one function now, shared by the day and the briefing;
its sentences are in `days.json`. What is left is the briefing itself, so the budget was raised to 46 KB, the
measured size rounded up to the next half KB, with the reason beside it in the gate's pass 17. One saving was
not taken: the room cards' 27 sentences could move into `days.json` for about 0.45 KB, but each is chosen by
the condition beside it, and the code would read worse without them.

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
  heading that says it is a game before its name. The line's caption, the note in Day 1's kicker, the
  briefing's heading, section names, buttons and the link back to it, the link to a role's first call, the building's
  caption and every other sentence the page takes from `days.json` are held to the same plain words, and
  the line's four milestones must be days of the game, in order, the first of them the sign-off's. Every
  day after the first leans on an earlier day and
  on a document an earlier day files, and its "So far" quotes that day, never joins two and runs to
  twenty-five words at most whatever was chosen. Its ninth section is the late start: the whole-team
  book plays every day exactly as it did before (seeds 0 to 2 and the page's own, every day and the end,
  against a copy of the old book kept in the test), and a role's late start at any of the thirteen days is
  played by those very moves; it opens with every earlier call the recommended option, all four questions,
  nothing owed and no plan questioned or let stand, and with the same calls, tasks, documents, trust and
  limit as the whole team's, the same days spent on a runway two days longer; a run from Day 1 in one role
  opens each colleague's day with their plan waiting, as before; and from every start the page offers (the
  whole team from each stop on the line and from Day 1 on each of the three days the vendor's freeze can
  fall, each role from its own days on its row and from Day 1 the same way: 42 in all) some line still ends
  funded, the best ending, which is what was measured. That is a memoised search over every move a player
  has. It tries first what a player who knows the method would do, drops a line that can no longer end
  funded (trust rises twice at most; every day still to come costs at least its cheapest option, a freeze
  ahead its days, a sealed debt the lesser of its days and its repair), and replays the line it finds to
  its verdict; all 42 take about 8 seconds, the QA lead from Day 1 the longest. It prints the trust,
  runway, documents and questions at the opening of each day for the whole team and for one role.
- `tools/playtest.mjs` plays each mode by real clicks to the verdict in headless Chrome, at laptop and
  phone widths, and checks focus, saves and the forwarding of old workbench links. It does the sixth
  task by its controls, and checks that every headline it saw is a sentence. Its ninth section is a link
  to a day: the stop for Day 45 on the title's line, pressed by a real click, opens the briefing, which
  lists the earlier days with their calls and prices (checked against `days.json`'s recommended options),
  the freeze and the limit under their days, the documents with the day each was filed, the run's numbers,
  the spare days the earlier days used, what the day works from and that nothing comes due, with nothing saved and the link kept; one press opens
  the day at the top with its "So far", saves the run and clears the link; a reload resumes past the
  briefing; from the day the briefing opens again with "Back to Day 45"; all thirteen links open their day,
  every one after the first on its briefing; and `#day-45` with a save offers both runs and replaces the
  save only when asked. It also reads the header pill. Its eleventh section keeps what an
  audit found by looking, as checks run with motion allowed: the title's first screen says what the game
  is and how to start, at 1440 and 390 wide, with the opening lines at 46 to 56 characters a line and
  every button on the title as tall as Start; a day's question and its first option are on the first
  screen at 1440 by 900 and 1024 by 768, on Days 20 and 82 as well as 1, 9 and 45, and on the QA lead's
  Day 45, opened past their briefings, and at 390 by 844 on Day 1; the header does not
  move between days; on Day 75 only the labels of what is left are shown, none on another; on Day 82
  nothing sits on anything else down to 320 wide; a figure plays only as the answer to a press, and only
  on screen; a pin flies only to a day strip that can be seen; a document goes on file when its task is
  done; Day 15's three documents line up; the sponsor is offered a question on a sound plan and on an
  unsound one, and in one role the evidence comes before the other options; and a day offers one way to
  leave the run. Its twelfth section is the title: the line is thirteen links drawn to time with the
  four milestones named, on the first screen; focusing Day 45 puts its headline in the caption, the
  arrow keys move along the line, and "Start at Day 45" opens its briefing by the book, saved, and then
  the day; pointing at a stop does the same, and the stop's own link opens its briefing unsaved; on a phone the five links are 44px
  targets and the other eight are marks; Day 1's card starts a whole-team run with the call that was
  pressed, and its kicker says "Your answer starts the game"; every stop that is a link has its number
  underlined before any hover (all thirteen at 1440, the five links on a phone), and the caption says to
  press a day; in play the strip names its phases, says the next milestone and rings a role's own days.
  Every mode's first press, and every move after it, must leave no "This page is out of date" on the
  page. And with `sim.soFar` deleted in the page, as an old `sim.js` would lack it, Start must leave the
  title as it was, save nothing, and say so with a Reload button. The first-screen check of section 11
  runs every one of its days at 390 by 844 too. Its thirteenth section is the building and the rows: the
  caption, the key of seven rooms in two columns on the building's edges reading "QA · Maya · Days 45,
  82", the line under the building, the three marks drawn at twice their size, and a room's card opening
  on its person; five role rows at 1440 (64px, or 93px with a first call) and the sponsor's, each one
  press, with the role's own days lit on a 180px line and its words under seventy with no dash; the day's
  card at 20px, 26px,
  12.5, 25 and 15.5px with answers of 48px and a plain price, the same component as Day 1's card; the
  faults council 9 measured, each measured again (the context's measure, a tinted box's inset, the
  building on the rail's edge at 1024, the building at a whole scale on a phone, faces at twice their
  size, strip numbers at 11px); and, at 390 on Day 1, no frame drawn while the building is off the
  screen until it is scrolled to. Its fourteenth section starts the QA lead at Day 45 from her row by a
  real click (the pointer pressed and let go over the link, so the row's cover would take it if it lay on
  top): every role's own days are links on its row and a late first call has one in words; her briefing
  opens as Maya, with her calls, documents, runway, four questions and nothing owed, and a reload opens it
  again by its address; one press by a real click opens Day 45 in one role, her days ringed, no debt
  arriving and the first answer on the first screen at 1440 by 900, saved; a reload then resumes past the
  briefing by "Carry on from Day 45"; `#day-45` alone is still the whole team, briefing and day; with a run
  saved the row's link offers the same choice as any link and leaves the save alone; "Play as Maya" still
  starts at Day 1; an address with a role or day the game does not have falls back to the title; at 390 and
  320 every link on the rows is at least 24px tall, the one a finger lands on, touching no other and inside
  its row, with nothing scrolling sideways; and at 390 and 320, for the whole team and for Maya, the
  briefing stacks with its documents in one column, and neither it nor the day it opens scrolls sideways,
  the link back a 24px target.
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

Round ten. The owner approved a role that starts at a later day. The first version of the role book
questioned every plan that was not the method's way while questions lasted, and a search over every move a
player has showed what that left: four roles had spent all four questions by Day 45, Priya's Day 90 slide
then cost three of the sponsor's six points of trust, and the best a QA lead starting at Day 45 could reach
was paused, a platform lead starting at Day 75 stopped whatever they did. A player who knows the method
keeps a question for the sponsor's slide, so the book does: every start a row offers can now reach funded
with conditions, and the test holds it there. Three outside readers, shown the title as newcomers, all
understood the game and could not find how to start later: the stops did not look pressable, "by the book"
meant nothing to them, and Day 1's card could have been a preview. So the stops' numbers are underlined, the
caption says to press a day and that the days before it are played for you the recommended way, the card's
kicker says the answer starts the game, and the building's caption follows the picture.

Round eleven. The owner asked that a late start assume what would have been done by then, and present it
with the evidence, the documents and a recap of how it went. Until then the book played a role's earlier
days as that role would have: a colleague's plan stood unless a question was spare for it, so a late start
in one role began with fewer questions, sometimes with a debt falling due (the QA lead's Day 45 opened with
the engineering lead's Day 30 shortcut, which pushed her first answer below the fold at 1440), and six late
starts could reach funded with conditions at best. Now every day before the start is done the recommended
way, in one role as in the whole team, by one condition in the rules: no plan waits before the run's start.
The book's rule for keeping a question for Day 90 had nothing left to do, and is gone. The note that said the
earlier days were played for you became the heading of a briefing: the calls and their prices, the documents
and their days, and where the run stands, read before one press opens the day.

## Open items

- "Lena" (platform lead) and "Ines" (sponsor) are names the game adds; the case has four named people.
  The case gives Day 75, the bill, to the architect. The game gives it to the platform lead, so that
  role has a day of its own.
- A link to a day, for the whole team or for one role, always opens on seed 0, so the vendor's freeze
  falls on Day 20.
- A late start in one role that was saved before round eleven no longer replays under the new rule, so it
  is dropped when the page loads and the title offers a fresh start. Late starts for the whole team, and
  every run from Day 1, keep their saves.
