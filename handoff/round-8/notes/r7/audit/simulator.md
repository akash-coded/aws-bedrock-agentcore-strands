# Audit: Ninety Days (/simulator/)

Played with motion on: whole team to the verdict by the method (1440 dark) and by shortcuts (390 dark), one role, the organisation, days opened by link at 1440 light, 1024, 390 light and 320. No script errors, no sideways scroll, playtest.mjs passes. Screenshots are under `SP/r7/simqa/`.

## 1. Findings

1. **BROKEN. Day 75 task, every width, both themes.** Tick a fix and its label stays, so "×1.6", "×1.5", "×1.3" print on top of each other. `A-1440-dark/d75-bill-two.jpg`, `L-1024-dark/L75-bill-ticked.jpg`, `L-390-light/L75-bill-ticked.jpg`. Cause: game.css `.nd-go .nd-bill-labs span{animation:nd-show … both}` holds opacity 1 over `.gone`. With reduced motion it is correct, which is why it was missed.
2. **BROKEN. Day 82, 320.** The "$2,000" pill sits on the words "The assistant". `L-320-dark/L82-pw.jpg`. Cause: `.nd-pw-held .nd-pw-run{right:calc(50% + 10px)}` leaves a box narrower than the 62px pill.
3. **POOR. Every day, 390 and 320.** The site's round back-to-top button (`.sw-top`, base.css) sits on game controls: the first letters of an option, "On to Day 4", a room chip. `B-390-dark/d82-1-w2.jpg`, `B-390-dark/d01-pin-0.jpg`, `L-320-dark/L82-pw.jpg`. The mail button is hidden during play; this one is not.
4. **POOR. The pictures on small screens.** At 390 the building is drawn at 1x between two dead bars, room names 5px tall. At 320 it is squeezed below 1x and the letters break. The 44px pause button covers the lobby door, and a person on Day 9. `mapphone-390/map-phone.jpg`, `mapphone-320/map-phone.jpg`, `B-390-dark/d09-1-top.jpg`. At 1024 the room close-up also floats between dark bars (`L-1024-dark/L45-top.jpg`). Cause: game.js `fit()` only whole-number scales, no fill for the map.
5. **POOR. Day 82 and pins.** The refund animation plays once on load where nobody is looking: cut by the fold at 1440x900, on the second screen at 390. `A-1440-dark/d82-1-top.jpg`, `B-390-dark/d82-1-w2.jpg`. After a task the pins fly to a day strip that has scrolled away (`anim/pin3-3.jpg`). Cause: `.nd-go` is set at render, not when the figure is seen.
6. **POOR. Every day, 1440x900 and 1024x768.** The question and its options start under the fold (first option at 845px on Day 1, 951 on Day 45, 1146 on Day 82). The strip, the meters and a second picture of the same room come first. `A-1440-dark/d01-1-top.jpg`, `L-1024-dark/L45-top.jpg`.
7. **POOR. "So far".** By the method, Days 12, 20 and 75 all say "on Day 9, you had six people rank the nine targets", which tells a cold reader of the Day 75 bill nothing (`A-1440-dark/d75-bill-1.jpg`, `d20-1-top.jpg`). On a shortcut path it joins two unrelated days: "on Day 75, you opened a comparison of cheaper models. Today a choice from Day 20 comes back." (`B-390-dark/d82-1-top.jpg`). Cause: days.json `needs:"targets"` on d5, d7, d11; sim.js `soFar`, the `fired.id !== from.id` branch.
8. **POOR. The other two ways to play.** As sponsor the screen says "2 questions left to ask" and offers only "Let it stand". The ask button shows only when the colleague is wrong, which gives the answer away (`org-1440/org-d01-w2.jpg`; game.js `playScreen`, the `right.id === state.pending` test). In one role, "Ask to see the evidence" shows no evidence, only "Ask for this instead" and the worse option, with the question printed twice (`role-1440/role-d01-ask-w2.jpg`). "You are Maya" is at the foot of the panel.
9. **POOR. The verdict, every width.** The card touches the meters (gap 0). The calls table wraps in a narrow middle column beside an empty one that says "On file." twelve times. Fifteen definitions hang beside three questions. The panel is 3,670px long at 390. `A-1440-dark/end-1-top.jpg`, `endprobe-1440/end-two.jpg`, `B-390-dark/end-w2.jpg`. Cause: `.nd-meters{margin:0}` beats `.nd-panel>*+*`; `.nd-tb.calls`; `.nd-paper.two`. The same margin fault glues "Go deeper" to the line above (`A-1440-dark/d30-3-platform.jpg`, `.nd-deeper`).
10. **POOR. The verdict's numbers.** "Saved 31.2 person-days, $9,984" is the same on a funded run and on a stopped run, 26 days late, with the assistant switched off. `A-1440-dark/end-1-top.jpg`, `B-390-dark/end-top.jpg`. Cause: sim.js `ledger`, `f` never falls on that path.
11. **POOR. The building, every width.** Most of it is near black: four rooms dimmed, two shuttered until Day 15. The sky shows as stepped pink or orange stripes down both sides, which reads as a frame fault. `art/map-1.jpg`, `art/map-75.jpg`. Cause: art.js dims by half; the sky is drawn behind a building 10px narrower than the canvas.
12. **POLISH. Days 6 and 15.** "On file" and the count go up before the task is done. `A-1440-dark/d06-2-task.jpg`.
13. **POLISH. Top bar.** The pill changes from "The tutorial" to "Read the lesson" between days and the whole menu jumps 30px (`A-1440-dark/d20-1-top.jpg` against `d30-3-platform.jpg`). On the title, "Tutorial" and the pill "The tutorial" sit in one bar and open the same page (`t-1440-dark/title-a.jpg`). "Manual" is fine.
14. **POLISH. The close-up.** Blank faces at five times size, seven people lined up in front of the table, Priya standing inside a stool, the plane drawn through the roof mast. `art/scene-9.jpg`, `art/scene-15.jpg`, `anim/pin3-final.jpg`.
15. **POLISH. Small things.** Two pause buttons on one screen (`A-1440-dark/d01-1-top.jpg`). "Leave this run" twice, still there on the verdict, 18px tall on a phone. "signed" out of line in the sign-off cards (`A-1440-dark/d15-4-gate-full.jpg`). "1 day" in italics in a colleague's plan (`role-1440/role-d01-ask.jpg`). At 1024 "Ninety Days" is not lined up with the column. The day strip looks like tabs and is not. The wall and the paper are both small striped blocks (`anim/held-pw.jpg`, `anim/paid-pw.jpg`).

## 2. Animations and colour: keep or remove

- Keep: the score splitting in three. It is the lesson, it is smooth, it ends right. Name the columns under the bars.
- Keep: the bill multiplying and shrinking as fixes are ticked. Fix finding 1.
- Keep, but start it when it scrolls into view: the refund at paper or wall. Draw the wall as a wall.
- Keep only when the day strip is on screen: the flying pin. Otherwise it is movement leaving the page. The landed pin is 7px; make it bigger.
- Remove: the plane crossing every day. It steps at 8 frames a second, crosses the mast and says nothing.
- Remove: the sky stripes down the building's sides. Keep the sky above the roof and in the windows.
- Keep: one sky per phase, dusk and stars on Day 90. It is the clearest colour in the game.
- Keep: rose only for what is owed, and the phase hues on the day strip.
- Change: dimming of the other rooms. At half they turn to mud and the owners' wall hues vanish.
- Remove: the second pause button.

## 3. The still for the home page

Use Day 45, cropped to the play column at reading size, not a shrunk page: the QA room with the score bar against the rose line and the blue afternoon window, the headline "Day 45. The first test score is 82.4. The promise was 80.", and the three options with their prices in days. If it may move, three frames: that screen, the click on "82.4, at least 79.1", then the one bar breaking into 85, 65.5 and 80 (`A-1440-dark/d45-split-1.jpg` and `d45-split-3.jpg`). A stranger sees a number, a decision and a consequence in five seconds.

## 4. Good, do not change

1. The headlines: a sentence with the number and the stake, on every day.
2. Options with their price in days, and the rose "From Day 6: limits left for later … 3 days gone" boxes when a debt lands.
3. Day 45's finished split figure and its three choices per kind of case.
4. Links to a day: "Days 1 to 30 were played by the book so you can start here", and a saved run is never replaced without asking (`anim/linksave-title.jpg`).
5. The room walls that show state: the score against its bar, the bill's bars, the two bars on the Day 90 board.
