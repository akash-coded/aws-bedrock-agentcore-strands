// Screenshot every social card on the og sheet as a 1200×630 JPEG.
//
//   python3 site/build.py --shots
//   node site/tools/ogshots.mjs http://localhost:8765/og/_sheet.html site/assets/og
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const [url, outDir] = process.argv.slice(2);
if (!url || !outDir) { console.error("usage: node ogshots.mjs <sheet url> <output dir>"); process.exit(2); }
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `og-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function target() {
  for (let i = 0; i < 60; i++) {
    try { const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find((t) => t.type === "page"); if (page) return page.webSocketDebuggerUrl; } catch {}
    await sleep(250);
  }
  throw new Error("Chrome did not start");
}
const ws = new WebSocket(await target());
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const waiting = new Map();
ws.addEventListener("message", (ev) => { const m = JSON.parse(ev.data); if (m.id && waiting.has(m.id)) { const { ok, no } = waiting.get(m.id); waiting.delete(m.id); m.error ? no(new Error(m.error.message)) : ok(m.result); } });
const send = (method, params = {}) => new Promise((ok, no) => { const id = ++seq; waiting.set(id, { ok, no }); ws.send(JSON.stringify({ id, method, params })); });
const evaluate = async (expression) => (await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true })).result.value;
mkdirSync(outDir, { recursive: true });
await send("Page.enable"); await send("Runtime.enable");
await send("Emulation.setDeviceMetricsOverride", { width: 1240, height: 900, deviceScaleFactor: 1, mobile: false });
await send("Page.navigate", { url }); await sleep(2500);
await evaluate(`document.fonts.ready.then(() => true)`); await sleep(400);
const cards = await evaluate(`[...document.querySelectorAll(".ogcard")].map(el => { const r = el.getBoundingClientRect(); return { name: el.dataset.og, x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; })`);
let n = 0;
try {
  for (const c of cards) {
    const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 84, captureBeyondViewport: true, clip: { x: c.x, y: c.y, width: c.w, height: c.h, scale: 1 } });
    writeFileSync(join(outDir, `${c.name}.jpg`), Buffer.from(data, "base64")); n++;
  }
} finally {
  ws.close(); const exited = new Promise((r) => chrome.once("exit", r)); chrome.kill(); await Promise.race([exited, sleep(5000)]);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
console.log(`${n} cards`);
