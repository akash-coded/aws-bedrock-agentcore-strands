// drive a page: node drive.mjs <url> <outDir> <width> <height> <steps.json>   (env MOTION=1 to allow motion)
// steps: [{"shot":"name"}, {"click":"css selector"}, {"text":"button text"}, {"eval":"js"}, {"wait":300}, {"full":"name"}]
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const [url, out, W = "1440", H = "900", stepsFile] = process.argv.slice(2);
const steps = JSON.parse(readFileSync(stepsFile, "utf8"));
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `drive-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--no-first-run", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsurl; for (let i = 0; i < 60; i++) { try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); wsurl = l.find((t) => t.type === "page").webSocketDebuggerUrl; break; } catch {} await sleep(250); }
const ws = new WebSocket(wsurl); await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const waiting = new Map(); const errors = [];
ws.addEventListener("message", (ev) => { const m = JSON.parse(ev.data);
  if (m.method === "Runtime.exceptionThrown") errors.push((m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 300));
  if (m.method === "Log.entryAdded" && m.params.entry.level === "error") errors.push(m.params.entry.text.slice(0, 200));
  if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m.result || m.error); waiting.delete(m.id); } });
const send = (method, params = {}) => new Promise((ok) => { const id = ++seq; waiting.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
const ev = async (e) => { const r = await send("Runtime.evaluate", { expression: e, awaitPromise: true, returnByValue: true }); return r.result ? r.result.value : undefined; };
mkdirSync(out, { recursive: true });
try {
  await send("Page.enable"); await send("Runtime.enable"); await send("Log.enable");
  await send("Emulation.setDeviceMetricsOverride", { width: +W, height: +H, deviceScaleFactor: 1, mobile: +W < 600 });
  await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: process.env.MOTION ? "no-preference" : "reduce" }] });
  await send("Page.navigate", { url }); await sleep(1800);
  for (const s of steps) {
    if (s.wait) await sleep(s.wait);
    if (s.click) { const ok = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(s.click)});if(!e)return false;e.click();return true})()`); if (!ok) console.log("  no element for", s.click); await sleep(250); }
    if (s.text) { const ok = await ev(`(()=>{const e=[...document.querySelectorAll('button,a,label')].find(b=>b.textContent.trim().startsWith(${JSON.stringify(s.text)}));if(!e)return false;e.click();return true})()`); if (!ok) console.log("  no button", s.text); await sleep(250); }
    if (s.eval) console.log("  eval:", JSON.stringify(await ev(s.eval)));
    if (s.webp) { const { data } = await send("Page.captureScreenshot", { format: "webp", quality: 82 }); writeFileSync(s.webp, Buffer.from(data, "base64")); }
    if (s.clip) { const [x, y, width, height, scale = 2] = s.clip; const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 82, clip: { x, y, width, height, scale } }); writeFileSync(join(out, s.name + ".jpg"), Buffer.from(data, "base64")); }
    if (s.shot) { const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 74 }); writeFileSync(join(out, s.shot + ".jpg"), Buffer.from(data, "base64")); }
    if (s.full) { const h = await ev("Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)"); const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 72, captureBeyondViewport: true, clip: { x: 0, y: 0, width: +W, height: Math.min(h, s.max || 2600), scale: 1 } }); writeFileSync(join(out, s.full + ".jpg"), Buffer.from(data, "base64")); }
  }
  console.log(errors.length ? "ERRORS:\n" + errors.join("\n") : "no script errors");
} finally { ws.close(); chrome.kill(); await sleep(400); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
