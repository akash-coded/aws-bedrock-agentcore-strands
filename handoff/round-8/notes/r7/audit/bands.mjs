// Shoot each band of the home page after its entrance has finished. Motion on.
// usage: node bands.mjs <outDir> <width> <height> <light|dark> [bandIds comma list]
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const [outDir, W, H, theme, list] = process.argv.slice(2);
const width = +W, height = +H;
const BANDS = (list || "why,method,roles,simulator,tutorial,library,FOOT").split(",");
const SETTLE = +(process.env.SETTLE || 3600);
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 10200 + Math.floor(Math.random() * 3000);
const profile = join(tmpdir(), `bands-${PORT}`);
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
const shot = async (file) => { const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 80 }); writeFileSync(join(outDir, file), Buffer.from(data, "base64")); };
mkdirSync(outDir, { recursive: true });
try {
  await send("Page.enable"); await send("Runtime.enable"); await send("Log.enable");
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: width < 600 ? 2 : 1, mobile: width < 600 });
  await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: theme }, { name: "prefers-reduced-motion", value: "no-preference" }] });
  await send("Page.addScriptToEvaluateOnNewDocument", { source: `try{localStorage.setItem("manual-theme", ${JSON.stringify(theme)})}catch(e){}` });
  await send("Page.navigate", { url: process.env.URL || "http://localhost:8833/" });
  await sleep(2600);
  const tag = `b-${theme}-${width}`;
  const report = {};
  for (const id of BANDS) {
    const sel = id === "FOOT" ? "footer.ft" : "#" + id;
    const box = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(sel)});if(!e)return null;const r=e.getBoundingClientRect();return {top:r.top+scrollY,h:r.height}})()`);
    if (!box) { console.log("no band", id); continue; }
    report[id] = Math.round(box.h);
    const hd = await ev(`(document.querySelector("header.hd")||{offsetHeight:0}).offsetHeight`);
    let y = Math.max(0, box.top - hd), n = 0;
    const end = box.top + box.h;
    // step through first so the entrance triggers, then come back
    await ev(`scrollTo({top:${y},behavior:"instant"});1`); await sleep(SETTLE);
    while (true) {
      await ev(`scrollTo({top:${y},behavior:"instant"});1`); await sleep(n ? 1200 : 300);
      n++; await shot(`${tag}-${id}-${n}.jpg`);
      if (y + height >= end - 4 || n >= 8) break;
      y += height - hd - 60;
    }
  }
  const m = await ev(`({h: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth, iw: innerWidth})`);
  console.log(`${tag}: page ${m.h}px; bands ${JSON.stringify(report)}` + (m.sw > m.iw ? `; SCROLLS SIDEWAYS by ${m.sw - m.iw}px` : "") + (errors.length ? `; ERRORS: ${errors.join(" | ")}` : ""));
} finally { ws.close(); chrome.kill(); await sleep(400); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
