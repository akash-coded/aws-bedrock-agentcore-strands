# Round 7 context: the SkyWays site (read this first)

`SP` below means `handoff/round-8/notes`.
Repo: `.` (the site is in `site/`).

## The product

"SkyWays, the agentic manual": a free manual for building software with AI agents. A static site: Python
renders plain HTML (`site/build.py`, `site/render.py`, `site/pages/*.py`), one stylesheet
(`site/theme/base.css`), small vanilla scripts, no framework, GitHub Pages. One lifecycle (the SkyWays PDLC:
P0 Frame, P1 Design & Spec, P2 Build & Prove, P3 Run & Learn, one sign-off between P1 and P2, and a way back
from P3 to P0), five role journeys, 55 tutorial lessons, a pixel-art game ("Ninety Days", at `/simulator/`)
and an older single-file reference tool (the workbench, at `/workbench/`). Dark by default, light on a toggle.

The visual and behaviour contracts are `site/DESIGN.md`, `site/EXPERIENCE.md` and `site/GAME.md`.

## What the owner said this round (verbatim)

"The illustrations are also broken in homepage, everywhere else too. Either fix them properly or
replace/remove them as deemed fit by the council. Also, homepage globe looks buggy, and is now worse than
before. I meant something more fluid, elegant, dynamic, etc. And you didn't have to apply framer motion for
the sake of it. Also, in home page, the simulator depiction now is too long and then there is random text
below that. Many such issues have come up. I want you to properly ponder on them, find them all, fix them
all, etc."

And one round earlier, in frustration: "Where is the intelligence? I've given you so many skills, so much
inputs, and a whole council and BMAD approach to work with, and you're still making so many mistakes."

Standing taste, from earlier rounds: premium, roomy, few elements, one strong visual per section; the hero is
a clean call-out. Short human sentences, no clever sayings. Every screen and heading readable cold (a reader
who lands in the middle must understand it). Keep what the owner found clear; add beside it, do not replace
it. The owner also said last round: "So far the design is quite a vibe, quite a good thing."

## What is already known (do not rediscover it)

1. **A cache fault made the last release look far worse than it is.** The site served `theme/base.css` and
   its scripts under one unchanging address with a ten-minute browser cache. A reader who arrived just after
   the release got the new pages with the previous stylesheet: sketches rendered as black blobs, the three
   simulator pictures stacked in a tall column with a numbered list under them, black aircraft shapes and a
   black wedge on the globe. Proof: `SP/stale/stale-hero.jpg`, `stale-sim.jpg`, `stale-sim2.jpg`,
   `stale-sketch.jpg`. This is fixed in the build (every stylesheet and script now carries a content version
   in its address). It explains "broken", but not everything: the owner's taste verdicts stand on their own.
2. **Real faults seen with the correct stylesheet, in a real browser with motion on** (`SP/r7/hero/*.jpg`):
   the aircraft breaks into dashed fragments while it changes shape (`home-dark-1440-t3.jpg`,
   `home-light-1440-t1.jpg`); the phase pills collide with each other and sit on the globe; "the next round"
   is clipped by the globe; at 768px and on a phone the pills overlap and the floating mail button covers
   one (`home-dark-768-t0.jpg`, `home-dark-390-t1.jpg`); on a phone the globe is cut by the first screen.
   The simulator band on the home page is a whole-page screenshot shrunk into a browser frame, too small to
   read, with a line of monospaced caption under it that the pause button sits on.
3. The last round's checks ran mostly in headless Chrome with reduced motion. That is why moving faults
   were missed. Safari and Firefox have not been looked at.

## The site to look at

A frozen copy of the current build is served at **http://localhost:8833/** (use this one; the copy on 8811
is being changed while you work). Pages: `/` (home), `/learn/` and `/learn/<slug>/` (lessons; slugs are the
file names in `site/content/learn/lessons/`), `/method/`, `/product-manager/` `/solution-architect/`
`/engineering/` `/qa/` `/devops/` (roles), `/protocol/`, `/models/`, `/frameworks/`, `/templates/`,
`/prompts/`, `/pictures/`, `/simulator/` (the game; `/simulator/#day-45` opens a day), `/workbench/`.

Screenshots already taken (JPEG; open them with the Read tool), named `<page>-<theme>-<width>-NN.jpg`, one
per screenful from the top, motion on:
- `SP/r7/base/home-dark-1440-01..09`, `home-light-1440-01..09`, `home-dark-390-01..13`
- `SP/r7/base/lesson-dark-1440-01..10`, `lesson-light-1440-..`, `lesson-dark-390-01..14` (lesson `p0-frame`)
- `SP/r7/base/learn-dark-1440-..`, `method-dark-1440-..`, `sim-dark-1440-..`, `workbench-dark-1440-..`
- `SP/r7/hero/home-dark-1440-t0..t5.jpg`: the hero at 0.8s, 2.5s, 6s, 11s, 16s and 22s after load
- All 98 lesson sketches, twelve to a sheet, with the correct stylesheet: `SP/sk/rev-1.jpg` to `rev-9.jpg`

## Tools for looking yourself

- `node SP/walk.mjs <outDir> <width> <height> <light|dark> name=url [name=url ...]` walks a page with motion
  on and writes one screenshot per screenful. Env: `MAX=14` screens, `TIMES="0,1500,4000"` extra shots of the
  first screen at those milliseconds after load, `STEPS='[{"click":"css"},{"wait":500},{"eval":"js"}]'` to act
  before the walk. It prints script errors and sideways scroll. Widths under 600 are emulated as a phone.
- `node SP/drive.mjs <url> <outDir> <width> <height> <steps.json>` runs steps
  (`{"shot":"name"}`, `{"click":"css"}`, `{"text":"button text"}`, `{"eval":"js"}`, `{"wait":ms}`,
  `{"full":"name"}`); set env `MOTION=1` or it runs with reduced motion.
- Write your screenshots under `SP/r7/<your-name>/`. Read images with the Read tool.

## Rules for you

- Look, do not change. Do not edit anything under the repo, do not run `site/build.py`, do not run any git
  command that changes state, do not commit or push. Your output is your report.
- Be concrete. Every finding names the page, the width and theme, what is seen, and the screenshot that
  shows it. No hedging and no survey of options.
- Plain words. No em or en dashes in your report.
