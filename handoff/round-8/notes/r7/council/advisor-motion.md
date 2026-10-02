# Advisor: the motion designer

## Q1. Sketches: keep and triage

They are good: one character, one hand, real type. Refuse model pictures: they cannot letter, hold the character or follow the theme. Recurring faults:

1. Four or five notes where the style wants three: `a-hair-above-the-mark`, `measure-back-to-the-stake`, `something-soft-underneath`. Repair.
2. Props nobody can recognise: `lift-the-blanket`, `the-last-sure-thread`, `a-glass-on-the-wild-mushrooms`, `what-comes-out-of-the-exhaust`, `three-tokens-one-way`, `a-stand-in-the-right-size`, `where-the-two-tracks-part`, `the-third-adaptor-goes-home`, `raw-fish-gets-its-own-board`. Cut.
3. One idea drawn twice: `a-slow-puncture` (repeats `measure-back-to-the-stake`), `a-sign-or-a-sizer` and `only-the-chips-it-holds` (repeat `a-notice-where-the-valve-should-be`). Cut.

About 85 survive. Cap the sheet at the prose width: at 760px it is the brightest, largest thing on a dark lesson (`lesson-dark-1440-03`). Keep the home sample, but swap it for `the-needle-never-shakes`, which reads cold. "38 minutes, 240 a day" does not.

## Q2. Hero: the chairman's picture is right, with three cuts

Seen today (my frames, `SP/r7/motion/`): the aircraft is 90px on a 490px globe and covers the P3 pill (`c10`); it crumples on the first bend (`c0`); the globe turns about as fast as the aircraft flies, so two things fight.

Build this (R is the globe's radius):

- **Canvas** 2.9R wide, 2.3R tall. Each frame: back arcs, then the disc and dots, then front arcs, trail, aircraft. Everything is a function of one elapsed time; pause stops it.
- **Helix** radius 1.3R, tilted 18 degrees so the front arc climbs left to right, seen 12 degrees from above. Each lap rises 0.14R and the whole helix sinks at that rate, so the aircraft holds its height. Three coils: the current one at full strength, the one below at 30%, the one under that at 10%. They fade, never clip. Line 1.5px. Front arc in the four hues, back arc one grey-blue at 35%.
- **Timing** 30s a lap: 22s in front at steady speed (5.5s a phase), 8s behind, speed blended over one second each side. No hold at the sign-off: an aircraft that stops in the air reads as a stutter.
- **Aircraft** 0.11R long (27px at 1440), seen from above, ink colour, turned to the path, full size near, 70% far. Yes, it changes shape: three outlines with the same twelve points in the same order. Dart in P0, airliner in P1 and P2, jet in P3. Points ease over 500ms at the boundary. It is an outline until the sign-off and fills solid there in 400ms; that is the one event worth watching. It turns back into the dart while hidden behind the disc. No dashes, no flame, no shadow.
- **Trail** the last 0.9R of path, tapering from 2.5px and 90% to nothing, in the hue of the phase it lies in.
- **Sign-off** a rose tick 0.06R long across the path at 45%. It brightens and grows by half for 400ms as the aircraft crosses.
- **Globe** one turn in four minutes. Keep its two-second spin-down on arrival; that is the whole entrance.
- **Legend** one line of real type under the globe. Current phase at full ink, the others at 45%, 250ms change.
- **Still frame** (reduced motion, print, paused): solid airliner just past the tick, trail behind it, three coils, all four names at full strength.
- **Phone** R is 27vw so the ring fits 390. Buttons side by side and the counts moved under the globe, so it fits the first screen.

Remove from the proposal: drag (a hidden gesture that explains nothing and fights the scroll on a phone), the hold, and node dots on the path.

## Q3. Simulator band: one move of the game

Show one room at whole-number pixel scale (the Day 45 QA room) and under it the real question in real type, "Day 45. The first test score is 82.4. The promise was 80.", with its choices as buttons that open `/simulator/#day-45`. No browser frame, no tilt (it softens every pixel in `home-dark-1440-06`), no rolling, no caption. Nothing moves. At 390: room 358px wide, headline, choices stacked, under one screen.

## Q4. Motion

Remove: the home bands rising on scroll; the staggered notes in sketches; the top-bar pill morph (keep a plain 150ms page cross-fade); the spring (one curve for the site); the rolling simulator pictures; the funnel's 2.2s assembly. Show the funnel complete and draw only its phase bar, 600ms.

Keep: the hero flight, the globe's arrival, the game's four animations if each answers a press.

Rule: if the still frame says the same thing, it stays still. Motion is for a thing that is itself a movement, or an answer to the reader's hand. Never hide words to animate them in.

## Q5. Faults nobody has named

1. Home section two, 1440 dark: 0.9s after a scroll the phase names are still withheld and the screen is three quarters empty (`home-dark-1440-02`).
2. Hero depth is false: the upper coil crosses in front of the globe's left limb and fades out mid-disc (`c13`).
3. Hero: nothing flies for 8 of every 32 seconds (`c12`, `c13`).
4. Phone: the back-to-top button sits on text and links (`home-dark-390-03`, `-07`, `-08`).
5. Lesson flow map text is about 9px at 1440 (`lesson-dark-1440-02`).
6. Lesson column has three widths: prose 640, sketch 760, diagram 944 (`lesson-dark-1440-03`, `-06`).
7. The funnel reads "back to Frame , with what you learned": a space before the comma (`f-2500`).

Do not change: the dotted globe's rendering; the methods table with the sign-off line through it (`home-dark-1440-03`); the funnel's final frame (`f-2500`).
