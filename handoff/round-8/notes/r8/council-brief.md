# Council 7 brief: depth, simulations, tools, and a site with a personality

You are one advisor on a council of five. Decide; do not survey. Say what to refuse and what to build
first. 1,100 words at most. Plain words, no em or en dashes.

`SP` means `handoff/round-8/notes`.
Repo: `.` (the site is in `site/`).

## Read first

1. `SP/r7/context.md`: the product, the owner's taste, the tools for looking (use port 8811, not 8833:
   `http://localhost:8811/` is the working build, which already has this round's fixes).
2. `site/DESIGN.md`, `site/EXPERIENCE.md`, `site/GAME.md` (the contracts the site is built to).
3. What the last council decided, in one paragraph: the lesson sketches stay but were cut from 98 to 77 and
   shrunk to the text column; the hero is now one canvas with a thin spiral and no pills; the home page's
   simulator band is one real day of the game as a card; all entrance and scroll-triggered motion was
   removed (motion is only for a thing that is itself a movement, or an answer to the reader's hand);
   floating buttons no longer sit on text; stylesheets and scripts carry a version in their address.

## What the owner said after that (verbatim, trimmed only where it repeats)

"Leadership page also needs your deep inspection and overhaul and improvement. It's a text spaghetti and
currently directionless. Also, the simulator when we open, reads Ninety Days? Why? What's the meaning of
that to someone visiting the site for the first time? Also, heading like 'Day 4. Six people must agree to
one list. None of them has seen it.', what does that mean? Seen what list? None means who? Make them
clearer to understand and more readily understandable at a glance. Where are diagrams, options to pick
things and do a better use of visuals. Right now it just looks slightly pretty. I need depth too and actual
nuances too. Give the site a personality. And improve performance throughout and the whole UI and UX flaws
and experience. Several minor visual or logical or functional or polish issues exist. Fix them all. The
user journey and each page experience has to be smooth and coherent and feel wow and well laid out with
attention to minute details.

The simulation is difficult to follow. No need to use day-wise structure, if the council comes up with a
better alternate. You need intelligent, innovative, ingenious and inspired simulations. Detailed, to give a
feel of all substeps, properly, simulate running prompts to get things done, choices made, details picked
and finalised, techniques applied and then artefacts created and shown properly with everything being
properly sequenced in several well-crafted, fun, interactive, highly insightful, useful and also educative
lessons. But don't break anything. Everything should be polished, amazing, no mistakes and also highly
performant. And I thought the simulator will be more dynamic with diagram drawing for example as one
simulation, with HLD, zooming in and out majestically, LLDs, context diagrams, etc. Similarly crafting
PRD-lite, PRD, enhanced PRD, agent specs, spec-kits, modern spec doc, in that teaching them along the way
to pick markdown or even better LLM-native/AIDD-native formats along the way. Also, such level of detailing
everywhere. Not all role paths have to be identical to each other. They need to be best crafted to convey
the concepts for that in the best possible way. And similarly, simulate using model playground like tools
at the right stage or stages, similarly picking configs by some light affirmation testing using innovative
techniques, tools, etc. Testing multiple versions of system prompts, the art and method of crafting them,
what tools they can use, how they can leverage Claude or ChatGPT there. And also any advanced techniques
and traps and how to overcome them or never fall into them by adopting what guardrails or practices. This
is one example. I want you to think of such connected, coherent and meaningful, genuinely amazing
experiences for the candidates.

Build up understanding of all possible usages of Claude, Claude chat, skills, connectors, scheduled tasks,
every feature of Claude projects and their potential creative and technical usages, Claude Code, Claude
remote session, Claude on Chrome, Claude in terminal, Claude in VS Code, etc. and parallels in
Codex/ChatGPT, and where Google AI Studio or Jules or other such niche but useful tools can be used.
Manuals on them too. And for these and more tools and features naturally incorporated into different
simulations and workflows like a seasoned professional working at 200% efficiency but impeccable
productivity.

[About the home page's table of four methods against the four phases:] it's clean but not informative
enough. Doesn't convey by picture how the methods are different and have weaknesses or incompleteness or
limited application and their salient features too. And how SkyWays PDLC or our AI-native PDLC is useful
and how. It should be clear to any visitor and be impactful too. In the tutorial, text in most pages
doesn't fit full page. The hand-drawn style illustrations by themselves are not making sense. A picture
should be even clearer to understand than words and be relatable. Those new hand-drawn style illustrations
are also too big for their pages or something looks off about them. I like the cleanliness and elegance of
the per role structure. Take inspiration from them maybe for the tutorial and even further improve them.
The frameworks page ('The frameworks, and how they merge into P0 to P3') also has useful content. Maybe we
can borrow some inspiration and ideas for our home page. And bring out the value prop in the home page."

Standing taste: premium, roomy, few elements, one strong visual per section; short human sentences; every
screen readable cold; keep what the owner found clear and add beside it.

## Evidence (open with the Read tool; look before you answer)

- Home, as it is now: `SP/r8/base/home-dark-1440-01.jpg` to `-09`, and the hero at `-t0`.
- Leadership page (`/protocol/`): `SP/r8/base/protocol-dark-1440-01.jpg` to `-14`, phone `protocol-dark-390-01` to `-08`.
  Source: `site/pages/protocol.py`.
- A role page, which the owner likes: `SP/r8/base/pm-dark-1440-01.jpg` to `-10`. Source: `site/render.py` (`role_page`).
- A lesson: `SP/r8/base/lesson-dark-1440-01.jpg` to `-08`, phone `lesson-dark-390-*`. The tutorial's front: `learn-dark-1440-*`.
- The frameworks page (use these, the working build's copy is mid-edit): `SP/r7/manual/frameworks-dark-1440-01.jpg` to `-10`.
  Source: `site/render.py` (`frameworks_page`), `site/content/library/frameworks.json`, `site/pages/illos.py`.
- The game: `SP/r8/base/sim-dark-1440-*`, `simday-dark-1440-*`; its words and rules: `site/play/days.json`, `site/play/sim.js`;
  an audit of it: `SP/r7/audit/simulator.md`. The older workbench (calculators, playbooks, nine decision
  walks): an audit and plan at `SP/r7/audit/workbench.md`.
- The sketches as they are now, 77 of them: `SP/sk/rev-1.jpg` to `rev-7.jpg`.
- The role content the simulations can draw on (every step, template and prompt, already written):
  `site/content/roles/*.json`, and the 55 lessons in `site/content/learn/lessons/`.

## Hard constraints

- A static site on GitHub Pages: Python renders HTML, one stylesheet, small vanilla scripts, no framework,
  no server, no model calls. So "running a prompt" in a simulation is authored: the page holds the prompts,
  the model's replies and the artefacts, and shows the ones the player's choices lead to. It must still feel
  live and must never pretend a canned reply is a real one.
- One worked case runs through everything: a fictional airline building an assistant that rebooks stranded
  passengers, over ninety days, with a cast of six roles. Numbers already in the lessons and the game stay true.
- Facts about real tools (Claude, ChatGPT, Codex, AI Studio, Jules and so on) must be accurate, dated and
  sourced, because they change monthly. A manual that is wrong is worse than none.
- Nothing that exists may break: the game, the workbench, deep links, the lessons, the role pages.
- Performance is a feature: no page may get slower to first read; anything heavy loads only when asked for.
- Motion rule as above. Dark by default, light on a toggle, both must work. Phones from 320px.

## The questions

**Q1. The simulations.** Design the set. What replaces or sits beside the day-by-day game? Give a concrete
list (five to nine) of hands-on simulations: for each, its name, who it is for, where it sits in P0 to P3,
what the player actually does with their hands (not "learns about"), what they run or draft, which tool it
simulates, what artefact they leave with, and the one trap it teaches. They must connect: what one makes,
the next uses. Say what one shared interaction model can carry all of them on a static site (so the build
is one engine and many scripts, not nine separate apps), how a "prompt run" is shown honestly, how diagrams
are drawn and zoomed (context, HLD, LLD), how documents grow (PRD-lite to PRD to agent spec) and where the
player is taught to choose a format (markdown, or formats written for models). Name the first three to
build and why. Say what happens to "Ninety Days" (keep as the story mode, rename, fold in, retire).

**Q2. Tool fluency.** How should the site teach the tools themselves (Claude in its forms, ChatGPT and
Codex, Google AI Studio, Jules, others worth naming): as manuals, as cards inside simulations, as both?
Give the structure: which pages, what each must contain, how deep, how each stays true as the tools change,
and how a tool shows up inside a simulation "like a seasoned professional" would use it. Say which tools
earn a manual and which only a mention.

**Q3. The Leadership page.** Diagnose it from the screenshots and the source, then give its new shape:
what a sponsor needs in the first screen, the order of what follows, what becomes a picture or a control
instead of prose, what is cut or moved to another page.

**Q4. The home page's case.** The owner wants the value shown, and a picture that shows how the four
methods differ (what each is for, where each is weak or silent) and what the SkyWays PDLC adds. Design that
picture and say what the home page should borrow from the frameworks page. Keep the table the owner called
clean, or replace it: decide.

**Q5. The tutorial page and its sketches.** The owner: the text does not use the page; the sketches do not
make sense alone and look too big; the role pages are the model to follow. Decide the lesson layout (what
goes in the empty right side at 1440, where a sketch sits and at what size, what the role pages have that
lessons lack) and the fate of the sketches under the owner's new standard: a picture must be clearer than
the words and relatable. Be concrete about which kinds of sketch survive.

**Q6. Personality.** In five lines: what is this site's personality, in voice and in look, and the three
places it should show first. No mascots.

**Q7. Order of work and risk.** Given all of the above, the order to build in, what to leave for a later
round, and the three most likely ways this goes wrong.
