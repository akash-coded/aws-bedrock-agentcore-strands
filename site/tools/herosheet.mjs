// The hero's picture at twelve moments of its flight, the rest among them, at five widths, in both themes, on
// sheets a person can look at before a release. The acceptance gate measures the hero; this is for the eye.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/herosheet.mjs http://localhost:8799/ /tmp/hero
//
// Each sheet is a first visit in the sitting, so the entrance and the camera's pull-back are on it. Every moment is
// read from the hero's own times (window.GlobeTimes, theme/hero.js), never typed in: the launch, the tag's arrival,
// the pull-back, each change of form, the sign-off before and after, behind the Earth, round two one turn higher
// (a lap on), and the rest. It puts the hero's clock at each with window.GlobeAt(seconds), photographs the picture,
// and writes <out>/hero-<theme>-<width>.jpg, the twelve left to right, top to bottom, each captioned with its moment,
// its second and the words the tag carries. Headless Chrome over the DevTools protocol, the same as accept.mjs.
import { createServer } from "node:net";
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [BASE, OUT] = process.argv.slice(2);
if (!BASE || !OUT) { console.error("usage: node herosheet.mjs <site url, ending in /> <output dir>"); process.exit(2); }
const MOMENTS = (T) => [["the launch", Math.max(0.05, T.pre - 0.65)], ["P0, the tag in", T.pre + 0.3], ["the camera pulls back", T.pre + 2.5],
  ["into P1", T.p1 + 0.3], ["the drawing", T.p1 + 2.5], ["on the bar", T.gate - 0.05], ["signed", T.gate + 0.35], ["built, P2", T.gate + 1.6],
  ["into P3", T.p3 + 0.3], ["behind the Earth", T.back + 2], ["round two", T.lap + 1], ["the rest", T.rest + 3]];
const SIZES = [[1440, 900], [1024, 768], [768, 1024], [390, 844], [320, 640]];
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
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");

mkdirSync(OUT, { recursive: true });
let code = 0;
try {
  await send("Page.enable"); await send("Runtime.enable");
  // every load is a first visit in the sitting: the head's script finds nothing in sessionStorage, so the entrance plays
  await send("Page.addScriptToEvaluateOnNewDocument", { source: "try { sessionStorage.removeItem('hero') } catch (e) {}" });
  for (const theme of ["dark", "light"]) {
    await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: theme }, { name: "prefers-reduced-motion", value: "no-preference" }] });
    for (const [w, h] of SIZES) {
      await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 2, mobile: w < 600 });
      await evaluate("window.__left = true");
      await send("Page.navigate", { url: BASE });
      for (let i = 0; i < 80 && !(await evaluate("!window.__left && !!window.GlobeTimes")); i++) await sleep(100);
      await sleep(600);
      const T = await evaluate(`(() => { document.documentElement.setAttribute("data-theme", ${JSON.stringify(theme)}); const b = document.querySelector('.hero2 [data-motion-toggle]');
        if (b) { b.checked = true; b.dispatchEvent(new Event('change', { bubbles: true })); } return window.GlobeTimes || null; })()`);
      if (!T || !T.launch) { console.error(T ? "the hero did not play its entrance on a first visit" : "the hero publishes no times (window.GlobeTimes): this sheet needs the hero of council 10"); code = 1; break; }
      await evaluate("document.fonts.ready.then(() => true)");
      await sleep(300);
      const cells = [], said = [];
      for (const [name, sec] of MOMENTS(T)) {
        const m = await evaluate(`(() => { window.GlobeAt(${sec.toFixed(3)}); const r = document.querySelector('.hero2 .scene').getBoundingClientRect(), s = window.GlobeState || {};
          return { x: Math.max(0, r.left), y: r.top + scrollY, w: Math.min(innerWidth, r.right) - Math.max(0, r.left), h: r.height, tag: s.tag || "", rest: s.rest }; })()`);
        await sleep(80);
        const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 86, captureBeyondViewport: true,
          clip: { x: m.x, y: m.y, width: m.w, height: m.h, scale: 1 } });
        const words = m.rest === 1 ? "at rest" : m.tag || "no tag";
        cells.push(`<figure><img src="data:image/jpeg;base64,${data}"><figcaption><b>${esc(name)}</b> ${sec.toFixed(2)}s · ${esc(words)}</figcaption></figure>`);
        said.push(`${sec.toFixed(2)}s ${words}`);
      }
      // lay the twelve on one sheet and photograph the sheet
      const html = `<body style="margin:0;background:${theme === "dark" ? "#121316" : "#F7F6F2"};padding:6px;font:12px ui-monospace,monospace;color:#888">
        <style>main{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}figure{margin:0}img{width:100%;display:block}figcaption{padding:2px 4px}b{color:${theme === "dark" ? "#ECEAE4" : "#1A1A1A"};font-weight:600}</style>
        <p style="margin:2px 4px 8px">${w} x ${h}, ${theme}: a first visit; a round of ${T.lap}s, P1 at ${T.p1}s, the sign-off at ${T.gate}s, P3 at ${T.p3}s, behind the Earth at ${T.back}s, at rest from ${T.rest}s</p>
        <main>${cells.join("")}</main></body>`;
      await send("Emulation.setDeviceMetricsOverride", { width: 1600, height: 1000, deviceScaleFactor: 1, mobile: false });
      await send("Page.navigate", { url: "about:blank" });
      await evaluate(`document.open(); document.write(${JSON.stringify(html)}); document.close(); true`);
      await sleep(700);
      const hh = await evaluate("document.documentElement.scrollHeight");
      const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 84, captureBeyondViewport: true, clip: { x: 0, y: 0, width: 1600, height: hh, scale: 1 } });
      const file = join(OUT, `hero-${theme}-${w}.jpg`);
      writeFileSync(file, Buffer.from(data, "base64"));
      console.log(`${file}  ${said.join(" | ")}`);
    }
    if (code) break;
  }
} finally {
  ws.close();
  const exited = new Promise((r) => chrome.once("exit", r));
  chrome.kill();
  await Promise.race([exited, sleep(5000)]);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
process.exit(code);
