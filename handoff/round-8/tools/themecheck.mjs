import { spawn } from "node:child_process";
import { rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const BASE = process.argv[2];
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `tc-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--no-first-run", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsurl; for (let i = 0; i < 60; i++) { try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); wsurl = l.find((t) => t.type === "page").webSocketDebuggerUrl; break; } catch {} await sleep(250); }
const ws = new WebSocket(wsurl); await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const waiting = new Map();
ws.addEventListener("message", (ev) => { const m = JSON.parse(ev.data); if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m.result); waiting.delete(m.id); } });
const send = (method, params = {}) => new Promise((ok) => { const id = ++seq; waiting.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
const ev = async (e) => (await send("Runtime.evaluate", { expression: e, awaitPromise: true, returnByValue: true })).result.value;
const STATE = `JSON.stringify({bg:getComputedStyle(document.body).backgroundColor, ink:getComputedStyle(document.body).color, attr:document.documentElement.getAttribute('data-theme'), meta:document.querySelector('meta[name=theme-color]').content, label:document.querySelector('[data-theme-toggle]').getAttribute('aria-label'), scheme:getComputedStyle(document.documentElement).colorScheme, stored:localStorage.getItem('manual-theme')})`;
try {
  await send("Page.enable"); await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  for (const sys of ["light", "dark"]) {
    await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: sys }] });
    await send("Page.navigate", { url: BASE }); await sleep(1500);
    await ev("localStorage.clear()"); await send("Page.navigate", { url: BASE }); await sleep(1500);
    console.log(`system ${sys}, no choice:`, await ev(STATE));
  }
  await send("Emulation.setEmulatedMedia", { media: "print", features: [{ name: "prefers-color-scheme", value: "light" }] });
  await sleep(300); console.log("print:", await ev(STATE));
  await send("Emulation.setEmulatedMedia", { media: "", features: [{ name: "prefers-color-scheme", value: "light" }] });
  await ev("document.querySelector('[data-theme-toggle]').click()"); await sleep(300);
  console.log("after toggle:", await ev(STATE));
  await send("Page.navigate", { url: BASE + "qa/" }); await sleep(1500);
  console.log("next page:", await ev(STATE));
  await ev("document.querySelector('[data-theme-toggle]').click()"); await sleep(300);
  console.log("toggled back:", await ev(STATE));
} finally { ws.close(); chrome.kill(); await sleep(500); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
