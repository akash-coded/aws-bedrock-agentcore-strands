# Review 4: the one who ships it

My own frames of the prototype are in `SP/r7/review4/`.

## Part 1

**Strongest: C.** It alone says how each verdict is checked, and it alone saw that the cause is half fixed: the sketches carry no paint of their own, so any stale or missing stylesheet turns them black again. A is the best build spec, and the prototype follows it.

**Biggest blind spot: E.** It refuses the shape change on the evidence of the old 90px hero, and it orders fifteen redraws with no check in a round about mistakes. In the prototype the change is clean in every clip (`review4/a2`, `a4`, `a6`, `j2`, `j4`).

**All five missed:**

1. The order of release. Nobody split the work so a fault can be traced and reverted: deletions first, then the hero, then the new simulator band.
2. The owner has not yet seen the sketches drawn correctly. A cull to 50 acts on a verdict the owner never gave.
3. The widths between 390 and 1440. At 1024 the phase line wraps, leaving "P3 Run & Learn" alone, 13px from "by Akash Das" (`review4/home-dark-1024-t2.jpg`).
4. The eight seconds behind the Earth: no aircraft, no name lit (`p3/home-dark-1440-t6.jpg`).

## Part 2

1. **Sketches: cut the named weak ones, no quota; about 75 survive.** Cut what two or more advisors named (about 22), because a quota removes good pairs (`p0-frame` has two that read cold) and keeps a weak single. Check: the build's sketch check passes, a person opens the redrawn sheets, and a pass with the stylesheet blocked shows no black fill.
2. **Home sample: keep, swapped to `the-needle-never-shakes`.** It reads cold and comes from lesson one, where that band sends the reader.
3. **Shape change: keep as built.** The owner asked for it, and it is clean at 1440 in every clip. Check: twelve seeks through each change at four widths, on a sheet a person opens.
4. **Three coils, with colour and the tick on the live coil only; the two below in grey.** Three rose ticks show at once (`p3/home-dark-1440-t7.jpg`) for a method with one sign-off, and the hues on the live coil are what tie the picture to the phase line.
5. **75 seconds.** The owner's complaint was "very slowly", and four minutes goes back to it; the aircraft laps in 30, so the Earth is already the slower thing. A frame costs 0.66ms.
6. **Boards: remove the reveal.** The watchdog shows everything 2.6 seconds after load (`engine.js` line 358), so only a board on screen in those seconds ever animates: script hides content for an effect that almost never plays. Check: 100ms after load, every board cell has opacity 1.
7. **Remove view transitions entirely.** A cross-fade still differs by browser, and removal is a deletion with nothing left to test. Check: no "view-transition" in the built site, including the inline style on the Simulator button.
8. **Relabel in place.** The owner asked for the funnel there, so add one small label over the method names and draw the figure complete on arrival; nothing is redrawn.
9. **Drop it on phones.** It is one rule, and the counts return in "Read the 55 lessons". Check: at 390 by 844 and 360 by 740 the phase line ends on the first screen.
10. **Changes to the prototype:**
    1. Ship the repo's `hero.js`, not the copy on 8844. That copy still has drag (the cursor turns to "grab" over the disc and pointer handlers turn the Earth) and has no seek hook (`GlobeAt` is undefined), so the gate cannot film it.
    2. Fit the phone and the middle widths. At 390 the picture and its line run from 595 to 1001 on an 844 screen, and the pause button covers the jet (`review4/home-dark-390-t3.jpg`). The 8811 copy moves it beside the phase line, where it sits under the mail button at 390 and is cut by the right edge at 1024 (`review4/live/`). Keep it in that row, clear of both.
    3. Cut the hidden stretch behind the Earth from eight seconds to five.
