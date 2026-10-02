// The workbench, driven in a real browser: every route, both widths, both themes.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/workbench.test.mjs http://localhost:8799/workbench/
//
// The workbench is one self-contained file (site/app/SkyWays-Architect.html) that the build frames and
// publishes at /workbench/. This checks what a reader meets there, with motion on:
//   1. every route opens without a script error, with its title in the first screen and no sideways scroll,
//      at 1440x900 and 390x844, dark and light, and its text meets 4.5:1;
//   2. the page opens dark, the toggle turns it light, and the choice is stored under the site's own key;
//   3. the top bar carries the mark, one filled pill to the game, one quiet link to the manual, the tutorial
//      at the head of the Learn list, and the theme toggle;
//   4. a link from the game or a lesson to a part of a page lands on that part, loaded cold;
//   5. all seventeen calculators recompute, the evidence pack survives a reload, a decision walk can be
//      finished, and state saved by the earlier version still loads;
//   6. no old name, mascot, rank or points counter is left on any route, and nothing moves on its own;
//   7. the ten pictures simshots.mjs captures still have their selectors and their pixel sizes;
//   8. the file opened alone from disk, with no network, still has its fonts and its calculators.
// Headless Chrome over the DevTools protocol, the same as accept.mjs, so there is nothing to install.
import { spawn } from "node:child_process";
import { rmSync, readFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const BASE = process.argv[2];
if (!BASE) { console.error("usage: node workbench.test.mjs <workbench url>"); process.exit(2); }
const HERE = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(HERE, "..", "app", "SkyWays-Architect.html");
const PICTURES = join(HERE, "..", "assets", "pictures");
// While working on one thing: ONLY=routes,theme runs some sections; ROUTES=start,quest some routes; SIZES=390 one
// width; THEMES=dark one theme; MORE=1 lists every low-contrast text instead of the first six.
const list = (name) => (process.env[name] || "").split(",").filter(Boolean);
const ONLY = list("ONLY"), SOME_ROUTES = list("ROUTES"), SIZES = list("SIZES"), THEMES = list("THEMES");
const want = (name) => !ONLY.length || ONLY.includes(name);

const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `workbench-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "--allow-file-access-from-files", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
setTimeout(() => { console.error("workbench: timed out"); process.exit(3); }, 20 * 60 * 1000).unref();
let wsurl;
for (let i = 0; i < 60 && !wsurl; i++) {
  try { wsurl = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find((t) => t.type === "page").webSocketDebuggerUrl; } catch { await sleep(250); }
}
const ws = new WebSocket(wsurl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const waiting = new Map(); let thrown = []; let failedRequests = [];
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.method === "Runtime.exceptionThrown") thrown.push((m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 200));
  if (m.method === "Log.entryAdded" && m.params.entry.level === "error") thrown.push(m.params.entry.text.slice(0, 160));
  if (m.method === "Network.loadingFailed") failedRequests.push(m.params.errorText);
  if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m.result || {}); waiting.delete(m.id); }
});
const send = (method, params = {}) => new Promise((ok) => { const id = ++seq; waiting.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
const evaluate = async (expression) => {
  const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error("in page: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text).slice(0, 300));
  return r.result?.value;
};

let passed = 0; const failures = [];
const check = (ok, what, detail = "") => {
  if (ok) { passed += 1; if (process.env.VERBOSE) console.log("  ok    " + what); }
  else { failures.push(what); console.log("  FAIL  " + what + (detail ? "  [" + String(detail).slice(0, process.env.MORE ? 6000 : 400) + "]" : "")); }
};

// ---- the places a reader can be --------------------------------------------------------------------
const ROUTES = [
  ["start", "#/start"], ["quest", "#/quest"], ["story", "#/story"], ["episode", "#/episode/req1"],
  ["sims", "#/simulations"], ["sim-nfr", "#/simulations/nfr"], ["loopmap", "#/loopmap"], ["concepts", "#/concepts"],
  ["learn", "#/learn"], ["unit", "#/learn/bar"], ["compare", "#/compare"], ["process", "#/process"],
  ["process-sa", "#/process/sa"], ["route", "#/route"], ["route-sa", "#/route/sa"], ["effort", "#/effort"],
  ["gov", "#/governance"], ["toolkit", "#/toolkit"], ["tool-bar", "#/toolkit/bar"], ["evidence", "#/evidence"],
  ["overview", "#/overview"], ["sa", "#/sa"], ["pm", "#/pm"], ["eng", "#/eng"], ["guide", "#/guide"],
  ["guide-ref", "#/guide/ref-frameworks"],
];
// every link into a part of a page that the manual, the lessons and the game carry (grep "workbench/#/")
const PART_LINKS = [
  ["#/toolkit/aifit", "tool-aifit"], ["#/toolkit/autonomy", "tool-autonomy"], ["#/toolkit/bar", "tool-bar"],
  ["#/toolkit/bolts", "tool-bolts"], ["#/toolkit/bvb", "tool-bvb"], ["#/toolkit/confidence", "tool-confidence"],
  ["#/toolkit/cutover", "tool-cutover"], ["#/toolkit/gateclass", "tool-gateclass"], ["#/toolkit/gates", "tool-gates"],
  ["#/toolkit/leaks", "tool-leaks"], ["#/toolkit/maturity", "tool-maturity"], ["#/toolkit/queue", "tool-queue"],
  ["#/toolkit/report", "tool-report"], ["#/toolkit/utree", "tool-utree"], ["#/governance/gv-gates", "gv-gates"],
];
const PAGE_LINKS = ["#/start", "#/loopmap", "#/evidence", "#/effort", "#/toolkit", "#/story", "#/governance", "#/concepts",
  "#/compare", "#/simulations", "#/quest", "#/process", "#/learn", "#/guide", "#/episode/adr1", "#/episode/req1"];
const GONE = ["PDLC Simulator", "this simulator", "whole simulator", "Your rank", "Ground crew", "Hi, I'm Sky", "Champion",
  "in the vault", "Open the vault", "streak", "side quest", "Points from checks", "Welcome to SkyWays", "—", "–"];
// the pictures simshots.mjs captures, with the route each lives on
const SHOTS = [
  ["sim-flight-plan", "#/quest", ".xrt"], ["sim-line-vs-loop", "#/start", "#illo-pdlc"], ["sim-spine", "#/start", "#illo-spine"],
  ["sim-methods", "#/start", "#illo-methods"], ["sim-roles", "#/start", "#illo-roles"],
  ["sim-three-efforts", "#/effort", "#ef-tiers .xef-tiers"], ["sim-same-task", "#/effort", "#ef-same .xtw"],
  ["sim-concept-map", "#/concepts", ".xzm-w"], ["sim-loop-map", "#/loopmap", "#lm-big"], ["sim-gates", "#/governance", "#gv-gates .xfig"],
];
// what the earlier version left in a reader's browser
const SAVED = {
  "skyways.pack": JSON.stringify([{ title: "Acceptance bar calculator", text: "ACCEPTANCE BAR SHEET" }, { title: "The NFR workshop · simulation", text: "RATIFIED NFRs" }]),
  "skyways.quest": JSON.stringify({ v: { req1: 1 }, c: { req1: 1 }, s: {}, t: { bar: 1 } }),
  "skyways.game": JSON.stringify({ pts: 3, streak: 1, best: 1, q: { "u:bar": { t: 2, ok: 1 }, "e:req1": { t: 3, ok: 1 } }, b: { bar: { t: 1 } }, beats: { bar: { 0: 1, 4: 1, 5: 1 } } }),
  "skyways.learn": JSON.stringify({ done: { bar: 1 } }),
  "skyways.process": JSON.stringify({ qa: { 0: 1 } }),
  "skyways.product": "Northgate", "skyways.lens": "pm", "skyways.seen": JSON.stringify(["learn", "episode", "process", "toolkit"]),
  "skyways.heromode": "light", "skyways.tours.off": "1",
};

// ---- helpers run inside the page ---------------------------------------------------------------------
const CONTRAST = `(() => {
  const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', { willReadFrequently: true });
  const rgba = (c) => { cx.clearRect(0,0,1,1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0,0,1,1); const d = cx.getImageData(0,0,1,1).data; return [d[0],d[1],d[2],d[3]/255]; };
  const over = (top, under) => { const a = top[3]; return [0,1,2].map(i => top[i]*a + under[i]*(1-a)).concat(1); };
  const lum = ([r,g,b]) => { const f = v => { v/=255; return v<=.03928 ? v/12.92 : Math.pow((v+.055)/1.055,2.4); }; return .2126*f(r)+.7152*f(g)+.0722*f(b); };
  const cr = (a,b) => { const x=lum(a), y=lum(b); return (Math.max(x,y)+.05)/(Math.min(x,y)+.05); };
  const page = (() => { const h = rgba(getComputedStyle(document.documentElement).backgroundColor), b = rgba(getComputedStyle(document.body).backgroundColor); return over(b, over(h, [255,255,255,1])); })();
  const memo = new Map();
  const bgOf = (e) => { if (!e) return page; if (memo.has(e)) return memo.get(e); const cs = getComputedStyle(e); let v;
    if (cs.backgroundImage !== 'none' && !/^url/.test(cs.backgroundImage)) v = null;
    else { const c = rgba(cs.backgroundColor); if (c[3] >= .995) v = c; else { const u = bgOf(e.parentElement); v = u ? (c[3] > 0 ? over(c, u) : u) : null; } }
    memo.set(e, v); return v; };
  const vis = (e) => { const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) return false; for (let a = e; a; a = a.parentElement) { const cs = getComputedStyle(a); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) return false; if (a.tagName === 'DETAILS' && !a.open && !(a.querySelector(':scope > summary') || { contains: () => false }).contains(e)) return false; } return true; };
  const low = {}; let seen = 0, skipped = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n; while ((n = walker.nextNode())) { if (!n.textContent.trim()) continue; const e = n.parentElement;
    if (!e || e.closest('svg,script,style,noscript,[aria-hidden="true"],.sw-drawer,.xmodal:not(.on),.xsheet:not(.on),.xdrop') || e.closest(':disabled')) continue;
    if (!vis(e)) continue; const cs = getComputedStyle(e); const bg = bgOf(e); if (!bg) { skipped += 1; continue; } seen += 1;
    let op = 1; for (let a = e; a; a = a.parentElement) op *= +getComputedStyle(a).opacity;
    const c = rgba(cs.color); const fg = over([c[0], c[1], c[2], c[3] * op], bg); const ratio = cr(fg, bg);
    const fs = parseFloat(cs.fontSize); const large = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700);
    if (ratio < (large ? 3 : 4.5) - 0.03) { const k = (e.closest('[class]')?.className || e.tagName).toString().trim().split(/\\s+/).slice(0,3).join('.') + ' ' + ratio.toFixed(2) + ' "' + n.textContent.trim().slice(0, 24) + '"'; low[k] = (low[k] || 0) + 1; } }
  return { seen, skipped, low: Object.entries(low).sort((a, b) => b[1] - a[1]).slice(0, ${process.env.MORE ? 80 : 6}).map(([k, v]) => k + ' x' + v) };
})()`;
const settle = async (ms = 700) => { await evaluate(`document.fonts.ready.then(() => true)`); await sleep(ms); };
const go = async (hash, ms = 900) => { await evaluate(`location.hash = ${JSON.stringify(hash)}; true`); await sleep(ms); };
const fresh = async (url, ms = 1600) => { await send("Page.navigate", { url: "about:blank" }); await sleep(60); await send("Page.navigate", { url }); await sleep(ms); await settle(200); };
let bootScript = null;
const boot = async (source) => {          // what runs before the page's own script on every new document
  if (bootScript) await send("Page.removeScriptToEvaluateOnNewDocument", { identifier: bootScript });
  bootScript = source ? (await send("Page.addScriptToEvaluateOnNewDocument", { source })).identifier : null;
};
const viewport = (w, h) => send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 600 });
const hex = (c) => { const m = String(c).match(/\d+/g) || []; return "#" + m.slice(0, 3).map((v) => (+v).toString(16).padStart(2, "0")).join("").toUpperCase(); };
const QUIET = `try{localStorage.setItem("skyways.tours.off","1")}catch(e){}`;
const themeBoot = (theme) => QUIET + (theme === "light" ? `;try{localStorage.setItem("manual-theme","light")}catch(e){}` : `;try{localStorage.removeItem("manual-theme")}catch(e){}`);

try {
  await send("Page.enable"); await send("Runtime.enable"); await send("Log.enable"); await send("Network.enable");
  // the reader's system says light throughout, so a dark page here is the page's own default and not the system's
  await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: "light" }, { name: "prefers-reduced-motion", value: "no-preference" }] });

  // ---- 1. every route, both widths, both themes -------------------------------------------------------
  if (want("routes")) for (const [w, h] of [[1440, 900], [390, 844]]) for (const theme of ["dark", "light"]) {
    if ((SIZES.length && !SIZES.includes(String(w))) || (THEMES.length && !THEMES.includes(theme))) continue;
    console.log(`routes at ${w}x${h}, ${theme}`);
    await viewport(w, h); await boot(themeBoot(theme)); await fresh(BASE + "#/start");
    const text = {};
    for (const [name, hash] of ROUTES) {
      if (SOME_ROUTES.length && !SOME_ROUTES.includes(name)) continue;
      thrown = []; await go(hash, 1000); await settle(150);
      const tag = `${name} ${w} ${theme}`;
      const m = await evaluate(`(() => { const pg = document.querySelector(".page.on"); const h1 = pg && [...pg.querySelectorAll("h1")].find((x) => x.getBoundingClientRect().width > 0);
        return { h1: h1 ? Math.round(h1.getBoundingClientRect().top + scrollY) : null, h1n: pg ? [...pg.querySelectorAll("h1")].filter((x) => x.getBoundingClientRect().width > 0).length : 0,
          sw: document.documentElement.scrollWidth, iw: innerWidth, title: document.title,
          moving: document.getAnimations().filter((a) => a.playState === "running" && (a.effect?.getTiming().iterations === Infinity)).length,
          text: document.body.innerText }; })()`);
      check(!thrown.length, `${tag}: no script error`, thrown.join(" | "));
      check(m.h1 !== null && m.h1 < h, `${tag}: a title inside the first screen`, `h1 at ${m.h1}`);
      check(m.sw <= m.iw, `${tag}: no sideways scroll`, `${m.sw - m.iw}px`);
      check(m.moving === 0, `${tag}: nothing loops on its own`, `${m.moving} looping animations`);
      const c = await evaluate(CONTRAST);
      check(c.low.length === 0, `${tag}: text contrast 4.5:1`, c.low.join(" | "));
      text[name] = m.text + " " + m.title;
    }
    if (w === 1440 && theme === "dark") for (const [name] of ROUTES) {
      if (!(name in text)) continue;
      const hit = GONE.filter((g) => text[name].includes(g));
      check(!hit.length, `${name}: no old name, rank, mascot line or dash`, hit.join(", "));
    }
    const leftovers = await evaluate(`document.querySelectorAll(".om, .sky, .xpts, .xplore, .g-float, .g-burst, .hero2 .mode, .hero2 .orb").length`);
    check(leftovers === 0, `${w} ${theme}: no mascot, rank, points pill or exploration card in the page`, leftovers);
  }

  // ---- 2. dark by default, light on the toggle, the site's own key --------------------------------------
  if (want("theme")) for (const [w, h] of [[1440, 900], [390, 844]]) {
    console.log(`theme at ${w}x${h}`);
    await viewport(w, h); await boot(QUIET + `;try{if(!sessionStorage.getItem("t")){localStorage.removeItem("manual-theme");sessionStorage.setItem("t","1")}}catch(e){}`);
    await fresh(BASE + "#/toolkit");
    const page = `(() => { const cv = document.createElement("canvas"); cv.width = cv.height = 1; const cx = cv.getContext("2d");
      const px = (c) => { cx.clearRect(0,0,1,1); cx.fillStyle = c; cx.fillRect(0,0,1,1); return [...cx.getImageData(0,0,1,1).data]; };
      const b = px(getComputedStyle(document.body).backgroundColor), r = px(getComputedStyle(document.documentElement).backgroundColor);
      const c = b[3] > 250 ? b : r; return "rgb(" + c.slice(0,3).join(",") + ")"; })()`;
    check(hex(await evaluate(page)) === "#121316", `${w}: with no stored choice the page is dark (#121316)`, hex(await evaluate(page)));
    const tgl = `[...document.querySelectorAll("[data-theme-toggle]")].find((b) => b.getBoundingClientRect().width > 0)`;
    check(await evaluate(`!!${tgl}`), `${w}: the theme toggle is in reach`);
    await evaluate(`(${tgl} || { click() {} }).click(); true`); await sleep(500);
    const s = await evaluate(`({ attr: document.documentElement.getAttribute("data-theme"), key: localStorage.getItem("manual-theme") })`);
    check(s.attr === "light" && s.key === "light", `${w}: the toggle sets data-theme and manual-theme to light`, JSON.stringify(s));
    check(hex(await evaluate(page)) === "#F7F6F2", `${w}: light is the site's paper (#F7F6F2)`, hex(await evaluate(page)));
    await send("Page.reload"); await sleep(1500);
    check(hex(await evaluate(page)) === "#F7F6F2", `${w}: the choice survives a reload`, hex(await evaluate(page)));
    await evaluate(`(${tgl} || { click() {} }).click(); true`); await sleep(400);
    const d = await evaluate(`({ attr: document.documentElement.getAttribute("data-theme"), key: localStorage.getItem("manual-theme") })`);
    check(d.attr === "dark" && d.key === "dark" && hex(await evaluate(page)) === "#121316", `${w}: and back to dark`, JSON.stringify(d));
  }

  // ---- 3. the top bar ------------------------------------------------------------------------------------
  if (want("bar")) for (const [w, h] of [[1440, 900], [390, 844]]) {
    console.log(`top bar at ${w}x${h}`);
    await viewport(w, h); await boot(themeBoot("dark")); await fresh(BASE + "#/toolkit");
    const b = await evaluate(`(() => { const nav = document.getElementById("topnav"); const shown = (e) => !!e && e.getBoundingClientRect().width > 0;
      const href = (sel) => [...document.querySelectorAll(sel)].map((a) => a.getAttribute("href"));
      return { pills: [...nav.querySelectorAll("a.xplay")].filter(shown).map((a) => a.getAttribute("href")), quiet: [...nav.querySelectorAll("a.xquiet")].filter(shown).map((a) => a.getAttribute("href")),
        learn: href('#topnav .xmenu a, #xsheet a'), brand: (nav.querySelector(".xbrand") || { innerText: "" }).innerText.replace(/\\s+/g, " ").trim(),
        strip: document.querySelectorAll(".sw-strip").length, bars: Math.round(nav.getBoundingClientRect().bottom), title: document.title,
        sheet: href("#xsheet a") }; })()`);
    check(b.pills.length === 1 && b.pills[0] === "../simulator/", `${w}: one filled pill, to the game`, JSON.stringify(b.pills));
    if (w >= 1000) check(b.quiet.length === 1 && b.quiet[0] === "../", `${w}: one quiet link, to the manual`, JSON.stringify(b.quiet));
    else check(b.sheet.includes("../") && b.sheet.includes("../learn/"), `${w}: the phone menu leads with the manual and the tutorial`, JSON.stringify(b.sheet.slice(0, 4)));
    check(b.learn.includes("../learn/"), `${w}: the tutorial is in the Learn list`);
    // on a wide screen the brand reads "SkyWays", then "Workbench"; on a phone there is room for the mark and one word, and it is Workbench
    check((w < 1000 || /SkyWays/.test(b.brand)) && /Workbench/.test(b.brand) && !/Simulator|Consultancy/.test(b.brand), `${w}: the brand names the workbench`, b.brand);
    check(b.strip === 0, `${w}: one bar, no strip above it`);
    check(/workbench/i.test(b.title) && !/Simulator/.test(b.title), `${w}: the tab title names the workbench`, b.title);
    if (w >= 1440) {      // the two floating buttons must not sit on the rail or the words
      await evaluate(`scrollTo(0, 2400); true`); await sleep(500);
      const cover = await evaluate(`(() => { const out = []; document.querySelectorAll(".sw-pill, .sw-top").forEach((b) => { const r = b.getBoundingClientRect(); if (r.width < 1 || getComputedStyle(b).opacity === "0" || getComputedStyle(b).display === "none") return;
        const rail = document.querySelector(".page.on .rail2, .page.on .rail"), main = document.querySelector(".page.on main");
        [rail, main].forEach((box) => { if (!box) return; const q = box.getBoundingClientRect(); const pad = box === main ? parseFloat(getComputedStyle(box).paddingRight) : 0;
          if (r.left < q.right - pad && r.right > q.left && r.top < q.bottom && r.bottom > q.top) out.push(b.className + " over " + box.className); }); }); return out; })()`);
      check(cover.length === 0, `${w}: no floating button sits on the rail or the words`, cover.join(" | "));
    }
  }

  // ---- 4. links into a part of a page, loaded cold -------------------------------------------------------
  if (want("links")) for (const [w, h] of [[1440, 900], [390, 844]]) {
    console.log(`deep links at ${w}x${h}`);
    await viewport(w, h); await boot(themeBoot("dark"));
    for (const [hash, id] of PART_LINKS) {
      thrown = []; await fresh(BASE + hash, 2300);
      const top = await evaluate(`(() => { const e = document.getElementById(${JSON.stringify(id)}); return e ? Math.round(e.getBoundingClientRect().top) : null; })()`);
      check(top !== null && top >= 60 && top <= 140 && !thrown.length, `${hash} ${w}: lands on its target`, `top ${top} ${thrown.join(" | ")}`);
    }
    await fresh(BASE + "#/start");
    const dead = await evaluate(`${JSON.stringify(PAGE_LINKS.concat(PART_LINKS.map((l) => l[0])))}.filter((l) => !routeOK(l))`);
    check(dead.length === 0, `${w}: all ${PAGE_LINKS.length + PART_LINKS.length} links from the manual and the game resolve`, dead.join(", "));
  }

  // ---- 5. calculators, the pack, a walk, saved state -------------------------------------------------------
  if (want("tools")) {
    console.log("calculators, evidence pack, a decision walk, saved state");
    await viewport(1440, 900); await boot(QUIET + `;try{if(!sessionStorage.getItem("t")){Object.keys(localStorage).filter((k)=>k.indexOf("skyways.")===0&&k!=="skyways.tours.off").forEach((k)=>localStorage.removeItem(k));sessionStorage.setItem("t","1")}}catch(e){}`);
    thrown = []; await fresh(BASE + "#/toolkit");
    const calc = await evaluate(`TOOLS.map((t) => { const box = document.querySelector('[data-tool="' + t.id + '"]'), res = document.getElementById("tres-" + t.id), art = document.getElementById("tart-" + t.id);
      const before = res.textContent + "|" + art.value; let changed = false;
      for (const f of box.querySelectorAll("input,select,textarea")) { if (f.tagName === "SELECT") f.selectedIndex = (f.selectedIndex + 1) % f.options.length; else if (f.type === "number" || f.type === "range") f.value = String((+f.value || 1) * 2 + 1); else if (f.type === "checkbox" || f.type === "radio") f.click(); else f.value = f.value + " x";
        f.dispatchEvent(new Event("input", { bubbles: true })); f.dispatchEvent(new Event("change", { bubbles: true })); if (res.textContent + "|" + art.value !== before) { changed = true; break; } }
      return [t.id, changed && !/Check the values/.test(res.textContent) && art.value.length > 40]; })`);
    check(calc.length === 17, "seventeen calculators", calc.length);
    for (const [id, ok] of calc) check(ok, `calculator ${id}: an input changes the result`);
    await evaluate(`document.querySelector('[data-add="bar"]').click(); true`); await sleep(200);
    const n1 = await evaluate(`({ n: document.querySelector("[data-minen]").textContent.trim(), ls: JSON.parse(localStorage.getItem("skyways.pack") || "[]").length })`);
    check(n1.n === "1" && n1.ls === 1, "Add to the evidence pack: the count is 1", JSON.stringify(n1));
    await send("Page.reload"); await sleep(1600);
    const n2 = await evaluate(`document.querySelector("[data-minen]").textContent.trim()`);
    check(n2 === "1", "after a reload the count is still 1", n2);
    await go("#/simulations/nfr", 1300);
    const walk = await evaluate(`(async () => { const vis = (e) => e.offsetParent !== null; const main = document.getElementById("simulationsMain"); let last = "";
      for (let i = 0; i < 12; i++) { const sim = main.querySelector("#sim-nfr") || main; const o = [...sim.querySelectorAll(".xopt")].filter(vis); if (o.length) { o[0].click(); await new Promise((r) => setTimeout(r, 200)); }
        const next = [...sim.querySelectorAll(".xbtn.dark")].filter(vis)[0]; if (!next) break; last = next.textContent.trim(); if (/Added/.test(last)) break; next.click(); await new Promise((r) => setTimeout(r, 250)); last = ([...sim.querySelectorAll(".xbtn.dark")].filter(vis)[0] || { textContent: last }).textContent.trim(); if (/Added/.test(last)) break; }
      return { last, pack: JSON.parse(localStorage.getItem("skyways.pack") || "[]").map((m) => m.title) }; })()`);
    check(/Added to the evidence pack/.test(walk.last) && walk.pack.some((t) => /NFR workshop/.test(t)), "the NFR walk ends on \"Added to the evidence pack\"", JSON.stringify(walk));
    check(!thrown.length, "no script error while using the tools", thrown.join(" | "));

    await boot(`try{if(!sessionStorage.getItem("s")){const S=${JSON.stringify(SAVED)};Object.keys(S).forEach((k)=>localStorage.setItem(k,S[k]));sessionStorage.setItem("s","1")}}catch(e){}`);
    thrown = []; await fresh(BASE + "#/quest", 1800);
    const q = await evaluate(`({ pack: document.querySelector("[data-minen]").textContent.trim(), hud: (document.querySelector(".xq-hud") || { innerText: "" }).innerText.replace(/\\s+/g, " "), railOff: document.body.classList.contains("rail-off") })`);
    check(q.pack === "2", "saved state: the pack shows its two documents", q.pack);
    check(/4 ?of 13/.test(q.hud), "saved state: four of thirteen days answered", q.hud.slice(0, 160));
    await go("#/process/qa", 1300);
    const pr = await evaluate(`(() => { const m = document.getElementById("processMain"); return { product: [...m.querySelectorAll("input")].some((i) => i.value === "Northgate"), ticked: m.querySelectorAll("input[type=checkbox]:checked").length, keys: Object.keys(localStorage).filter((k) => k.indexOf("skyways.") === 0).length }; })()`);
    check(pr.product && pr.ticked === 1, "saved state: the product name and the ticked step come back", JSON.stringify(pr));
    await go("#/learn", 1200);
    const ln = await evaluate(`JSON.parse(localStorage.getItem("skyways.learn") || "{}").done && JSON.parse(localStorage.getItem("skyways.game") || "{}").q && JSON.parse(localStorage.getItem("skyways.game")).q["e:req1"].ok === 1`);
    check(ln === true && !thrown.length, "saved state: the finished unit and the answered check are kept", thrown.join(" | "));
    await evaluate(`document.querySelector("[data-opensearch]").click(); true`); await sleep(300);
    const found = await evaluate(`(() => { const i = document.querySelector("#xsm input"); if (!i) return -1; i.value = "acceptance bar"; i.dispatchEvent(new Event("input", { bubbles: true })); return document.querySelector("#xsm").innerText.includes("Acceptance bar calculator") ? 1 : 0; })()`);
    check(found === 1, "search finds the acceptance bar calculator", found);
  }

  // ---- 7. the ten pictures ----------------------------------------------------------------------------------
  const webpSize = (file) => {
    const b = readFileSync(file); const kind = b.toString("latin1", 12, 16);
    if (kind === "VP8X") return [1 + b.readUIntLE(24, 3), 1 + b.readUIntLE(27, 3)];
    if (kind === "VP8 ") return [b.readUInt16LE(26) & 0x3fff, b.readUInt16LE(28) & 0x3fff];
    if (kind === "VP8L") { const v = b.readUInt32LE(21); return [1 + (v & 0x3fff), 1 + ((v >> 14) & 0x3fff)]; }
    return [0, 0];
  };
  if (want("pictures")) {
    console.log("the ten pictures");
    // simshots.mjs shoots in a fresh profile, so the pictures show what a new reader sees. The sections before
    // this one leave progress in the browser (answered stops shorten the flight plan's P0 column), so it is
    // cleared here before the page is measured.
    await viewport(1440, 900); await boot(`try{localStorage.clear()}catch(e){};` + themeBoot("light") + `;try{localStorage.setItem("skyways.rail","on")}catch(e){}`);
    await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: "light" }, { name: "prefers-reduced-motion", value: "reduce" }] });
    await fresh(BASE + "#/start", 2500);
    for (const [name, hash, sel] of SHOTS) {
      await go(hash, 1500);
      const box = await evaluate(`(() => { const el = document.querySelector(".page.on " + ${JSON.stringify(sel)}) || document.querySelector(${JSON.stringify(sel)}); if (!el) return null; const b = el.getBoundingClientRect(); return { w: b.width, h: b.height }; })()`);
      const file = join(PICTURES, name + ".webp");
      if (!box || !box.w) { check(false, `${name}: its selector ${sel} is on ${hash}`); continue; }
      if (!existsSync(file)) { check(false, `${name}: the picture file exists`); continue; }
      const [pw, ph] = webpSize(file); const ew = 2 * Math.min(1440, box.w + 20), eh = 2 * (box.h + 20);
      check(Math.abs(pw - ew) <= 6 && Math.abs(ph - eh) <= 6, `${name}: the page still draws it at the picture's size`, `picture ${pw}x${ph}, page would give ${Math.round(ew)}x${Math.round(eh)}`);
    }
    await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: "light" }, { name: "prefers-reduced-motion", value: "no-preference" }] });
  }

  // ---- 8. the file alone, from disk, with no network ------------------------------------------------------
  if (want("alone")) {
    console.log("opened alone from disk");
    await viewport(1440, 900); await boot(QUIET);
    await send("Network.emulateNetworkConditions", { offline: true, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
    thrown = []; failedRequests = [];
    await fresh(pathToFileURL(SOURCE).href + "#/toolkit", 2200);
    const a = await evaluate(`(() => { const h = document.querySelector(".page.on .xh1"); const shown = (e) => e.getBoundingClientRect().width > 0;
      return { family: h ? getComputedStyle(h).fontFamily.split(",")[0].replace(/"/g, "").trim() : "", has: document.fonts.check('600 32px "Instrument Sans"') && [...document.fonts].some((f) => /Instrument Sans/.test(f.family) && f.status === "loaded"),
        body: getComputedStyle(document.body).fontFamily.split(",")[0].replace(/"/g, "").trim(), tools: typeof TOOLS !== "undefined" ? TOOLS.length : 0, res: (document.getElementById("tres-bar") || { textContent: "" }).textContent.length,
        out: [...document.querySelectorAll('#topnav a[href^="../"], .xsheet a[href^="../"]')].filter(shown).length, remote: [...document.querySelectorAll("link[href^=http], script[src^=http], img[src^=http]")].length }; })()`);
    check(a.family === "Instrument Sans" && a.has, "from file://, offline: the title is set in Instrument Sans", JSON.stringify(a));
    check(a.body === "Geist", "from file://, offline: the text is Geist", a.body);
    check(a.tools === 17 && a.res > 20, "from file://, offline: the calculators run", JSON.stringify(a));
    check(a.out === 0, "from file://: no link points out of the file to a site that is not there", a.out);
    check(a.remote === 0 && failedRequests.length === 0 && !thrown.length, "from file://: nothing is fetched and nothing fails", failedRequests.concat(thrown).join(" | "));
    await send("Network.emulateNetworkConditions", { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
  }
} catch (e) {
  check(false, "the test itself ran to the end", e.message);
} finally {
  ws.close(); const exited = new Promise((r) => chrome.once("exit", r)); chrome.kill(); await Promise.race([exited, sleep(5000)]);
  try { rmSync(profile, { recursive: true, force: true }); } catch { /* ignore */ }
}
const total = passed + failures.length;
console.log(failures.length ? `workbench: ${failures.length} of ${total} checks failed` : `workbench: all ${total} checks passed`);
process.exit(failures.length ? 1 : 0);
