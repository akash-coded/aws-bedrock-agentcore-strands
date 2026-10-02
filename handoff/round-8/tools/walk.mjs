// Walk a page the way a reader does: motion ON, scroll one screen at a time, one screenshot per screen.
// usage: node walk.mjs <outDir> <width> <height> <light|dark> name=url [name=url ...]
//   env MAX=14 (screens per page), PAUSE=900 (ms to settle after each scroll), FIRST=2600 (ms after load),
//       TIMES="0,1500,4000" (extra shots of the first screen at these ms after load, for things that move),
//       STEPS='[{"click":"sel"},{"wait":500}]' (run after load, before the walk)
// writes <name>-<theme>-<w>-01.jpg ... and prints console errors and the page's scroll width.
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const [outDir, W, H, theme, ...pairs] = process.argv.slice(2);
const width = +W, height = +H;
const MAX = +(process.env.MAX || 14), PAUSE = +(process.env.PAUSE || 900), FIRST = +(process.env.FIRST || 2600);
const TIMES = (process.env.TIMES || "").split(",").filter(Boolean).map(Number);
const STEPS = JSON.parse(process.env.STEPS || "[]");
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `walk-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsurl;
for (let i = 0; i < 60; i++) { try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); wsurl = l.find((t) => t.type === "page").webSocketDebuggerUrl; break; } catch {} await sleep(250); }
const ws = new WebSocket(wsurl); await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const waiting = new Map(); let errors = [];
ws.addEventListener("message", (ev) => { const m = JSON.parse(ev.data);
  if (m.method === "Runtime.exceptionThrown") errors.push((m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 300));
  if (m.method === "Log.entryAdded" && m.params.entry.level === "error") errors.push(m.params.entry.text.slice(0, 200) + " " + (m.params.entry.url || ""));
  if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m.result || m.error); waiting.delete(m.id); } });
const send = (method, params = {}) => new Promise((ok) => { const id = ++seq; waiting.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
const ev = async (e) => { const r = await send("Runtime.evaluate", { expression: e, awaitPromise: true, returnByValue: true }); return r.result ? r.result.value : undefined; };
const shot = async (file) => { const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 78 }); writeFileSync(join(outDir, file), Buffer.from(data, "base64")); };
mkdirSync(outDir, { recursive: true });
try {
  await send("Page.enable"); await send("Runtime.enable"); await send("Log.enable");
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: width < 600 ? 2 : 1, mobile: width < 600 });
  await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: theme }, { name: "prefers-reduced-motion", value: "no-preference" }] });
  await send("Page.addScriptToEvaluateOnNewDocument", { source: `try{localStorage.setItem("manual-theme", ${JSON.stringify(theme)})}catch(e){}` });
  for (const p of pairs) {
    const i = p.indexOf("="); const name = p.slice(0, i), url = p.slice(i + 1);
    errors = [];
    const tag = `${name}-${theme}-${width}`;
    await send("Page.navigate", { url });
    let t0 = Date.now();
    for (const [k, t] of TIMES.entries()) { await sleep(Math.max(0, t - (Date.now() - t0))); await shot(`${tag}-t${k}.jpg`); }
    await sleep(Math.max(0, FIRST - (Date.now() - t0)));
    for (const s of STEPS) {
      if (s.wait) await sleep(s.wait);
      if (s.click) { const ok = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(s.click)});if(!e)return false;e.click();return true})()`); if (!ok) console.log("  no element for", s.click); await sleep(300); }
      if (s.eval) console.log("  eval:", JSON.stringify(await ev(s.eval)));
    }
    const m = await ev(`({h: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight), sw: document.documentElement.scrollWidth, iw: innerWidth})`);
    let n = 0;
    for (let y = 0; y < m.h && n < MAX; y += Math.round(height * 0.86)) {
      await ev(`scrollTo({top:${y},behavior:"instant"});1`); await sleep(PAUSE);
      n++; await shot(`${tag}-${String(n).padStart(2, "0")}.jpg`);
    }
    console.log(`${tag}: ${n} screens of a ${m.h}px page` + (m.sw > m.iw ? `; SCROLLS SIDEWAYS by ${m.sw - m.iw}px` : "") + (errors.length ? `; ERRORS: ${errors.join(" | ")}` : ""));
  }
} finally { ws.close(); chrome.kill(); await sleep(400); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
