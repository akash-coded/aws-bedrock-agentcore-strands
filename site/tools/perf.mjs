// The performance sheet: what the manual's pages cost a reader, measured on two builds side by side, the build
// before a round and the round's own. It is not part of the gate. Bytes are held by accept.mjs (pass 17) and the
// hero's frame by pass 13; timing moves too much between loads to fail a build on (council 10 saw first paint vary
// by 0.4s), so it is read here, as medians and as after against before, before a release.
//
//   git worktree add --detach /tmp/before <the last commit before the round>
//   (cd /tmp/before && python3.12 site/build.py)            the build before, in /tmp/before/site/_site
//   python3.12 site/build.py                                 the round's build, in site/_site
//   node site/tools/perf.mjs --before /tmp/before/site/_site --after site/_site --out /tmp/perf --only bytes
//   ... then --only paint, --only hero, --only minute and --only scroll, one at a time
//   node site/tools/perf.mjs --table --out /tmp/perf         the table again from the saved numbers, no browser
//
// Each section runs alone with --only (a list, comma-separated, runs several) and takes under ten minutes. On a
// machine that other runs share, the four timed ones need it to themselves: run each under an exclusive lock
// (`flock /tmp/claude-0/chrome.lock node site/tools/perf.mjs ... --only paint`); bytes can share it.
//
//   bytes   everything a first visit to each kind of page asks for, scrolled to its end, at 1440 x 900 and at
//           390 x 844: the home page, a lesson, the simulator, the workbench, the FDE guide, a role page and a
//           lab. Raw, and gzipped at level 9 from the built files as pass 17 counts (a font or a picture counts as
//           it is; a KB is 1,024 bytes), and what crossed the wire.
//   paint   the home page with the cache empty, five loads a setting: first paint, largest paint and its element,
//           the hero's first frame and the fonts; at 1440 x 900 at full speed, and at 390 x 844 at 3x with the
//           processor slowed 4x on council 9's slow 4G (150ms, 1.6 Mbps) and on DevTools' Slow 4G (562.5ms,
//           1.44 Mbps).
//   hero    the hero drawn in software, as pass 13 measures it: at 1280 x 800 and at 390 x 844 at 3x, slowed 4x,
//           in the first seconds after load and in steady flight: its script a frame (window.GlobeMs), its frames
//           in three seconds, the worst gap between them, the worst of twelve taps on the headline, the main
//           thread's share.
//   minute  seventy seconds on the home page's first screen, 390 x 844 at 3x slowed 4x: main-thread time
//           (Performance.getMetrics) and the hero's frames, on a first visit in the sitting and on a later one.
//   scroll  five flicks down the whole home page with the processor slowed 4x, at 390 x 844 at 3x and at
//           1440 x 900: the gaps between frames, over the whole flick and once the hero has left the screen, the
//           main thread's share and layout shift. The flick is a wheel: headless Chrome does not scroll for a
//           synthetic touch.
//
// It serves each build itself as GitHub Pages does (gzip, max-age=600, the query string ignored) on a port the
// system gives it, so a page is timed as it is sent and nothing else needs to be running. The cache is off, so
// every load asks for every file; a later visit differs from a first only by what the page kept in sessionStorage.
// Where time is measured, before and after take turns (before, after, before, after), so a slow moment on the
// machine falls on both. The machine's own speed moves (on 3 October 2026 a container restart made Chrome's
// drawing in software about twice as slow), so each bar is judged against before as measured in the same run,
// keeping council 10's ratio, and every absolute number is printed beside it. Each section saves its numbers to
// <out>/<section>.json; every run then writes the table of the sections saved so far to <out>/perf.md and all the
// numbers to <out>/perf.json, and prints the table.

import { createServer } from "node:net";
import { createServer as createHttpServer } from "node:http";
import { spawn, execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync, statSync, mkdirSync, rmSync } from "node:fs";
import { gzipSync } from "node:zlib";
import { tmpdir, loadavg, cpus } from "node:os";
import { join, resolve, extname, sep } from "node:path";

const SECTIONS = ["bytes", "paint", "hero", "minute", "scroll"];
const argv = process.argv.slice(2);
const opt = (k) => { const i = argv.indexOf(`--${k}`); return i >= 0 ? argv[i + 1] : undefined; };
const usage = (why) => {
  console.error(`${why}\nusage: node perf.mjs --before <built site> --after <built site> [--only ${SECTIONS.join("|")}] [--out <dir>] [--runs <n>] [--seconds <n>]\n       node perf.mjs --table [--out <dir>]`);
  process.exit(2);
};
const OUT = resolve(opt("out") || join(tmpdir(), "perf"));
const ONLY = (opt("only") || SECTIONS.join(",")).split(",").map((s) => s.trim()).filter(Boolean);
const RUNS = opt("runs") ? Math.max(1, +opt("runs")) : null;      // loads of each build a setting; each section has its own default
const SECONDS = Math.max(5, +(opt("seconds") || 70));             // the minute section's length
const TABLE = argv.includes("--table");
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const say = (s) => console.log(s);

if (ONLY.some((s) => !SECTIONS.includes(s))) usage(`no section called ${ONLY.filter((s) => !SECTIONS.includes(s)).join(", ")}`);
if (!TABLE) for (const k of ["before", "after"]) if (!opt(k) || !existsSync(join(opt(k), "index.html"))) usage(`--${k} must name a built site: a folder with index.html`);

// The kinds of page. Each lists its addresses in order and takes the first a build has: the FDE guide had no page
// of its own before council 10, and the lesson the home page linked for it stood in its place.
const KINDS = [
  { id: "home", what: "The home page", paths: [""] },
  { id: "lesson", what: "A lesson", paths: ["learn/the-hard-gate/"] },
  { id: "simulator", what: "The simulator", paths: ["simulator/"] },
  { id: "workbench", what: "The workbench", paths: ["workbench/"] },
  { id: "fde", what: "The FDE guide", paths: ["forward-deployed-engineer/", "learn/ai-dlc-for-forward-deployed-engineers/"] },
  { id: "role", what: "A role page", paths: ["product-manager/"] },
  { id: "lab", what: "A lab", paths: ["labs/grow-the-spec/"] },
];

// ---------------------------------------------------------------- the builds, served as GitHub Pages serves them

const BLANK = "__perf_blank__";     // a page with no script on each build's own origin: where each timed load starts
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8", ".json": "application/json", ".svg": "image/svg+xml", ".xml": "application/xml",
  ".txt": "text/plain; charset=utf-8", ".md": "text/markdown; charset=utf-8", ".webmanifest": "application/manifest+json",
  ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif", ".avif": "image/avif",
  ".ico": "image/x-icon", ".woff2": "font/woff2", ".woff": "font/woff", ".pdf": "application/pdf", ".mp4": "video/mp4" };
const ZIPPED = /^(text\/|application\/(json|xml|manifest\+json)|image\/svg\+xml)/;
const cleanup = [];

function build(dir) {
  const root = resolve(dir), git = (...a) => execFileSync("git", ["-C", root, ...a], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
  let commit = null, dirty = null;
  try { commit = git("rev-parse", "--short", "HEAD"); dirty = git("status", "--porcelain", "--untracked-files=no") !== ""; } catch {}
  return { root, commit, dirty };
}

async function serve(root) {
  const zipped = new Map();
  const server = createHttpServer((req, res) => {
    let path;
    try { path = decodeURIComponent(new URL(req.url, "http://localhost").pathname); } catch { res.writeHead(400); res.end(); return; }
    if (path === `/${BLANK}`) { res.writeHead(200, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" }); res.end("<!doctype html><title>blank</title><link rel=icon href=\"data:,\">"); return; }   // its own icon, or the browser asks for /favicon.ico
    let file = join(root, path), status = 200;
    if (file !== root && !file.startsWith(root + sep)) { res.writeHead(403); res.end(); return; }
    if (existsSync(file) && statSync(file).isDirectory()) {
      if (!path.endsWith("/")) { res.writeHead(301, { location: encodeURI(path + "/") }); res.end(); return; }
      file = join(file, "index.html");
    }
    if (!existsSync(file)) { status = 404; file = join(root, "404.html"); }
    if (!existsSync(file)) { res.writeHead(404, { "content-type": "text/plain" }); res.end("not found"); return; }
    const type = TYPES[extname(file).toLowerCase()] || "application/octet-stream", headers = { "content-type": type, "cache-control": "max-age=600" };
    let body = readFileSync(file);
    if (ZIPPED.test(type) && /\bgzip\b/.test(req.headers["accept-encoding"] || "")) {
      if (!zipped.has(file)) zipped.set(file, gzipSync(body, { level: 6 }));
      body = zipped.get(file); headers["content-encoding"] = "gzip"; headers.vary = "Accept-Encoding";
    }
    headers["content-length"] = body.length;
    res.writeHead(status, headers); res.end(req.method === "HEAD" ? undefined : body);
  });
  const port = await new Promise((ok) => server.listen(0, "127.0.0.1", () => ok(server.address().port)));
  cleanup.push(() => server.close());
  return { url: `http://127.0.0.1:${port}/`, root };
}

// ---------------------------------------------------------------- headless Chrome over the DevTools protocol

async function browser() {
  const port = await new Promise((ok) => { const s = createServer().listen(0, "127.0.0.1", () => { const p = s.address().port; s.close(() => ok(p)); }); });   // a port no other Chrome holds, so a run never drives another run's browser
  const profile = join(tmpdir(), `perf-${port}`);
  const proc = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
    "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
  const kill = () => { try { proc.kill("SIGKILL"); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} };
  cleanup.push(kill);
  let wsurl, version = "";
  for (let i = 0; i < 120 && !wsurl; i++) {
    try { wsurl = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === "page")?.webSocketDebuggerUrl; } catch {}
    if (!wsurl) await sleep(250);
  }
  if (!wsurl) throw new Error(`Chrome did not start (CHROME=${CHROME})`);
  try { version = (await (await fetch(`http://127.0.0.1:${port}/json/version`)).json()).Browser; } catch {}
  const ws = new WebSocket(wsurl);
  await new Promise((ok, no) => { ws.addEventListener("open", ok, { once: true }); ws.addEventListener("error", no, { once: true }); });
  let seq = 0;
  const waiting = new Map(), listeners = new Set();
  ws.addEventListener("message", (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && waiting.has(m.id)) { const w = waiting.get(m.id); waiting.delete(m.id); w(m); }
    else if (m.method) for (const f of [...listeners]) f(m);
  });
  const send = (method, params = {}, ms = 120000) => new Promise((ok, no) => {
    const id = ++seq, timer = setTimeout(() => { waiting.delete(id); no(new Error(`${method} had no answer in ${ms / 1000}s`)); }, ms);
    waiting.set(id, (m) => { clearTimeout(timer); if (m.error) no(new Error(`${method}: ${m.error.message}`)); else ok(m.result || {}); });
    ws.send(JSON.stringify({ id, method, params }));
  });
  const evaluate = async (expression, ms) => {
    const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true }, ms);
    if (r.exceptionDetails) throw new Error(`in the page: ${r.exceptionDetails.exception?.description || r.exceptionDetails.text}`);
    return r.result.value;
  };
  const on = (f) => { listeners.add(f); return () => listeners.delete(f); };
  const waitFor = (method, ms) => new Promise((ok) => {
    let off = null;
    const timer = setTimeout(() => { off(); ok(null); }, ms);
    off = on((m) => { if (m.method === method) { clearTimeout(timer); off(); ok(m); } });
  });
  for (const d of ["Page", "Runtime", "Performance", "Network"]) await send(`${d}.enable`);
  await send("Network.setCacheDisabled", { cacheDisabled: true });
  const close = async () => {
    try { ws.close(); } catch {}
    const gone = new Promise((ok) => proc.once("exit", ok));
    proc.kill(); await Promise.race([gone, sleep(4000)]); kill();
  };
  return {
    send, evaluate, on, waitFor, version, close,
    cpu: (rate) => send("Emulation.setCPUThrottlingRate", { rate }),
    net: (n) => send("Network.emulateNetworkConditions", n ? { offline: false, latency: n.latency, downloadThroughput: n.down, uploadThroughput: n.up }
      : { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 }),
    screen: async (w, h, dpr, mobile) => {
      await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: dpr, mobile });
      await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: "dark" }, { name: "prefers-reduced-motion", value: "no-preference" }] });
    },
    busy: async () => (await send("Performance.getMetrics")).metrics.find((m) => m.name === "TaskDuration").value * 1000,   // the renderer's main thread, ms
  };
}

// a navigation that returns once the page has loaded, or after ms if it never does (null then)
async function go(B, url, ms = 30000) {
  const loaded = B.waitFor("Page.loadEventFired", ms);
  const r = await B.send("Page.navigate", { url });
  if (r.errorText) throw new Error(`${url}: ${r.errorText}`);
  return loaded;
}

// Every load starts from the same place: about:blank, whose renderer starts its counters near zero, then the blank
// page on the build's own origin, where a first visit clears what a later one would find (the head's script marks
// a visit in sessionStorage, and a later visit skips the hero's entrance).
async function start(B, site, first) {
  await go(B, "about:blank", 5000);
  await go(B, site.url + BLANK, 10000);
  if (first) await B.evaluate("(() => { try { sessionStorage.clear(); localStorage.clear(); } catch (e) {} return true; })()");
}

const med = (a) => { const v = a.filter((x) => typeof x === "number" && !Number.isNaN(x)).sort((p, q) => p - q); if (!v.length) return null; const k = v.length >> 1; return v.length % 2 ? v[k] : (v[k - 1] + v[k]) / 2; };
const mean = (a) => { const v = a.filter((x) => typeof x === "number"); return v.length ? v.reduce((p, q) => p + q, 0) / v.length : null; };
const kb = (n) => (n / 1024).toLocaleString("en-GB", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

// ---------------------------------------------------------------- 1. bytes

const TEXT = /\.(html|css|js|mjs|json|svg|xml|txt|md|webmanifest|csv)$/i;
const weighed = new Map();
function weigh(file) {
  if (!weighed.has(file)) { const b = readFileSync(file); weighed.set(file, { raw: b.length, gz9: TEXT.test(file) ? gzipSync(b, { level: 9 }).length : b.length }); }
  return weighed.get(file);
}
const TO_THE_END = `(async () => { const wait = (ms) => new Promise((r) => setTimeout(r, ms)), d = document.documentElement;
  for (let y = 0, i = 0; y < d.scrollHeight - innerHeight && i < 400; i++) { y += Math.round(innerHeight * 0.8); scrollTo({ top: y, behavior: 'instant' }); await wait(150); }
  scrollTo({ top: d.scrollHeight, behavior: 'instant' }); await wait(600); return Math.round(scrollY); })()`;

async function bytes(B, sites) {
  const loads = [];
  for (const [w, h, dpr, mobile] of [[1440, 900, 1, false], [390, 844, 3, true]]) {
    await B.screen(w, h, dpr, mobile);
    for (const kind of KINDS) for (const which of ["before", "after"]) {
      const site = sites[which], path = kind.paths.find((p) => existsSync(join(site.root, p, "index.html")));
      if (path === undefined) { loads.push({ kind: kind.id, which, w, path: null }); say(`  ${w} ${which.padEnd(6)} ${kind.id}: not built`); continue; }
      await start(B, site, true);
      const reqs = new Map();
      let scrolled = false;
      const off = B.on((m) => {
        const p = m.params, r = p && reqs.get(p.requestId);
        if (m.method === "Network.requestWillBeSent" && /^https?:/.test(p.request.url)) {
          // a redirect keeps its id: the request is counted once, at the address it ended on
          reqs.set(p.requestId, { ...r, url: p.request.url, type: p.type || r?.type, scroll: r ? r.scroll : scrolled });
        } else if (m.method === "Network.responseReceived" && r) Object.assign(r, { status: p.response.status, type: p.type || r.type });
        else if (m.method === "Network.loadingFinished" && r) Object.assign(r, { wire: p.encodedDataLength, done: true });
        else if (m.method === "Network.loadingFailed" && r) Object.assign(r, { failed: p.errorText, done: true });
      });
      const quiet = async (cap) => {      // no request in flight, and none new for a second
        let n = -1, since = Date.now();
        for (const t0 = Date.now(); Date.now() - t0 < cap; await sleep(100)) {
          if (reqs.size !== n || [...reqs.values()].some((r) => !r.done)) { n = reqs.size; since = Date.now(); } else if (Date.now() - since >= 1000) return;
        }
      };
      await go(B, site.url + path, 30000);
      await quiet(15000);
      scrolled = true;
      await B.evaluate(TO_THE_END, 90000);
      await quiet(15000);
      off();
      const origin = new URL(site.url).origin, files = new Map(), external = [], missing = [];
      for (const r of reqs.values()) {
        const u = new URL(r.url);
        if (u.origin !== origin) { external.push({ url: r.url, wire: r.wire || 0, failed: r.failed || null }); continue; }
        let p = decodeURIComponent(u.pathname).slice(1);
        if (p === BLANK) continue;
        if (p === "" || p.endsWith("/")) p += "index.html";
        const f = join(site.root, p);
        if (r.failed || !existsSync(f) || statSync(f).isDirectory()) { missing.push(p); continue; }
        if (files.has(p)) { files.get(p).asked++; continue; }      // the same file asked for twice is counted once, as a reader's cache would
        files.set(p, { path: p, type: r.type || "Other", ...weigh(f), wire: r.wire || 0, scroll: r.scroll, asked: 1 });
      }
      const list = [...files.values()].sort((a, b) => b.gz9 - a.gz9), sum = (k) => list.reduce((n, f) => n + f[k], 0);
      const html = files.get(path + "index.html");
      const load = { kind: kind.id, which, w, path, n: list.length, raw: sum("raw"), gz9: sum("gz9"), wire: sum("wire"), html: html ? html.gz9 : null,
        onScroll: list.filter((f) => f.scroll).length, files: list, external, missing };
      loads.push(load);
      say(`  ${w} ${which.padEnd(6)} ${kind.id.padEnd(9)} /${path}: ${load.n} files, ${kb(load.raw)} KB raw, ${kb(load.gz9)} KB gzipped, ${kb(load.wire)} KB on the wire` +
        `${load.onScroll ? `, ${load.onScroll} asked for on scrolling` : ""}${external.length ? `, ${external.length} to other hosts` : ""}${missing.length ? `; missing: ${missing.join(", ")}` : ""}`);
    }
  }
  return { loads };
}

// ---------------------------------------------------------------- 2. paint

const NETS = { c9: { latency: 150, down: 1.6e6 / 8, up: 750e3 / 8 }, slow4g: { latency: 562.5, down: 1.44e6 / 8, up: 675e3 / 8 } };
const PAINTS = [
  { id: "desktop", what: "1440 x 900, full speed", w: 1440, h: 900, dpr: 1, mobile: false, net: null, cpu: 1 },
  { id: "c9", what: "390 x 844 at 3x, council 9's slow 4G, processor 4x", w: 390, h: 844, dpr: 3, mobile: true, net: NETS.c9, cpu: 4 },
  { id: "slow4g", what: "390 x 844 at 3x, DevTools' Slow 4G, processor 4x", w: 390, h: 844, dpr: 3, mobile: true, net: NETS.slow4g, cpu: 4 },
];
// installed before any of the page's scripts: the largest paint and its element, layout shift, long tasks, the
// hero's first frame and the fonts
const WATCH_PAINT = `(() => { const m = window.__perf = { lcp: 0, lcpEl: '', lcpH1: false, cls: 0, hero: 0, fonts: 0, longs: [] };
  const name = (e) => e.tagName.toLowerCase() + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\\s+/)[0] : '') + ' "' + (e.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 28) + '"';
  try { new PerformanceObserver((l) => { for (const e of l.getEntries()) { m.lcp = e.startTime; m.lcpEl = e.element ? name(e.element) : (e.url || '').split('/').pop(); m.lcpH1 = !!(e.element && e.element.closest('h1')); } }).observe({ type: 'largest-contentful-paint', buffered: true }); } catch (e) {}
  try { new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) m.cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); } catch (e) {}
  try { new PerformanceObserver((l) => { for (const e of l.getEntries()) m.longs.push([Math.round(e.startTime), Math.round(e.duration)]); }).observe({ type: 'longtask', buffered: true }); } catch (e) {}
  const poll = () => { if (window.GlobeMs && window.GlobeMs.n > 0) m.hero = performance.now(); else if (performance.now() < 30000) requestAnimationFrame(poll); };
  requestAnimationFrame(poll);
  if (document.fonts) document.fonts.ready.then(() => { m.fonts = performance.now(); }); })();`;
const SETTLED = `new Promise((ok) => { const t0 = performance.now(), m = window.__perf || {};
  const look = () => ((m.fonts > 0 && (m.hero > 0 || !document.querySelector('[data-globe]'))) || performance.now() - t0 > 20000 ? ok(true) : setTimeout(look, 100)); look(); })`;
const READ_PAINT = `(() => { const m = window.__perf || {}, p = {}, res = {}; performance.getEntriesByType('paint').forEach((e) => { p[e.name] = e.startTime; });
  const n = performance.getEntriesByType('navigation')[0] || {}, fcp = p['first-contentful-paint'] || 0;
  performance.getEntriesByType('resource').forEach((r) => { const k = r.name.replace(/[?#].*/, '').split('/').pop(); if (!(k in res)) res[k] = Math.round(r.responseEnd); });
  const tbt = (m.longs || []).filter(([s, d]) => s + d > fcp).reduce((a, [s, d]) => a + Math.max(0, d - 50), 0);
  return { fp: Math.round(p['first-paint'] || 0), fcp: Math.round(fcp), lcp: Math.round(m.lcp || 0), lcpEl: m.lcpEl || '', lcpH1: !!m.lcpH1, hero: Math.round(m.hero || 0),
    fonts: Math.round(m.fonts || 0), cls: +(m.cls || 0).toFixed(4), html: Math.round(n.responseEnd || 0), dcl: Math.round(n.domContentLoadedEventEnd || 0),
    load: Math.round(n.loadEventEnd || 0), longTasks: (m.longs || []).length, tbt: Math.round(tbt), res }; })()`;

async function paint(B, sites) {
  const runs = RUNS || 5, settings = {};
  const { identifier } = await B.send("Page.addScriptToEvaluateOnNewDocument", { source: WATCH_PAINT });
  for (const s of PAINTS) {
    settings[s.id] = { what: s.what, before: [], after: [] };
    await B.screen(s.w, s.h, s.dpr, s.mobile);
    for (let r = 0; r < runs; r++) for (const which of ["before", "after"]) {
      await B.cpu(1); await B.net(null);
      await start(B, sites[which], true);
      await B.net(s.net); await B.cpu(s.cpu);
      await go(B, sites[which].url, 40000);
      await B.evaluate(SETTLED, 40000).catch(() => null);
      await sleep(1500);                                    // a later, larger paint would still be reported
      const m = await B.evaluate(READ_PAINT);
      await B.cpu(1); await B.net(null);
      settings[s.id][which].push(m);
      say(`  ${s.id.padEnd(7)} ${which.padEnd(6)} first paint ${m.fcp}ms, largest ${m.lcp}ms (${m.lcpEl}), the hero's first frame ${m.hero}ms, fonts ${m.fonts}ms, load ${m.load}ms`);
    }
  }
  await B.send("Page.removeScriptToEvaluateOnNewDocument", { identifier });
  return { settings };
}

// ---------------------------------------------------------------- 3. the hero

// Pass 13's own measure (check 6): from the hero's frames as it counts them (window.GlobeMs), three seconds of
// frames, the worst gap between two of them, its script a frame, and twelve taps on the headline, each timed from
// the tap to its handler. The heap is collected before each window, so no window pays for the garbage of the last.
const WATCH_HERO = `(() => { const R = window.__cost = { t: [], taps: [], n0: window.GlobeMs.n, sum0: window.GlobeMs.sum, t0: performance.now(), on: true };
  let last = window.GlobeMs.n;
  const loop = (ts) => { if (!R.on) return; if (window.GlobeMs.n !== last) { R.t.push(ts); last = window.GlobeMs.n; } requestAnimationFrame(loop); };
  requestAnimationFrame(loop);
  const h1 = document.querySelector('.hero2 h1') || document.querySelector('h1');
  R.tap = (e) => R.taps.push(performance.now() - e.timeStamp); h1.addEventListener('pointerdown', R.tap);
  const b = h1.getBoundingClientRect(); return [Math.round(b.left + b.width / 2), Math.round(b.top + b.height / 2)]; })()`;
const READ_HERO = `(() => { const R = window.__cost; R.on = false; (document.querySelector('.hero2 h1') || document.querySelector('h1')).removeEventListener('pointerdown', R.tap);
  const end = R.t0 + 3000, t = [R.t0, ...R.t.filter((x) => x <= end), end]; let gap = 0;
  for (let i = 1; i < t.length; i++) gap = Math.max(gap, t[i] - t[i - 1]);
  const n = window.GlobeMs.n - R.n0;
  return { frames: t.length - 2, gap: Math.round(gap), ms: n > 0 ? +((window.GlobeMs.sum - R.sum0) / n).toFixed(3) : null, taps: R.taps.length, tap: R.taps.length ? Math.round(Math.max(...R.taps)) : null }; })()`;

async function heroWindow(B) {
  const [x, y] = await B.evaluate(WATCH_HERO), b0 = await B.busy(), t0 = Date.now();
  for (let i = 0; i < 12; i++) {
    await B.send("Input.dispatchMouseEvent", { type: "mousePressed", x, y, button: "left", clickCount: 1 });
    await B.send("Input.dispatchMouseEvent", { type: "mouseReleased", x, y, button: "left", clickCount: 1 });
    await sleep(Math.max(0, (i + 1) * 240 - (Date.now() - t0)));
  }
  await sleep(Math.max(0, 3150 - (Date.now() - t0)));
  const r = await B.evaluate(READ_HERO), b1 = await B.busy();
  r.busy = Math.round((b1 - b0) / (Date.now() - t0) * 100);
  return r;
}

// a first visit to the home page, at full speed; true once the hero has drawn, the page has loaded and its fonts
// are in (where pass 13 starts to measure)
async function heroLoad(B, site) {
  await B.cpu(1);
  await start(B, site, true);
  await go(B, site.url, 30000);
  return B.evaluate(`new Promise((ok) => { const t0 = performance.now(), look = () => (window.GlobeMs && window.GlobeMs.n > 0 && document.readyState === 'complete')
    ? document.fonts.ready.then(() => ok(true)) : performance.now() - t0 > 15000 ? ok(false) : setTimeout(look, 50); look(); })`, 30000);
}
// steady flight: three seconds past the sign-off where the hero gives its times, else 12s, the old hero's P2
const STEADY = `(() => { const T = window.GlobeTimes; if (window.GlobeAt) window.GlobeAt(T ? T.gate + 3 : 12); return T || null; })()`;

async function hero(B, sites) {
  const runs = RUNS || 3, settings = {};
  // The machine's speed, as pass 13 prints it: before's hero in steady flight at 1280 x 800, unthrottled. Council 10
  // set the hero's bars when the hero of 2 October 2026 took 0.92ms of script a frame here.
  let host = null;
  await B.screen(1280, 800, 1, false);
  if (await heroLoad(B, sites.before)) {
    await B.evaluate(STEADY); await sleep(600);
    const NOW = "[window.GlobeMs.n, window.GlobeMs.sum]", a = await B.evaluate(NOW); await sleep(1500); const b = await B.evaluate(NOW);
    if (b[0] > a[0]) host = +((b[1] - a[1]) / (b[0] - a[0])).toFixed(3);
  }
  say(`  before's hero unthrottled at 1280 x 800, steady flight: ${host ?? "-"}ms of script a frame`);
  for (const [w, h, dpr, mobile] of [[1280, 800, 1, false], [390, 844, 3, true]]) {
    const id = `${w}x${h}@${dpr}`;
    settings[id] = { what: `${w} x ${h}${dpr > 1 ? ` at ${dpr}x` : ""}, processor 4x`, before: [], after: [] };
    for (let r = 0; r < runs; r++) for (const which of ["before", "after"]) {
      await B.screen(w, h, dpr, mobile);
      if (!(await heroLoad(B, sites[which]))) { say(`  ${id} ${which}: the hero drew nothing`); settings[id][which].push(null); continue; }
      const load = loadavg()[0];
      await B.send("HeapProfiler.collectGarbage"); await B.cpu(4);
      const first = await heroWindow(B);
      const times = await B.evaluate(STEADY);
      await B.cpu(1); await B.send("HeapProfiler.collectGarbage"); await B.cpu(4);
      const steady = await heroWindow(B);
      await B.cpu(1);
      settings[id][which].push({ first, steady, load: +Math.max(load, loadavg()[0]).toFixed(2), times });
      const line = (v) => `${v.ms === null ? "-" : v.ms.toFixed(2)}ms a frame, ${v.frames} frames, gap ${v.gap}ms, tap ${v.tap}ms, main thread ${v.busy}%`;
      say(`  ${id} ${which.padEnd(6)} first seconds: ${line(first)}; steady: ${line(steady)} (load ${load.toFixed(1)})`);
    }
  }
  return { host, settings };
}

// ---------------------------------------------------------------- 4. seventy seconds on the first screen

async function minute(B, sites) {
  const visits = {};
  await B.screen(390, 844, 3, true);
  for (const visit of ["first", "later"]) for (const which of ["before", "after"]) {
    await B.cpu(1);
    // a later visit: the page was opened once already in this tab, by the first visit two runs earlier
    await start(B, sites[which], visit === "first");
    const b0 = await B.busy();
    await B.cpu(4);
    const t0 = Date.now();
    await B.send("Page.navigate", { url: sites[which].url });
    const marks = [], frames = [];
    let rested = null, seen = null;
    for (let s = 1; s <= SECONDS; s++) {
      await sleep(Math.max(0, t0 + s * 1000 - Date.now()));
      const g = await B.evaluate("[window.GlobeMs ? window.GlobeMs.n : 0, window.GlobeState && window.GlobeState.rest === 1, document.documentElement.classList.contains('hero-seen')]").catch(() => [null, false, null]);
      frames.push(g[0]);
      if (seen === null && g[0] !== null) seen = g[2];
      if (g[1] && rested === null) rested = s;
      if (s % 10 === 0 || s === SECONDS) marks.push({ s, busy: Math.round((await B.busy()) - b0), frames: g[0] });
    }
    await B.cpu(1);
    let lastFrame = 0;                     // the second by which the hero drew its last frame
    for (let i = frames.length - 1; i >= 0 && !lastFrame; i--) if (frames[i] > (i ? frames[i - 1] : 0)) lastFrame = i + 1;
    const end = marks[marks.length - 1];
    visits[`${which}-${visit}`] = { which, visit, seconds: SECONDS, busy: end.busy, frames: end.frames, rested, lastFrame, seen, marks, perSecond: frames };
    say(`  ${visit.padEnd(5)} ${which.padEnd(6)} ${SECONDS}s: ${(end.busy / 1000).toFixed(1)}s of main thread, ${end.frames} frames, the last drawn by ${lastFrame}s${rested ? `, at rest by ${rested}s` : ""}` +
      `${seen === (visit === "later") ? "" : `; the page took this for a ${seen ? "later" : "first"} visit`}`);
  }
  return { visits };
}

// ---------------------------------------------------------------- 5. a flick down the home page

// The gaps between frames, as the page keeps up with the flick, split where the hero's canvas leaves the screen:
// the hero draws until then (its cost is timed in the hero section), and the bands alone are on the screen after.
const FLICK = `(() => { const F = window.__flick = { f: [], t: [], gone: 0, shift: 0 }; let last = 0;
  const loop = (t) => { if (last) { F.f.push(+(t - last).toFixed(2)); F.t.push(+t.toFixed(1)); } last = t; F.raf = requestAnimationFrame(loop); };
  F.raf = requestAnimationFrame(loop);
  const cv = document.querySelector('[data-globe]');
  if (cv) new IntersectionObserver((en) => { if (!en[0].isIntersecting && !F.gone) F.gone = performance.now(); }).observe(cv);
  new PerformanceObserver((l) => { for (const e of l.getEntries()) F.shift += e.value; }).observe({ type: 'layout-shift' }); return true; })()`;

async function scroll(B, sites) {
  const runs = RUNS || 5, settings = {};
  for (const [w, h, dpr, mobile] of [[390, 844, 3, true], [1440, 900, 1, false]]) {
    const id = `${w}x${h}@${dpr}`;
    settings[id] = { what: `${w} x ${h}${dpr > 1 ? ` at ${dpr}x` : ""}, processor 4x`, before: [], after: [] };
    for (let r = 0; r < runs; r++) for (const which of ["before", "after"]) {
      await B.cpu(1); await B.screen(w, h, dpr, mobile);
      await start(B, sites[which], true);
      const t0 = Date.now();
      await go(B, sites[which].url, 30000);
      await sleep(Math.max(0, t0 + 3000 - Date.now()));        // as the council did: the reader flicks three seconds in
      await B.evaluate(FLICK);
      await B.cpu(4);
      const H = await B.evaluate("document.documentElement.scrollHeight - innerHeight"), b0 = await B.busy(), s0 = Date.now();
      await B.send("Input.synthesizeScrollGesture", { x: Math.round(w / 2), y: Math.round(h / 2), yDistance: -H, speed: 2400, gestureSourceType: "mouse", repeatCount: 0 }, 180000);
      const busy = (await B.busy()) - b0, secs = (Date.now() - s0) / 1000;
      await B.cpu(1);
      const F = await B.evaluate("(() => { const F = window.__flick; cancelAnimationFrame(F.raf); return { f: F.f, t: F.t, gone: F.gone, shift: F.shift, y: Math.round(scrollY) }; })()");
      const hero = F.gone ? F.t.filter((t) => t <= F.gone).length : 0;     // the frames that began while the hero was on the screen
      const one = { height: H, scrolled: F.y, seconds: +secs.toFixed(2), busy: Math.round(busy / secs / 10), shift: +F.shift.toFixed(4), hero, frames: F.f };
      settings[id][which].push(one);
      const line = (f) => { const s = [...f].sort((a, b) => a - b); return s.length ? `${s.length} frames, median ${med(s).toFixed(1)}ms, worst ${s[s.length - 1].toFixed(1)}ms, over 50ms ${s.filter((x) => x > 50.5).length}` : "no frames"; };
      say(`  ${id} ${which.padEnd(6)} ${F.y} of ${H}px in ${secs.toFixed(1)}s, main thread ${one.busy}%, layout shift ${one.shift}; with the hero on the screen: ${line(F.f.slice(0, hero))}; after it: ${line(F.f.slice(hero))}`);
    }
  }
  return { settings };
}

// ---------------------------------------------------------------- the table

// The bars: council 10's (verdict-home.md, section 4, and the brief for this sheet), as ratios of before where the
// machine's speed matters. The hero's rows are for information: pass 13 holds the hero against the old hero drawn
// on the same page, where this sheet sets page against page.
const BAR = { homeHtml: 21 * 1024, firstVisit: 176 * 1024, lcpLater: 150, firstMinute: 52 / 69.8, laterMinute: 25 / 69.8, slow: 50, shift: 0.05 };
const TICK = 1000 / 60;                     // frames come on the display's ticks
const sec = (ms) => `${(ms / 1000).toFixed(2)} s`;
const ratio = (a, b) => (b ? (a / b).toFixed(2) : "?");
const count = (n) => Math.round(n).toLocaleString("en-GB");
const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;

// part: "all" the flick, or only the frames "after" the hero left the screen
function flickStats(runs, part = "all") {
  const ok = runs.filter(Boolean), f = ok.flatMap((r) => (part === "after" ? r.frames.slice(r.hero) : r.frames)).sort((a, b) => a - b);
  if (!f.length) return null;
  return { n: f.length, flicks: ok.length, median: med(f), worst: f[f.length - 1], over: f.filter((x) => x > BAR.slow + 0.5).length,      // 50.0 to 50.5ms is three ticks
    shift: Math.max(...ok.map((r) => r.shift)), busy: Math.round(mean(ok.map((r) => r.busy))), whole: ok.every((r) => r.scrolled >= r.height - 2) };
}

function table(data) {
  const ran = SECTIONS.filter((s) => data[s]);
  if (!ran.length) return "No section has been run yet.\n";
  const rows = [], detail = [], notes = [];
  const row = (what, before, after, bar, met) => rows.push([what, before, after, bar, met === null ? "" : met ? "met" : "not met"]);
  const builds = (m) => `${m.before.commit || "?"}${m.before.dirty ? " with changes" : ""} and ${m.after.commit || "?"}${m.after.dirty ? " with changes" : ""}`;
  const meta = data[ran[0]].meta;
  if (new Set(ran.map((s) => builds(data[s].meta))).size > 1) notes.push(`Not every section measured the same two builds: ${ran.map((s) => `${s} on ${builds(data[s].meta)}`).join("; ")}.`);

  if (data.bytes) {
    const L = data.bytes.loads, at = (k, which, w) => L.find((l) => l.kind === k && l.which === which && l.w === w && l.path !== null);
    const hb = at("home", "before", 1440), ha = at("home", "after", 1440);
    if (hb && ha) row("The home page's HTML, gzipped", `${kb(hb.html)} KB`, `${kb(ha.html)} KB (${ratio(ha.html, hb.html)} of before)`, "under 21 KB", ha.html < BAR.homeHtml);
    const [b1, b3, a1, a3] = [["before", 1440], ["before", 390], ["after", 1440], ["after", 390]].map(([which, w]) => at("home", which, w));
    if (b1 && b3 && a1 && a3) row("A first visit to the home page, scrolled to the end, at 1440 and at 390: everything it asks for, gzipped (raw)",
      `${kb(b1.gz9)} and ${kb(b3.gz9)} KB (${kb(b1.raw)} KB raw; ${b1.n} and ${b3.n} files)`, `${kb(a1.gz9)} and ${kb(a3.gz9)} KB (${kb(a1.raw)} KB raw; ${a1.n} and ${a3.n} files; ${ratio(a1.gz9, b1.gz9)} of before)`,
      "under 176 KB", Math.max(a1.gz9, a3.gz9) < BAR.firstVisit);
    for (const k of KINDS.slice(1)) {
      const b = at(k.id, "before", 1440), a = at(k.id, "after", 1440);
      const cell = (l) => (l ? `${kb(l.gz9)} KB (${kb(l.raw)} KB raw), ${l.n} files${l.path !== k.paths[0] ? `, /${l.path}` : ""}` : "not built");
      row(`${k.what}: a first visit at 1440, scrolled to the end, gzipped (raw)`, cell(b), `${cell(a)}${a && b ? ` (${ratio(a.gz9, b.gz9)} of before)` : ""}`, "information", null);
    }
    const kinds = (l) => { const g = { Document: 0, Stylesheet: 0, Script: 0, Font: 0, Image: 0, other: 0 };
      for (const f of l.files) g[f.type in g ? f.type : "other"] += f.gz9;
      return `${kb(l.gz9)}: HTML ${kb(g.Document)}, CSS ${kb(g.Stylesheet)}, scripts ${kb(g.Script)}, fonts ${kb(g.Font)}, pictures ${kb(g.Image)}, other ${kb(g.other)}`; };
    for (const k of KINDS) for (const w of [1440, 390]) {
      const b = at(k.id, "before", w), a = at(k.id, "after", w), bw = at(k.id, "before", 1440), aw = at(k.id, "after", 1440);
      // at 390 a page is listed only where it asks for other bytes than at 1440
      if (w === 390 && Math.abs((b?.gz9 || 0) - (bw?.gz9 || 0)) <= 512 && Math.abs((a?.gz9 || 0) - (aw?.gz9 || 0)) <= 512) continue;
      detail.push([`${k.what} at ${w}`, b ? kinds(b) : "not built", a ? kinds(a) : "not built"]);
    }
    const ext = L.filter((l) => l.external?.length), miss = L.filter((l) => l.missing?.length);
    if (ext.length) notes.push(`Asked of other hosts, and not counted: ${ext.map((l) => `${l.which} /${l.path} at ${l.w}: ${l.external.map((e) => e.url).join(", ")}`).join("; ")}.`);
    if (miss.length) notes.push(`Asked for and not in the build: ${miss.map((l) => `${l.which} /${l.path} at ${l.w}: ${l.missing.join(", ")}`).join("; ")}.`);
  }

  if (data.paint) for (const s of PAINTS) {
    const S = data.paint.settings[s.id];
    if (!S || !S.before.length || !S.after.length) continue;
    const m = (runs, k) => med(runs.map((r) => r[k]));
    const span = (runs, k) => { const v = runs.map((r) => r[k]); return `${(Math.min(...v) / 1000).toFixed(2)} to ${(Math.max(...v) / 1000).toFixed(2)}`; };
    const el = (runs) => {
      if (runs.every((r) => r.lcpH1)) return `the h1 in ${runs.length} of ${runs.length}`;
      const c = {}; for (const r of runs) c[r.lcpEl] = (c[r.lcpEl] || 0) + 1;
      return Object.entries(c).map(([e, k]) => `${e} in ${k}`).join(", ");
    };
    const [fb, fa, lb, la, hb, ha] = [[S.before, "fcp"], [S.after, "fcp"], [S.before, "lcp"], [S.after, "lcp"], [S.before, "hero"], [S.after, "hero"]].map(([r, k]) => m(r, k));
    const n = Math.min(S.before.length, S.after.length), d = la - lb, slow = s.id === "slow4g";
    row(`First paint, then the hero's first frame, ${s.what}: medians of ${n}`, `${sec(fb)} (${span(S.before, "fcp")}), then ${sec(hb)}`,
      `${sec(fa)} (${span(S.after, "fcp")}; ${ratio(fa, fb)} of before), then ${sec(ha)}`, "information", null);
    row(`Largest paint and its element, ${s.what}: median of ${n}`, `${sec(lb)} (${span(S.before, "lcp")}), ${el(S.before)}`,
      `${sec(la)} (${span(S.after, "lcp")}; ${d >= 0 ? "+" : ""}${(d / 1000).toFixed(2)} s, ${ratio(la, lb)} of before), ${el(S.after)}`,
      slow ? `the h1, and no later than before's median plus 0.15 s (${sec(lb + BAR.lcpLater)})` : "the h1",
      S.after.every((r) => r.lcpH1) && (!slow || la <= lb + BAR.lcpLater));
  }

  if (data.hero) {
    if (data.hero.host) notes.push(`The machine's speed: before's hero in steady flight at 1280 x 800, unthrottled, took ${data.hero.host.toFixed(2)} ms of script a frame (council 10 set the hero's bars when the hero of 2 October 2026 took 0.92 ms).`);
    for (const S of Object.values(data.hero.settings)) for (const [k, phase] of [["first", "the first seconds"], ["steady", "steady flight"]]) {
      const pick = (which) => S[which].filter(Boolean).map((r) => r[k]), bs = pick("before"), as = pick("after");
      const v = (rs) => ({ ms: mean(rs.map((r) => r.ms)), frames: mean(rs.map((r) => r.frames)), gap: Math.max(...rs.map((r) => r.gap)), tap: Math.max(...rs.map((r) => r.tap ?? 0)) });
      const what = `The hero at ${S.what}, ${phase}: script a frame, frames in 3 s (a second), the worst gap and the worst tap (${plural(Math.min(bs.length, as.length), "load")})`;
      if (!bs.length || !as.length) { row(what, bs.length ? "" : "drew nothing", as.length ? "" : "drew nothing", "information", null); continue; }
      const b = v(bs), a = v(as);
      row(what, `${b.ms.toFixed(2)} ms, ${count(b.frames)} (${(b.frames / 3).toFixed(0)}), ${b.gap} ms, ${b.tap} ms`,
        `${a.ms.toFixed(2)} ms (${ratio(a.ms, b.ms)} of before), ${count(a.frames)} (${(a.frames / 3).toFixed(0)}; ${ratio(a.frames, b.frames)} of before), ${a.gap} ms, ${a.tap} ms`, "information: pass 13 holds the hero", null);
    }
  }

  if (data.minute) for (const [visit, r, words] of [["first", BAR.firstMinute, "a first visit"], ["later", BAR.laterMinute, "a later visit"]]) {
    const b = data.minute.visits[`before-${visit}`], a = data.minute.visits[`after-${visit}`];
    if (!b || !a) continue;
    const last = (x) => (x.lastFrame >= x.seconds - 1 ? "still drawing at the end" : `the last at ${x.lastFrame} s`);
    row(`${b.seconds} seconds on a phone's first screen (390 x 844 at 3x, processor 4x), ${words}: main-thread time, and the hero's frames`,
      `${(b.busy / 1000).toFixed(1)} s; ${count(b.frames)} frames, ${last(b)}`, `${(a.busy / 1000).toFixed(1)} s (${(a.busy / b.busy).toFixed(3)} of before); ${count(a.frames)} frames, ${last(a)}`,
      `at most ${r.toFixed(3)} of before's main-thread time (${(r * b.busy / 1000).toFixed(1)} s)`, a.busy <= r * b.busy);
  }

  // A flick: the verdict's bar is a median of one tick and no frame over 50 ms. Where before misses it on this
  // machine too, after is held to before: a median no longer, and no more frames over 50 ms a flick.
  if (data.scroll) for (const S of Object.values(data.scroll.settings)) for (const part of ["all", "after"]) {
    const b = flickStats(S.before, part), a = flickStats(S.after, part);
    if (!b || !a) continue;
    const cell = (x) => `${x.median.toFixed(1)} ms, ${x.worst.toFixed(1)} ms, ${x.over} of ${count(x.n)}${part === "all" ? `, ${x.shift.toFixed(3)}` : ""}${x.whole ? "" : "; short of the end"}`;
    const good = (x) => Math.round(x.median / TICK) <= 1 && x.over === 0;
    const what = part === "all"
      ? `A flick down the home page at ${S.what}, ${plural(Math.min(b.flicks, a.flicks), "flick")}: the median and the worst gap between frames, frames over 50 ms, the most layout shift`
      : `The same flicks at ${S.what.replace(", processor 4x", "")}, once the hero has left the screen: the median and the worst gap, frames over 50 ms`;
    const shift = part === "all" ? "; layout shift at most 0.05" : "", shiftOk = part === "all" ? a.shift <= BAR.shift : true;
    if (good(b)) row(what, cell(b), cell(a), `a median of 16.7 ms or less and none over 50 ms${shift}`, good(a) && a.whole && shiftOk);
    else row(what, cell(b), cell(a), `before misses 16.7 ms and 50 ms here too, so after is held to before: a median no longer, and no more frames over 50 ms a flick${shift}`,
      a.whole && shiftOk && Math.round(a.median / TICK) <= Math.round(b.median / TICK) && a.over / a.flicks <= b.over / b.flicks);
  }

  for (const s of ran) {
    const m = data[s].meta;
    notes.push(`${s}: ${m.started.slice(0, 16).replace("T", " ")} UTC, ${Math.round(m.seconds)} s, the machine's load ${m.load.join(" to ")}${m.runs ? `, ${plural(m.runs, "load")} of each build a setting` : ""}.`);
  }
  const md = (r) => `| ${r.map((c) => String(c).replace(/\|/g, "/")).join(" | ")} |`;
  const lines = ["# Performance, before and after", "",
    `Before: ${meta.before.commit || meta.before.root}. After: ${meta.after.commit || meta.after.root}${meta.after.dirty ? ", with changes not committed" : ""}. ${meta.chrome}, ${meta.cores} cores.`,
    "", md(["What", "Before", "After", "The bar", "Met"]), md(["---", "---", "---", "---", "---"]), ...rows.map(md)];
  if (detail.length) lines.push("", "What a first visit asks for, scrolled to the end, in KB gzipped at level 9:", "", md(["Page", "Before", "After"]), md(["---", "---", "---"]), ...detail.map(md));
  lines.push("", ...notes.map((n) => `- ${n}`));
  return lines.join("\n") + "\n";
}

function report() {
  const data = {};
  for (const s of SECTIONS) { const f = join(OUT, `${s}.json`); if (existsSync(f)) data[s] = JSON.parse(readFileSync(f, "utf8")); }
  const text = table(data);
  writeFileSync(join(OUT, "perf.md"), text);
  writeFileSync(join(OUT, "perf.json"), JSON.stringify({ written: new Date().toISOString(), sections: data }, null, 1));
  say("\n" + text + `\nwritten: ${join(OUT, "perf.md")} and ${join(OUT, "perf.json")}`);
}

// ---------------------------------------------------------------- run

const finish = () => { for (const f of cleanup.splice(0)) { try { f(); } catch {} } };
process.on("exit", finish);
for (const sig of ["SIGINT", "SIGTERM", "SIGHUP"]) process.on(sig, () => { finish(); process.exit(130); });

mkdirSync(OUT, { recursive: true });
if (!TABLE) {
  const builds = { before: build(opt("before")), after: build(opt("after")) };
  const sites = { before: await serve(builds.before.root), after: await serve(builds.after.root) };
  const B = await browser();
  const RUN = { bytes, paint, hero, minute, scroll }, DEFAULT_RUNS = { paint: 5, hero: 3, scroll: 5 };
  say(`before ${builds.before.commit || ""} ${builds.before.root}\nafter  ${builds.after.commit || ""} ${builds.after.root}\n${B.version}, ${cpus().length} cores`);
  let failed = false;
  for (const s of SECTIONS.filter((s) => ONLY.includes(s))) {
    const t0 = Date.now(), load0 = loadavg()[0];
    say(`\n${s}`);
    try {
      const result = await RUN[s](B, sites);
      const seconds = (Date.now() - t0) / 1000;
      result.meta = { section: s, started: new Date(t0).toISOString(), seconds: +seconds.toFixed(1), load: [+load0.toFixed(2), +loadavg()[0].toFixed(2)],
        runs: s in DEFAULT_RUNS ? RUNS || DEFAULT_RUNS[s] : s === "minute" ? 1 : null, chrome: B.version, node: process.version, cores: cpus().length, ...builds };
      writeFileSync(join(OUT, `${s}.json`), JSON.stringify(result, null, 1));
      say(`  ${s} took ${seconds.toFixed(0)}s${seconds > 600 ? ": over the ten minutes a section may hold the machine" : ""}`);
    } catch (e) { failed = true; say(`  ${s} failed: ${e.stack || e}`); await B.cpu(1).catch(() => {}); await B.net(null).catch(() => {}); }
  }
  await B.close();
  finish();
  report();
  process.exit(failed ? 1 : 0);
} else report();
