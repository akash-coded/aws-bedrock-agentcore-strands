/* The home page's picture, drawn in one canvas on one clock: a turning Earth, a fine spiral around it, and
   one aircraft that climbs the spiral.

     [data-globe]        the canvas. The land comes from #globe-land.
     [data-globe-rail]   the line of phase names under it; the phase the aircraft is in is marked on it

   The front of each turn of the spiral is the journey, P0 to P3. The back of the turn, behind the Earth, is
   the way back to Frame. Each turn sits one step above the last, and the whole spiral sinks at the rate the
   aircraft climbs, so it climbs for ever without leaving the picture. Only the turn being flown is in the
   four phase hues, with its one sign-off; the turns already flown are grey.

   Progressive enhancement only: without this the stylesheet draws a plain shaded disc and the names under
   it still read. Nothing is fetched. Everything is a function of one elapsed time, so the pause control
   holds all of it at once; it also stops when it is off screen or the tab is hidden, and it is drawn once
   and left alone for a reader who asked for reduced motion. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function wireGlobe() {
    var cv = document.querySelector("[data-globe]");
    var src = document.getElementById("globe-land");
    if (!cv || !src || !cv.getContext) return;
    var data;
    try { data = JSON.parse(src.textContent); } catch (e) { return; }
    var ctx = cv.getContext("2d");
    var rail = document.querySelector("[data-globe-rail]");
    var RAD = Math.PI / 180, TAU = Math.PI * 2;

    /* ---------------------------------------------------------------- the land, once */
    var n = 0, i, j, k;
    data.rows.forEach(function (row) { for (i = 1; i < row[1].length; i += 2) n += row[1][i]; });
    var sLat = new Float32Array(n), cLat = new Float32Array(n), sLon = new Float32Array(n), cLon = new Float32Array(n);
    var at = 0;
    data.rows.forEach(function (row, r) {
      var lat = (data.lat0 + r * data.step) * RAD, count = row[0], runs = row[1];
      for (i = 0; i < runs.length; i += 2) {
        for (j = 0; j < runs[i + 1]; j++) {
          k = runs[i] + j;
          var lon = (-180 + (k + 0.5) * 360 / count) * RAD;
          sLat[at] = Math.sin(lat); cLat[at] = Math.cos(lat); sLon[at] = Math.sin(lon); cLon[at] = Math.cos(lon);
          at++;
        }
      }
    });

    /* ---------------------------------------------------------------- the shape of things, in Earth radii */
    var TILT = 20 * RAD, sT = Math.sin(TILT), cT = Math.cos(TILT);        // the Earth leans toward the reader
    var LX = -0.46, LY = 0.56, LZ = 0.69;                                 // the light: up and to the left
    var RHO = 1.3;                                                        // the spiral's radius
    var ALPHA = 15 * RAD, sA = Math.sin(ALPHA), cA = Math.cos(ALPHA);     // how far its plane tips toward the reader
    var ROLL = 14 * RAD, sR = Math.sin(ROLL), cR = Math.cos(ROLL);        // it rises to the right
    var PITCH = 0.17;                                                     // one turn climbs this much
    var LAP = 27, SPIN = 75;                                              // seconds: one turn of the spiral, one of the Earth
    var PAST = 2.3, AHEAD = 0.6;                                          // turns drawn behind the aircraft and ahead of it
    var HOME = 58 * RAD;                                                  // it settles on Europe, Africa and Asia
    var STILL = 0.29;                                                     // a still picture: the aircraft just past the sign-off

    function smooth(x) { return x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x); }
    function ramp(f, a, b) { return smooth((f - a) / (b - a)); }

    // The aircraft is steady in front of the Earth (22 seconds) and quick behind it (5), with the change
    // of speed spread over the two ends of the front arc. FRAC[i] is how far round it is after i/256 of a lap.
    var FRAC = new Float32Array(257);
    (function () {
      var N = 4096, B = 0.035, tt = new Float64Array(N + 1), s = 0, a, f, w;
      for (a = 0; a < N; a++) {
        tt[a] = s; f = (a + 0.5) / N;
        if (f < B) w = 0.5 - 0.5 * smooth(f / B);                         // w: 0 in front of the Earth, 1 behind it
        else if (f < 0.5 - B) w = 0;
        else if (f < 0.5 + B) w = smooth((f - (0.5 - B)) / (2 * B));
        else if (f < 1 - B) w = 1;
        else w = 1 - 0.5 * smooth((f - (1 - B)) / B);
        s += 1 / (1 + w * 3.4);
      }
      tt[N] = s;
      var b = 0;
      for (a = 0; a <= 256; a++) {
        var want = a / 256 * s;
        while (b < N - 1 && tt[b + 1] < want) b++;
        FRAC[a] = (b + (want - tt[b]) / (tt[b + 1] - tt[b] || 1)) / N;
      }
      FRAC[256] = 1;
    })();
    function along(laps) {                                                // laps of time -> turns of the spiral
      var w = Math.floor(laps), f = (laps - w) * 256, a = f | 0;
      return w + FRAC[a] + (FRAC[Math.min(256, a + 1)] - FRAC[a]) * (f - a);
    }

    // Three aircraft with the same fourteen corners in the same order, so one eases into the next.
    function whole(half) {
      var pts = half.slice(), m;
      for (m = half.length - 2; m >= 1; m--) pts.push([half[m][0], -half[m][1]]);
      return pts;
    }
    var DART = whole([[16, 0], [5, -2.3], [-12.2, -10.8], [-13.8, -9.4], [-7.8, -2.6], [-11, -2.1], [-13.4, -1.5], [-11.8, 0]]);
    var LINER = whole([[15.5, 0], [3.5, -2.7], [-5.5, -14], [-9.5, -14], [-3.5, -2.7], [-10.5, -2.3], [-15.5, -7.2], [-13.5, 0]]);
    var JET = whole([[18, 0], [4, -2.3], [-9.5, -10.5], [-13, -10.5], [-8.5, -3.1], [-11.5, -2.7], [-16.5, -6.2], [-12.5, 0]]);

    /* ---------------------------------------------------------------- colour, from the page's own tokens */
    var C = {}, BANDS = 6, tone = [];
    function hex(v, fb) {
      var m = /^#([0-9a-f]{6})$/i.exec((v || "").trim()), h = m ? m[1] : fb;
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    }
    function rgba(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")"; }
    function mix(a, b, t) { return [Math.round(a[0] + (b[0] - a[0]) * t), Math.round(a[1] + (b[1] - a[1]) * t), Math.round(a[2] + (b[2] - a[2]) * t)]; }
    function colours() {
      var cs = getComputedStyle(cv), g = function (name, fb) { return hex(cs.getPropertyValue(name), fb); };
      C.dot = g("--g-dot", "4F7BAA"); C.lit = g("--g-lit", "EEF6FF");
      C.a = g("--g-a", "24487A"); C.m = g("--g-m", "0F2038"); C.b = g("--g-b", "060A12"); C.air = g("--g-air", "4C8FD8");
      C.leg = [g("--dg-slate", "8FA8BE"), g("--dg-indigo", "8E9BF0"), g("--dg-teal", "4FBDB6"), g("--dg-amber", "D9A94A")];
      C.gate = g("--dg-rose", "DE8A8A"); C.ink = g("--ink", "ECEAE4"); C.soft = g("--soft", "93908A"); C.bone = g("--bone", "121316");
      C.dark = C.bone[0] + C.bone[1] + C.bone[2] < 384;
      for (var b = 0; b < BANDS; b++) tone[b] = rgba(mix(C.dot, C.lit, Math.pow(b / (BANDS - 1), 1.35)), 1);
      body = null;
    }

    /* ---------------------------------------------------------------- size */
    var W = 0, H = 0, dpr = 1, cx = 0, cy = 0, R = 0, px = 1, body = null, glow = null;
    function fit() {
      var w = cv.clientWidth, h = cv.clientHeight;
      if (!w || !h) return false;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (w * dpr > 1500) dpr = 1500 / w;
      var nw = Math.round(w * dpr), nh = Math.round(h * dpr);
      if (nw !== W || nh !== H) { W = cv.width = nw; H = cv.height = nh; body = null; }
      R = Math.min(W / 2.92, H / 2.46);                                   // base.css draws its plain disc to the same measure
      cx = W / 2; cy = H / 2;
      px = R / 250;                                                       // the picture is drawn for a radius of 250
      return true;
    }
    function layer() { var c = document.createElement("canvas"); c.width = W; c.height = H; return c; }
    function paintBody() {                                                // the sphere and its air, once per size and theme
      glow = layer(); body = layer();
      var g = glow.getContext("2d"), b = body.getContext("2d"), gr;
      var edge = Math.min(cx, cy) * 0.99;                                 // the air ends inside the canvas: no edge ever shows
      gr = g.createRadialGradient(cx, cy, R * 0.92, cx, cy, edge);
      gr.addColorStop(0, rgba(C.air, C.dark ? 0.36 : 0.28)); gr.addColorStop(0.3, rgba(C.air, C.dark ? 0.15 : 0.12));
      gr.addColorStop(0.7, rgba(C.air, 0.03)); gr.addColorStop(1, rgba(C.air, 0));
      g.fillStyle = gr; g.fillRect(0, 0, W, H);
      b.save(); b.beginPath(); b.arc(cx, cy, R, 0, TAU); b.clip();
      gr = b.createRadialGradient(cx - R * 0.4, cy - R * 0.44, 0, cx - R * 0.4, cy - R * 0.44, R * 1.72);
      gr.addColorStop(0, rgba(C.a, 1)); gr.addColorStop(0.46, rgba(C.m, 1)); gr.addColorStop(0.86, rgba(C.b, 1));
      b.fillStyle = gr; b.fillRect(cx - R, cy - R, R * 2, R * 2);
      gr = b.createRadialGradient(cx, cy, R * 0.86, cx, cy, R);            // the thin bright air at the limb
      gr.addColorStop(0, rgba(C.air, 0)); gr.addColorStop(1, rgba(C.air, C.dark ? 0.34 : 0.3));
      b.fillStyle = gr; b.fillRect(cx - R, cy - R, R * 2, R * 2);
      b.restore();
      b.beginPath(); b.arc(cx, cy, R - 0.75 * px, 0, TAU); b.lineWidth = 1.5 * px; b.strokeStyle = rgba(C.air, 0.5); b.stroke();
    }

    /* ---------------------------------------------------------------- the spiral */
    var P = [0, 0, 0];
    function spot(u, up) {                                                // the point u turns along, with the aircraft at up
      var ph = u * TAU, X = -RHO * Math.cos(ph), Z = RHO * Math.sin(ph), Y = PITCH * (u - up);
      var y1 = Y * cA - Z * sA;
      P[0] = cx + R * (X * cR - y1 * sR); P[1] = cy - R * (X * sR + y1 * cR); P[2] = Y * sA + Z * cA;
    }
    function legOf(u) { var f = u - Math.floor(u); return f < 0.5 ? (f * 8) | 0 : 4; }   // 0 to 3: a phase; 4: the way back
    // How much of its hue a point keeps. The turn being flown has all of it. While the aircraft is behind
    // the Earth the hue passes from the turn just flown to the one about to be, so nothing changes at once.
    function live(u, up) {
      var k = Math.floor(u) - Math.floor(up), f = up - Math.floor(up), t = f < 0.5 ? 0 : smooth((f - 0.5) / 0.5);
      return k === 0 ? 1 - t : k === 1 ? t : 0;
    }
    function hue(leg, w) { return leg === 4 || w <= 0 ? C.soft : w >= 1 ? C.leg[leg] : mix(C.soft, C.leg[leg], w); }
    function fade(d) {                                                    // this turn, the one below at about a third, the one under that fainter
      if (d <= 0) { var p = -d; return p < 0.55 ? 1 - p * 0.55 : p < 1.3 ? 0.7 - (p - 0.55) / 0.75 * 0.42 : 0.28 * Math.max(0, 1 - (p - 1.3) / (PAST - 1.3)); }
      return 0.62 * Math.pow(Math.max(0, 1 - d / AHEAD), 0.8);
    }
    var STEP = 1 / 120;
    function track(up, front) {                                           // the half behind the Earth, or the half in front
      var u, leg, a, w, runLeg = -1, runA = -1, runW = -1, open = false, x0 = 0, y0 = 0, z0 = 0, has = false;
      ctx.lineCap = "butt"; ctx.lineJoin = "round";
      for (u = Math.ceil((up - PAST) / STEP) * STEP; u <= up + AHEAD + 1e-6; u += STEP) {
        spot(u, up);
        if (has) {
          var near = (P[2] + z0) / 2 >= 0;
          leg = legOf(u - STEP / 2);
          a = near === front ? Math.round(fade(u - STEP / 2 - up) * (near ? 1 : 0.62) * 24) / 24 : 0;
          w = leg === 4 ? 0 : Math.round(live(u - STEP / 2, up) * 8) / 8;
          if (a > 0 && (leg !== runLeg || a !== runA || w !== runW)) {
            if (open) ctx.stroke();
            ctx.beginPath(); ctx.moveTo(x0, y0); open = true; runLeg = leg; runA = a; runW = w;
            ctx.strokeStyle = rgba(hue(leg, w), a * (0.75 + 0.25 * w));
            ctx.lineWidth = (1.3 + 0.7 * w) * px;
          }
          if (a > 0) ctx.lineTo(P[0], P[1]);
          else { if (open) ctx.stroke(); open = false; runLeg = -1; }
        }
        x0 = P[0]; y0 = P[1]; z0 = P[2]; has = true;
      }
      if (open) ctx.stroke();
    }
    function comet(up, near) {                                            // the path just flown: wide at the aircraft, narrowing behind
      var N = 36, LEN = 0.12, a, x0, y0;
      spot(up, up); x0 = P[0]; y0 = P[1];
      ctx.lineCap = "butt";
      for (a = 1; a <= N; a++) {
        var u = up - LEN * a / N, leg = legOf(u + LEN / N / 2), t = 1 - (a - 0.5) / N;
        spot(u, up);
        ctx.strokeStyle = rgba(hue(leg, live(u, up)), (0.25 + 0.75 * t) * (near ? 1 : 0.6));
        ctx.lineWidth = (2 + 2.6 * t * t) * px;
        ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(P[0], P[1]); ctx.stroke();
        x0 = P[0]; y0 = P[1];
      }
    }
    function tick(u, up) {                                                // the sign-off: a short bar across the path
      spot(u, up); var x = P[0], y = P[1], z = P[2];
      if (z < 0) return;
      spot(u + 0.004, up); var dx = P[0] - x, dy = P[1] - y, l = Math.sqrt(dx * dx + dy * dy) || 1;
      var d = up - u, hit = d > 0 && d < 0.03 ? Math.sin(d / 0.03 * Math.PI) : 0;       // the aircraft has just crossed it
      var a = Math.min(1, fade(u - up) * 1.6) * (0.6 + 0.4 * hit) * live(u, up), len = (15 + 6 * hit) * px;
      if (a <= 0.02) return;
      ctx.strokeStyle = rgba(C.gate, a); ctx.lineWidth = 2.6 * px; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(x - dy / l * len, y + dx / l * len); ctx.lineTo(x + dy / l * len, y - dx / l * len); ctx.stroke();
    }
    function craft(up) {
      // a paper dart in P0, the outline of an airliner in P1, the airliner solid from the sign-off on,
      // a jet in P3, and the dart again by the time it comes round from behind the Earth
      var f = up - Math.floor(up), m, ax, ay;
      var toLiner = ramp(f, 0.113, 0.137), toJet = ramp(f, 0.363, 0.387), toDart = ramp(f, 0.66, 0.84);
      var solid = ramp(f, 0.25, 0.268) * (1 - toDart);
      spot(up, up); var x = P[0], y = P[1], z = P[2];
      spot(up + 0.003, up); var ang = Math.atan2(P[1] - y, P[0] - x);
      var s = px * 1.32 * (1 + 0.12 * z / RHO), a = z >= 0 ? 1 : 0.7;
      ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s);
      ctx.beginPath();
      for (m = 0; m < 14; m++) {
        ax = DART[m][0] + (LINER[m][0] - DART[m][0]) * toLiner; ay = DART[m][1] + (LINER[m][1] - DART[m][1]) * toLiner;
        ax += (JET[m][0] - ax) * toJet; ay += (JET[m][1] - ay) * toJet;
        ax += (DART[m][0] - ax) * toDart; ay += (DART[m][1] - ay) * toDart;
        if (m) ctx.lineTo(ax, ay); else ctx.moveTo(ax, ay);
      }
      ctx.closePath();
      ctx.fillStyle = rgba(C.bone, a * 0.92); ctx.fill();                 // an outline: a drawing of an aircraft
      if (solid > 0) { ctx.fillStyle = rgba(C.ink, a * solid); ctx.fill(); }   // signed off: it is built
      ctx.lineJoin = "round"; ctx.lineWidth = 1.5; ctx.strokeStyle = rgba(C.ink, a); ctx.stroke();
      ctx.restore();
    }

    /* ---------------------------------------------------------------- the Earth's land */
    // Drawn in a few brightness bands, each as one path and one fill. A dot near the limb goes in a
    // fainter band of the same colour, so the edge of the Earth thins out.
    var buf = [], count = new Int32Array(BANDS * 2);
    for (i = 0; i < BANDS * 2; i++) buf.push(new Float32Array(n * 3));
    function land(lon0) {
      var sL = Math.sin(lon0), cL = Math.cos(lon0), dot = Math.max(1.1 * dpr, R / 185), b, p, q, o;
      for (b = 0; b < BANDS * 2; b++) count[b] = 0;
      for (p = 0; p < n; p++) {
        var sd = sLon[p] * cL - cLon[p] * sL, cd = cLon[p] * cL + sLon[p] * sL;
        var cz = cLat[p] * cd, z = sT * sLat[p] + cT * cz;
        if (z <= 0.02) continue;                                          // the far side
        var x = cLat[p] * sd, y = cT * sLat[p] - sT * cz, lit = x * LX + y * LY + z * LZ;
        b = lit <= 0 ? 0 : Math.min(BANDS - 1, (lit * BANDS) | 0);
        if (z < 0.24) b += BANDS;
        q = buf[b]; o = count[b] * 3;
        q[o] = cx + R * x; q[o + 1] = cy - R * y; q[o + 2] = dot * (0.55 + 0.45 * z);
        count[b]++;
      }
      for (b = 0; b < BANDS * 2; b++) {
        var m = count[b];
        if (!m) continue;
        var band = b % BANDS;
        ctx.globalAlpha = (0.3 + 0.7 * band / (BANDS - 1)) * (b < BANDS ? 1 : 0.45);
        ctx.fillStyle = tone[band];
        ctx.beginPath();
        q = buf[b];
        for (p = 0; p < m; p++) { o = p * 3; ctx.moveTo(q[o] + q[o + 2], q[o + 1]); ctx.arc(q[o], q[o + 1], q[o + 2], 0, 6.2832); }
        ctx.fill();
      }
      ctx.globalAlpha = 1;
    }

    /* ---------------------------------------------------------------- one frame */
    // The only arrival is the Earth's: it starts a little early and spins down to its steady turn in the
    // first second or two. The path and the aircraft are simply there. A second visit in the same sitting
    // finds it already settled.
    var seen = document.documentElement.classList.contains("hero-seen");
    var clock = 0, lastLeg = -2;
    function draw() {
      if (!W && !fit()) return;
      if (!body) paintBody();
      var t0 = performance.now();
      var up = reduce ? STILL : along(clock / LAP + 0.02);
      var lon0 = HOME + (reduce || seen ? 0 : 54 * RAD * Math.exp(-clock / 0.6)) - clock * TAU / SPIN;
      spot(up, up);
      var near = P[2] >= 0, lap = Math.floor(up);
      ctx.clearRect(0, 0, W, H);
      ctx.drawImage(glow, 0, 0);
      track(up, false);
      if (!near) { comet(up, false); craft(up); }
      ctx.drawImage(body, 0, 0);
      land(lon0);
      track(up, true);
      tick(lap + 0.25, up); tick(lap + 1.25, up);
      if (near) { comet(up, true); craft(up); }
      var leg = reduce ? -1 : legOf(up);
      if (rail && leg !== lastLeg) { rail.setAttribute("data-at", leg < 0 ? "" : leg === 4 ? "back" : String(leg)); lastLeg = leg; }
      // for the acceptance gate: how long a frame's drawing takes, and how many were drawn
      var g = window.GlobeMs || (window.GlobeMs = { n: 0, sum: 0, max: 0 });
      var ms = performance.now() - t0;
      g.n++; g.sum += ms; if (ms > g.max) g.max = ms;
    }

    colours(); fit(); draw();
    cv.parentNode.classList.add("on");                                    // the stylesheet's plain disc steps aside
    new MutationObserver(function () { colours(); draw(); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    window.addEventListener("resize", function () { if (fit()) draw(); });
    if (reduce) return;

    // drawn on every frame the display offers, only while it can be seen. Where everything is depends only
    // on how long it has been running, so a slow or throttled frame rate arrives at the same place.
    var shown = true, last = 0, raf = 0, paused = false;
    function frame(now) {
      raf = 0;
      if (!shown || paused || document.hidden) return;
      clock += (last ? Math.min(now - last, 100) : 16) / 1000;
      last = now;
      draw();
      raf = requestAnimationFrame(frame);
    }
    function go() { if (!raf && shown && !paused && !document.hidden) { last = 0; raf = requestAnimationFrame(frame); } }
    var box = document.querySelector(".hero2 [data-motion-toggle]");
    if (box) {
      paused = box.checked;      // a reload can bring the box back ticked
      box.addEventListener("change", function () { paused = box.checked; go(); });
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { shown = en[0].isIntersecting; go(); }).observe(cv);
    }
    document.addEventListener("visibilitychange", go);
    // for the acceptance gate: put the clock at a given second and draw that frame
    window.GlobeAt = function (sec) { clock = sec; draw(); return legOf(along(clock / LAP + 0.02)); };
    go();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", wireGlobe); else wireGlobe();
})();
