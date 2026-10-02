// The acceptance gate for the site's pages: what must hold before a change to layout or motion ships.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/accept.mjs http://localhost:8799/
//
// Eighteen passes, most over one page of each kind, in headless Chrome over the DevTools protocol (the same
// approach as shoot.mjs, so there is nothing to install):
//
//    1. no script            nothing a reader needs is left hidden (opacity 0, scaled to nothing, undrawn), and
//                            the simulator shows its thirteen days as text
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
//   10. floating buttons     back-to-top and mail never sit on the words: below 1440 wide none is shown;
//                            at 1440 each sits in the side gutter, clear of the page's column
//   11. versions             every local stylesheet and script is asked for by an address that carries its version,
//                            so a new page can never be paired with an old file from a browser's cache
//   12. no stylesheet        with every stylesheet blocked, no mark in a sketch falls back to a solid black fill
//   13. the hero             one clock (the pause holds it; a tab left and come back to goes on from where it was);
//                            at twelve moments round a lap, at four widths, the line under the picture names the
//                            phase the aircraft is in; the picture ends inside the first screen on a phone and a
//                            laptop; its drawing stays inside its budget with the processor slowed four times; and
//                            the page does not shift as it is scrolled
//   14. the measure          on a lesson at 1440, no prose runs over 75 characters a line: each paragraph's
//                            characters a line, from its width and the average width of its own text in its font
//   15. two right edges      on a lesson at 1440, text stops at one right edge and pictures, tables and code at
//                            one other: every block of the page, and a caption that sits on the page, ends on
//                            one of two lines, and anything on a third is listed
//   16. the game's first paint  with script, the simulator's text for a reader without script is hidden from the
//                            first paint, while the game's own script has still not arrived; when the rules fail to
//                            load, the text comes back
//   17. the bytes            read from the built site with node's zlib (level 9): base.css under 32 KB as shipped
//                            (the build drops its comments), the game's three scripts under 46 KB, every page's
//                            HTML under 25 KB (the pages that were already
//                            larger on 2 October 2026 each held to its size that day, rounded up, plus one KB), and
//                            no font file but the four the site has
//   18. map height           every page under learn/ in the sitemap, at 1440 x 900: the figure that holds a lesson's
//                            map (data-map, from pages/maps.py) is at most 630px tall, 70% of the screen (council 9)
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

import { createServer } from "node:net";
import { spawn } from "node:child_process";
import { rmSync, readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { gzipSync } from "node:zlib";
import { tmpdir } from "node:os";
import { join } from "node:path";

const BASE = process.argv[2];
if (!BASE) { console.error("usage: node accept.mjs <site url, ending in />"); process.exit(2); }
const PAGES = ["", "method/", "product-manager/", "qa/", "protocol/", "models/", "templates/", "prompts/",
  "frameworks/", "pictures/", "learn/", "learn/fundamentals/", "learn/the-hard-gate/", "learn/p0-frame/", "simulator/",
  "labs/", "labs/grow-the-spec/", "labs/grow-the-spec/others/", "labs/write-the-system-prompt/",
  "labs/write-the-system-prompt/others/", "tools/", "tools/claude-at-the-desk/",
  "tools/chatgpt-and-codex/", "tools/google-ai-studio-and-jules/"];
// The simulator draws on a canvas from script, which the browser's list of animations cannot see. Its
// loop counts its own frames in window.NDFrames, so the gate can ask.
const FRAMES = `(typeof window.NDFrames === "number" ? window.NDFrames : -1)`;
// animations allowed to keep running, provided the page that runs them carries a pause control
const PAUSABLE = /^(twr-|nd-)/;
const LOADED = `(() => { const h = document.querySelector('.hd'); return !!h && getComputedStyle(h).position === 'sticky' && !!document.querySelector('main h1, .hero2 h1'); })()`;
const HAS_PAUSE = `!!document.querySelector('[data-motion-toggle]')`;
const SCROLL_THROUGH = `(async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 500) { scrollTo({ top: y, behavior: 'instant' }); await new Promise((r) => requestAnimationFrame(() => setTimeout(r, 90))); } await new Promise((r) => setTimeout(r, 900)); return true; })()`;

const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = await new Promise((ok) => { const s = createServer().listen(0, "127.0.0.1", () => { const p = s.address().port; s.close(() => ok(p)); }); });   // a port no other Chrome holds, so a run never drives another run's browser
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
const held = [];                  // requests the gate has paused (pass 16)
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.method === "Fetch.requestPaused") held.push(m.params);
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

// the simulator's thirteen days as text, for a reader without script: shown, and saying why
const PLAIN = `(() => { const p = document.querySelector('.nd-plain'); return p ? getComputedStyle(p).display !== 'none' && p.getBoundingClientRect().height > 400 && /The game needs script to run/.test(p.textContent) : null; })()`;
await pass("1. no script: nothing left hidden", { width: 1280, height: 800, noscript: true, wait: 3200 }, async () => {
  const h = await evaluate(HIDDEN), out = Object.keys(h).length ? ["hidden: " + list(h)] : [];
  if ((await evaluate(PLAIN)) === false) out.push("without script the thirteen days as text are not shown");
  return out;
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

// 14 and 15, on the lesson pages (main.lm): the measure, and two right edges. Other pages have nothing to check.
const MEASURE = `(async () => {
  await document.fonts.ready;
  const main = document.querySelector('main.lm');
  if (!main) return null;
  const ctx = document.createElement('canvas').getContext('2d');
  const els = [...main.querySelectorAll('.lede, .prose p, .prose li, .prose blockquote')]
    .filter((e) => !e.closest('.bbw, .tw, figure, .codebox, .dgb') && e.offsetParent && e.textContent.trim().length > 60);
  let worst = { cpl: 0 };
  for (const e of els) {
    const cs = getComputedStyle(e);
    ctx.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    const text = e.textContent.replace(/\\s+/g, ' ').trim();
    const w = e.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    const cpl = w / (ctx.measureText(text).width / text.length);
    if (cpl > worst.cpl) worst = { cpl: Math.round(cpl * 10) / 10, w: Math.round(w), fs: cs.fontSize, text: text.slice(0, 48) };
  }
  return { n: els.length, worst };
})()`;
await pass("14. the measure: on a lesson at 1440, no prose line over 75 characters", { width: 1440, height: 900, reduce: true, wait: 900 }, async () => {
  const m = await evaluate(MEASURE);
  if (!m) return [];
  if (!m.n) return ["no prose found to measure"];
  return m.worst.cpl > 75 ? [`prose runs ${m.worst.cpl} characters a line (${m.worst.w}px at ${m.worst.fs}): "${m.worst.text}..."`] : [];
});
const EDGES = `(() => {
  const main = document.querySelector('main.lm');
  if (!main) return null;
  const vis = (e) => { const cs = getComputedStyle(e), r = e.getBoundingClientRect(); return cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0 && r.height > 0; };
  const name = (e) => e.tagName.toLowerCase() + (e.classList[0] ? '.' + e.classList[0] : '');
  const prose = main.querySelector('.prose');
  const items = [...main.children].filter((e) => e !== prose);
  [...(prose ? prose.children : [])].forEach((e) => items.push(...(e.matches('.lm-note') ? e.children : [e])));
  // a caption under a figure with no frame of its own sits on the page; inside a frame it is the frame's business
  (prose ? [...prose.querySelectorAll('figure')] : []).forEach((f) => { const cs = getComputedStyle(f);
    if (!parseFloat(cs.borderTopWidth) && /rgba\\(0, 0, 0, 0\\)|transparent/.test(cs.backgroundColor)) items.push(...f.querySelectorAll(':scope > figcaption')); });
  const edges = [];
  for (const e of items.filter(vis)) {
    const r = Math.round(e.getBoundingClientRect().right);
    let g = edges.find((x) => Math.abs(x.at - r) <= 1);
    if (!g) edges.push(g = { at: r, n: 0, what: {} });
    g.n++; g.what[name(e)] = (g.what[name(e)] || 0) + 1;
  }
  return edges.sort((a, b) => b.n - a.n);
})()`;
await pass("15. two right edges: on a lesson at 1440, text ends on one line, pictures, tables and code on one other", { width: 1440, height: 900, reduce: true, wait: 900 }, async () => {
  const edges = await evaluate(EDGES);
  if (!edges || edges.length <= 2) return [];
  const say = (g) => `${g.at} (${Object.entries(g.what).map(([k, v]) => v > 1 ? `${k} x${v}` : k).join(", ")})`;
  return [`${edges.length} right edges, two allowed: ${edges.map(say).join("; ")}`];
});

// 16. the game's first paint: the page's head marks it for script before it paints, so the text for a
// reader without script never shows while the game's scripts are on their way. The gate holds game.js
// back, so the page paints with the rules and the pictures but not the game, and looks; then lets it go.
// Then it fails sim.js, as a browser that could not fetch the rules would, and the text must come back.
console.log("\n16. the game's first paint: the text for a reader without script is hidden while the game loads");
{
  const out = [];
  await send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await send("Emulation.setEmulatedMedia", { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "reduce" }] });
  const STATE = `({ painted: performance.getEntriesByType('paint').some((e) => e.name === 'first-contentful-paint'), mark: document.documentElement.classList.contains('nd-js'),
    plain: (() => { const p = document.querySelector('.nd-plain'); return p ? getComputedStyle(p).display !== 'none' && !p.hidden : null; })(), game: !!document.querySelector('#nd:not([hidden]) .nd-line') })`;
  const hold = async (pattern) => { held.length = 0; await send("Fetch.enable", { patterns: [{ urlPattern: pattern, requestStage: "Request" }] }); };
  await send("Network.enable"); await send("Network.setCacheDisabled", { cacheDisabled: true });      // every load asks for every file
  await hold("*play/game.js*");
  await send("Page.navigate", { url: BASE + "simulator/" });
  for (let i = 0; i < 40 && !held.length; i++) await sleep(100);
  await sleep(1200);
  const early = await evaluate(STATE);
  if (!held.length) out.push("game.js was never asked for");
  else if (!early.painted) out.push("with game.js held back, the page never painted");
  else if (!early.mark || early.plain !== false) out.push(`at first paint, before game.js arrived, the text for a reader without script is ${early.plain ? "shown" : "missing"}`);
  for (const p of held.splice(0)) await send("Fetch.continueRequest", { requestId: p.requestId });
  await send("Fetch.disable"); await sleep(1500);
  const booted = await evaluate(STATE);
  if (!booted.game || booted.plain !== false) out.push(`once game.js arrived: game ${booted.game}, the text shown ${booted.plain}`);
  await hold("*play/sim.js*");
  await send("Page.navigate", { url: BASE + "simulator/" });
  for (let i = 0; i < 40 && !held.length; i++) await sleep(100);
  if (!held.length) out.push("sim.js was never asked for");
  for (const p of held.splice(0)) await send("Fetch.failRequest", { requestId: p.requestId, errorReason: "Failed" });
  await send("Fetch.disable"); await sleep(1800);
  await send("Network.setCacheDisabled", { cacheDisabled: false });
  const failed = await evaluate(STATE);
  if (failed.plain !== true || failed.mark) out.push(`with sim.js unreachable the game cannot start, and the text for a reader without script is ${failed.plain ? "shown" : "still hidden"}`);
  if (out.length) { failures += out.length; console.log("  FAIL /simulator/  " + out.join("; ")); }
  else console.log("  ok   /simulator/  hidden at first paint with game.js held back, the game up once it came, the text back when sim.js could not load");
}

// 17. the bytes, from the built site. A budget is a ceiling: a page or a file over it fails, and the way
// back is to make the thing smaller, not the number larger. The pages over 25 KB on the day this pass was
// written are each held to what they were (rounded up, plus one KB), so they can shrink and never grow.
// One hold was raised since, on purpose: the picture pack (pictures/index.html, 29 to 38) on 2 October 2026, when it
// gained the thirty lesson sketches and the leadership page's map, each with its card and its image data.
console.log("\n17. the bytes: base.css, the game's scripts, every page's HTML, the fonts");
{
  const out = [], SITE = new URL("../_site/", import.meta.url).pathname;
  const kb = (f) => gzipSync(readFileSync(SITE + f), { level: 9 }).length / 1024;
  const HELD = { "workbench/index.html": 825, "app/SkyWays-Architect.html": 824, "prompts/index.html": 57, "templates/index.html": 48, "solution-architect/index.html": 46,
    "devops/index.html": 44, "qa/index.html": 44, "engineering/index.html": 43, "product-manager/index.html": 35, "labs/grow-the-spec/index.html": 34, "pictures/index.html": 38,
    "learn/evolution-of-the-pdlc/index.html": 29, "learn/what-is-aidd/index.html": 28 };
  const FONTS = ["assets/fonts/geist-mono.woff2", "assets/fonts/geist.woff2", "assets/fonts/instrument-sans.woff2", "assets/fonts/patrick-hand.woff2"];
  if (!existsSync(SITE + "index.html")) out.push(`no built site at ${SITE}`);
  else {
    const files = [];
    (function walk(d) { for (const f of readdirSync(SITE + d)) { const p = d + f; if (statSync(SITE + p).isDirectory()) walk(p + "/"); else files.push(p); } })("");
    const css = kb("theme/base.css"), game = ["play/game.js", "play/sim.js", "play/art.js"].reduce((n, f) => n + kb(f), 0);
    // Lowered from 40 on purpose on 3 October 2026: the build now ships every stylesheet without its comments (build.py, lean()),
    // which took base.css from 39.7 to about 29.5 KB. The budget follows it down, so the room is kept for work, not for comments.
    if (css >= 32) out.push(`base.css is ${css.toFixed(1)} KB gzipped as shipped; the budget is 32`);
    for (const f of files.filter((f) => f.endsWith(".css"))) if (readFileSync(SITE + f, "utf8").includes("/*")) out.push(`${f} ships with its comments`);
    // Raised from 45 on purpose on 2 October 2026: the owner asked for a briefing before a late start (the earlier calls, the documents,
    // where the run stands), which took the three scripts to 45.97 KB after the savings in site/GAME.md; 46 is that, rounded up to the next half KB.
    if (game >= 46) out.push(`the game's scripts are ${game.toFixed(1)} KB gzipped; the budget is 46`);
    const pages = files.filter((f) => f.endsWith(".html")), over = [];
    let most = { f: "", n: 0 };
    for (const f of pages) { const n = kb(f), cap = HELD[f] || 25; if (n >= cap) over.push(`${f} ${n.toFixed(1)} KB (${cap})`); if (!HELD[f] && n > most.n) most = { f, n }; }
    if (over.length) out.push("pages over their budget: " + over.join(", "));
    const fonts = files.filter((f) => /\.(woff2?|ttf|otf|eot)$/i.test(f)).sort();
    if (fonts.join(" ") !== FONTS.join(" ")) out.push(`the font files are ${fonts.join(", ")}`);
    const remote = pages.filter((f) => /fonts\.(googleapis|gstatic)\.com/.test(readFileSync(SITE + f, "utf8")));
    if (remote.length) out.push(`a page asks a font host for a font: ${remote.slice(0, 3).join(", ")}`);
    if (!out.length) console.log(`  ok   base.css ${css.toFixed(1)} KB, the game's scripts ${game.toFixed(1)} KB, ${pages.length} pages (the largest held to 25 KB is /${most.f.replace(/index\.html$/, "")} at ${most.n.toFixed(1)}), four fonts`);
  }
  if (out.length) { failures += out.length; console.log("  FAIL  " + out.join("; ")); }
}

// 18. map height. Council 9 capped a lesson's map at 70% of a 1440 by 900 screen: 630px for the figure, its
// drawing, frame and caption together. Every page under learn/ that the sitemap lists is opened at that size,
// and the figure pages/maps.py marks with data-map is measured; a page without a map has nothing to check.
// The same loop holds council 10's lesson frame on every lesson (a page whose main is .lm): pass 14's measure
// and pass 15's two right edges, which those passes check on two lessons only; one left edge, the breadcrumb's;
// and the guide (aside.lguide), which at 0, 25, 50 and 75% of the way down is on screen, ends within 24px of the
// column's right edge, and marks one section: the last whose heading has passed the upper third of the window,
// or the first before any has (site.js wireSteps, with the first link's mark standing for the lesson's opening).
console.log("\n18. every lesson at 1440 x 900: the map at most 630px tall, the measure, the edges, the guide");
{
  const out = [], CAP = 0.7 * 900;
  thrown.length = 0;
  await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await send("Emulation.setEmulatedMedia", { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "reduce" }] });
  const sitemap = await fetch(BASE + "sitemap.xml").then((r) => (r.ok ? r.text() : "")).catch(() => "");
  const lessons = [...new Set([...sitemap.matchAll(/<loc>[^<]*?\/learn\/([a-z0-9-]+)\/<\/loc>/g)].map((x) => x[1]))];
  if (!lessons.length) out.push("the sitemap lists no page under learn/");
  const LEFT = `(() => { const main = document.querySelector('main.lm'), c = document.querySelector('.crumbs');
    const prose = main.querySelector('.prose'), at = [];
    for (const e of [...main.children].filter((e) => e !== prose).concat([...(prose ? prose.children : [])])) {
      const r = e.getBoundingClientRect(); if (getComputedStyle(e).display !== 'none' && r.width > 0 && r.height > 0) at.push(Math.round(r.left)); }
    return { min: Math.min(...at), max: Math.max(...at), crumbs: c ? Math.round(c.getBoundingClientRect().left) : null }; })()`;
  const GUIDE = (p) => `(async () => { const g = document.querySelector('.lguide'); if (!g) return null;
    scrollTo({ top: Math.round(${p} * (document.documentElement.scrollHeight - innerHeight)), behavior: 'instant' });
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(r, 50))));
    const r = g.getBoundingClientRect(), row = g.parentElement, edge = row.getBoundingClientRect().right - parseFloat(getComputedStyle(row).paddingRight);
    const links = [...g.querySelectorAll('.rl[data-for]')], line = Math.max(140, innerHeight * 0.3);
    let want = links[0];
    for (const a of links) { const h = document.getElementById(a.getAttribute('href').slice(1)); if (h && h.getBoundingClientRect().top < line) want = a; }
    const on = links.filter((a) => a.hasAttribute('aria-current'));
    return { top: Math.round(r.top), bottom: Math.round(r.bottom), off: Math.round(edge - r.right), on: on.map((a) => a.textContent),
      ok: on.length === 1 && on[0] === want, want: want ? want.textContent : 'no section' }; })()`;
  let maps = 0, tallest = { h: 0, at: "" }, framed = 0, worst = { cpl: 0, at: "" };
  for (const slug of lessons) {
    const at = `/learn/${slug}/`;
    await send("Page.navigate", { url: BASE + at.slice(1) });
    await sleep(900);
    const m = await evaluate(`(async () => { await document.fonts.ready; const f = document.querySelector('main figure[data-map]');
      return { loaded: ${LOADED}, h: f ? Math.round(f.getBoundingClientRect().height * 10) / 10 : null }; })()`);
    if (!m.loaded) { out.push(`${at} did not load`); continue; }
    const cpl = await evaluate(MEASURE);
    if (cpl) {
      framed++;
      if (!cpl.n) out.push(`${at}: no prose found to measure`);
      else if (cpl.worst.cpl > 75) out.push(`${at}: prose runs ${cpl.worst.cpl} characters a line ("${cpl.worst.text}...")`);
      if (cpl.n && cpl.worst.cpl > worst.cpl) worst = { cpl: cpl.worst.cpl, at };
      const edges = await evaluate(EDGES), left = await evaluate(LEFT);
      if (edges.length > 2) out.push(`${at}: ${edges.length} right edges, two allowed: ${edges.map((g) => `${g.at} (${Object.keys(g.what).join(", ")})`).join("; ")}`);
      if (left.max - left.min > 1 || Math.abs(left.min - left.crumbs) > 1) out.push(`${at}: blocks start from x ${left.min} to ${left.max}, the breadcrumb at ${left.crumbs}`);
      for (const p of [0, 0.25, 0.5, 0.75]) {
        const g = await evaluate(GUIDE(p)), where = `${at} at ${p * 100}%`;
        if (!g) { out.push(`${at}: no guide`); break; }
        if (g.top < 0 || g.bottom > 900) out.push(`${where}: the guide runs from y ${g.top} to ${g.bottom}`);
        if (Math.abs(g.off) > 24) out.push(`${where}: the guide ends ${g.off}px inside the column's right edge`);
        if (!g.ok) out.push(`${where}: the guide marks ${g.on.length ? g.on.join(" and ") : "nothing"}, not ${g.want}`);
      }
    }
    if (m.h === null) continue;
    maps++;
    if (m.h > tallest.h) tallest = { h: m.h, at };
    if (m.h > CAP) out.push(`${at} is ${m.h}px tall`);
  }
  if (lessons.length && !maps) out.push("no lesson has a figure marked data-map to measure");
  if (lessons.length && !framed) out.push("no lesson has a main.lm to check");
  if (thrown.length) out.push("script error: " + thrown[0]);
  if (out.length) { failures += out.length; console.log(`  FAIL  (the cap is ${CAP}px) ` + out.join("; ")); }
  else console.log(`  ok   ${maps} lessons with a map, the tallest ${tallest.at} at ${tallest.h}px; ${framed} lessons in the frame, ` +
    `the longest line ${worst.cpl} characters (${worst.at}), one left edge, two right ones, the guide on screen and marking the section being read`);
}

// 19. the home page's bands (council 10): one function for each band's parcel, H3 to H8, in the order the bands run,
// each called at 1440 x 900 and at 390 x 844 on a fresh load of the home page (dark, reduced motion, at the top). A
// function returns its failures as sentences; one that needs another state (motion, the light theme, a hover, a
// scroll) sets it itself. A parcel writes only inside its own function, between its own two comments, and never
// edits the list that calls them, so parcels built side by side never touch the same lines.
console.log("\n19. the home page's bands: each band's own checks at 1440 x 900 and 390 x 844");
{
  // home · H3 map: the methods band, #methods
  async function bandH3(w, h) {
    // At 1440 x 900 with the eyebrow just under the header, the frame and its lower pill end inside the screen. At both
    // widths each shape (on a phone, its strip) spans the phases named in the sentence a screen reader hears, and its
    // ends sit in the phases that sentence names; nothing is under 11px and no handwriting under 16px; at most eight
    // notes show; every text is 4.5:1 against the layers painted under it (the wash and the shapes are siblings, not
    // ancestors, so the stack at the words is read), in both themes. At 390 the map is measured again at 320: no
    // sideways scroll, each head inside its column, the sign-off's pill on one line.
    const out = [];
    const MAP = `(async () => {
      await document.fonts.ready;
      const band = document.getElementById('methods'), map = band && band.querySelector('figure.vm');
      if (!map) return null;
      const shown = (e) => !!e && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().height > 0;
      scrollTo({ top: band.querySelector('.eyebrow').getBoundingClientRect().top + scrollY - 84, behavior: 'instant' });
      await new Promise((r) => setTimeout(r, 150));
      const fr = map.querySelector('.vm-fr'), low = map.querySelector('.vm-so .b');
      const o = { frame: Math.round((shown(fr) ? fr : map.querySelector('.vm-g')).getBoundingClientRect().bottom),
        pill: shown(low) ? Math.round(low.getBoundingClientRect().bottom) : 0, pillH: Math.round(map.querySelector('.vm-so em').getBoundingClientRect().height),
        over: document.documentElement.scrollWidth - document.documentElement.clientWidth, spans: [], small: [], heads: [], notes: 0, shapes: 0 };
      const cols = [...map.querySelectorAll('.vm-p')].map((a) => a.getBoundingClientRect());
      const names = [...map.querySelectorAll('.vm-p .c-name')].map((n) => n.textContent.replace('&', 'and'));
      const col = (x) => cols.findIndex((c) => x >= c.left && x < c.right);
      const mid = (e) => { const q = e.getBoundingClientRect(); return col((q.left + q.right) / 2); };
      for (const li of map.querySelectorAll('.vm-r')) {
        o.shapes++;
        const said = li.querySelector('.vm-pl > .vh').textContent, nm = li.querySelector('.vm-nm').textContent;
        const cov = (said.match(/covers (.+?)(?=[,;.]|$)/) || [, ''])[1];
        const want = cov === 'all four phases' ? [0, 3] : cov.split(' to ').map((x) => names.indexOf(x));
        if (want.length === 1) want.push(want[0]);
        const bar = li.querySelector('.vm-bar'), r = (shown(bar) ? bar : li.querySelector('.vm-pl')).getBoundingClientRect();
        const got = [col(r.left + 1), col(r.right - 1)];
        if (got.join() !== want.join()) o.spans.push(nm + ' is drawn across phases ' + got.join(' to ') + ' and read as "covers ' + cov + '"');
        const ends = [...said.matchAll(/ in (Frame|Design and Spec|Build and Prove|Run and Learn)/g)].map((x) => names.indexOf(x[1]));
        const add = said.match(/this manual adds (.+?)(?=[,;.]|$)/);
        if ([...li.querySelectorAll('.vm-lt')].map(mid).join() !== ends.join() || [...li.querySelectorAll('.vm-ex')].map(mid).join() !== (add ? [names.indexOf(add[1])] : []).join())
          o.spans.push(nm + ': its ends are not in the phases its sentence names');
      }
      const texts = [...band.querySelectorAll('*')].filter((e) => !e.closest('.vh') && e.checkVisibility() && [...e.childNodes].some((t) => t.nodeType === 3 && t.nodeValue.trim()));
      for (const e of texts) {
        const cs = getComputedStyle(e), fs = parseFloat(cs.fontSize), hand = /Patrick/.test(cs.fontFamily);
        if (fs < (hand ? 16 : 11)) o.small.push((hand ? 'handwriting at ' : '') + fs + 'px, "' + e.textContent.trim().slice(0, 30) + '"');
      }
      o.notes = new Set(texts.filter((e) => /Patrick/.test(getComputedStyle(e).fontFamily)).map((e) => e.textContent.trim())).size;
      for (const a of map.querySelectorAll('.vm-p')) {
        const r = a.getBoundingClientRect();
        for (const k of a.querySelectorAll('.c-key,.c-name')) { const q = k.getBoundingClientRect(); if (q.left < r.left - 0.5 || q.right > r.right + 0.5) o.heads.push(k.textContent); }
      }
      return o;
    })()`;
    const CONTRAST = (light) => `(async () => {
      if (${light}) document.documentElement.setAttribute('data-theme', 'light');
      await document.fonts.ready;
      const band = document.getElementById('methods');
      const cv = document.createElement('canvas'); cv.width = cv.height = 1;
      const cx = cv.getContext('2d', { willReadFrequently: true });
      const paint = (base, c) => { cx.globalCompositeOperation = 'copy'; cx.fillStyle = base; cx.fillRect(0, 0, 1, 1);
        cx.globalCompositeOperation = 'source-over'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); return cx.getImageData(0, 0, 1, 1).data; };
      const rgba = (c) => { const k = paint('#000', c), w = paint('#fff', c), a = Math.max(0, Math.min(1, 1 - (w[0] - k[0] + w[1] - k[1] + w[2] - k[2]) / 765));
        return a > 0.004 ? [k[0] / a, k[1] / a, k[2] / a, a] : [0, 0, 0, 0]; };
      const over = (t, u) => [0, 1, 2].map((i) => t[i] * t[3] + u[i] * (1 - t[3])).concat(1);
      const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
      const cr = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
      const done = new Set(), low = [];
      const top = band.getBoundingClientRect().top + scrollY, end = top + band.offsetHeight;
      for (let y = top - 64; y < end; y += innerHeight - 140) {
        scrollTo({ top: y, behavior: 'instant' });
        await new Promise((r) => setTimeout(r, 80));
        const tw = document.createTreeWalker(band, NodeFilter.SHOW_TEXT, { acceptNode: (t) => (t.nodeValue.trim() ? 1 : 3) });
        for (let t = tw.nextNode(); t; t = tw.nextNode()) {
          if (done.has(t)) continue;
          const e = t.parentElement, rg = document.createRange(); rg.selectNodeContents(t);
          const rr = rg.getClientRects()[0];
          if (e.closest('.vh') || !e.checkVisibility({ opacityProperty: true, visibilityProperty: true }) || !rr || rr.width < 2) { done.add(t); continue; }
          if (rr.top < 70 || rr.bottom > innerHeight - 4) continue;
          done.add(t);
          for (const fx of [0.2, 0.5, 0.8]) {
            let bg = [255, 255, 255, 1];
            for (const el of document.elementsFromPoint(rr.left + rr.width * fx, rr.top + rr.height * 0.55).reverse()) {
              const c = rgba(getComputedStyle(el).backgroundColor);
              if (c[3] > 0) bg = over(c, bg);
              if (el === e) break;
            }
            const ratio = cr(over(rgba(getComputedStyle(e).color), bg), bg);
            if (ratio < 4.5) { low.push(ratio.toFixed(2) + ':1, "' + t.nodeValue.trim().slice(0, 28) + '"'); break; }
          }
        }
      }
      return low;
    })()`;
    const say = (m, at) => {
      if (!m) return out.push(`${at}: no method map (figure.vm) in #methods`);
      if (m.shapes !== 5) out.push(`${at}: ${m.shapes} shapes on the map, five expected`);
      if (m.over > 0) out.push(`${at}: the page scrolls sideways by ${m.over}px`);
      if (m.spans.length) out.push(`${at}: ${m.spans.join("; ")}`);
      if (m.small.length) out.push(`${at}: text too small: ${m.small.slice(0, 3).join("; ")}`);
      if (m.notes > 8) out.push(`${at}: ${m.notes} handwritten notes show; eight at most`);
      if (m.heads.length) out.push(`${at}: a phase's key or name runs out of its column: ${m.heads.join(", ")}`);
      if (m.pillH > 24) out.push(`${at}: the sign-off's pill wraps (${m.pillH}px tall)`);
    };
    try {
      const m = await evaluate(MAP);
      say(m, `${w}px`);
      if (m && w >= 1440 && (m.frame > h || m.pill > h)) out.push(`with the eyebrow under the header the frame ends at ${m.frame}px and its pill at ${m.pill}px, past the ${h}px screen`);
      for (const light of [false, true]) {
        const low = await evaluate(CONTRAST(light));
        if (low.length) out.push(`${light ? "light" : "dark"}: under 4.5:1: ${low.slice(0, 4).join("; ")}`);
      }
      if (w === 390) {
        await send("Emulation.setDeviceMetricsOverride", { width: 320, height: 640, deviceScaleFactor: 1, mobile: true });
        await sleep(500);
        say(await evaluate(MAP), "320px");
      }
    } catch (e) {
      out.push("the map's checks could not run: " + e.message.slice(0, 160));
    }
    return out;
  }
  // end of home · H3

  // home · H4 chooser: #choose
  async function bandH4(w, h) {
    return [];
  }
  // end of home · H4

  // home · H5 people: the tutorial band, #tutorial
  async function bandH5(w, h) {
    return [];
  }
  // end of home · H5

  // home · H6 day card: the simulator band, #simulator
  async function bandH6(w, h) {
    return [];
  }
  // end of home · H6

  // home · H7 library: #library
  // Nine cards, each one link: the workbench, the tutorial and the simulator, then six shelves (verdict-home 1.7). Each
  // count is the one the page it opens states; at 1440 a row's names share a baseline; on a phone (390, then 320) no
  // text is under 11px, every card is 44px or more, nothing scrolls sideways, and at 390 the band is 1,500px or less.
  // The room is the band's one picture: 4 KB or less, whole pixels, keeping its left wall on a wide card and centred on
  // a phone, and shown nowhere else on the page. Each tool's ground is the same in both themes, every text 4.5:1 on its
  // ground in both, the cards flat at rest and moved by a transform and a colour; on paper the words are ink.
  async function bandH7(w, h) {
    const out = [];
    const LOOK = `(async () => {
      await document.fonts.ready;
      const lib = document.querySelector('#library .lib');
      if (!lib) return null;
      const cv = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
      const rgb = (c) => { cv.clearRect(0, 0, 1, 1); cv.fillStyle = '#000'; cv.fillStyle = c; cv.fillRect(0, 0, 1, 1); return [...cv.getImageData(0, 0, 1, 1).data]; };
      const lum = (p) => p.slice(0, 3).map((x) => (x /= 255) <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4).reduce((s, x, i) => s + x * [0.2126, 0.7152, 0.0722][i], 0);
      const ground = (e) => { for (; e; e = e.parentElement) { const p = rgb(getComputedStyle(e).backgroundColor); if (p[3] > 250) return p; } return rgb(getComputedStyle(document.body).backgroundColor); };
      const seen = (e) => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden'; };
      // every piece of text the band shows, with its size and its contrast on what is behind it (text drawn half
      // transparent is first laid on its ground, as the eye sees it)
      const texts = [];
      for (const e of lib.querySelectorAll('*')) {
        if (!seen(e)) continue;
        const own = [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()), after = getComputedStyle(e, '::after').content;
        if (!own && !(after && !/^(none|normal)$/.test(after))) continue;
        const cs = getComputedStyle(e), bg = ground(e), op = +cs.opacity, c = rgb(cs.color);
        const fg = c.slice(0, 3).map((v, i) => v * op * c[3] / 255 + bg[i] * (1 - op * c[3] / 255)), a = lum(fg), b = lum(bg);
        texts.push({ t: (own ? e.textContent : after).trim().replace(/\\s+/g, ' ').slice(0, 30), px: parseFloat(cs.fontSize), bold: +cs.fontWeight >= 600,
          ratio: Math.round(((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)) * 100) / 100, ink: Math.round(a * 1000) / 1000, paper: Math.round(b * 1000) / 1000 });
      }
      const cards = [...lib.children].map((c) => { const r = c.getBoundingClientRect(), n = c.querySelector(':scope > b, .fl-b > b'), cs = getComputedStyle(c);
        return { tag: c.tagName, cls: c.className, href: c.getAttribute('href'), count: ((c.querySelector('.lib-k') || {}).textContent || '').replace(/\\s+/g, ' '),
          name: n ? n.textContent : '', words: c.textContent, top: Math.round(r.top), h: Math.round(r.height), w: Math.round(r.width),
          nameBottom: n ? Math.round(n.getBoundingClientRect().bottom * 10) / 10 : 0, transform: cs.transform }; });
      const pic = (k) => { const p = lib.querySelector('.fl-' + k + ' .fl-p'); return p ? rgb(getComputedStyle(p).backgroundColor).join() : ''; };
      const imgs = [...lib.querySelectorAll('img')].map((i) => { const r = i.getBoundingClientRect(), p = i.parentElement.getBoundingClientRect();
        return { nw: i.naturalWidth, nh: i.naturalHeight, w: r.width, h: r.height, px: getComputedStyle(i).imageRendering,
          left: Math.round(p.left - r.left), right: Math.round(r.right - p.right) }; });
      const all = [...document.querySelectorAll('img')].map((i) => (i.currentSrc || i.src).replace(/[?#].*$/, ''));
      return { cards, texts, imgs, twice: all.filter((s, i) => all.indexOf(s) !== i), wb: pic('wb'), sim: pic('sim'), learn: pic('learn'),
        paper: rgb(getComputedStyle(document.documentElement).getPropertyValue('--sk-paper').trim()).join(), rows: lib.querySelectorAll('.trk > span').length,
        sums: [...lib.querySelectorAll('.wbc-r b')].map((b) => b.textContent), meter: (lib.querySelector('.wbc-m i') || document.body).style.getPropertyValue('--v'),
        band: Math.round(document.querySelector('#library').getBoundingClientRect().height), over: document.documentElement.scrollWidth - document.documentElement.clientWidth };
    })()`;
    const theme = (light) => evaluate(`(document.documentElement.${light ? "setAttribute('data-theme','light')" : "removeAttribute('data-theme')"}, true)`);
    const low = (m, at) => { for (const t of m.texts) if (t.ratio < (t.px >= 24 || (t.px >= 18.66 && t.bold) ? 3 : 4.5)) out.push(`${at}: "${t.t}" is ${t.ratio}:1 on its ground`); };
    const m = await evaluate(LOOK);
    if (!m) return ["the library has no .lib grid"];
    const kinds = m.cards.map((c) => c.cls).join(" | ");
    if (kinds !== "fl fl-wb | fl fl-learn | fl fl-sim | shf | shf | shf | shf | shf | shf" || m.cards.some((c) => c.tag !== "A")) {
      return [`the cards are ${kinds}; want the workbench, the tutorial and the simulator, then six shelves, each card one link`];
    }
    const go = ["workbench/", "", "simulator/", "templates/", "prompts/", "models/", "tools/", "frameworks/", "pictures/"];
    m.cards.forEach((c, i) => { if (go[i] && c.href !== go[i]) out.push(`card ${i + 1} ("${c.name}") goes to ${c.href}, not ${go[i]}`); });
    if (m.cards.some((c) => c.transform !== "none")) out.push("a card is not flat at rest");
    if (/Recommended|Most popular|\bNew\b/.test(m.cards.map((c) => c.words).join(" "))) out.push("a card wears a badge");
    if (m.wb !== "20,33,49,255" || m.sim !== "43,41,66,255") out.push(`the workbench's ground is ${m.wb} and the simulator's ${m.sim}; want #142131 and #2B2942`);
    if (m.learn !== m.paper) out.push(`the tutorial's ground is ${m.learn}, not the lessons' paper (${m.paper})`);
    const num = (i, re) => +((m.cards[i].count.match(re) || [])[1]);
    if (m.rows !== num(1, /(\d+) tracks/)) out.push(`the tutorial's picture lists ${m.rows} tracks and its count says ${num(1, /(\d+) tracks/)}`);
    const [saves, costs] = m.sums.map((s) => +s.replace(/\D/g, "")), bar = `${Math.round((100 * costs) / (saves + costs))}%`;
    if (m.sums[2] !== bar || m.meter !== bar) out.push(`the calculator's bar reads ${m.sums[2]} with its meter at ${m.meter}; ${m.sums[0]} and ${m.sums[1]} make ${bar}`);
    // the room: the band's one picture, the game's own art at one times, shown at whole pixels
    if (m.imgs.length !== 1) out.push(`the band has ${m.imgs.length} pictures; the room is its only one`);
    for (const i of m.imgs) {
      const k = i.w / i.nw;
      if (i.nw !== 144 || i.nh !== 52) out.push(`the room is ${i.nw} x ${i.nh}, not the game's 144 x 52`);
      if (k !== Math.round(k) || i.h / i.nh !== k || i.px !== "pixelated") out.push(`the room is shown at ${k.toFixed(2)} times (${i.px}), not whole pixels`);
      if (w >= 561 ? i.left !== 0 : Math.abs(i.left - i.right) > 1) out.push(`the room is ${i.left}px from its picture's left edge and ${i.right}px from its right; it keeps its left wall on a wide card and is centred on a phone`);
    }
    if (m.twice.length) out.push(`a picture appears twice on the page: ${[...new Set(m.twice)].join(", ")}`);
    low(m, "dark");
    if (w >= 1001) {
      // a row's names share one baseline (1px): the tools' row and each row of shelves
      const rows = {};
      for (const c of m.cards) (rows[c.top] = rows[c.top] || []).push(c);
      for (const r of Object.values(rows)) {
        const b = r.map((c) => c.nameBottom);
        if (Math.max(...b) - Math.min(...b) > 1) out.push(`the names in the row of ${r.map((c) => c.name).join(", ")} do not share a baseline (${b.join(", ")})`);
      }
      // every count, against the page each card opens (both are counted when the site is built)
      const s = await evaluate(`(async () => {
        const page = async (u) => new DOMParser().parseFromString(await (await fetch(u)).text(), 'text/html');
        const meta = async (u) => [...(await page(u)).querySelectorAll('.pmeta span')].map((x) => x.textContent.replace(/\\s+/g, ' ').trim()).join(' · ');
        const learn = await page('learn/'), methods = [...(await page('frameworks/')).querySelectorAll('table')].find((t) => (t.querySelector('th') || {}).textContent === 'Method');
        return { learn: [...learn.querySelectorAll('.pmeta span')].map((x) => x.textContent).join(' · '), lessonOne: 'learn/' + learn.querySelector('a.ll').getAttribute('href'),
          templates: await meta('templates/'), prompts: await meta('prompts/'), pictures: await meta('pictures/'), jobs: await meta('tools/'),
          models: (([...(await page('models/')).querySelectorAll('.mnum')].pop() || {}).textContent || '').replace(/^.* of /, ''),
          methods: methods ? methods.querySelectorAll('tbody tr').length : 0,
          days: JSON.parse((await page('simulator/')).getElementById('nd-data').textContent).days.length,
          tools: ((await (await fetch('app/SkyWays-Architect.html')).text()).match(/TOOLS\\.push\\(\\{id:/g) || []).length,
          size: (await (await fetch(document.querySelector('#library img').currentSrc)).arrayBuffer()).byteLength };
      })()`);
      const there = (t, re) => +((t.match(re) || [])[1]);
      if (m.cards[1].href !== s.lessonOne) out.push(`the tutorial's card goes to ${m.cards[1].href}, not lesson one (${s.lessonOne})`);
      const pairs = [["calculators", num(0, /(\d+) calculators/), s.tools], ["lessons", num(1, /(\d+) lessons/), there(s.learn, /(\d+) lessons/)],
        ["tracks", num(1, /(\d+) tracks/), there(s.learn, /(\d+) tracks/)], ["hours", num(1, /about (\d+) hours/), there(s.learn, /about (\d+) hours/)],
        ["decisions", num(2, /(\d+) decisions/), s.days], ["templates", num(3, /(\d+) templates/), there(s.templates, /(\d+) templates/)],
        ["prompts", num(4, /(\d+) prompts/), there(s.prompts, /(\d+) prompts/)], ["rules of thumb", num(5, /(\d+) rules of thumb/), +s.models],
        ["jobs", num(6, /(\d+) jobs/), there(s.jobs, /(\d+) jobs/)], ["methods", num(7, /(\d+) methods/), s.methods],
        ["pictures", num(8, /(\d+) pictures/), there(s.pictures, /(\d+) pictures/)]];
      for (const [what, here, it] of pairs) if (!(here > 0) || here !== it) out.push(`the library counts ${here} ${what}; the page it opens counts ${it}`);
      if (!(s.size > 0 && s.size <= 4096)) out.push(`the room's picture is ${s.size} bytes; 4 KB is the most`);
      // the same grounds in the light theme, and every text 4.5:1 there too
      await theme(true);
      const l = await evaluate(LOOK);
      await theme(false);
      if (l.wb !== m.wb || l.sim !== m.sim) out.push("a tool's ground changes with the theme");
      if (l.learn !== l.paper) out.push(`in the light theme the tutorial's ground is ${l.learn}, not the lessons' paper (${l.paper})`);
      low(l, "light");
      // a hover moves the border to ink at 34% and lifts the card 3px in 250ms: a transform and a colour, nothing else
      await send("Emulation.setEmulatedMedia", { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "no-preference" }] });
      const at = await evaluate(`(() => { const c = document.querySelector('#library .shf'); c.scrollIntoView({ block: 'center', behavior: 'instant' });
        const r = c.getBoundingClientRect(), cs = getComputedStyle(c); return { x: r.left + r.width / 2, y: r.top + r.height / 2, moves: cs.transitionProperty + ' ' + cs.transitionDuration, rest: cs.borderTopColor }; })()`);
      await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: at.x, y: at.y });
      await sleep(400);
      const hover = await evaluate(`(() => { const cs = getComputedStyle(document.querySelector('#library .shf')); return { t: cs.transform, b: cs.borderTopColor }; })()`);
      await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: 2, y: 2 });
      if (at.moves !== "border-color, transform 0.25s, 0.25s") out.push(`a card moves by ${at.moves}; a transform and a colour in 250ms is all`);
      if (hover.t !== "matrix(1, 0, 0, 1, 0, -3)" || hover.b === at.rest) out.push(`a hovered card has transform ${hover.t} and border ${hover.b} (at rest ${at.rest})`);
      // on paper: the pictures are the screen's, and every word is ink on paper
      await send("Emulation.setEmulatedMedia", { media: "print", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "reduce" }] });
      await sleep(300);
      const p = await evaluate(LOOK);
      for (const t of p.texts) if (t.ink > 0.2 || t.paper < 0.8) { out.push(`in print, "${t.t}" is not ink on paper`); break; }
    } else {
      // a phone: 390, then 320
      for (const [pw, ph] of [[w, h], [320, 640]]) {
        if (pw !== w) { await send("Emulation.setDeviceMetricsOverride", { width: pw, height: ph, deviceScaleFactor: 1, mobile: true }); await sleep(400); }
        const q = pw === w ? m : await evaluate(LOOK);
        const small = q.texts.filter((t) => t.px < 11);
        if (small.length) out.push(`at ${pw}px, text under 11px: ${small.map((t) => `"${t.t}" ${t.px}px`).join(", ")}`);
        const short = q.cards.filter((c) => c.h < 44 || c.w < 44);
        if (short.length) out.push(`at ${pw}px, cards under 44px: ${short.map((c) => c.name).join(", ")}`);
        if (q.over > 0) out.push(`at ${pw}px the page scrolls sideways by ${q.over}px`);
        if (pw === 390 && q.band > 1500) out.push(`at 390px the band is ${q.band}px tall; 1,500 is the most`);
        if (q.imgs[0] && q.imgs[0].w / q.imgs[0].nw !== 2) out.push(`at ${pw}px the room is shown at ${q.imgs[0].w / q.imgs[0].nw} times, not two`);
        if (pw !== w) low(q, `${pw}px`);
      }
    }
    return out;
  }
  // end of home · H7

  // home · H8 close: #work-with-us
  async function bandH8(w, h) {
    return [];
  }
  // end of home · H8

  const BANDS = [["H3 map", bandH3], ["H4 chooser", bandH4], ["H5 people", bandH5], ["H6 day card", bandH6],
    ["H7 library", bandH7], ["H8 close", bandH8]];
  const out = [];
  thrown.length = 0;
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    for (const [name, check] of BANDS) {
      await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 600 });
      await send("Emulation.setEmulatedMedia", { media: "", features: [{ name: "prefers-color-scheme", value: "dark" },
        { name: "prefers-reduced-motion", value: "reduce" }] });
      await send("Page.navigate", { url: BASE });
      await sleep(1200);
      if (!(await evaluate(LOADED))) { out.push(`${name} at ${w} x ${h}: the page did not load`); continue; }
      for (const p of await check(w, h)) out.push(`${name} at ${w} x ${h}: ${p}`);
    }
  }
  if (thrown.length) out.push("script error: " + thrown[0]);
  if (out.length) { failures += out.length; console.log("  FAIL /  " + out.join("; ")); }
  else console.log(`  ok   /  ${BANDS.length} bands, each checked at 1440 x 900 and 390 x 844`);
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
console.log(failures ? `\n${failures} failure(s)` : "\nall eighteen passes hold");
process.exit(failures ? 1 : 0);
