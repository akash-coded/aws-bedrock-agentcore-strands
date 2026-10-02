# Home page audit (http://localhost:8833/)

Looked at 1440x900, 1280x720, 1024x768, 768x1024, 390x844, 320x640, dark and light, motion on.
Screenshots are in `SP/r7/audit/home/`. CSS line numbers are `site/theme/base.css` unless stated.

## Known faults, one line each (not re-reported)

- Aircraft breaks into dashes while changing shape. New detail: at the left turn the dart is a kinked outline pointing backwards (`dd-library-dark-1440.jpg`, `z5-herotext-dark-1280.jpg`, `dd-roles-light-768.jpg`); the jet flies over the P3 pill (`t-27s-dark-1440.jpg`).
- Phase pills collide and sit on the globe; "the next round" is clipped; pills overlap at 768 and on a phone; the phone globe is cut by the first screen.
- Simulator band is a shrunken whole-page screenshot with a mono caption. New detail: the screenshot carries its own site header and mail button, so at 768 two mail buttons stack (`b-dark-768-simulator-1.jpg`).

## Findings

1. **BROKEN. Floating buttons cover content. All bands, every width under about 1400, both themes.** Back-to-top occupies x 18 to 60 while content starts at 24. It hides the "OPS" code and the edge of "Play Ninety Days" at 1280 (`b-dark-1280-roles-1.jpg`, `b-dark-1280-simulator-1.jpg`), "Practice" at 1024 and 390 (`b-light-1024-tutorial-1.jpg`, `b-dark-390-tutorial-1.jpg`), "BMAD Method" at 320 (`b-dark-320-method-1.jpg`), the copyright at 768 (`b-dark-768-FOOT-1.jpg`). The mail button hides "116 prompts" in the 320 hero (`home-dark-320-t2.jpg`) and the simulator's pause control at 1280. Cause: `site/frame/frame.css` `.sw-top{left:18px}`, `.sw-pill{right:18px}` against `.wrap{padding:0 24px}`.

2. **BROKEN. "Why" band, 1024, both themes.** The dashed loop line runs through the "LC" of "SkyWays PDLC"; the four method labels wrap to three lines and touch each other (3px between "per decision" and "Spec-driven"); "four phases, one loop" wraps. `z4-core-light-1024.jpg`, `z2-spine-dark-1024.jpg`. Cause: `.sp-core a{width:12%}` with `.sp-core a b{white-space:nowrap}` (1534, 1535) overflows into `.sp-loop{left:-20px}` (1507); `.spine .sp-in{width:15.4%;grid-auto-rows:44px}` (1529).

3. **BROKEN. Hero, 320, dark and light.** The "P0 Frame" pill is cut in half by the bottom edge of the hero. `home-dark-320-02.jpg`. Cause: pill positions in `pages/globe.py` against the hero's clipped height under 1000px (1904 area).

4. **POOR. Section heads, 1024 and wider, both themes.** The gap from eyebrow to heading is 18px in "why", "method", "library", 34px in "tutorial" and 63px in "roles" (measured). One-line headings drop away from their eyebrow. `b-dark-1440-roles-1.jpg` beside `b-dark-1440-why-1.jpg`. Cause: `.sec-h.split{align-items:end}` (1468).

5. **POOR. "Why" figure, 768 and wider, both themes.** The loop label reads "back to Frame , with what you learned": a space before the comma. `z-spine-dark-1440.jpg`. Cause: `.sp-back{display:inline-flex;gap:7px}` (1511) with the tail in its own `<span>` in `pages/spine.py` `figure`.

6. **POOR. Footer, 768 and below, both themes.** Three different left edges on one phone page: hero 20px, bands 24px, footer 16px (measured). The copyright sits 11 to 24px above the links beside it, link rows are unevenly spaced, and at 768 the footer is one 1042px column with the right half empty. `b-dark-768-FOOT-1.jpg`, `b-dark-390-FOOT-2.jpg`. Cause: `.ft .in{padding:0 16px}` (323), `.hero2 .in{padding:52px 20px 0}` (1441), `.ft ul a,.ft .lg a{min-height:44px}` (1803) with no `align-items:center` on `.ft .lg`.

7. **POOR. Footer links, all widths, both themes.** Blue underlined links, the only blue text on the page; they look like unstyled browser links next to the white "more" links above. `home-dark-1440-09.jpg`, `ft-hover-light-1440.jpg`.

8. **POOR. "Why" figure, 390 and 320.** The methods become bordered boxes in a ragged 2, 1, 1 stack; "SkyWays PDLC" and "four phases, one loop" each break into two lines beside the small line. `b-dark-390-why-1.jpg`, `b-dark-320-why-1.jpg`. Cause: the under 1000px rules for `.sp-in` and `.sp-core` (1552 to 1575).

9. **POOR. Light theme, 390 and 768.** The globe's glow is a grey smear behind the lede and both buttons (`home-light-390-t3.jpg`). The simulator frame's shadow shows as a grey smudge across the hairline into the tutorial band (`b-light-390-simulator-2.jpg`, `b-light-768-tutorial-1.jpg`). Cause: hero glow in `.hero2 .scene`; `.simshot` shadow not clipped by `.band.play`.

10. **POOR. Hero, dark, all widths.** Stars sit under the words. One lands right after "teaches" and reads as a full stop ("It teaches. one way"); another sits inside the "Play the simulator" button. `z5-herotext-dark-1280.jpg`. Cause: the star field in `pages/globe.py` `scene` is drawn behind `.hx`.

11. **POOR. Roles menu against the roles band, 1024 and wider.** The menu says "Engineering lead: From a story file to a shipped bolt" and "QA lead: From 'it works' to a number you can defend" (the same ending as Product manager). The band says "a written task, code that ships" and "proof that it works". `dd-roles-dark-1440.jpg` beside `b-dark-1440-roles-1.jpg`. Cause: `render._nav` uses the `ROLE_ORDER` taglines; `HOME_ROUTE` fixes only the band.

12. **POLISH. Method table, 768 and wider.** The P2 heading and its "adds" text start 11px right of the P2 bars; P0, P1 and P3 line up exactly. `methT-6000.jpg`. Cause: `.cover thead th.gated{padding-left:14px}` against `.cover tbody td.gated{padding-left:3px}` (1600, 1601).

13. **POLISH. Mail and back-to-top buttons, both themes.** The mail button's hover label "Ideas & contact" is in the system font (`hov-mail-dark-1440.jpg`); `font:600 13px/1 inherit` in `frame.css` `.sw-pill` is invalid and dropped. The mail button is always black (nearly invisible on dark) and back-to-top always white (the brightest thing on a dark page). Both stay lit above the menu's scrim (`drawer-dark-1440.jpg`).

14. **POLISH. Roles band, 390.** The route wraps after two or three words with about 90px unused ("a vibe, a number you / can defend"). `b-dark-390-roles-1.jpg`. Cause: `.s-route` at 1649.

15. **POLISH. Hero, 1280x720.** The hero is 746px tall, so the pause control is cut by the fold and sits against the mail button. `home-dark-1280-t1.jpg`.

16. **POLISH. Top bar and headline, 320.** The wordmark is 4px from the Simulator pill; the headline breaks as "software with / AI agents.", so the grey sentence starts mid line. `home-dark-320-t2.jpg`.

17. **POLISH. Tutorial band, 390.** The arrow of "From lesson 3 of..." floats at the far right, away from the wrapped text. `b-dark-390-tutorial-2.jpg`. Cause: `.learn-k{display:inline-flex;gap:8px}` (1715).

18. **POLISH. Simulator frame, hover.** The fake window title "Ninety Days" gets a link underline. `sim-hover-dark-1440.jpg`.

19. **POLISH. Gutter, 1024 to about 1330 wide.** Headings start 24px from the screen edge, tight beside roomy bands. `home-dark-1280-t1.jpg`. Cause: `--wrap:1280px` with a fixed `padding:0 24px`.

## Good, do not change

1. The method table at 1440 and 768 in both themes: bars, sign-off line and legend read at a glance (`b-light-1440-method-1.jpg`).
2. The lifecycle figure at 1280 and 1440: it assembles in under 2.5 seconds and its last frame is complete (`whyT-2500.jpg`).
3. Role rows and library tiles, with their hover states (`z-seats-hover-dark-1440.jpg`, `lib-hover-dark-1440.jpg`).
4. Controls behave: pause holds flight and globe, the simulator pause works, the theme switches at once, drawer and menus close on Escape (`pz-3s-dark-1440.jpg`, `tgl-120ms-dark-1440.jpg`).
5. Measured: no small text under 4.5:1 or under 11px in either theme, no sideways scroll at any width, no script errors.
