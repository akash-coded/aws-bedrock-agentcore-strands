// Ninety Days, played in a real browser: every way to play, by real clicks, to the verdict.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/playtest.mjs http://localhost:8799/simulator/
//
// The rules are tested without a browser by sim.test.mjs. This checks the page that sits on them:
// that each mode can be played from the title to the verdict with nothing but the controls on the
// page, that no script error is thrown on the way, that the focus stays inside the game after every
// move, that a reload in the middle of a run comes back to the same day, that a damaged save starts
// clean, that nothing scrolls sideways on a phone, that the sixth task can be done by its controls,
// that a link to a day opens it without replacing a run in progress, and that every day's headline
// is a sentence. Section 11 is what an audit found by looking, each as a check that would catch it
// next time, and it runs with motion allowed, because that is where the faults were: a label that
// stays after its fix is ticked, a pill that sits on a word at 320, a question under the fold, a
// header that moves between days, a figure that plays where nobody is looking. Section 12 is the title's
// line of the ninety days, Day 1's card, and the safeguard on every press: a press that throws leaves the
// page as it was and says "This page is out of date. Reload to play.", which must never show on this tree.
// Section 13 is the building's key, the role rows, the day on the card's metrics, the faults council 9
// measured by eye, each as a number, and the loop that rests while its canvases are off the screen.
// Headless Chrome over the DevTools protocol, the same as accept.mjs, so there is nothing to install.
import { spawn } from "node:child_process";
import { rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const URL_ = process.argv[2];
if (!URL_) { console.error("usage: node playtest.mjs <simulator url>"); process.exit(2); }
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `playtest-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsurl;
for (let i = 0; i < 60 && !wsurl; i++) {
  try { wsurl = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find((t) => t.type === "page").webSocketDebuggerUrl; } catch { await sleep(250); }
}
const ws = new WebSocket(wsurl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const waiting = new Map(); const thrown = [];
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.method === "Runtime.exceptionThrown") thrown.push((m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 200));
  // a press that throws is caught by the page, which says so on the console: that is a script error too
  if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error") { const t = (m.params.args || []).map((a) => a.value || "").join(" "); if (/^Ninety Days stopped/.test(t)) thrown.push(t.slice(0, 200)); }
  if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m.result || {}); waiting.delete(m.id); }
});
const send = (method, params = {}) => new Promise((ok) => { const id = ++seq; waiting.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
const evaluate = async (expression) => (await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true })).result?.value;

// One move, made the way a player would: find what the page offers and press it. `pick` is which
// option to take when there is a choice: 0 the first, 1 the second, -1 the last.
const STEP = (pick, ask) => `(() => {
  const q = (s) => [...document.querySelectorAll(s)];
  const game = document.getElementById("nd");
  if (game.querySelector(".nd-verdict")) return "END";
  const byText = (t) => q("#nd button").find((b) => b.textContent.trim().startsWith(t));
  const at = (list) => list[${pick} < 0 ? list.length - 1 : Math.min(${pick}, list.length - 1)];
  const form = game.querySelector("form.nd-task:not(.nd-org)");
  if (form) {
    const groups = {};
    form.querySelectorAll("input[type=radio]").forEach((r) => (groups[r.name] = groups[r.name] || []).push(r));
    Object.values(groups).forEach((g) => at(g).click());
    const boxes = [...form.querySelectorAll("input[type=checkbox]")];
    if (form.querySelector("#lm-law")) (${pick} === 1 ? ["law", "system", "cap"] : ["law", "fast"]).forEach((id) => { const b = form.querySelector("#lm-" + id); if (!b.checked) b.click(); });
    else if (form.querySelector("#sd-saving")) boxes.slice(0, 3).forEach((b) => { if (!b.checked) b.click(); });
    else if (form.querySelector("#lk-context")) { if (!boxes[0].checked) boxes[0].click(); }
    else if (boxes.length && ${pick} === 1) boxes.forEach((b) => { if (!b.checked) b.click(); });
    form.querySelector("button[type=submit]").click();
    return "task";
  }
  const asked = ${ask} && byText("Ask to see the evidence");
  if (asked) { asked.click(); return "asked"; }
  if (${ask} && game.querySelector(".nd-evidence")) {       // the evidence is on screen: ask for something else
    const alt = q("#nd .nd-opts.alt .nd-opt"), back = byText("Send it back") || byText("Build the slide yourself");
    if (alt.length) { at(alt).click(); return "other"; }
    if (back) { back.click(); return "other"; }
  }
  const stand = byText("Let it stand"); if (stand) { stand.click(); return "stand"; }
  const gate = byText("Sign and start the build"); if (gate) { gate.click(); return "gate"; }
  const opts = q("#nd .nd-panel .nd-opt");
  if (opts.length) { at(opts).click(); return "choice"; }
  const next = game.querySelector(".nd-next"); if (next) { next.click(); return "next"; }
  return "STUCK";
})()`;
const FOCUS = `(() => { const a = document.activeElement; return !!a && !!a.closest("#nd"); })()`;
// the safeguard's notice: on this tree no press may ever bring it up
const BROKE = `(() => { const b = document.querySelector("#nd .nd-broke"); return b ? b.textContent : ""; })()`;

let failures = 0;
const fail = (what) => { failures++; console.log("  FAIL " + what); };
const heads = new Set();          // every day headline seen on the way
const HEAD = `(() => { const h = document.querySelector("#nd .nd-dayhead h2"); return h ? h.textContent : ""; })()`;

async function fresh(width = 1280, height = 800, reduce = true) {
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: width < 600 });
  await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: reduce ? "reduce" : "no-preference" }] });
  await send("Page.navigate", { url: URL_ }); await sleep(900);
  await evaluate(`(localStorage.clear(), 1)`);
  await send("Page.navigate", { url: URL_ }); await sleep(1100);
}
async function play(label, start, pick, ask = false, phone = false, motion = false) {
  thrown.length = 0;
  await fresh(phone ? 375 : 1280, phone ? 812 : 800, !motion);
  const began = await evaluate(start);
  if (!began) return fail(`${label}: could not start`);
  await sleep(150);
  const broke = await evaluate(BROKE);
  if (broke) return fail(`${label}: the first press says "${broke}"`);
  let moves = 0, last = "";
  while (moves++ < 160) {
    last = await evaluate(STEP(pick, ask));
    if (last === "END" || last === "STUCK") break;
    await sleep(25);
    const h = await evaluate(HEAD); if (h) heads.add(h);
    if (!(await evaluate(FOCUS))) { fail(`${label}: the focus left the game after a ${last}`); break; }
    const said = await evaluate(BROKE); if (said) { fail(`${label}: after a ${last} the page says "${said}"`); break; }
    if (phone) { const over = await evaluate(`document.documentElement.scrollWidth - document.documentElement.clientWidth`); if (over > 0) { fail(`${label}: scrolls sideways by ${over}px`); break; } }
  }
  const verdict = await evaluate(`(document.querySelector(".nd-verdict h2") || {}).textContent || ""`);
  if (last !== "END") fail(`${label}: ${last === "STUCK" ? "nothing to press" : "no verdict"} after ${moves} moves`);
  if (thrown.length) fail(`${label}: script error: ${thrown[0]}`);
  console.log(`  ${last === "END" && !thrown.length ? "ok  " : "    "} ${label}: ${verdict || "(no verdict)"} in ${moves} moves`);
  return { verdict, saved: await evaluate(SAVED) };
}
// the verdict's "Saved" figure, as printed
const SAVED = `(() => { const d = [...document.querySelectorAll("#nd .nd-meters.end div")].find((x) => /^Saved/.test(x.querySelector("dt").textContent)); return d ? d.querySelector("dd").textContent : ""; })()`;

const START = `(() => { const b = [...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim() === "Start at Day 1"); if (!b) return false; b.click(); return true; })()`;
const ROLE = (n) => `(() => { const b = document.querySelectorAll("#nd .nd-rolebtns button")[${n}]; if (!b) return false; b.click(); return true; })()`;
const ORG = (ids) => `(() => { const b = [...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim() === "Set the rules"); if (!b) return false; b.click();
  ${JSON.stringify(ids)}.forEach((id) => document.getElementById("po-" + id).click());
  document.querySelector("#nd form.nd-org button[type=submit]").click(); return true; })()`;

try {
  await send("Page.enable"); await send("Runtime.enable");

  console.log("\n1. the whole team");
  const first = await play("always the first option", START, 0);
  if (first.verdict !== "Stopped" || !first.saved || /^31\.2 /.test(first.saved)) fail(`a stopped run reports "${first.saved}" saved, the figure of a funded one`);
  else console.log(`  ok   the stopped run reports its own saving: ${first.saved}`);
  await play("always the second option", START, 1);
  await play("always the last option", START, -1);

  console.log("\n2. one role");
  for (let r = 0; r < 5; r++) await play(`role ${r + 1}, colleagues left alone`, ROLE(r), 1);
  await play("role 4, three questions asked", ROLE(3), 1, true);

  console.log("\n3. the organisation");
  await play("no rules", ORG([]), 0);
  await play("three rules, two questions", ORG(["signed", "code", "both"]), 0, true);

  console.log("\n4. a phone, 375 wide");
  await play("the whole team, second option", START, 1, false, true);

  console.log("\n5. with motion allowed, and then paused");
  await play("the whole team, second option", START, 1, false, false, true);
  // the verdict, as that run left it: one pause control, no way to "leave" a run that is over, air under the card,
  // the calls in two columns, and the glossary folded
  const end = await evaluate(`(() => { const q = (s) => [...document.querySelectorAll(s)], r = (n) => n.getBoundingClientRect();
    const card = document.querySelector("#nd .nd-verdict"), m = document.querySelector("#nd .nd-meters.end"), t = document.querySelector("#nd .nd-tb.calls"), sh = document.querySelector("#nd details.nd-shelf");
    return { pauses: q("#nd [data-motion-toggle]").length, leave: q("a").filter((a) => a.textContent.trim() === "Leave this run" && a.getClientRects().length).length,
      gap: Math.round(r(m).top - r(card).bottom), cols: t ? t.querySelectorAll("thead th").length : 0, rows: t ? t.querySelectorAll("tbody tr").length : 0,
      narrow: t ? Math.min(...[...t.querySelectorAll("tbody td")].map((c) => r(c).width)) : 0, folded: sh ? !sh.open : null }; })()`);
  if (end.pauses !== 1) fail(`the verdict shows ${end.pauses} pause controls`);
  else if (end.leave) fail("the verdict still offers to leave a run that is over");
  else if (end.gap < 12) fail(`the verdict card sits ${end.gap}px from the numbers under it`);
  else if (end.cols !== 2 || end.rows !== 13 || end.narrow < 300) fail(`the calls table has ${end.cols} columns, ${end.rows} rows, the narrowest cell ${Math.round(end.narrow)}px`);
  else if (end.folded !== true) fail("the list of what was put on file is not folded");
  else console.log(`  ok   the verdict: one pause control, ${end.gap}px under the card, thirteen calls in two columns, the glossary folded`);
  thrown.length = 0;
  await fresh(1280, 800, false);
  await evaluate(START); await sleep(900);
  const moving = await evaluate(`window.NDFrames`);
  const controls = await evaluate(`document.querySelectorAll("#nd [data-motion-toggle]").length`);
  if (controls !== 1) fail(`a day shows ${controls} pause controls, not one`);
  await evaluate(`document.querySelector("#nd [data-motion-toggle]").click()`); await sleep(300);
  const held = await evaluate(`window.NDFrames`); await sleep(700);
  const after = await evaluate(`window.NDFrames`);
  if (!(moving > 0)) fail("with motion allowed the picture never moved"); else if (after !== held) fail(`paused, the picture drew ${after - held} more frames`); else console.log("  ok   the pause control stops the picture");
  // paused, a new day still shows its people: count the skin-coloured pixels in today's room, on the
  // building (at this width the building is the picture of the room)
  for (let i = 0; i < 2; i++) { await evaluate(STEP(1, false)); await sleep(60); }
  const people = await evaluate(`(() => { const data = JSON.parse(document.getElementById("nd-data").textContent), n0 = +/^Day (\\d+)/.exec(document.querySelector("#nd .nd-dayhead h2").textContent)[1];
    const room = data.days.find((d) => d.day === n0).room, r = window.NDArt.roomRect(room), c = document.querySelector(".nd-map-cv"), k = c.width / window.NDArt.BW;
    const d = c.getContext("2d").getImageData(r.x * k, (r.y + 4) * k, r.w * k, r.h * k).data; let n = 0;
    for (let i = 0; i < d.length; i += 4) if (d[i] > 130 && d[i + 1] > 80 && d[i + 2] > 50 && d[i] - d[i + 2] > 40 && d[i] > d[i + 1]) n++; return n / (k * k); })()`);
  if (people < 20) fail(`paused, the next day's room is empty (${people} skin-coloured pixels)`); else console.log("  ok   paused, the next day's room has its people in it");

  console.log("\n6. saves");
  thrown.length = 0;
  await fresh();
  await evaluate(START); await sleep(100);
  for (let i = 0; i < 7; i++) { await evaluate(STEP(1, false)); await sleep(25); }
  const before = await evaluate(`document.querySelector("#nd h2").textContent`);
  await send("Page.navigate", { url: URL_ }); await sleep(1100);
  const offer = await evaluate(`(() => { const b = [...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim().startsWith("Carry on")); if (!b) return ""; b.click(); return document.querySelector("#nd h2").textContent; })()`);
  if (offer !== before) fail(`a reload did not come back to the same day: "${before}" then "${offer}"`); else console.log(`  ok   a reload comes back to "${before}"`);
  await evaluate(`(localStorage.setItem("skyways.ninety", "{not json"), 1)`);
  await send("Page.navigate", { url: URL_ }); await sleep(1100);
  const clean = await evaluate(`!![...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim() === "Start at Day 1")`);
  if (!clean || thrown.length) fail("a damaged save did not start clean" + (thrown[0] ? ": " + thrown[0] : "")); else console.log("  ok   a damaged save starts clean");

  await evaluate(`(localStorage.setItem("skyways.ninety", '{"v":1}'), 1)`);
  await send("Page.navigate", { url: URL_ }); await sleep(1100);
  const half = await evaluate(`!![...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim() === "Start at Day 1")`);
  if (!half || thrown.length) fail("a save with no history did not start clean" + (thrown[0] ? ": " + thrown[0] : "")); else console.log("  ok   a save with no history starts clean");

  console.log("\n7. an old workbench link");
  await send("Page.navigate", { url: URL_ + "#/toolkit/bar" }); await sleep(1500);
  const landed = await evaluate(`location.pathname + location.hash`);
  if (!/workbench\/#\/toolkit\/bar$/.test(landed)) fail(`an old route was not forwarded: ${landed}`); else console.log("  ok   #/toolkit/bar is forwarded to the workbench");

  console.log("\n8. the sixth task, on a phone: which of these can move?");
  thrown.length = 0;
  await fresh(375, 812);
  await evaluate(START); await sleep(150);
  for (let i = 0; i < 5; i++) { await evaluate(STEP(1, false)); await sleep(40); }       // Days 1 and 4 by the method, then Day 6's method option
  const TICK = (ids) => `(() => { ${JSON.stringify(ids)}.forEach((id) => document.getElementById("lm-" + id).click()); return document.querySelectorAll("#nd .nd-bends li").length; })()`;
  const SUBMIT = `(() => { const f = document.querySelector("#nd form.nd-task"); f.querySelector("button[type=submit]").click(); const g = document.querySelector("#nd form.nd-task"); return g ? (g.querySelector(".nd-status").textContent || "(no status)") : "SENT"; })()`;
  const six = await evaluate(`(() => { const f = document.querySelector("#nd form.nd-task"); if (!f || !f.querySelector("#lm-law")) return null;
    const boxes = [...f.querySelectorAll("label.nd-check")]; return { title: f.querySelector("h3").textContent, n: boxes.length, low: Math.min(...boxes.map((b) => b.getBoundingClientRect().height)) }; })()`);
  if (!six) fail("Day 6's method option does not open the limits task");
  else {
    if (six.n !== 6 || six.low < 44) fail(`the limits task shows ${six.n} lines, the shortest ${Math.round(six.low)}px tall`);
    const empty = await evaluate(SUBMIT);
    if (empty === "SENT" || empty === "(no status)") fail("the limits task, submitted empty, does not say what is missing"); else console.log(`  ok   submitted empty, it says: "${empty}"`);
    const one = await evaluate(TICK(["law"])), still = await evaluate(TICK(["fast"])), three = await evaluate(TICK(["system", "cap"]));
    if (one !== 1 || still !== 1 || three !== 3) fail(`ticking limits rewrites ${one}, ${still}, ${three} targets, not 1, 1, 3`); else console.log("  ok   each real limit ticked rewrites one target, and a wish rewrites none");
    await evaluate(TICK(["fast"]));                                                        // untick the wish
    const sent = await evaluate(SUBMIT); await sleep(60);
    const pinned = await evaluate(`(document.querySelector("#nd .nd-sealed") || {}).textContent || ""`);
    if (sent !== "SENT" || pinned) fail(`the limits task done right: ${sent}, and "${pinned}"`); else console.log("  ok   done right, nothing is pinned");
    if (!(await evaluate(FOCUS))) fail("the focus left the game after the limits task");
    // and done badly: undo the day, take the same option, tick one wish and nothing else
    await evaluate(`[...document.querySelectorAll("#nd button")].find((b) => b.textContent.trim() === "Undo today").click()`); await sleep(60);
    await evaluate(STEP(1, false)); await sleep(60);
    await evaluate(TICK(["fast"])); await evaluate(SUBMIT); await sleep(60);
    const bad = await evaluate(`({ line: (document.querySelector("#nd .nd-sealed") || {}).textContent || "", pins: document.querySelectorAll("#nd .nd-strip li.owed").length, back: [...document.querySelectorAll("#nd .nd-debts button")].length })`);
    if (!/Day 9, Day 15, and Day 30/.test(bad.line) || bad.pins !== 3 || bad.back !== 1) fail(`the limits task done badly: "${bad.line}", ${bad.pins} days pinned, ${bad.back} ways back`);
    else console.log("  ok   done badly, three days are pinned and one trip back repairs them");
    const over = await evaluate(`document.documentElement.scrollWidth - document.documentElement.clientWidth`);
    if (over > 0) fail(`the limits task scrolls sideways by ${over}px`);
  }
  if (thrown.length) fail("the sixth task: script error: " + thrown[0]);

  console.log("\n9. a link to a day");
  thrown.length = 0;
  const blank = async () => { await send("Page.navigate", { url: "about:blank" }); await sleep(150); };
  const open = async (hash) => { await blank(); await send("Page.navigate", { url: URL_ + hash }); await sleep(1100); };
  const SAVE = `localStorage.getItem("skyways.ninety")`;
  const BUTTONS = `[...document.querySelectorAll("#nd .nd-title button, #nd .nd-panel .nd-acts button")].map((b) => b.textContent.trim())`;
  const PRESS = (t) => `(() => { const b = [...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim().startsWith(${JSON.stringify(t)})); if (!b) return false; b.click(); return true; })()`;
  // the pill holds both of its labels and shows one: read the one that shows
  const PILL = `(() => { const a = document.querySelector("a.play[data-ctx-lesson]"), on = (s) => { const n = a.querySelector(s + " [data-on]"); return n ? n.textContent : ""; };
    return a ? { href: a.getAttribute("href"), lg: on(".lg"), sm: on(".sm"), title: a.getAttribute("title"), manual: [...document.querySelectorAll(".hd .ctx a:not(.play)")].map((x) => x.textContent.trim()).join("|") } : null; })()`;
  // no save: the day opens, says how it got there, and nothing is saved until a move is made
  await fresh();
  const pill0 = await evaluate(PILL);
  await open("#day-45");
  const cold = await evaluate(`({ h: ${HEAD}, book: (document.querySelector("#nd .nd-book") || {}).textContent || "", sofar: (document.querySelector("#nd .nd-sofar") || {}).textContent || "", save: ${SAVE}, hash: location.hash })`);
  if (!/^Day 45\. /.test(cold.h)) fail(`#day-45 with no save opened "${cold.h}"`);
  else if (cold.book !== "Days 1 to 30 were played by the book so you can start here.") fail(`#day-45 does not say how it got there: "${cold.book}"`);
  else if (!/^So far: on Day 15, you /.test(cold.sofar)) fail(`#day-45 opens without its "So far": "${cold.sofar}"`);
  else if (cold.save) fail("#day-45 saved a run before any move was made");
  else console.log(`  ok   #day-45 with no save opens "${cold.h}", and says the earlier days were played by the book`);
  heads.add(cold.h);
  const pill45 = await evaluate(PILL);
  if (!pill0 || !pill45) fail("the header pill is missing");
  else if (!/learn\/$/.test(pill0.href) || pill0.lg !== "The tutorial" || pill0.sm !== "Tutorial" || pill0.title) fail(`on the title the header pill is ${JSON.stringify(pill0)}`);
  else if (!/learn\/prove-ai-accuracy\/$/.test(pill45.href) || pill45.lg !== "Read the lesson" || pill45.sm !== "Lesson" || !pill45.title) fail(`on Day 45 the header pill is ${JSON.stringify(pill45)}`);
  else console.log(`  ok   the header pill: the tutorial on the title, "${pill45.title}" on Day 45`);
  await evaluate(STEP(1, false)); await sleep(60);
  const moved = await evaluate(`({ save: ${SAVE}, hash: location.hash })`);
  if (!moved.save || moved.hash) fail(`after a move on a linked day: save ${moved.save ? "kept" : "missing"}, hash "${moved.hash}"`); else console.log("  ok   the first move saves the run and clears the link");
  // every day opens cold from its link, and a day with no lesson sends the pill back to the tutorial
  for (const n of [1, 4, 6, 9, 12, 15, 20, 30, 45, 60, 75, 82, 90]) {
    await evaluate(`(localStorage.clear(), 1)`); await open("#day-" + n);
    const h = await evaluate(HEAD); if (h) heads.add(h);
    if (!new RegExp("^Day " + n + "\\. ").test(h)) fail(`#day-${n} opened "${h}"`);
    if (n === 1 || n === 12) { const p = await evaluate(PILL); if (!p || !/learn\/$/.test(p.href) || p.lg !== "The tutorial") fail(`on Day ${n}, which has no lesson, the header pill is ${JSON.stringify(p)}`); }
  }
  if (!thrown.length) console.log("  ok   all thirteen days open from their links");
  // the "So far" of a day opened cold is about that day: the bill's is about cost, the refund's about the limit
  for (const [n, word] of [[75, "cost"], [82, "refund"], [20, "framework"]]) {
    await evaluate(`(localStorage.clear(), 1)`); await open("#day-" + n);
    const so = await evaluate(`(document.querySelector("#nd .nd-sofar") || {}).textContent || ""`);
    if (!new RegExp(word).test(so)) fail(`Day ${n}, opened cold, has a "So far" that does not mention ${word}: "${so}"`);
  }
  // a save: both choices are offered, and only the second replaces it
  await fresh();
  await evaluate(START); await sleep(100);
  for (let i = 0; i < 7; i++) { await evaluate(STEP(1, false)); await sleep(25); }
  const mine = await evaluate(SAVE);
  await open("#day-45");
  const both = await evaluate(BUTTONS), kept = await evaluate(SAVE);
  if (both.join("|") !== "Carry on from Day 9|Open Day 45 on a fresh run") fail(`#day-45 with a save offers: ${both.join(" | ") || "nothing"}`);
  else if (kept !== mine) fail("#day-45 changed the save before the player chose");
  else console.log("  ok   #day-45 with a save offers both, and leaves the save alone");
  await evaluate(PRESS("Carry on from Day 9")); await sleep(80);
  const carried = await evaluate(`({ h: ${HEAD}, save: ${SAVE} })`);
  if (!/^Day 9\. /.test(carried.h) || carried.save !== mine) fail(`carrying on from a link: "${carried.h}", save ${carried.save === mine ? "kept" : "changed"}`); else console.log("  ok   carrying on comes back to Day 9 with the save untouched");
  await open("#day-45");
  await evaluate(PRESS("Open Day 45 on a fresh run")); await sleep(80);
  const replaced = await evaluate(`({ h: ${HEAD}, from: (JSON.parse(${SAVE} || "{}").opts || {}).from, hash: location.hash })`);
  if (!/^Day 45\. /.test(replaced.h) || replaced.from !== 8 || replaced.hash) fail(`a fresh run from a link: "${replaced.h}", saved from ${replaced.from}, hash "${replaced.hash}"`); else console.log("  ok   a fresh run replaces the save only when it is asked for");
  // a day that is not one of the thirteen, and a link followed while the page is open
  for (const bad of ["#day-44", "#day-0", "#day-900", "#day-", "#day-45x"]) {
    await evaluate(`(localStorage.clear(), 1)`); await open(bad);
    if (!(await evaluate(`!![...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim() === "Start at Day 1")`))) fail(`${bad} did not fall back to the title`);
  }
  await evaluate(`(location.hash = "#day-75", 1)`); await sleep(300);
  const hopped = await evaluate(HEAD);
  if (!/^Day 75\. /.test(hopped)) fail(`changing the address to #day-75 opened "${hopped}"`); else console.log("  ok   unknown days fall back to the title, and a link followed on the page opens its day");
  if (thrown.length) fail("a link to a day: script error: " + thrown[0]);

  console.log("\n10. every headline is a sentence");
  const VERB = /\b(is|are|was|were|has|have|must|cannot|set|starts|asks|will|tried|sent|refused|build|buy|borrow)\b/i;
  const bare = [...heads].filter((h) => { const rest = h.replace(/^Day \d+\.\s*/, ""); return !rest || !(/\d/.test(rest) || VERB.test(rest)); });
  if (heads.size < 13) fail(`only ${heads.size} headlines were seen`);
  else if (bare.length) fail(`a headline is a bare noun: ${bare.join(" | ")}`);
  else console.log(`  ok   ${heads.size} headlines seen, each with a verb or a number`);

  console.log("\n11. what an audit found by looking, with motion allowed");
  thrown.length = 0;
  const size = async (w, h) => { await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 600 }); await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "no-preference" }] }); };
  const fromCold = async (w, h, hash) => { await size(w, h); await blank(); await send("Page.navigate", { url: URL_ }); await sleep(500); await evaluate(`(localStorage.clear(), 1)`); await blank(); await send("Page.navigate", { url: URL_ + hash }); await sleep(1200); };
  const CLICK = (sel) => `(() => { const e = document.querySelector(${JSON.stringify(sel)}); if (!e) return false; e.click(); return true; })()`;
  const OPTION = (t) => `(() => { const b = [...document.querySelectorAll("#nd .nd-opt")].find((x) => x.textContent.trim().startsWith(${JSON.stringify(t)})); if (!b) return false; b.click(); return true; })()`;
  // the same test of "on screen" the page uses: below the site's bar, above the fold
  const SEEN = `((n) => { if (!n) return false; const r = n.getBoundingClientRect(); return r.height > 0 && r.top >= 60 && r.bottom <= innerHeight; })`;

  // The title says what this is before it says its name, and the first screen tells a first-time visitor
  // all of it: a game, an airline's AI project, ninety days, thirteen decisions that cost days, and how to start.
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    await fromCold(w, h, "");
    const t = await evaluate(`(() => { const h1 = document.querySelector(".nd-top h1"), start = [...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim() === "Start at Day 1");
      const seen = [...document.querySelectorAll(".nd-top h1, .nd-top .lede, .nd-top .nd-facts")].filter((n) => n.getBoundingClientRect().bottom <= innerHeight).map((n) => n.innerText).join(" ");
      // the opening lines' measure: characters on each line but the last
      const lede = document.querySelector(".nd-top .lede"), t = lede.firstChild, r = document.createRange(), per = {};
      for (let i = 0; i < t.length; i++) { r.setStart(t, i); r.setEnd(t, i + 1); const k = Math.round(r.getBoundingClientRect().top); per[k] = (per[k] || 0) + 1; }
      const lines = Object.keys(per).sort((a, b) => a - b).map((k) => per[k]);
      const tall = [...document.querySelectorAll("#nd .nd-rolebtns button, #nd .nd-waygrid button")].map((b) => Math.round(b.getBoundingClientRect().height));
      return { h1: h1.innerText.replace(/\\s+/g, " "), seen, start: start ? Math.round(start.getBoundingClientRect().bottom) : 9999, startH: start ? Math.round(start.getBoundingClientRect().height) : 0,
        lines, tall, rows: new Set([...document.querySelectorAll("#nd .nd-rolebtns button")].map((b) => Math.round(b.getBoundingClientRect().top))).size, h: innerHeight }; })()`);
    const says = [/game/i, /fictional airline/, /AI assistant/, /stranded passengers/, /ninety days/, /thirteen decisions/, /costs days/].filter((r) => !r.test(t.seen));
    if (!/^A game\b/.test(t.h1) || !/Ninety Days/.test(t.h1) || t.h1.indexOf("game") > t.h1.indexOf("Ninety Days")) fail(`${w} wide: the page's heading reads "${t.h1}"`);
    else if (says.length) fail(`${w} wide: the title's first screen does not say ${says.join(", ")}`);
    else if (t.start > t.h) fail(`${w} wide: "Start at Day 1" ends at ${t.start}px of a ${t.h}px screen`);
    else if (w > 1000 && (Math.max(...t.lines) > 56 || Math.max(...t.lines) < 46)) fail(`${w} wide: the opening lines run ${t.lines.join(", ")} characters a line (46 to 56)`);
    else if (t.tall.some((x) => x !== t.startH) || t.rows !== 5) fail(`${w} wide: the title's buttons are ${t.tall.join(", ")}px beside a ${t.startH}px Start, the roles in ${t.rows} rows`);
    else console.log(`  ok   ${w} wide: the title says what the game is before its name, "Start at Day 1" is on the first screen, the opening lines run ${t.lines.slice(0, -1).join(", ")} characters a line, every button is ${t.startH}px`);
  }

  // a. the question and its first option are on the first screen, also on the two days that bring news
  // above the scene: Day 20 (the vendor's freeze) and Day 82 (the refund that met its limit)
  for (const [w, h] of [[1440, 900], [1024, 768], [390, 844]]) {
    for (const hash of ["", "#day-45", "#day-9", "#day-20", "#day-82"]) {
      await fromCold(w, h, hash);
      if (!hash) { await evaluate(START); await sleep(400); }
      const at = await evaluate(`(() => { const l = document.querySelector("#nd .nd-opts legend"), o = document.querySelector("#nd .nd-opts .nd-opt"), p = document.querySelector("#nd .nd-scene-cv"), m = document.querySelector("#nd .nd-map-cv");
        const vis = (n) => { if (!n) return false; const r = n.getBoundingClientRect(); return r.width > 100 && r.top < innerHeight && r.bottom > 60; };
        return { y: scrollY, q: l ? Math.round(l.getBoundingClientRect().top) : -1, bottom: o ? Math.round(o.getBoundingClientRect().bottom) : 9999, h: innerHeight, picture: vis(p) || vis(m) }; })()`);
      const name = `${w}x${h}, ${hash ? "Day " + hash.slice(5) + " by its link" : "Day 1"}`;
      if (at.y !== 0 || at.q < 60 || at.bottom > at.h) fail(`${name}: the first option ends at ${at.bottom}px of a ${at.h}px screen (scrolled ${at.y})`);
      else if (!at.picture) fail(`${name}: no picture of the room on the first screen`);
      else console.log(`  ok   ${name}: the question and its first option are on the first screen (it ends at ${at.bottom} of ${at.h}), with a picture of the room`);
    }
  }

  // b. the header does not move between days: the pill is as wide on the title, on Day 1 and on Day 45
  await fromCold(1440, 900, "");
  const WIDTH = `(() => { const a = document.querySelector("a.play[data-ctx-lesson]"); return a ? Math.round(a.getBoundingClientRect().width * 10) / 10 : -1; })()`;
  const w0 = await evaluate(WIDTH); await evaluate(START); await sleep(300);
  const w1 = await evaluate(WIDTH); await fromCold(1440, 900, "#day-45");
  const w45 = await evaluate(WIDTH);
  const p45 = await evaluate(PILL);
  if (!(w0 > 0) || w0 !== w1 || w1 !== w45) fail(`the header pill is ${w0}px on the title, ${w1}px on Day 1 and ${w45}px on Day 45`);
  else if (p45.lg !== "Read the lesson" || !/The manual/.test(p45.manual)) fail(`on Day 45 the bar reads "${p45.manual}" and "${p45.lg}"`);
  else console.log(`  ok   the header pill is ${w0}px wide on the title, on Day 1 and on Day 45, beside "${p45.manual}"`);

  // c. Day 75: tick two fixes, and only the labels of what is left are shown, none on another
  for (const [w, h] of [[1280, 800], [320, 640]]) {
    await fromCold(w, h, "#day-75");
    await evaluate(OPTION("The log of every model call")); await sleep(1700);          // let the figure play out, if it played
    const LABELS = `(() => [...document.querySelectorAll("#nd .nd-bill-labs span")].map((s) => { const r = s.getBoundingClientRect(), c = getComputedStyle(s); return { t: s.textContent, on: c.visibility !== "hidden" && +c.opacity > 0.5 && r.width > 4, l: r.left, r: r.right }; }))()`;
    const before = await evaluate(LABELS);
    await evaluate(CLICK("#lk-context")); await evaluate(CLICK("#lk-tier")); await sleep(700);
    const after = await evaluate(LABELS), on = after.filter((x) => x.on);
    const clash = on.some((x, i) => i && x.l < on[i - 1].r - 0.5), total = await evaluate(`document.querySelector("#nd .nd-bill-top b").textContent`);
    const over = await evaluate(`document.documentElement.scrollWidth - document.documentElement.clientWidth`);
    if (before.filter((x) => x.on).length !== 5) fail(`${w} wide: the bill opens with ${before.filter((x) => x.on).length} labels, not five`);
    else if (on.map((x) => x.t).join(" ") !== "estimate ×1.3 ×1.41") fail(`${w} wide: with two fixes ticked the bill still shows: ${on.map((x) => x.t).join(" ")}`);
    else if (clash) fail(`${w} wide: two of the bill's labels print on each other`);
    else if (total !== "1.83 times") fail(`${w} wide: with two fixes ticked the bill reads ${total}`);
    else if (over > 0) fail(`${w} wide: Day 75's task scrolls sideways by ${over}px`);
    else console.log(`  ok   ${w} wide, Day 75: two fixes ticked, and the bill shows "${on.map((x) => x.t).join(" ")}" and ${total}`);
  }

  // d. Day 82: nothing sits on anything else, down to 320 wide
  for (const [w, h] of [[1280, 800], [320, 640]]) {
    await fromCold(w, h, "#day-82"); await sleep(400);
    const pw = await evaluate(`(() => { const r = (s) => { const n = document.querySelector(s); return n ? n.getBoundingClientRect() : null; }, hit = (a, b) => a && b && a.left < b.right - 0.5 && b.left < a.right - 0.5 && a.top < b.bottom - 0.5 && b.top < a.bottom - 0.5;
      const pill = r("#nd .nd-pw-run b"), from = r("#nd .nd-pw-end.from"), to = r("#nd .nd-pw-end.to"), wall = r("#nd .nd-pw-stop"), name = r("#nd .nd-pw-track em"), box = r("#nd .nd-pw-row");
      return { pill: !!pill, onFrom: hit(pill, from), onTo: hit(pill, to), onWall: hit(pill, wall), onName: hit(pill, name), inside: pill && pill.left >= box.left - 0.5 && pill.right <= box.right + 0.5,
        go: document.querySelector("#nd .nd-pw").classList.contains("nd-go"), over: document.documentElement.scrollWidth - document.documentElement.clientWidth }; })()`);
    if (!pw.pill) fail(`${w} wide: Day 82 has no refund figure`);
    else if (pw.onFrom || pw.onTo || pw.onWall || pw.onName || !pw.inside) fail(`${w} wide, Day 82: the refund sits on something: ${JSON.stringify(pw)}`);
    else if (pw.over > 0) fail(`${w} wide: Day 82 scrolls sideways by ${pw.over}px`);
    else if (pw.go) fail(`${w} wide: Day 82, opened by its link with no press, plays its figure`);
    else console.log(`  ok   ${w} wide, Day 82: the refund, the wall and the two names are clear of each other, and nothing plays unasked`);
  }

  // e. a figure plays only as the answer to a press, and only if it is on screen when it starts
  for (const [w, h] of [[1280, 800], [375, 812]]) {
    await fromCold(w, h, "#day-75");
    await evaluate(OPTION("The log of every model call")); await sleep(80);
    const bill = await evaluate(`(() => { const f = document.querySelector("#nd .nd-bill"); return { go: f.classList.contains("nd-go"), seen: ${SEEN}(f) }; })()`);
    if (!bill.go || !bill.seen) fail(`${w} wide: the bill, opened by a press, ${bill.seen ? "is on screen and does not play" : "is not brought on screen"}`);
    await sleep(1500); await evaluate(CLICK("#lk-context")); await evaluate(CLICK("#lk-tier")); await evaluate(CLICK("#nd form.nd-task button[type=submit]")); await sleep(200);
    await evaluate(CLICK("#nd .nd-next")); await sleep(120);
    const pw = await evaluate(`(() => { const f = document.querySelector("#nd .nd-pw"); return f ? { go: f.classList.contains("nd-go"), seen: ${SEEN}(f) } : null; })()`);
    if (!pw) fail(`${w} wide: "On to Day 82" did not open Day 82`);
    else if (pw.go !== pw.seen) fail(`${w} wide: on Day 82 the refund ${pw.go ? "plays off the screen" : "is on screen after a press and does not play"}`);
    else if (bill.go && bill.seen) console.log(`  ok   ${w} wide: the bill plays on screen after its press; the refund is ${pw.seen ? "on screen and plays" : "below the fold and is shown finished"}`);
  }

  // f. a pin flies only to a day strip that is on screen, and the pin that lands can be seen
  for (const [w, h, scroll] of [[1280, 800, false], [375, 812, true]]) {
    await fromCold(w, h, ""); await evaluate(START); await sleep(900);
    if (scroll) { await evaluate(`(document.querySelector("#nd .nd-opt").scrollIntoView({ block: "center", behavior: "instant" }), 1)`); await sleep(100); }
    await evaluate(OPTION("Start the design from the 31")); await sleep(60);
    const pin = await evaluate(`(() => { const flying = !!document.querySelector(".nd-pin"), cell = document.querySelector("#nd .nd-strip li.owed"), i = cell && cell.querySelector("i");
      return { flying, strip: ${SEEN}(cell), line: ${SEEN}(document.querySelector("#nd .nd-sealed")), size: i ? Math.round(i.getBoundingClientRect().width) : 0 }; })()`);
    if (pin.size < 9) fail(`${w} wide: the pin on the day strip is ${pin.size}px`);
    else if (!pin.line) fail(`${w} wide: after a press the line that says what was pinned is not on screen`);
    else if (pin.flying !== pin.strip) fail(`${w} wide: ${pin.flying ? "a pin flies to a day strip that is off the screen" : "the day strip is on screen and no pin flies to it"}`);
    else console.log(`  ok   ${w} wide: the day strip is ${pin.strip ? "on screen, and a pin flies to it" : "off the screen, and no pin flies"}; the pin there is ${pin.size}px`);
    await sleep(700);
    if (await evaluate(`!!document.querySelector(".nd-pin")`)) fail(`${w} wide: a flying pin was left on the page`);
  }

  // g. Day 6: a document goes on file when its task is done, not when the option is pressed
  await fromCold(1280, 800, "#day-6");
  const FILED = `(() => { const d = [...document.querySelectorAll("#nd .nd-meters div")].find((x) => x.querySelector("dt").textContent === "On file"); return { n: parseInt(d.querySelector("dd").textContent, 10), box: !!document.querySelector("#nd .nd-filedbox") }; })()`;
  const f0 = await evaluate(FILED); await evaluate(OPTION("Now, sorted by kind")); await sleep(120);
  const f1 = await evaluate(FILED); await evaluate(TICK(["law", "system", "cap"])); await evaluate(CLICK("#nd form.nd-task button[type=submit]")); await sleep(120);
  const f2 = await evaluate(FILED);
  if (f1.n !== f0.n || f1.box) fail(`Day 6: with the task still open, "On file" went from ${f0.n} to ${f1.n}`);
  else if (f2.n !== f0.n + 1 || !f2.box) fail(`Day 6: with the task done, "On file" is ${f2.n} after ${f0.n}`);
  else console.log(`  ok   Day 6: "On file" stays at ${f0.n} while the task is open, and is ${f2.n} when it is done`);

  // h. Day 15: the three documents of the sign-off line up
  await fromCold(1280, 800, "#day-15");
  await evaluate(OPTION("One page")); await sleep(120); await evaluate(CLICK("#nd form.nd-task button[type=submit]")); await sleep(150);
  const lamps = await evaluate(`[...document.querySelectorAll("#nd .nd-lamps li span")].map((s) => Math.round(s.getBoundingClientRect().bottom))`);
  if (lamps.length !== 3 || new Set(lamps).size !== 1) fail(`Day 15: "signed" sits at ${lamps.join(", ")}px in the three cards`); else console.log(`  ok   Day 15: "signed" is on one line across the three documents`);

  // i. the sponsor may ask about any plan, sound or not; asking costs a question and shows evidence
  await fromCold(1280, 800, ""); await evaluate(ORG([])); await sleep(300);
  const ASK = `(() => { const b = [...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim().startsWith("Ask to see the evidence")); return { ask: !!b, plan: (document.querySelector("#nd .nd-plan .nd-you") || {}).textContent || "", left: (([...document.querySelectorAll("#nd .nd-meters div")].find((x) => x.querySelector("dt").textContent === "Questions") || document.body).querySelector("dd") || {}).textContent || "",
    who: !!document.querySelector("#nd .nd-you-are") && document.querySelector("#nd .nd-you-are").getBoundingClientRect().top < document.querySelector("#nd .nd-dayhead").getBoundingClientRect().top }; })()`;
  const d1 = await evaluate(ASK);                                   // Day 1 with no rules: the architect merges the list, a sound plan
  await evaluate(PRESS("Ask to see the evidence")); await sleep(120);
  const d1e = await evaluate(`({ text: (document.querySelector("#nd .nd-evidence") || {}).innerText || "", others: document.querySelectorAll("#nd .nd-opts.alt .nd-opt").length, focus: !!document.activeElement.closest(".nd-evidence, .nd-plan"), left: ${ASK}.left })`);
  await evaluate(PRESS("Let it stand")); await sleep(80); await evaluate(CLICK("#nd .nd-next")); await sleep(200);
  const d4 = await evaluate(ASK);                                   // Day 4: the minutes go out, an unsound one
  if (!d1.ask || !d4.ask) fail(`the sponsor is offered a question on Day 1 (${d1.ask}) and on Day 4 (${d4.ask}): the offer gives the answer away`);
  else if (!/Merge them/.test(d1.plan) || !/full minutes/.test(d4.plan)) fail(`the two plans are not one sound and one unsound: "${d1.plan}", "${d4.plan}"`);
  else if (!/on file/i.test(d1e.text) || !/Requirements register/.test(d1e.text)) fail(`asked for the evidence, the page shows: "${d1e.text}"`);
  else if (d1.left !== "2 left" || d1e.left !== "1 left" || d1e.others !== 1) fail(`a question on a sound plan: ${d1.left}, then ${d1e.left}, with ${d1e.others} other options`);
  else if (!d1.who) fail("the sponsor is not told who they are before the day");
  else console.log("  ok   the sponsor is offered a question on a sound plan and on an unsound one; it costs one and shows what is on file");
  // one role: the question is printed once, and the evidence is there before anything else is offered
  await fromCold(1280, 800, ""); await evaluate(ROLE(3)); await sleep(300);
  await evaluate(PRESS("Ask to see the evidence")); await sleep(120);
  const role = await evaluate(`(() => { const ask = JSON.parse(document.getElementById("nd-data").textContent).days[0].ask, all = [...document.querySelectorAll("#nd .nd-panel *")].filter((n) => n.children.length === 0 && n.textContent.trim() === ask && n.getClientRects().length);
    const ev = document.querySelector("#nd .nd-evidence"), alt = document.querySelector("#nd .nd-opts.alt"); return { asks: all.length, ev: ev ? ev.innerText : "", order: !!ev && !!alt && ev.getBoundingClientRect().top < alt.getBoundingClientRect().top, who: (document.querySelector("#nd .nd-panel > :first-child") || {}).className }; })()`);
  if (role.asks !== 1) fail(`in one role, with the evidence open, the day's question is printed ${role.asks} times`);
  else if (!/After today/.test(role.ev) || !role.order) fail(`in one role, "Ask to see the evidence" shows: "${role.ev}"`);
  else if (role.who !== "nd-you-are") fail(`in one role the panel opens with ${role.who}, not with who the player is`);
  else console.log("  ok   in one role the evidence comes before the other options, the question is printed once, and the panel opens with who you are");

  // j. during a run there is one way to leave it
  const leave = await evaluate(`[...document.querySelectorAll("a")].filter((a) => a.textContent.trim() === "Leave this run" && a.getClientRects().length).length`);
  if (leave !== 1) fail(`a day offers "Leave this run" ${leave} times`); else console.log("  ok   a day offers one way to leave the run");
  if (thrown.length) fail("section 11: script error: " + thrown[0]);

  console.log("\n12. the line of the ninety days, Day 1's card, and a press that fails");
  thrown.length = 0;
  const KEY = `localStorage.getItem("skyways.ninety")`;
  // a. at 1440 the line is a list of thirteen links to the days, drawn to time, with the four milestones marked
  await fromCold(1440, 900, "");
  const line = await evaluate(`(() => { const ol = document.querySelector("#nd .nd-line .nd-line-stops"); if (!ol) return null;
    const a = [...ol.querySelectorAll("a")].filter((x) => x.getClientRects().length), r = ol.getBoundingClientRect(), bar = document.querySelector("#nd .nd-line-bar").getBoundingClientRect();
    const x = (n) => { const d = n.querySelector("i").getBoundingClientRect(); return (d.left + d.width / 2 - bar.left) / bar.width; };
    return { hrefs: a.map((x) => x.getAttribute("href")).join(" "), flags: [...ol.querySelectorAll("em")].map((e) => e.textContent).join("|"), names: [...document.querySelectorAll("#nd .nd-line-ph span")].map((s) => s.textContent).join("|"),
      x45: x(a[8]), x15: x(a[5]), bottom: Math.round(document.querySelector("#nd .nd-line").getBoundingClientRect().bottom), tabs: a.filter((x) => x.tabIndex === 0).length, w: Math.round(bar.width) }; })()`);
  if (!line) fail("the title has no line of the ninety days");
  else if (line.hrefs !== [1, 4, 6, 9, 12, 15, 20, 30, 45, 60, 75, 82, 90].map((n) => "#day-" + n).join(" ")) fail(`the line's links are ${line.hrefs}`);
  else if (line.flags !== "Sign-off|First test|First bill|Sponsor's slide" || line.names !== "Frame|Design and spec|Build and prove|Run and learn") fail(`the line's words: ${line.flags}; ${line.names}`);
  else if (Math.abs(line.x45 - 44 / 89) > 0.02 || Math.abs(line.x15 - 14 / 89) > 0.02) fail(`the line is not drawn to time: Day 15 at ${line.x15.toFixed(3)}, Day 45 at ${line.x45.toFixed(3)} of its width`);
  else if (line.bottom > 900 || line.tabs !== 1) fail(`the line ends at ${line.bottom}px of 900, with ${line.tabs} stops on the Tab key`);
  else console.log(`  ok   1440 wide: thirteen links drawn to time across ${line.w}px, the four milestones named, the whole line on the first screen (it ends at ${line.bottom})`);
  // b. focusing a stop puts its headline in the caption and Start opens it, by the book, as a fresh saved run
  // (a headless page has no window focus, so focus events do not fire until it is told it has)
  await send("Emulation.setFocusEmulationEnabled", { enabled: true });
  const aimed = await evaluate(`(() => { const a = document.querySelector('#nd .nd-line a[href="#day-45"]'); a.focus(); const start = document.querySelector("#nd .nd-line .nd-start");
    return { cap: document.querySelector("#nd .nd-line-cap").textContent, start: start.textContent, head: JSON.parse(document.getElementById("nd-data").textContent).days.find((d) => d.day === 45).head }; })()`);
  await evaluate(`(document.activeElement.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowRight", bubbles: true })), 1)`);
  const stepped = await evaluate(`({ on: document.activeElement.getAttribute("href"), start: document.querySelector("#nd .nd-line .nd-start").textContent })`);
  await evaluate(`(document.activeElement.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowLeft", bubbles: true })), 1)`);
  await evaluate(CLICK("#nd .nd-line .nd-start")); await sleep(300);
  const opened = await evaluate(`({ h: ${HEAD}, book: (document.querySelector("#nd .nd-book") || {}).textContent || "", save: ${KEY}, hash: location.hash, broke: ${BROKE} })`);
  if (aimed.cap !== "Day 45. " + aimed.head || aimed.start !== "Start at Day 45") fail(`focusing Day 45: the caption reads "${aimed.cap}", the button "${aimed.start}"`);
  else if (stepped.on !== "#day-60" || stepped.start !== "Start at Day 60") fail(`the arrow key from Day 45 went to ${stepped.on}, and Start reads "${stepped.start}"`);
  else if (!/^Day 45\. /.test(opened.h) || !/^Days 1 to 30 were played by the book/.test(opened.book) || !opened.save || opened.hash || opened.broke) fail(`"Start at Day 45" opened ${JSON.stringify(opened)}`);
  else console.log(`  ok   focusing Day 45 puts its headline under the line, the arrow keys move along it, and "Start at Day 45" opens it by the book, saved`);
  // c. pointing at a stop does the same, and a stop is a link: with a save, following it offers the choice as before
  await fromCold(1440, 900, "");
  await evaluate(`(document.querySelector('#nd .nd-line a[href="#day-75"]').dispatchEvent(new PointerEvent("pointerenter")), 1)`);
  const pointed = await evaluate(`document.querySelector("#nd .nd-line .nd-start").textContent`);
  await evaluate(CLICK('#nd .nd-line a[href="#day-75"]')); await sleep(400);
  const linkedDay = await evaluate(`({ h: ${HEAD}, save: ${KEY}, hash: location.hash })`);
  if (pointed !== "Start at Day 75") fail(`pointing at Day 75, Start reads "${pointed}"`);
  else if (!/^Day 75\. /.test(linkedDay.h) || linkedDay.save || linkedDay.hash !== "#day-75") fail(`the Day 75 stop, followed: ${JSON.stringify(linkedDay)}`);
  else console.log("  ok   pointing at Day 75 reads \"Start at Day 75\"; the stop itself is the link #day-75, and opens it unsaved, as a link does");
  // d. on a phone only Day 1 and the four milestones are links, each a 44px target, and the line is on the first screen
  await fromCold(390, 844, "");
  const small = await evaluate(`(() => { const a = [...document.querySelectorAll("#nd .nd-line-stops a")].filter((x) => x.getClientRects().length), r = (n) => n.getBoundingClientRect();
    return { days: a.map((x) => x.querySelector("b").textContent).join(" "), least: Math.min(...a.map((x) => Math.min(r(x).width, r(x).height))), marks: [...document.querySelectorAll("#nd .nd-line-stops .mk")].filter((x) => x.getClientRects().length).length,
      clash: a.some((x, i) => i && r(x).left < r(a[i - 1]).right - 0.5), bottom: Math.round(r(document.querySelector("#nd .nd-line")).bottom), over: document.documentElement.scrollWidth - document.documentElement.clientWidth }; })()`);
  if (small.days !== "1 15 45 75 90" || small.marks !== 8) fail(`390 wide: the links are ${small.days}, with ${small.marks} marks`);
  else if (small.least < 44 || small.clash) fail(`390 wide: the smallest stop is ${Math.round(small.least)}px${small.clash ? ", and two overlap" : ""}`);
  else if (small.bottom > 844 || small.over > 0) fail(`390 wide: the line ends at ${small.bottom}px, the page scrolls sideways by ${small.over}px`);
  else console.log(`  ok   390 wide: Day 1 and the four milestones are links of 44px or more, the other eight are marks, and the line ends at ${small.bottom}`);
  // e. Day 1's card: pressing an answer starts a whole-team run and makes that call
  await fromCold(1440, 900, "");
  const card = await evaluate(`(() => { const c = document.querySelector("#nd .nd-d1"); if (!c) return null; const b = [...c.querySelectorAll(".dc-o button")];
    return { kick: c.querySelector(".dc-k").textContent, answers: b.map((x) => x.textContent).join(" | "), tall: b.map((x) => Math.round(x.getBoundingClientRect().height)), pic: Math.round(c.querySelector("canvas").getBoundingClientRect().width) }; })()`);
  await evaluate(`[...document.querySelectorAll("#nd .nd-d1 .dc-o button")][1].click()`); await sleep(300);
  const made = await evaluate(`({ h: ${HEAD}, you: (document.querySelector("#nd .nd-out .nd-you b") || {}).textContent || "", save: JSON.parse(${KEY} || "{}"), broke: ${BROKE} })`);
  if (!card) fail("the title has no Day 1 card");
  else if (card.kick !== "Day 1 of 90 · Boardroom" || card.answers !== "Start the design from the 31 as writtenno days | Merge them into one list that keeps who asked1 day" || card.tall.some((x) => x !== 48) || card.pic !== 576) fail(`the Day 1 card: ${JSON.stringify(card)}`);
  else if (!/^Day 1\. /.test(made.h) || made.you !== "Merge them into one list that keeps who asked" || (made.save.opts || {}).mode !== "team" || (made.save.history || []).length !== 1 || made.broke) fail(`an answer on the card: ${JSON.stringify(made)}`);
  else console.log("  ok   Day 1's card: the boardroom at four times, two answers of 48px with their price, and the second starts a whole-team run with that call made");
  // f. in play: the phases over the strip, the next milestone under it, and a ring on one's own days
  await fromCold(1280, 800, ""); await evaluate(ROLE(1)); await sleep(300);
  const strip = await evaluate(`({ names: [...document.querySelectorAll("#nd .nd-phases span")].map((s) => s.textContent).join("|"), ahead: (document.querySelector("#nd .nd-ahead") || {}).textContent || "",
    mine: [...document.querySelectorAll("#nd .nd-strip li.mine")].map((li) => li.querySelector("span").textContent).join(" "), cells: new Set([...document.querySelectorAll("#nd .nd-strip li")].map((li) => Math.round(li.getBoundingClientRect().width))).size })`);
  if (strip.names !== "Frame|Design and spec|Build and prove|Run and learn" || strip.ahead !== "Next: the sign-off, Day 15") fail(`the strip in play: ${JSON.stringify(strip)}`);
  else if (strip.mine !== "1 4 6 9 12 20" || strip.cells !== 1) fail(`as the architect, the ringed days are ${strip.mine}, in cells of ${strip.cells} widths`);
  else console.log(`  ok   in play the strip keeps equal cells, names its phases, says "${strip.ahead}", and rings the architect's six days`);
  // g. a press that throws: an old sim.js under this game.js, with one function missing. The title stays, the
  // panel says so with a Reload button, and nothing is saved. On the real tree the notice never showed above.
  thrown.length = 0;
  await fromCold(1440, 900, "");
  await evaluate(`(delete window.ND.sim.soFar, 1)`);
  await evaluate(START); await sleep(200);
  const stale = await evaluate(`({ said: ${BROKE}, reload: !![...document.querySelectorAll("#nd .nd-broke button")].find((b) => b.textContent.trim() === "Reload"), focus: (document.activeElement || {}).textContent || "",
    title: !!document.querySelector("#nd .nd-line .nd-start") && !!document.querySelector("#nd .nd-d1"), playing: document.documentElement.classList.contains("nd-playing"),
    heading: Math.round(parseFloat(getComputedStyle(document.querySelector(".nd-top .nd-what")).fontSize)), save: ${KEY} })`);
  const logged = thrown.slice(); thrown.length = 0;
  if (stale.said !== "This page is out of date. Reload to play.Reload" || !stale.reload || stale.focus !== "Reload") fail(`a press that throws says "${stale.said}", focus on "${stale.focus}"`);
  else if (!stale.title || stale.playing || stale.heading < 30) fail(`a press that throws changed the screen: ${JSON.stringify(stale)}`);
  else if (stale.save) fail(`a press that throws saved a run: ${stale.save}`);
  else if (!logged.some((t) => /soFar/.test(t))) fail(`a press that throws leaves no console line naming the error: ${logged.join(" | ")}`);
  else console.log("  ok   with sim.soFar missing, Start leaves the title as it was, saves nothing, and says \"This page is out of date. Reload to play.\" with a Reload button");
  if (thrown.length) fail("section 12: script error: " + thrown[0]);

  {                               // its own block: section 12 has a card and a line of its own
    console.log("\n13. the building's key, the role rows, the day's card, and the loop at rest");
    thrown.length = 0;
    const box = (s) => `(() => { const n = document.querySelector(${JSON.stringify(s)}); if (!n) return null; const b = n.getBoundingClientRect(); return { l: Math.round(b.left), t: Math.round(b.top), r: Math.round(b.right), b: Math.round(b.bottom), w: Math.round(b.width), h: Math.round(b.height) }; })()`;
    // a. the title at 1440: a caption over the building, the key under it in two columns that end on the
    // building's edges, each room's line "QA · Maya · Days 45, 82", where Day 1 is, and the three marks
    await fromCold(1440, 900, "");
    const key = await evaluate(`(() => { const r = (n) => n.getBoundingClientRect(), chips = [...document.querySelectorAll("#nd .nd-chip")], map = r(document.querySelector("#nd .nd-map"));
      const marks = [...document.querySelectorAll("#nd .nd-marks li")];
      return { over: (document.querySelector("#nd .nd-over") || {}).textContent || "", texts: chips.map((c) => c.textContent), cols: new Set(chips.map((c) => Math.round(r(c).left))).size,
        left: Math.min(...chips.map((c) => r(c).left)) - map.left, right: Math.max(...chips.map((c) => r(c).right)) - map.right, below: Math.min(...chips.map((c) => r(c).top)) > map.bottom,
        where: document.querySelector("#nd .nd-where").textContent, marks: marks.map((m) => m.textContent).join("|"), samples: marks.map((m) => { const c = m.querySelector("canvas"); return c ? r(c).width + "x" + r(c).height + ":" + c.width + "x" + c.height : "none"; }).join(" ") }; })()`);
    const words = JSON.parse(await evaluate(`document.getElementById("nd-data").textContent`));
    if (key.over !== words.building.caption) fail(`the caption over the building reads "${key.over}"`);
    else if (key.texts.length !== 7 || !key.texts.includes("QA · Maya · Days 45, 82") || !key.texts.includes("Boardroom · Ines · Days 1, 9, 90") || !key.texts.includes("Contact centre · Day 82") || !key.texts.every((t) => /^[A-Z][a-z A-Z]+( · [A-Z][a-z]+)? · Days? [\d, ]+$/.test(t))) fail(`the key reads: ${key.texts.join(" | ")}`);
    else if (key.cols !== 2 || Math.abs(key.left) > 1 || Math.abs(key.right) > 1 || !key.below) fail(`at 1440 the key is in ${key.cols} columns, ${key.left}px and ${key.right}px off the building's edges`);
    else if (key.where !== "Day 1: the boardroom, top floor") fail(`under the building on the title: "${key.where}"`);
    else if (key.marks !== "Today's room|Shut until the sign-off|Something is due there" || key.samples !== "40x24:20x12 40x24:20x12 40x24:20x12") fail(`the marks: ${key.marks}, drawn ${key.samples}`);
    else console.log(`  ok   1440 wide: the building's caption, a key of seven rooms in two columns on its edges ("QA · Maya · Days 45, 82"), "${key.where}", and three marks drawn at twice their size`);
    // b. a room's card opens on its person, on the title as in play
    await evaluate(CLICK('#nd .nd-chip[data-room="qa"]')); await sleep(120);
    const qa = await evaluate(`({ card: (document.querySelector("#nd .nd-card p") || {}).textContent || "", focus: !!document.activeElement.closest(".nd-card"), pressed: document.querySelector('#nd .nd-chip[data-room="qa"]').getAttribute("aria-pressed") })`);
    await evaluate(CLICK('#nd .nd-chip[data-room="board"]')); await sleep(120);
    const board = await evaluate(`(document.querySelector("#nd .nd-card p") || {}).textContent || ""`);
    if (qa.card !== "Maya, QA lead, makes the calls on Days 45 and 82. Day 82 is held in the contact centre." || !qa.focus || qa.pressed !== "true") fail(`the QA room's card on the title: ${JSON.stringify(qa)}`);
    else if (!/^Ines, the sponsor, sits here with the finance controller and the compliance officer\. Days 1, 9 and 90 are held here\.$/.test(board)) fail(`the boardroom's card: "${board}"`);
    else console.log(`  ok   a room's card opens on its person: "${qa.card}"`);
    // c. the role rows: five of 64px at 1440, each one press, with the role's days lit on a 180px line, then the sponsor's row
    const rows = await evaluate(`(() => { const data = JSON.parse(document.getElementById("nd-data").textContent), r = (n) => n.getBoundingClientRect();
      return [...document.querySelectorAll("#nd .nd-rolebtns .nd-role, #nd .nd-orgrow .nd-role")].map((row, k) => { const b = row.querySelectorAll("button"), m = row.querySelector(".nd-mini");
        row.scrollIntoView({ block: "center", behavior: "instant" });
        const t = r(row.querySelector(".nd-role-says")), hit = document.elementFromPoint(t.left + 4, t.top + 4);      // a press on the row's words is a press on its button
        return { h: Math.round(r(row).height), buttons: b.length, label: b[0] ? b[0].textContent : "", line: m ? Math.round(r(m).width) : 0, lit: row.querySelectorAll(".nd-mini i.on").length,
          who: row.querySelector(".nd-role-who").textContent, press: !!hit && hit === b[0] }; }); })()`);
    const want = Object.values(words.roles).map((R) => ({ name: words.cast[R.who].name, calls: words.days.filter((d) => d.owner === R.who).length }));
    const cards = Object.values(words.roles).map((R) => R.card).concat(words.org.card), cw = cards.map((c) => [c.decide, c.leave, c.pick].join(" ").split(/\s+/).length);
    if (rows.length !== 6) fail(`the title has ${rows.length} rows to play from, not five roles and the sponsor`);
    else if (rows.some((x, k) => x.buttons !== 1 || !x.press || x.line !== 180)) fail(`a row is not one press with a 180px line: ${JSON.stringify(rows)}`);
    else if (rows.slice(0, 5).some((x) => Math.abs(x.h - 64) > 1)) fail(`at 1440 the role rows are ${rows.map((x) => x.h).join(", ")}px tall, not 64`);
    else if (rows.slice(0, 5).some((x, k) => x.label !== "Play as " + want[k].name || x.lit !== want[k].calls || !x.who.includes(want[k].calls + (want[k].calls > 1 ? " calls" : " call")))) fail(`the role rows: ${rows.map((x) => x.label + ", " + x.lit + " lit, " + x.who).join(" | ")}`);
    else if (rows[5].label !== "Set the rules") fail(`the sponsor's row offers "${rows[5].label}"`);
    else if ((await evaluate(`(() => { document.querySelector("#nd .nd-ways").scrollIntoView({ block: "start", behavior: "instant" }); return document.querySelector("#nd .nd-stage").getBoundingClientRect().bottom - document.querySelector("#nd .nd-ways").getBoundingClientRect().top; })()`)) > 0) fail("scrolled to the rows, the building's column lies over them");
    else if (cw.some((n) => n >= 70) || cards.some((c) => /[–—]/.test(Object.values(c).join(" ")) || !/^Pick this if /.test(c.pick))) fail(`a row's words run to ${Math.max(...cw)} words, or carry a dash`);
    else console.log(`  ok   1440 wide: five role rows of 64px and the sponsor's, each one press, "${rows[3].label}" with ${rows[3].lit} days lit on a 180px line, ${Math.max(...cw)} words at most`);
    // d. the day on the card's metrics, and one answer component on the title and in play
    const titleOpt = await evaluate(`(() => { const b = document.querySelector("#nd .nd-d1 .dc-o button"); return b.className + "|" + getComputedStyle(b.querySelector(".nd-opt-p")).backgroundColor; })()`);
    await evaluate(START); await sleep(400);
    const card = await evaluate(`(() => { const c = document.querySelector("#nd .nd-day"), cs = getComputedStyle(c), f = (s, p) => getComputedStyle(document.querySelector(s))[p], o = document.querySelector("#nd .nd-opts .nd-opt");
      const m = getComputedStyle(document.querySelector("#nd .nd-map"));
      const p = document.body.appendChild(document.createElement("i")); p.style.background = "var(--paper)"; const paper = getComputedStyle(p).backgroundColor; p.remove();
      return { radius: cs.borderTopLeftRadius, pad: cs.paddingLeft, bg: cs.backgroundColor === paper,
        kick: f("#nd .nd-kick", "fontSize") + " " + /mono/i.test(f("#nd .nd-kick", "fontFamily")), head: f("#nd .nd-dayhead h2", "fontSize") + " " + f("#nd .nd-dayhead h2", "textWrap"), body: f("#nd .nd-ctx", "fontSize") + " " + f("#nd .nd-lines span", "fontSize") + " " + f("#nd .nd-opts legend", "fontSize"),
        opt: Math.round(o.getBoundingClientRect().height) + " " + o.className + "|" + getComputedStyle(o.querySelector(".nd-opt-p")).backgroundColor, map: m.borderTopLeftRadius + " " + (m.boxShadow.match(/rgba?\\(/g) || []).length,
        where: document.querySelector("#nd .nd-where").textContent }; })()`);
    if (card.radius !== "20px" || card.pad !== "26px" || !card.bg) fail(`the day's card: ${JSON.stringify(card)}`);
    else if (card.kick !== "12.5px true" || card.head !== "25px balance" || card.body !== "15.5px 15.5px 15.5px") fail(`the day's sizes: kicker ${card.kick}, headline ${card.head}, body ${card.body}`);
    else if (card.opt !== "48 " + titleOpt.replace(/\|.*/, "") + "|rgba(0, 0, 0, 0)" || titleOpt !== "nd-opt|rgba(0, 0, 0, 0)") fail(`the answers: ${card.opt} in play, ${titleOpt} on the title`);
    else if (card.map !== "20px 2") fail(`the building's frame: ${card.map}`);
    else if (card.where !== "Today: the boardroom, top floor") fail(`under the building on Day 1: "${card.where}"`);
    else console.log(`  ok   1440 wide: the day on the card's paper (20px corner, 26px inset, 12.5, 25 and 15.5px), answers of 48px with a plain price, the same component as Day 1's card; "${card.where}"`);
    // e. the faults council 9 measured, each measured again: the context's measure, one inset for a tinted box,
    // the building at 1024 on the rail's edge, the building at a whole scale on a phone, faces at twice their
    // size, strip numbers at the 11px floor
    const MEASURE = `(() => { const c = document.querySelector("#nd .nd-ctx"), cs = getComputedStyle(c), x = document.createElement("canvas").getContext("2d"); x.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily; const t = c.textContent; return Math.round(c.clientWidth / (x.measureText(t).width / t.length)); })()`;
    const faults = [];
    for (const [w, h] of [[1440, 900], [1024, 768]]) {
      await fromCold(w, h, "#day-20");
      const cpl = await evaluate(MEASURE), inset = await evaluate(`getComputedStyle(document.querySelector("#nd .nd-events li")).paddingLeft`);
      if (cpl > 75) fail(`${w} wide: the context runs ${cpl} characters a line`);
      if (inset !== "16px") fail(`${w} wide: a tinted box is inset ${inset}`);
      faults.push(`${w}: context ${cpl} a line, box inset ${inset}`);
      if (w === 1024) {
        const edge = await evaluate(`({ map: ${box("#nd .nd-map")}, rail: ${box("#nd .nd-hud")}, card: ${box("#nd .nd-day")}, key: ${box("#nd .nd-rooms")} })`);
        if (edge.map.l !== edge.rail.l || Math.abs(edge.key.r - edge.card.r) > 1) fail(`1024 wide: the building starts at ${edge.map.l} against the rail at ${edge.rail.l}, the key ends at ${edge.key.r} against the card at ${edge.card.r}`);
        faults.push(`1024: building at x ${edge.map.l}, rail at ${edge.rail.l}`);
      }
    }
    for (const w of [390, 320]) {
      await fromCold(w, w === 390 ? 844 : 640, "#day-1");
      const ph = await evaluate(`(() => { const c = document.querySelector("#nd .nd-map-cv"), b = c.getBoundingClientRect(), f = document.querySelector("#nd .nd-face"), s = document.querySelector("#nd .nd-strip li");
        return { scale: b.width / c.width, col: Math.round(document.querySelector("#nd .nd-map").getBoundingClientRect().width), w: Math.round(b.width), face: Math.round(f.getBoundingClientRect().width) / 24,
          strip: Math.min(parseFloat(getComputedStyle(s).fontSize), parseFloat(getComputedStyle(s.querySelector("span")).fontSize)), scene: document.querySelector("#nd .nd-scene canvas").getBoundingClientRect().width / 144 }; })()`);
      if (ph.scale !== 1 || (w === 390 && ph.w !== ph.col)) fail(`${w} wide: the building is drawn at ${ph.scale.toFixed(3)} screen pixels to an art pixel, ${ph.w}px in a ${ph.col}px frame`);
      if (ph.face !== 2 || ph.scene !== 2) fail(`${w} wide: faces at ${ph.face}x and the room at ${ph.scene}x`);
      if (ph.strip < 11) fail(`${w} wide: the strip's numbers are ${ph.strip}px`);
      faults.push(`${w}: building at ${ph.scale}x (${ph.w}px in ${ph.col}), room at ${ph.scene}x, faces at ${ph.face}x, strip at ${ph.strip}px`);
    }
    console.log(`  ok   measured again: ${faults.join("; ")}`);
    // f. the loop rests while its canvases are off the screen: at 390 on Day 1 the building is far down the page,
    // and once the people have walked into the room at the top, nothing is drawn until the building is scrolled to
    await fromCold(390, 844, ""); await evaluate(START); await sleep(2200);
    const f0 = await evaluate(`window.NDFrames`); await sleep(1200);
    const f1 = await evaluate(`window.NDFrames`);
    await evaluate(`(document.querySelector("#nd .nd-map").scrollIntoView({ block: "center", behavior: "instant" }), 1)`); await sleep(900);
    const f2 = await evaluate(`window.NDFrames`);
    if (!(f0 > 0)) fail("at 390 the room's people never walked in");
    else if (f1 !== f0) fail(`at 390 on Day 1, with the building off the screen, the loop drew ${f1 - f0} frames in 1.2 seconds`);
    else if (!(f2 > f1)) fail("scrolled to, the building does not move");
    else console.log(`  ok   390 wide, Day 1: ${f0} frames as the people walk in, then none while the building is off the screen, and ${f2 - f1} once it is scrolled to`);
    if (thrown.length) fail("section 13: script error: " + thrown[0]);
  }
} catch (e) {
  failures++; console.log("\nthe play test itself failed: " + e.message);
} finally {
  ws.close();
  const exited = new Promise((r) => chrome.once("exit", r));
  chrome.kill();
  await Promise.race([exited, sleep(5000)]);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
console.log(failures ? `\n${failures} failure(s)` : "\nevery way to play reaches its verdict");
process.exit(failures ? 1 : 0);
