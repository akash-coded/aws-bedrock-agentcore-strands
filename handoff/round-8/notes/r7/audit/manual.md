# Manual and library pages: visual audit (round 7)

Build looked at: http://localhost:8833. Widths 1440, 1024, 390, 320; dark and light; motion on.
Screenshots are in `M` = `handoff/round-8/notes/r7/manual/`.
No page scrolls sideways at any width and no page throws a script error. Faults are the same in both themes unless said.

## 1. Findings, most serious first

1. **BROKEN. Stray brackets and colons left by the dash sweep, in text people copy.** /templates/, /prompts/, /product-manager/, /solution-architect/: `**Pain** (<what happened>` then `**Evidence**) <trace id>`, `**Fix**) where that control...`. /frameworks/ acronym table, "From" column: AIDD ":", BMAD ":", RACI "(", SDD ")", p^n ":". The two-number figure (PM step 8 and the picture pack) shows "(" and ")" as baseline values. Shots: `templates-dark-1440-12.jpg`, `frameworks-dark-1440-07.jpg`, `frameworks-dark-1440-08.jpg`, `pic-two-numbers-dark.jpg`. Cause: `content/roles/_src/product_manager_c.py` lines 389 and 420 (and the architect source), `content/library/frameworks.json` decoder rows, `pages/figures.py` line 220.

2. **BROKEN. /pictures/, dark (the default): all ten "From the simulator" cards have no picture**, only a title and links. They show in light. Shot: `pics-filter-sim-1.jpg`. Cause: `pages/pictures.py` (about line 161) writes one `<img class="light">` for these; `base.css` line 1150 hides `.pic img.light` in dark.

3. **BROKEN. Search in the drawer on a phone (390 and 320).** Each result is three columns in a row, so a title reads one word per line ("The / Hard / Gate: / The / Hand-off"). Fine at 1440. Shot: `nav-390-search-gate.jpg`. Cause: `base.css` line 1318, `.menu li>a{display:flex}` in the phone block, beats `.mr a{display:grid}`.

4. **BROKEN. /frameworks/ figures, 1440, both themes: labels collide.** "Merge" figure, P3 column: "Learn and adjust, into the next brief" spills out of its box and "hand-off further" is struck through by the border. "Traditional vs agentic": the "AI-fit verdict" chip sits under "eight-field spec"; "P1 · Design & Spec" touches its box edge. First figure: "code generated from the spec," and "PRD.md and" touch the cell border. Shots: `zoom-fw-merge-p3-dark.jpg`, `zoom-fw-vs-agentic-dark.jpg`, `zoom-fw-methods-cells-dark.jpg`, `frameworks-light-1440-03.jpg`. Cause: `pages/bb.py` `node()` and `wrap()` size boxes from an estimated text width. Note: this build's /frameworks/ has no funnel figure and no bar table; its five figures are these.

5. **BROKEN on a phone. Figures shrink until the words cannot be read.** /method/ loops board: labels are 3.2px at 390, 2.5px at 320. Role-page figures (bolt plan, two numbers): about 5px. /frameworks/ figures: about 6px behind a sideways scroll. Shots: `method-dark-390-06.jpg`, `sheet-rolefig-390.jpg`, `frameworks-dark-390-02.jpg`. Cause: `.dgs svg{width:100%}` (line 688) with no minimum width; `figure.fig svg` the same.

6. **POOR. The guide button is covered by the back-to-top button on every wide page once it scrolls.** Both sit at left 18px, bottom 18px; the arrow is on top. Shots: `pm-dark-1440-01.jpg` (guide), `pm-dark-1440-02.jpg` (arrow in its place), `fab-overlap-scrolled.jpg`. Cause: `.tour-fab` (`base.css`, z-index 8990) and `.sw-top` (`frame/frame.css` line 131, z-index 9000).

7. **POOR. The floating mail and back-to-top buttons cover words** at 1024, 390 and 320 on every page: line ends, the "Owner" label, list numbers, the start of a heading. Shots: `method-dark-390-02.jpg`, `pm-dark-390-08.jpg`, `pm-dark-1024-01.jpg`, `method-dark-1024-06.jpg`. Cause: `.sw-pill` and `.sw-top` in `frame/frame.css` are fixed over the text column; nothing keeps the column clear of them.

8. **POOR. Page change between the manual and the simulator reads as a glitch in the top bar.** For about 200ms the menu words are doubled ("Rolesrial", "Metnod"), then the pill is gone, then a different pill appears. Role page to /method/: the same doubling, and "Product manager" hangs as a ghost. Manual page to manual page (/method/ to /protocol/) is a clean short cross-fade. Shots: `vt/vt-method-1-f04-273ms.jpg`, `vt/vt-method-1-f07-288ms.jpg`, `sheet-vt-role-to-method.jpg`, `sheet-vt-method-to-protocol.jpg`. Cause: `.hd{view-transition-name:site-bar}` fades two bars whose menus sit at different places; `render._ctx` names the pills `ctx-sim` and `ctx-read`, so nothing travels, and `ctx-in` waits 120ms.

9. **POOR. /method/ delegation board: each phase label is a big empty dark slab** with a small "P0" in its corner, full width on a phone. Shots: `method-dark-1440-06.jpg`, `method-dark-390-09.jpg`. Cause: `pages/dg.py` line 152 uses `class="lk"`, which picks up the card rule `.lc,.lk{display:grid...}` at `base.css` line 856.

10. **POOR. /method/ role matrix is cut mid-word.** At 1024 the P3 column loses about 30px ("kee", "name"); at 390 only half a column shows, with no cue to scroll. Shots: `method-dark-1024-06.jpg`, `method-dark-390-08.jpg`. Cause: `.dgm` columns `minmax(196px,1fr)` inside `.dgmw` (lines 629 to 631).

11. **POOR. Old names.** "Try it in the simulator" (four times on /frameworks/) and three /protocol/ links ("The simulator's thirteen episodes") open the workbench. /frameworks/ says "playbook" eight times, "hard gate" eleven times and never "sign-off"; "spine" eleven times beside "P0 to P3", "SkyWays PDLC" and "one loop" for the same thing. /method/ has the eyebrow "The spine", board labels "Hard gate", and a page title with "one hard gate". The picture "The agentic PDLC in one picture" says "from its own chair" and "Click a phase to open it" inside a still image. Shots: `frameworks-dark-1440-02.jpg`, `frameworks-dark-1440-08.jpg`, `protocol-dark-1440-19.jpg`, `method-dark-1440-01.jpg`, `pic-frameworks-spine-dark.jpg`. Cause: `render.py` lines 1085 to 1125, `pages/protocol.py` lines 217 and 683, `content/library/frameworks.json`.

12. **POOR. /method/ tower figure.** Labels are 7.7px at 1440 and 5.3px at 390; in dark the clouds are near-black smudges; a plane sits on the lock; the label says "hard gate". Shots: `twr-t1.jpg`, `twr-t2.jpg`, `method-dark-390-01.jpg`. Cause: `svg.twr`, viewBox 640 wide with 10px text, drawn at 491px or less.

13. **POOR. Tables on a phone.** Role pages: the "Tool" column takes half the width and the advice runs three words a line. Four-column tables on /protocol/ and /frameworks/ run one or two words a line and still scroll. Shots: `pm-dark-390-07.jpg`, `frameworks-dark-390-03.jpg`, `sheet-390-b.jpg`. EXPERIENCE.md lists this as not done.

14. **POOR. Phase colours change between pages.** /frameworks/ figures paint P0 green, P1 blue, P2 violet, P3 orange. On role pages every phase chip in a step head is the role's one colour. Shots: `frameworks-dark-1440-03.jpg`, `pm-dark-1440-09.jpg`. Cause: `--bb-*` hues in `pages/bb.py`; `.step .ph .pd` (line 744).

15. **POOR. Not-found page.** No top bar, no mark, system font, and "The SkyWays simulator, which used to be at the root". Shot: `nf-dark-1440-01.jpg`. Cause: `site/404.html` is a separate file with its own styles.

16. **POLISH. Top bar at 320:** the name ends 5px from the pill and the menu button is 2px from the edge. At 1024 on a role page "The agentic manual" is 10px from "Tutorial". Shots: `method-light-320-01.jpg`, `pm-dark-1024-01.jpg`. Cause: `.hd .in` padding and gap under 860px (line 116).

17. **POLISH. Phone gutters differ.** Role, /protocol/, /templates/ and /prompts/ text starts at 16px under a breadcrumb at 24px; the footer is 16px under 24px pages; "MIT licence" sits lower than the copyright line. /templates/ and /prompts/ open with the "By role" list above the title. Shots: `pm-dark-390-01.jpg`, `method-dark-390-15.jpg`, `sheet-390-a.jpg`.

18. **POLISH. Small things.** Capital labels with wide tracking ("WHAT THE HARD GATE IS", "TRY IT IN THE SIMULATOR", "WHAT IT MEANS") against DESIGN.md. Loop label ends "the sponsor's". Governance is listed under "back from production" but drawn P0 to P3. "judgement call?." on /templates/. /protocol/: the last list row touches the callout and a link touches the columns above it. /models/: "1 of 12" floats mid-row. Shots: `method-dark-1440-03.jpg`, `templates-dark-1440-02.jpg`, `protocol-dark-1440-18.jpg`, `protocol-dark-1440-08.jpg`, `models-dark-1440-02.jpg`.

## 2. Good, do not change

- Role pages at 1440: the rail that marks the step, the roadmap, the step cards, and Copy turning green with a tick (`role-1440-copied.jpg`).
- The top bar never overlaps or wraps from 1440 down to 320, and the Roles and Library menus and the drawer open cleanly on a wide screen (`nav-1440-roles.jpg`, `nav-1440-drawer.jpg`).
- The cross-fade between two manual pages (`sheet-vt-method-to-protocol.jpg`).
- /protocol/ as a whole: numbered sections, ruled columns, calculators, the maturity check (`protocol-dark-1440-10.jpg`).
- /method/ phase board at 1440 and stacked on a phone, in both themes (`method-light-1440-02.jpg`, `method-dark-390-04.jpg`).
