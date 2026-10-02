# Advisor: front-end reliability

I ran the frozen build in system WebKit (Safari 26.6's engine), motion on, with a runner at `SP/r7/engineer/wk`; `wk-*` shots are in that folder. Firefox is not installed here: nothing was seen in Firefox.

## What each browser sees today

- **CSS `d:` animation.** Safari has none, so it shows four still aircraft in turn. That works (`wk-home-t1.jpg` to `t5`). The dashed fragments show there too (`wk-home-plan-stage.jpg`): they are the P1 drawing itself, a dashed outline at 3.3 times size. Smoother easing will not cure it.
- **`linear()` spring.** Read from the code, not seen: Firefox under 112 drops the shape change; Safari under 17.2 snaps two funnel parts.
- **Cross-document view transitions.** Chrome and Safari 18.2 up: two pages lie on each other for a quarter second (`wk-vt-120ms.jpg`). Firefox: nothing.
- **`offset-path`, `color-mix`, `:has()`, `text-wrap`, scroll timelines.** All work in Safari 26. The globe costs 1.4ms a frame. The hero pause holds every hero loop and the globe, but not the simulator roll.

## Q1. Sketches: keep and triage

Refuse model pictures: 98 bitmaps, labels laid over by hand, nothing a gate can check. Inline SVG is small and sharp.

The cause is only half fixed. The sketches carry no paint of their own (`class="z zk"`, no `fill`), so any wrong or missing sheet turns them black again. The stamp cannot stop an old cached page asking for `base.css?v=old` and getting the new file, since Pages ignores the query. Write `fill="none"` and the stroke into the SVG.

Cut: `seven-stones-three-kinds`, `three-tokens-one-way`, `a-stand-in-the-right-size`, `measure-back-to-the-stake`, `plumb-line-after-the-wall`, `something-soft-underneath`, `lift-the-blanket`, `what-comes-out-of-the-exhaust`, `down-one-step`, `the-baton-on-the-track`, `the-last-sure-thread`, `the-third-adaptor-goes-home`. Then one per lesson: about 50 survive.

Recurring faults: labels touching the sheet edge (`tap-turned-down-to-the-drain`, `leaking-on-schedule`); props nobody can name without the label; one standing pose; faint grey lines across the worker, like a glitch.

Keep the home sample, with its own paint.

Check: the build fails if any `svg.sk` shape lacks `fill` and `stroke` attributes; a gate pass blocks `*.css` and fails on a black fill larger than the worker; every label's box sits inside the sheet and off other labels; the build writes the sheet of all sketches for a person.

## Q2. Hero: yes to one canvas, with three removals

One canvas and one clock ends the split where Safari runs different code from Chrome. Conditions: the clock counts elapsed time, as the globe's does now; `window.Hero.seek(t)` exists for the gate; pixel ratio capped at 2; the still SVG already made for the social card shows when there is no script; reduced motion draws one frame; the phase line is HTML.

Remove drag. On a phone the globe sits where the thumb scrolls, Safari's back swipe starts at its edge, and drag has no rule for paused.

Remove the dashed plan stage. Keep the shape change the owner asked for: every shape solid, the same count of corner points, about 24px long. Remove the pills, as proposed.

Check: the gate seeks twelve times round a lap at 1440, 1024, 768 and 390 in both themes. No label box meets another or a floating button. The picture ends inside the first screen at 390 by 844 (today it runs from 572 to 993). A frame costs under 6ms at quarter speed. It writes a contact sheet a person must open.

## Q3. Simulator band

One still crop of the building at a whole-number pixel scale. Beside it, one day's decision as real HTML: the headline and three choices with their price in days, each linking to `/simulator/#day-45`. No roll, no browser frame, no caption, no second pause button.

Check: no text in an image; smallest text 14px at 390; the band fits one screen at 1440 by 900 and one and a half at 390 by 844; the image has width and height set.

## Q4. Motion

Remove: view transitions; notes fading into sketches and parts into figures; the 2.2 second funnel assembly; the simulator roll; the spring curve.

Keep: the hero flight, the plain section rise, scroll-led dashes, the copy tick, the game's four.

Rule: motion never hides or delays what the reader could already read. If the gate cannot film it, it does not ship.

## Q5. Faults not yet named

1. Sketch notes blink. Lesson `p0-frame`, 1440 dark: with 100px of the sketch on screen nine notes are at opacity 1; 60px later they are at 0, then return (`wk-blink-1-before.jpg`, `wk-blink-2-after.jpg`).
2. The funnel band is nearly empty for two seconds after scrolling to it (`SP/r7/base/home-dark-1440-02.jpg`, `wk-walk-02a.jpg`).
3. At 390 dark the round to-top button covers text: "four phases, one loop", "Seven ways these projects fail", "MIT licence" (`home-dark-390-02`, `-03`, `-10`).
4. Flow map text in that lesson measures 8px at 1440 and 6px at 390 (`lesson-dark-1440-02.jpg`).

Do not change: the methods table (`home-dark-1440-03`); the globe's dot drawing and its stop rules; the gate's no-script, reduced-motion and print passes.

## What the gate must add

1. WebKit and Firefox passes (Playwright, a download needing the owner's yes; until then `wk` covers WebKit).
2. Film through the seek hook, not one moment.
3. Fixed buttons against text at 390 and 768, every screenful.
4. Cache: fail if a local stylesheet or script address lacks `?v=` equal to its hash; after deploy, compare the live files.
5. The blocked-stylesheet pass.
6. Pixel ratio 2 and 3; resize 1440 to 390 and back; a tab opened in the background, then shown.
