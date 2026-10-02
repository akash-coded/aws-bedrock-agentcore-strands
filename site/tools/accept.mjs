// The acceptance gate for the site's pages: what must hold before a change to layout or motion ships.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/accept.mjs http://localhost:8799/
//
// Thirteen passes over one page of each kind, in headless Chrome over the DevTools protocol (the same
// approach as shoot.mjs, so there is nothing to install):
//
//    1. no script            nothing a reader needs is left hidden (opacity 0, scaled to nothing, undrawn)
//    2. reduced motion       nothing hidden, and no animation running at all
//    3. nothing waits        with motion allowed, 700ms after load nothing on the whole page is hidden: no
//                            entrance, no part that waits to be scrolled to. After four seconds the only things
//                            still moving follow the scroll or sit on a page with a pause control
//    4. scrolled through     the whole page scrolled past: nothing is hidden, and nothing started moving
//                            because it was scrolled to
//    5. a phone, 375 x 812   no sideways scroll, and the page's title ends inside the first screen
//    6. a small phone, 320   no sideways scroll
//    7. the bar fits         at 320, 990, 1024, 1100 and 1180 wide the top bar's last control ends inside the screen
//    8. print                nothing a reader needs is left hidden on paper
//    9. the top bar          its pill never points at the page it is on; the simulator and a lesson each offer the other
//   10. floating buttons     back-to-top, mail and the guide never sit on the words: below 1440 wide none is shown;
//                            at 1440 each sits in the side gutter, clear of the page's column
//   11. versions             every local stylesheet and script is asked for by an address that carries its version,
//                            so a new page can never be paired with an old file from a browser's cache
//   12. no stylesheet        with every stylesheet blocked, no mark in a sketch falls back to a solid black fill
//   13. the hero             one clock (the pause holds it; a tab left and come back to goes on from where it was);
//                            at twelve moments round a lap, at four widths, the line under the picture names the
//                            phase the aircraft is in; the picture ends inside the first screen on a phone and a
//                            laptop; its drawing stays inside its budget with the processor slowed four times; and
//                            the page does not shift as it is scrolled
//
// Every pass first checks that the page really loaded: its top bar is there and styled. It exits 1 if
// any pass fails and prints what failed. It measures; it does not judge taste: for that, look. The hero can
// be put at any second of its clock with window.GlobeAt(seconds), and site/tools/herosheet.mjs lays twelve
// such moments at four widths on one sheet for a person to look at before a release.
//
// What it cannot see: other browsers. Nothing on the site now depends on a feature only Chrome has (the
// hero is one canvas; there are no view transitions and no CSS path animation), but Safari and Firefox are
// not run here. The globe and the simulator draw on canvases from script, which the browser's list of
// animations cannot see, so each reports for itself: window.GlobeMs (drawing time and frames) and
// window.NDFrames (frames drawn).

import { spawn } from "node:child_process";
import { rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const BASE = process.argv[2];
if (!BASE) { console.error("usage: node accept.mjs <site url, ending in />"); process.exit(2); }
const PAGES = ["", "method/", "product-manager/", "qa/", "protocol/", "models/", "templates/", "prompts/",
  "frameworks/", "pictures/", "learn/", "learn/fundamentals/", "learn/the-hard-gate/", "learn/p0-frame/", "simulator/",
  "labs/", "labs/grow-the-spec/"];
// The simulator draws on a canvas from script, which the browser's list of animations cannot see. Its
// loop counts its own frames in window.NDFrames, so the gate can ask.
const FRAMES = `(typeof window.NDFrames === "number" ? window.NDFrames : -1)`;
// animations allowed to keep running, provided the page that runs them carries a pause control
const PAUSABLE = /^(twr-|nd-)/;
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
  const sel = '.hero2 .hx>*,.sc-rail li,.sec-h>*,.spine li,.spine .sp-core a,.spine .sp-trunk i,.spine .sp-loop,.spine .sp-back,.spine .sp-gate,' +
    '.spine .sp-fun path,.spine .sp-craft,.spine .sp-note,.cover .bar,.seats a,.daycard,.daycard *,.tile,.roadmap .rn,main .sec,.dgb,' +
    '.step>summary,.mix a,.lc,.lk,[data-reveal]>*,figure.fig>svg>*,.mmg svg>*,figure.sketch svg>*,.prose>*';
  const bad = {};
  document.querySelectorAll(sel).forEach((e) => {
    const cs = getComputedStyle(e);
    let why = '';
    if (+cs.opacity < 0.05) why = 'opacity ' + cs.opacity;
    else if (cs.scale && /^0(\\s|$)/.test(cs.scale)) why = 'scaled to nothing';
    else if (e.matches('.spine .sp-fun path') && parseFloat(cs.strokeDashoffset) > 0.01) why = 'not drawn';
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
await pass("3. motion allowed: nothing waits for an animation", { width: 1280, height: 800, wait: 700 }, async () => {
  const out = [];
  const h = await evaluate(HIDDEN);                       // 700ms after load, the whole page, unscrolled
  if (Object.keys(h).length) out.push("hidden 700ms after load: " + list(h));
  await sleep(3400);
  const r = await evaluate(RUNNING);
  const stray = Object.fromEntries(Object.entries(r).filter(([k]) => !PAUSABLE.test(k) && !k.includes("follows the scroll")));
  const pausable = Object.keys(r).some((k) => PAUSABLE.test(k));
  if (Object.keys(stray).length) out.push("still running after four seconds: " + list(stray));
  if (pausable && !(await evaluate(HAS_PAUSE))) out.push("something keeps moving and the page has no pause control");
  if ((await evaluate(FRAMES)) > 0 && !(await evaluate(HAS_PAUSE))) out.push("the canvas keeps moving and the page has no pause control");
  return out;
});
await pass("4. scrolled through, motion allowed: nothing hidden, nothing set off by the scroll", { width: 1280, height: 800, wait: 1800 }, async () => {
  const out = [];
  await evaluate(SCROLL_THROUGH);
  const h = await evaluate(HIDDEN);
  if (Object.keys(h).length) out.push("hidden: " + list(h));
  const r = await evaluate(RUNNING);
  const stray = Object.fromEntries(Object.entries(r).filter(([k]) => !PAUSABLE.test(k) && !k.includes("follows the scroll")));
  if (Object.keys(stray).length) out.push("moving after the scroll: " + list(stray));
  return out;
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
const BAR = `(() => { const kids = [...document.querySelectorAll('.hd .in > *')].filter((e) => getComputedStyle(e).display !== 'none');
  const right = Math.max(...kids.map((e) => e.getBoundingClientRect().right)), left = Math.min(...kids.map((e) => e.getBoundingClientRect().left));
  return { right: Math.round(right), left: Math.round(left), w: innerWidth, over: document.documentElement.scrollWidth - document.documentElement.clientWidth }; })()`;
for (const w of [320, 990, 1024, 1100, 1180]) {
  await pass(`7. the top bar fits at ${w}px`, { width: w, height: 800, reduce: true, wait: 900 }, async () => {
    const m = await evaluate(BAR);
    const out = [];
    if (m.right > m.w || m.left < 0) out.push(`the bar runs from ${m.left} to ${m.right} on a ${m.w}px screen`);
    if (m.over > 0) out.push(`scrolls sideways by ${m.over}px`);
    return out;
  });
}
await pass("8. print: nothing left hidden on paper", { width: 1280, height: 800, wait: 1500, print: true }, async () => {
  // the hero's picture is a screen thing: paper does not carry it
  const paper = HIDDEN.replace(".sc-rail li,", "");
  if (paper === HIDDEN) throw new Error("the selector for the hero's picture no longer matches");
  const h = await evaluate(paper);
  return Object.keys(h).length ? ["hidden: " + list(h)] : [];
});
await pass("9. the top bar: the pill never points at the page it is on", { width: 1280, height: 800, reduce: true, wait: 1200 }, async () => {
  const out = [];
  const m = await evaluate(`(() => { const a = document.querySelector('.hd .ctx .play'); if (!a) return null;
    const u = new URL(a.href); return { same: u.pathname === location.pathname, path: u.pathname, here: location.pathname, text: a.textContent.trim() }; })()`);
  if (!m) return ["the top bar has no pill"];
  if (m.same) out.push(`the pill ("${m.text}") points at this page`);
  if (/\/simulator\/$/.test(m.here) && /\/simulator\//.test(m.path)) out.push("inside the simulator the pill still offers the simulator");
  if (/\/learn\//.test(m.here) && !/\/simulator\//.test(m.path)) out.push("inside the tutorial the pill does not offer the simulator");
  return out;
});
const FLOATING = `(async () => { scrollTo({ top: 900, behavior: 'instant' }); await new Promise((r) => setTimeout(r, 400));
  const col = document.querySelector('.cols') || document.querySelector('main .wrap') || document.querySelector('.wrap') || document.querySelector('main');
  const c = col.getBoundingClientRect(), pad = parseFloat(getComputedStyle(col).paddingLeft) || 0;
  return [...document.querySelectorAll('.sw-top, .sw-pill, .tour-fab')].filter((e) => getComputedStyle(e).display !== 'none' && +getComputedStyle(e).opacity > 0.05)
    .map((e) => { const r = e.getBoundingClientRect(); return { cls: e.className.split(' ')[0], inside: r.right > c.left + pad && r.left < c.right - pad }; }); })()`;
for (const w of [390, 1024, 1280]) {
  await pass(`10. floating buttons at ${w}px: none shown`, { width: w, height: 800, reduce: true, wait: 900 }, async () => {
    const f = await evaluate(FLOATING);
    return f.length ? ["shown: " + f.map((x) => x.cls).join(", ")] : [];
  });
}
await pass("10. floating buttons at 1440px: each in the side gutter", { width: 1440, height: 900, reduce: true, wait: 900 }, async () => {
  const f = (await evaluate(FLOATING)).filter((x) => x.inside);
  return f.length ? ["over the page's column: " + f.map((x) => x.cls).join(", ")] : [];
});
await pass("11. versions: every local stylesheet and script is asked for by its version", { width: 1280, height: 800, reduce: true, wait: 300 }, async () => {
  const bare = await evaluate(`[...document.querySelectorAll('link[rel="stylesheet"][href], script[src]')]
    .map((e) => e.getAttribute('href') || e.getAttribute('src')).filter((u) => !/^https?:/.test(u) && !/[?&]v=[0-9a-f]{6,}/.test(u))`);
  return bare.length ? ["no version on: " + bare.join(", ")] : [];
});

// 12. sketches with no stylesheet at all
console.log("\n12. no stylesheet: no mark in a sketch falls back to a solid black fill");
{
  const out = [];
  await send("Network.enable");
  await send("Network.setBlockedURLs", { urls: ["*.css*"] });
  for (const p of ["", "learn/p0-frame/", "learn/what-is-the-agentic-pdlc/"]) {
    await send("Page.navigate", { url: BASE + p });
    await sleep(1500);
    const m = await evaluate(`(() => { const all = [...document.querySelectorAll('svg.sk *')]; return { n: document.querySelectorAll('svg.sk').length,
      black: all.filter((e) => !/^(text|tspan)$/i.test(e.tagName) && getComputedStyle(e).fill === 'rgb(0, 0, 0)').length,
      styled: getComputedStyle(document.body).backgroundColor }; })()`);
    if (!m.n) out.push(`/${p} has no sketch to check`);
    if (m.black) out.push(`/${p}: ${m.black} marks would be filled black`);
  }
  await send("Network.setBlockedURLs", { urls: [] });
  if (out.length) { failures += out.length; console.log("  FAIL  " + out.join("; ")); } else console.log("  ok   three pages with sketches");
}

// 13. the hero, on the home page only
console.log("\n13. the hero: one clock, the right phase named, inside the first screen, the budget, no shift");
{
  const out = [];
  thrown.length = 0;
  const media = { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "no-preference" }] };
  await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await send("Emulation.setEmulatedMedia", media);
  await send("Page.navigate", { url: BASE });
  await sleep(2600);
  const frames = () => evaluate("(window.GlobeMs || { n: -1 }).n");
  const tick = (on) => evaluate(`(() => { const b = document.querySelector('.hero2 [data-motion-toggle]'); b.checked = ${on}; b.dispatchEvent(new Event('change', { bubbles: true })); return true; })()`);
  let a = await frames(); await sleep(500); let b = await frames();
  if (b - a < 10) out.push(`the picture drew ${b - a} frames in half a second`);
  await tick(true); await sleep(200); a = await frames(); await sleep(500); b = await frames();
  if (b !== a) out.push(`paused, and ${b - a} frames were still drawn`);
  await tick(false); await sleep(200); a = await frames(); await sleep(500); b = await frames();
  if (b - a < 10) out.push("resumed, and the picture stayed still");
  // twelve moments round a lap, at four widths: the line under the picture names the phase the aircraft is in
  const NAMES = { 0: "P0", 1: "P1", 2: "P2", 3: "P3", 4: "back" };
  for (const [w, h] of [[1440, 900], [1024, 768], [768, 1024], [390, 844]]) {
    await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 600 });
    await send("Page.navigate", { url: BASE });
    await sleep(1500);
    if (typeof (await evaluate("typeof window.GlobeAt")) !== "string" || (await evaluate("typeof window.GlobeAt")) !== "function") { out.push(`at ${w}px the picture has no clock to set`); continue; }
    await tick(true);
    await evaluate(`document.head.insertAdjacentHTML('beforeend', '<style>.sc-rail li{transition:none!important}</style>'); true`);   // the line is read at once, not mid-change
    const seen = new Set();
    for (let k = 0; k < 12; k++) {
      const m = await evaluate(`(() => { const leg = window.GlobeAt(${(k * 27 / 12 + 0.4).toFixed(2)}); const r = document.querySelector('[data-globe-rail]');
        const lit = [...r.children].filter((li) => getComputedStyle(li).color === getComputedStyle(document.querySelector('.hero2 h1')).color).map((li) => li.textContent.trim());
        return { leg, at: r.getAttribute('data-at'), lit }; })()`);
      seen.add(m.leg);
      const want = m.leg === 4 ? "back" : String(m.leg);
      if (m.at !== want) out.push(`at ${w}px, moment ${k}: the aircraft is in ${NAMES[m.leg]} and the line says ${m.at}`);
      else if (m.lit.length !== 1 || !(m.leg === 4 ? /back to Frame/.test(m.lit[0]) : m.lit[0].startsWith(NAMES[m.leg]))) out.push(`at ${w}px, moment ${k}: lit in the line: ${m.lit.join(" | ") || "nothing"}`);
    }
    if (seen.size !== 5) out.push(`at ${w}px a lap passed through ${seen.size} of its five parts`);
    const box = await evaluate(`(() => { const s = document.querySelector('.scene'), r = s.getBoundingClientRect(), c = document.querySelector('.sc-stage').getBoundingClientRect();
      return { bottom: Math.round(r.bottom), stage: Math.round(c.bottom), left: Math.round(c.left), right: Math.round(c.right), over: document.documentElement.scrollWidth - innerWidth }; })()`);
    if ((w === 390 || w === 1440) && box.bottom > h) out.push(`at ${w} x ${h} the picture and its line end at ${box.bottom}px, below the first screen`);
    if (box.over > 0) out.push(`at ${w}px the page scrolls sideways by ${box.over}px`);
  }
  // the drawing, with the processor slowed four times
  await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await send("Page.navigate", { url: BASE });
  await sleep(2000);
  await send("Emulation.setCPUThrottlingRate", { rate: 4 });
  await evaluate("window.GlobeMs = { n: 0, sum: 0, max: 0 }; true");
  await sleep(3000);
  const g = await evaluate("window.GlobeMs");
  await send("Emulation.setCPUThrottlingRate", { rate: 1 });
  if (!g || g.n < 30) out.push(`the picture drew ${g ? g.n : 0} frames in three seconds`);
  else if (g.sum / g.n > 6) out.push(`the picture takes ${(g.sum / g.n).toFixed(1)}ms a frame at a quarter speed; 6ms is the budget`);
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
console.log(failures ? `\n${failures} failure(s)` : "\nall thirteen passes hold");
process.exit(failures ? 1 : 0);
