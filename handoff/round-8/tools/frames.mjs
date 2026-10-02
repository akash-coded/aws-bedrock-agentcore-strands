// frames of the section-two entrance, and the hover state
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const [BASE, out, W = "1440", H = "900"] = process.argv.slice(2);
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `fr-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--no-first-run", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsurl; for (let i = 0; i < 60; i++) { try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); wsurl = l.find((t) => t.type === "page").webSocketDebuggerUrl; break; } catch {} await sleep(250); }
const ws = new WebSocket(wsurl); await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const waiting = new Map();
ws.addEventListener("message", (ev) => { const m = JSON.parse(ev.data); if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m.result); waiting.delete(m.id); } });
const send = (method, params = {}) => new Promise((ok) => { const id = ++seq; waiting.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
const ev = async (e) => (await send("Runtime.evaluate", { expression: e, awaitPromise: true, returnByValue: true })).result.value;
mkdirSync(out, { recursive: true });
const shot = async (name) => { const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 70 }); writeFileSync(join(out, name + ".jpg"), Buffer.from(data, "base64")); };
try {
  await send("Page.enable"); await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", { width: +W, height: +H, deviceScaleFactor: 1, mobile: +W < 600 });
  await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "no-preference" }] });
  await send("Page.navigate", { url: BASE }); await sleep(3500);
  console.log("armed:", await ev("document.documentElement.classList.contains('rv-on')"));
  const y = await ev("Math.round(document.querySelector('#method').getBoundingClientRect().top + scrollY - 64)");
  await ev(`scrollTo({top:${y},behavior:'instant'})`);
  const t0 = Date.now();
  for (const t of [120, 420, 720, 1020, 1700]) { await sleep(Math.max(0, t - (Date.now() - t0))); await shot("f" + String(t).padStart(4, "0")); }
  // hover a name
  const r = JSON.parse(await ev("JSON.stringify((b=>({x:b.x+20,y:b.y+b.height/2}))(document.querySelectorAll('.wv-m a')[2].getBoundingClientRect()))"));
  await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: r.x, y: r.y }); await sleep(400);
  await shot("hover");
} finally { ws.close(); chrome.kill(); await sleep(400); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
