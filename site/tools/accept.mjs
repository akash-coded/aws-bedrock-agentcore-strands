// The acceptance gate for the site's pages: what must hold before a change to layout or motion ships.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/accept.mjs http://localhost:8799/
//
// Five passes over one page of each kind, in headless Chrome over the DevTools protocol (the same
// approach as shoot.mjs, so there is nothing to install):
//
//   1. no script            nothing a reader needs is left hidden (opacity 0, scaled to nothing, undrawn)
//   2. reduced motion       nothing hidden, and no animation running at all
//   3. motion allowed       four seconds after load, the only things still moving follow the scroll, or
//                           sit on a page that carries a pause control (the hero's flight, the tower)
//   4. scrolled through     with motion allowed and the whole page scrolled past, nothing is left hidden
//   5. a phone, 375 x 812   no sideways scroll, and the page's title ends inside the first screen
//
// Every pass first checks that the page really loaded: its top bar is there and styled. It exits 1 if
// any pass fails and prints what failed. It measures; it does not judge taste.
//
// What it cannot see: the globe is drawn on a canvas by script, so it is not among the browser's
// animations; the pause control stopping it is checked by hand. The simulator's canvas reports its own
// frames, so that one is checked: none under reduced motion, and a pause control when it moves.

import { spawn } from "node:child_process";
import { rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const BASE = process.argv[2];
if (!BASE) { console.error("usage: node accept.mjs <site url, ending in />"); process.exit(2); }
const PAGES = ["", "method/", "product-manager/", "qa/", "protocol/", "models/", "templates/", "prompts/",
  "frameworks/", "pictures/", "learn/", "learn/fundamentals/", "learn/the-hard-gate/", "simulator/"];
// The simulator draws on a canvas from script, which the browser's list of animations cannot see. Its
// loop counts its own frames in window.NDFrames, so the gate can ask.
const FRAMES = `(typeof window.NDFrames === "number" ? window.NDFrames : -1)`;
// animations allowed to keep running, provided the page that runs them carries a pause control
const PAUSABLE = /^(sc-fly|twr-)/;
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
  const sel = '.rv,.spine .sp-trunk i,.spine .sp-loop,.spine .sp-ph li,.spine .sp-back,.spine .sp-gate,.cover .bar,.sc-wp li,.scene .leg,.scene .stop,.roadmap .rn,.hero2 .hx>*,main .sec,.dgb,' +
    '.step>summary,.mix a,.lc,.lk,.seats a,.tile,[data-reveal]>*,figure.fig>svg>*,.mmg svg>*';
  const bad = {};
  document.querySelectorAll(sel).forEach((e) => {
    const cs = getComputedStyle(e);
    let why = '';
    if (+cs.opacity < 0.05) why = 'opacity ' + cs.opacity;
    else if (cs.scale && /^0(\\s|$)/.test(cs.scale)) why = 'scaled to nothing';
    else if (e.matches('.scene .leg') && parseFloat(cs.strokeDashoffset) > 0.01) why = 'not drawn';
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

async function pass(label, { width, height, reduce = false, noscript = false, wait = 4200 }, check) {
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: width < 600 });
  await send("Emulation.setEmulatedMedia", { features: [
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
console.log(failures ? `\n${failures} failure(s)` : "\nall five passes hold");
process.exit(failures ? 1 : 0);
