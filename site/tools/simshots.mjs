// Screenshot the simulator's main screens for the tutorial's simulator lesson.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/simshots.mjs http://localhost:8799/simulator/ site/assets/learn
//
// The simulator has one colour scheme, so each screen is captured once, in light, at 2x, as WebP,
// clipped to the top of the page the way a reader first sees it. A step may click something first
// (a simulation option, say) so that the screenshot shows the simulator doing its job.

import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

// Each screen is the top of a page ({ top: height }), or one element clipped with a margin
// ({ sel, from, pad }), after an optional script — clicking the recommended option of a simulation,
// say, so that the screenshot shows the simulator doing its job.
const BEST = (id) => `(() => {
  const k = SIMS[${JSON.stringify(id)}].steps[0].opts.findIndex((o) => o.best);
  const b = document.querySelectorAll('[data-sim="${id}"] .xopt')[k];
  if (b) b.click();
  return !!b;
})()`;
const SCREENS = [
  ["sim-story", "#/story", { top: 760 }],
  ["sim-simulation", "#/simulations/incident", { from: "#simsec-incident", sel: '[data-sim="incident"]', pad: 20, script: BEST("incident") }],
  ["sim-toolkit", "#/toolkit/confidence", { sel: "#tool-confidence", pad: 20 }],
  ["sim-loopmap", "#/loopmap", { sel: "#lm-big", pad: 10 }],
  ["sim-evidence", "#/evidence", { sel: "#evidenceMain .xevid .xsec:nth-of-type(2)", pad: 14 }],
];

const [url, outDir] = process.argv.slice(2);
if (!url || !outDir) {
  console.error("usage: node simshots.mjs <simulator url> <output dir>");
  process.exit(2);
}
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `simshots-${PORT}`);
const chrome = spawn(CHROME, [
  "--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank",
], { stdio: "ignore" });

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
ws.addEventListener("message", (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && waiting.has(msg.id)) {
    const { ok, no } = waiting.get(msg.id);
    waiting.delete(msg.id);
    msg.error ? no(new Error(msg.error.message)) : ok(msg.result);
  }
});
const send = (method, params = {}) => new Promise((ok, no) => {
  const id = ++seq;
  waiting.set(id, { ok, no });
  ws.send(JSON.stringify({ id, method, params }));
});
const evaluate = async (expression) =>
  (await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true })).result.value;

mkdirSync(outDir, { recursive: true });
await send("Page.enable");
await send("Runtime.enable");
const WIDTH = 1200;
try {
  await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
  for (const [name, route, how] of SCREENS) {
    await send("Emulation.setDeviceMetricsOverride", { width: WIDTH, height: how.top || 900, deviceScaleFactor: 2, mobile: false });
    // a fresh load per screen: the simulator is one page, and a hash change keeps the last one's state
    await send("Page.navigate", { url: "about:blank" });
    await sleep(300);
    await send("Page.navigate", { url: url + route });
    await sleep(2500);
    await evaluate(`document.fonts.ready.then(() => true)`);
    if (how.script && !(await evaluate(how.script))) throw new Error(`${name}: the script found nothing to act on`);
    await sleep(how.script ? 1200 : 200);
    // the site frame's contact pill floats over whatever is underneath it; it is not part of the tool
    await evaluate(`document.querySelectorAll(".sw-pill").forEach((e) => { e.style.display = "none"; }); true`);
    let clip;
    if (how.top) {
      await evaluate(`window.scrollTo(0, 0); true`);
      await sleep(400);
      clip = { x: 0, y: 0, width: WIDTH, height: how.top };
    } else {
      // the sticky header would otherwise sit across the top of a clipped element
      await evaluate(`(() => {
        let h = document.getElementById("topnav");
        while (h && !["fixed", "sticky"].includes(getComputedStyle(h).position)) h = h.parentElement;
        (h || document.getElementById("topnav")).style.visibility = "hidden";
        return true;
      })()`);
      clip = await evaluate(`(() => {
        const el = document.querySelector(${JSON.stringify(how.sel)});
        const from = ${JSON.stringify(how.from || "")} ? document.querySelector(${JSON.stringify(how.from || "")}) : el;
        if (!el || !from) return null;
        const a = from.getBoundingClientRect(), b = el.getBoundingClientRect(), p = ${how.pad || 0};
        const left = Math.max(0, Math.min(a.left, b.left) - p), top = Math.min(a.top, b.top) - p + scrollY;
        const right = Math.min(innerWidth, Math.max(a.right, b.right) + p), bottom = Math.max(a.bottom, b.bottom) + p + scrollY;
        return { x: left, y: top, width: right - left, height: bottom - top };
      })()`);
      if (!clip) throw new Error(`${name}: ${how.sel} not found`);
    }
    const { data } = await send("Page.captureScreenshot", {
      format: "webp", quality: 82, captureBeyondViewport: !how.top, clip: { ...clip, scale: 1 },
    });
    const file = join(outDir, `${name}.webp`);
    writeFileSync(file, Buffer.from(data, "base64"));
    console.log(`${name.padEnd(16)} ${route.padEnd(26)} ${Math.round(clip.width)}×${Math.round(clip.height)}  ${file}`);
  }
} finally {
  ws.close();
  const exited = new Promise((r) => chrome.once("exit", r));
  chrome.kill();
  await Promise.race([exited, sleep(5000)]);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
