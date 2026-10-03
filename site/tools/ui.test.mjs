// The site's parts, measured as a keyboard user, a phone and a pair of eyes meet them: focus rings, touch
// targets and contrast, on a page of every kind, at four widths in both themes.
//
//   python3 site/build.py
//   python3 -m http.server 8799 -d site/_site &
//   node site/tools/ui.test.mjs http://localhost:8799/
//
// Council 10's audit measured the site this way (twenty-one page states, 168 runs); this is its measurer,
// kept. Each run loads a page with the theme already chosen, scrolls through it so every reveal has played,
// presses Tab once so focus behaves as it does for a keyboard user, and measures. One Chrome, a few tabs
// (UI_TABS, default 3), each tab with storage of its own. UI_ONLY=<regex> runs only the states whose names
// match, for a quick look.
//
//   A6   a focus ring is never cut: no box that clips (overflow other than visible) cuts a ring by more
//        than 1px, after the browser has scrolled the focused thing into view as a Tab press would
//   A13  on a phone (390 and 320) every control is 44px tall or more: buttons, summaries, a label that wraps
//        a hidden checkbox, the footer's links. Links inside sentences are text. The stepper's dots are the
//        one exception, held instead to 24px between centres with a 24px touch area each. And any other
//        target under 24px is spaced so a 24px circle on it touches no other target (WCAG 2.5.8)
//   A14  every text is 4.5:1 or more against its backdrop (3:1 at 24px and over, or 18.66px bold), placeholders
//        included. Anything that fails on its stylesheet's colours, or sits on a gradient or a picture, is
//        measured again from the screen's own pixels, and the pixels decide. A disabled control is exempt
//   A15  every focus ring inside a code box is 3:1 or more against what it is drawn on
//   A1   no code box scrolls sideways at 1024 and 390: a prompt or a template wraps (every fold opened to look)
//   A4   the home page's role rows start on the column their heading sets (1px), at every width, and no rule
//        moves a row's words on hover (no padding in a .seats a:hover rule, none in its transition)
//   A10  on a phone (390 and 320) the top bar sits on the page's column: the menu icon starts and the theme
//        circle ends within 1px of 20px and of the width less 20px
//   A11  on a page with a rail, at 1440 and 1024, the rail's heading and the page's eyebrow share a text top (1px)
//   copy Copy copies a prompt or a template exactly as its source in content/roles/ has it, byte for byte, with
//        the box wrapped (prompts, templates and a role page, at 390)
//   404  the 404 page wears the site's eyebrow (Geist Mono, loaded, with its leading rule) and the site's 3px
//        focus ring, and its list's words start on its column
//   A7   one set of corners: every box 120 by 60px or larger (a border, a fill or a shadow, rounded) has corners of
//        11, 16 or 20px (a box inside a box, a box on the page, a tile); a pill or a circle is not a box
//   A8   one set of buttons: every button that is drawn as one (.btn, a button with a border or a fill) and every pill
//        a reader presses is 36, 43 or 51px tall at 1440 (1px either way) and 44px or more at 390, and a button's
//        corner is 11px. Copy, the day card's answers and the stepper's dots are their own components
//   A9   one heading scale: on every inner page every h2 is 27px at 620 at 1440, every h3 is 19.5px (a summary's
//        title) or 18px (a subhead). The home page's bands, the lessons, the game and the lab's bench keep their own
//   A12  no visible text is set in capitals by text-transform
//   A2   one page head: on every landing page, at 1440 and 390, the eyebrow's text sits within 2px of where its
//        variant's sits on the others (the full head, or the head in a column beside a rail); every eyebrow is
//        written .eyebrow; the head's lede is 56 characters a line or fewer
//   A3   crumbs that lead somewhere: one crumb is the page, the last; on a phone the crumb shown is a link back
//   A5   tables that fit a phone: at 390 and 320 no table scrolls sideways (every fold opened), unless marked .wide
//
// A5, A7, A8, A9 and A12 measure with every fold open (a step, a how-to, a reference), as a reader can open them.
// UI_CHECKS=<regex> runs only the checks whose ids match.
//
// A check is a small function over one run's measurements (CHECKS, near the end); what it reads is gathered
// in the page by a collector of the same kind (COLLECTORS). A new check adds its collector and its function. A check
// that compares pages with each other also has an `across` function, given every run it applies to.
// Faults that live in a part another parcel replaces or owns are listed in KNOWN, with the owner; they are
// printed, they do not fail, and an entry that no longer matches anything is reported so it can go.
//
// It prints one line per check and a closing line, and exits 1 if a check fails.

import { spawn } from "node:child_process";
import { readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const BASE = process.argv[2];
if (!BASE || !/\/$/.test(BASE)) { console.error("usage: node ui.test.mjs <site url, ending in />"); process.exit(2); }
const TABS = Math.max(1, +process.env.UI_TABS || 3);
const ONLY = process.env.UI_ONLY ? new RegExp(process.env.UI_ONLY) : null;
const PICK = process.env.UI_CHECKS ? new RegExp(`^(?:${process.env.UI_CHECKS})$`) : null;
const WIDTHS = [1440, 1024, 390, 320], THEMES = ["dark", "light"];
const WHOLE = "/aws-bedrock-agentcore-strands/";      // the 404 page asks for whole addresses, served here from BASE

// ------------------------------------------------------------------ the twenty-one page states
const SEARCH = `(async () => { document.querySelector('details.menu').open = true; const i = document.querySelector('[data-search]');
  i.focus(); i.value = 'gate'; i.dispatchEvent(new Event('input', { bubbles: true })); await new Promise((r) => setTimeout(r, 900));
  return document.querySelectorAll('[data-search-results] li').length; })()`;
const STATES = [
  { name: "home", path: "" },
  { name: "method", path: "method/" },
  { name: "role-pm", path: "product-manager/", role: "product-manager" },
  { name: "protocol", path: "protocol/" },
  { name: "templates", path: "templates/" },
  { name: "prompts", path: "prompts/" },
  { name: "models", path: "models/" },
  { name: "frameworks", path: "frameworks/" },
  { name: "pictures", path: "pictures/" },
  { name: "tools", path: "tools/" },
  { name: "tool-desk", path: "tools/claude-at-the-desk/" },
  { name: "labs", path: "labs/" },
  { name: "lab-grow", path: "labs/grow-the-spec/" },
  { name: "learn", path: "learn/" },
  { name: "lesson-hardgate", path: "learn/the-hard-gate/" },
  { name: "lesson-evolution", path: "learn/evolution-of-the-pdlc/" },
  { name: "sim-title", path: "simulator/" },
  { name: "sim-day45", path: "simulator/#day-45", wait: 1800 },
  { name: "workbench", path: "workbench/", wait: 2500 },
  { name: "search", path: "", before: SEARCH, root: ".mp" },      // the drawer open on the query "gate"
  { name: "404", path: "404.html" },
];

// ------------------------------------------------------------------ faults owned elsewhere
// Each entry: the check ("*" for all), the states, a pattern the fault's line must match (its selector, its words,
// the box that clips it), who owns the fix and why it is not fixed here. `tool: true` matches anything inside the
// workbench's pristine tool (not its sw- frame).
const KNOWN = [
  { check: "A2", state: /^learn$/, match: /eyebrow's text top/, owner: "the lesson lane, learn.py's _rail",
    why: "on a phone the tutorial's front page opens on its course list's fold, above its title, so its eyebrow sits 73px lower" },
  { check: "*", state: /^workbench$/, tool: true, owner: "U5", why: "the workbench's own faults, fixed in its source and exported (workbench.test.mjs)" },
  { check: "A7", state: /^sim-/, match: /\.nd-/, owner: "the game", why: "the game's own parts (play/game.css, GAME.md): its role cards at 14px" },
  { check: "A8", state: /^sim-/, match: /\.nd-/, owner: "the game", why: "the game's own buttons (play/game.css, GAME.md): 45px at 12, every button on its title as tall as Start (playtest.mjs), room chips 52px" },
];

// ------------------------------------------------------------------ measured inside the page
// HELPERS is built once per run in the page and handed to every collector. Each collector is a self-contained
// function of it (it is sent to the page as text), and returns plain data.
function HELPERS(opt) {
  const DE = document.documentElement, W = DE.clientWidth;
  const root = (opt.root && document.querySelector(opt.root)) || document.body;
  const framed = DE.classList.contains("sw-framed");
  // a colour painted on black and on white gives its true rgb and alpha, whatever syntax the browser reports
  const cv = document.createElement("canvas"); cv.width = cv.height = 1;
  const cx = cv.getContext("2d", { willReadFrequently: true });
  const memoC = new Map();
  const paint = (base, c) => { cx.globalCompositeOperation = "copy"; cx.fillStyle = base; cx.fillRect(0, 0, 1, 1);
    cx.globalCompositeOperation = "source-over"; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); return cx.getImageData(0, 0, 1, 1).data; };
  const rgba = (c) => {
    if (memoC.has(c)) return memoC.get(c);
    const k = paint("#000", c), w = paint("#fff", c);
    const a = Math.max(0, Math.min(1, 1 - (w[0] - k[0] + w[1] - k[1] + w[2] - k[2]) / 765));
    const v = a > 0.004 ? [Math.min(255, k[0] / a), Math.min(255, k[1] / a), Math.min(255, k[2] / a), a] : [0, 0, 0, 0];
    memoC.set(c, v); return v;
  };
  const over = (t, u) => [0, 1, 2].map((i) => t[i] * t[3] + u[i] * (1 - t[3])).concat(1);
  const lum = ([r, g, b]) => { const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const cr = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const hex = (c) => "#" + c.slice(0, 3).map((v) => Math.round(v).toString(16).padStart(2, "0")).join("").toUpperCase();
  const r1 = (v) => Math.round(v * 10) / 10;
  // names: a short selector, and one with the ids taken out, to group the same part across a page
  const cls = (x) => (typeof x.className === "string" ? x.className : (x.className && x.className.baseVal) || "").trim().split(/\s+/).filter(Boolean);
  const part = (x) => x.tagName.toLowerCase() + (x.id ? "#" + x.id : "") + cls(x).slice(0, 2).map((c) => "." + c).join("");
  const sel = (e) => { const p = []; for (let x = e, i = 0; x && i < 3 && x !== document.body && x !== DE; i++, x = x.parentElement) p.unshift(part(x)); return p.join(" > "); };
  const kind = (s) => s.replace(/#[\w-]+/g, "#*");
  const text = (e, n = 40) => ((e.innerText || e.textContent || "").replace(/\s+/g, " ").trim() || e.getAttribute("aria-label") || "").slice(0, n);
  // the workbench is the pristine tool inside the site's frame, whose parts carry an sw- prefix
  const tool = (e) => { if (!framed) return false; const f = e.closest('[class^="sw-"],[class*=" sw-"],[id^="sw-"]'); return !f || f === DE; };
  // visible: painted, on screen sideways, and not clipped to nothing by an ancestor. The memo holds while the folds
  // stay as they are: a collector that opens or shuts them calls fresh(), which also lays the page out again, as
  // the first checkVisibility() after a fold opens can answer for the page as it was
  const memoV = new Map(), fresh = () => { memoV.clear(); void DE.offsetHeight; };
  const clippedAway = (e) => {
    for (let a = e; a && a !== DE; a = a.parentElement) {
      if (memoV.has(a)) { if (memoV.get(a)) return true; continue; }
      const cs = getComputedStyle(a), r = a.getBoundingClientRect();
      const hid = /rect\(0(px)?,? 0/.test(cs.clip) || /inset\(50%/.test(cs.clipPath) || ((cs.overflow === "hidden" || cs.overflow === "clip") && (r.width <= 1 || r.height <= 1));
      memoV.set(a, hid); if (hid) return true;
    }
    return false;
  };
  const isVis = (e) => {
    if (!e || !e.checkVisibility || !e.checkVisibility({ opacityProperty: true, visibilityProperty: true, contentVisibilityAuto: true })) return false;
    const r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1 || r.right < -20 || r.left > W + 20) return false;
    return !clippedAway(e);
  };
  // the colour behind an element: its own and its ancestors' backgrounds composited, and whether a gradient or
  // a picture is among them (then only the screen's pixels can say)
  const pageBg = over(rgba(getComputedStyle(document.body).backgroundColor), over(rgba(getComputedStyle(DE).backgroundColor), [255, 255, 255, 1]));
  const memoB = new Map();
  const bgOf = (e) => {
    if (!e || e === DE || e === document.body) return { c: pageBg, img: false };
    if (memoB.has(e)) return memoB.get(e);
    const cs = getComputedStyle(e), under = bgOf(e.parentElement), c = rgba(cs.backgroundColor);
    let v;
    if (cs.backgroundImage && cs.backgroundImage !== "none") v = { c: c[3] > 0 ? over(c, under.c) : under.c, img: true };
    else if (c[3] >= 0.995) v = { c, img: false };
    else if (c[3] > 0) v = { c: over(c, under.c), img: under.img };
    else v = under;
    memoB.set(e, v); return v;
  };
  const opacity = (e) => { let op = 1; for (let a = e; a && a !== DE; a = a.parentElement) op *= +getComputedStyle(a).opacity; return op; };
  return { DE, W, root, rgba, over, cr, hex, r1, sel, kind, text, tool, isVis, bgOf, opacity, fresh };
}

// In the order they run: focus last, because focusing scrolls the page, its rails and its tables.
const COLLECTORS = {
  // A14: every text node's colour against its backdrop. Candidates (a fail on the stylesheet's colours, or text
  // on a gradient or a picture) keep a handle on their text node for the pixel check done from outside.
  contrast(H) {
    const { root, rgba, over, cr, hex, r1, sel, isVis, bgOf, opacity, tool } = H;
    const out = { n: 0, cands: [], placeholders: [] };
    const nodes = (window.__uiT = []);
    const seen = new Set();
    const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.nodeValue.trim() ? 1 : 3) });
    for (let n = tw.nextNode(); n; n = tw.nextNode()) {
      const e = n.parentElement;
      if (!e || seen.has(e)) continue;
      seen.add(e);
      if (e.closest("script,style,noscript,template,title,option") || !isVis(e)) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      const rr = rg.getBoundingClientRect(); if (rr.width < 1 || rr.height < 1) continue;
      const cs = getComputedStyle(e), svg = e.closest("svg");
      let fs = parseFloat(cs.fontSize);
      if (svg) { const m = e.getScreenCTM && e.getScreenCTM(); if (m) fs *= Math.hypot(m.a, m.b); }
      fs = r1(fs);
      let fg, bg, img, raw, alpha;
      if (svg) {
        if (!cs.fill || cs.fill === "none" || /url\(/.test(cs.fill)) continue;
        raw = rgba(cs.fill); alpha = raw[3] * +cs.fillOpacity * opacity(e);
        const host = bgOf(svg.parentElement); bg = host.c; img = host.img;
        try {   // the shapes painted under the text in the same drawing
          const bb = e.getBBox(), m = e.getScreenCTM();
          const p = new DOMPoint(bb.x + bb.width * 0.5, bb.y + bb.height * 0.55).matrixTransform(m);
          for (const sh of svg.querySelectorAll("rect,circle,ellipse,path,polygon")) {
            if (!(sh.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING) || sh.contains(e)) continue;
            const scs = getComputedStyle(sh); if (!scs.fill || scs.fill === "none" || /url\(/.test(scs.fill)) continue;
            const sm = sh.getScreenCTM(); if (!sm) continue;
            let inside = false; try { inside = sh.isPointInFill(p.matrixTransform(sm.inverse())); } catch {}
            if (!inside) continue;
            const c = rgba(scs.fill); bg = over([c[0], c[1], c[2], c[3] * +scs.fillOpacity * opacity(sh)], bg);
          }
        } catch {}
      } else {
        if (/text/.test(cs.backgroundClip || cs.webkitBackgroundClip || "")) continue;       // gradient text: not measured
        const tf = cs.webkitTextFillColor;
        raw = rgba(tf && tf !== cs.color && rgba(tf)[3] > 0 ? tf : cs.color); alpha = raw[3] * opacity(e);
        const b = bgOf(e); bg = b.c; img = b.img;
      }
      fg = over([raw[0], raw[1], raw[2], alpha], bg);
      out.n++;
      const ratio = cr(fg, bg), need = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700) ? 3 : 4.5;
      if (ratio >= need && !img) continue;
      out.cands.push({ ti: nodes.push(n) - 1, sel: sel(e), txt: n.nodeValue.replace(/\s+/g, " ").trim().slice(0, 32), fs, need, css: +ratio.toFixed(2),
        fg: hex(raw), fgA: +alpha.toFixed(3), img, dis: !!e.closest(':disabled,[aria-disabled="true"],.disabled'), tool: tool(e) });
    }
    for (const i of root.querySelectorAll("input[placeholder],textarea[placeholder]")) {
      if (!isVis(i)) continue;
      const b = bgOf(i).c, fg = over(rgba(getComputedStyle(i, "::placeholder").color), b), ratio = cr(fg, b);
      out.placeholders.push({ sel: sel(i) + "::placeholder", txt: i.placeholder.slice(0, 32), ratio: +ratio.toFixed(2), fg: hex(fg), bg: hex(b), tool: tool(i) });
    }
    // for the pixel check: bring a candidate's first line to the middle of the screen and give its box on the page
    window.__uiBox = async (k) => {
      const n = window.__uiT[k]; if (!n || !n.parentElement) return null;
      n.parentElement.scrollIntoView({ block: "center", inline: "nearest", behavior: "instant" });
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(r, 40))));
      const rg = document.createRange(); rg.selectNodeContents(n);
      const q = [...rg.getClientRects()].find((q) => q.width > 2 && q.height > 2) || rg.getBoundingClientRect();
      if (!q || q.width < 2 || q.height < 4) return null;
      const inset = Math.max(1, Math.round(q.height * 0.12)), x = Math.max(0, q.left);
      return { x: x + scrollX, y: q.top + inset + scrollY, width: Math.max(2, Math.min(q.right, innerWidth) - x), height: Math.max(2, q.height - 2 * inset) };
    };
    // the text made transparent for a moment, so the backdrop can be shot alone
    window.__uiHide = async (k, on) => {
      const e = window.__uiT[k].parentElement, p = ["color", "fill", "-webkit-text-fill-color", "text-shadow", "text-decoration-color", "transition"];
      if (on) { e.__ui = p.map((q) => [q, e.style.getPropertyValue(q), e.style.getPropertyPriority(q)]);
        for (const q of p) e.style.setProperty(q, q === "text-shadow" || q === "transition" ? "none" : "transparent", "important"); }
      else for (const [q, v, pr] of e.__ui) v ? e.style.setProperty(q, v, pr) : e.style.removeProperty(q);
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    };
    // the backdrop is the median pixel of the line shot without its text; the text's colour is composited over it.
    // The shot with the text must differ from it somewhere, or the line was not there to see.
    window.__uiPx = async (withText, without, fgHex, a) => {
      const read = async (b64) => { const bm = await createImageBitmap(await (await fetch("data:image/png;base64," + b64)).blob());
        const c = new OffscreenCanvas(bm.width, bm.height), x = c.getContext("2d"); x.drawImage(bm, 0, 0); return x.getImageData(0, 0, bm.width, bm.height).data; };
      const d = await read(without), t = await read(withText), px = [];
      for (let i = 0; i < d.length; i += 4) px.push([d[i], d[i + 1], d[i + 2]]);
      const L = ([r, g, b]) => 0.2126 * r + 0.7152 * g + 0.0722 * b;
      px.sort((p, q) => L(p) - L(q));
      const B = px[px.length >> 1];
      let ink = 1; for (let i = 0; i < t.length; i += 4) ink = Math.max(ink, cr([t[i], t[i + 1], t[i + 2]], B));
      const css = [1, 3, 5].map((i) => parseInt(fgHex.slice(i, i + 2), 16)), comp = css.map((v, i) => v * a + B[i] * (1 - a));
      return { bg: hex(B), ink: +ink.toFixed(2), ratio: +cr(comp, B).toFixed(2) };
    };
    return out;
  },

  // A13: controls on a phone, the stepper's dots, and every other small target's spacing
  targets(H) {
    const { root, W, r1, sel, kind, text, isVis, tool } = H;
    const out = { n: 0, short: [], dots: [], crowded: [] };
    const hiddenInput = (i) => { if (!i) return false; const cs = getComputedStyle(i), r = i.getBoundingClientRect();
      return +cs.opacity < 0.05 || r.width < 2 || r.height < 2 || /inset\(50%/.test(cs.clipPath) || /rect\(0/.test(cs.clip); };
    const inSentence = (e) => getComputedStyle(e).display === "inline" && [...e.parentElement.childNodes].some((c) => c !== e && c.nodeType === 3 && c.nodeValue.trim().length > 1);
    const seen = new Set();
    for (const e of root.querySelectorAll("button,summary,[role=button],input[type=submit],input[type=button],input[type=reset],label,.ft a")) {
      if (!isVis(e) || e.closest("[inert]")) continue;
      if (e.tagName === "LABEL") {
        const i = e.querySelector("input[type=checkbox],input[type=radio]") || (e.htmlFor && document.getElementById(e.htmlFor));
        if (!i || !/^(checkbox|radio)$/.test(i.type) || !hiddenInput(i)) continue;
      }
      if (e.tagName === "A" && inSentence(e)) continue;
      if (e.matches(".stp-dot")) continue;                            // held to 24px below
      out.n++;
      const h = r1(e.getBoundingClientRect().height);
      const s = sel(e), k = kind(s) + "|" + Math.round(h);
      if (h < 44 && !seen.has(k)) { seen.add(k); out.short.push({ sel: s, h, txt: text(e, 30), tool: tool(e) }); }
    }
    // the stepper's dots: 24px between centres, and each answers a tap across 24px, swept through its centre both
    // ways (the browser hit-tests whole pixels, so a sweep, not a single point either side)
    for (const g of root.querySelectorAll("[data-step-dots]")) {
      const ds = [...g.children].filter(isVis); if (ds.length < 2) continue;
      g.scrollIntoView({ block: "center", behavior: "instant" });
      const c = ds.map((d) => { const r = d.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; });
      let apart = Infinity, area = Infinity;
      for (let i = 1; i < c.length; i++) apart = Math.min(apart, Math.hypot(c[i][0] - c[i - 1][0], c[i][1] - c[i - 1][1]));
      const hits = (d, x, y) => { const at = document.elementFromPoint(x, y); return at === d || d.contains(at); };
      ds.forEach((d, i) => {
        const span = (dx, dy) => { let n = hits(d, c[i][0], c[i][1]) ? 0.25 : 0;
          for (const s of [-1, 1]) for (let t = 0.25; t < 20 && hits(d, c[i][0] + s * dx * t, c[i][1] + s * dy * t); t += 0.25) n += 0.25;
          return n; };
        area = Math.min(area, span(1, 0), span(0, 1)); });
      out.dots.push({ sel: sel(g), apart: r1(apart), area: r1(area), n: ds.length });
    }
    // WCAG 2.5.8: a target whose box is under 24px, and whose 24px circle touches another target (what a finger can
    // hit of it: a link that wraps is its lines, not the box round them) or another small target's circle
    const T = [...root.querySelectorAll("a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],label")].filter((e) => {
      if (e.tagName === "LABEL") { const i = e.querySelector("input[type=checkbox],input[type=radio]") || (e.htmlFor && document.getElementById(e.htmlFor)); if (!i || isVis(i)) return false; }
      return isVis(e) && !e.closest("[inert]");
    }).map((e) => { const r = e.getBoundingClientRect(), inl = getComputedStyle(e).display === "inline";
      return { e, r, frags: inl ? [...e.getClientRects()].filter((q) => q.width > 0 && q.height > 0) : [r], inline: e.tagName === "A" && inSentence(e) }; });
    const small = T.filter((t) => !t.inline && (t.r.width < 24 || t.r.height < 24));
    const done = new Set();
    for (const t of small) {
      const x = t.r.left + t.r.width / 2, y = t.r.top + t.r.height / 2;
      let near = null;
      for (const o of T) {
        if (o === t || o.e.contains(t.e) || t.e.contains(o.e)) continue;
        if (o.frags.some((q) => Math.hypot(Math.max(q.left - x, 0, x - q.right), Math.max(q.top - y, 0, y - q.bottom)) < 12)) { near = o; break; }
        if (!o.inline && (o.r.width < 24 || o.r.height < 24) && Math.hypot(o.r.left + o.r.width / 2 - x, o.r.top + o.r.height / 2 - y) < 24) { near = o; break; }
      }
      const s = sel(t.e), k = kind(s);
      if (near && !done.has(k)) { done.add(k); out.crowded.push({ sel: s, w: r1(t.r.width), h: r1(t.r.height), near: sel(near.e), txt: text(t.e, 30), tool: tool(t.e) }); }
    }
    return out;
  },

  // A1: every code box, with every fold that holds one opened for the measure and shut again after
  wrap(H) {
    const { root, sel, text, isVis } = H;
    const st = document.createElement("style");
    st.textContent = "*,*::before,*::after{transition:none!important}::details-content{transition:none!important}";
    document.head.appendChild(st);
    const shut = [...root.querySelectorAll("details:not([open])")].filter((d) => d.querySelector(".blk pre,.codebox pre"));
    shut.forEach((d) => (d.open = true));
    H.fresh();
    const out = { n: 0, over: [] };
    for (const p of root.querySelectorAll(".blk pre,.codebox pre")) {
      if (!isVis(p)) continue;
      out.n++;
      const hidden = p.scrollWidth - p.clientWidth;
      if (hidden > 1) out.over.push({ sel: sel(p), hidden, share: Math.round((100 * hidden) / p.scrollWidth), txt: text(p, 30), tool: H.tool(p) });
    }
    shut.forEach((d) => (d.open = false));
    H.fresh();
    st.remove();
    return out;
  },

  // A4: the home page's role rows against their heading, and the rules that run on hover
  seats(H) {
    const band = document.querySelector("#roles"), row = band && band.querySelector(".seats a");
    if (!row) return null;
    const left = (e) => { const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.nodeValue.trim() ? 1 : 3) });
      const n = w.nextNode(), rg = document.createRange(); rg.selectNodeContents(n); return rg.getClientRects()[0].left; };
    const moves = [];
    const walk = (rules) => { for (const r of rules) { if (r.cssRules) walk(r.cssRules);
      if (r.selectorText && /\.seats a:hover/.test(r.selectorText) && [...r.style].some((p) => /^padding/.test(p))) moves.push(r.selectorText); } };
    for (const sh of document.styleSheets) { try { walk(sh.cssRules); } catch {} }
    return { h2: H.r1(left(band.querySelector("h2"))), code: H.r1(left(row.querySelector(".s-code"))), moves, transition: getComputedStyle(row).transitionProperty };
  },

  // A10: the top bar's two ends on a phone
  header(H) {
    const icon = document.querySelector(".hd .menu>summary svg"), tgl = document.querySelector(".hd .tgl");
    if (!icon || !tgl || !H.isVis(tgl)) return null;
    return { icon: H.r1(icon.getBoundingClientRect().left), tgl: H.r1(tgl.getBoundingClientRect().right), w: H.W };
  },

  // A11: the rail's heading and the page head's eyebrow, text top to text top
  railtop(H) {
    const rail = document.querySelector("aside.rail:not(.lrail)"), ey = document.querySelector("main .phead :is(.kicker,.eyebrow)");
    if (!rail || !ey || !H.isVis(rail) || !H.isVis(ey)) return null;
    const top = (e) => { const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.nodeValue.trim() ? 1 : 3) });
      const n = w.nextNode(), rg = document.createRange(); rg.selectNodeContents(n); return rg.getClientRects()[0].top + scrollY; };
    return { rail: H.r1(top(rail)), eyebrow: H.r1(top(ey)), railSel: H.sel(rail.querySelector("p,h2,a") || rail) };
  },

  // copy: every Copy pressed, as a reader would, with its fold open (a closed step's text is not rendered), and
  // with the clipboard's writer replaced by one that keeps what it is given
  async copy(H) {
    const got = {}, cb = navigator.clipboard;
    if (!cb) return null;
    const st = document.createElement("style");
    st.textContent = "*,*::before,*::after{transition:none!important}::details-content{transition:none!important}";
    document.head.appendChild(st);
    const shut = [...H.root.querySelectorAll("details:not([open])")].filter((d) => d.querySelector("[data-copy]"));
    shut.forEach((d) => (d.open = true));
    const was = cb.writeText;
    cb.writeText = (t) => { got.last = t; return Promise.resolve(); };
    const out = [];
    for (const b of H.root.querySelectorAll("[data-copy]")) {
      got.last = null; b.click(); await new Promise((r) => setTimeout(r, 0));
      out.push({ id: b.getAttribute("data-copy"), text: got.last });
    }
    cb.writeText = was;
    shut.forEach((d) => (d.open = false));
    st.remove();
    return out;
  },

  // 404: its eyebrow, its focus ring and its list against its column
  async notfound(H) {
    if (document.querySelector(".hd") || !document.querySelector("main .k")) return null;
    const k = document.querySelector("main .k"), cs = getComputedStyle(k), b = getComputedStyle(k, "::before");
    const family = cs.fontFamily.split(",")[0].replace(/["']/g, "").trim();
    const loaded = [...document.fonts].some((f) => f.family.replace(/["']/g, "") === family && f.status === "loaded");
    const rings = [];
    for (const a of document.querySelectorAll("a[href]")) { a.focus(); const c = getComputedStyle(a); rings.push(a.matches(":focus-visible") ? c.outlineStyle + " " + c.outlineWidth : "none"); a.blur(); }
    const left = (e) => { const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.nodeValue.trim() ? 1 : 3) });
      const n = w.nextNode(), rg = document.createRange(); rg.selectNodeContents(n); return rg.getClientRects()[0].left; };
    return { family, loaded, rule: b.content !== "none" && parseFloat(b.width) >= 12, rings: [...new Set(rings)],
      h1: H.r1(left(document.querySelector("main h1"))), row: H.r1(left(document.querySelector("main li a"))) };
  },

  // A7, A8, A9, A12: the page's parts, with every fold open (not the top bar's lists or the drawer): the corners of
  // its boxes, the height and corner of its buttons and pills, its headings, and any text set in capitals
  parts(H) {
    const { root, r1, sel, kind, text, isVis, tool, rgba } = H;
    const st = document.createElement("style");
    st.textContent = "*,*::before,*::after{transition:none!important}::details-content{transition:none!important}";
    document.head.appendChild(st);
    const shut = [...root.querySelectorAll("details:not([open])")].filter((d) => !d.closest(".hd") && !tool(d));
    shut.forEach((d) => (d.open = true));
    H.fresh();
    const out = { boxes: [], ctrls: [], heads: [], caps: [], n: { boxes: 0, ctrls: 0, heads: 0, caps: 0 } };
    // a corner as px (a percentage is of the shorter side), and whether a box is drawn at all
    const corners = (cs, r) => ["TopLeft", "TopRight", "BottomRight", "BottomLeft"].map((c) => {
      const v = cs["border" + c + "Radius"].split(" ")[0]; return v.endsWith("%") ? (parseFloat(v) / 100) * Math.min(r.width, r.height) : parseFloat(v); });
    const drawn = (cs) => rgba(cs.backgroundColor)[3] > 0.01 || (cs.backgroundImage && cs.backgroundImage !== "none") || (cs.boxShadow && cs.boxShadow !== "none") ||
      ["Top", "Right", "Bottom", "Left"].some((s) => parseFloat(cs["border" + s + "Width"]) > 0 && cs["border" + s + "Style"] !== "none" && rgba(cs["border" + s + "Color"])[3] > 0.01);
    const hiddenInput = (l) => { const i = l.querySelector("input[type=checkbox],input[type=radio]"); if (!i) return false;
      const cs = getComputedStyle(i), r = i.getBoundingClientRect(); return +cs.opacity < 0.05 || r.width < 2 || r.height < 2 || /inset\(50%/.test(cs.clipPath); };
    const seen = new Set();
    const once = (list, k, v) => { if (!seen.has(k)) { seen.add(k); list.push(v); } };
    for (const e of root.querySelectorAll("*")) {
      if ((e instanceof SVGElement && e.tagName.toLowerCase() !== "svg") || !isVis(e)) continue;
      const cs = getComputedStyle(e), r = e.getBoundingClientRect(), s = sel(e), t = tool(e);
      const cn = corners(cs, r), round = cn.filter((x) => x > 0.4), pill = round.length > 0 && round.every((x) => x >= Math.min(r.width, r.height) / 2 - 0.6);
      // A7: a box, rounded, 120 by 60 or larger, that is not a pill or a circle
      if (round.length && !pill && cs.display !== "inline" && r.width >= 120 && r.height >= 60 && drawn(cs)) {
        out.n.boxes++;
        const c = cn.map(r1).join("/");
        once(out.boxes, "b|" + kind(s) + "|" + c, { sel: s, corners: c, round: round.map(r1), w: r1(r.width), h: r1(r.height), tool: t });
      }
      // A8: a button drawn as one, or a pill a reader presses
      if (!e.closest("[inert]") && !e.matches(".cp,.stp-dot,.dc-o :is(a,button)") && !e.closest(".bh")) {
        const btn = e.matches('.btn,button,[role=button],input:is([type=submit],[type=button],[type=reset])') && drawn(cs);
        const presses = e.matches("a[href],summary") || (e.tagName === "LABEL" && hiddenInput(e));
        if (btn || (presses && pill && drawn(cs))) {
          out.n.ctrls++;
          once(out.ctrls, "c|" + kind(s) + "|" + Math.round(r.height) + "|" + r1(cn[0]), { sel: s, h: r1(r.height), corner: pill ? "pill" : r1(cn[0]), txt: text(e, 24), tool: t });
        }
      }
      // A9: the headings of the page
      if (/^H[23]$/.test(e.tagName) && e.closest("main")) {
        out.n.heads++;
        once(out.heads, "h|" + kind(s) + "|" + cs.fontSize + "|" + cs.fontWeight, { sel: s, tag: e.tagName.toLowerCase(), fs: r1(parseFloat(cs.fontSize)), fw: +cs.fontWeight,
          own: !!e.closest(".h4,.daycard,.nd-app,.lab-bench,.lm,.sec-h,.play-t,.tour-card"), txt: text(e, 30), tool: t });
      }
      // A12: text in capitals by text-transform
      if ([...e.childNodes].some((n) => n.nodeType === 3 && n.nodeValue.trim())) {
        out.n.caps++;
        if (cs.textTransform === "uppercase") once(out.caps, "t|" + kind(s), { sel: s, txt: text(e, 30), tool: t });
      }
    }
    shut.forEach((d) => (d.open = false));
    H.fresh();
    st.remove();
    return out;
  },

  // A2: the page head, its eyebrow's text top on the page, any eyebrow written .kicker, its lede in characters
  pagehead(H) {
    const ph = document.querySelector("main .phead"), kicker = document.querySelectorAll(".kicker").length;
    if (!ph) return { none: true, eyebrow: null, kicker };
    const ey = ph.querySelector(".eyebrow,.kicker"), lede = ph.querySelector(".lede");
    const top = (e) => { const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.nodeValue.trim() ? 1 : 3) });
      const n = w.nextNode(), rg = document.createRange(); rg.selectNodeContents(n); return rg.getClientRects()[0].top + scrollY; };
    let ch = 0;
    if (lede) { const cs = getComputedStyle(lede), c = document.createElement("canvas").getContext("2d");
      c.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`; ch = c.measureText("0").width; }
    return { variant: ph.classList.contains("in-col") ? "in a column" : "full", eyebrow: ey ? H.r1(top(ey)) : null,
      kicker, lede: lede && ch ? H.r1(lede.getBoundingClientRect().width / ch) : null };
  },

  // A3: the breadcrumbs, how many say they are the page, and the ones a reader can see
  crumbtrail(H) {
    const nav = document.querySelector("nav.crumbs");
    if (!nav) return null;
    const lis = [...nav.querySelectorAll("li")];
    return { current: nav.querySelectorAll("[aria-current]").length, last: !!lis.length && !!lis[lis.length - 1].querySelector("[aria-current]"),
      shown: lis.filter((li) => H.isVis(li)).map((li) => ({ link: !!li.querySelector("a[href]"), cur: !!li.querySelector("[aria-current]"), txt: H.text(li, 30) })) };
  },

  // A5: every table, with every fold opened (not the top bar's lists or the drawer), against its own box
  tables(H) {
    const st = document.createElement("style");
    st.textContent = "*,*::before,*::after{transition:none!important}::details-content{transition:none!important}";
    document.head.appendChild(st);
    const shut = [...H.root.querySelectorAll("details:not([open])")].filter((d) => !d.closest(".hd") && !H.tool(d));
    shut.forEach((d) => (d.open = true));
    H.fresh();
    const out = { n: 0, over: [] };
    for (const t of H.root.querySelectorAll(".tw")) {
      if (!H.isVis(t) || t.matches(".wide")) continue;
      out.n++;
      const over = t.scrollWidth - t.clientWidth;
      if (over > 1) out.over.push({ sel: H.sel(t), over, w: H.r1(t.clientWidth), cols: t.querySelectorAll("thead th").length, txt: H.text(t.querySelector("th,td") || t, 24), tool: H.tool(t) });
    }
    shut.forEach((d) => (d.open = false));
    H.fresh();
    st.remove();
    return out;
  },

  // A6 and A15: each focusable thing focused in turn (the browser scrolls it into view, as for a Tab press), its
  // ring against every box that clips it, and a ring inside a code box against what it is drawn on
  async focus(H) {
    const { root, DE, rgba, over, cr, hex, r1, sel, kind, text, isVis, bgOf, tool } = H;
    const out = { n: 0, rings: 0, cut: [], code: [] };
    const st = document.createElement("style");
    st.textContent = "*,*::before,*::after{transition:none!important;animation-play-state:paused!important;scroll-behavior:auto!important}";
    document.head.appendChild(st);
    const FSEL = 'a[href],button,input:not([type=hidden]),select,textarea,summary,[tabindex]:not([tabindex="-1"]),iframe';
    const all = [...root.querySelectorAll(FSEL)].filter((e) => isVis(e) && !e.disabled && !e.closest("[inert]") && !e.matches(".skip"));
    const clipCache = new Map();
    const clipOf = (a) => {   // how a box clips: per axis, and its borders
      if (clipCache.has(a)) return clipCache.get(a);
      const cs = getComputedStyle(a), paint = /paint|strict|content/.test(cs.contain);
      const v = { x: paint || cs.overflowX !== "visible", y: paint || cs.overflowY !== "visible",
        b: [cs.borderTopWidth, cs.borderRightWidth, cs.borderBottomWidth, cs.borderLeftWidth].map(parseFloat) };
      clipCache.set(a, v); return v;
    };
    const sx = scrollX, sy = scrollY, seenCut = new Set();
    for (const e of all.slice(0, 900)) {
      e.focus();
      if (document.activeElement !== e) continue;
      out.n++;
      const cs = getComputedStyle(e), ow = cs.outlineStyle === "none" ? 0 : parseFloat(cs.outlineWidth);
      if (ow > 0 && e.matches(":focus-visible")) {
        out.rings++;
        const ext = ow + (parseFloat(cs.outlineOffset) || 0);
        const frags = cs.display === "inline" ? [...e.getClientRects()].filter((q) => q.width > 0 && q.height > 0) : [e.getBoundingClientRect()];
        let cut = null;
        for (let a = e.parentElement; a && a !== document.body && a !== DE && !cut; a = a.parentElement) {
          const k = clipOf(a); if (!k.x && !k.y) continue;
          const ar = a.getBoundingClientRect();
          for (const q of frags) {
            const L = k.x ? ar.left + k.b[3] - (q.left - ext) : 0, R = k.x ? q.right + ext - (ar.right - k.b[1]) : 0;
            const T = k.y ? ar.top + k.b[0] - (q.top - ext) : 0, B = k.y ? q.bottom + ext - (ar.bottom - k.b[2]) : 0;
            const m = Math.max(L, R, T, B);
            if (m > 1) { cut = { by: sel(a), cut: r1(m), sides: [L > 1 && "L", R > 1 && "R", T > 1 && "T", B > 1 && "B"].filter(Boolean).join("") }; break; }
          }
        }
        const s = sel(e);
        if (cut && !seenCut.has(kind(s))) { seenCut.add(kind(s)); out.cut.push({ sel: s, ...cut, ring: ow + "px", txt: text(e, 30), tool: tool(e) }); }
        if (e.closest(".blk,.codebox")) {   // the ring against what it lies on: the element itself when drawn inside, else what is under its edge
          const r = e.getBoundingClientRect();
          let under = e;
          if (ext > 0) { const hit = document.elementsFromPoint(r.left - ext + ow / 2, r.top + r.height / 2).find((x) => x !== e && !e.contains(x)); under = hit || e.parentElement; }
          const bg = bgOf(under).c, oc = rgba(cs.outlineColor), ratio = +cr(over(oc, bg), bg).toFixed(2);
          const was = out.code.find((f) => f.kind === kind(s));
          if (!was) out.code.push({ sel: s, kind: kind(s), ratio, outline: hex(oc), bg: hex(bg), n: 1, tool: tool(e) });
          else { was.n++; if (ratio < was.ratio) Object.assign(was, { sel: s, ratio, outline: hex(oc), bg: hex(bg) }); }
        }
      }
      e.blur();
    }
    scrollTo(sx, sy); st.remove();
    return out;
  },
};

// The source of every template and prompt: content/roles/*.json, by the ids the pages give their boxes
// (lt- and lp- on the library pages, t- and p- on a role page).
const SOURCE = (() => {
  const dir = join(dirname(fileURLToPath(import.meta.url)), "..", "content", "roles"), m = new Map();
  for (const f of readdirSync(dir).filter((f) => f.endsWith(".json"))) {
    const role = JSON.parse(readFileSync(join(dir, f), "utf8"));
    for (const s of role.steps) {
      m.set(`lt-${role.id}-${s.id}`, s.template.body); m.set(`t-${s.id}@${role.id}`, s.template.body);
      s.prompts.forEach((p, i) => { m.set(`lp-${role.id}-${s.id}-${i}`, p.body); m.set(`p-${s.id}-${i}@${role.id}`, p.body); });
    }
  }
  return m;
})();
const firstDiff = (a, b) => { let i = 0; while (i < a.length && a[i] === b[i]) i++; return i; };

// ------------------------------------------------------------------ the checks: one run's measurements in, faults out
// Each returns { n: how many things it measured, faults: [{ key, ... }] }. A fault's key names it the same way
// on every run, so one fault seen at eight widths and themes prints once. `needs` names the collectors and the
// widths; `states`, where given, the page states it runs on.
const CHECKS = [
  { id: "A6", what: "no focus ring cut by more than 1px by a box that clips it", needs: { focus: WIDTHS },
    fn: (r) => ({ n: r.focus.rings, faults: r.focus.cut.map((f) => ({ ...f, key: `${f.sel} ("${f.txt}"): ring cut ${f.cut}px (${f.sides}) by ${f.by}` })) }) },
  { id: "A13", what: "every control 44px or taller on a phone; the stepper's dots 24px apart, 24px to touch; small targets spaced", needs: { targets: [390, 320] },
    fn: (r) => ({ n: r.targets.n + r.targets.dots.length, faults: [
      ...r.targets.short.map((f) => ({ ...f, key: `${f.sel} ("${f.txt}"): ${f.h}px tall` })),
      ...r.targets.dots.filter((d) => d.apart < 23.5 || d.area < 23.5).map((d) => ({ ...d, key: `${d.sel}: dots ${d.apart}px apart, ${d.area}px to touch` })),
      ...r.targets.crowded.map((f) => ({ ...f, key: `${f.sel} ("${f.txt}"): ${f.w}x${f.h}px, within 24px of ${f.near}` }))] }) },
  { id: "A14", what: "every text 4.5:1 against its backdrop from the pixels (3:1 when large); placeholders too", needs: { contrast: WIDTHS },
    fn: (r) => ({ n: r.contrast.n + r.contrast.placeholders.length, faults: [
      ...r.contrast.groups.filter((g) => !g.dis && g.seen < g.need).map((g) => ({ ...g, key: `${g.sel} ("${g.txt}"): ${g.seen}:1${g.px ? "" : " (not found on screen)"}, needs ${g.need}` })),
      ...r.contrast.placeholders.filter((p) => p.ratio < 4.5).map((p) => ({ ...p, key: `${p.sel} ("${p.txt}"): ${p.ratio}:1, needs 4.5` }))] }) },
  { id: "A15", what: "every focus ring inside a code box 3:1 against what it is drawn on", needs: { focus: WIDTHS },
    fn: (r) => ({ n: r.focus.code.reduce((n, f) => n + f.n, 0), faults: r.focus.code.filter((f) => f.ratio < 3).map((f) => ({ ...f, key: `${f.sel}: ring ${f.outline} on ${f.bg}, ${f.ratio}:1` })) }) },
  { id: "A1", what: "no code box scrolls sideways at 1024 and 390: prompts and templates wrap", needs: { wrap: [1024, 390] },
    fn: (r) => ({ n: r.wrap.n, faults: r.wrap.over.map((f) => ({ ...f, key: `${f.sel} ("${f.txt}"): ${f.hidden}px (${f.share}%) off to the side` })) }) },
  { id: "A4", what: "the role rows start on their heading's column, and no hover rule moves their words", needs: { seats: WIDTHS }, states: /^home$/,
    fn: (r) => !r.seats ? { n: 0, faults: [{ key: "the role rows were not found" }] } : { n: 1, faults: [
      ...(Math.abs(r.seats.code - r.seats.h2) > 1 ? [{ key: `the first role code starts at ${r.seats.code}, its heading at ${r.seats.h2}` }] : []),
      ...r.seats.moves.map((s) => ({ key: `${s} changes padding on hover` })),
      ...(/padding|all/.test(r.seats.transition) ? [{ key: `a role row's transition carries ${r.seats.transition}` }] : [])] } },
  { id: "A10", what: "on a phone the top bar's menu icon and theme circle sit on the column (20px in)", needs: { header: [390, 320] },
    fn: (r) => !r.header ? { n: 0, faults: [] } : { n: 1, faults: [
      ...(Math.abs(r.header.icon - 20) > 1 ? [{ key: `the menu icon starts at ${r.header.icon}, not 20` }] : []),
      ...(Math.abs(r.header.tgl - (r.header.w - 20)) > 1 ? [{ key: `the theme circle ends at ${r.header.tgl}, not ${r.header.w - 20}` }] : [])] } },
  { id: "A11", what: "a rail's heading and the page's eyebrow share a text top at 1440 and 1024", needs: { railtop: [1440, 1024] },
    states: /^(role-pm|protocol|templates|prompts|tool-desk)$/,
    fn: (r) => !r.railtop ? { n: 0, faults: [{ key: "no rail heading or no eyebrow found" }] } : { n: 1, faults: Math.abs(r.railtop.rail - r.railtop.eyebrow) > 1
      ? [{ key: `${r.railtop.railSel} text top ${r.railtop.rail}, the eyebrow's ${r.railtop.eyebrow}` }] : [] } },
  { id: "copy", what: "Copy copies each prompt and template exactly as its source has it", needs: { copy: [390] }, states: /^(prompts|templates|role-pm)$/,
    fn: (r, state) => { const faults = [], role = state.role;
      if (!r.copy || !r.copy.length) faults.push({ key: r.copy ? "no Copy button found" : "no clipboard to watch" });
      for (const c of r.copy || []) {
        const want = SOURCE.get(c.id) ?? SOURCE.get(`${c.id}@${role}`);
        if (want === undefined) faults.push({ key: `${c.id}: no source found for it` });
        else if (c.text !== want) faults.push({ key: `${c.id}: copied text differs from its source at character ${firstDiff(c.text || "", want)}` });
      }
      return { n: (r.copy || []).length, faults }; } },
  { id: "404", what: "the 404 page: the site's eyebrow, its 3px focus ring, its list on its column", needs: { notfound: WIDTHS }, states: /^404$/,
    fn: (r) => !r.notfound ? { n: 0, faults: [{ key: "the 404 page's eyebrow was not found" }] } : { n: 1, faults: [
      ...(r.notfound.family !== "Geist Mono" || !r.notfound.loaded ? [{ key: `the eyebrow is set in ${r.notfound.family}${r.notfound.loaded ? "" : ", not loaded"}` }] : []),
      ...(!r.notfound.rule ? [{ key: "the eyebrow has no leading rule" }] : []),
      ...(r.notfound.rings.some((x) => x !== "solid 3px") ? [{ key: `focus rings: ${r.notfound.rings.join(", ")}` }] : []),
      ...(Math.abs(r.notfound.row - r.notfound.h1) > 1 ? [{ key: `a row's words start at ${r.notfound.row}, the title at ${r.notfound.h1}` }] : [])] } },
  { id: "A7", what: "every box 120 by 60px or larger has corners of 11, 16 or 20px", needs: { parts: WIDTHS },
    fn: (r) => ({ n: r.parts.n.boxes, faults: r.parts.boxes.filter((b) => b.round.some((x) => ![11, 16, 20].some((o) => Math.abs(x - o) < 0.5)))
      .map((b) => ({ ...b, key: `${b.sel}: corners ${b.corners}px` })) }) },
  { id: "A8", what: "every button and pill 36, 43 or 51px tall at 1440 and 44px or more at 390; a button's corner 11px", needs: { parts: [1440, 390] },
    fn: (r, state, width) => ({ n: r.parts.n.ctrls, faults: r.parts.ctrls.flatMap((c) => [
      ...((width === 1440 ? ![36, 43, 51].some((s) => Math.abs(c.h - s) <= 1) : c.h < 44) ? [{ ...c, key: `${c.sel} ("${c.txt}"): ${c.h}px tall` }] : []),
      ...(c.corner !== "pill" && Math.abs(c.corner - 11) > 0.5 ? [{ ...c, key: `${c.sel} ("${c.txt}"): corner ${c.corner}px` }] : [])]) }) },
  { id: "A9", what: "on inner pages every h2 27px at 620, every h3 19.5px or 18px, at 1440", needs: { parts: [1440] },
    states: /^(?!home$|search$|lesson-|sim-|workbench$|404$)/,
    fn: (r) => ({ n: r.parts.n.heads, faults: r.parts.heads.filter((h) => !h.own && (h.tag === "h2" ? Math.abs(h.fs - 27) > 0.5 || h.fw !== 620 : ![18, 19.5].some((s) => Math.abs(h.fs - s) < 0.3)))
      .map((h) => ({ ...h, key: `${h.sel} ("${h.txt}"): ${h.fs}px at ${h.fw}` })) }) },
  { id: "A12", what: "no visible text set in capitals by text-transform", needs: { parts: WIDTHS },
    fn: (r) => ({ n: r.parts.n.caps, faults: r.parts.caps.map((c) => ({ ...c, key: `${c.sel} ("${c.txt}"): text-transform uppercase` })) }) },
  { id: "A2", what: "one page head: each variant's eyebrow at one height (2px), every eyebrow .eyebrow, a lede of 56 characters or fewer",
    needs: { pagehead: [1440, 390] }, states: /^(role-pm|protocol|templates|prompts|models|frameworks|pictures|tools|tool-desk|labs|lab-grow|learn|method)$/,
    fn: (r) => r.pagehead.none ? { n: 1, faults: [{ key: "no page head (main .phead)" }] } : { n: 1, faults: [
      ...(r.pagehead.kicker ? [{ key: `${r.pagehead.kicker} eyebrow written .kicker` }] : []),
      ...(r.pagehead.eyebrow === null ? [{ key: "the head has no eyebrow" }] : []),
      ...(r.pagehead.lede > 56.5 ? [{ key: `the lede runs ${r.pagehead.lede} characters a line` }] : [])] },
    // each variant's eyebrow, at each width, against the middle of its variant's values there
    across: (rows) => {
      const by = new Map();
      for (const r of rows) if (r.rec.pagehead && r.rec.pagehead.eyebrow !== null) {
        const k = r.rec.pagehead.variant + "|" + r.width; if (!by.has(k)) by.set(k, []); by.get(k).push(r); }
      const out = [];
      for (const [k, rs] of by) {
        const v = rs.map((r) => r.rec.pagehead.eyebrow).sort((a, b) => a - b), mid = v[v.length >> 1];
        for (const r of rs) if (Math.abs(r.rec.pagehead.eyebrow - mid) > 2)
          out.push({ state: r.state.name, width: r.width, theme: r.theme, key: `the eyebrow's text top is ${r.rec.pagehead.eyebrow}px; the ${k.split("|")[0]} head's is ${mid}px` });
      }
      return out; } },
  { id: "A3", what: "one crumb is the page, the last; on a phone the crumb shown leads back", needs: { crumbtrail: [1440, 390, 320] },
    fn: (r, state, width) => !r.crumbtrail ? { n: 0, faults: [] } : { n: 1, faults: [
      ...(r.crumbtrail.current !== 1 || !r.crumbtrail.last ? [{ key: `${r.crumbtrail.current} crumbs say they are the page${r.crumbtrail.last ? "" : ", and the last does not"}` }] : []),
      ...(width < 600 ? r.crumbtrail.shown.filter((c) => !c.cur && !c.link).map((c) => ({ key: `on a phone the crumb "${c.txt}" is not a link` })) : []),
      ...(width < 600 && !r.crumbtrail.shown.some((c) => c.link) ? [{ key: "on a phone no crumb leads back" }] : [])] } },
  { id: "A5", what: "at 390 and 320 no table scrolls sideways, every fold opened, unless marked .wide", needs: { tables: [390, 320] },
    fn: (r) => ({ n: r.tables.n, faults: r.tables.over.map((t) => ({ ...t, key: `${t.sel} ("${t.txt}", ${t.cols} columns): ${t.over}px past its ${t.w}px box` })) }) },
].filter((c) => !PICK || PICK.test(c.id));

// ------------------------------------------------------------------ the browser: one Chrome, a tab per worker
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333 + Math.floor(Math.random() * 400);
const profile = join(tmpdir(), `ui-${PORT}`);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--no-first-run",
  "--no-default-browser-check", "--hide-scrollbars", "--disable-background-timer-throttling", "--disable-renderer-backgrounding",
  "--disable-backgrounding-occluded-windows", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function browserUrl() {
  for (let i = 0; i < 80; i++) {
    try { return (await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json()).webSocketDebuggerUrl; } catch {}
    await sleep(250);
  }
  throw new Error("Chrome did not start");
}
const ws = new WebSocket(await browserUrl());
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0;
const waiting = new Map(), tabs = new Map();
ws.addEventListener("message", (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id) { const w = waiting.get(m.id); if (w) { waiting.delete(m.id); m.error ? w.no(new Error(m.error.message)) : w.ok(m.result); } return; }
  const tab = m.sessionId && tabs.get(m.sessionId); if (tab) tab.on(m.method, m.params);
});
const send = (method, params = {}, sessionId) => new Promise((ok, no) => {
  const id = ++seq; waiting.set(id, { ok, no });
  ws.send(JSON.stringify(sessionId ? { id, method, params, sessionId } : { id, method, params }));
});

// a tab in a browser context of its own, so its storage (the theme the reader chose) is its own
async function openTab() {
  const { browserContextId } = await send("Target.createBrowserContext");
  const { targetId } = await send("Target.createTarget", { url: "about:blank", browserContextId });
  const { sessionId } = await send("Target.attachToTarget", { targetId, flatten: true });
  const tab = { thrown: [], loaded: null, script: null };
  tab.send = (m, p) => send(m, p, sessionId);
  tab.on = (method, p) => {
    if (method === "Page.loadEventFired" && tab.loaded) { tab.loaded(); tab.loaded = null; }
    else if (method === "Runtime.exceptionThrown") tab.thrown.push((p.exceptionDetails.exception?.description || p.exceptionDetails.text || "").split("\n")[0].slice(0, 140));
    else if (method === "Fetch.requestPaused") {
      const u = new URL(p.request.url), whole = u.pathname.startsWith(WHOLE);
      tab.send("Fetch.continueRequest", whole ? { requestId: p.requestId, url: BASE + u.pathname.slice(WHOLE.length) + u.search } : { requestId: p.requestId }).catch(() => {});
    }
  };
  tabs.set(sessionId, tab);
  tab.evaluate = async (expression) => {
    const r = await tab.send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error((r.exceptionDetails.exception?.description || r.exceptionDetails.text || "").split("\n")[0]);
    return r.result.value;
  };
  await tab.send("Page.enable"); await tab.send("Runtime.enable");
  await tab.send("Emulation.setFocusEmulationEnabled", { enabled: true });     // a tab behind another still has focus
  if (!new URL(BASE).pathname.startsWith(WHOLE)) await tab.send("Fetch.enable", { patterns: [{ urlPattern: "*" + WHOLE + "*" }] });
  return tab;
}

// ------------------------------------------------------------------ one run: a state at a width in a theme
const SCROLL_THROUGH = `(async () => { await document.fonts.ready; const H = innerHeight;
  for (let y = 0; y < document.documentElement.scrollHeight; y += H) { scrollTo({ top: y, behavior: "instant" });
    await new Promise((r) => requestAnimationFrame(() => setTimeout(r, 50))); }
  scrollTo({ top: 0, behavior: "instant" }); await new Promise((r) => setTimeout(r, 400)); return true; })()`;
const page = (names, root) => `(async () => { await document.fonts.ready; const H = (${HELPERS})(${JSON.stringify({ root })}); const R = {};
  ${names.map((n) => `R[${JSON.stringify(n)}] = await (${COLLECTORS[n].toString().replace(/^(async\s+)?(\w+)\s*\(/, "$1function (")})(H);`).join("\n")}
  return R; })()`;

async function run(tab, job) {
  const { state, width, theme } = job, t0 = Date.now();
  const names = Object.keys(COLLECTORS).filter((n) => CHECKS.some((c) => c.needs[n] && c.needs[n].includes(width) && (!c.states || c.states.test(state.name))));
  tab.thrown.length = 0;
  await tab.send("Emulation.setDeviceMetricsOverride", { width, height: width < 600 ? 844 : 900, deviceScaleFactor: 1, mobile: width < 600 });
  await tab.send("Emulation.setTouchEmulationEnabled", width < 600 ? { enabled: true, maxTouchPoints: 5 } : { enabled: false });
  await tab.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: theme }, { name: "prefers-reduced-motion", value: "no-preference" }] });
  // the theme the reader chose, and nothing else left from an earlier run
  if (tab.script) await tab.send("Page.removeScriptToEvaluateOnNewDocument", { identifier: tab.script });
  tab.script = (await tab.send("Page.addScriptToEvaluateOnNewDocument", {
    source: `try{localStorage.clear();sessionStorage.clear();localStorage.setItem('manual-theme','${theme}')}catch(e){}` })).identifier;
  let done = new Promise((r) => (tab.loaded = r));
  await tab.send("Page.navigate", { url: "about:blank" }); await Promise.race([done, sleep(2000)]);
  done = new Promise((r) => (tab.loaded = r));
  await tab.send("Page.navigate", { url: new URL(state.path, BASE).href });
  await Promise.race([done, sleep(15000)]);
  await sleep(state.wait || 900);
  await tab.evaluate(SCROLL_THROUGH);
  // one Tab press, so focus behaves as it does for a keyboard user
  for (const type of ["keyDown", "keyUp"]) await tab.send("Input.dispatchKeyEvent", { type, key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 });
  await sleep(60);
  if (state.before) { await tab.evaluate(state.before); await sleep(300); }
  const rec = await tab.evaluate(page(names, state.root));
  if (rec.contrast) await pixels(tab, rec.contrast);
  rec.ms = Date.now() - t0; rec.thrown = tab.thrown.slice(0, 3);
  return rec;
}

// The stylesheet's colours cannot see a gradient, a picture or a part laid over another. Up to two of each kind of
// candidate (selector, colour, size) are shot from the screen, and the lowest ratio the pixels give is kept.
async function pixels(tab, c) {
  const groups = new Map();
  for (const f of c.cands) {
    const k = [f.sel, f.fg, f.fs, f.need].join("|"), g = groups.get(k);
    if (!g) groups.set(k, { ...f, tis: [f.ti], count: 1 }); else { g.count++; if (g.tis.length < 2) g.tis.push(f.ti); }
  }
  c.groups = [];
  for (const g of [...groups.values()].slice(0, 60)) {
    let px = null;
    for (const ti of g.tis) {
      const clip = await tab.evaluate(`window.__uiBox(${ti})`);
      if (!clip) continue;
      const shoot = async () => (await tab.send("Page.captureScreenshot", { format: "png", clip: { ...clip, scale: 1 } })).data;
      const a = await shoot();
      await tab.evaluate(`window.__uiHide(${ti}, true)`);
      const b = await shoot();
      await tab.evaluate(`window.__uiHide(${ti}, false)`);
      if (!a || !b) continue;
      const p = await tab.evaluate(`window.__uiPx(${JSON.stringify(a)}, ${JSON.stringify(b)}, "${g.fg}", ${g.fgA})`);
      if (p.ink < 1.25) continue;                                     // no ink in the shot: the line was not there to see
      if (!px || p.ratio < px.ratio) px = p;
    }
    // the pixels decide; where the line could not be found on screen, the stylesheet's figure stands
    c.groups.push({ sel: g.sel, txt: g.txt, fs: g.fs, need: g.need, css: g.css, fg: g.fg, dis: g.dis, tool: g.tool, count: g.count, px, seen: px ? px.ratio : g.css });
  }
  delete c.cands;
}

// ------------------------------------------------------------------ all runs, then the report
const known = (check, f) => KNOWN.find((k) => (k.check === "*" || k.check === check) && k.state.test(f.state) &&
  (!k.match || k.match.test(f.key)) && (k.tool === undefined || !!f.tool === k.tool));
const states = STATES.filter((s) => !ONLY || ONLY.test(s.name));
const HEAVY = /templates|prompts|pictures|home|search|workbench|protocol/;          // started first, so the tabs end together
const jobs = states.flatMap((state) => WIDTHS.flatMap((width) => THEMES.map((theme) => ({ state, width, theme }))))
  .sort((a, b) => HEAVY.test(b.state.name) - HEAVY.test(a.state.name));
const results = [];
const t0 = Date.now();
let failed = 0;
try {
  const pool = await Promise.all(Array.from({ length: Math.min(TABS, jobs.length) }, openTab));
  let next = 0;
  await Promise.all(pool.map(async (tab) => {
    while (next < jobs.length) {
      const job = jobs[next++];
      let rec;
      try { rec = await run(tab, job); } catch (e) { rec = { error: String(e.message || e).slice(0, 200) }; }
      results.push({ ...job, rec });
      if (process.env.UI_VERBOSE) console.log(`  ${job.state.name} ${job.width} ${job.theme} ${rec.error ? "ERROR " + rec.error : rec.ms + "ms"}`);
    }
  }));

  const used = new Set();
  const label = (r) => `${r.state.name} ${r.width} ${r.theme}`;
  console.log(`ui.test: ${states.length} states x ${WIDTHS.length} widths x ${THEMES.length} themes = ${jobs.length} runs, ${TABS} tabs`);
  const broken = results.filter((r) => r.rec.error);
  for (const c of CHECKS) {
    const groups = new Map(), held = new Map();
    let n = 0;
    const applied = [];
    for (const r of results) {
      if (r.rec.error || !Object.entries(c.needs).every(([k, ws]) => !ws.includes(r.width) || r.rec[k])) continue;
      if (!Object.entries(c.needs).some(([, ws]) => ws.includes(r.width)) || (c.states && !c.states.test(r.state.name))) continue;
      const out = c.fn(r.rec, r.state, r.width);
      applied.push(r);
      n += out.n;
      for (const f of out.faults) {
        const k = known(c.id, { ...f, state: r.state.name });
        const into = k ? held : groups, key = (k ? `[${k.owner}] ` : "") + `${r.state.name}: ${f.key}`;
        if (k) used.add(k);
        if (!into.has(key)) into.set(key, []);
        into.get(key).push(`${r.width} ${r.theme}`);
      }
    }
    for (const f of c.across ? c.across(applied) : []) {
      const k = known(c.id, f), into = k ? held : groups, key = (k ? `[${k.owner}] ` : "") + `${f.state}: ${f.key}`;
      if (k) used.add(k);
      if (!into.has(key)) into.set(key, []);
      into.get(key).push(`${f.width} ${f.theme}`);
    }
    const bad = groups.size + (broken.length ? 1 : 0);
    if (bad) failed++;
    console.log(`${c.id.padEnd(4)} ${bad ? "FAIL" : "ok  "}  ${c.what} (${n} measured${held.size ? `; ${held.size} known, owned elsewhere` : ""})`);
    for (const [k, where] of groups) console.log(`       ${k}  [${where.join(", ")}]`);
    for (const [k, where] of held) console.log(`       known ${k}  [${where.length} runs]`);
  }
  for (const r of broken) console.log(`       could not measure ${label(r)}: ${r.rec.error}`);
  const thrown = [...new Set(results.flatMap((r) => (r.rec.thrown || []).map((t) => `${r.state.name}: ${t}`)))];
  for (const t of thrown) console.log(`       script error on ${t}`);
  if (!ONLY) for (const k of KNOWN) if (!used.has(k) && (k.check === "*" || CHECKS.some((c) => c.id === k.check)))
    console.log(`       KNOWN no longer matches anything, remove it: ${k.owner}: ${k.why}`);
} catch (e) {
  failed++;
  console.log(`ui.test could not run: ${e.message}`);
} finally {
  ws.close(); chrome.kill();
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
const secs = Math.round((Date.now() - t0) / 1000);
console.log(failed ? `ui.test: ${failed} of ${CHECKS.length} checks failed (${results.length} runs in ${Math.floor(secs / 60)}m${String(secs % 60).padStart(2, "0")}s)`
  : `ui.test: all ${CHECKS.length} checks hold over ${results.length} runs (${Math.floor(secs / 60)}m${String(secs % 60).padStart(2, "0")}s)`);
process.exit(failed ? 1 : 0);
