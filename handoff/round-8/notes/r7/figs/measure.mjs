// Measure figure text: node measure.mjs [base] > report
//   loads each page at four widths and reports (1) every text node inside a figure, board or map whose
//   rendered font size is under 11px and (2) every figure that makes the page scroll sideways.
//   env PAGES="a,b" to limit pages, VERBOSE=1 to list each small text, THEME=light|dark (default dark)
import { spawn } from "node:child_process";
import { rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const BASE = process.argv[2] || "http://localhost:8877";
const OUT = process.argv[3] || "";
const THEME = process.env.THEME || "dark";
const ALL = ["/method/", "/frameworks/", "/product-manager/", "/engineering/", "/qa/", "/models/", "/prompts/",
  "/learn/what-is-the-agentic-pdlc/", "/learn/the-hard-gate/", "/learn/p0-frame/", "/learn/bolts-vs-sprints/"];
const PAGES = process.env.PAGES ? process.env.PAGES.split(",") : ALL;
const SIZES = process.env.WIDTHS ? process.env.WIDTHS.split(",").map((w) => [+w, 900]) : [[1440, 900], [1024, 768], [390, 844], [320, 640]];
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9800 + Math.floor(Math.random() * 150);
const profile = join(tmpdir(), `measure-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsurl;
for (let i = 0; i < 60; i++) { try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); wsurl = l.find((t) => t.type === "page").webSocketDebuggerUrl; break; } catch {} await sleep(250); }
const ws = new WebSocket(wsurl); await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const waiting = new Map();
ws.addEventListener("message", (ev) => { const m = JSON.parse(ev.data); if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m.result || m.error); waiting.delete(m.id); } });
const send = (method, params = {}) => new Promise((ok) => { const id = ++seq; waiting.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
const ev = async (e) => { const r = await send("Runtime.evaluate", { expression: e, awaitPromise: true, returnByValue: true }); return r.result ? r.result.value : undefined; };

// what counts as a figure, board or map on this site
const PROBE = `(() => {
  const SEL = 'figure.bbw, figure.dgb, figure.fig, figure.pfig, svg.twr, figure.lmodel, svg.mg, figure.poster, .dgs';
  const roots = [...document.querySelectorAll(SEL)].filter(r => !r.parentElement.closest(SEL));
  const name = (r) => (r.id ? '#' + r.id : '') + '.' + String(r.className.baseVal ?? r.className).trim().split(/\\s+/).join('.')
      + (r.getAttribute('aria-label') ? ' [' + r.getAttribute('aria-label').slice(0, 44) + ']' : (r.querySelector('svg[aria-label]') ? ' [' + r.querySelector('svg[aria-label]').getAttribute('aria-label').slice(0, 44) + ']' : ''));
  const small = [], wide = [], clipped = [];
  const vw = document.documentElement.clientWidth;
  for (const r of roots) {
    const w = document.createTreeWalker(r, NodeFilter.SHOW_TEXT);
    for (let n = w.nextNode(); n; n = w.nextNode()) {
      const s = n.nodeValue.trim(); if (!s) continue;
      const el = n.parentElement; if (!el || el.closest('style,script,title,desc,.vh,[hidden]')) continue;
      const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      if (!el.getClientRects().length) continue;
      let k = 1;
      const g = el.closest('svg');
      if (g && el instanceof SVGElement && el.getScreenCTM) { const m = el.getScreenCTM(); if (m) k = Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)); }
      const px = parseFloat(cs.fontSize) * k;
      if (px < 10.95) small.push({ fig: name(r), px: +px.toFixed(1), text: s.slice(0, 40) });
    }
    // a figure that runs past the viewport with nothing to scroll it inside
    const b = r.getBoundingClientRect();
    let clip = false; for (let p = r.parentElement; p && p !== document.body; p = p.parentElement) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden') { clip = true; break; } }
    if (!clip && b.right > vw + 1) wide.push({ fig: name(r), over: Math.round(b.right - vw) });
    // a scroller inside the figure (or the figure itself) that hides part of the drawing
    for (const s of [r, ...r.querySelectorAll('*')]) { const o = getComputedStyle(s).overflowX; if ((o === 'auto' || o === 'scroll') && s.scrollWidth > s.clientWidth + 1) clipped.push({ fig: name(r), hidden: s.scrollWidth - s.clientWidth, cue: !!(s.closest('[data-scrolls]') || s.matches('.scrolls') || s.closest('.scrolls')) }); }
  }
  return { figures: roots.length, small, wide, clipped, pageOver: Math.max(0, document.documentElement.scrollWidth - innerWidth) };
})()`;

let totalSmall = 0, totalWide = 0, totalFigs = 0, pagesOver = 0; const lines = []; const bySize = {};
try {
  await send("Page.enable"); await send("Runtime.enable");
  await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: THEME }, { name: "prefers-reduced-motion", value: "no-preference" }] });
  await send("Page.addScriptToEvaluateOnNewDocument", { source: `try{localStorage.setItem("manual-theme", ${JSON.stringify(THEME)})}catch(e){}` });
  for (const [w, h] of SIZES) {
    await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 600 });
    bySize[w] = { small: 0, wide: 0, over: 0 };
    for (const p of PAGES) {
      await send("Page.navigate", { url: BASE + p }); await sleep(+(process.env.WAIT || 1500));
      const r = await ev(PROBE);
      if (!r) { lines.push(`${w} ${p}: probe failed`); continue; }
      totalSmall += r.small.length; totalWide += r.wide.length; totalFigs += r.figures; if (r.pageOver) pagesOver++;
      bySize[w].small += r.small.length; bySize[w].wide += r.wide.length; bySize[w].over += r.pageOver ? 1 : 0;
      const per = {}; for (const s of r.small) { (per[s.fig] ||= []).push(s); }
      lines.push(`${String(w).padStart(4)} ${p}: ${r.figures} figures, ${r.small.length} texts under 11px` + (r.pageOver ? `, PAGE SCROLLS SIDEWAYS by ${r.pageOver}px` : "") + (r.wide.length ? `, figures past the edge: ${r.wide.map((x) => x.fig + " +" + x.over).join("; ")}` : ""));
      for (const [f, arr] of Object.entries(per)) { const mn = Math.min(...arr.map((a) => a.px)); lines.push(`       ${arr.length} under 11px (smallest ${mn}px) in ${f}` + (process.env.VERBOSE ? "\n" + arr.map((a) => `          ${a.px}px  ${a.text}`).join("\n") : "")); }
      for (const c of r.clipped) lines.push(`       scrolls inside its box, ${c.hidden}px hidden: ${c.fig}`);
    }
  }
} finally { ws.close(); chrome.kill(); await sleep(300); try { rmSync(profile, { recursive: true, force: true }); } catch {} }
const head = `TOTAL: ${totalSmall} text nodes under 11px across ${PAGES.length} pages x ${SIZES.length} widths (${totalFigs} figure renderings); ${totalWide} figures run past the page edge; ${pagesOver} page loads scroll sideways\n`
  + Object.entries(bySize).map(([w, v]) => `  at ${w}: ${v.small} under 11px, ${v.wide} past the edge, ${v.over} pages scrolling sideways`).join("\n");
const report = head + "\n\n" + lines.join("\n") + "\n";
if (OUT) writeFileSync(OUT, report);
console.log(report);
