// The acceptance gate for the site's pages: what must hold before a change to layout or motion ships.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/accept.mjs http://localhost:8799/
//
// Twenty passes, most over one page of each kind, in headless Chrome over the DevTools protocol (the same
// approach as shoot.mjs, so there is nothing to install):
//
//    1. no script            nothing a reader needs is left hidden (opacity 0, scaled to nothing, clipped away);
//                            the simulator shows its thirteen days as text; the home page's close is a plain link
//                            to the repository's discussions page, and the page prints no address
//    2. reduced motion       nothing hidden, and no animation running at all; the hero draws its still twice at
//                            most, and once more when the fonts arrive
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
//   13. the hero             on the home page, every moment read from the hero's own times (window.GlobeTimes):
//                            one clock (the pause holds it; a hidden tab goes on from where it was); at twelve
//                            moments and five widths the tag names the phase, the sign-off and the way back, sits
//                            8px inside the stage clear of the aircraft and the pause control, and the aircraft is
//                            30px long or more; the picture ends inside the first screen; its whole cost slowed
//                            four times against a frozen reference served in its place (frames, gaps, taps, script);
//                            61 frames a second at most when 120 are offered; it comes to rest, a later visit sooner;
//                            reduced motion draws the rest frame; the entrance plays once a sitting; the tag waits
//                            for its fonts; the rest's labels touch nothing; and the page does not shift as it is
//                            scrolled
//   14. the measure          on a lesson at 1440, no prose runs over 75 characters a line: each paragraph's
//                            characters a line, from its width and the average width of its own text in its font
//   15. two right edges      on a lesson at 1440, text stops at one right edge and pictures, tables and code at
//                            one other: every block of the page, and a caption that sits on the page, ends on
//                            one of two lines, and anything on a third is listed
//   16. the game's first paint  with script, the simulator's text for a reader without script is hidden from the
//                            first paint, while the game's own script has still not arrived; when the rules fail to
//                            load, the text comes back
//   17. the bytes            read from the built site with node's zlib (level 9): base.css under 32 KB as shipped
//                            (the build drops its comments), the game's three scripts under 46 KB, theme/hero.js
//                            under 10 KB, frame/frame.js (every page loads it) under 6 KB; every page's HTML under
//                            25 KB (the pages that were already larger on 2 October 2026 each held to its size that
//                            day, rounded up, plus one KB); the home page's HTML under 21 KB with no <style> block,
//                            and everything a first visit to it asks for, scrolled to the end, under 176 KB
//                            (council 10); the FDE guide's stylesheet under 2 KB and its hub under 22 KB; and no
//                            font file but the four the site has
//   18. every lesson         every page under learn/ in the sitemap, at 1440 x 900: the figure that holds a lesson's
//                            map (data-map, from pages/maps.py) is at most 630px tall, 70% of the screen (council 9);
//                            and on every lesson (council 10): no prose over 75 characters a line, one left edge
//                            (the breadcrumb's) and two right ones, and the guide on screen at 0, 25, 50 and 75% of
//                            the way down, within 24px of the column's right edge, marking one section (the last
//                            whose heading has passed the upper third, or the first before any has); the title in
//                            two lines, its grey continuation 3:1 or more in both themes and no hyphenated word
//                            broken; only six gaps between the blocks of the prose; no heading under 24px tracked
//                            tighter than -0.005em; and at 390 wide no table that scrolls sideways, cells at 15px,
//                            and every fold 44px tall or more
//   19. the home page        at 1440 x 900 and 390 x 844: the home verdict's order, eyebrows and headings, the page
//                            8,700px tall or less at 1440 and 13,200px at 390, and a first visit that asks for no
//                            file pass 17 leaves out; then each band's own checks, one function for each band's
//                            parcel (the map, the chooser, the people, the day card, the library, the close)
//   20. the FDE guide        on the hub and its three stages, at 1440, 1024, 390 and 320 in both themes: the
//                            framework's twelve step links each reach a step on its own stage's page; its columns
//                            carry the phases' hues and its heads ink; no sideways scroll, no text under 11px, its
//                            links 44px tall on a phone; the hub's figure within 630, 1,200 and 1,450px and a
//                            stage's figure on the first screen; 4.5:1 in the figure, the altitude table and the
//                            step blocks; nothing hidden without script, under reduced motion or on paper; and
//                            every site link on the four pages lands
//
// Every pass first checks that the page really loaded: its top bar is there and styled. Passes 1 to 4 and 8 look
// for the parts script or an animation may hide (HIDDEN); on the home page each of its parts there must be found,
// so a class renamed in the markup fails the pass instead of leaving nothing checked. It exits 1 if
// any pass fails and prints what failed. It measures; it does not judge taste: for that, look. The hero can
// be put at any second of its clock with window.GlobeAt(seconds), and site/tools/herosheet.mjs lays twelve
// moments of its flight, the rest among them, at five widths on sheets for a person to look at before a release.
//
// What it cannot see: other browsers. Nothing on the site now depends on a feature only Chrome has (the
// hero is one canvas; there are no view transitions and no CSS path animation), but Safari and Firefox are
// not run here. The globe and the simulator draw on canvases from script, which the browser's list of
// animations cannot see, so each reports for itself: window.GlobeMs (drawing time and frames), with
// window.GlobeTimes and window.GlobeState (the hero's moments, its words and where it draws them), and
// window.NDFrames (frames drawn).

import { createServer } from "node:net";
import { spawn } from "node:child_process";
import { rmSync, readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { gzipSync } from "node:zlib";
import { tmpdir, loadavg } from "node:os";
import { join } from "node:path";

const BASE = process.argv[2];
if (!BASE) { console.error("usage: node accept.mjs <site url, ending in />"); process.exit(2); }
const PAGES = ["", "method/", "product-manager/", "qa/", "protocol/", "models/", "templates/", "prompts/",
  "frameworks/", "pictures/", "learn/", "learn/fundamentals/", "learn/the-hard-gate/", "learn/p0-frame/", "simulator/",
  "labs/", "labs/grow-the-spec/", "labs/grow-the-spec/others/", "labs/write-the-system-prompt/",
  "labs/write-the-system-prompt/others/", "tools/", "tools/claude-at-the-desk/",
  "tools/chatgpt-and-codex/", "tools/google-ai-studio-and-jules/", "forward-deployed-engineer/",
  "forward-deployed-engineer/frame/"];
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

// Things that script or an animation may hide, and must have shown by now: first the home page's parts, band by
// band in the order of verdict-home 1.0, then other pages' parts.
const HOME_PARTS = [".hero2 .hx>*", ".sc-rail li",   // the hero: its words, and the rail a reader without script sees
  ".sec-h>*",                                          // each band's eyebrow, heading and line
  ".vm-p", ".vm-pl", ".vm-n", ".vm-q>li",              // the methods: the map's phase heads, shapes, notes and questions
  ".pk-c",                                             // your team: the chooser's four columns, three of them fieldsets
  ".seats a",                                          // by role
  "#tutorial .q", "#tutorial .q svg.sk>*",             // the tutorial: the four people and their drawings
  ".daycard", ".daycard *", ".dc-ex",                  // the simulator: the day card and its "Example day" pill
  ".lib .fl", ".lib .fl-p>*", ".lib .shf",             // the library: the three tools, what their pictures show, six shelves
  ".cx-in", ".cx-o>li"];                               // the close: its panel and its four offers
const OTHER_PARTS = [".tg .tile", ".roadmap .rn", "main .sec", ".dgb", ".step>summary", ".mix a", ".lc", ".lk", "[data-reveal]>*",
  "figure.fig>svg>*", ".mmg svg>*", "figure.sketch svg>*", ".prose>*"];
const HIDDEN = `(() => {
  const sel = ${JSON.stringify([...HOME_PARTS, ...OTHER_PARTS].join(","))};
  const bad = {};
  document.querySelectorAll(sel).forEach((e) => {
    const cs = getComputedStyle(e);
    let why = '';
    if (+cs.opacity < 0.05) why = 'opacity ' + cs.opacity;
    else if (cs.scale && /^0(\\s|$)/.test(cs.scale)) why = 'scaled to nothing';
    else if (/inset\\([^)]*100%/.test(cs.clipPath)) why = 'clipped away';
    if (why) {
      const cls = (e.className.baseVal ?? e.className ?? '').toString().split(' ')[0];
      const k = (cls || (e.parentElement?.className || '').toString().split(' ').pop() + ' ' + e.tagName.toLowerCase()) + ' (' + why + ')';
      bad[k] = (bad[k] || 0) + 1;
    }
  });
  return bad;
})()`;
// The guard (council 10): on the home page, its parts above that match nothing there. It is read wherever HIDDEN is
// read, so a class renamed in the markup and not here fails the pass instead of leaving that part unchecked.
const HOME = new URL(BASE).href.replace(/[?#].*$/, "");
const ON_HOME = `(location.origin + location.pathname === ${JSON.stringify(HOME)})`;
const UNMATCHED = `(${ON_HOME} ? ${JSON.stringify(HOME_PARTS)}.filter((s) => !document.querySelector(s)) : [])`;
// Everything a first visit to the home page asks for, scrolled to the end (council 10), read from the built site: the
// files index.html names that a browser fetches (its stylesheets, preloads, icon, scripts and pictures) and the fonts
// those stylesheets name. Text counts gzipped (level 9); pictures and fonts, already compressed, count as they are.
// Pass 17 holds the sum to 176 KB; the home pass checks that a first visit really asks for nothing else.
function firstVisit() {
  const site = new URL("../_site/", import.meta.url).pathname, html = readFileSync(site + "index.html", "utf8"), files = new Set(["index.html"]);
  const local = (u, from) => { const x = new URL(u, "http://site/" + from); return x.origin === "http://site" ? decodeURIComponent(x.pathname.slice(1)) : null; };
  for (const [t, tag] of html.matchAll(/<(link|script|img|source|video|audio)\b[^>]*>/gi)) {
    if (/^link$/i.test(tag) && !/\srel="[^"]*\b(stylesheet|icon|preload|modulepreload|manifest)\b/i.test(t)) continue;
    for (const [, u] of t.matchAll(/\s(?:href|src|poster)="([^"]+)"/gi)) { const f = local(u, ""); if (f) files.add(f); }
  }
  for (const css of [...files].filter((f) => f.endsWith(".css") && existsSync(site + f))) {
    for (const [, u] of readFileSync(site + css, "utf8").matchAll(/url\(\s*["']?([^"')]+?\.(?:woff2?|ttf|otf)(?:[?#][^"')]*)?)["']?\s*\)/gi)) {
      const f = local(u, css); if (f) files.add(f);
    }
  }
  const missing = [...files].filter((f) => !existsSync(site + f));
  const size = (f) => { const b = readFileSync(site + f); return /\.(png|jpe?g|gif|webp|avif|woff2?)$/i.test(f) ? b.length : gzipSync(b, { level: 9 }).length; };
  return { files: [...files], missing, bytes: [...files].filter((f) => !missing.includes(f)).reduce((n, f) => n + size(f), 0) };
}
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
// what HIDDEN finds, as a pass's failures; and on the home page, each of its parts that is no longer there (the guard)
const hidden = async (say = "hidden", expr = HIDDEN) => {
  const h = await evaluate(expr), gone = await evaluate(UNMATCHED);
  return [...(Object.keys(h).length ? [`${say}: ${list(h)}`] : []),
    ...(gone.length ? [`nothing on the home page matches ${gone.join(", ")}, which HIDDEN looks for there`] : [])];
};

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
// the home page's close for a reader without script (council 10, H8): its one button a plain link to the repository's
// discussions page, shown, and no address printed anywhere in the page
const CLOSE = `(() => { if (!${ON_HOME}) return null;
  const a = document.querySelector('#work-with-us .btn'), r = a ? a.getBoundingClientRect() : null;
  return { href: a ? a.getAttribute('href') : '', shown: !!r && r.width > 0 && r.height > 0 && getComputedStyle(a).visibility !== 'hidden',
    mailto: document.documentElement.outerHTML.includes('mailto:') }; })()`;
await pass("1. no script: nothing left hidden", { width: 1280, height: 800, noscript: true, wait: 3200 }, async () => {
  const out = await hidden();
  if ((await evaluate(PLAIN)) === false) out.push("without script the thirteen days as text are not shown");
  const c = await evaluate(CLOSE);
  if (c) {
    if (!/^https:\/\/github\.com\/[^/]+\/[^/]+\/discussions\/?$/.test(c.href)) out.push(`without script the close's button goes to "${c.href}", not the repository's discussions page`);
    if (!c.shown) out.push("without script the close's button is not shown");
    if (c.mailto) out.push("the home page carries a mailto: address");
  }
  return out;
});
await pass("2. reduced motion: nothing hidden, nothing running", { width: 1280, height: 800, reduce: true }, async () => {
  const out = await hidden();
  const r = await evaluate(RUNNING);
  if (Object.keys(r).length) out.push("running: " + list(r));
  const f = await evaluate(FRAMES);
  if (f > 0) out.push(`the canvas drew ${f} frames`);
  const g = await evaluate("window.GlobeMs ? window.GlobeMs.n : 0"); if (g > 3) out.push(`the globe drew ${g} frames; its still is drawn twice at most, and once more when the fonts arrive`);
  return out;
});
await pass("3. motion allowed: nothing waits for an animation", { width: 1280, height: 800, wait: 700 }, async () => {
  const out = await hidden("hidden 700ms after load");   // the whole page, unscrolled
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
  await evaluate(SCROLL_THROUGH);
  const out = await hidden();
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
  return hidden("hidden", paper);
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

// 13. the hero, on the home page only. Council 10 staged the flight like a launch, gave it words and a rest, and
// asked the gate to see its words, its fit and its whole cost. Every moment is read from the hero's own times
// (window.GlobeTimes: the lap, the launch's wait, P1, the sign-off's bar, P3, behind the Earth, the rest, and whether
// the entrance played), never typed in, so a change to the flight's timing moves the checks with it. What it draws
// is read from window.GlobeState (the tag's words and box, the aircraft's box and length, the rest's labels and
// forms; boxes in css px from the canvas's top left); the pause control is measured on the page. Each finding
// carries the number of its check.
console.log("\n13. the hero: one clock; its words, fit and size at twelve moments; its whole cost; the rest");
{
  const out = [], said = [];
  const fail = (k, s) => { const m = `${k}. ${s}`; if (!out.includes(m)) out.push(m); };
  thrown.length = 0;
  const MOTION = { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "no-preference" }] };
  const STILL = { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "reduce" }] };
  const screen = async (w, h, dpr = 1, media = MOTION) => {
    await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: dpr, mobile: w < 600 });
    await send("Emulation.setEmulatedMedia", media);
  };
  const cpu = (rate) => send("Emulation.setCPUThrottlingRate", { rate });
  const frames = () => evaluate("window.GlobeMs ? window.GlobeMs.n : -1");
  const BOX = "document.querySelector('.hero2 [data-motion-toggle]')";
  const tick = (on) => evaluate(`(() => { const b = ${BOX}; if (!b) return false; b.checked = ${on}; b.dispatchEvent(new Event('change', { bubbles: true })); return true; })()`);
  const isBox = (a) => Array.isArray(a) && a.length === 4 && a.every((v) => typeof v === "number");
  // two boxes overlap by more than a pixel each way (a pixel is left for rounding)
  const hits = (a, b) => isBox(a) && isBox(b) && Math.min(a[0] + a[2], b[0] + b[2]) - Math.max(a[0], b[0]) > 1 && Math.min(a[1] + a[3], b[1] + b[3]) - Math.max(a[1], b[1]) > 1;
  // where the stage can be seen (the canvas, inside the screen's width and any box that clips it), and the pause control
  const STAGE = `(() => { const c = document.querySelector('[data-globe]'), r = c.getBoundingClientRect();
    let L = Math.max(r.left, 0), R = Math.min(r.right, document.documentElement.clientWidth), T = r.top, B = r.bottom;
    for (let e = c.parentElement; e && e !== document.documentElement; e = e.parentElement) { const cs = getComputedStyle(e), q = e.getBoundingClientRect();
      if (cs.overflowX !== 'visible') { L = Math.max(L, q.left); R = Math.min(R, q.right); }
      if (cs.overflowY !== 'visible') { T = Math.max(T, q.top); B = Math.min(B, q.bottom); } }
    const p = ${BOX}, pb = p && (p.closest('.mpause') || p).getBoundingClientRect();
    return { w: r.width, edge: [L - r.left, T - r.top, R - r.left, B - r.top], pause: pb && pb.width ? [pb.left - r.left, pb.top - r.top, pb.width, pb.height] : null }; })()`;
  // A visit to the home page. A first visit in the sitting plays the entrance (the head's script finds nothing in
  // sessionStorage); a later one does not. It returns once the hero has drawn its first frame.
  let fresh = null;
  const hooks = [];
  async function visit(first) {
    if (first && fresh === null) fresh = (await send("Page.addScriptToEvaluateOnNewDocument", { source: "try { sessionStorage.removeItem('hero') } catch (e) {}" })).identifier;
    if (!first && fresh !== null) { await send("Page.removeScriptToEvaluateOnNewDocument", { identifier: fresh }); fresh = null; }
    await evaluate("window.__left = true");
    await send("Page.navigate", { url: BASE });
    for (let i = 0; i < 160; i++) {
      await sleep(50);
      if (await evaluate("!window.__left && !!window.GlobeMs && window.GlobeMs.n > 0").catch(() => false)) return true;
    }
    return false;
  }
  const hook = async (source) => { const { identifier } = await send("Page.addScriptToEvaluateOnNewDocument", { source }); hooks.push(identifier); return identifier; };
  const unhook = async (id) => { await send("Page.removeScriptToEvaluateOnNewDocument", { identifier: id }); hooks.splice(hooks.indexOf(id), 1); };
  try {
    // 1. One clock. Running, it draws; paused, it holds (its frames and its clock); unpaused, it draws again. A tab
    // hidden (the gate brings a second tab to the front) draws nothing, and shown again it goes on from where it was.
    await screen(1280, 800);
    if (!(await visit(false))) fail(1, "the hero drew nothing");
    else {
      await sleep(900);
      let a = await frames(); await sleep(500); let b = await frames();
      if (b - a < 10) fail(1, `running, it drew ${b - a} frames in half a second`);
      await tick(true); await sleep(200);
      a = await frames(); const c0 = await evaluate("window.GlobeState ? window.GlobeState.clock : null"); await sleep(500);
      b = await frames(); const c1 = await evaluate("window.GlobeState ? window.GlobeState.clock : null");
      if (b !== a) fail(1, `paused, it drew ${b - a} frames in half a second`);
      if (c1 !== c0) fail(1, `paused, its clock moved from ${c0} to ${c1}`);
      await tick(false); await sleep(200);
      a = await frames(); await sleep(500); b = await frames();
      if (b - a < 10) fail(1, `unpaused, it drew ${b - a} frames in half a second`);
      const DEV = `http://127.0.0.1:${PORT}/json`;
      const me = (await (await fetch(`${DEV}/list`)).json()).find((t) => t.id === ws.url.split("/").pop());
      if (!me) throw new Error("the gate could not find its own tab to bring back");
      const other = await (await fetch(`${DEV}/new?about:blank`, { method: "PUT" })).json();
      const before = await evaluate("window.GlobeState ? window.GlobeState.clock : null");
      await fetch(`${DEV}/activate/${other.id}`); await sleep(300);
      const hidden = await evaluate("document.hidden"), h0 = await frames(); await sleep(1500); const h1 = await frames();
      await fetch(`${DEV}/activate/${me.id}`); await sleep(600);
      const after = await evaluate("window.GlobeState ? window.GlobeState.clock : null"), h2 = await frames();
      await fetch(`${DEV}/close/${other.id}`);
      if (!hidden) fail(1, "the gate could not hide the tab");
      else if (h1 !== h0) fail(1, `in a hidden tab it drew ${h1 - h0} frames in 1.5 seconds`);
      if (h2 - h1 < 10) fail(1, `shown again, it drew ${h2 - h1} frames in 0.6 seconds`);
      if (typeof before !== "number" || typeof after !== "number") fail(1, "the hero does not report its clock (window.GlobeState.clock)");
      else if (after - before > 1.4 || after - before < 0.2) fail(1, `hidden for 1.8 seconds and shown for 0.6, its clock went from ${before} to ${after}: it did not go on from where it was`);
    }

    // 2 to 5 and 12, at five widths, each a first visit (the camera's close shot is part of round one), paused, its
    // clock put at each moment with window.GlobeAt. Twelve moments of a round, built from the hero's own times, each
    // with the words its tag must start with: the sign-off's from 0.3s before the bar to 1.3s after it (each edge tried
    // from both sides), "Back to Frame" behind the Earth. The last is round two's P0, at the whole view, where the dart
    // is drawn at the size a reader keeps.
    const MOMENTS = (T) => [[T.pre + 0.6, "P0"], [T.p1 + 0.5, "P1"], [T.gate - 0.6, "P1"], [T.gate - 0.2, "Sign-off"],
      [T.gate + 0.5, "Sign-off"], [T.gate + 1.15, "Sign-off"], [T.gate + 1.5, "P2"], [T.p3 - 1, "P2"], [T.p3 + 0.5, "P3"],
      [T.back - 1, "P3"], [T.back + 1.5, "Back to Frame"], [T.lap + 1, "P0"]];
    const WHERE = ["in P0", "in P1", "in P2", "in P3", "behind the Earth"];
    const LABELS = ["P0's name", "P1's name", "P2's name", "P3's name", "the sign-off's label", "the way back's label"], FORMS = ["the dart", "the drawing", "the airliner", "the jet"];
    let small = null;
    const ends = [];
    for (const [w, h] of [[1440, 900], [1024, 768], [768, 1024], [390, 844], [320, 640]]) {
      await screen(w, h);
      if (!(await visit(true))) { fail(2, `at ${w}px the hero drew nothing`); continue; }
      await sleep(600);
      await tick(true);
      // 5. the picture ends inside the first screen on a phone and a laptop, and nothing scrolls sideways
      const fold = await evaluate(`(() => { const b = (s) => { const e = document.querySelector(s); return e ? e.getBoundingClientRect().bottom : 0; };
        return { end: Math.round(Math.max(b('.hero2 .scene'), b('.hero2 .sc-stage'))), over: document.documentElement.scrollWidth - document.documentElement.clientWidth }; })()`);
      if ((w === 1440 || w === 390) && fold.end > h) fail(5, `at ${w} x ${h} the picture ends at ${fold.end}px, below the first screen`);
      if (w === 1440 || w === 390) ends.push(`${fold.end}px at ${w} x ${h}`);
      if (fold.over > 0) fail(5, `at ${w}px the page scrolls sideways by ${fold.over}px`);
      const T = await evaluate("window.GlobeTimes || null");
      if (!T || (await evaluate("typeof window.GlobeAt")) !== "function") {
        for (const k of [2, 3, 4, 12]) fail(k, "the hero publishes no times, or no clock to set (window.GlobeTimes, window.GlobeAt)");
        continue;
      }
      let least = null;
      for (const [t, want] of MOMENTS(T)) {
        const m = await evaluate(`(() => { const leg = window.GlobeAt(${t.toFixed(3)}), s = window.GlobeState || {};
          return { leg, tag: s.tag, box: s.box, craft: s.craft, len: s.len, stage: ${STAGE} }; })()`);
        const at = `at ${w}px, ${t.toFixed(2)}s`, leg = want === "Sign-off" ? (t < T.gate ? 1 : 2) : want === "Back to Frame" ? 4 : +want[1];
        // 2. the words, and the hero's times they are read against
        if (m.leg !== leg) fail(2, `${at}: GlobeTimes put the aircraft ${WHERE[leg]}, but it is ${WHERE[m.leg] || m.leg}`);
        if (typeof m.tag !== "string") fail(2, "the hero reports no tag (window.GlobeState.tag)");
        else if (!m.tag.startsWith(want)) fail(2, `${at}: the tag says "${m.tag}"; "${want}" is due`);
        // 3. the tag sits 8px inside the stage, clear of the aircraft and of the pause control
        if (m.tag && !isBox(m.box)) fail(3, `${at}: the tag has no box (GlobeState.box)`);
        else if (isBox(m.box)) {
          const [x, y, bw, bh] = m.box, e = m.stage.edge, room = Math.round(Math.min(x - e[0], y - e[1], e[2] - x - bw, e[3] - y - bh));
          if (room < 8) fail(3, `${at}: the tag is ${room}px from the stage's edge; 8 is the least`);
          if (!isBox(m.craft)) fail(3, "the hero reports no box for the aircraft (GlobeState.craft)");
          else if (hits(m.box, m.craft)) fail(3, `${at}: the tag covers the aircraft`);
          if (hits(m.box, m.stage.pause)) fail(3, `${at}: the tag runs under the pause control`);
        }
        // 4. the aircraft's length, in front of the Earth (behind it, it is drawn smaller and dimmed)
        if (m.leg >= 0 && m.leg < 4) {
          if (typeof m.len !== "number") fail(4, "the hero reports no length for the aircraft (window.GlobeState.len)");
          else if (!least || m.len < least.len) least = { len: m.len, at };
        }
      }
      if (least && least.len < 30) fail(4, `${least.at}: the aircraft is ${least.len}px long; 30 is the least`);
      if (least && (!small || least.len < small.len)) small = least;
      // 12. at rest, in both themes, no two of the labels, the forms and the pause control overlap
      for (const theme of ["dark", "light"]) {
        const r = await evaluate(`(async () => { document.documentElement.setAttribute('data-theme', '${theme}');
          await new Promise((ok) => requestAnimationFrame(() => setTimeout(ok, 30)));
          window.GlobeAt(${(T.rest + 2).toFixed(2)}); const s = window.GlobeState || {};
          return { rest: s.rest, labels: s.labels, forms: s.forms, stage: ${STAGE} }; })()`);
        const k = `at ${w}px in the ${theme} theme, at rest`;
        if (r.rest !== 1) fail(12, `${k} GlobeState.rest is ${r.rest}`);
        if (!Array.isArray(r.labels) || !Array.isArray(r.forms)) { fail(12, "the hero reports no rest labels or forms (window.GlobeState.labels, .forms)"); continue; }
        const due = r.stage.w >= 400 ? 6 : 4;
        if (r.labels.length !== due) fail(12, `${k} it names ${r.labels.length} things; ${due} are due on a stage ${Math.round(r.stage.w)}px wide`);
        if (r.forms.length !== 4) fail(12, `${k} it parks ${r.forms.length} forms; 4 are due`);
        const all = [...r.labels.map((b, i) => [LABELS[i] || `label ${i + 1}`, b]), ...r.forms.map((b, i) => [FORMS[i] || `form ${i + 1}`, b])];
        const e = r.stage.edge;
        for (const [name, b] of all) {
          if (!isBox(b)) fail(12, `${k} ${name} has no box`);
          else if (b[0] < e[0] || b[1] < e[1] || b[0] + b[2] > e[2] || b[1] + b[3] > e[3]) fail(12, `${k} ${name} runs past the stage's edge`);
        }
        all.push(["the pause control", r.stage.pause]);
        for (let i = 0; i < all.length; i++) for (let j = i + 1; j < all.length; j++) if (hits(all[i][1], all[j][1])) fail(12, `${k} ${all[i][0]} and ${all[j][0]} overlap`);
      }
      await evaluate("document.documentElement.removeAttribute('data-theme'); true");
    }
    if (ends.length) said.push(`the picture ends at ${ends.join(" and ")}`);
    if (small) said.push(`the aircraft at least ${small.len}px (${small.at.replace(/, .*/, "")})`);

    // 6. The whole cost, against a frozen reference. An absolute floor measures the host, not the hero: on 3 October
    // 2026 the machine under the gate changed and the same code lost a third of its frames. So every measurement runs
    // in the same pass, at the same settings, once with the hero and once with today's hero of 2 October 2026 served in
    // its place (tools/reference/hero-2026-10-02.js, through Fetch, as pass 16 holds back game.js), interleaved
    // (reference, hero, reference, hero) so that a drift on the host falls on both. At 1280 x 800 and at 390 x 844 at
    // scale 3, slowed four times, in the first four seconds of a first visit (once the page has loaded and its fonts
    // are in, as the council measured) and in steady flight (P2 for each): the hero draws at least 90% of the
    // reference's frames; its worst gap between frames is at most the reference's plus 50ms; a tap on the headline
    // waits at most 100ms, or the reference's worst plus 30ms; and its script a frame is at most 1.25 times the
    // reference's (the council's 6ms stood against today's 4.8ms). The council's absolute numbers (72 frames, 100ms,
    // 6ms) are printed beside each line for information, with the host's load and the reference's script a frame
    // unthrottled, which shows the host's speed (0.92ms where the council set the bars). Frames come on the display's
    // ticks (16.7ms), so gaps and taps are read to the whole millisecond. The page's heap is collected before each
    // window: without it, a run that follows the hero's paid for the hero's garbage (measured 3 October 2026: the
    // reference drew 89 to 96 frames after a run of itself and 63 to 71 after a run of the hero).
    const WATCH = `(() => { const R = window.__cost = { t: [], s: [], taps: [], n0: window.GlobeMs.n, sum0: window.GlobeMs.sum, t0: performance.now(), on: true };
      let last = window.GlobeMs.n, sum = window.GlobeMs.sum;
      const loop = (ts) => { if (!R.on) return; const g = window.GlobeMs; if (g.n !== last) { R.t.push(ts); R.s.push(g.sum - sum); last = g.n; sum = g.sum; } requestAnimationFrame(loop); };
      requestAnimationFrame(loop);
      R.tap = (e) => R.taps.push(performance.now() - e.timeStamp);
      document.querySelector('.hero2 h1').addEventListener('pointerdown', R.tap);
      const h = document.querySelector('.hero2 h1').getBoundingClientRect(); return [h.left + h.width / 2, h.top + h.height / 2]; })()`;
    const READ = `(() => { const R = window.__cost; R.on = false; document.querySelector('.hero2 h1').removeEventListener('pointerdown', R.tap);
      const end = R.t0 + 3000, t = [R.t0, ...R.t.filter((x) => x <= end), end]; let gap = 0, at = 0;
      for (let i = 1; i < t.length; i++) if (t[i] - t[i - 1] > gap) { gap = t[i] - t[i - 1]; at = i; }
      const n = window.GlobeMs.n - R.n0, own = at < t.length - 1 ? R.s[at - 1] : null;
      return { frames: t.length - 2, gap: Math.round(gap), own, ms: n > 0 ? (window.GlobeMs.sum - R.sum0) / n : null, taps: R.taps.length, tap: R.taps.length ? Math.round(Math.max(...R.taps)) : null }; })()`;
    async function cost() {
      const [x, y] = await evaluate(WATCH), t0 = Date.now();
      for (let i = 0; i < 12; i++) {
        await send("Input.dispatchMouseEvent", { type: "mousePressed", x, y, button: "left", clickCount: 1 });
        await send("Input.dispatchMouseEvent", { type: "mouseReleased", x, y, button: "left", clickCount: 1 });
        await sleep(Math.max(0, (i + 1) * 240 - (Date.now() - t0)));
      }
      await sleep(Math.max(0, 3150 - (Date.now() - t0)));
      return evaluate(READ);
    }
    const REFERENCE = readFileSync(new URL("reference/hero-2026-10-02.js", import.meta.url)).toString("base64");
    const REF_STEADY = 12;          // the reference's steady flight: its P2 runs from 11 to about 15.5s of its 27s lap
    let swap = false;
    const serve = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.method !== "Fetch.requestPaused" || !/\/theme\/hero\.js/.test(m.params.request.url)) return;
      (swap ? send("Fetch.fulfillRequest", { requestId: m.params.requestId, responseCode: 200, body: REFERENCE,
        responseHeaders: [{ name: "Content-Type", value: "text/javascript" }] }) : send("Fetch.continueRequest", { requestId: m.params.requestId })).catch(() => {});
    };
    ws.addEventListener("message", serve);
    await send("Network.setCacheDisabled", { cacheDisabled: true });       // every load asks for theme/hero.js
    await send("Fetch.enable", { patterns: [{ urlPattern: "*theme/hero.js*", requestStage: "Request" }] });
    async function slowed(w, h, dpr, ref) {
      swap = ref;
      await cpu(1); await screen(w, h, dpr);
      if (!(await visit(true))) return null;
      await evaluate("document.fonts.ready.then(() => new Promise((ok) => (document.readyState === 'complete' ? ok() : addEventListener('load', ok, { once: true })))).then(() => true)");
      const load = loadavg()[0];
      await send("HeapProfiler.collectGarbage");          // each window starts from a collected heap: no run pays for the one before
      await cpu(4);
      const first = await cost();
      const T = ref ? null : await evaluate("window.GlobeTimes || null");
      await evaluate(`window.GlobeAt(${(T ? T.gate + 3 : REF_STEADY).toFixed(2)}); true`);   // steady flight, in P2
      await cpu(1); await send("HeapProfiler.collectGarbage"); await cpu(4);
      const steady = await cost();
      await cpu(1);
      first.load = steady.load = Math.max(load, loadavg()[0]);
      return [first, steady];
    }
    // the host's speed: the reference's script a frame unthrottled, in steady flight at 1280 x 800
    let host = null;
    swap = true; await cpu(1); await screen(1280, 800);
    if (await visit(false)) {
      await sleep(600); await evaluate(`window.GlobeAt(${REF_STEADY}); true`);
      const NOW = "({ n: window.GlobeMs.n, s: window.GlobeMs.sum })", a = await evaluate(NOW); await sleep(1500); const b = await evaluate(NOW);
      if (b.n > a.n) host = (b.s - a.s) / (b.n - a.n);
    }
    const mean = (a) => { const v = a.filter((x) => typeof x === "number"); return v.length ? v.reduce((p, q) => p + q, 0) / v.length : null; };
    for (const [w, h, dpr] of [[1280, 800, 1], [390, 844, 3]]) {
      const where = `at ${w} x ${h}${dpr > 1 ? ` at scale ${dpr}` : ""}, slowed four times`;
      const runs = { ref: [], hero: [] };
      for (const k of ["ref", "hero", "ref", "hero"]) { const r = await slowed(w, h, dpr, k === "ref"); if (r) runs[k].push(r); }
      if (runs.ref.length < 2 || runs.hero.length < 2) { fail(6, `${where}: ${runs.hero.length < 2 ? "the hero" : "the reference"} drew nothing`); continue; }
      const got = [];
      ["in the first four seconds", "in steady flight"].forEach((phase, i) => {
        const H = runs.hero.map((r) => r[i]), R = runs.ref.map((r) => r[i]), at = `${where}, ${phase}`;
        const hf = H[0].frames + H[1].frames, rf = R[0].frames + R[1].frames, ratio = rf ? hf / rf : 0;
        const worst = H[0].gap >= H[1].gap ? H[0] : H[1], hg = worst.gap, rg = Math.max(R[0].gap, R[1].gap);
        const ht = Math.max(H[0].tap ?? 0, H[1].tap ?? 0), rt = Math.max(R[0].tap ?? 0, R[1].tap ?? 0);
        const hms = mean(H.map((r) => r.ms)), rms = mean(R.map((r) => r.ms));
        if (ratio < 0.9) fail(6, `${at}: the hero drew ${H[0].frames} and ${H[1].frames} frames to the reference's ${R[0].frames} and ${R[1].frames}, ${ratio.toFixed(2)} of them; 0.9 is the least`);
        if (hg > rg + 50) fail(6, `${at}: its worst gap between frames is ${hg}ms (its own script ${worst.own === null ? "-" : worst.own.toFixed(1)}ms of it), the reference's ${rg}ms; ${rg + 50} is the most`);
        if (H.some((r) => r.taps < 12)) fail(6, `${at}: only ${Math.min(H[0].taps, H[1].taps)} of twelve taps on the headline arrived`);
        else if (ht > Math.max(100, rt + 30)) fail(6, `${at}: a tap on the headline waited ${ht}ms, the reference's worst ${rt}ms; ${Math.max(100, rt + 30)} is the most`);
        if (hms === null) fail(6, `${at}: no frame was drawn`);
        else if (rms && hms > 1.25 * rms) fail(6, `${at}: its script takes ${hms.toFixed(1)}ms a frame, the reference's ${rms.toFixed(1)}; ${(1.25 * rms).toFixed(1)} is the most`);
        got.push(`${i ? "steady" : "first four seconds"}: frames ${H[0].frames}+${H[1].frames} to ${R[0].frames}+${R[1].frames} (${ratio.toFixed(2)}), worst gap ${hg} to ${rg}ms, tap ${ht} to ${rt}ms, ` +
          `script ${hms === null ? "-" : hms.toFixed(1)} to ${rms === null ? "-" : rms.toFixed(1)}ms`);
      });
      const load = Math.max(...[...runs.ref, ...runs.hero].map((r) => r[0].load));
      said.push(`${w}${dpr > 1 ? "@" + dpr : ""} at 4x, hero to reference: ${got.join("; ")} (the council's absolute bars: 72 frames, 100ms, 6ms; load up to ${load.toFixed(1)})`);
    }
    said.push(`the reference's script a frame unthrottled at 1280: ${host === null ? "-" : host.toFixed(2)}ms on this host (0.92 where the council set the bars)`);
    await send("Fetch.disable");
    ws.removeEventListener("message", serve);
    await send("Network.setCacheDisabled", { cacheDisabled: false });
    held.length = 0;

    // 7. A display that offers 120 frames a second: before the page's scripts run, requestAnimationFrame is replaced by
    // a timer that calls back every 8.3ms. The hero may draw 61 a second at most.
    await screen(1280, 800);
    const fast = await hook(`(() => { const P = 1000 / 120, q = new Map(); let id = 0; window.__offered = 0;
      window.requestAnimationFrame = (cb) => { const t = performance.now(), h = ++id;
        q.set(h, setTimeout(() => { q.delete(h); window.__offered++; cb(performance.now()); }, Math.max(0, Math.ceil((t + 0.5) / P) * P - t))); return h; };
      window.cancelAnimationFrame = (h) => { clearTimeout(q.get(h)); q.delete(h); }; })();`);
    if (!(await visit(false))) fail(7, "the hero drew nothing");
    else {
      await sleep(1000);
      const NOW = "({ n: window.GlobeMs.n, o: window.__offered, t: performance.now() })";
      const a = await evaluate(NOW); await sleep(2000); const b = await evaluate(NOW);
      const s = (b.t - a.t) / 1000, offered = (b.o - a.o) / s, drawn = (b.n - a.n) / s;
      if (drawn > 61) fail(7, `offered ${Math.round(offered)} frames a second, it drew ${Math.round(drawn)}; 61 is the most`);
      else if (offered < 80) fail(7, `the gate could offer only ${Math.round(offered)} frames a second, too few to see a cap`);
      said.push(`offered ${Math.round(offered)} frames a second, it drew ${Math.round(drawn)}`);
    }
    await unhook(fast);

    // 8 and 10. The rest, in real time. A first visit in the sitting plays the entrance (GlobeTimes.launch) and rests
    // by GlobeTimes.rest plus 2s, within a minute of its first frame: the pause control is ticked, no frame is drawn
    // in the next second and the main thread is all but idle; unticked, it flies again. A second load in the same tab
    // does not play the entrance, and rests within 30 seconds of its first frame. A hero without times is given the
    // whole minute, and half of it.
    await send("Performance.enable");
    const busy = async () => (await send("Performance.getMetrics")).metrics.find((m) => m.name === "TaskDuration").value;
    const rests = [];
    for (const [first, most] of [[true, 60], [false, 30]]) {
      const k = first ? "a first visit" : "a later visit";
      await screen(1280, 800);
      if (!(await visit(first))) { fail(8, `${k}: the hero drew nothing`); rests.push("-"); continue; }
      const t0 = Date.now(), T = await evaluate("window.GlobeTimes || null");
      if (!T) fail(10, "the hero publishes no times (window.GlobeTimes)");
      else if (T.launch !== first) fail(10, `${k} has GlobeTimes.launch ${T.launch}`);
      const due = T ? T.rest + 2 : most;
      if (due > most) fail(8, `${k} comes to rest at ${T.rest}s; it must be still within ${most}s of its first frame`);
      await sleep(Math.max(0, Math.min(due, most + 2) * 1000 - (Date.now() - t0)));
      // the hero's clock runs on drawn frames, and on a busy machine it can fall behind the wall's: wait for it, within the budget
      for (let i = 0; i < 40; i++) {
        const c = await evaluate("window.GlobeState ? [window.GlobeState.clock, window.GlobeState.rest] : null");
        if (!c || c[1] === 1 || c[0] >= due || Date.now() - t0 > (most + 2) * 1000) break;
        await sleep(250);
      }
      const s = await evaluate("window.GlobeState || null"), on = await evaluate(`(() => { const b = ${BOX}; return b ? b.checked : null; })()`);
      const n0 = await frames(), b0 = await busy(), c0 = Date.now(); await sleep(1000);
      const n1 = await frames(), share = (await busy() - b0) / ((Date.now() - c0) / 1000);
      const when = `${k}, ${due.toFixed(1)}s after its first frame`;
      if (!s || s.rest !== 1) fail(8, `${when}: GlobeState.rest is ${s ? s.rest : "missing"}`);
      if (on !== true) fail(8, `${when}: the pause control is not ticked`);
      if (n1 !== n0) fail(8, `${when}: it drew ${n1 - n0} frames in the next second`);
      if (share > 0.05) fail(8, `${when}: the main thread is ${Math.round(share * 100)}% busy; 5% is the most at rest`);
      if (first) {
        await tick(false); await sleep(200);
        const a = await frames(); await sleep(500); const b = await frames();
        if (b - a < 10) fail(8, `unticked at rest, it drew ${b - a} frames in half a second`);
      }
      rests.push(T ? `${T.rest}s` : "-");
    }
    await send("Performance.disable");
    said.push(`it rests at ${rests[0]}, and at ${rests[1]} on a later visit`);

    // 9. Reduced motion: the rest frame drawn once (twice at most, and once more when a font arrives after the first
    // frame), and no pause control.
    await screen(1280, 800, 1, STILL);
    const late = await hook("window.__late = 0; document.fonts.addEventListener('loadingdone', () => { if (window.GlobeMs && window.GlobeMs.n > 0) window.__late = 1; });");
    if (!(await visit(false))) fail(9, "under reduced motion the hero drew nothing");
    else {
      await sleep(3000);
      const r = await evaluate(`({ n: window.GlobeMs.n, late: window.__late, s: window.GlobeState || null,
        shown: (() => { const p = ${BOX}, e = p && (p.closest('.mpause') || p); return !!e && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().width > 0; })() })`);
      if (r.n > 2 + r.late) fail(9, `under reduced motion it drew ${r.n} frames in three seconds; ${2 + r.late} is the most${r.late ? ", one of them for a font that arrived" : ""}`);
      if (!r.s || r.s.rest !== 1) fail(9, `under reduced motion GlobeState.rest is ${r.s ? r.s.rest : "missing"}: the still is not the rest frame`);
      if (r.shown || (r.s && r.s.pause)) fail(9, "under reduced motion a pause control shows");
    }
    await unhook(late);

    // 11. The tag waits for its fonts. With the two Geist files held back (and no cache), a first visit flies without
    // a tag; let go, the fonts arrive and the tag is drawn.
    await screen(1280, 800);
    await send("Network.setCacheDisabled", { cacheDisabled: true });
    held.length = 0;
    await send("Fetch.enable", { patterns: [{ urlPattern: "*fonts/geist*", requestStage: "Request" }] });
    const READY = `(document.fonts.check('600 14px Geist') && document.fonts.check("600 12px 'Geist Mono'"))`;
    const flew = await visit(true);
    await sleep(1500);
    const early = await evaluate(`({ ready: ${READY}, s: window.GlobeState || null })`), asked = held.length;
    for (const p of held.splice(0)) await send("Fetch.continueRequest", { requestId: p.requestId });
    await send("Fetch.disable");
    let ready = false;
    for (let i = 0; i < 30 && !ready; i++) { await sleep(100); ready = await evaluate(READY); }
    await sleep(600);
    const later = await evaluate("window.GlobeState || null");
    await send("Network.setCacheDisabled", { cacheDisabled: false });
    if (!flew) fail(11, "with its fonts held back the hero drew nothing");
    else if (!asked) fail(11, "no Geist font was asked for while the gate held them, so the wait could not be seen");
    else if (early.ready) fail(11, "the fonts were ready although the gate held them back");
    else if (!early.s) fail(11, "the hero reports no tag (window.GlobeState)");
    else {
      if (early.s.tag) fail(11, `the tag ("${early.s.tag}") was drawn before its fonts were ready`);
      if (!ready) fail(11, "let go, the fonts were still not ready after three seconds");
      else if (!later || !later.tag) fail(11, "the fonts arrived and no tag was drawn");
    }

    // 13. Nothing moves the page under the reader while it scrolls.
    await screen(1280, 800);
    await visit(false);
    await sleep(2000);
    const shift = await evaluate(`(async () => { let cls = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
      const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 500) { scrollTo({ top: y, behavior: 'instant' }); await new Promise((r) => setTimeout(r, 120)); }
      await new Promise((r) => setTimeout(r, 600)); return cls; })()`);
    if (shift > 0.05) fail(13, `the page shifts by ${shift.toFixed(3)} as it is scrolled; 0.05 is the most`);
  } catch (e) {
    out.push(`the pass could not finish: ${e.message}`);
  } finally {
    await cpu(1).catch(() => {});
    await send("Fetch.disable").catch(() => {});
    await send("Network.setCacheDisabled", { cacheDisabled: false }).catch(() => {});
    for (const id of [...hooks, ...(fresh === null ? [] : [fresh])]) await send("Page.removeScriptToEvaluateOnNewDocument", { identifier: id }).catch(() => {});
  }
  if (thrown.length) out.push("script error: " + thrown[0]);
  if (out.length) {
    failures += out.length;
    // by check, at most four findings each
    const by = new Map();
    for (const m of out) { const k = /^\d+\./.test(m) ? +m.split(".")[0] : 99; by.set(k, [...(by.get(k) || []), m]); }
    for (const k of [...by.keys()].sort((a, b) => a - b)) {
      by.get(k).slice(0, 4).forEach((m) => console.log("  FAIL /  " + m));
      if (by.get(k).length > 4) console.log(`         and ${by.get(k).length - 4} more like them`);
    }
  } else console.log("  ok   /");
  if (said.length) console.log("       " + said.join("; "));
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
  if (prose) items.push(...prose.children);
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
console.log("\n17. the bytes: base.css, the scripts, every page's HTML, the home page's first visit, the fonts");
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
    const hero = kb("theme/hero.js"); if (hero >= 10) out.push(`theme/hero.js is ${hero.toFixed(1)} KB gzipped; the budget is 10 (council 10)`);
    // build.py --shots writes two sheets for the shooting tools (learn/_shots/, og/_sheet.html); CI builds without
    // --shots, so neither is deployed and neither is a page a reader loads
    const pages = files.filter((f) => f.endsWith(".html") && !f.startsWith("learn/_shots/") && !f.startsWith("og/")), over = [];
    let most = { f: "", n: 0 };
    for (const f of pages) { const n = kb(f), cap = HELD[f] || 25; if (n >= cap) over.push(`${f} ${n.toFixed(1)} KB (${cap})`); if (!HELD[f] && n > most.n) most = { f, n }; }
    if (over.length) out.push("pages over their budget: " + over.join(", "));
    // The FDE guide (council 10): its own stylesheet, which only its four pages load, under 2 KB, and its hub under
    // 22 KB, the sketch included. Ceilings below the 25 every page has, so neither is a hold in HELD.
    const GUIDE_KB = { "theme/fde.css": 2, "forward-deployed-engineer/index.html": 22 }, guide = {};
    for (const [f, cap] of Object.entries(GUIDE_KB)) {
      if (!existsSync(SITE + f)) { out.push(`${f} was not built`); continue; }
      guide[f] = kb(f);
      if (guide[f] >= cap) out.push(`${f} is ${guide[f].toFixed(2)} KB gzipped; the FDE guide's budget for it is ${cap}`);
    }
    // The home page (council 10): its HTML under 21 KB, with no <style> block (its rules belong in base.css, which is
    // cached and ships without comments); everything a first visit asks for, scrolled to the end, under 176 KB
    // (firstVisit, above). And frame/frame.js, which every page loads: 5.4 KB on 3 October 2026, when it gained the
    // consultancy's topic, so 6 leaves room for one more feature without inviting drift.
    const home = kb("index.html"), visit = firstVisit(), frame = kb("frame/frame.js");
    if (home >= 21) out.push(`the home page's HTML is ${home.toFixed(1)} KB gzipped; the budget is 21 (council 10)`);
    if (/<style\b/i.test(readFileSync(SITE + "index.html", "utf8").replace(/<script\b[\s\S]*?<\/script>|<!--[\s\S]*?-->/gi, ""))) out.push("the home page carries a <style> block; its rules belong in base.css");
    if (visit.missing.length) out.push(`the home page names ${visit.missing.join(", ")}, which the build did not make`);
    if (visit.bytes / 1024 >= 176) out.push(`a first visit to the home page asks for ${(visit.bytes / 1024).toFixed(1)} KB in ${visit.files.length} files; the budget is 176 (council 10)`);
    if (frame >= 6) out.push(`frame/frame.js is ${frame.toFixed(2)} KB gzipped; the budget is 6`);
    const fonts = files.filter((f) => /\.(woff2?|ttf|otf|eot)$/i.test(f)).sort();
    if (fonts.join(" ") !== FONTS.join(" ")) out.push(`the font files are ${fonts.join(", ")}`);
    const remote = pages.filter((f) => /fonts\.(googleapis|gstatic)\.com/.test(readFileSync(SITE + f, "utf8")));
    if (remote.length) out.push(`a page asks a font host for a font: ${remote.slice(0, 3).join(", ")}`);
    if (!out.length) console.log(`  ok   base.css ${css.toFixed(1)} KB, the game's scripts ${game.toFixed(1)} KB, ${pages.length} pages (the largest held to 25 KB is /${most.f.replace(/index\.html$/, "")} at ${most.n.toFixed(1)}), four fonts, the FDE guide's stylesheet ${guide["theme/fde.css"].toFixed(1)} KB and its hub ${guide["forward-deployed-engineer/index.html"].toFixed(1)}; ` +
      `the home page ${home.toFixed(1)} KB and a first visit to it ${(visit.bytes / 1024).toFixed(1)} KB in ${visit.files.length} files, hero.js ${hero.toFixed(1)} KB, frame.js ${frame.toFixed(1)} KB`);
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
// And the lesson's type (council 10, 1.4): the title in two lines, the part after its first ": " or "? " in the
// grey continuation, 3:1 or more against the page in both themes, no hyphenated word in it broken across two
// lines; in .prose, only six gaps between stacked blocks (8, 16, 18, 24, 32 and 64px, each to 1px); no heading in
// the lesson or its guide under 24px tracked tighter than -0.005em. Then at 390 wide: no table scrolls sideways,
// its cells are 15px, and every fold's summary ("Show the answer") is 44px tall or more.
console.log("\n18. every lesson at 1440 x 900: the map at most 630px tall, the measure, the edges, the guide, the type");
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
  const TYPE = `(() => { const main = document.querySelector('main.lm'), h1 = main.querySelector('h1'), c = h1.querySelector('.c');
    const t = h1.textContent, k = t.search(/[:?] /), cv = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
    const lum = (col) => { cv.clearRect(0, 0, 1, 1); cv.fillStyle = '#000'; cv.fillStyle = col; cv.fillRect(0, 0, 1, 1);
      const v = [...cv.getImageData(0, 0, 1, 1).data].slice(0, 3).map((x) => (x /= 255) <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4);
      return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
    const html = document.documentElement, was = html.getAttribute('data-theme'), grey = [];
    if (c) { for (const th of ['dark', 'light']) { html.setAttribute('data-theme', th);
        const a = lum(getComputedStyle(c).color), b = lum(getComputedStyle(document.body).backgroundColor);
        grey.push(Math.round((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05) * 100) / 100); }
      was === null ? html.removeAttribute('data-theme') : html.setAttribute('data-theme', was); }
    const prose = main.querySelector('.prose'), OK = [8, 16, 18, 24, 32, 64], gaps = [];
    const kids = [...prose.children].filter((e) => getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().height > 0);
    for (let i = 1; i < kids.length; i++) { const g = kids[i].getBoundingClientRect().top - kids[i - 1].getBoundingClientRect().bottom;
      if (!OK.some((v) => Math.abs(g - v) <= 1)) gaps.push(kids[i - 1].tagName.toLowerCase() + ' to ' + kids[i].tagName.toLowerCase() + ' ' + Math.round(g) + 'px'); }
    const tight = [...document.querySelectorAll('main.lm :is(h1,h2,h3,h4,h5,h6), .lguide :is(h1,h2,h3,h4,h5,h6)')].filter((e) => {
      const cs = getComputedStyle(e), fs = parseFloat(cs.fontSize), ls = parseFloat(cs.letterSpacing) || 0; return fs < 24 && ls / fs < -0.0051; })
      .map((e) => '"' + e.textContent.slice(0, 32) + '"');
    return { lines: Math.round(h1.getBoundingClientRect().height / parseFloat(getComputedStyle(h1).lineHeight)), grey,
      split: k < 0 ? !c : !!c && c.textContent === t.slice(k + 2), broken: [...h1.querySelectorAll('.nw')].filter((e) => e.getClientRects().length > 1).map((e) => e.textContent),
      gaps, tight }; })()`;
  const AT390 = `(async () => { await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    const tw = [...document.querySelectorAll('main.lm .prose .tw:not(.wide)')];
    return { scroll: tw.filter((t) => t.scrollWidth > t.clientWidth + 1).map((t) => t.scrollWidth + 'px in ' + t.clientWidth),
      small: tw.filter((t) => { const d = t.querySelector('td'); return d && parseFloat(getComputedStyle(d).fontSize) < 15; }).length,
      folds: [...document.querySelectorAll('main.lm .prose summary')].map((s) => Math.round(s.getBoundingClientRect().height * 10) / 10).filter((h) => h < 44) }; })()`;
  let maps = 0, tallest = { h: 0, at: "" }, framed = 0, worst = { cpl: 0, at: "" }, grey = { r: 99, at: "" };
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
      const t = await evaluate(TYPE);
      if (t.lines !== 2) out.push(`${at}: the title takes ${t.lines} lines`);
      if (!t.split) out.push(`${at}: the title's grey continuation is not the part after its first ": " or "? "`);
      for (const r of t.grey) { if (r < 3) out.push(`${at}: the title's grey continuation is ${r}:1`); if (r < grey.r) grey = { r, at }; }
      if (t.broken.length) out.push(`${at}: the title breaks inside ${t.broken.join(", ")}`);
      if (t.gaps.length) out.push(`${at}: gaps off the six in .prose: ${t.gaps.slice(0, 4).join(", ")}${t.gaps.length > 4 ? ` and ${t.gaps.length - 4} more` : ""}`);
      if (t.tight.length) out.push(`${at}: headings under 24px tracked tighter than -0.005em: ${t.tight.slice(0, 3).join(", ")}`);
      await send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
      const ph = await evaluate(AT390);
      await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
      if (ph.scroll.length) out.push(`${at} at 390: a table scrolls sideways, ${ph.scroll.join(", ")}`);
      if (ph.small) out.push(`${at} at 390: ${ph.small} table(s) with cells under 15px`);
      if (ph.folds.length) out.push(`${at} at 390: a fold's summary is ${ph.folds.join(", ")}px tall, under 44`);
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
    `the longest line ${worst.cpl} characters (${worst.at}), one left edge, two right ones, the guide on screen and marking the section being read; ` +
    `every title in two lines, its grey at ${grey.r}:1 or more (${grey.at}), six gaps, no small heading tracked tight; at 390 no table scrolls, ` +
    `every fold 44px or taller`);
}

// 19. the home page's bands (council 10): one function for each band's parcel, H3 to H8, in the order the bands run,
// each called at 1440 x 900 and at 390 x 844 on a fresh load of the home page (dark, reduced motion, at the top). A
// function returns its failures as sentences; one that needs another state (motion, the light theme, a hover, a
// scroll) sets it itself. A parcel writes only inside its own function, between its own two comments, and never
// edits the list that calls them, so parcels built side by side never touch the same lines. Before the bands, the
// gate's own parcel (H10) checks the page as a whole: its order, its headings, its height and its first visit.
console.log("\n19. the home page: its order, headings and height, then each band's own checks at 1440 x 900 and 390 x 844");
{
  // home · H10 the page: its order, headings and height
  // Top to bottom as verdict-home 1.0 has it: the hero, then in main the seven bands in order, each with its eyebrow
  // and heading (the simulator's "ninety-day" carries a non-breaking hyphen, U+2011, read here as a hyphen), each
  // below the one before, then the footer; one h1, and main's h2s are the seven headings and no others. The page is
  // 8,700px tall or less at 1440 and 13,200 or less at 390. And a first visit, cache off and scrolled to the end, asks
  // for no file that pass 17's count of its bytes (firstVisit) leaves out.
  const ORDER = [["top", "The agentic manual", "One manual for building software with AI agents."],
    ["methods", "The methods", "How AI-DLC, BMAD and the rest fit together."],
    ["choose", "Your team", "Which agentic methods should your team use?"],
    ["roles", "By role", "Start from the job you do."],
    ["tutorial", "The tutorial", "Learn to run agent projects one question at a time."],
    ["simulator", "The simulator", "Play a ninety-day AI project in fifteen minutes."],
    ["library", "The library", "Take the tools, templates and prompts with you."],
    ["work-with-us", "SkyWays Consultancy", "Work with the consultancy that wrote this manual."]];
  const TALL = { 1440: 8700, 390: 13200 }, tall = {};
  async function pageH10(w, h) {
    const out = [];
    const m = await evaluate(`(async () => {
      await document.fonts.ready;
      const say = (e) => (e ? e.textContent.replace(/\\u2011/g, '-').replace(/\\s+/g, ' ').trim() : ''), main = document.querySelector('main'), hero = document.getElementById('top');
      const bands = ${JSON.stringify(ORDER.map(([id]) => id))}.map((id) => { const b = document.getElementById(id), r = b ? b.getBoundingClientRect() : null;
        return { id, there: !!b, eyebrow: say(b && b.querySelector('.eyebrow')), heading: say(b && b.querySelector(id === 'top' ? 'h1' : 'h2')),
          top: r ? Math.round(r.top + scrollY) : 0, bottom: r ? Math.round(r.bottom + scrollY) : 0 }; });
      return { bands, kids: main ? [...main.children].filter((e) => e.tagName === 'SECTION').map((e) => e.id || 'a section with no id') : [],
        h1: document.querySelectorAll('h1').length, h2: main ? [...main.querySelectorAll('h2')].map(say) : [],
        heroFirst: !!hero && hero.nextElementSibling === main, footer: !!main && main.nextElementSibling?.tagName === 'FOOTER', tall: document.documentElement.scrollHeight };
    })()`);
    const ids = ORDER.slice(1).map(([id]) => id);
    if (m.kids.join() !== ids.join()) out.push(`main's bands run ${m.kids.join(", ") || "nowhere"}; verdict-home 1.0 runs ${ids.join(", ")}`);
    if (!m.heroFirst) out.push("main does not follow the hero (#top)");
    if (!m.footer) out.push("the footer does not follow main");
    m.bands.forEach((b, i) => {
      const [, eyebrow, heading] = ORDER[i];
      if (!b.there) return out.push(`there is no #${b.id}`);
      if (b.eyebrow !== eyebrow) out.push(`#${b.id}'s eyebrow reads "${b.eyebrow}", not "${eyebrow}"`);
      if (b.heading !== heading) out.push(`#${b.id}'s heading reads "${b.heading}", not "${heading}"`);
      if (i && b.top < m.bands[i - 1].bottom - 1) out.push(`#${b.id} starts at ${b.top}px, above the end of #${m.bands[i - 1].id} (${m.bands[i - 1].bottom}px)`);
    });
    if (m.h1 !== 1) out.push(`the page has ${m.h1} h1s; one`);
    const others = m.h2.filter((t) => !ORDER.some(([, , heading]) => heading === t));
    if (m.h2.length !== 7) out.push(`main has ${m.h2.length} h2s${others.length ? ` ("${others.join('", "')}" among them)` : ""}; the seven headings of verdict-home 1.0 and no others`);
    tall[w] = m.tall;
    if (TALL[w] && m.tall > TALL[w]) out.push(`the page is ${m.tall.toLocaleString("en-GB")}px tall at ${w}; ${TALL[w].toLocaleString("en-GB")} is the most`);
    // a first visit with motion allowed, the cache off, scrolled to the end: every file it asks for is one pass 17 counts
    await send("Network.enable");
    await send("Network.setCacheDisabled", { cacheDisabled: true });
    await send("Emulation.setEmulatedMedia", { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "no-preference" }] });
    await send("Page.navigate", { url: BASE });
    await sleep(1500);
    const asked = await evaluate(`(async () => { const end = document.documentElement.scrollHeight;
      for (let y = 0; y < end; y += 400) { scrollTo({ top: y, behavior: 'instant' }); await new Promise((r) => setTimeout(r, 60)); }
      await new Promise((r) => setTimeout(r, 1200));
      return performance.getEntriesByType('resource').map((e) => e.name); })()`);
    await send("Network.setCacheDisabled", { cacheDisabled: false });
    const counted = new Set(firstVisit().files), site = new URL(BASE);
    const local = (u) => { const x = new URL(u); return x.origin === site.origin && x.pathname.startsWith(site.pathname) ? decodeURIComponent(x.pathname.slice(site.pathname.length)) || "index.html" : u; };
    const missed = [...new Set(asked.filter((u) => !/^(data|blob):/.test(u)).map(local))].filter((f) => !counted.has(f));
    if (!asked.length) out.push("the browser lists no request for a first visit, so the files it asks for could not be read");
    if (missed.length) out.push(`a first visit asks for ${missed.join(", ")}, which pass 17 does not count`);
    return out;
  }
  // end of home · H10

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
    // At 1440 x 900 with the eyebrow under the header and nothing chosen, the heading, its line and all four columns
    // with both their lines end inside the screen. Each of the three questions is a fieldset whose legend is the
    // question, with two radios; with nothing chosen every Yes and No line shows. Yes hides the No line; No hides the
    // Yes line and turns the method's name to --soft, 4.5:1 or more on the page; a radio reached by the keyboard
    // rings its label; nothing is written to storage. At 390 each Yes and No is 44px tall or more. Every text is 4.5:1 in both
    // themes, a greyed name included. On paper there are no toggles and both lines show, whatever was chosen.
    const out = [];
    const SEE = `(async () => {
      await document.fonts.ready;
      const band = document.getElementById('choose'), pk = band && band.querySelector('.pk');
      if (!pk) return null;
      scrollTo({ top: band.querySelector('.eyebrow').getBoundingClientRect().top + scrollY - 84, behavior: 'instant' });
      await new Promise((r) => setTimeout(r, 150));
      const sets = [...pk.querySelectorAll('fieldset')], vis = (e) => !!e && e.checkVisibility();
      const ends = [...pk.children, band.querySelector('h2'), band.querySelector('.sec-h p:not(.eyebrow)')].map((e) => e.getBoundingClientRect().bottom);
      return { bottom: Math.round(Math.max(...ends)), over: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        cols: pk.children.length, sets: sets.length,
        legends: sets.filter((f) => f.firstElementChild?.tagName === 'LEGEND' && f.querySelectorAll('input[type=radio]').length === 2).length,
        both: sets.filter((f) => vis(f.querySelector('.y')) && vis(f.querySelector('.n'))).length,
        toggles: sets.filter((f) => vis(f.querySelector('.yn'))).length,
        targets: [...pk.querySelectorAll('.yn label')].map((l) => Math.round(l.getBoundingClientRect().height)),
        small: [...band.querySelectorAll('*')].filter((e) => vis(e) && [...e.childNodes].some((t) => t.nodeType === 3 && t.nodeValue.trim())
          && parseFloat(getComputedStyle(e).fontSize) < 11).map((e) => e.textContent.trim().slice(0, 30)) };
    })()`;
    // the colour helpers the contrast checks share: a colour painted on black and on white gives its rgb and alpha
    const HELP = `const cv = document.createElement('canvas'); cv.width = cv.height = 1;
      const cx = cv.getContext('2d', { willReadFrequently: true });
      const paint = (base, c) => { cx.globalCompositeOperation = 'copy'; cx.fillStyle = base; cx.fillRect(0, 0, 1, 1);
        cx.globalCompositeOperation = 'source-over'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); return cx.getImageData(0, 0, 1, 1).data; };
      const rgba = (c) => { const k = paint('#000', c), w = paint('#fff', c), a = Math.max(0, Math.min(1, 1 - (w[0] - k[0] + w[1] - k[1] + w[2] - k[2]) / 765));
        return a > 0.004 ? [k[0] / a, k[1] / a, k[2] / a, a] : [0, 0, 0, 0]; };
      const over = (t, u) => [0, 1, 2].map((i) => t[i] * t[3] + u[i] * (1 - t[3])).concat(1);
      const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
      const cr = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
      const under = (e, x, y) => { let bg = [255, 255, 255, 1];
        for (const el of document.elementsFromPoint(x, y).reverse()) { const c = rgba(getComputedStyle(el).backgroundColor); if (c[3] > 0) bg = over(c, bg); if (el === e) break; }
        return bg; };`;
    const ACT = `(async () => {
      ${HELP}
      const stored = () => JSON.stringify([Object.entries(localStorage), Object.entries(sessionStorage), document.cookie]), before = stored();
      const f = document.querySelector('#choose fieldset'), yes = f.querySelector('[value=y]'), no = f.querySelector('[value=n]');
      const shown = (s) => f.querySelector(s).checkVisibility(), wait = () => new Promise((r) => setTimeout(r, 60));
      f.scrollIntoView({ block: 'center' }); await wait();
      const o = {};
      no.click(); await wait();
      o.no = [shown('.y'), shown('.n')];
      const a = f.querySelector('h3 a'), probe = document.createElement('i');
      probe.style.color = 'var(--soft)'; f.append(probe);
      o.soft = getComputedStyle(a).color === getComputedStyle(probe).color; probe.remove();
      const q = a.getBoundingClientRect();
      o.softRatio = +cr(over(rgba(getComputedStyle(a).color), under(a, q.left + q.width / 2, q.top + q.height / 2)), under(a, q.left + q.width / 2, q.top + q.height / 2)).toFixed(2);
      yes.click(); await wait();
      o.yes = [shown('.y'), shown('.n')];
      no.click(); await wait();                         // left on No, for the paper and contrast checks
      o.stored = stored() !== before;
      return o;
    })()`;
    const PAPER = `[...document.querySelectorAll('#choose fieldset')].map((f) => !f.querySelector('.yn').checkVisibility() && f.querySelector('.y').checkVisibility() && f.querySelector('.n').checkVisibility()).every(Boolean)`;
    const CONTRAST = (light) => `(async () => {
      if (${light}) document.documentElement.setAttribute('data-theme', 'light');
      await document.fonts.ready;
      ${HELP}
      const band = document.getElementById('choose'), low = [], done = new Set();
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
          const bg = under(e, rr.left + rr.width / 2, rr.top + rr.height * 0.55), ratio = cr(over(rgba(getComputedStyle(e).color), bg), bg);
          if (ratio < 4.5) low.push(ratio.toFixed(2) + ':1, "' + t.nodeValue.trim().slice(0, 28) + '"');
        }
      }
      return low;
    })()`;
    try {
      const m = await evaluate(SEE);
      if (!m) return ["no chooser (.pk) in #choose"];
      if (m.cols !== 4 || m.sets !== 3 || m.legends !== 3) out.push(`${m.cols} columns and ${m.legends} of ${m.sets} questions as a fieldset with a legend and two radios; four columns and three such questions expected`);
      if (m.both !== m.sets) out.push(`with nothing chosen, ${m.sets - m.both} questions do not show both their lines`);
      if (m.toggles !== m.sets) out.push(`${m.toggles} of ${m.sets} questions show their Yes and No`);
      if (m.over > 0) out.push(`the page scrolls sideways by ${m.over}px`);
      if (m.small.length) out.push(`text under 11px: ${m.small.slice(0, 3).join("; ")}`);
      if (w >= 1440 && m.bottom > h) out.push(`with the eyebrow under the header the chooser ends at ${m.bottom}px, past the ${h}px screen`);
      if (w < 600 && m.targets.some((t) => t < 44)) out.push(`a Yes or No is ${Math.min(...m.targets)}px tall; 44 on a phone`);
      // the focus ring, reached as a reader reaches it: a Tab from the link before the first question (a script's
      // focus() does not count as the keyboard, so it would not show the ring)
      await evaluate(`(() => { const a = [...document.querySelectorAll('#choose .pk-c:first-child a')].pop(); a.scrollIntoView({ block: 'center' }); a.focus(); return true; })()`);
      for (const type of ["keyDown", "keyUp"]) await send("Input.dispatchKeyEvent", { type, key: "Tab", code: "Tab", windowsVirtualKeyCode: 9, nativeVirtualKeyCode: 9 });
      await sleep(100);
      if (!(await evaluate(`(() => { const e = document.activeElement, l = e && e.type === 'radio' && e.closest('#choose label'); if (!l) return false;
        const cs = getComputedStyle(l); return cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) >= 2; })()`))) out.push("a radio reached by the keyboard shows no ring round its label");
      const a = await evaluate(ACT);
      if (a.no.join() !== "false,true") out.push("No does not leave the No line alone");
      if (a.yes.join() !== "true,false") out.push("Yes does not leave the Yes line alone");
      if (!a.soft || a.softRatio < 4.5) out.push(`after No the method's name is ${a.soft ? "" : "not "}--soft, at ${a.softRatio}:1`);
      if (a.stored) out.push("a choice wrote to storage or a cookie");
      for (const light of [false, true]) {
        const low = await evaluate(CONTRAST(light));
        if (low.length) out.push(`${light ? "light" : "dark"}: under 4.5:1: ${low.slice(0, 4).join("; ")}`);
      }
      await send("Emulation.setEmulatedMedia", { media: "print", features: [{ name: "prefers-color-scheme", value: "dark" }] });
      await sleep(150);
      if (!(await evaluate(PAPER))) out.push("on paper, after a choice, a toggle shows or a line is hidden");
      await send("Emulation.setEmulatedMedia", { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "reduce" }] });
    } catch (e) {
      out.push("the chooser's checks could not run: " + e.message.slice(0, 160));
    }
    return out;
  }
  // end of home · H4

  // home · H5 people: the tutorial band, #tutorial
  async function bandH5(w, h) {
    // Four people in the lifecycle's order, each with a name and a job, a question in an h3, an answer of 24 words
    // or fewer and one link, to a lesson (a page whose main is .lm), never to a role page. Four across from
    // 1181px, two by two from 601 to 1180, one column at 600 and under, the picture on top. At 1440 x 900 with
    // the eyebrow under the header, every question and lesson link is in view. The handwriting is 13px or more
    // at every width checked and 4.5:1 or more on its paper in both themes (the dark theme's toned paper and deeper
    // pens are U1's, verdict-learn 4.3.3).
    const out = [], JOBS = ["product manager", "solution architect", "engineering lead", "QA lead"];
    const cards = await evaluate(`(async () => { await document.fonts.ready;
      return Promise.all([...document.querySelectorAll('#tutorial .qs > li')].map(async (c) => {
        const a = [...c.querySelectorAll('a[href]')], q = c.querySelectorAll('h3');
        const page = a.length === 1 ? await fetch(a[0].href).then((r) => r.text()).catch(() => '') : '';
        return { who: (c.querySelector('.q-who')?.textContent || '').trim(), h3: q.length, ask: q[0]?.textContent.trim() || '',
          words: (q[0]?.nextElementSibling?.textContent || '').trim().split(/\\s+/).filter(Boolean).length,
          links: a.length, href: a[0]?.getAttribute('href') || '', lesson: /<main\\b[^>]*class="[^"]*\\blm\\b/.test(page) };
      })); })()`);
    if (cards.length !== 4) return [`${cards.length} people cards; four`];
    cards.forEach((c, i) => {
      const at = `card ${i + 1} (${c.who || "no name"})`;
      if (!new RegExp(`^[A-Z][a-z]+, ${JOBS[i]}$`).test(c.who)) out.push(`${at}: the name and job should read "<name>, ${JOBS[i]}"`);
      if (c.h3 !== 1 || !/\?”$/.test(c.ask)) out.push(`${at}: one question in an h3, in quotes`);
      if (!c.words || c.words > 24) out.push(`${at}: an answer of ${c.words} words, where 1 to 24 are the rule`);
      if (c.links !== 1) out.push(`${at}: ${c.links} links; one, to its lesson`);
      else if (!c.lesson) out.push(`${at}: its link, ${c.href}, is not a lesson`);
    });
    const READ = `(async () => { await document.fonts.ready;
      const lum = (c) => { const v = c.match(/[\\d.]+/g).slice(0, 3).map((x) => { x = +x / 255; return x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; });
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
      const cards = [...document.querySelectorAll('#tutorial .qs > li')], hand = [];
      for (const c of cards) {
        const svg = c.querySelector('svg.sk'), bg = getComputedStyle(c.querySelector('.sk-paper') || c).backgroundColor;
        const k = svg ? svg.getBoundingClientRect().width / svg.viewBox.baseVal.width : 0;
        for (const t of svg ? svg.querySelectorAll('text') : []) {
          const cs = getComputedStyle(t), [a, b] = [lum(cs.fill), lum(bg)].sort((p, q) => q - p);
          hand.push({ t: t.textContent, px: Math.round(parseFloat(cs.fontSize) * k * 10) / 10, cr: Math.round((a + 0.05) / (b + 0.05) * 100) / 100, bg });
        }
      }
      return { hand, cols: new Set(cards.map((c) => Math.round(c.getBoundingClientRect().left))).size,
        top: cards.every((c) => { const p = c.querySelector('.sk-paper'), q = c.querySelector('h3');
          return !!p && !!q && p.getBoundingClientRect().bottom <= q.getBoundingClientRect().top; }) }; })()`;
    let now = w;
    for (const x of w >= 600 ? [w, 1181, 1180, 1024, 601] : [600, w, 320]) {
      if (x !== now) {
        await send("Emulation.setDeviceMetricsOverride", { width: x, height: h, deviceScaleFactor: 1, mobile: x < 600 });
        await sleep(200);
        now = x;
      }
      const want = x >= 1181 ? 4 : x >= 601 ? 2 : 1;
      const dark = await evaluate(READ);
      if (dark.cols !== want) out.push(`at ${x}px the cards run in ${dark.cols} columns; ${want}`);
      if (!dark.top) out.push(`at ${x}px a picture is not above its question`);
      if (!dark.hand.length) out.push(`at ${x}px the drawings have no handwriting to measure`);
      const small = dark.hand.filter((t) => t.px < 13).sort((a, b) => a.px - b.px)[0];
      if (small) out.push(`at ${x}px the handwriting is ${small.px}px ("${small.t}"); 13 is the floor`);
      const faint = dark.hand.filter((t) => t.cr < 4.5).sort((a, b) => a.cr - b.cr)[0];
      if (faint) out.push(`at ${x}px, dark, the handwriting is ${faint.cr}:1 on its paper ("${faint.t}"); 4.5 is the floor`);
    }
    await evaluate(`document.documentElement.setAttribute('data-theme', 'light')`);
    const faint = (await evaluate(READ)).hand.filter((t) => t.cr < 4.5).sort((a, b) => a.cr - b.cr)[0];
    if (faint) out.push(`light, the handwriting is ${faint.cr}:1 on its paper ("${faint.t}"); 4.5 is the floor`);
    if (w === 1440 && h === 900) {
      await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: false });
      await sleep(200);
      const fit = await evaluate(`(async () => { const b = document.getElementById('tutorial'), hd = document.querySelector('.hd');
        scrollTo({ top: b.querySelector('.eyebrow').getBoundingClientRect().top + scrollY - hd.getBoundingClientRect().bottom - 12, behavior: 'instant' });
        await new Promise((r) => setTimeout(r, 200));
        const ends = [...b.querySelectorAll('.qs h3, .qs a')].map((e) => e.getBoundingClientRect());
        return { top: Math.min(...ends.map((r) => r.top)) >= hd.getBoundingClientRect().bottom, end: Math.round(Math.max(...ends.map((r) => r.bottom))) }; })()`);
      if (!fit.top || fit.end > h) out.push(`with the eyebrow under the header, the questions and lesson links end at ${fit.end}px, past the screen's ${h}`);
    }
    return out;
  }
  // end of home · H5

  // home · H6 day card: the simulator band, #simulator
  // The room loads with the page; "Example day" sits on its picture at 4.5:1 whatever lies under the pill; over
  // 1000px the card stands at the earlier frame's tilt, faces the reader on hover and on focus inside it, turns in
  // 400ms with motion allowed and at once under reduced motion, wears the dark theme's own deeper shadow; at 1000px
  // and under, and on paper, it is flat with no shadow; and a .daycard outside the band (the game's) never tilts.
  async function bandH6(w, h) {
    const out = [];
    const media = (reduce, print = false) => send("Emulation.setEmulatedMedia", { media: print ? "print" : "", features: [
      { name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: reduce ? "reduce" : "no-preference" }] });
    // the card's state now: at the tilt, facing the reader, or flat; its shadow, its transition, anything running
    const at = () => evaluate(`(() => { const c = document.querySelector('#simulator .daycard'), cs = getComputedStyle(c);
      const near = (s) => { if (cs.transform === 'none') return false; const a = new DOMMatrix(cs.transform).toFloat64Array(), b = new DOMMatrix(s).toFloat64Array();
        return a.every((v, i) => Math.abs(v - b[i]) < 1e-3); };
      return { tilt: near('rotateY(-9deg) rotateX(3deg)'), face: near('rotateY(-3deg) rotateX(1deg)'), none: cs.transform === 'none',
        shadow: cs.boxShadow, dur: cs.transitionDuration, prop: cs.transitionProperty, moving: c.getAnimations().length,
        persp: getComputedStyle(document.querySelector('#simulator .wrap')).perspective, over: document.documentElement.scrollWidth - innerWidth }; })()`);
    const mouse = async (onCard, wait = 150) => {
      const p = onCard ? await evaluate(`(() => { const r = document.querySelector('#simulator .daycard').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`) : { x: 2, y: h - 2 };
      await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: p.x, y: p.y });
      await sleep(wait);
    };
    // the room is fetched with the page, not when the band nears the screen: the reader is still at the top
    const pic = await evaluate(`(() => { const i = document.querySelector('#simulator .dc-pic img'), e = document.querySelector('#simulator .dc-pic .dc-ex');
      const p = document.querySelector('#simulator .dc-pic').getBoundingClientRect(), r = e ? e.getBoundingClientRect() : null;
      const ctx = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
      const rgba = (s) => { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = s; ctx.fillRect(0, 0, 1, 1); const d = ctx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
      const lum = (c) => c.slice(0, 3).map((v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }).reduce((s, v, k) => s + v * [0.2126, 0.7152, 0.0722][k], 0);
      let ratio = 0;
      if (e) { const cs = getComputedStyle(e), t = rgba(cs.color), b = rgba(cs.backgroundColor);
        // the pill is laid over the picture: judge it over white, the worst ground for light letters
        const g = b.slice(0, 3).map((v) => b[3] * v + (1 - b[3]) * 255), L = [lum(t), lum(g)].sort((x, y) => y - x);
        ratio = Math.round((L[0] + 0.05) / (L[1] + 0.05) * 100) / 100; }
      return { done: i.complete && i.naturalWidth === 144, lazy: i.getAttribute('loading'), below: Math.round(p.top - innerHeight),
        pill: e ? e.textContent.trim() : null, size: e ? parseFloat(getComputedStyle(e).fontSize) : 0, ratio,
        inside: !!r && r.left >= p.left && r.top >= p.top && r.right <= p.right && r.bottom <= p.bottom }; })()`);
    if (!pic.done) out.push(`the room's picture is not loaded while the band is still ${pic.below}px below the screen`);
    if (pic.lazy) out.push(`the room's picture loads ${pic.lazy}`);
    if (pic.pill !== "Example day") out.push(`the picture's pill reads ${JSON.stringify(pic.pill)}, not "Example day"`);
    else {
      if (!pic.inside) out.push("the \"Example day\" pill is not inside the picture");
      if (pic.ratio < 4.5) out.push(`"Example day" is ${pic.ratio}:1 on its pill (over white, the worst ground); 4.5 is the floor`);
      if (pic.size < 11) out.push(`"Example day" is ${pic.size}px; nothing is under 11`);
    }
    // the game's own Day 1 card is a .daycard too, outside #simulator: it never tilts
    if (!(await evaluate(`(() => { const a = document.body.appendChild(document.createElement('article')); a.className = 'daycard';
      const t = getComputedStyle(a).transform; a.remove(); return t === 'none'; })()`))) out.push("a .daycard outside the simulator band tilts too (the game's Day 1 card is one)");
    if (w <= 1000) {
      const m = await at();
      if (!m.none) out.push("the card is tilted at 1000px and under");
      if (m.persp !== "none") out.push(`the band's grid keeps a perspective (${m.persp}) at 1000px and under`);
      return out;
    }
    await evaluate(`(() => { const c = document.querySelector('#simulator .daycard'); scrollTo({ top: c.getBoundingClientRect().top + scrollY - 120, behavior: 'instant' }); return true; })()`);
    await mouse(false);
    let m = await at();
    if (!m.tilt) out.push("at rest the card is not at rotateY(-9deg) rotateX(3deg)");
    if (!m.shadow.includes("rgba(0, 0, 0, 0.92)")) out.push(`in the dark theme the card's shadow is not its own deeper one (${m.shadow.slice(0, 60)})`);
    // reduced motion, as this pass runs: hover turns it at once, and nothing animates
    await mouse(true);
    m = await at();
    if (!m.face) out.push("hovered, the card does not turn to face the reader (rotateY(-3deg) rotateX(1deg))");
    if (m.moving) out.push(`under reduced motion the card still animates (${m.moving} running)`);
    if (parseFloat(m.dur) !== 0) out.push(`under reduced motion the card's transition is ${m.dur}`);
    await mouse(false);
    await evaluate("document.querySelector('#simulator .dc-o a').focus({ preventScroll: true }), true");
    m = await at();
    if (!m.face) out.push("with focus on an answer inside it, the card does not face the reader");
    await evaluate("document.activeElement.blur(), true");
    if (!(await at()).tilt) out.push("with focus gone, the card does not go back to its tilt");
    // motion allowed: the turn is one transition on transform, in 400ms
    await media(false);
    await sleep(100);
    m = await at();
    if (m.prop !== "transform" || Math.abs(parseFloat(m.dur) - 0.4) > 1e-6) out.push(`with motion allowed the card turns by "${m.prop} ${m.dur}", not transform in 400ms`);
    await mouse(true, 0);                          // read at once: on a busy machine a pause could outlast the 400ms turn
    m = await at();
    if (!m.moving) out.push("with motion allowed, hovering starts no transition");
    await sleep(600);
    if (!(await at()).face) out.push("with motion allowed, the card does not arrive facing the reader");
    await mouse(false);
    await media(true);
    // the light theme's shadow is its own too
    await evaluate("document.documentElement.setAttribute('data-theme', 'light'), true");
    m = await at();
    if (!m.shadow.includes("rgba(4, 6, 14, 0.7)")) out.push(`in the light theme the card's shadow is not the long one (${m.shadow.slice(0, 60)})`);
    await evaluate("document.documentElement.removeAttribute('data-theme'), true");
    // paper: flat, no shadow
    await media(true, true);
    await sleep(100);
    m = await at();
    if (!m.none || m.shadow !== "none") out.push(`in print the card is ${m.none ? "flat" : "tilted"} with ${m.shadow === "none" ? "no shadow" : "a shadow"}`);
    await media(true);
    // the edge of the rule, and no sideways scroll where the tilt is narrowest
    for (const [vw, tilted] of [[1000, false], [1001, true], [1024, true], [1100, true]]) {
      await send("Emulation.setDeviceMetricsOverride", { width: vw, height: h, deviceScaleFactor: 1, mobile: false });
      await sleep(150);
      m = await at();
      if (tilted ? !m.tilt : !m.none) out.push(`at ${vw}px the card is ${m.none ? "flat" : m.tilt ? "tilted" : "turned part way"}`);
      if (m.over > 0) out.push(`at ${vw}px the page scrolls sideways by ${m.over}px`);
    }
    return out;
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
  // One panel at radius 20 with one filled button and no form, logo, testimonial or figure; four offers, each
  // ending in "You leave with", in the same words as the organisation's makesOffer, with no price; four columns
  // at 1440; at 390 the band within 1,300px, 20px inside the panel, 48px above and below it, each label on its
  // words' line. Every text on the panel 4.5:1 in both themes. With script the button opens the drawer on the
  // consultancy's topic and a message from it is tagged so, and the footer's button opens it on the drawer's own
  // first choice; on paper the button prints where it goes. Without script it is a link to the discussions page and
  // no address is printed in the page: pass 1 reads that, on its load without script.
  async function bandH8(w, h) {
    const out = [];
    const m = await evaluate(`(() => { const b = document.querySelector('#work-with-us'); if (!b) return null;
      const p = b.querySelector('.cx-in'), btn = b.querySelectorAll('.btn'), lis = [...b.querySelectorAll('.cx-o > li')];
      const words = (e) => (e ? e.textContent.replace(/\\s+/g, ' ').trim() : '');
      const offers = lis.map((li) => { const k = li.lastElementChild, lab = k && k.querySelector('span'), t = lab && lab.nextSibling;
        let inline = false;
        if (t && t.length > 2) { const r = document.createRange(); r.setStart(t, 1); r.setEnd(t, 2); inline = Math.abs(r.getBoundingClientRect().top - lab.getBoundingClientRect().top) < 6; }
        return { name: words(li.querySelector('h3')), does: words(li.querySelector('h3 + p')), last: words(k),
          leave: lab ? words(k).slice(words(lab).length).trim() : '', top: Math.round(li.getBoundingClientRect().top), inline }; });
      const org = [...document.querySelectorAll('script[type="application/ld+json"]')].flatMap((s) => { try { const j = JSON.parse(s.textContent); return j['@graph'] || [j]; } catch { return []; } })
        .find((x) => x['@type'] === 'Organization' && x.makesOffer);
      const cs = getComputedStyle(p), bs = getComputedStyle(b), a = btn[0];
      return { offers, ld: org ? org.makesOffer : null, buttons: btn.length, pri: !!a && a.matches('.btn.pri'),
        extra: [...b.querySelectorAll('form, input, select, textarea, img, svg, picture, figure, blockquote, iframe, video, canvas')].map((e) => e.tagName.toLowerCase()),
        radius: cs.borderRadius, pad: cs.paddingLeft, bandPad: bs.paddingTop + ' ' + bs.paddingBottom, height: Math.round(b.getBoundingClientRect().height),
        btnH: a ? Math.round(a.getBoundingClientRect().height * 10) / 10 : 0, href: a ? a.getAttribute('href') : '', note: words(b.querySelector('.ba small')) }; })()`);
    if (!m) return ["the home page has no #work-with-us band"];
    if (m.buttons !== 1 || !m.pri) out.push(`the band has ${m.buttons} buttons${m.pri ? "" : ", and none is the filled one"}; one filled button is the rule`);
    if (m.extra.length) out.push(`the band carries ${[...new Set(m.extra)].join(", ")}: no form, logo, testimonial or figure`);
    if (m.offers.length !== 4) out.push(`${m.offers.length} offers, not four`);
    m.offers.forEach((o, i) => {
      if (!o.name || !o.does) out.push(`offer ${i + 1} lacks its name or what we do`);
      if (!/^You leave with \S/.test(o.last)) out.push(`offer ${i + 1} ("${o.name}") does not end with "You leave with" and what that is`);
    });
    if (m.note !== "Say what you want to change, and by when.") out.push(`the line beside the button reads "${m.note}"`);
    // the organisation's offers in the page's own words, with nothing on a price
    if (!Array.isArray(m.ld) || m.ld.length !== m.offers.length) out.push(`makesOffer holds ${Array.isArray(m.ld) ? m.ld.length : "no"} offers for ${m.offers.length} on the page`);
    else {
      m.ld.forEach((x, i) => { const s = x.itemOffered || {}, o = m.offers[i];
        if (x["@type"] !== "Offer" || s.name !== o.name || s.description !== o.does || (s.serviceOutput || {}).name !== o.leave)
          out.push(`makesOffer ${i + 1} does not say what the page says ("${s.name}")`); });
      if (/price/i.test(JSON.stringify(m.ld))) out.push("makesOffer names a price");
    }
    if (m.radius !== "20px") out.push(`the panel's radius is ${m.radius}, not 20px`);
    if (w > 1000) {
      if (new Set(m.offers.map((o) => o.top)).size !== 1) out.push(`at ${w} the four offers do not stand in one row`);
      if (![36, 43, 51].some((v) => Math.abs(m.btnH - v) <= 0.5)) out.push(`the button is ${m.btnH}px tall; 36, 43 or 51 at ${w}`);
    } else {
      if (m.height > 1300) out.push(`the band is ${m.height}px tall at ${w}; 1,300 is the limit`);
      if (m.pad !== "20px") out.push(`the panel keeps ${m.pad} inside at ${w}, not 20px`);
      if (m.bandPad !== "48px 48px") out.push(`the band keeps ${m.bandPad} above and below at ${w}, not 48px`);
      m.offers.forEach((o, i) => { if (!o.inline) out.push(`at ${w} "You leave with" is not on the same line as offer ${i + 1}'s words`); });
      if (m.btnH < 44) out.push(`the button is ${m.btnH}px tall at ${w}; 44 at least`);
    }
    // every text on the panel, 4.5:1 on the panel's paper, in both themes
    const CONTRAST = `(() => { const p = document.querySelector('#work-with-us .cx-in'), ctx = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
      const rgb = (s) => { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = s; ctx.fillRect(0, 0, 1, 1); return [...ctx.getImageData(0, 0, 1, 1).data]; };
      const lum = (c) => c.slice(0, 3).map((v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }).reduce((s, v, k) => s + v * [0.2126, 0.7152, 0.0722][k], 0);
      const g = rgb(getComputedStyle(p).backgroundColor), worst = { r: 99 };
      p.querySelectorAll('.eyebrow, h2, .sec-h p:not(.eyebrow), h3, .cx-o p, .cx-k span, small').forEach((e) => { const t = rgb(getComputedStyle(e).color);
        const f = t.slice(0, 3).map((v, k) => (t[3] / 255) * v + (1 - t[3] / 255) * g[k]), L = [lum(f), lum(g)].sort((x, y) => y - x), r = (L[0] + 0.05) / (L[1] + 0.05);
        if (r < worst.r) { worst.r = Math.round(r * 100) / 100; worst.what = e.className || e.tagName.toLowerCase(); } });
      return worst; })()`;
    for (const theme of ["dark", "light"]) {
      if (theme === "light") await evaluate("document.documentElement.setAttribute('data-theme', 'light'), true");
      const c = await evaluate(CONTRAST);
      if (c.r < 4.5) out.push(`in the ${theme} theme ${c.what} is ${c.r}:1 on the panel; 4.5 is the floor`);
    }
    await evaluate("document.documentElement.removeAttribute('data-theme'), true");
    // with script, by real clicks and keys, so focus goes where a reader's would
    const click = async (sel) => {
      const p = await evaluate(`(() => { const e = document.querySelector('${sel}'); scrollTo({ top: e.getBoundingClientRect().top + scrollY - innerHeight / 2, behavior: 'instant' });
        const r = e.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
      await sleep(100);
      for (const type of ["mousePressed", "mouseReleased"]) await send("Input.dispatchMouseEvent", { type, x: p.x, y: p.y, button: "left", clickCount: 1 });
      await sleep(250);
    };
    const escape = async () => {
      for (const type of ["keyDown", "keyUp"]) await send("Input.dispatchKeyEvent", { type, key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
      await sleep(150);
      return evaluate(`[document.querySelector('#sw-contact').classList.contains('on'), !!document.activeElement && document.activeElement.matches('#work-with-us .btn')]`);
    };
    const DRAWER = `(() => { const d = document.querySelector('#sw-contact'), t = document.querySelector('#sw-topic');
      return { on: !!d && d.classList.contains('on') && d.getAttribute('aria-hidden') === 'false', topic: t ? t.value : null,
        first: t ? ([...t.options].find((o) => o.defaultSelected) || {}).value : null, at: location.pathname + location.search + location.hash }; })()`;
    await click("#work-with-us .btn");
    let d = await evaluate(DRAWER);
    if (!d.on) out.push("with script the close's button does not open the contact drawer");
    else {
      if (d.topic !== "consultancy") out.push(`the close's button opens the drawer on the topic "${d.topic}", not the consultancy's`);
      if (d.at !== "/") out.push(`the close's button also went to ${d.at}`);
      const back = await escape();
      if (back[0]) out.push("Escape does not close the drawer");
      else if (!back[1]) out.push("closed, the drawer does not hand focus back to the close's button");
      // the footer's button chooses no topic: the drawer is back on its own first choice, not the close's
      await click(".ft [data-sw-open]");
      d = await evaluate(DRAWER);
      if (!d.on) out.push("the footer's button no longer opens the drawer");
      else if (d.topic !== d.first || d.first === "consultancy") out.push(`the footer's button opens the drawer on "${d.topic}" (its own first choice is "${d.first}")`);
      await escape();
      // the close again, and a message sent from it: its subject is tagged for the consultancy
      await click("#work-with-us .btn");
      const subject = await evaluate(`(async () => { const f = document.querySelector('#sw-contact form');
        if (f.elements.topic.value !== 'consultancy') return 'the topic ' + f.elements.topic.value;
        f.elements.name.value = 'Helen Gate'; f.elements.email.value = 'helen@example.com'; f.elements.message.value = 'A ranked list of our ideas, by June.';
        f.requestSubmit(); await new Promise((r) => setTimeout(r, 300));
        const a = [...document.querySelectorAll('#sw-contact .sw-status a')].find((x) => x.href.startsWith('mailto:'));
        return a ? decodeURIComponent(a.href.split('subject=')[1].split('&')[0]) : 'no mail link'; })()`);
      if (!subject.startsWith("[SkyWays Consultancy]")) out.push(`a message from the close is headed "${subject}", not tagged [SkyWays Consultancy]`);
    }
    // paper: the button prints where it goes
    await send("Emulation.setEmulatedMedia", { media: "print", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "reduce" }] });
    const after = await evaluate(`getComputedStyle(document.querySelector('#work-with-us .btn'), '::after').content`);
    if (!m.href || !after.includes(m.href)) out.push(`on paper the button does not print where it goes (${after})`);
    await send("Emulation.setEmulatedMedia", { media: "", features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "reduce" }] });
    return out;
  }
  // end of home · H8

  const PAGE = ["H10 the page", pageH10];
  const BANDS = [["H3 map", bandH3], ["H4 chooser", bandH4], ["H5 people", bandH5], ["H6 day card", bandH6],
    ["H7 library", bandH7], ["H8 close", bandH8]];
  const out = [];
  thrown.length = 0;
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    for (const [name, check] of [PAGE, ...BANDS]) {
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
  else console.log(`  ok   /  the order and headings of verdict-home 1.0; ${tall[1440].toLocaleString("en-GB")}px tall at 1440 (8,700) and ${tall[390].toLocaleString("en-GB")} at 390 (13,200); ` +
    `a first visit asks for what pass 17 counts; ${BANDS.length} bands, each checked at 1440 x 900 and 390 x 844`);
}

// 20. the forward-deployed engineer guide (council 10): the FDE paper's criteria 3 to 6 on the guide's four pages,
// the hub and its stages Frame, Deliver and Evolve, at 1440, 1024, 390 and 320 wide, in both themes.
//   the figure    twelve step links, each to a step on its own stage's page; four phase columns, their rules in
//                 --dg-slate, --dg-indigo, --dg-teal and --dg-amber (from computed styles), each row's steps under
//                 them, or two by two on a phone; every step's top edge in its phase's hue; a --dg-rose pill under
//                 each open row; stage heads in ink, with no hue; the page's accent nowhere inside
//   fit           no sideways scroll, every step shut or open; no text under 11px; every link in the figure 44px
//                 tall under 760px; the hub's figure 630px tall or less at 1440 with its first two stages on the
//                 first screen, 1,200 at 390 and 1,450 at 320; on a stage page the whole figure on the first screen
//   contrast      every text in the figure, the hub's altitude table, and a step's chips and its two new blocks
//                 (inside your own company, say it like this), 4.5:1 or more on its backdrop (3:1 when large)
//   the modes     without script, and with script under reduced motion, the figure, every step's summary and
//                 every table row are shown, and under reduced motion nothing runs; on paper, the same, and light
//   the links     every link in the guide's rail and page that stays on the site lands on a page, and on an id there
console.log("\n20. the FDE guide: its figure, fit, contrast and modes, on the hub and its three stages");
{
  const GUIDE = "forward-deployed-engineer/", HUB_AND_STAGES = ["", "frame/", "deliver/", "evolve/"];
  const SIZES = [[1440, 900], [1024, 768], [390, 844], [320, 640]];
  // colours as numbers, a backdrop composed up the tree, a contrast ratio, whether a thing can be seen, and the theme
  const KIT = `const root = document.documentElement, phone = matchMedia('(max-width: 760px)').matches;
    const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', { willReadFrequently: true });
    const rgba = (c) => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1);
      const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
    const blend = (t, b, a = t[3]) => [0, 1, 2].map((i) => t[i] * a + b[i] * (1 - a)).concat(1);
    const lum = (c) => c.slice(0, 3).reduce((s, v, i) => { v /= 255; return s + [0.2126, 0.7152, 0.0722][i] * (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4); }, 0);
    const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
    const backdrop = (e) => { const layers = []; for (let a = e; a; a = a.parentElement) { const c = rgba(getComputedStyle(a).backgroundColor);
        if (c[3] > 0) { layers.push(c); if (c[3] >= 1) break; } } return layers.reduceRight((b, c) => blend(c, b), [255, 255, 255, 1]); };
    const same = (a, b) => a[3] > 0.5 && [0, 1, 2].every((i) => Math.abs(a[i] - b[i]) <= 2);
    const said = (e) => { const w = document.createTreeWalker((e.querySelector && e.querySelector('strong')) || e, NodeFilter.SHOW_TEXT), t = [];
      while (w.nextNode()) t.push(w.currentNode.textContent); return t.join(' ').replace(/\\s+/g, ' ').trim().slice(0, 32); };
    const shown = (e) => { const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1 || getComputedStyle(e).visibility === 'hidden') return false;
      for (let a = e; a; a = a.parentElement) { const cs = getComputedStyle(a); if (+cs.opacity < 0.05 || /inset\\([^)]*100%/.test(cs.clipPath)) return false; }
      return true; };
    // a theme is set, then every transition it set off has finished (none under reduced motion), so colours are read at rest
    const theme = async (t) => { if (t === 'light') root.setAttribute('data-theme', 'light'); else root.removeAttribute('data-theme');
      await document.fonts.ready; await new Promise((r) => requestAnimationFrame(() => setTimeout(r, 60)));
      await Promise.race([Promise.all(document.getAnimations().map((a) => a.finished.catch(() => {}))), new Promise((r) => setTimeout(r, 1500))]); };`;
  // what a reader needs, shown: the figure, every step's summary, every table row; under reduced motion, nothing
  // running; on paper, a light page and light boxes
  const SHOWN = (t, mode) => `(async () => { ${KIT}
    await theme('${t}');
    const out = [], fig = document.querySelector('main .fx'), hub = !document.querySelector('main.fx-st');
    if (!fig) return { out: ['the page has no framework figure'] };
    const need = [['step links', '.fx-s a'], ['step names', '.fx-s a strong'], ['stage heads', '.fx-h'], ['signature pills', '.fx-so b'],
      ['steps\\' questions', '.fx-r:not(.fx-m) .fx-s a > span'], ['figure\\'s foot line', '.fx-f'],
      [hub ? 'table rows' : 'brief\\'s rows', hub ? '.fdt tbody tr' : '.fx-b tr']];
    if (!phone) need.push(['phase columns', '.fx-ph > span'], ['steps\\' artefacts', '.fx-r:not(.fx-m) .fx-s em']);
    if (!hub) need.push(['step summaries', 'details.step > summary']);
    for (const [what, sel] of need) { const all = [...document.querySelectorAll(sel)], gone = all.filter((e) => !shown(e));
      if (!all.length) out.push('no ' + what); else if (gone.length) out.push(gone.length + ' of ' + all.length + ' ' + what + ' hidden ("' + said(gone[0]) + '")'); }
    if ('${mode}' === 'reduced') { const run = document.getAnimations().filter((a) => a.playState === 'running');
      const what = (a) => (a.animationName ? 'the animation ' + a.animationName : a.transitionProperty ? 'a transition of ' + a.transitionProperty : 'an animation from script');
      if (run.length) out.push(run.length + ' running under reduced motion (' + what(run[0]) + ')'); }
    if ('${mode}' === 'print') { const dark = [document.body, ...fig.querySelectorAll('.fx-s a')].filter((e) => lum(backdrop(e)) < 0.8);
      if (dark.length) out.push('on paper ' + (dark[0] === document.body ? 'the page' : 'the box "' + said(dark[0]) + '"') + ' is not light'); }
    return { out }; })()`;
  // the figure's form and colours, the fit, the smallest text, and the contrast of the guide's own parts
  const LOOK = (t) => `(async () => { ${KIT}
    scrollTo({ top: 0, behavior: 'instant' }); await theme('${t}');
    const out = [], W = innerWidth, H = innerHeight, fig = document.querySelector('main .fx'), hub = !document.querySelector('main.fx-st');
    if (!fig || document.querySelectorAll('main .fx').length !== 1) return { out: ['the page has no framework figure, or more than one'] };
    const tok = (v) => { const i = document.createElement('i'); i.style.color = 'var(' + v + ')'; fig.appendChild(i); const c = rgba(getComputedStyle(i).color); i.remove(); return c; };
    const HUE = ['--dg-slate', '--dg-indigo', '--dg-teal', '--dg-amber'].map(tok), ROSE = tok('--dg-rose'), INK = tok('--ink'), ACCENT = [tok('--dg-sky'), tok('--accent')];
    const paint = (e) => { const cs = getComputedStyle(e);
      return [cs.color, cs.backgroundColor, cs.borderTopColor, cs.borderRightColor, cs.borderBottomColor, cs.borderLeftColor].map(rgba); };
    // the figure: three stages, each P0 to P3; twelve links; the hues on the columns only
    const rows = [...fig.querySelectorAll('.fx-g > li')], heads = rows.map((r) => r.querySelector('.fx-h')), links = [...fig.querySelectorAll('.fx-s a')];
    const open = rows.filter((r) => !r.classList.contains('fx-m')), phase = (a) => (a.querySelector('i b') || {}).textContent || '';
    if (rows.length !== 3 || heads.some((h) => !h)) out.push('the figure has ' + rows.length + ' stages with heads, not three');
    if (links.length !== 12) out.push('the figure has ' + links.length + ' step links, not twelve');
    if (open.length !== (hub ? 3 : 1)) out.push(open.length + ' of the figure\\'s rows are open; ' + (hub ? 'the hub opens all three' : 'a stage page opens its own'));
    rows.forEach((r, k) => { const p = [...r.querySelectorAll('.fx-s a')].map(phase).join(' ');
      if (p !== 'P0 P1 P2 P3') out.push('stage ' + (k + 1) + '\\'s steps run ' + (p || 'nowhere') + ', not P0 to P3'); });
    links.forEach((a) => { const h = HUE[+phase(a).slice(1)];
      if (!h || !same(rgba(getComputedStyle(a).borderTopColor), h)) out.push('step "' + said(a) + '" has no top edge in its phase\\'s hue'); });
    const cols = [...fig.querySelectorAll('.fx-ph > [class^=p]')];
    if (!phone) {
      if (cols.length !== 4) out.push('the figure has ' + cols.length + ' phase columns, not four');
      cols.forEach((c, k) => { const cs = getComputedStyle(c);
        if (!HUE[k] || parseFloat(cs.borderBottomWidth) < 2 || !same(rgba(cs.borderBottomColor), HUE[k])) out.push('column ' + (k + 1) + '\\'s rule is not drawn in --dg-' + ['slate', 'indigo', 'teal', 'amber'][k]); });
      rows.forEach((r, k) => [...r.querySelectorAll('.fx-s a')].forEach((a, j) => {
        if (cols[j] && Math.abs(a.getBoundingClientRect().left - cols[j].getBoundingClientRect().left) > 2) out.push('stage ' + (k + 1) + '\\'s step ' + (j + 1) + ' is not under its column'); }));
    } else rows.forEach((r, k) => { const b = [...r.querySelectorAll('.fx-s a')].map((a) => a.getBoundingClientRect());
      const square = Math.abs(b[0].top - b[1].top) < 2 && Math.abs(b[2].top - b[3].top) < 2 && b[2].top > b[0].top && b[1].left > b[0].left && Math.abs(b[2].left - b[0].left) < 2;
      if (b.length === 4 && !square) out.push('on a phone stage ' + (k + 1) + '\\'s steps are not two by two'); });
    const pills = [...fig.querySelectorAll('.fx-so b')];
    if (pills.length !== open.length) out.push(pills.length + ' signature pills under ' + open.length + ' open rows');
    pills.forEach((b) => { if (!same(rgba(getComputedStyle(b).backgroundColor), ROSE)) out.push('a signature pill is not --dg-rose'); });
    heads.filter(Boolean).forEach((h) => { const hued = [h, ...h.querySelectorAll('*')].some((e) => paint(e).some((c) => [...HUE, ROSE, ...ACCENT].some((x) => same(c, x))));
      if (hued || !h.querySelector('strong') || !same(rgba(getComputedStyle(h.querySelector('strong')).color), INK)) out.push('the head of "' + said(h) + '" is not in ink'); });
    const sky = [...fig.querySelectorAll('*')].find((e) => paint(e).some((c) => ACCENT.some((x) => same(c, x))));
    if (sky) out.push('the page\\'s accent is drawn inside the figure ("' + said(sky) + '")');
    // the fit
    const over = () => root.scrollWidth - root.clientWidth, box = fig.getBoundingClientRect(), figH = Math.round(box.height);
    if (over() > 0) out.push('the page scrolls sideways by ' + over() + 'px');
    if (hub && W === 1440) { if (figH > 630) out.push('the figure is ' + figH + 'px tall; 630 is the most');
      const two = Math.round(rows[1] ? rows[1].getBoundingClientRect().bottom + scrollY : 1e4); if (two > H) out.push('the first two stages end at ' + two + 'px, below the first screen'); }
    if (hub && W === 390 && figH > 1200) out.push('the figure is ' + figH + 'px tall; 1200 is the most');
    if (hub && W === 320 && figH > 1450) out.push('the figure is ' + figH + 'px tall; 1450 is the most');
    if (!hub && W === 1440 && box.bottom + scrollY > H) out.push('the figure ends at ' + Math.round(box.bottom + scrollY) + 'px, below the first screen');
    if (phone) { const short = [...fig.querySelectorAll('a')].filter((a) => a.getBoundingClientRect().height < 44);
      if (short.length) out.push(short.length + ' links in the figure under 44px tall ("' + said(short[0]) + '", ' + Math.round(short[0].getBoundingClientRect().height) + 'px)'); }
    // every step open, then the sideways scroll again, the smallest text on the page, and the contrast; the steps
    // are put back as they were served before the next theme is measured
    const served = [...document.querySelectorAll('details.step')].map((d) => d.open);
    root.classList.add('all-open'); document.querySelectorAll('details.step').forEach((d) => { d.open = true; });
    await new Promise((r) => requestAnimationFrame(() => setTimeout(r, 60)));
    if (over() > 0) out.push('with every step open the page scrolls sideways by ' + over() + 'px');
    // each text: an element's own words, or the words its ::before draws (a stacked table's column names)
    const texts = (els) => { const t = []; for (const e of els) { if (!e.getClientRects().length || e.closest('.vh, svg')) continue;
        const cs = getComputedStyle(e); if (cs.visibility === 'hidden') continue;
        if ([...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) t.push([e, cs, said(e)]);
        const b = getComputedStyle(e, '::before'); if (b.content && !/^(none|normal|""|'')$/.test(b.content)) t.push([e, b, b.content.slice(1, 33).replace(/"$/, '')]); }
      return t; };
    let small = { px: 99 };
    for (const [, cs, words] of texts(document.body.querySelectorAll('*'))) { const px = parseFloat(cs.fontSize); if (px < small.px) small = { px, words }; }
    if (small.px < 11) out.push('text at ' + small.px + 'px ("' + small.words + '"); 11 is the least');
    const parts = hub ? [['the altitude table', '.fx-al']] : [['chips', '.fhat'], ['inside your own company', 'section:has(> .fint)'], ['say it like this', 'section:has(> .fsay)']];
    const scope = [fig];
    for (const [what, sel] of parts) { const got = [...document.querySelectorAll('main ' + sel)]; if (!got.length) out.push('no ' + what + ' to measure'); scope.push(...got); }
    const steps = document.querySelectorAll('main details.step').length;
    if (!hub && ['.fhat', '.fint', '.fsay'].some((s) => document.querySelectorAll('main ' + s).length !== steps)) out.push('a step without its chips or its two new blocks');
    let low = 99; const faint = [];
    for (const [e, cs, words] of texts(scope.flatMap((s) => [s, ...s.querySelectorAll('*')]))) {
      let fade = 1; for (let a = e; a; a = a.parentElement) fade *= +getComputedStyle(a).opacity;
      const bg = backdrop(e), r = ratio(blend(blend(rgba(cs.color), bg), bg, fade), bg), px = parseFloat(cs.fontSize);
      low = Math.min(low, r);
      if (r < (px >= 24 || (px >= 18.66 && +cs.fontWeight >= 700) ? 3 : 4.5)) faint.push({ r, words, px });
    }
    if (faint.length) { const f = faint.sort((a, b) => a.r - b.r)[0]; out.push(faint.length + ' texts under 4.5:1, the faintest ' + f.r.toFixed(2) + ':1 on "' + f.words + '" (' + f.px + 'px)'); }
    document.querySelectorAll('details.step').forEach((d, i) => { d.open = served[i]; }); root.classList.remove('all-open');
    await new Promise((r) => requestAnimationFrame(() => setTimeout(r, 60)));
    return { out, figH, low: +low.toFixed(2), small: small.px };
  })()`;
  // every link in the guide's rail and page that stays on the site: a page that exists, and its id; the figure's
  // twelve each to a step on its own stage's page
  const LANDS = `(async () => {
    const out = [], here = location.origin + location.pathname, docs = new Map([[here, Promise.resolve(document)]]);
    const page = (u) => { if (!docs.has(u)) docs.set(u, fetch(u).then((r) => (r.ok ? r.text() : null))
      .then((t) => t && new DOMParser().parseFromString(t, 'text/html')).catch(() => null)); return docs.get(u); };
    for (const row of document.querySelectorAll('main .fx .fx-g > li')) {
      const head = row.querySelector('.fx-h'), at = head && head.href ? new URL(head.href).pathname : location.pathname;
      for (const a of row.querySelectorAll('.fx-s a')) { const u = new URL(a.href), d = await page(u.origin + u.pathname), id = decodeURIComponent(u.hash.slice(1));
        const t = d && id ? d.getElementById(id) : null;
        if (u.pathname !== at || !t || !t.matches('details.step'))
          out.push('the figure\\'s "' + (a.querySelector('strong') || a).textContent + '" goes to ' + a.getAttribute('href') + ', not to a step on its stage\\'s page'); } }
    const links = [...document.querySelectorAll('.cols a[href]')].filter((a) => new URL(a.href).origin === location.origin);
    for (const a of links) { const u = new URL(a.href), d = await page(u.origin + u.pathname), id = decodeURIComponent(u.hash.slice(1));
      if (!d) out.push(a.getAttribute('href') + ' leads to no page'); else if (id && !d.getElementById(id)) out.push(a.getAttribute('href') + ' leads to no id on its page'); }
    return { out: [...new Set(out)], n: links.length };
  })()`;
  const seen = new Map(), stat = { fig: {}, low: 99, small: 99, links: 0 };
  const note = (p, where, problems) => { for (const m of problems) { const k = `/${GUIDE}${p}  ${m}`; if (!seen.has(k)) seen.set(k, []); if (where) seen.get(k).push(where); } };
  const ask = (expression) => evaluate(expression).catch((e) => ({ out: ["the check itself failed: " + e.message.slice(0, 160)] }));
  const media = (o) => send("Emulation.setEmulatedMedia", { media: o.print ? "print" : "", features: [{ name: "prefers-color-scheme", value: "dark" },
    { name: "prefers-reduced-motion", value: o.reduce ? "reduce" : "no-preference" }] });
  const load = async (p, noscript, wait) => {
    await send("Emulation.setScriptExecutionDisabled", { value: noscript });
    await send("Page.navigate", { url: BASE + GUIDE + p });
    await sleep(wait);
    await send("Emulation.setScriptExecutionDisabled", { value: false });   // the check itself needs script
    return evaluate(LOADED);
  };
  thrown.length = 0;
  for (const p of HUB_AND_STAGES) {
    for (const [w, h] of SIZES) {
      await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 600 });
      await media({});
      if (!(await load(p, true, 1000))) { note(p, `${w}`, ["did not load without script"]); continue; }
      for (const t of ["dark", "light"]) note(p, `${w} ${t}, no script`, (await ask(SHOWN(t, ""))).out);
      await media({ reduce: true });
      if (!(await load(p, false, 900))) { note(p, `${w}`, ["did not load"]); continue; }
      for (const t of ["dark", "light"]) {
        note(p, `${w} ${t}`, (await ask(SHOWN(t, "reduced"))).out);
        const m = await ask(LOOK(t));
        note(p, `${w} ${t}`, m.out);
        if (m.figH && (!p || w === 1440)) stat.fig[`${p || "the hub "}${w}`] = m.figH;
        if (m.low) stat.low = Math.min(stat.low, m.low);
        if (m.small) stat.small = Math.min(stat.small, m.small);
      }
      if (w === 1440) { const l = await ask(LANDS); note(p, "", l.out); stat.links += l.n || 0; }
    }
    // on paper, from either theme: the same things shown, and the page light
    await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
    await media({ print: true, reduce: true });
    if (!(await load(p, false, 900))) note(p, "print", ["did not load"]);
    else for (const t of ["dark", "light"]) note(p, `print, ${t}`, (await ask(SHOWN(t, "print"))).out);
  }
  await media({});
  const out = [...seen].map(([k, where]) => (where.length ? `${k} (at ${where.join(", ")})` : k));
  if (thrown.length) out.push("script error: " + thrown[0]);
  if (out.length) { failures += out.length; console.log("  FAIL  " + out.join("; ")); }
  else console.log(`  ok   4 pages at 4 widths in both themes; the hub's figure ${stat.fig["the hub 1440"]}px tall at 1440 (630), ` +
    `${stat.fig["the hub 390"]} at 390 (1200), ${stat.fig["the hub 320"]} at 320 (1450); the smallest text ${stat.small}px; the lowest contrast ` +
    `${stat.low}:1; ${stat.links} links land`);
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
console.log(failures ? `\n${failures} failure(s)` : "\nall twenty passes hold");
process.exit(failures ? 1 : 0);
