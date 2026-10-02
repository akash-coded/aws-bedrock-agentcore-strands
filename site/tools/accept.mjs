// The acceptance gate for the site's pages: what must hold before a change to layout or motion ships.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/accept.mjs http://localhost:8799/
//
// Nine passes over one page of each kind, in headless Chrome over the DevTools protocol (the same
// approach as shoot.mjs, so there is nothing to install):
//
//   1. no script            nothing a reader needs is left hidden (opacity 0, scaled to nothing, undrawn)
//   2. reduced motion       nothing hidden, and no animation running at all
//   3. motion allowed       four seconds after load, the only things still moving follow the scroll, or
//                           sit on a page that carries a pause control (the hero's flight, the tower)
//   4. scrolled through     with motion allowed and the whole page scrolled past, nothing is left hidden
//   5. a phone, 375 x 812   no sideways scroll, and the page's title ends inside the first screen
//   6. a small phone, 320   no sideways scroll
//   7. print                nothing a reader needs is left hidden on paper
//   8. the top bar          its pill never points at the page it is on; the simulator and a lesson each offer the other
//   9. the hero             one clock (the pause holds the flight, the aircraft's shape and the sign-off together); the
//                           four-drawings path, for a browser that cannot ease a shape, shows one aircraft at a time;
//                           the globe's drawing stays inside its budget with the processor slowed four times; and the
//                           page does not shift as it is scrolled
//
// Every pass first checks that the page really loaded: its top bar is there and styled. It exits 1 if
// any pass fails and prints what failed. It measures; it does not judge taste.
//
// What it cannot see: other browsers. Safari has no CSS `d`, so it takes the four-drawings path for the
// aircraft, which pass 9 forces here; a browser without cross-document view transitions does not morph the
// top bar's pill, and the page simply changes. Both are the plain path by design, and neither is run here.
// The globe and the simulator draw on canvases from script, which the browser's list of animations cannot
// see, so each reports for itself: window.GlobeMs (drawing time) and window.NDFrames (frames drawn).

import { spawn } from "node:child_process";
import { rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const BASE = process.argv[2];
if (!BASE) { console.error("usage: node accept.mjs <site url, ending in />"); process.exit(2); }
const PAGES = ["", "method/", "product-manager/", "qa/", "protocol/", "models/", "templates/", "prompts/",
  "frameworks/", "pictures/", "learn/", "learn/fundamentals/", "learn/the-hard-gate/", "learn/p0-frame/", "simulator/"];
// The simulator draws on a canvas from script, which the browser's list of animations cannot see. Its
// loop counts its own frames in window.NDFrames, so the gate can ask.
const FRAMES = `(typeof window.NDFrames === "number" ? window.NDFrames : -1)`;
// animations allowed to keep running, provided the page that runs them carries a pause control
const PAUSABLE = /^(sc-(fly|shape|flame|gate|turn\d)|sim-roll|twr-)/;
const LOADED = `(() => { const h = document.querySelector('.hd'); return !!h && getComputedStyle(h).position === 'sticky' && !!document.querySelector('main h1, .hero2 h1'); })()`;
const HAS_PAUSE = `!!document.querySelector('[data-motion-toggle]')`;
const SCROLL_THROUGH = `(async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 500) { scrollTo({ top: y, behavior: 'instant' }); await new Promise((r) => requestAnimationFrame(() => setTimeout(r, 90))); } await new Promise((r) => setTimeout(r, 900)); return true; })()`;

const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `accept-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function target() {
  for (let i = 0; i < 60; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find((t) => t.type === "page");
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(250);
  }
  throw new Error("Chrome did not start");
}
const ws = new WebSocket(await target());
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0;
const waiting = new Map();
const thrown = [];
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.method === "Runtime.exceptionThrown") {
    thrown.push((m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 160));
  }
  if (m.id && waiting.has(m.id)) {
    const { ok, no } = waiting.get(m.id);
    waiting.delete(m.id);
    m.error ? no(new Error(m.error.message)) : ok(m.result);
  }
});
const send = (method, params = {}) => new Promise((ok, no) => {
  const id = ++seq;
  waiting.set(id, { ok, no });
  ws.send(JSON.stringify({ id, method, params }));
});
const evaluate = async (expression) => {
  const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails).slice(0, 300));
  return r.result.value;
};

// Things that script or an animation may hide, and must have shown by now.
const HIDDEN = `(() => {
  const sel = '.rv,.spine .sp-trunk i,.spine .sp-loop,.spine .sp-ph li,.spine .sp-back,.spine .sp-gate,.spine .sp-in li,.spine .sp-fun path,.spine .sp-core a,.spine .sp-craft,.spine .sp-note,.cover .bar,.sc-wp li,.scene .leg,.scene .stop,.scene .back,.scene .next,.roadmap .rn,.hero2 .hx>*,main .sec,.dgb,' +
    '.step>summary,.mix a,.lc,.lk,.seats a,.tile,[data-reveal]>*,figure.fig>svg>*,.mmg svg>*,figure.sketch [data-an]';
  const bad = {};
  document.querySelectorAll(sel).forEach((e) => {
    const cs = getComputedStyle(e);
    let why = '';
    if (+cs.opacity < 0.05) why = 'opacity ' + cs.opacity;
    else if (cs.scale && /^0(\\s|$)/.test(cs.scale)) why = 'scaled to nothing';
    else if (e.matches('.scene .leg,.spine .sp-fun path') && parseFloat(cs.strokeDashoffset) > 0.01) why = 'not drawn';
    else if (/inset\\([^)]*100%/.test(cs.clipPath)) why = 'clipped away';
    if (why) {
      const cls = (e.className.baseVal ?? e.className ?? '').toString().split(' ')[0];
      const k = (cls || (e.parentElement?.className || '').toString().split(' ').pop() + ' ' + e.tagName.toLowerCase()) + ' (' + why + ')';
      bad[k] = (bad[k] || 0) + 1;
    }
  });
  return bad;
})()`;
const RUNNING = `(() => {
  const o = {};
  document.getAnimations().forEach((a) => {
    if (a.playState !== 'running') return;
    const scroll = a.timeline && a.timeline.constructor.name !== 'DocumentTimeline';
    const name = a.animationName || 'transition';
    o[name + (scroll ? ' [follows the scroll]' : '')] = (o[name + (scroll ? ' [follows the scroll]' : '')] || 0) + 1;
  });
  return o;
})()`;
const PHONE = `(() => {
  const h = document.querySelector('main h1, .hero2 h1');
  return { h1: h ? Math.round(h.getBoundingClientRect().bottom) : -1,
           over: document.documentElement.scrollWidth - document.documentElement.clientWidth };
})()`;

let failures = 0;
try {
await send("Page.enable");
await send("Runtime.enable");
const list = (o) => Object.entries(o).map(([k, v]) => `${k} x${v}`).join(", ");

async function pass(label, { width, height, reduce = false, noscript = false, wait = 4200, print = false }, check) {
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: width < 600 });
  await send("Emulation.setEmulatedMedia", { media: print ? "print" : "", features: [
    { name: "prefers-color-scheme", value: "dark" },
    { name: "prefers-reduced-motion", value: reduce ? "reduce" : "no-preference" }] });
  console.log(`\n${label}`);
  for (const p of PAGES) {
    thrown.length = 0;
    await send("Emulation.setScriptExecutionDisabled", { value: noscript });
    await send("Page.navigate", { url: BASE + p });
    await sleep(wait);
    await send("Emulation.setScriptExecutionDisabled", { value: false });   // the check itself needs script
    const problems = (await evaluate(LOADED)) ? await check() : ["the page did not load (no styled top bar, or no title)"];
    if (thrown.length) problems.push("script error: " + thrown[0]);
    if (problems.length) { failures += problems.length; console.log(`  FAIL /${p}  ${problems.join("; ")}`); }
    else console.log(`  ok   /${p}`);
  }
}

await pass("1. no script: nothing left hidden", { width: 1280, height: 800, noscript: true, wait: 3200 }, async () => {
  const h = await evaluate(HIDDEN);
  return Object.keys(h).length ? ["hidden: " + list(h)] : [];
});
await pass("2. reduced motion: nothing hidden, nothing running", { width: 1280, height: 800, reduce: true }, async () => {
  const out = [];
  const h = await evaluate(HIDDEN);
  const r = await evaluate(RUNNING);
  if (Object.keys(h).length) out.push("hidden: " + list(h));
  if (Object.keys(r).length) out.push("running: " + list(r));
  const f = await evaluate(FRAMES);
  if (f > 0) out.push(`the canvas drew ${f} frames`);
  return out;
});
await pass("3. motion allowed: after four seconds only pausable or scroll-led motion remains", { width: 1280, height: 800 }, async () => {
  const out = [];
  // bands below the fold wait for the scroll, and so do the figures inside them
  const below = HIDDEN.replace(/'\.rv,[^']*?,\.sc-wp li,/, "'.sc-wp li,");
  if (below === HIDDEN) throw new Error("the selector for bands below the fold no longer matches");
  const h = await evaluate(below);
  const r = await evaluate(RUNNING);
  const stray = Object.fromEntries(Object.entries(r).filter(([k]) => !PAUSABLE.test(k) && !k.includes("follows the scroll")));
  const pausable = Object.keys(r).some((k) => PAUSABLE.test(k));
  if (Object.keys(h).length) out.push("hidden: " + list(h));
  if (Object.keys(stray).length) out.push("still running: " + list(stray));
  if (pausable && !(await evaluate(HAS_PAUSE))) out.push("something keeps moving and the page has no pause control");
  if ((await evaluate(FRAMES)) > 0 && !(await evaluate(HAS_PAUSE))) out.push("the canvas keeps moving and the page has no pause control");
  return out;
});
await pass("4. scrolled through, motion allowed: nothing left hidden", { width: 1280, height: 800, wait: 1800 }, async () => {
  await evaluate(SCROLL_THROUGH);
  const h = await evaluate(HIDDEN);
  return Object.keys(h).length ? ["hidden: " + list(h)] : [];
});
await pass("5. a phone, 375 x 812: no sideways scroll, the title inside the first screen", { width: 375, height: 812, reduce: true }, async () => {
  const out = [];
  const m = await evaluate(PHONE);
  if (m.over > 0) out.push(`scrolls sideways by ${m.over}px`);
  if (m.h1 < 0 || m.h1 > 812) out.push(`the title ends at ${m.h1}px`);
  return out;
});
await pass("6. a small phone, 320 x 640: no sideways scroll", { width: 320, height: 640, reduce: true, wait: 1500 }, async () => {
  const m = await evaluate(PHONE);
  return m.over > 0 ? [`scrolls sideways by ${m.over}px`] : [];
});
await pass("7. print: nothing left hidden on paper", { width: 1280, height: 800, wait: 1500, print: true }, async () => {
  // the hero's picture is a screen thing: paper does not carry it
  const paper = HIDDEN.replace(".sc-wp li,.scene .leg,.scene .stop,.scene .back,.scene .next,", "");
  if (paper === HIDDEN) throw new Error("the selector for the hero's picture no longer matches");
  const h = await evaluate(paper);
  return Object.keys(h).length ? ["hidden: " + list(h)] : [];
});
await pass("8. the top bar: the pill never points at the page it is on", { width: 1280, height: 800, reduce: true, wait: 1200 }, async () => {
  const out = [];
  const m = await evaluate(`(() => { const a = document.querySelector('.hd .ctx .play'); if (!a) return null;
    const u = new URL(a.href); return { same: u.pathname === location.pathname, path: u.pathname, here: location.pathname, text: a.textContent.trim() }; })()`);
  if (!m) return ["the top bar has no pill"];
  if (m.same) out.push(`the pill ("${m.text}") points at this page`);
  if (/\/simulator\/$/.test(m.here) && /\/simulator\//.test(m.path)) out.push("inside the simulator the pill still offers the simulator");
  if (/\/learn\//.test(m.here) && !/\/simulator\//.test(m.path)) out.push("inside the tutorial the pill does not offer the simulator");
  return out;
});

// 9. the hero, on the home page only
console.log("\n9. the hero: one clock, the four-drawings path, the globe's budget, no shift");
{
  const out = [];
  thrown.length = 0;
  await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await send("Emulation.setEmulatedMedia", { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "no-preference" }] });
  await send("Page.navigate", { url: BASE });
  await sleep(3200);
  const LOOPS = `document.getAnimations().filter((a) => /^sc-(fly|shape|flame|gate|turn\\d)$/.test(a.animationName || ''))`;
  const states = async () => evaluate(`(() => { const o = {}; ${LOOPS}.forEach((a) => { o[a.animationName + ':' + a.playState] = 1; }); return Object.keys(o); })()`);
  const tick = (on) => evaluate(`(() => { const b = document.querySelector('.hero2 [data-motion-toggle]'); b.checked = ${on}; b.dispatchEvent(new Event('change', { bubbles: true })); return true; })()`);
  await tick(true); await sleep(300);
  let s = await states();
  if (!s.length) out.push("no looping animation found in the hero");
  if (s.some((k) => !k.endsWith(":paused"))) out.push("paused, and still running: " + s.filter((k) => !k.endsWith(":paused")).join(", "));
  await tick(false); await sleep(300);
  s = await states();
  if (s.some((k) => !k.endsWith(":running"))) out.push("resumed, and still held: " + s.filter((k) => !k.endsWith(":running")).join(", "));
  // a browser that cannot ease one path into another: four drawings, one at a time
  const shown = await evaluate(`(async () => { document.documentElement.classList.add('sc-turns'); await new Promise((r) => setTimeout(r, 900));
    const all = [...document.querySelectorAll('.sc-near .sc-plane .sc-still')]; const on = all.filter((e) => +getComputedStyle(e).opacity > 0.5).length;
    const morph = getComputedStyle(document.querySelector('.sc-near .sc-plane .sc-morph')).display;
    document.documentElement.classList.remove('sc-turns'); return { n: all.length, on, morph }; })()`);
  if (shown.n !== 4 || shown.on !== 1 || shown.morph !== "none") out.push(`the four-drawings path shows ${shown.on} of ${shown.n} aircraft (the easing one: ${shown.morph})`);
  // the globe's drawing, with the processor slowed four times
  await send("Emulation.setCPUThrottlingRate", { rate: 4 });
  await evaluate("window.GlobeMs = { n: 0, sum: 0, max: 0 }; true");
  await sleep(3000);
  const g = await evaluate("window.GlobeMs");
  await send("Emulation.setCPUThrottlingRate", { rate: 1 });
  if (!g || g.n < 30) out.push(`the globe drew ${g ? g.n : 0} frames in three seconds`);
  else if (g.sum / g.n > 6) out.push(`the globe takes ${(g.sum / g.n).toFixed(1)}ms a frame at a quarter speed; 6ms is the budget`);
  // nothing moves the page under the reader
  await send("Page.navigate", { url: BASE });
  await sleep(2600);
  const shift = await evaluate(`(async () => { let cls = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
    const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 500) { scrollTo({ top: y, behavior: 'instant' }); await new Promise((r) => setTimeout(r, 120)); }
    await new Promise((r) => setTimeout(r, 600)); return cls; })()`);
  if (shift > 0.05) out.push(`the page shifts by ${shift.toFixed(3)} as it is scrolled; 0.05 is the limit`);
  if (thrown.length) out.push("script error: " + thrown[0]);
  if (out.length) { failures += out.length; console.log("  FAIL /  " + out.join("; ")); } else console.log("  ok   /");
}

} catch (e) {
  failures++;
  console.log("\nthe gate itself failed: " + e.message);
} finally {
  ws.close();
  const exited = new Promise((r) => chrome.once("exit", r));
  chrome.kill();
  await Promise.race([exited, sleep(5000)]);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
console.log(failures ? `\n${failures} failure(s)` : "\nall nine passes hold");
process.exit(failures ? 1 : 0);
