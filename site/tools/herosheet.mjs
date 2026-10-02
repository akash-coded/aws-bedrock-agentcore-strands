// The hero's picture at twelve moments of one lap, at four widths, in both themes, on sheets a person can
// look at before a release. The acceptance gate measures the hero; this is for the eye.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/herosheet.mjs http://localhost:8799/ /tmp/hero
//
// It puts the hero's clock at each moment with window.GlobeAt(seconds) (theme/hero.js), photographs the
// picture and the line under it, and writes <out>/hero-<theme>-<width>.jpg: twelve frames, left to right,
// top to bottom. Headless Chrome over the DevTools protocol, the same as accept.mjs: nothing to install.
import { createServer } from "node:net";
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [BASE, OUT] = process.argv.slice(2);
if (!BASE || !OUT) { console.error("usage: node herosheet.mjs <site url, ending in /> <output dir>"); process.exit(2); }
const LAP = 27, MOMENTS = 12;
const SIZES = [[1440, 900], [1024, 768], [768, 1024], [390, 844]];
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = await new Promise((ok) => { const s = createServer().listen(0, "127.0.0.1", () => { const p = s.address().port; s.close(() => ok(p)); }); });   // a port no other Chrome holds, so a run never drives another run's browser
const profile = join(tmpdir(), `herosheet-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsurl;
for (let i = 0; i < 60 && !wsurl; i++) {
  try { wsurl = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find((t) => t.type === "page").webSocketDebuggerUrl; } catch { await sleep(250); }
}
const ws = new WebSocket(wsurl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0;
const waiting = new Map();
ws.addEventListener("message", (ev) => { const m = JSON.parse(ev.data); if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m.result || m.error); waiting.delete(m.id); } });
const send = (method, params = {}) => new Promise((ok) => { const id = ++seq; waiting.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
const evaluate = async (e) => (await send("Runtime.evaluate", { expression: e, awaitPromise: true, returnByValue: true })).result?.value;

mkdirSync(OUT, { recursive: true });
try {
  await send("Page.enable"); await send("Runtime.enable");
  for (const theme of ["dark", "light"]) {
    await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: theme }, { name: "prefers-reduced-motion", value: "no-preference" }] });
    for (const [w, h] of SIZES) {
      await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 2, mobile: w < 600 });
      await send("Page.navigate", { url: BASE });
      await sleep(1500);
      await evaluate(`document.documentElement.setAttribute("data-theme", ${JSON.stringify(theme)}); const b = document.querySelector('.hero2 [data-motion-toggle]'); b.checked = true; b.dispatchEvent(new Event('change', { bubbles: true })); true`);
      await sleep(300);
      const cells = [];
      for (let k = 0; k < MOMENTS; k++) {
        const sec = (k * LAP / MOMENTS + 0.4).toFixed(2);
        const box = await evaluate(`(() => { window.GlobeAt(${sec}); const r = document.querySelector('.scene').getBoundingClientRect();
          return { x: Math.max(0, r.left), y: r.top + scrollY, w: Math.min(innerWidth, r.right) - Math.max(0, r.left), h: r.height }; })()`);
        await sleep(320);                                     // the line under the picture has changed colour by now
        const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 86, captureBeyondViewport: true,
          clip: { x: box.x, y: box.y, width: box.w, height: box.h, scale: 1 } });
        cells.push(`<figure><img src="data:image/jpeg;base64,${data}"><figcaption>${sec}s</figcaption></figure>`);
      }
      // lay the twelve on one sheet and photograph the sheet
      const html = `<body style="margin:0;background:${theme === "dark" ? "#121316" : "#F7F6F2"};display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:6px;font:12px ui-monospace,monospace;color:#888">
        <style>figure{margin:0}img{width:100%;display:block}figcaption{padding:2px 4px}</style>${cells.join("")}</body>`;
      await send("Emulation.setDeviceMetricsOverride", { width: 1600, height: 1000, deviceScaleFactor: 1, mobile: false });
      await send("Page.navigate", { url: "about:blank" });
      await evaluate(`document.open(); document.write(${JSON.stringify(html)}); document.close(); true`);
      await sleep(700);
      const hh = await evaluate("document.documentElement.scrollHeight");
      const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 84, captureBeyondViewport: true, clip: { x: 0, y: 0, width: 1600, height: hh, scale: 1 } });
      const file = join(OUT, `hero-${theme}-${w}.jpg`);
      writeFileSync(file, Buffer.from(data, "base64"));
      console.log(file);
    }
  }
} finally {
  ws.close();
  const exited = new Promise((r) => chrome.once("exit", r));
  chrome.kill();
  await Promise.race([exited, sleep(5000)]);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
