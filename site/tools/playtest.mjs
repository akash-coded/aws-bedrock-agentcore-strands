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
// is a sentence. Headless Chrome over the DevTools protocol,
// the same as accept.mjs, so there is nothing to install.
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
  const stand = byText("Let it stand"); if (stand) { stand.click(); return "stand"; }
  const gate = byText("Sign and start the build"); if (gate) { gate.click(); return "gate"; }
  const opts = q("#nd .nd-panel .nd-opt");
  if (opts.length) { at(opts).click(); return "choice"; }
  const next = game.querySelector(".nd-next"); if (next) { next.click(); return "next"; }
  return "STUCK";
})()`;
const FOCUS = `(() => { const a = document.activeElement; return !!a && !!a.closest("#nd"); })()`;

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
  let moves = 0, last = "";
  while (moves++ < 160) {
    last = await evaluate(STEP(pick, ask));
    if (last === "END" || last === "STUCK") break;
    await sleep(25);
    const h = await evaluate(HEAD); if (h) heads.add(h);
    if (!(await evaluate(FOCUS))) { fail(`${label}: the focus left the game after a ${last}`); break; }
    if (phone) { const over = await evaluate(`document.documentElement.scrollWidth - document.documentElement.clientWidth`); if (over > 0) { fail(`${label}: scrolls sideways by ${over}px`); break; } }
  }
  const verdict = await evaluate(`(document.querySelector(".nd-verdict h2") || {}).textContent || ""`);
  if (last !== "END") fail(`${label}: ${last === "STUCK" ? "nothing to press" : "no verdict"} after ${moves} moves`);
  if (thrown.length) fail(`${label}: script error: ${thrown[0]}`);
  console.log(`  ${last === "END" && !thrown.length ? "ok  " : "    "} ${label}: ${verdict || "(no verdict)"} in ${moves} moves`);
}

const START = `(() => { const b = [...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim() === "Start at Day 1"); if (!b) return false; b.click(); return true; })()`;
const ROLE = (n) => `(() => { const b = document.querySelectorAll("#nd .nd-rolebtns button")[${n}]; if (!b) return false; b.click(); return true; })()`;
const ORG = (ids) => `(() => { const b = [...document.querySelectorAll("#nd button")].find((x) => x.textContent.trim() === "Set the rules"); if (!b) return false; b.click();
  ${JSON.stringify(ids)}.forEach((id) => document.getElementById("po-" + id).click());
  document.querySelector("#nd form.nd-org button[type=submit]").click(); return true; })()`;

try {
  await send("Page.enable"); await send("Runtime.enable");

  console.log("\n1. the whole team");
  await play("always the first option", START, 0);
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
  thrown.length = 0;
  await fresh(1280, 800, false);
  await evaluate(START); await sleep(900);
  const moving = await evaluate(`window.NDFrames`);
  await evaluate(`document.querySelector("#nd [data-motion-toggle]").click()`); await sleep(300);
  const held = await evaluate(`window.NDFrames`); await sleep(700);
  const after = await evaluate(`window.NDFrames`);
  if (!(moving > 0)) fail("with motion allowed the picture never moved"); else if (after !== held) fail(`paused, the picture drew ${after - held} more frames`); else console.log("  ok   the pause control stops the picture");
  // paused, a new day still shows its people: count the room's skin-coloured pixels
  for (let i = 0; i < 2; i++) { await evaluate(STEP(1, false)); await sleep(60); }
  const people = await evaluate(`(() => { const c = document.querySelector(".nd-scene-cv"), d = c.getContext("2d").getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 0; i < d.length; i += 4) if (d[i] > 130 && d[i + 1] > 80 && d[i + 2] > 50 && d[i] - d[i + 2] > 40 && d[i] > d[i + 1]) n++; return n; })()`);
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
  const PILL = `(() => { const a = document.querySelector("a.play[data-ctx-lesson]"); return a ? { href: a.getAttribute("href"), lg: (a.querySelector(".lg") || {}).textContent, sm: (a.querySelector(".sm") || {}).textContent, title: a.getAttribute("title") } : null; })()`;
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
