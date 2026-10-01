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
// clean, and that nothing scrolls sideways on a phone. Headless Chrome over the DevTools protocol,
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
    if (form.querySelector("#sd-saving")) boxes.slice(0, 3).forEach((b) => { if (!b.checked) b.click(); });
    else if (form.querySelector("#lk-context")) { if (!boxes[0].checked) boxes[0].click(); }
    else if (boxes.length && ${pick} === 1) boxes.forEach((b) => { if (!b.checked) b.click(); });
    form.querySelector("button[type=submit]").click();
    return "task";
  }
  const asked = ${ask} && byText("Ask to see the evidence");
  if (asked) { asked.click(); return "asked"; }
  const stand = byText("Let it stand"); if (stand) { stand.click(); return "stand"; }
  const gate = byText("Open the gate"); if (gate) { gate.click(); return "gate"; }
  const opts = q("#nd .nd-panel .nd-opt");
  if (opts.length) { at(opts).click(); return "choice"; }
  const next = game.querySelector(".nd-next"); if (next) { next.click(); return "next"; }
  return "STUCK";
})()`;
const FOCUS = `(() => { const a = document.activeElement; return !!a && !!a.closest("#nd"); })()`;

let failures = 0;
const fail = (what) => { failures++; console.log("  FAIL " + what); };

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
