# Review 3: the visual designer

My frames: `SP/r7/rev3/` (prototype, 1440 and 390, both themes, sixteen moments of a lap), with crops in `hi/` and the method boards in `n150/`, `n500/`.

## Part 1

**Strongest: A.** It is the only answer that drew the hero in numbers: a 30 second lap with 22 in front, coils that fade, an outline that fills at the sign-off, a still frame, a phone radius. The prototype follows it almost line for line, and that part works. Its motion rule ("if the still frame says the same thing, it stays still") decides cases the other rules leave open. It is wrong twice: a 27px aircraft cannot show its shape, and a four minute Earth reads as still.

**Biggest blind spot: B.** It forgets whose site it is. It removes both things the owner asked for by name, the change of shape and the rising spiral, on a guess ("will not be seen") that the prototype disproves. At about 45px the dart, airliner and jet are told apart at a glance (`hi/c-home-dark-1440-t1`, `t3`, `t16`).

**All five missed two things.** First, the eight seconds behind the Earth. Nobody said what the picture is while nothing flies. In the prototype that is its busiest frame: three coloured rings, three rose ticks, no phase lit (`rev3/home-dark-1440-t13`). Second, the phone sum. All assumed the picture fits the first screen once the counts move. At 390 by 844 the buttons end near 535px and the canvas is 369px tall. The canvas has to shrink.

## Part 2

1. **Sketches: cut the weak and the repeats, about 70 stay, no cap of one per lesson.** The faults sit in particular drawings (props nobody can name, one idea drawn six times), and several lessons hold two that both pass with the caption covered (`what-is-aidd` on `rev-2`, `agentic-ai-for-executives` on `rev-7`).
2. **Home sample: keep it, swap to `the-needle-never-shakes`.** It comes from lesson one, which the button beside it opens, and without it that band has no picture (`home-dark-1440-07`).
3. **Shape change: keep as built.** All three shapes read, the frame between two shapes is a clean aircraft (`hi/c-home-dark-1440-t2`), and outline to solid at the sign-off is the best idea in the picture.
4. **Two coils, colour on the live one only.** The live arc keeps its four quiet hues because the line under the globe is keyed to them; the ghost goes neutral with no tick, since today four ring ends and three ticks can show at once (`hi/c-home-dark-1440-t22`).
5. **Keep 75 seconds.** At mid disc the aircraft moves about 41 pixels a second and the land under 20, so they do not compete, and four minutes brings back "turns very slowly".
6. **Method boards: remove the reveal.** 150ms after the scroll one column of four is there; at 500ms the fourth is still a ghost (`n150/method-dark-1440-02`, `n500/`).
7. **Page changes: remove entirely.** A cross-fade of any length lays two headlines on each other (`r7/engineer/wk-vt-120ms.jpg`).
8. **Section two: relabel and quieten.** A small label over the four names ("Four methods you may know") and soft ink, so the four phases are read first under "four places"; the owner asked for the funnel here.
9. **Phone: drop the counts.** The same numbers come lower on the page; under the picture they would be a third row of small type.
10. **The prototype.** At 1440, in both themes, it is fluid and elegant, not only tidier. Three changes:
    - **The phone is not done.** At 390 the canvas is 437px wide, so both ring ends are cut. The picture runs from 595 to 1001 on an 844 screen: the globe is cut, the phase line is off screen, and the pause button sits on the globe (`rev3/home-dark-390-t8`, `home-dark-390-02`). Use a radius near 27vw; put pause beside the phase line.
    - **Drag is still in the build.** The disc shows a grab cursor, the pointer handlers are in the script, and the canvas sets `touch-action: pan-y`. Remove them.
    - **The sign-off cannot be seen.** The tick (16 to 26px) is shorter than the wings (37px), so the aircraft covers it while crossing (`hi/c-home-dark-1440-t7`, `t8`). Make it longer than the wingspan, and remove the beads on the lines and the dotted trail behind the Earth (`t19`).
