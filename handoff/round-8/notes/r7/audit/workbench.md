# The workbench: audit and upgrade plan

Source: `site/app/SkyWays-Architect.html` (5,211 lines, 1.99 MB; styles on lines 7 to 2020, script from 2043). Screenshots: `scratchpad/r7/workbench/`. Nothing was changed.

## Part 1. Audit

Walked 26 routes at 1440x900 and 390x844, the site's dark setting stored.

**What works.** No script errors and no sideways scroll at either width. All 17 calculators recompute when an input changes. The NFR simulation runs eight decisions and files its document to the pack (`x-sim-nfr-end-1440.jpg`). Search, the tour, Swap, the route chips, the rail toggle, the phone menu and the older walk-through all respond. All 31 deep links in the repo resolve.

**One real bug.** A cold link to a part of a page lands short, because the "what is here" card is inserted 60 ms after the scroll target is measured (`showPage` wrapper, line 5114). `#/toolkit/bar` puts the calculator's top at y=735 on a phone and y=366 at 1440 (`x-deeplink-tool-bar-390.jpg`, `x-deeplink-tool-bar-1440.jpg`); `#/governance/gv-gates` at 674 and 343; `#/sa/step-5` at 597 and 306. All 15 such links from the game, the lessons and the mental models are affected.

**Out of place on every route.**
- Light only. The body is `rgb(250,251,254)` whatever `manual-theme` says. Only the hero follows the system setting, so a reader from the dark manual gets a dark hero on a white page (`start-dark-1440-01.jpg`).
- The tab title reads "SkyWays PDLC Simulator" (line 2851), overriding the build's title.
- Three bars: the frame's strip (50px), the tool's bar (60px, holding 5 lists, 6 pills and a points counter), then a rail. On a phone they take 159px and the title starts at y=271 (`x-start-390.jpg`).
- Display type is Outfit at 700 to 800 with a text shadow. Text is already Geist and Geist Mono.
- 19 of 21 pages open with a mascot card in three cells under capitals ("WHAT IS HERE", "HOW TO USE IT", "YOU LEAVE WITH"): 168 to 308px at 1440, 385 to 589px on a phone. On 15 routes the first paragraph starts below the first phone screen.
- Gradient washes, 13 blur rules, 88 shadows, 22 capitals rules, 13 sizes under 11px.
- The back-to-top button covers a rail link (`episode-dark-1440-03.jpg`, `learn-dark-1440-02.jpg`).
- Phase hues are green, blue, violet, amber with a pink gate; the site uses slate, indigo, teal, amber and rose. P1 is "Specify" 12 times and "Design & Spec" 5 times.

| Route | For | Out of place | Must survive |
|---|---|---|---|
| start `#/start` | Front door | "Welcome to SkyWays", "Hi, I'm Sky", "by SkyWays Consultancy", "Your rank: Ground crew"; 8,498px long (`start-dark-1440-02.jpg`) | Four figures (`#illo-*`), role chips |
| quest `#/quest` | Ninety days as a map | "The whole simulator as one route", rank, "Second officer at 1 stops", vault, side quests (`quest-dark-1440-01.jpg`) | The map `.xrt`, progress counts |
| story `#/story` | Thirteen episodes | "this simulator"; cast as cards (`story-dark-1440-01.jpg`) | Episode list, cast |
| episode `#/episode/<id>` | One day in eleven sections | Opener 308px; breadcrumb repeats the title (`episode-dark-1440-01.jpg`) | Worked days, scenes, checks |
| sims `#/simulations[/<id>]` | Nine decision walks | Opener 234px | All nine walks |
| loopmap `#/loopmap` | Four phases, eight loops | "hard gate" without "sign-off" | `#lm-big`, detail panel |
| concepts `#/concepts` | 55 concepts on a map | "this playbook"; map unreadable at Fit on a phone (`x-concepts-map-390.jpg`) | `.xzm-w`, role filter |
| learn `#/learn[/<unit>]` | Seventeen units | "points on the flight plan", streaks (`unit-dark-1440-01.jpg`) | Units, sliders, checks |
| compare `#/compare` | Two methods side by side | "Agentic PDLC (this playbook)" (`compare-dark-1440-02.jpg`) | Twelve-row table |
| process `#/process[/<role>]` | Each role's steps with prompts | 14-word title wraps to three lines (`x-process-qa-1440.jpg`) | Six playbooks, ticks, prompt export |
| route `#/route[/<role-time-need>]` | Reading order by role and time | "Boarding pass", "Passenger", barcode (`route-sa-dark-1440-02.jpg`) | Shareable hash |
| effort `#/effort` | Chat, platform or code | Capitals badges (`effort-dark-1440-02.jpg`) | `.xef-tiers`, `.xtw`, exercise |
| gov `#/governance` | Gates, documents, who signs | Stock photograph with a dark caption bar (`gov-dark-1440-02.jpg`) | `#gv-gates .xfig`, RACI |
| toolkit `#/toolkit[/<id>]` | Seventeen calculators | Mascot in "How to use this tool" (`x-tool-bar-1440.jpg`) | Every calculator, its output |
| evidence `#/evidence` | The pack, its download | Photograph (`evidence-dark-1440-02.jpg`) | Pack list, Markdown download |
| overview `#/overview` | First-generation walk-through | Own rail and type; "Engineering Champion", "QA Champion" (`overview-dark-1440-01.jpg`) | Scenarios and ledger |
| sa, pm, eng | Role playbooks, 18 steps | On a phone the rail sits above the title: h1 at y=1,044 (`sheet-390-10.jpg`) | Steps, sample documents |
| guide `#/guide[/…]` | Reference, glossary, sources | "How to use this site"; table crushed on a phone (`sheet-390-04.jpg`) | Lineage and confidence marks |

## Part 2. The upgrade plan

Edit the source file; `build.py` refuses a build if the framed copy differs from it. Another worker is editing `frame.css` this round, so re-read it first.

**0. Write the test first** (new `site/tools/workbench.test.mjs`, 200 lines, no risk).

**1. Fix cold deep links** (4 lines, low). Remember the last id passed to `scrollToId` and call it again after `placeOpener()` and `crumbs()`.

**2. Fold the opener** (15 lines, low). Make `.opener` a closed `<details>`: "How to use this page". It returns 170 to 590px per page.

**3. Remove and rename** (about 60 lines of script, 120 of CSS deleted, low).

| What | Where | Action |
|---|---|---|
| Mascot | `skyMascot()` 4945, six call sites; `.sky`, `HERO_LINES` 4955; `.opener .om` 5102 | Return an empty string; delete the hero bubble and its timer |
| Ranks | `Q_RANK` 3882; `.rk` in `.xq-hud` 3920 and `.xclimb-hud` 4976 | Delete the cell, keep the counts |
| Points | `gHud()`, `.xpill.xpts`, "Points from checks", "best streak" 4555 | Stop rendering; keep reading and writing `skyways.game` |
| Exploration | `.xplore`, "points on the flight plan" 2120 | Remove |
| Old names | "PDLC Simulator" 6, 2837, 2851; "this simulator" 2954, 3860, 3919, 3929, 3949, 4354, 4823, 4975, 5069 | "Workbench", "this workbench" |
| Publisher | "by SkyWays Consultancy" 2837, 4963 | Delete; the footer signs it |
| Roles | "Engineering Champion", "QA Champion" 2131, 2132, 2375, 2742 | "Engineering lead", "QA lead" |
| Vault, side quests | 7 and 12 strings near 3895 to 3920 | "evidence pack", "simulations and tools" |
| Frame | "SkyWays Architect" in `build.py` 51 and 77, `frame.js` 11, 31, 110 | "SkyWays workbench" |

Leave "AIDD" (12 uses, the site's spelling) and the 86 "hard gate" strings; add "sign-off" beside the first on start, loopmap and gov. Six links in `render.py` and `pages/protocol.py` still say "in the simulator" for the workbench.

**4. Words** (10 strings, low).

| Now | Becomes |
|---|---|
| Product development for the agentic era, on one page | Run the numbers, follow your role's steps, read the case day by day |
| Welcome to SkyWays | The workbench |
| The whole simulator as one route | The ninety days on one map |
| End to end, one decision at a time | Practise nine decisions from the case |
| One picture that every page returns to | Four phases and eight loops in one picture |
| What this playbook teaches, on one page | Fifty-five concepts, one sentence each |
| What each role does anyway, done better, then done for an agent | Each role's steps, with a prompt for every one |
| Tell it who you are, and it issues your route | Say your role and your time, get a reading order |
| Stops cleared | Days answered |
| Agentic PDLC (this playbook) | SkyWays PDLC |

**5. Type** (12 lines and one font, low). Line 1004: `--display` starts with "Instrument Sans". Replace the Outfit face on line 652 with `site/assets/fonts/instrument-sans.woff2` as base64, the way Geist is already embedded on lines 650 and 651, so the file still works alone. `.xh1`, `.hero2 h1` and the `font-weight:800` rule at 921 go to 620 with -0.035em; delete the shadow at 1006. Delete the two unused B612 Mono faces on line 287. Keep Inter: SVG labels are measured in it (899, 924). Six "SF Mono" rules take `var(--mono)`. Capitals become sentence-case mono at 12.5px; nothing under 11px.

**6. Top bar** (`renderNav` 2836 to 2845, about 12 long lines; `frame.js` loses 45, `frame.css` 30; medium). One bar, as on the site: mark, "SkyWays", small "Workbench" linking to `#/start`; the five lists restyled; search; "Evidence pack n" as text; quiet link "Manual" (`../`); filled pill "Simulator" (`../simulator/`); the `◐` toggle. "Tutorial" (`../learn/`) heads the Learn list. On a phone the pill and Menu stay, and Manual and Tutorial lead the sheet. Remove `.xpts`, `#xshare`, `[data-openconcepts]`, `.xhome`, the Contact pill with `#xcontact`, the `.xlinks2` cards, and the frame's `strip()` and `navChip()`. Hide the three outbound links when `location.protocol` is `file:`.

**7. Theme** (1 line, a 40-line token block, about 470 declarations by codemod, 12 lines of toggle; high risk, so last).
- Today: ten `:root` blocks set 42 properties, the last wins. Colour ones: `--canvas --paper --ink --ink2 --soft --faint --line --line2 --navy --navy2 --board --bone --rule --slate --sage --ochre --plum --stage --ha --hb --p0` to `--p3`, `--pm --sa --eng --qa --red --grn --amb`; the hero has `--hbg --hfg --hfg2 --hline --hcard --hgrid`. They are used 1,847 times.
- Literals: 815 hex (176 distinct) and 101 `rgba()` in 820 CSS declarations: 140 white fills, 135 pale tints (61 distinct), 40 dark fills (34 are `#0B1437`), 99 white, 92 hue and 25 dark text colours, 108 borders. The script holds 883 hex, nearly all in SVG palettes `BB`, `IC`, `RC`, `HUES`. Of 475 inline `style` attributes, 69 set a colour, 19 with a literal; 226 only pass a hue through a property.
- Do: (a) the site's bootstrap line first in the head (`render.py` 295); (b) one final block with the site's light tokens, and its dark tokens under `@media screen{:root:not([data-theme="light"])}`, plus `--on`, `--ok`, `--warn`, `--stop`; (c) a codemod by table: white fills to `var(--paper)`, `#0B1437` to `var(--navy)`, white text on ink to `var(--on)`, tints to `color-mix(in oklab, hue 12%, var(--paper))`; (d) pictures stay on paper, as sketches do: re-declare the light tokens on `.ill, .xfig, .xscene, .xrt, .xvs-pic, .xmap, #lm-big, .xzm-w, .xcmap-w, .pg-pic, .prmap, [id^="illo-"]`; (e) retire `.hero2 .mode` and `skyways.heromode`; (f) in `simshots.mjs` set `manual-theme` to light before capture; (g) `build.py` line 75: theme-color becomes `#121316`.

**8. Density** (40 lines, low). Delete `body::before`, the rail tints, `.glass` blur and most shadows. On phones turn the playbook and guide rails into the chip row other pages use. Cut start to hero, map and four figures. Move back-to-top off the rail.

**Not now:** phase hues and "Specify": they change all ten pictures.

**Do not touch:** the router and every hash; the keys `skyways.pack, quest, game, learn, process, product, lens, jrole, rail, seen, tour.*, tours.off`; calculator `compute()` functions and the ids `tool-`, `tres-`, `tart-`; simulation and episode data; the SVG builders; the ten selectors in `simshots.mjs`; search, the tour, print rules, the pack download.

**Verify** (the test from step 0, both widths, both themes):
- Each route: no exception, an h1 in the first screen, no sideways scroll.
- No key: body is `#121316`. Toggle: `data-theme` and `manual-theme` flip, body is `#F7F6F2`. Contrast at least 4.5:1.
- `.xh1` computes to Instrument Sans when opened from `file://` with no network.
- The 15 links to a part of a page, loaded cold: target top between 60 and 140.
- Each calculator: change one input, the result changes, no "Check the values".
- Add to pack, reload: the count is 1. The NFR walk ends on "Added to the evidence pack".
- Seed today's saved state: the counts show.
- Page text holds none of: PDLC Simulator, this simulator, Your rank, Hi, I'm Sky, Champion, in the vault, streak.
- `simshots.mjs` writes 10 of 10 at today's pixel sizes.
