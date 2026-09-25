// Capture the simulator's pictures for the picture pack (site/pages/pictures.py).
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/simshots.mjs http://localhost:8799/simulator/ site/assets/pictures
//
// Each entry is a route in the tool and a selector; the element is captured at 2x as WebP, clipped to its
// own box. The list mirrors SIM in site/pages/pictures.py, which reads the files' sizes from their headers.
// Chrome's DevTools protocol over Node's built-in WebSocket, so there is nothing to install.

import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [base, outDir] = process.argv.slice(2);
if (!base || !outDir) { console.error("usage: node simshots.mjs <simulator url> <output dir>"); process.exit(2); }

const SHOTS = [
  { name: "sim-flight-plan", route: "#/quest", sel: ".xrt" },
  { name: "sim-line-vs-loop", route: "#/start", sel: "#illo-pdlc" },
  { name: "sim-spine", route: "#/start", sel: "#illo-spine" },
  { name: "sim-methods", route: "#/start", sel: "#illo-methods" },
  { name: "sim-roles", route: "#/start", sel: "#illo-roles" },
  { name: "sim-three-efforts", route: "#/effort", sel: "#ef-tiers .xef-tiers" },
  { name: "sim-same-task", route: "#/effort", sel: "#ef-same .xtw" },
  { name: "sim-concept-map", route: "#/concepts", sel: ".xzm-w" },
  { name: "sim-loop-map", route: "#/loopmap", sel: "#lm-big" },
  { name: "sim-gates", route: "#/governance", sel: "#gv-gates .xfig" },
];

const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `simshots-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
setTimeout(() => { console.error("timed out"); process.exit(3); }, 240000);

let wsu;
for (let i = 0; i < 60 && !wsu; i++) {
  try { wsu = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find((t) => t.type === "page")?.webSocketDebuggerUrl; } catch { /* not up yet */ }
  await sleep(250);
}
const ws = new WebSocket(wsu);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let id = 0; const wait = new Map();
ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && wait.has(m.id)) { wait.get(m.id)(m.result || m.error); wait.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; wait.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => (await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.value;

mkdirSync(outDir, { recursive: true });
await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 2, mobile: false });
await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: "light" }, { name: "prefers-reduced-motion", value: "reduce" }] });
await send("Page.navigate", { url: base + "#/start" }); await sleep(3500);
await ev(`localStorage.setItem("skyways.tours.off","1"); localStorage.setItem("skyways.heromode","light"); true`);

let done = 0;
for (const s of SHOTS) {
  await ev(`location.hash=${JSON.stringify(s.route)}; true`); await sleep(1800);
  const box = await ev(`(() => { const el = document.querySelector(".page.on " + ${JSON.stringify(s.sel)}) || document.querySelector(${JSON.stringify(s.sel)}); if (!el || !el.getBoundingClientRect().width) return null;
    el.scrollIntoView({ block: "start", behavior: "instant" }); window.scrollBy(0, -80);
    const b = el.getBoundingClientRect(); return { x: b.x + scrollX, y: b.y + scrollY, w: b.width, h: b.height, ph: document.documentElement.scrollHeight }; })()`);
  if (!box) { console.error("missing", s.name, s.sel); continue; }
  await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: Math.min(box.ph, 16000), deviceScaleFactor: 2, mobile: false });
  await sleep(400);
  const pad = 10;
  const { data } = await send("Page.captureScreenshot", { format: "webp", quality: 90, captureBeyondViewport: true,
    clip: { x: Math.max(0, box.x - pad), y: Math.max(0, box.y - pad), width: Math.min(1440, box.w + 2 * pad), height: box.h + 2 * pad, scale: 1 } });
  writeFileSync(join(outDir, `${s.name}.webp`), Buffer.from(data, "base64"));
  await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 2, mobile: false });
  done += 1; console.log(`  ${s.name}  ${Math.round(box.w)}×${Math.round(box.h)}`);
}
console.log(`${done} of ${SHOTS.length} simulator pictures written to ${outDir}`);
ws.close(); chrome.kill(); try { rmSync(profile, { recursive: true, force: true }); } catch { /* ignore */ }
process.exit(done === SHOTS.length ? 0 : 1);
