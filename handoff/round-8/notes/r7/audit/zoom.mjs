// General driver with theme, motion, real mouse hover, real Tab key, and element clips.
// usage: node zoom.mjs <outDir> <width> <height> <light|dark> <steps.json>   env MOTION=0 for reduced motion, URL=...
// steps: {wait}, {eval}, {click:sel}, {shot:name}, {to:sel} scroll under header, {clip:sel,name,pad,scale},
//        {hover:sel}, {tab:n}, {key:"Escape"}, {rect:[x,y,w,h],name,scale} (viewport coords)
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const [outDir, W, H, theme, stepsFile] = process.argv.slice(2);
const width = +W, height = +H;
const steps = JSON.parse(readFileSync(stepsFile, "utf8"));
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 14200 + Math.floor(Math.random() * 3000);
const profile = join(tmpdir(), `zoom-${PORT}`);
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
const ev = async (e) => { const r = await send("Runtime.evaluate", { expression: e, awaitPromise: true, returnByValue: true }); return r.result ? r.result.value : (r.exceptionDetails ? "EXC " + JSON.stringify(r.exceptionDetails).slice(0, 300) : undefined); };
const save = (name, data) => writeFileSync(join(outDir, name + ".jpg"), Buffer.from(data, "base64"));
mkdirSync(outDir, { recursive: true });
const tag = `${theme}-${width}`;
try {
  await send("Page.enable"); await send("Runtime.enable"); await send("Log.enable");
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: width < 600 ? 2 : 1, mobile: width < 600 });
  if (width < 600) await send("Emulation.setTouchEmulationEnabled", { enabled: true });
  await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: theme }, { name: "prefers-reduced-motion", value: process.env.MOTION === "0" ? "reduce" : "no-preference" }] });
  if (!process.env.NOTHEME) await send("Page.addScriptToEvaluateOnNewDocument", { source: `try{localStorage.setItem("manual-theme", ${JSON.stringify(theme)})}catch(e){}` });
  await send("Page.navigate", { url: process.env.URL || "http://localhost:8833/" });
  await sleep(+(process.env.FIRST || 2400));
  for (const s of steps) {
    if (s.wait) await sleep(s.wait);
    if (s.eval) console.log("  eval:", JSON.stringify(await ev(s.eval)));
    if (s.click) { const ok = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(s.click)});if(!e)return false;e.click();return true})()`); if (!ok) console.log("  no element for", s.click); await sleep(300); }
    if (s.to) { await ev(`(()=>{const e=document.querySelector(${JSON.stringify(s.to)});const hd=(document.querySelector("header.hd")||{offsetHeight:0}).offsetHeight;scrollTo({top:e.getBoundingClientRect().top+scrollY-hd-(${s.off || 0}),behavior:"instant"})})()`); await sleep(s.settle || 300); }
    if (s.hover) { const r = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(s.hover)});if(!e)return null;const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`); if (!r) console.log("  no element for", s.hover); else { await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: r[0], y: r[1] }); await sleep(450); } }
    if (s.mclick) { const r = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(s.mclick)});if(!e)return null;const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()`); if (!r) console.log("  no element for", s.mclick); else { await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: r[0], y: r[1] }); await send("Input.dispatchMouseEvent", { type: "mousePressed", x: r[0], y: r[1], button: "left", clickCount: 1 }); await send("Input.dispatchMouseEvent", { type: "mouseReleased", x: r[0], y: r[1], button: "left", clickCount: 1 }); await sleep(450); } }
    if (s.tab) for (let i = 0; i < s.tab; i++) { await send("Input.dispatchKeyEvent", { type: "keyDown", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 }); await send("Input.dispatchKeyEvent", { type: "keyUp", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 }); await sleep(120); }
    if (s.key) { const vk = { Escape: 27, Enter: 13, " ": 32 }[s.key] || 0; await send("Input.dispatchKeyEvent", { type: "keyDown", key: s.key, code: s.key === " " ? "Space" : s.key, windowsVirtualKeyCode: vk, text: s.key === "Enter" ? "\r" : s.key === " " ? " " : undefined }); await send("Input.dispatchKeyEvent", { type: "keyUp", key: s.key, code: s.key === " " ? "Space" : s.key, windowsVirtualKeyCode: vk }); await sleep(300); }
    if (s.shot) { const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 82 }); save(`${s.shot}-${tag}`, data); }
    if (s.clip) { const r = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(s.clip)});if(!e)return null;const r=e.getBoundingClientRect();return [r.left+scrollX,r.top+scrollY,r.width,r.height]})()`);
      if (!r) console.log("  no element for", s.clip); else { const p = s.pad ?? 12; const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 88, clip: { x: Math.max(0, r[0] - p), y: Math.max(0, r[1] - p), width: r[2] + 2 * p, height: r[3] + 2 * p, scale: s.scale || 2 } }); save(`${s.name}-${tag}`, data); } }
    if (s.rect) { const sy = await ev("scrollY"); const [x, y, w, h] = s.rect; const { data } = await send("Page.captureScreenshot", { format: "jpeg", quality: 88, clip: { x, y: y + sy, width: w, height: h, scale: s.scale || 2 } }); save(`${s.name}-${tag}`, data); }
  }
  console.log(`${tag}: ` + (errors.length ? "ERRORS: " + errors.join(" | ") : "no script errors"));
} finally { ws.close(); chrome.kill(); await sleep(400); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
