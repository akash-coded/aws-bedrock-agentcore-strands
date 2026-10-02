// Collision check for drawn figures: node check.mjs <url> <width> [height]
//   for every visible svg in a figure: text that leaves its box, text on text, text off the canvas,
//   a line through a label that has no backing; for every HTML figure: anything wider than its box.
import { spawn } from "node:child_process";
import { rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const [url, W = "1440", H = "900"] = process.argv.slice(2);
const SEL = process.env.SEL || "svg.bb, .dgs svg, figure.fig svg, svg.twr, svg.mg";
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9500 + Math.floor(Math.random() * 250);
const profile = join(tmpdir(), `check-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--no-first-run", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsurl; for (let i = 0; i < 60; i++) { try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); wsurl = l.find((t) => t.type === "page").webSocketDebuggerUrl; break; } catch {} await sleep(250); }
const ws = new WebSocket(wsurl); await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const waiting = new Map();
ws.addEventListener("message", (ev) => { const m = JSON.parse(ev.data); if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m.result || m.error); waiting.delete(m.id); } });
const send = (method, params = {}) => new Promise((ok) => { const id = ++seq; waiting.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
const ev = async (e) => { const r = await send("Runtime.evaluate", { expression: e, awaitPromise: true, returnByValue: true }); return r.result ? r.result.value : r; };
const PROBE = `(async () => {
  await document.fonts.ready;
  const out = [];
  const vis = (e) => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
  for (const svg of document.querySelectorAll(${JSON.stringify(SEL)})) {
    if (!vis(svg)) continue;
    const id = (svg.closest('[id]') || {}).id || svg.getAttribute('aria-label')?.slice(0, 40) || '?';
    const sb = svg.getBoundingClientRect();
    const k = svg.viewBox.baseVal.width ? sb.width / svg.viewBox.baseVal.width : 1;
    const texts = [...svg.querySelectorAll('text')].filter(vis).map(t => ({ t, b: t.getBoundingClientRect(), s: t.textContent.trim() })).filter(x => x.s);
    const rects = [...svg.querySelectorAll('rect')].filter(vis).map(r => ({ r, b: r.getBoundingClientRect() })).filter(x => x.b.width > 6 && x.b.height > 6);
    const issues = [];
    const tol = 1.2 * k;
    let minpx = 99;
    for (const x of texts) {
      const px = parseFloat(getComputedStyle(x.t).fontSize) * k; if (px < minpx) minpx = px;
      const cx = (x.b.left + x.b.right) / 2, cy = (x.b.top + x.b.bottom) / 2;
      const holders = rects.filter(q => q.b.left <= cx && q.b.right >= cx && q.b.top <= cy && q.b.bottom >= cy && q.b.width * q.b.height < sb.width * sb.height * 0.92)
        .sort((a, b) => a.b.width * a.b.height - b.b.width * b.b.height);
      x.holder = holders[0];
      if (holders[0]) { const h = holders[0].b; const pad = 3 * k;
        const over = Math.max(h.left + pad - x.b.left, x.b.right - (h.right - pad), 0);
        const overY = Math.max(h.top - x.b.top, x.b.bottom - h.bottom, 0);
        if (over > tol) issues.push('leaves its box by ' + (over / k).toFixed(1) + ': "' + x.s.slice(0, 50) + '"');
        if (overY > tol) issues.push('taller than its box by ' + (overY / k).toFixed(1) + ': "' + x.s.slice(0, 50) + '"'); }
      if (x.b.left < sb.left - tol || x.b.right > sb.right + tol || x.b.top < sb.top - tol || x.b.bottom > sb.bottom + tol) issues.push('off the canvas: "' + x.s.slice(0, 50) + '"');
    }
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i].b, b = texts[j].b; const sh = 1.5 * k;
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left) - sh, oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) - 0.42 * Math.min(a.height, b.height);
      if (ox > 0 && oy > 0) issues.push('text on text: "' + texts[i].s.slice(0, 32) + '" and "' + texts[j].s.slice(0, 32) + '"');
    }
    // a line through a label that has no backing of its own, or along a box edge through its text
    const strokes = [...svg.querySelectorAll('path, line, polyline')].filter(p => vis(p) && (getComputedStyle(p).fill === 'none' || p.tagName === 'line') && getComputedStyle(p).stroke !== 'none' && !p.closest('g[transform]'));
    for (const p of strokes) {
      let pts = [];
      try { const L = p.getTotalLength(); const m = p.getScreenCTM(); for (let d = 0; d <= L; d += 3) { const q = p.getPointAtLength(d); pts.push([q.x * m.a + q.y * m.c + m.e, q.x * m.b + q.y * m.d + m.f]); } } catch (e) { continue; }
      for (const x of texts) {
        const backed = x.holder && x.holder.b.width * x.holder.b.height < x.b.width * x.b.height * 3.2;
        if (backed) continue;
        const b = x.b; const sh = 1.5 * k;
        if (pts.some(([px, py]) => px > b.left + sh && px < b.right - sh && py > b.top + 0.22 * b.height && py < b.bottom - 0.22 * b.height)) { issues.push('a line crosses "' + x.s.slice(0, 44) + '"'); }
      }
    }
    out.push({ id, w: Math.round(sb.width), k: +k.toFixed(3), minpx: +minpx.toFixed(1), n: texts.length, issues: [...new Set(issues)] });
  }
  const html = [];
  for (const f of document.querySelectorAll('.bbn, .dgb, .poster')) {
    if (!vis(f)) continue;
    const fb = f.getBoundingClientRect(); const id = (f.closest('[id]') || {}).id || '?'; const bad = [];
    for (const e of f.querySelectorAll('*')) { if (!vis(e) || e.closest('svg')) continue; const b = e.getBoundingClientRect(); if (b.right > fb.right + 2.6 || b.left < fb.left - 2.6) { let clip = false; for (let p = e.parentElement; p && p !== f.parentElement; p = p.parentElement) { const o = getComputedStyle(p).overflowX; if (o !== 'visible') { clip = true; break; } } if (!clip) bad.push(e.tagName.toLowerCase() + '.' + e.className + ' +' + Math.round(b.right - fb.right)); } }
    let minpx = 99; const tw = document.createTreeWalker(f, NodeFilter.SHOW_TEXT); for (let n = tw.nextNode(); n; n = tw.nextNode()) { if (!n.nodeValue.trim() || !n.parentElement || n.parentElement.closest('svg,.vh') || !vis(n.parentElement)) continue; const px = parseFloat(getComputedStyle(n.parentElement).fontSize); if (px < minpx) minpx = px; }
    html.push({ id, w: Math.round(fb.width), minpx, bad: [...new Set(bad)].slice(0, 6) });
  }
  return JSON.stringify({ out, html, over: document.documentElement.scrollWidth - innerWidth });
})()`;
try {
  await send("Page.enable"); await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", { width: +W, height: +H, deviceScaleFactor: 1, mobile: +W < 600 });
  await send("Page.navigate", { url }); await sleep(1800);
  const raw = await ev(PROBE);
  if (typeof raw !== "string") { console.log("probe failed", JSON.stringify(raw).slice(0, 600)); }
  else {
    const r = JSON.parse(raw);
    let bad = 0;
    for (const f of r.out) { if (f.issues.length || f.minpx < 10.95) { bad++; console.log(`SVG ${f.id}  (w ${f.w}, scale ${f.k}, smallest ${f.minpx}px)`); for (const i of f.issues) console.log("    " + i); } }
    for (const f of r.html) { if (f.bad.length || f.minpx < 10.95) { bad++; console.log(`HTML ${f.id} (w ${f.w}, smallest ${f.minpx}px) ${f.bad.join("; ")}`); } }
    console.log(`${url} at ${W}: ${r.out.length} drawings and ${r.html.length} html figures looked at, ${bad} with faults` + (r.over > 0 ? `; PAGE SCROLLS SIDEWAYS by ${r.over}` : ""));
  }
} finally { ws.close(); chrome.kill(); await sleep(300); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
