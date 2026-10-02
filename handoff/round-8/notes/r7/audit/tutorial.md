# Tutorial audit (lesson index, track page, ten lessons)

Looked at 12 pages at 1440, 1024, 390 and 320, dark and light, motion on, every screen to the foot (about 1,400 shots), plus filmed scroll-ins and clicks. Screenshots are under `SP/r7/tutorial/` (`walk/`, `sheets/`, `shots/`, `nav/`, `film/`).

## 1. Findings, most serious first

1. **BROKEN. The top bar does not fit between 981 and 1031px.** Track page at 1024, both themes: the theme toggle is half off the right edge and the page scrolls sideways by 7px (41px at 990). Lessons with "Play this day" do the same from 981 to 1004. Shots: `walk/track-dark-1024-01.jpg`, `shots/hd-gate-dark-990.jpg`. Cause: `.hd .in` is one no-wrap row; `.brand small` hides only at 980 and `.hd .quiet` only at 900, so "Find your start" + "Simulator" (230px) or "Apply it" + "Play this day" (205px) cannot fit (`render._ctx`).

2. **BROKEN. Every sketch and figure blinks as it arrives** (all lessons, widths and themes). It is on screen complete, then the whole drawing drops to nothing and fades back, notes last. On a phone more than half the sketch is showing when it vanishes. Shots: `sheets/film-p0-sk0-390.jpg` (frames s01, s02, s04), `sheets/film-p0-sk0.jpg`, `sheets/film-p0-fig.jpg`. Cause: `engine.js wireFigures` adds `fig-in` only when the top passes the 88% line (`rootMargin -12%`) and nothing is hidden before that; `.fig-in>*` in base.css also matches the sketch's own svg, so all 57 parts fade from zero, not only `[data-an]`.

3. **POOR. Flow maps and charts are too small to read.** At 1440 flow map text is about 8px (the contract's floor is 11px). At 1024 the map is cut on the right with no hint that it scrolls. At 390 it is 6px inside a sideways scroller, and `figure.fig` charts shrink to 358px with 6 to 7px text. Shots: `walk/whatis-dark-1440-07.jpg`, `walk/gate-dark-1024-02.jpg`, `walk/p0-dark-390-07.jpg`, `sheets/bolts-dark-390-1.jpg` (screen 02). Cause: `.bbw svg.bb{width:100%;min-width:700px}`; the `.bbw::after` hint shows only under 740px; `.prose .fig` has no minimum size.

4. **POOR. Tables on a phone.** The middle column wraps at one or two words a line (cells 14 lines tall) while the last column is sliced mid-word at the edge, and nothing says it scrolls. Every "Apply it in your role" and "Sources" table, and "Start where you are" on the index. Shot: `walk/whatis-dark-390-18.jpg`. Cause: `thead th{white-space:nowrap}` with `table{width:100%}` and no column minimum inside `.prose .tw`.

5. **POOR. Floating buttons sit on reading text.** Phone: the white back-to-top disc and the mail disc cover the first and last words of two lines on most screens, headings and figure labels included (`walk/p0-light-390-03.jpg`, `walk/p0-dark-390-07.jpg`). At 1024 the bottom-left button covers lesson numbers in the rail and the mail button covers line ends (`walk/gate-dark-1024-01.jpg`, `walk/gate-dark-1024-02.jpg`). Cause: `frame.css .sw-top` and `.sw-pill`, and `.tour-fab`, are fixed 12 to 18px from the edges with no gutter kept; `.lrail` starts at 24px.

6. **POOR. "Copy" is printed over the first line of code** wherever the block is wider than its box (1024 and phones). Shots: `walk/bolts-light-1024-10.jpg`, `walk/p0-dark-390-14.jpg`. Cause: `.codebox .cp{position:absolute;top:9px;right:9px}` with no room kept in `.prose pre`; under 820px `.cp{min-height:44px}` makes it cover two lines.

7. **POOR. The left rail does not show where you are.** On a lesson in a late track (GenAI interview questions) and on a track page (Running delivery) the rail opens at its top and the current item is below its fold. On a phone "All lessons" opens 2,900px of list from "Start here"; the current lesson is three and a half screens down. Shots: `walk/interview-dark-1440-01.jpg`, `walk/track-dark-1440-01.jpg`, `shots/lnav-interview-dark-390.jpg`. Cause: `learn.py _rail` sets `aria-current` but nothing scrolls it into view inside `.rail{overflow-y:auto}`.

8. **POOR. On a phone "On this page" is a shut box with no arrow**, so it reads as an empty card. Shots: `walk/p0-dark-390-01.jpg`, `shots/otp-p0-dark-390.jpg` (open, still no marker). Cause: `.otp>summary{display:flex}` under 820px removes the marker; `guide.js foldOnPhones` shuts it.

9. **POOR. At 320px the wordmark touches the pill** ("SkyWaysSimulator", 5px apart) and the toggle is 5px from the screen edge. Shot: `walk/p0-dark-320-01.jpg`. Cause: the row is 9px wider than `.hd .in`; only "Play this day" has a short label, "Simulator" does not.

10. **POLISH. Phone breadcrumb** wraps with a stray "›" starting the next line and 44px between lines (three lines at 320). Shots: `walk/p0-dark-390-01.jpg`, `sheets/gate-dark-320-a.jpg`. Cause: `.crumbs li+li::before` and `.crumbs a{min-height:44px}`.

11. **POLISH. Phone footer:** "MIT licence" sits 24px lower than the copyright line beside it. Shot: `walk/p0-dark-390-18.jpg`. Cause: `.ft .lg a{display:inline-flex;min-height:44px}`.

12. **POLISH. Track page:** two hairlines 29px apart under the counts. Shot: `walk/track-dark-1440-01.jpg`. Cause: `.lmeta` bottom border, then the first row's rule in `.lcards`.

13. **POLISH. The small model figure is centred** while text and sketches are left aligned, so it hangs to the right of its paragraph. Shot: `walk/gate-dark-1440-06.jpg`. Cause: `.prose figure.lmodel{margin:6px auto 26px}`.

14. **POLISH. Capitals with wide tracking:** "WHAT THE HARD GATE IS" on the P0 to P3 board. The contract says never. Shot: `walk/whatis-dark-1440-02.jpg`. Cause: `.dgb .bkey .bxt{text-transform:uppercase;letter-spacing:.05em}`.

15. **POLISH. Three sketches run the orange path arrow along the paper's bottom edge** (both hard gate sketches, the case study belt), and "from outside" sits about 8px from the left edge (guardrails). Shots: `sheets/sk-390-dark-a.jpg`, `sheets/sk-390-dark-b.jpg`. Cause: coordinates in those sketch files.

16. **POLISH. Light theme: the sheet is white on off-white with no edge**, so it reads as a pale patch, not paper. Shot: `walk/gate-light-1440-05.jpg`. Cause: `.sk-paper` has no border; `--sk-paper:#FFFFFF` on `#F7F6F2`.

## 2. Good, do not change

1. **The sketches themselves.** All 20 render whole at 320 and 390 once settled, no part stays hidden, handwriting is 13.4px or more, the caption is readable, there is 14px above and 30 to 44px below, and none touches a table, code block or another picture (`sheets/sk-390-dark-a.jpg`, `sheets/sk-320-light-a.jpg`). The dark theme's paper card sits well.
2. **The pill.** "Play this day" opens the right day of the game (15, 30, 75), the pill becomes "Read the lesson", and the change is a clean quarter-second cross-fade with no broken frame at 1440 or 390 (`sheets/nav-gate-play.jpg`, `sheets/nav-gate-play-390.jpg`). "Apply it" lands with its heading clear of the bar (`nav/p0-apply-f99-after.jpg`).
3. **Lesson to lesson and track to lesson handover** (`sheets/nav-track-lesson.jpg`, `sheets/nav-p0-next.jpg`), the progress bar, the "next lesson" block and the plain FAQ.
4. **No sideways page scroll at 320, 390 or 1440** on any page; tables and code scroll inside their own boxes; no script errors in 96 page loads.
5. **The markdown twin** (`/learn/p0-frame/index.md`) is well formed: headings, tables, the folded answer, absolute links, and both images resolve.
