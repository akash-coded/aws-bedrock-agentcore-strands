/* The home page — the globe behind the flight, and the sections that settle in as they arrive.
   Progressive enhancement only: without this the canvas keeps its CSS disc, the orbit still reads,
   and every section is simply there.

     [data-globe]     the land lattice from #globe-land, drawn as a turning Earth: one turn a minute
     .rv              a block that rises into place the first time it is scrolled to

   Nothing is fetched. The globe stops when it is off screen, when the tab is hidden, and it is
   drawn once and left alone for a reader who asked for reduced motion. */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------ reveal */
  function wireReveal() {
    var els = [].slice.call(document.querySelectorAll(".rv"));
    if (!els.length) return;
    // A page opened in a background tab has no running clock: nothing is armed there, and it is all simply present.
    if (reduce || !("IntersectionObserver" in window) || document.hidden) return;
    // Only now are the blocks hidden: this script is the one that brings them back. A block already
    // on screen is left as it is, so nothing the reader can see blinks.
    els.forEach(function (e) { if (e.getBoundingClientRect().top < innerHeight) e.classList.add("in"); });
    document.documentElement.classList.add("rv-on");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (e) { io.observe(e); });
    // Leaving the tab, or printing, shows everything at once: content this script hid is content it must show.
    var all = function () { els.forEach(function (e) { e.classList.add("in"); }); io.disconnect(); };
    document.addEventListener("visibilitychange", function () { if (document.hidden) all(); });
    window.addEventListener("beforeprint", all);
  }

  /* ------------------------------------------------------------------- globe */
  function wireGlobe() {
    var cv = document.querySelector("[data-globe]");
    var src = document.getElementById("globe-land");
    if (!cv || !src || !cv.getContext) return;
    var data;
    try { data = JSON.parse(src.textContent); } catch (e) { return; }
    var ctx = cv.getContext("2d");
    var RAD = Math.PI / 180;

    // every dot once: sin and cos of its latitude and longitude
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

    var TILT = 20 * RAD, sT = Math.sin(TILT), cT = Math.cos(TILT);
    var LX = -0.46, LY = 0.56, LZ = 0.69;            // where the light comes from: up and to the left
    // It settles on Europe, Africa and Asia. With motion allowed it arrives there: it starts a
    // quarter turn early and spins down to its cruising speed in the first two seconds.
    var seen = document.documentElement.classList.contains("hero-seen");
    var HOME = 58 * RAD, SWEEP = seen ? 0 : 54 * RAD;
    var size = 0, dpr = 1, lon0 = HOME + (reduce ? 0 : SWEEP);

    // The land is drawn in a few brightness bands, each as one path and one fill. A dot near the
    // limb goes in a fainter band of the same colour, so the edge of the Earth thins out.
    var BANDS = 6, tone = [], buf = [], count = new Int32Array(BANDS * 2);
    for (i = 0; i < BANDS * 2; i++) buf.push(new Float32Array(n * 3));
    function mix(a, b, t) {
      return "rgb(" + Math.round(a[0] + (b[0] - a[0]) * t) + "," + Math.round(a[1] + (b[1] - a[1]) * t) + "," + Math.round(a[2] + (b[2] - a[2]) * t) + ")";
    }
    function rgb(v, fallback) {
      var m = /^#([0-9a-f]{6})$/i.exec(v || "");
      var h = m ? m[1] : fallback;
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    }
    function colours() {
      var cs = getComputedStyle(cv);
      var dim = rgb((cs.getPropertyValue("--g-dot") || "").trim(), "4F7BAA");
      var lit = rgb((cs.getPropertyValue("--g-lit") || "").trim(), "EEF6FF");
      for (var b = 0; b < BANDS; b++) tone[b] = mix(dim, lit, Math.pow(b / (BANDS - 1), 1.35));
    }
    function fit() {
      var w = cv.clientWidth;
      if (!w) return false;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      size = Math.min(1100, Math.round(w * dpr));
      if (cv.width !== size) { cv.width = size; cv.height = size; }
      return true;
    }

    function draw() {
      if (!size && !fit()) return;
      var t0 = performance.now();
      var c = size / 2, R = c - 1.5 * (size / cv.clientWidth || 1);
      ctx.clearRect(0, 0, size, size);
      var sL = Math.sin(lon0), cL = Math.cos(lon0);
      var dot = Math.max(1.1 * (size / (cv.clientWidth || size)), R / 185);
      var b, p, q;
      for (b = 0; b < BANDS * 2; b++) count[b] = 0;
      for (p = 0; p < n; p++) {
        var sd = sLon[p] * cL - cLon[p] * sL;          // sin(lon - lon0)
        var cd = cLon[p] * cL + sLon[p] * sL;          // cos(lon - lon0)
        var cz = cLat[p] * cd;
        var z = sT * sLat[p] + cT * cz;
        if (z <= 0.02) continue;                        // the far side
        var x = cLat[p] * sd;
        var y = cT * sLat[p] - sT * cz;
        var lit = x * LX + y * LY + z * LZ;
        b = lit <= 0 ? 0 : Math.min(BANDS - 1, (lit * BANDS) | 0);
        if (z < 0.24) b += BANDS;
        q = buf[b]; var k = count[b] * 3;
        q[k] = c + R * x; q[k + 1] = c - R * y; q[k + 2] = dot * (0.55 + 0.45 * z);
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
        for (p = 0; p < m; p++) {
          var o = p * 3;
          ctx.moveTo(q[o] + q[o + 2], q[o + 1]);
          ctx.arc(q[o], q[o + 1], q[o + 2], 0, 6.2832);
        }
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      // for the acceptance gate: how long a frame's drawing takes, and how many were drawn
      var g = window.GlobeMs || (window.GlobeMs = { n: 0, sum: 0, max: 0 });
      var ms = performance.now() - t0;
      g.n++; g.sum += ms; if (ms > g.max) g.max = ms;
    }

    colours(); fit(); draw();
    new MutationObserver(function () { colours(); draw(); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    window.addEventListener("resize", function () { if (fit()) draw(); });
    if (reduce) return;

    // one turn a minute, drawn on every frame the display offers, only while it can be seen
    var shown = true, last = 0, raf = 0, elapsed = 0;
    var CRUISE = (360 / 60) * RAD, TAU = 0.6;         // radians a second; the spin-down's time constant, in seconds
    function tick(now) {
      raf = 0;
      if (!shown || paused || document.hidden) return;
      // Where the globe is depends only on how long it has been turning, so a slow or throttled
      // frame rate arrives at the same place: HOME after the spin-down, then the steady turn.
      elapsed += (last ? Math.min(now - last, 100) : 16) / 1000;
      lon0 = HOME + SWEEP * Math.exp(-elapsed / TAU) - CRUISE * elapsed;
      last = now;
      draw();
      raf = requestAnimationFrame(tick);
    }
    var paused = false;
    function go() { if (!raf && shown && !paused && !document.hidden) { last = 0; raf = requestAnimationFrame(tick); } }
    var box = document.querySelector(".hero2 [data-motion-toggle]");
    if (box) {
      paused = box.checked;      // a reload can bring the box back ticked
      box.addEventListener("change", function () { paused = box.checked; go(); });
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { shown = en[0].isIntersecting; go(); }).observe(cv);
    }
    document.addEventListener("visibilitychange", go);
    go();
  }

  function init() { wireReveal(); wireGlobe(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
