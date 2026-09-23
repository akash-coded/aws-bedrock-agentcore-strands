// Screenshot every embeddable board and figure, light and dark, for the wiki copies of the lessons.
//
//   python3 site/build.py --shots
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/shoot.mjs http://localhost:8799/learn/_shots/ site/assets/learn
//
// The site embeds the live boards; the wiki cannot run them, so it shows these instead, inside a
// <picture> that follows the reader's colour mode. Uses Chrome's DevTools protocol over the
// WebSocket built into Node 22+, so there is nothing to install. Each capture is clipped to the
// visual's own box, at 2x, as WebP.

import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [url, outDir] = process.argv.slice(2);
if (!url || !outDir) {
  console.error("usage: node shoot.mjs <shots page url> <output dir>");
  process.exit(2);
}
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `shoot-${PORT}`);
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
let total = 0;
try {
  for (const theme of ["light", "dark"]) {
    await send("Emulation.setDeviceMetricsOverride", { width: 1120, height: 900, deviceScaleFactor: 2, mobile: false });
    // reduced motion: the boards render their final state immediately instead of revealing
    await send("Emulation.setEmulatedMedia", { features: [
      { name: "prefers-color-scheme", value: theme },
      { name: "prefers-reduced-motion", value: "reduce" },
    ] });
    await send("Page.navigate", { url });
    await sleep(2500);
    await evaluate(`document.documentElement.setAttribute("data-theme", ${JSON.stringify(theme)}); true`);
    await evaluate(`document.fonts.ready.then(() => true)`);
    await sleep(600);
    const shots = await evaluate(`[...document.querySelectorAll(".shot")].map(el => {
      const r = el.getBoundingClientRect();
      return { name: el.dataset.shot, x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height };
    })`);
    for (const s of shots) {
      const { data } = await send("Page.captureScreenshot", {
        format: "webp", quality: 90, captureBeyondViewport: true,
        clip: { x: s.x, y: s.y, width: s.w, height: s.h, scale: 1 },
      });
      const file = join(outDir, `${s.name}.${theme}.webp`);
      writeFileSync(file, Buffer.from(data, "base64"));
      total++;
      console.log(`${theme.padEnd(5)} ${s.name.padEnd(28)} ${Math.round(s.w)}×${Math.round(s.h)}  ${file}`);
    }
  }
} finally {
  ws.close();
  // Chrome keeps writing to its profile until it has exited; remove it after, and never fail on it.
  const exited = new Promise((r) => chrome.once("exit", r));
  chrome.kill();
  await Promise.race([exited, sleep(5000)]);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
console.log(`${total} screenshots`);
