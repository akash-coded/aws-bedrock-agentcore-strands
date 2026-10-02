/* The home page's picture: one canvas, one clock (DESIGN.md, Motion). A flight round the Earth through the four
   phases, staged like a launch, that comes to rest in one named still: the rest frame, all that reduced motion draws.
   In no frame: shadowBlur, ctx.filter, a new gradient, getImageData, text set or measured. At most 60 frames a
   second. For the gate: GlobeTimes, GlobeState, GlobeAt(seconds), GlobeMs. */
(function () {
  "use strict";
  var cv = document.querySelector("[data-globe]"), src = document.getElementById("globe-land"), data;
  if (!cv || !src || !cv.getContext) return;
  try { data = JSON.parse(src.textContent); } catch (e) { return; }
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ctx = cv.getContext("2d"), RAD = Math.PI / 180, TAU = Math.PI * 2, n = 0, at = 0, i, j;

  data.rows.forEach(function (row) { for (i = 1; i < row[1].length; i += 2) n += row[1][i]; });
  var sLat = new Float32Array(n), cLat = new Float32Array(n), sLon = new Float32Array(n), cLon = new Float32Array(n);
  data.rows.forEach(function (row, r) {
    var lat = (data.lat0 + r * data.step) * RAD, runs = row[1], lon;
    for (i = 0; i < runs.length; i += 2) for (j = 0; j < runs[i + 1]; j++, at++) {
      lon = (-180 + (runs[i] + j + 0.5) * 360 / row[0]) * RAD;
      sLat[at] = Math.sin(lat); cLat[at] = Math.cos(lat); sLon[at] = Math.sin(lon); cLon[at] = Math.cos(lon);
    }
  });

  var sT = Math.sin(20 * RAD), cT = Math.cos(20 * RAD), LX = -0.46, LY = 0.56, LZ = 0.69;
  var RHO = 1.3, PITCH = 0.17;
  var sA = Math.sin(15 * RAD), cA = Math.cos(15 * RAD), sR = Math.sin(14 * RAD), cR = Math.cos(14 * RAD);
  var SPIN = 75, PAST = 2.3, AHEAD = 0.6, HOME = 58 * RAD;
  var GATE = 0.25, MID = [0.0625, 0.1875, 0.3125, 0.4375];

  function smooth(x) { return x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x); }
  function ramp(f, a, b) { return smooth((f - a) / (b - a)); }
  function clamp(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }

  // a lap: 5 s a phase in front of the Earth, all but stopped on the bar, quick behind
  var N = 8192, FRAC = new Float32Array(1025), TIME = new Float32Array(1025), LAP;
  (function () {
    var tt = new Float64Array(N + 1), s = 0, a, b = 0, f, w, g, want;
    for (a = 0; a < N; a++) {
      tt[a] = s; f = (a + 0.5) / N; g = Math.abs(f - GATE) / 0.011;
      w = f < 0.5 ? 0 : f < 0.57 ? smooth((f - 0.5) / 0.07) : f < 0.93 ? 1 : 1 - smooth((f - 0.93) / 0.07);
      s += 1 / (1 + w * 3.4) / (1 - 0.94 * (g < 1 ? smooth(1 - g) : 0));
    }
    tt[N] = s; LAP = s * 40 / N;
    for (a = 0; a <= 1024; a++) {
      want = a / 1024 * s;
      while (b < N - 1 && tt[b + 1] < want) b++;
      FRAC[a] = (b + (want - tt[b]) / (tt[b + 1] - tt[b] || 1)) / N;
      TIME[a] = tt[a * 8] / s;
    }
    FRAC[1024] = 1;
  })();
  function look(T, x) { var w = Math.floor(x), f = (x - w) * 1024, a = f | 0; return w + T[a] + (T[Math.min(1024, a + 1)] - T[a]) * (f - a); }
  function along(laps) { return look(FRAC, laps); }
  function when(turns) { return look(TIME, turns) * LAP; }
  var T_P1 = when(0.125), T_GATE = when(GATE), T_P3 = when(0.375), T_BACK = when(0.5), LEFT = [T_P1, T_GATE + 0.05, T_P3];

  function whole(h) { var p = h.slice(), m; for (m = h.length - 2; m >= 1; m--) p.push([h[m][0], -h[m][1]]); return p; }
  var DART = whole([[16, 0], [5, -2.3], [-12.2, -10.8], [-13.8, -9.4], [-7.8, -2.6], [-11, -2.1], [-13.4, -1.5], [-11.8, 0]]);
  var LINER = whole([[15.5, 0], [3.5, -2.7], [-5.5, -14], [-9.5, -14], [-3.5, -2.7], [-10.5, -2.3], [-15.5, -7.2], [-13.5, 0]]);
  var JET = whole([[18, 0], [4, -2.3], [-9.5, -10.5], [-13, -10.5], [-8.5, -3.1], [-11.5, -2.7], [-16.5, -6.2], [-12.5, 0]]);

  var TAG = [["P0", "Frame", "An idea.", " Is it worth building at all?"],
    ["P1", "Design & Spec", "A drawing.", " What exactly, and who signs?"],
    ["P2", "Build & Prove", "Built.", " Does it meet the bar?"],
    ["P3", "Run & Learn", "Live.", " Is it working, and what did it cost?"],
    ["", "Sign-off", "", "Nothing is built until it is signed."],
    ["", "Back to Frame", "", "One level up, with what it learned."]];

  var C = {}, tone = [], SPR = {};
  function hex(v) { var m = /^#([0-9a-f]{6})$/i.exec((v || "").trim()), h = m ? m[1] : "8B8B8B"; return [0, 2, 4].map(function (k) { return parseInt(h.slice(k, k + 2), 16); }); }
  function rgba(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")"; }
  function mix(a, b, t) { return [0, 1, 2].map(function (k) { return Math.round(a[k] + (b[k] - a[k]) * t); }); }
  function colours() {
    var cs = getComputedStyle(cv), g = function (name) { return hex(cs.getPropertyValue("--" + name)); };
    var keep = parseFloat(cs.getPropertyValue("--dg-text")) / 100 || 1;
    C.dot = g("g-dot"); C.lit = g("g-lit"); C.a = g("g-a"); C.m = g("g-m"); C.b = g("g-b"); C.air = g("g-air");
    C.leg = [g("dg-slate"), g("dg-indigo"), g("dg-teal"), g("dg-amber")]; C.gate = g("dg-rose");
    C.ink = g("ink"); C.ink2 = g("ink2"); C.soft = g("soft"); C.bone = g("bone"); C.rule = g("rule");
    C.dark = C.bone[0] + C.bone[1] + C.bone[2] < 384;
    C.word = C.leg.map(function (h) { return mix(C.ink, h, keep); }); C.gword = mix(C.ink, C.gate, keep);
    for (var b = 0; b < 6; b++) tone[b] = rgba(mix(C.dot, C.lit, Math.pow(b / 5, 1.35)), 1);
    body = null; SPR = {};
  }

  var W = 0, H = 0, dpr = 1, cx = 0, cy = 0, R = 0, px = 1, cx0, cy0, R0, cam = 1, body = null, glow, edge, small, LH, FONT = {}, PZ = null, PB = null;
  function bx(x, y, w, h) { return { x: x, y: y, w: w, h: h }; }
  function grow(b, g) { return bx(b.x - g, b.y - g, b.w + 2 * g, b.h + 2 * g); }
  function hits(a, b) { return b && a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y; }
  function css(b) { var x = Math.round(b.x / dpr), y = Math.round(b.y / dpr); return [x, y, Math.round((b.x + b.w) / dpr) - x, Math.round((b.y + b.h) / dpr) - y]; }
  function fit() {
    var w = cv.clientWidth, h = cv.clientHeight, s, p, r, c;
    if (!w || !h) return false;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    if (w * dpr > 1500) dpr = 1500 / w;
    var nw = Math.round(w * dpr), nh = Math.round(h * dpr);
    if (nw !== W || nh !== H) { W = cv.width = nw; H = cv.height = nh; body = null; SPR = {}; }
    R0 = Math.min(W / 2.92, H / 2.46); cx0 = W / 2; cy0 = H / 2;
    small = w < 400;
    s = (w > 520 ? 1 : 0.93) * dpr; LH = 18 * s;
    FONT.k = "600 " + 12 * s + "px 'Geist Mono',monospace"; FONT.n = "600 " + 14 * s + "px Geist,sans-serif"; FONT.q = "400 " + 13 * s + "px Geist,sans-serif";
    p = document.querySelector(".hero2 .mpause"); PZ = PB = null;
    if (p && p.offsetParent) {
      r = p.getBoundingClientRect(); c = cv.getBoundingClientRect(); p = bx((r.left - c.left) * dpr, (r.top - c.top) * dpr, r.width * dpr, r.height * dpr);
      PZ = css(p); PB = grow(p, 6 * dpr);
    }
    return true;
  }
  function camera(t) {
    var e = smooth((t - 0.6) / (CAM_END - 0.6)), k = 1.55 - 0.55 * e, fx = cx0 - 0.97 * R0, fy = cy0 + 0.242 * R0;
    R = R0 * k; cam = k;
    cx = 0.3 * W + (fx - 0.3 * W) * e + k * (cx0 - fx); cy = 0.6 * H + (fy - 0.6 * H) * e + k * (cy0 - fy);
  }
  function layer() { var c = document.createElement("canvas"); c.width = W; c.height = H; return c; }
  function paintBody() {
    glow = layer(); body = layer(); edge = layer();
    var g = glow.getContext("2d"), b = body.getContext("2d"), e = edge.getContext("2d"), gr, r = R0, x = cx0, y = cy0;
    gr = g.createRadialGradient(x, y, r * 0.92, x, y, Math.min(x, y) * 0.99);
    gr.addColorStop(0, rgba(C.air, C.dark ? 0.36 : 0.28)); gr.addColorStop(0.3, rgba(C.air, C.dark ? 0.15 : 0.12));
    gr.addColorStop(0.7, rgba(C.air, 0.03)); gr.addColorStop(1, rgba(C.air, 0));
    g.fillStyle = gr; g.fillRect(0, 0, W, H);
    b.beginPath(); b.arc(x, y, r, 0, TAU); b.clip();
    gr = b.createRadialGradient(x - r * 0.4, y - r * 0.44, 0, x - r * 0.4, y - r * 0.44, r * 1.72);
    gr.addColorStop(0, rgba(C.a, 1)); gr.addColorStop(0.46, rgba(C.m, 1)); gr.addColorStop(0.86, rgba(C.b, 1));
    b.fillStyle = gr; b.fillRect(x - r, y - r, r * 2, r * 2);
    gr = b.createRadialGradient(x, y, r * 0.86, x, y, r);
    gr.addColorStop(0, rgba(C.air, 0)); gr.addColorStop(1, rgba(C.air, C.dark ? 0.34 : 0.3));
    b.fillStyle = gr; b.fillRect(x - r, y - r, r * 2, r * 2);
    // close up, the stage's edges fade out rather than cut the Earth
    [[W, 0], [0, H]].forEach(function (v) {
      gr = e.createLinearGradient(0, 0, v[0], v[1]);
      gr.addColorStop(0, "#000"); gr.addColorStop(0.14, "#0000"); gr.addColorStop(0.86, "#0000"); gr.addColorStop(1, "#000");
      e.fillStyle = gr; e.fillRect(0, 0, W, H);
    });
  }
  function blit(img) { ctx.drawImage(img, cx - cam * cx0, cy - cam * cy0, W * cam, H * cam); }

  var P = [0, 0, 0];
  function spot(u, up) {
    var ph = u * TAU, X = -RHO * Math.cos(ph), Z = RHO * Math.sin(ph), Y = PITCH * (u - up), y1 = Y * cA - Z * sA;
    P[0] = cx + R * (X * cR - y1 * sR); P[1] = cy - R * (X * sR + y1 * cR); P[2] = Y * sA + Z * cA;
  }
  function legOf(u) { var f = u - Math.floor(u); return f < 0.5 ? (f * 8) | 0 : 4; }
  function live(u, up) {
    var k = Math.floor(u) - Math.floor(up), f = up - Math.floor(up), t = f < 0.5 ? 0 : smooth((f - 0.5) / 0.5);
    return k === 0 ? 1 - t : k === 1 ? t : 0;
  }
  function hue(leg, w) { return leg === 4 || w <= 0 ? C.soft : w >= 1 ? C.leg[leg] : mix(C.soft, C.leg[leg], w); }
  function fade(d) {
    if (d <= 0) { var p = -d; return p < 0.55 ? 1 - p * 0.55 : p < 1.3 ? 0.7 - (p - 0.55) / 0.75 * 0.42 : 0.28 * Math.max(0, 1 - (p - 1.3) / (PAST - 1.3)); }
    return 0.62 * Math.pow(Math.max(0, 1 - d / AHEAD), 0.8);
  }
  var STEP = 1 / 120;
  function track(up, front, cut) {
    var u, m, leg, a, w, d, rl = -1, ra = -1, rw = -1, rd = -1, open = false, x0 = 0, y0 = 0, z0 = 0, has = false;
    var u0 = Math.ceil((up - PAST) / STEP) * STEP; if (launch && u0 < 0.03) u0 = 0.03;
    ctx.lineCap = "butt"; ctx.lineJoin = "round";
    for (u = u0; u <= up + AHEAD + 1e-6; u += STEP) {
      spot(u, up);
      if (has) {
        m = u - STEP / 2; leg = legOf(m); d = m > cut ? 1 : 0;
        a = ((P[2] + z0) / 2 >= 0) === front ? Math.round(fade(m - up) * (front ? 1 : 0.62) * 24) / 24 : 0;
        w = leg === 4 ? 0 : Math.round(live(m, up) * 8) / 8;
        if (a > 0 && (leg !== rl || a !== ra || w !== rw || d !== rd)) {
          if (open) ctx.stroke();
          ctx.setLineDash(d ? [5 * px, 5 * px] : []);
          ctx.beginPath(); ctx.moveTo(x0, y0); open = true; rl = leg; ra = a; rw = w; rd = d;
          ctx.strokeStyle = rgba(hue(leg, w), a * (0.75 + 0.25 * w));
          ctx.lineWidth = (1.3 + 0.7 * w) * px;
        }
        if (a > 0) ctx.lineTo(P[0], P[1]);
        else { if (open) ctx.stroke(); open = false; rl = -1; }
      }
      x0 = P[0]; y0 = P[1]; z0 = P[2]; has = true;
    }
    if (open) ctx.stroke();
    ctx.setLineDash([]);
  }
  function comet(up, near) {
    var a, u, t, x0, y0;
    spot(up, up); x0 = P[0]; y0 = P[1];
    ctx.lineCap = "butt";
    for (a = 1; a <= 36; a++) {
      u = up - 0.12 * a / 36; if (launch && u < 0.03) break;
      t = 1 - (a - 0.5) / 36;
      spot(u, up);
      ctx.strokeStyle = rgba(hue(legOf(u + 0.0017), live(u, up)), (0.25 + 0.75 * t) * (near ? 1 : 0.6));
      ctx.lineWidth = (2 + 2.6 * t * t) * px;
      ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(P[0], P[1]); ctx.stroke();
      x0 = P[0]; y0 = P[1];
    }
  }
  function tick(u, up, tl) {
    spot(u, up); var x = P[0], y = P[1], hit = 0, ring = -1, d;
    if (P[2] < 0) return;
    spot(u + 0.004, up); var dx = P[0] - x, dy = P[1] - y, l = Math.sqrt(dx * dx + dy * dy) || 1;
    if (Math.floor(u) === Math.floor(up) && tl >= 0) {
      d = tl - T_GATE;
      hit = d > -0.25 && d < 1.2 ? Math.sin(clamp((d + 0.25) / 1.45) * Math.PI) : 0;
      ring = d >= 0 && d < 0.9 ? d / 0.9 : -1;
    }
    var a = Math.min(1, fade(u - up) * 1.6) * (0.65 + 0.35 * hit) * live(u, up), len = (17 + 7 * hit) * px;
    if (a <= 0.02) return;
    ctx.strokeStyle = rgba(C.gate, a); ctx.lineWidth = 2.8 * px; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(x - dy / l * len, y + dx / l * len); ctx.lineTo(x + dy / l * len, y - dx / l * len); ctx.stroke();
    if (ring >= 0) {
      ctx.strokeStyle = rgba(C.gate, 0.85 * (1 - ring)); ctx.lineWidth = (2.2 - 1.2 * ring) * px;
      ctx.beginPath(); ctx.arc(x, y, (8 + 46 * (1 - Math.pow(1 - ring, 3))) * px, 0, TAU); ctx.stroke();
    }
  }

  var FORM = { shape: [] };
  for (i = 0; i < 14; i++) FORM.shape.push([0, 0]);
  // dart, drawing (dashed, on blueprint), built airliner, jet, in the phase's hue; solid once signed
  function form(f, tl) {
    var toLiner = ramp(f, 0.118, 0.14), toJet = ramp(f, 0.368, 0.39), toDart = ramp(f, 0.66, 0.84), m, ax, ay, c;
    var built = f > 0.5 ? 1 : tl < 0 ? (f > GATE ? 1 : 0) : ramp(tl, T_GATE + 0.05, T_GATE + 0.45);
    for (m = 0; m < 14; m++) {
      ax = DART[m][0] + (LINER[m][0] - DART[m][0]) * toLiner; ay = DART[m][1] + (LINER[m][1] - DART[m][1]) * toLiner;
      ax += (JET[m][0] - ax) * toJet; ay += (JET[m][1] - ay) * toJet;
      FORM.shape[m][0] = ax + (DART[m][0] - ax) * toDart; FORM.shape[m][1] = ay + (DART[m][1] - ay) * toDart;
    }
    FORM.solid = built * (1 - toDart);
    FORM.dash = toLiner * (1 - built);
    FORM.fold = 1 - toLiner + (f > 0.5 ? toDart : 0);
    FORM.trail = f < 0.5 ? toJet : 0;
    c = mix(C.leg[0], C.leg[1], toLiner); c = mix(c, C.leg[2], f > 0.5 ? 0 : built); c = mix(c, C.leg[3], toJet);
    FORM.col = mix(c, C.leg[0], toDart);
    return FORM;
  }
  function size(z) { return Math.max(px * 1.8, 1.2 * dpr) * (1 + 0.12 * z / RHO); }
  function plane(u, up, k, fm, a, trace) {
    spot(u + 0.003, up); var m, x = P[0], y = P[1];
    spot(u, up);
    var ang = Math.atan2(y - P[1], x - P[0]), s = size(P[2]) * k, sh = fm.shape, co = Math.cos(ang) * s, si = Math.sin(ang) * s, X, Y, l0 = 0, l1 = 0, col = fm.col, edge = mix(col, C.ink, 0.18), z = P[2], b;
    x = P[0]; y = P[1]; b = [x, y, x, y];
    if (z < 0) a *= 0.7;
    for (m = 0; m < 14; m++) {
      X = x + sh[m][0] * co - sh[m][1] * si; Y = y + sh[m][0] * si + sh[m][1] * co;
      b[0] = Math.min(b[0], X); b[1] = Math.min(b[1], Y); b[2] = Math.max(b[2], X); b[3] = Math.max(b[3], Y);
      l0 = Math.min(l0, sh[m][0]); l1 = Math.max(l1, sh[m][0]);
    }
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s);
    ctx.beginPath();
    for (m = 0; m < 14; m++) ctx.lineTo(sh[m][0], sh[m][1]);
    ctx.closePath();
    if (!trace) {
      ctx.fillStyle = rgba(mix(C.bone, col, 0.3 * fm.dash), a * 0.92); ctx.fill();
      if (fm.solid > 0) { ctx.fillStyle = rgba(col, a * fm.solid); ctx.fill(); }
    }
    ctx.lineJoin = "round"; ctx.lineWidth = (trace ? 1 : 1.6) * dpr / s; ctx.strokeStyle = rgba(edge, a);
    if (fm.dash > 0.5) ctx.setLineDash([2.4, 2]);
    ctx.stroke(); ctx.setLineDash([]);
    if (!trace && fm.fold > 0.02) {
      ctx.strokeStyle = rgba(edge, a * Math.min(1, fm.fold)); ctx.lineWidth = 1.1 * dpr / s;
      ctx.beginPath(); ctx.moveTo(15, 0); ctx.lineTo(-11.5, 0); ctx.stroke();
    }
    if (!trace && fm.trail > 0.02) {
      ctx.lineCap = "round"; ctx.lineWidth = 1.7 * dpr / s;
      for (m = 0; m < 8; m++) {
        ctx.strokeStyle = rgba(C.ink, a * fm.trail * 0.8 * (1 - m / 8));
        ctx.beginPath(); ctx.moveTo(-13 - m * 7, 3.6); ctx.lineTo(-20 - m * 7, 3.6); ctx.moveTo(-13 - m * 7, -3.6); ctx.lineTo(-20 - m * 7, -3.6); ctx.stroke();
      }
    }
    ctx.restore();
    b = bx(b[0], b[1], b[2] - b[0], b[3] - b[1]); b.len = (l1 - l0) * s; b.cx = x; b.cy = y; b.z = z;
    return b;
  }
  function pulse(tl, t0) { var d = (tl - t0) / 0.42; return d > 0 && d < 1 ? 0.2 * Math.sin(d * Math.PI) * (1 - d * 0.4) : 0; }
  var CR = bx(0, 0, 0, 0);
  function craft(up, tl) {
    var born = launch && up < 1 ? clamp(clock / 0.5) : 1, pop = tl < 0 ? 0 : pulse(tl, T_P1 - 0.05) + pulse(tl, T_GATE + 0.05) + pulse(tl, T_P3 - 0.05);
    if (born < 1) pop += 0.12 * Math.sin(born * Math.PI) - 0.5 * (1 - born);
    CR = plane(up, up, 1 + pop, form(up - Math.floor(up), tl), clamp(born * 1.6));
  }
  function exposures(up, tl, full, out) {
    var lap = Math.floor(up), f = up - lap, q, a;
    for (q = 0; q < 3; q++) {
      a = (tl < 0 ? (f > MID[q] ? 0.5 : 0) : clamp((tl - LEFT[q]) / 0.5) * 0.5) * (1 - ramp(f, 0.5, 0.62));
      a += (1 - a) * full;
      spot(lap + MID[q], up);
      if (a > 0.01 && P[2] >= 0) out.push(plane(lap + MID[q], up, 1, form(MID[q], -1), a, full < 0.5));
    }
  }

  function sprite(id, l1, l2) {
    if (SPR[id]) return SPR[id];
    var c = document.createElement("canvas"), g = c.getContext("2d"), pad = (l2 ? 10 : 8) * dpr, lw = Math.max(1, Math.round(dpr));
    function line(l, y) {
      for (var x = pad, r = 0; l && r < l.length; r += 3) {
        if (!l[r]) continue;
        g.font = FONT[l[r + 1]];
        if (y) { g.fillStyle = rgba(l[r + 2], 1); g.fillText(l[r], x, y); }
        x += g.measureText(l[r]).width;
      }
      return x + pad;
    }
    var w = Math.ceil(Math.max(line(l1), line(l2))), h = Math.round(l2 ? 2 * LH + 9 * dpr : LH + 8 * dpr);
    c.width = w; c.height = h;
    g.beginPath(); if (g.roundRect) g.roundRect(lw / 2, lw / 2, w - lw, h - lw, 8 * dpr); else g.rect(lw / 2, lw / 2, w - lw, h - lw);
    g.fillStyle = rgba(C.bone, 0.9); g.fill(); g.lineWidth = lw; g.strokeStyle = rgba(C.rule, 1); g.stroke();
    line(l1, l2 ? LH + dpr : LH - 0.5 * dpr); line(l2, 2 * LH + dpr);
    return (SPR[id] = { c: c, w: w, h: h });
  }
  function place(xy, w, h, way, keep) {
    var m = 8 * dpr, k, b;
    for (k = 0; k < xy.length; k += 2) {
      b = bx(Math.round(Math.max(m, Math.min(W - m - w, xy[k]))), Math.round(Math.max(m, Math.min(H - m - h, xy[k + 1]))), w, h);
      if (!way.some(function (o) { return hits(b, o); })) return b;
      if (keep === true) keep = b;
    }
    return keep || null;
  }
  var TB = null;
  function carry(up, tl, k) {
    var f = up - Math.floor(up), q = f < 0.5 ? (f * 8) | 0 : 5, c = CR, t0, e, a, s, b, y, v, g = 8 * dpr, o = 14 * dpr, xy = [], T;
    if (tl > T_GATE - 0.3 && tl < T_GATE + 1.3) { q = 4; t0 = T_GATE - 0.3; }
    else t0 = [0, T_P1, T_GATE + 1.3, T_P3, 0, T_BACK][q];
    e = clamp((!q && launch && up < 1 ? clock - 0.35 : tl - t0) / 0.25);
    a = e * k * (c.z < 0 ? 0.8 : 1);
    if (a <= 0.01 || !FOK) return;
    T = TAG[q];
    s = sprite("t" + q, [T[0] && T[0] + " ", "k", C.word[q], T[1], "n", q === 4 ? C.gword : C.ink], [T[2], "q", C.ink, T[3], "q", C.ink2]);
    for (v = 0; v < 4; v++) {
      xy.push(c.cx < W * 0.6 && v < 2 ? c.cx + o : c.cx - o - s.w, (v % 2 === 0) === (q === 3 || q === 5) ? c.y - g - s.h : c.y + c.h + g);
    }
    b = place(xy, s.w, s.h, [PB, c], true);
    y = Math.min(H - g - s.h, b.y + Math.round(6 * dpr * (1 - smooth(e))));
    ctx.globalAlpha = a;
    if (c.z >= 0) {
      v = y > c.cy;
      ctx.strokeStyle = rgba(C.soft, 0.6); ctx.lineWidth = dpr; ctx.beginPath();
      ctx.moveTo(c.cx, v ? c.y + c.h - 2 * dpr : c.y + 2 * dpr); ctx.lineTo(Math.max(b.x + o, Math.min(b.x + s.w - o, c.cx)), v ? y : y + s.h); ctx.stroke();
    }
    ctx.drawImage(s.c, b.x, y);
    ctx.globalAlpha = 1;
    TB = bx(b.x, y, s.w, s.h); TB.t = (T[0] && T[0] + " ") + T[1]; TB.q = T[2] + T[3];
  }
  // at rest: four names, and on a stage 400px or wider the sign-off (placed second: least room) and the way back
  var LB = [];
  function names(up, k, forms) {
    var lap = Math.floor(up), g = 6 * dpr, way = forms.map(function (b) { return grow(b, g - dpr); }).concat(PB || []), s, b, a, F, x, y, d;
    [0, 4, 1, 2, 3, 5].forEach(function (q) {
      if (small && q > 3) return;
      s = q < 4 ? sprite("n" + q, [TAG[q][0] + " ", "k", C.word[q], TAG[q][1], "n", C.ink])
        : q === 4 ? sprite("n4", ["sign-off", "k", C.gword]) : sprite("n5", ["then back to Frame, one level up", "q", C.ink2]);
      if (q < 4) {
        F = forms[q]; if (!F) return;
        x = F.x + F.w / 2 - s.w / 2; y = F.y + F.h / 2 - s.h / 2;
        d = [x, F.y + F.h + g, x, F.y - g - s.h, F.x + F.w + g, y, F.x - g - s.w, y, x, F.y + F.h + 3 * g + s.h];
        if (q === 3) d = d.slice(2, 4).concat(d.slice(0, 2), d.slice(4));
      } else if (q === 4) {
        spot(lap + GATE, up); x = P[0] - s.w / 2; y = 21 * px + g;
        d = [x, P[1] - y - s.h, x, P[1] + y, P[0] + y, P[1] - s.h / 2, P[0] - y - s.w, P[1] - s.h / 2, x, P[1] - y - 2 * s.h - g, x, P[1] + y + s.h + g];
      } else {
        spot(lap + 1, up); x = P[0] - 8 * dpr;
        d = [x, P[1] - 12 * dpr - s.h, x, P[1] - 2 * (12 * dpr + s.h), x, P[1] + 12 * dpr];
      }
      b = place(d, s.w, s.h, way);
      if (!b) return;
      way.push(grow(b, g - dpr));
      a = clamp((k - (q < 4 ? q * 0.25 : q * 0.15 + 0.3)) / 0.3);
      if (a > 0.01) { ctx.globalAlpha = a; ctx.drawImage(s.c, b.x, b.y); LB.push(css(b)); }
    });
    ctx.globalAlpha = 1;
  }

  var buf = [], count = new Int32Array(12);
  for (i = 0; i < 12; i++) buf.push(new Float32Array(n * 3));
  function land(lon0) {
    var sL = Math.sin(lon0), cL = Math.cos(lon0), dot = Math.max(1.1 * dpr, R / 185), b, p, q, o, x, y, z, X, Y, cz, sd, cd;
    for (b = 0; b < 12; b++) count[b] = 0;
    for (p = 0; p < n; p++) {
      sd = sLon[p] * cL - cLon[p] * sL; cd = cLon[p] * cL + sLon[p] * sL;
      cz = cLat[p] * cd; z = sT * sLat[p] + cT * cz;
      if (z <= 0.02) continue;
      x = cLat[p] * sd; y = cT * sLat[p] - sT * cz; X = cx + R * x; Y = cy - R * y;
      if (X < -dot || X > W + dot || Y < -dot || Y > H + dot) continue;
      o = x * LX + y * LY + z * LZ;
      b = o <= 0 ? 0 : Math.min(5, (o * 6) | 0);
      if (z < 0.24) b += 6;
      q = buf[b]; o = count[b] * 3;
      q[o] = X; q[o + 1] = Y; q[o + 2] = dot * (0.55 + 0.45 * z);
      count[b]++;
    }
    for (b = 0; b < 12; b++) {
      if (!count[b]) continue;
      ctx.globalAlpha = (0.3 + 0.14 * (b % 6)) * (b < 6 ? 1 : 0.45);
      ctx.fillStyle = tone[b % 6];
      ctx.beginPath();
      for (q = buf[b], p = 0; p < count[b]; p++) { o = p * 3; ctx.moveTo(q[o] + q[o + 2], q[o + 1]); ctx.arc(q[o], q[o + 1], q[o + 2], 0, TAU); }
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  }

  // a first visit launches and rests in round two's P3; a later one rests in its first
  var launch = !reduce && !document.documentElement.classList.contains("hero-seen");
  var PRE = launch ? 0.9 : 0, O0 = launch ? when(0.03) : 0, offset = O0, restAt = when(launch ? 1.4375 : 0.4375);
  var CAM_END = PRE - O0 + T_GATE, clock = 0, stopped = reduce, noRest = false, FOK = true, FONTS = ["600 14px Geist", "600 12px 'Geist Mono'"];
  function draw() {
    if (!W && !fit()) return;
    if (!body) paintBody();
    var t0 = performance.now(), t = Math.max(0, clock - PRE) + offset, ft = t, k = -9, x, forms = [];
    if (reduce || stopped) { ft = restAt; k = 9; }
    else if (!noRest && t > restAt - 1.2) {
      x = Math.min(1, (t - restAt + 1.2) / 2.4); ft = restAt - 1.2 + 2.4 * (x - x * x / 2); k = t - restAt;
    }
    var up = along(ft / LAP), lap = Math.floor(up), f = up - lap, tl = k > 8 ? -1 : ft - when(lap);
    // past the next sign-off the route is dashed; signed, it turns solid from the bar out
    var cut = lap + GATE + (f > GATE ? (tl < 0 ? 1 : smooth((tl - T_GATE - 0.05) / 0.5) * 0.62) : 0);
    if (cut > lap + GATE + 0.61) cut = lap + 1 + GATE;
    if (launch && clock < CAM_END) camera(clock); else { R = R0; cx = cx0; cy = cy0; cam = 1; }
    px = R / 250;
    spot(up, up);
    var near = P[2] >= 0;
    ctx.clearRect(0, 0, W, H);
    blit(glow);
    track(up, false, cut);
    if (!near) { comet(up, false); craft(up, tl); }
    blit(body);
    ctx.beginPath(); ctx.arc(cx, cy, R - 0.75 * px, 0, TAU); ctx.lineWidth = 1.5 * px; ctx.strokeStyle = rgba(C.air, 0.5); ctx.stroke();
    land(HOME - (reduce ? 0 : clock < PRE ? clock : ft + PRE - O0) * TAU / SPIN);
    track(up, true, cut);
    tick(lap + GATE, up, tl); tick(lap + 1 + GATE, up, -1);
    if (cam > 1) {
      ctx.globalCompositeOperation = "destination-out"; ctx.globalAlpha = clamp((cam - 1) * 8);
      ctx.drawImage(edge, 0, 0);
      ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = 1;
    }
    exposures(up, tl, clamp(k + 0.4), forms);
    if (near) { comet(up, true); craft(up, tl); }
    forms.push(CR);
    TB = null; LB = [];
    if (k > -0.4 && FOK) names(up, k, forms);
    if (k < -0.1) carry(up, tl, 1 - clamp((k + 0.4) / 0.3));
    window.GlobeState = { clock: +clock.toFixed(2), leg: legOf(up), tag: TB ? TB.t : "", q: TB ? TB.q : "",
      rest: +clamp((k + 0.4) / 1.75).toFixed(2), cam: +cam.toFixed(3), box: TB && css(TB), craft: css(CR), len: +(CR.len / dpr).toFixed(1),
      pause: PZ, labels: LB, forms: k > -0.4 ? forms.map(css) : [] };
    var g = window.GlobeMs || (window.GlobeMs = { n: 0, sum: 0, max: 0 }), ms = performance.now() - t0;
    g.n++; g.sum += ms; if (ms > g.max) g.max = ms;
  }

  colours();
  cv.parentNode.classList.add("on");
  fit();
  if (document.fonts) {
    var ready = function () { return FONTS.every(function (f) { return document.fonts.check(f); }); }, arrive = function (e) {
      if (!FOK && (FOK = ready() || e.type === "loadingerror")) { SPR = {}; draw(); }
    };
    FOK = ready();
    document.fonts.addEventListener("loadingdone", arrive); document.fonts.addEventListener("loadingerror", arrive);
  }
  draw();
  new MutationObserver(function () { colours(); draw(); }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  window.addEventListener("resize", function () { if (fit()) draw(); });
  window.GlobeAt = function (sec) { stopped = false; noRest = false; offset = O0; clock = sec; draw(); return window.GlobeState.leg; };
  var o = PRE - O0, r2 = function (v) { return +(o + v).toFixed(2); };
  window.GlobeTimes = { lap: +LAP.toFixed(2), pre: PRE, p1: r2(T_P1), gate: r2(T_GATE), p3: r2(T_P3), back: r2(T_BACK), rest: r2(restAt), launch: launch };
  if (reduce) return;

  var shown = true, last = 0, raf = 0, paused = false, box = document.querySelector(".hero2 [data-motion-toggle]");
  function frame(now) {
    raf = 0;
    if (!shown || paused || document.hidden) return;
    if (last && now - last < 14) { raf = requestAnimationFrame(frame); return; }
    clock += (last ? Math.min(now - last, 100) : 16) / 1000;
    last = now;
    draw();
    if (!noRest && Math.max(0, clock - PRE) + offset > restAt + 1.4) {
      stopped = true; draw();
      if (box) box.checked = paused = true;
      return;
    }
    raf = requestAnimationFrame(frame);
  }
  function go() { if (!raf && shown && !paused && !document.hidden) { last = 0; raf = requestAnimationFrame(frame); } }
  if (box) {
    paused = box.checked;
    box.addEventListener("change", function () {
      paused = box.checked;
      if (!paused && stopped) { stopped = false; noRest = true; offset = restAt - Math.max(0, clock - PRE); }
      go();
    });
  }
  if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { shown = en[0].isIntersecting; go(); }).observe(cv);
  document.addEventListener("visibilitychange", go);
  go();
})();
