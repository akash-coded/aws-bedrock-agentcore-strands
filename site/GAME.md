---
name: Ninety Days, the SkyWays simulator
status: first release
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

1. **What arrived.** A debt from an earlier day comes due, with the player's own choice quoted back.
2. **The scene.** Forty words at most, spoken by the people in the room.
3. **The call.** Two or three options. Each shows its price in days before it is chosen. What it will
   cost later is not shown.
4. **A hands-on task**, on five of the days: set the bar from two costs (Day 15), read a score one kind
   of case at a time (45), route nine changes for review (60), find the leak in the bill (75), build the
   slide (90). The first four open only behind the method's option; a shortcut skips the task with it.
5. **What it did.** A document goes on file, or something is pinned to a later day.

A full run is ten to fifteen minutes. A save is the list of actions taken, replayed on load.

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
- **One hard gate.** Day 15 needs three signed documents: the spec, the bar per slice, the authority
  budget. Short of them, the player holds the gate and writes what is missing, or opens it anyway.
- **Something nobody asks about.** From Day 30 the refund limit is in the prompt and not in the tool.
  No day prompts the player to check. Looking in on the Platform room shows it, and one day moves the
  limit into the tool. On Day 82 the refund is refused, or paid.
- **The ending.** Funded needs trust of five and the date met. Then funded with conditions, paused,
  stopped. Trust starts at four and rises twice at most: when the tool refuses the refund on Day 82, and
  when the slide carries both numbers and the loss. The slide on Day 90 is built from the run's own
  numbers; leave the cost off it and finance finds it.

The runway, the trust scale, the price of every option and the size of every debt are in
`play/days.json`. The verdict's thresholds, the ledger and a few debts that depend on how a task was done
are in `play/sim.js`. The case's own figures (82.4 and 79.1, the $400 limit and the $2,000 refund, 4.4
times as 1.6 × 1.5 × 1.3 × 1.41, the bars of 50, 80, 98 and 71, a first cycle of 31.2 person-days saved,
a $4,200 model bill and $6,912 of review time, net minus $1,128) come from the lessons and the workbench.
Where the manual disagrees with itself the game follows the lessons: the bars use the lesson's costs
($9 and $36), and Day 1 gives 12 requirements and 9 quality targets. The split of the 500 cases into
three kinds (400, 55 and 45) and the ledger away from the canonical line are the game's own, and
illustrative. A score on fewer than a hundred cases takes Wilson's lower bound, as the lesson says.

## Three ways to play

One engine, three controllers.

- **The whole team** (the default, with no choice before Day 1): every call is the player's.
- **One role**: the player makes their own role's calls. On every other day they see what a colleague
  plans to do, and may ask to see the evidence four times in a run. A colleague does the day properly
  when the document they lean on is on file and it is not one of their habits. Nothing is random. Every
  role can reach the best ending; none can reach it by leaving colleagues alone.
- **The organisation**: the player is the sponsor. They pick up to three rules to enforce out of six,
  then watch the days run with the same colleagues, and may ask a question twice. The best three rules
  alone are funded with conditions; with the two questions well spent they are funded; no rules at all
  is stopped.

## The picture (`play/art.js`)

SkyWays' head office at night, cut open: seven rooms and a lobby on four floors, drawn at one logical
pixel per unit and scaled by whole numbers. Everything is drawn in code; there are no image files.

- The room where today happens is lit and the others are turned down. The same room is shown close up
  above the dialogue.
- The walls show the state: the notes wall, the whiteboard, the build wall, the score against its bar,
  the bill, the departures board, the day board in the lobby.
- People are 10 by 22, about four heads tall, with no faces at that size: a jacket in the muted hue of
  the role, a light shirt, the role's accent on the lanyard. Faces appear only as 24 by 24 portraits
  beside what is said.
- The only lettering on the canvas is room names and the day board. Every sentence is page text.
- The plane is drawn side on, nose to the right, and only ever flies to the right.
- Rose means the gate and what is owed, as on the rest of the site.

Motion, under the site's rules: people walk into the day's room once; the build floors stay shuttered
until the gate has been dealt with and then lift; one plane crosses per day; the incident lands with a
short rose flash. Monitors and the roof beacon keep blinking, so the picture carries the site's pause control.
With reduced motion nothing is animated at all and each state is drawn once.

## Access

- The canvases are hidden from a screen reader. The game is the panel: a heading that takes the focus
  on each new day, the scene, a group of real buttons with the question as its legend, the outcome.
- Keys 1 to 3 choose an option while the focus is inside the group.
- Meter changes are announced in one polite status line. A debt coming due is in the day's own text.
- Tasks are radios, checkboxes and buttons. Nothing is dragged.
- "Undo today" returns to the start of the day. Nothing sealed has been opened by then, so it gives
  nothing away.
- Without script the page is the thirteen days as text.

## Tests

- `tools/sim.test.mjs` plays every combination of choices in whole-team mode, every role and every set
  of rules, without a browser. It asserts that no path dead-ends, that no shortcut is free, that the
  method's line is funded only when the date is moved on evidence, and that always-cheapest and
  always-most-careful both lose. It also lints the words.
- `tools/playtest.mjs` plays each mode by real clicks to the verdict in headless Chrome, at laptop and
  phone widths, and checks focus, saves and the forwarding of old workbench links.
- `tools/accept.mjs` includes the page, and asks the canvas how many frames it drew.

## What the council decided

Five advisors and five reviewers. All ten agreed on the frame: a game as the front door, the old tool
kept as the workbench at its own address, words as page text, rules before art. The reviews changed
four things. The economist's: two meters, and a budget that does not fit, so the date has to move. The
learning designer's: an over-do option only where the manual teaches against it, and one thing nobody
prompts the player to check. The owner's advocate's: portraits, people who move, a plane that reads as
a plane, and a verdict worth beating. The phone reviewer's: native controls, and undo for a slipped tap.

Refused for this release: sound, walking between floors, points and ranks, a pixel font for sentences,
random events. Not yet built: a short link that reopens a finished run, a picture of the Day 90
building to share, and a sixth task (sorting the constraints on Day 6).

## Open items

- The workbench still has its mascot, its ranks and a light-only theme. Only its plane was turned round.
- "Lena" (platform lead) and "Ines" (sponsor) are names the game adds; the case has four named people.
  The case gives Day 75, the bill, to the architect. The game gives it to the platform lead, so that
  role has a day of its own.
- The wiki still links to `/simulator/#/…` routes. They are forwarded, so nothing is broken.
