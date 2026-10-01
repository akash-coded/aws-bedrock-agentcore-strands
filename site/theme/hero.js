/* The home page — the globe behind the flight, and the sections that settle in as they arrive.
   Progressive enhancement only: without this the canvas keeps its CSS disc, the orbit still reads,
   and every section is simply there.

     [data-globe]     the land lattice from #globe-land, drawn as a slowly turning Earth
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
    var HOME = 58 * RAD, SWEEP = 54 * RAD;
    var size = 0, dpr = 1, ink = {}, lon0 = HOME + (reduce ? 0 : SWEEP);

    function colours() {
      var cs = getComputedStyle(cv);
      ["--g-dot", "--g-lit", "--g-a", "--g-b", "--g-rim"].forEach(function (v) {
        ink[v] = (cs.getPropertyValue(v) || "").trim();
      });
    }
    function fit() {
      var w = cv.clientWidth;
      if (!w) return false;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      size = Math.round(w * dpr);
      if (cv.width !== size) { cv.width = size; cv.height = size; }
      return true;
    }

    function draw() {
      if (!size && !fit()) return;
      var c = size / 2, R = c - 1.5 * dpr;
      ctx.clearRect(0, 0, size, size);
      // the sphere itself: lit from the upper left, falling off to the limb
      var g = ctx.createRadialGradient(c - R * 0.38, c - R * 0.42, R * 0.06, c, c, R);
      g.addColorStop(0, ink["--g-a"] || "#1b2333");
      g.addColorStop(1, ink["--g-b"] || "#0d1017");
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(c, c, R, 0, 6.2832); ctx.fill();
      // the land
      var sL = Math.sin(lon0), cL = Math.cos(lon0);
      var dot = Math.max(1.05 * dpr, R / 190);
      for (var p = 0; p < n; p++) {
        var sd = sLon[p] * cL - cLon[p] * sL;          // sin(lon - lon0)
        var cd = cLon[p] * cL + sLon[p] * sL;          // cos(lon - lon0)
        var cz = cLat[p] * cd;
        var z = sT * sLat[p] + cT * cz;
        if (z <= 0.02) continue;                        // the far side
        var x = cLat[p] * sd;
        var y = cT * sLat[p] - sT * cz;
        var lit = x * LX + y * LY + z * LZ;
        var a = (0.22 + 0.78 * Math.max(0, lit)) * Math.min(1, z * 3.2);
        var r = dot * (0.55 + 0.45 * z);
        ctx.globalAlpha = a;
        ctx.fillStyle = lit > 0.72 ? (ink["--g-lit"] || "#fff") : (ink["--g-dot"] || "#9fb4c8");
        ctx.beginPath(); ctx.arc(c + R * x, c - R * y, r, 0, 6.2832); ctx.fill();
      }
      ctx.globalAlpha = 1;
      // a thin bright limb on the lit side
      var rim = ctx.createLinearGradient(c - R, c - R, c + R, c + R);
      rim.addColorStop(0, ink["--g-rim"] || "rgba(255,255,255,.5)");
      rim.addColorStop(0.55, "rgba(0,0,0,0)");
      ctx.strokeStyle = rim; ctx.lineWidth = 1.5 * dpr;
      ctx.beginPath(); ctx.arc(c, c, R, 0, 6.2832); ctx.stroke();
    }

    colours(); fit(); draw();
    new MutationObserver(function () { colours(); draw(); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    if (window.matchMedia) {
      var mq = matchMedia("(prefers-color-scheme: dark)");
      var onScheme = function () { colours(); draw(); };
      if (mq.addEventListener) mq.addEventListener("change", onScheme); else if (mq.addListener) mq.addListener(onScheme);
    }
    window.addEventListener("resize", function () { if (fit()) draw(); });
    if (reduce) return;

    // one turn every four minutes, drawn about thirty times a second, only while it can be seen
    var seen = true, last = 0, raf = 0, elapsed = 0;
    var CRUISE = (360 / 240) * RAD, TAU = 0.6;        // radians a second; the spin-down's time constant, in seconds
    function tick(now) {
      raf = 0;
      if (!seen || paused || document.hidden) return;
      if (now - last > 32) {
        // Where the globe is depends only on how long it has been turning, so a slow or throttled
        // frame rate arrives at the same place: HOME after the spin-down, then the steady drift.
        elapsed += (last ? Math.min(now - last, 100) : 32) / 1000;
        lon0 = HOME + SWEEP * Math.exp(-elapsed / TAU) - CRUISE * elapsed;
        last = now;
        draw();
      }
      raf = requestAnimationFrame(tick);
    }
    var paused = false;
    function go() { if (!raf && seen && !paused && !document.hidden) { last = 0; raf = requestAnimationFrame(tick); } }
    var box = document.querySelector(".hero2 [data-motion-toggle]");
    if (box) {
      paused = box.checked;      // a reload can bring the box back ticked
      box.addEventListener("change", function () { paused = box.checked; go(); });
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { seen = en[0].isIntersecting; go(); }).observe(cv);
    }
    document.addEventListener("visibilitychange", go);
    go();
  }

  function init() { wireReveal(); wireGlobe(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
