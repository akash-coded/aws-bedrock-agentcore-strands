// A lab, played in a real browser: by the book, off the book, and every path between.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/lab.test.mjs http://localhost:8799/labs/grow-the-spec/
//
// The script is checked without a browser by site/pages/labs.py (every flag matches one line, every
// recording carries the prompt the parts join into, every call has the book's option). This checks the
// page that sits on it: that the lab can be played from the first beat to the debrief with nothing but
// the controls on the page, on each path the script has; that the prompt the page assembles is the
// prompt that was recorded, byte for byte; that marking every fault scores full and marking nothing
// scores nothing, with no false "caught"; that the document on the right ends in the state the script
// says; that a reload in the middle comes back to the same beat; that Run without a choice made does
// not go on; that the focus moves to each new beat; that no script error is thrown; that every beat, live or
// past, stacks its parts one under another; that nothing scrolls sideways on a phone; that without script
// the page reads as a document with every recording in it; and, where the debrief shows other models' replies to
// the same prompts, that both its tables carry the lab's own model and three more, fit at 1440 and 1024 and stack
// one block a row at 390 and 320, that its fold reads in six replies, each stamped with its model, maker and date
// and each exactly as its file in the repository, and that the reading version without script has the tables.
// Headless Chrome over the DevTools protocol, the same as accept.mjs, so there is nothing to install.
import { spawn } from "node:child_process";
import { readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const URL_ = process.argv[2];
if (!URL_) { console.error("usage: node lab.test.mjs <lab url>"); process.exit(2); }
const here = dirname(fileURLToPath(import.meta.url));
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `labtest-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsurl;
for (let i = 0; i < 60 && !wsurl; i++) {
  try { wsurl = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find((t) => t.type === "page").webSocketDebuggerUrl; } catch { await sleep(250); }
}
if (!wsurl) { console.error("Chrome did not start"); process.exit(1); }
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

let failures = 0;
const check = (ok, what) => { if (!ok) { failures++; console.log("  FAIL " + what); } };
const open = async (url, { width = 1280, height = 800, noscript = false } = {}) => {
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: width < 600 });
  await send("Emulation.setScriptExecutionDisabled", { value: noscript });
  await send("Page.navigate", { url });
  await sleep(900);
  await send("Emulation.setScriptExecutionDisabled", { value: false });
};

// One press, the way a player would: whatever the live beat offers. `plan` says which option to take
// in each slot or call, and whether to mark every fault, nothing, or everything (faults and sound lines).
const STEP = (plan) => `(() => {
  const plan = ${JSON.stringify(plan)};
  const live = document.querySelector(".lab-beat.live");
  if (!live) return document.querySelector(".lab-debrief") ? "END" : "STUCK: no live beat";
  const b = window.Lab.current(), id = live.getAttribute("data-beat");
  if (!b || b.id !== id) return "STUCK: live beat " + id + " is not the current one " + (b && b.id);
  const press = (sel) => { const e = live.querySelector(sel); if (!e) return false; e.click(); return true; };
  if (b.kind === "note" || b.kind === "run") return press('[data-act="ok"]') ? id + ":ok" : "STUCK: no Go on in " + id;
  if (b.kind === "compose") {
    const want = plan.slots[id] || {};
    for (const part of b.parts) {
      if (!part.options) continue;
      const v = want[part.id] || part.options[0].id;
      const r = live.querySelector('input[name="' + id + "-" + part.id + '"][value="' + v + '"]');
      if (!r) return "STUCK: no option " + v + " in " + id;
      r.click();
    }
    return press('[data-act="run"]') ? id + ":run" : "STUCK: no Run in " + id;
  }
  if (b.kind === "mark") {
    const lines = [...live.querySelectorAll("button.lab-ln")];
    const doc = window.Lab.data.replies[b.doc];
    lines.forEach((btn) => {
      const ln = doc.lines[+btn.getAttribute("data-ln")];
      if (plan.marks === "all" ? ln.flag : plan.marks === "everything" ? true : false) btn.click();
    });
    return press('[data-act="check"]') ? id + ":check" : "STUCK: no Check in " + id;
  }
  if (b.kind === "choose" || b.kind === "compare") {
    const v = plan.calls[id]; if (!v) return "STUCK: no plan for call " + id;
    return press('[data-opt="' + v + '"]') ? id + ":" + v : "STUCK: no option " + v + " in " + id;
  }
  if (b.kind === "file") return press('[data-act="file"]') ? id + ":file" : "STUCK: no File in " + id;
  return "STUCK: kind " + b.kind;
})()`;
const FOCUS = `(() => { const a = document.activeElement; return a ? (a.getAttribute("data-beat") || a.className.split(" ")[0] || a.tagName) : "none"; })()`;
const STATE = `(() => { const a = window.Lab.artefact(); return { done: document.getElementById("lab").getAttribute("data-done"), version: a.version,
  states: Object.fromEntries(a.sections.map((s) => [s.id, s.state])), decided: a.sections.filter((s) => s.state === "decided").length,
  tally: (document.querySelector(".lab-tally") || {}).textContent || "", scores: [...document.querySelectorAll(".lab-score")].map((e) => e.textContent.trim()),
  steps: (document.querySelector(".lab-foot span") || {}).textContent || "", over: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  rows: [...document.querySelectorAll(".lab-beat")].filter((b) => { const k = [...b.children].map((c) => c.getBoundingClientRect()).filter((r) => r.height);
    return k.some((r, i) => i && r.top < k[i - 1].bottom - 1); }).map((b) => b.getAttribute("data-beat")),
  wide: [...document.querySelectorAll("main *")].filter((e) => e.getBoundingClientRect().right > innerWidth + 1 || e.scrollWidth > e.clientWidth + 1).slice(0, 8)
    .map((e) => e.tagName.toLowerCase() + "." + String(e.className).split(" ")[0] + " r=" + Math.round(e.getBoundingClientRect().right) + " sw=" + e.scrollWidth + "/" + e.clientWidth) }; })()`;

async function play(plan, label, { width = 1280 } = {}) {
  await open(URL_, { width });
  await evaluate("localStorage.clear(); true");
  await open(URL_, { width });
  thrown.length = 0;
  const trail = [];
  for (let i = 0; i < 40; i++) {
    const r = await evaluate(STEP(plan));
    trail.push(r);
    if (r === "END" || r.startsWith("STUCK")) break;
    await sleep(120);
    const f = await evaluate(FOCUS);
    check(f !== "none" && f !== "BODY", `${label}: after ${r} the focus is on ${f}`);
  }
  const last = trail[trail.length - 1];
  check(last === "END", `${label}: ${last} (${trail.join(" → ")})`);
  check(!thrown.length, `${label}: script error: ${thrown[0]}`);
  const st = await evaluate(STATE);
  console.log(`  ${label}: ${trail.length - 1} presses, ${st.decided} of 8 decided, version ${st.version}, ${st.tally.trim()}`);
  return { st, trail };
}

try {
  await send("Page.enable"); await send("Runtime.enable");
  const prompts = {};
  for (const f of ["a-ask", "a-draft", "b-none", "b-defaults", "b-flag", "d-ears"]) prompts[f] = readFileSync(join(here, "..", "content", "labs", "grow-the-spec", `prompt-${f}.txt`), "utf8").replace(/\n$/, "");

  console.log("\n1. the page: script on, the reading version put away, the bench and the document shown");
  await open(URL_);
  const page = await evaluate(`(() => ({ on: document.documentElement.classList.contains("lab-on"), plain: getComputedStyle(document.querySelector(".lab-plain")).display,
    bench: !!document.querySelector(".lab-bench .lab-beat.live"), side: !!document.querySelector(".lab-side .lab-doc"), stamp: !!document.querySelector(".lab-plain") }))()`);
  check(page.on && page.plain === "none" && page.bench && page.side, `page: ${JSON.stringify(page)}`);
  check(!thrown.length, "script error on load: " + thrown[0]);

  console.log("\n2. the prompts the page assembles are the recorded ones");
  await evaluate("localStorage.clear(); true"); await open(URL_);
  await evaluate(STEP({ slots: {}, calls: {}, marks: "all" }));            // past the note
  for (const [what, file] of [["ask", "a-ask"], ["draft", "a-draft"]]) {
    await evaluate(`document.querySelector('input[name="ask-what"][value="${what}"]').click(); true`);
    const got = await evaluate(`window.Lab.prompt("ask")`);
    check(got === prompts[file], `prompt A with "${what}" is not prompt-${file}.txt (${got.length} vs ${prompts[file].length} chars)`);
  }
  await evaluate(`document.querySelector('input[name="ask-what"][value="ask"]').click(); document.querySelector('[data-act="run"]').click(); true`); await sleep(150);
  await evaluate(STEP({ slots: {}, calls: {}, marks: "all" })); await sleep(100);   // the run
  await evaluate(STEP({ slots: {}, calls: {}, marks: "all" })); await sleep(100);   // Priya answers
  for (const [gaps, file] of [["none", "b-none"], ["defaults", "b-defaults"], ["flag", "b-flag"]]) {
    await evaluate(`document.querySelector('input[name="gaps-gaps"][value="${gaps}"]').click(); true`);
    const got = await evaluate(`window.Lab.prompt("gaps")`);
    check(got === prompts[file], `prompt B with "${gaps}" is not prompt-${file}.txt (${got.length} vs ${prompts[file].length} chars)`);
  }
  const d = await evaluate(`window.Lab.prompt("ears")`);
  check(d === prompts["d-ears"], `prompt D is not prompt-d-ears.txt (${d.length} vs ${prompts["d-ears"].length} chars)`);
  console.log("  prompts A (both), B (all three) and D match their recordings");

  console.log("\n3. Run with a slot left open does not go on");
  await evaluate("localStorage.clear(); true"); await open(URL_);
  await evaluate(STEP({ slots: {}, calls: {}, marks: "all" })); await sleep(100);
  const before = await evaluate(`window.Lab.current().id`);
  await evaluate(`document.querySelector('[data-act="run"]').click(); true`); await sleep(100);
  const after = await evaluate(`({ id: window.Lab.current().id, need: !!document.querySelector(".lab-slot.need"), focus: document.activeElement && document.activeElement.type })`);
  check(before === "ask" && after.id === "ask" && after.need && after.focus === "radio", `pressed Run with nothing chosen: ${JSON.stringify(after)}`);
  console.log("  the slot is asked for, and takes the focus");

  console.log("\n4. by the book: every fault marked, every call the book's");
  const book = await play({ slots: { ask: { what: "ask" }, gaps: { gaps: "flag" } }, calls: { call: "owners", measures: "owners", hand: "struct" }, marks: "all" }, "by the book");
  check(book.st.done === "1" && book.st.decided === 7 && book.st.states.rec === "open" && book.st.version === 3, `by the book ends: ${JSON.stringify(book.st)}`);
  check(/caught 13 of 13/.test(book.st.tally.replace(/\s+/g, " ")) && /3 of 3 calls/.test(book.st.tally), `the tally: ${book.st.tally}`);
  check(book.st.scores.every((s) => / 0 marked that were sound/.test(s) === false), `a sound line was counted as marked: ${book.st.scores.join(" | ")}`);
  check(!book.st.rows.length, `a beat lays its parts side by side instead of one under another (a site rule on its class?): ${book.st.rows.join(", ")}`);
  const pack = await evaluate(`JSON.parse(localStorage.getItem("skyways.labs.pack") || "{}")["grow-the-spec"]`);
  check(pack && /8 Records\nNOT DECIDED/.test(pack.body) && /Spec|AC-1/.test(pack.body), "the filed document is not in the pack, or is not the book's");

  console.log("\n5. off the book: nothing marked, the wrong call each time");
  const off = await play({ slots: { ask: { what: "draft" }, gaps: { gaps: "defaults" } }, calls: { call: "keep", measures: "fill", hand: "prose" }, marks: "none" }, "off the book");
  check(off.st.done === "1" && off.st.states.rec === "guessed" && off.st.states.ac === "draft" && off.st.version === 2 && off.st.decided === 6, `off the book ends: ${JSON.stringify(off.st)}`);
  check(/caught 0 of 25/.test(off.st.tally.replace(/\s+/g, " ")) && /0 of 3 calls/.test(off.st.tally), `the tally: ${off.st.tally}`);

  console.log("\n6. the third path: say nothing, decide alone, drop the measures; everything marked");
  const mid = await play({ slots: { ask: { what: "ask" }, gaps: { gaps: "none" } }, calls: { call: "self", measures: "drop", hand: "struct" }, marks: "everything" }, "the third path");
  check(mid.st.done === "1" && mid.st.states.role === "decided" && mid.st.states.rec === "guessed" && mid.st.states.ac === "draft", `the third path ends: ${JSON.stringify(mid.st)}`);
  check(/1 of 3 calls/.test(mid.st.tally), `the tally: ${mid.st.tally}`);
  check(mid.st.scores.every((s) => /marked that were sound/.test(s)), `marking everything should count the sound lines: ${mid.st.scores.join(" | ")}`);

  console.log("\n7. a reload in the middle comes back to the same beat; Start again starts clean");
  await evaluate("localStorage.clear(); true"); await open(URL_);
  for (let i = 0; i < 4; i++) { await evaluate(STEP({ slots: { ask: { what: "ask" } }, calls: {}, marks: "all" })); await sleep(100); }
  const at = await evaluate(`window.Lab.current().id`);
  await open(URL_);
  const back = await evaluate(`({ id: window.Lab.current().id, shown: document.querySelectorAll(".lab-beat").length })`);
  check(back.id === at && back.shown >= 4, `after a reload: at ${back.id}, was at ${at}, ${back.shown} beats shown`);
  await evaluate(`document.querySelector('[data-act="reset"]').click(); true`); await sleep(100);
  check((await evaluate(`window.Lab.current().id`)) === "start", "Start again did not go back to the first beat");
  console.log(`  came back to ${back.id}`);

  console.log("\n8. a phone: nothing scrolls sideways, the document sits above the bench");
  for (const w of [320, 375]) {
    await evaluate("localStorage.clear(); true");
    const r = await play({ slots: { ask: { what: "ask" }, gaps: { gaps: "flag" } }, calls: { call: "owners", measures: "owners", hand: "struct" }, marks: "all" }, `${w}px`, { width: w });
    check(r.st.over <= 0, `at ${w}px the page scrolls sideways by ${r.st.over}px: ${r.st.wide.join(", ")}`);
    check(!r.st.rows.length, `at ${w}px a beat lays its parts side by side: ${r.st.rows.join(", ")}`);
    const order = await evaluate(`(() => { const s = document.querySelector(".lab-side").getBoundingClientRect(), b = document.querySelector(".lab-bench").getBoundingClientRect(); return s.top <= b.top; })()`);
    check(order, `at ${w}px the document is not above the bench`);
  }

  console.log("\n9. without script: the lab reads as a document, with every recording stamped");
  await open(URL_, { noscript: true });
  const plain = await evaluate(`(() => { const p = document.querySelector(".lab-plain"); return { shown: getComputedStyle(p).display !== "none", bench: getComputedStyle(document.getElementById("lab")).display,
    stamps: (p.textContent.match(/Recorded reply \\(/g) || []).length, doc: /8 Records/.test(p.textContent), h1: !!document.querySelector("main h1") }; })()`);
  check(plain.shown && plain.bench === "none" && plain.stamps >= 5 && plain.doc && plain.h1, `without script: ${JSON.stringify(plain)}`);
  console.log(`  ${plain.stamps} recordings, the document by the book at the end`);

  // The debrief's part on other models (debrief.others): two tables, the lab's own model and three more, built from
  // replies the build has checked; and a fold that reads the replies in from their own page. Skipped for a lab
  // whose debrief has no such part.
  console.log("\n10. the debrief: three more models, the same prompts");
  const OTHERS = `(() => { const o = document.querySelector(".lab-debrief .lab-others"); if (!o) return null;
    return { tables: [...o.querySelectorAll("table")].map((t) => ({ cols: [...t.querySelectorAll("thead th")].slice(1).map((th) => th.textContent.trim()),
        empty: [...t.querySelectorAll("tbody th, tbody td")].filter((c) => !c.textContent.trim()).length, rows: t.querySelectorAll("tbody tr").length,
        stacked: getComputedStyle(t.querySelector("tbody tr")).display === "block", over: t.parentElement.scrollWidth - t.parentElement.clientWidth,
        out: Math.round(t.getBoundingClientRect().right - t.parentElement.getBoundingClientRect().right) })),
      fold: (() => { const f = o.querySelector("details.lab-fold"); return f && { open: f.open, src: f.getAttribute("data-src") }; })(),
      page: document.documentElement.scrollWidth - document.documentElement.clientWidth }; })()`;
  const REPLIES = `(() => [...document.querySelectorAll(".lab-debrief .lab-fold .lab-reply")].map((r) => ({ id: r.id, stamp: r.querySelector(".lab-stamp").textContent,
    text: [...r.querySelectorAll(".lab-lines > .lab-ln")].map((l) => l.textContent).join("\\n") })))()`;
  const openFold = async () => {
    await evaluate(`(() => { const f = document.querySelector(".lab-debrief .lab-fold"); if (f && !f.open) f.querySelector("summary").click(); return true; })()`);
    for (let i = 0; i < 40; i++) { const n = await evaluate(`document.querySelectorAll(".lab-debrief .lab-fold .lab-reply").length`); if (n) break; await sleep(100); }
    return evaluate(REPLIES);
  };
  await play({ slots: { ask: { what: "ask" }, gaps: { gaps: "flag" } }, calls: { call: "owners", measures: "owners", hand: "struct" }, marks: "all" }, "by the book, 1440", { width: 1440 });
  const own = await evaluate(`window.Lab.data.replies["a-draft"] && window.Lab.data.replies["a-draft"].model`);
  const wide = await evaluate(OTHERS);
  if (!wide) console.log("  this lab's debrief has no part on other models");
  else {
    check(wide.tables.length === 2, `the debrief shows ${wide.tables.length} tables, not 2`);
    for (const t of wide.tables) {
      check(t.cols.length === 4 && t.cols[0] === own && new Set(t.cols).size === 4 && t.cols.every((c) => c), `a table's model columns are ${JSON.stringify(t.cols)}: the lab's own (${own}) and three more`);
      check(!t.empty && t.rows >= 3, `a table has ${t.empty} empty cells and ${t.rows} rows`);
      check(!t.stacked && t.over <= 0 && t.out <= 0, `at 1440 a table does not fit its box: ${JSON.stringify(t)}`);
    }
    check(wide.fold && wide.fold.open === false && wide.fold.src, `the fold of replies is not there, or not closed: ${JSON.stringify(wide.fold)}`);
    const reps = await openFold();
    check(reps.length === 6, `the fold holds ${reps.length} replies, not 6`);
    for (const r of reps) {
      const [, model, maker, date] = r.stamp.split(" · ");
      check(wide.tables[0].cols.includes(model) && maker && /^\d{1,2} [A-Z][a-z]+ \d{4}$/.test(date || ""), `a reply's stamp does not name a model, its maker and a date: ${r.stamp}`);
      let file = "";
      try { file = readFileSync(join(here, "..", "content", "labs", "grow-the-spec", "others", `${r.id}.md`), "utf8"); } catch { /* checked below */ }
      check(file && r.text === file.replace(/^\n+|\n+$/g, "").split("\n").map((l) => l.replace(/\s+$/, "")).join("\n"), `the reply ${r.id} on the page is not others/${r.id}.md as its model wrote it`);
    }
    check(!thrown.length, `script error in the debrief: ${thrown[0]}`);
    console.log(`  ${wide.tables.length} tables of ${wide.tables.map((t) => t.rows).join(" and ")} rows, columns ${wide.tables[0].cols.join(", ")}; the fold read in ${reps.length} replies, each as written`);

    await open(URL_, { width: 1024 });
    const mid = await evaluate(OTHERS);
    check(mid && mid.tables.every((t) => !t.stacked && t.cols.length === 4 && t.over <= 0 && t.out <= 0) && mid.page <= 0, `at 1024 the four model columns do not fit: ${JSON.stringify(mid)}`);
    for (const w of [390, 320]) {
      await open(URL_, { width: w });
      const small = await evaluate(OTHERS);
      check(small && small.tables.every((t) => t.stacked && t.over <= 0 && t.out <= 0), `at ${w}px a table does not stack one block a row: ${JSON.stringify(small && small.tables)}`);
      const n = (await openFold()).length;
      const over = await evaluate(`document.documentElement.scrollWidth - document.documentElement.clientWidth`);
      check(n === 6 && over <= 0, `at ${w}px with the replies open: ${n} replies, the page scrolls sideways by ${over}px`);
      await open(new URL(wide.fold.src, URL_).href, { width: w });
      const page = await evaluate(`({ over: document.documentElement.scrollWidth - document.documentElement.clientWidth, replies: document.querySelectorAll(".lab-others-replies .lab-reply").length })`);
      check(page.over <= 0 && page.replies === 6, `at ${w}px the replies' own page: ${JSON.stringify(page)}`);
    }
    console.log("  at 1024 the four model columns fit; at 390 and 320 each row is one block and nothing scrolls sideways, with the replies open and on their own page");

    await open(URL_, { noscript: true });
    const read = await evaluate(`(() => { const o = document.querySelector(".lab-plain .lab-others"); return o && { tables: o.querySelectorAll("table").length,
      cols: [...o.querySelectorAll("table")].map((t) => t.querySelectorAll("thead th").length - 1), link: !!o.querySelector('details.lab-fold a[href="${wide.fold.src}"]') }; })()`);
    check(read && read.tables === 2 && read.cols.every((c) => c === 4) && read.link, `without script the reading version lacks the tables or the way to the replies: ${JSON.stringify(read)}`);
    await open(new URL(wide.fold.src, URL_).href, { noscript: true });
    const alone = await evaluate(`[...document.querySelectorAll(".lab-others-replies .lab-reply .lab-stamp")].map((s) => s.textContent)`);
    check(alone.length === 6 && alone.every((s) => /\d{1,2} [A-Z][a-z]+ \d{4}/.test(s)), `without script the replies' page shows ${alone.length} dated replies, not 6`);
    console.log("  without script the reading version has both tables, and the replies' page has all six");
  }

  console.log(failures ? `\n${failures} failed` : "\nthe lab plays");
} finally {
  ws.close();
  const exited = new Promise((r) => chrome.once("exit", r));
  chrome.kill();
  await exited;
  // Chrome's helpers can still be writing its profile as it exits: a failed clean-up is not a failed test
  try { rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 }); } catch { /* left in the temp folder */ }
}
process.exit(failures ? 1 : 0);
