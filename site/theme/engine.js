/* ==========================================================================
   The agentic manual — interaction engine.

   Four behaviours, all declarative, all progressive enhancement. Every page
   is complete and readable with JavaScript off; this only makes it faster to
   use. Nothing here fetches, stores or reports anything.

     data-lens-toggle / data-lens="black|white"   two readings of the same thing
     data-calc="<name>"                           a live calculator
     data-score                                   a self-check that totals itself
     data-stepper                                 a sequence you walk

   Calculators are pure functions in CALCS. Adding one is adding a function
   and marking up the inputs; no wiring.
   ========================================================================== */
(function () {
  "use strict";

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); };
  var num = function (el) { var v = parseFloat(el.value); return isFinite(v) ? v : 0; };
  var money = function (n) {
    return (n < 0 ? "-" : "") + "$" + Math.abs(Math.round(n)).toLocaleString("en-GB");
  };
  var pct = function (n) { return (n * 100).toFixed(n < 0.1 ? 1 : 0) + "%"; };

  /* ---------------------------------------------------------------- lenses */
  /* Two readings of one idea: what it does, and how it works. Without JS both
     are visible, which is longer but never wrong. */
  var LENS_KEY = "manual-lens";

  function applyLens(mode) {
    document.documentElement.setAttribute("data-lens-mode", mode);
    $$("[data-lens-toggle] button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lens-set") === mode));
    });
    try { localStorage.setItem(LENS_KEY, mode); } catch (e) { /* private mode */ }
  }

  function wireLenses() {
    var groups = $$("[data-lens-toggle]");
    if (!groups.length) return;
    var saved = "black";
    try { saved = localStorage.getItem(LENS_KEY) || "black"; } catch (e) { /* ignore */ }
    groups.forEach(function (g) {
      g.addEventListener("click", function (ev) {
        var b = ev.target.closest("button[data-lens-set]");
        if (b) applyLens(b.getAttribute("data-lens-set"));
      });
    });
    applyLens(saved);
  }

  /* ----------------------------------------------------------- calculators */
  /* Each returns { <outputName>: value }. Values may be a number, a string, or
     { v: string, tone: "ok"|"warn"|"stop" } to colour the result. */
  var CALCS = {
    /* bar = N / (N + 1), N = damage / saving. A hold cuts the damage. */
    bar: function (i) {
      var saving = Math.max(i.saving, 0.01), damage = Math.max(i.damage, 0);
      var n = damage / saving, bar = n / (n + 1);
      var held = (damage * (i.holdcut / 100)) / saving;
      var barHeld = held / (held + 1);
      return {
        n: n.toFixed(1),
        bar: { v: pct(bar), tone: bar > 0.95 ? "stop" : bar > 0.85 ? "warn" : "ok" },
        barheld: { v: pct(barHeld), tone: barHeld > 0.95 ? "stop" : "ok" },
        verdict: bar > 0.95
          ? "Above 95% is a design signal, not a target: put a person on this step."
          : "Reachable. Prove it with the lower bound, not the score."
      };
    },

    /* net = cases x minutes x rate - run - review */
    value: function (i) {
      var gross = i.cases * i.minutes * i.rate;
      var run = i.cases * i.runcost;
      var review = i.cases * (i.reviewshare / 100) * i.reviewmin * i.rate;
      var net = gross - run - review;
      return {
        gross: money(gross), run: money(-run), review: money(-review),
        net: { v: money(net) + " / day", tone: net > 0 ? "ok" : "stop" },
        year: money(net * 250),
        verdict: net <= 0
          ? "Negative. The review load is usually the term to attack first."
          : review > gross * 0.3
            ? "Positive, but review eats " + pct(review / gross) + " of the saving. That is the cycle-2 job."
            : "Positive, with review under control."
      };
    },

    /* lower bound and cases owed */
    proof: function (i) {
      var p = i.score / 100, n = Math.max(i.n, 1), bar = i.bar / 100, z = 1.96;
      var lo = p - z * Math.sqrt((p * (1 - p)) / n);
      var den = 1 + (z * z) / n;
      var centre = (p + (z * z) / (2 * n)) / den;
      var half = (z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n))) / den;
      var wilson = centre - half;
      var use = n < 100 ? wilson : lo;
      var proven = use >= bar;
      var needed = p > bar ? Math.ceil((z * z * p * (1 - p)) / Math.pow(p - bar, 2)) : Infinity;
      return {
        normal: pct(lo), wilson: pct(wilson),
        bound: { v: pct(use) + (n < 100 ? " (Wilson)" : ""), tone: proven ? "ok" : "warn" },
        verdict: proven
          ? { v: "Proven — the lower bound clears the bar.", tone: "ok" }
          : p <= bar
            ? { v: "The score itself is below the bar. More cases will not fix this.", tone: "stop" }
            : { v: "Not proven. Owe " + (needed - n).toLocaleString("en-GB") + " more cases (" +
                   needed.toLocaleString("en-GB") + " total).", tone: "warn" }
      };
    },

    /* the four bill factors multiply; f is the cacheable share of spend */
    bill: function (i) {
      var ctx = i.tokens_now / Math.max(i.tokens_base, 1);
      var tier = i.tier_now / Math.max(i.tier_base, 0.01);
      var f = i.cacheshare / 100, d = 0.9;
      var cache = (1 - d * (i.hit_now / 100) * f) / (1 - d * (i.hit_base / 100) * f);
      var retry = (1 + i.retry_now) / (1 + i.retry_base);
      var product = ctx * tier * cache * retry;
      var worst = [["context", ctx], ["tier", tier], ["cache", cache], ["retries", retry]]
        .sort(function (a, b) { return b[1] - a[1]; })[0];
      return {
        ctx: ctx.toFixed(2), tier: tier.toFixed(2), cache: cache.toFixed(2), retry: retry.toFixed(2),
        product: { v: product.toFixed(2) + "x", tone: product > 2 ? "stop" : product > 1.3 ? "warn" : "ok" },
        verdict: "Largest single factor: " + worst[0] + " at " + worst[1].toFixed(2) +
                 "x. Fix in order of (factor - 1) / days, not by size."
      };
    },

    /* days = cases needed / (share x cases per day) */
    evidence: function (i) {
      var perDay = (i.share / 100) * i.cases;
      var days = perDay > 0 ? i.needed / perDay : Infinity;
      return {
        perday: Math.round(perDay) + " / day",
        days: { v: isFinite(days) ? Math.ceil(days) + " days" : "never", tone: days > 45 ? "stop" : days > 21 ? "warn" : "ok" },
        verdict: days > 45
          ? "Too slow to learn from. Start at a larger share, or accept that this slice stays gated."
          : "Workable. Widen when the live lower bound holds, not on the date."
      };
    },

    /* Little's law on review slots */
    queue: function (i) {
      var slots = i.r45 * 2 + i.r23 * 1 + i.r1 * 0;
      var all = (i.r45 + i.r23 + i.r1) * 2;
      var cap = Math.max(i.capacity, 0.1);
      return {
        slotsall: all, slotsrouted: slots,
        before: (all / cap).toFixed(1) + " days",
        after: { v: (slots / cap).toFixed(1) + " days", tone: "ok" },
        verdict: "Capacity is fixed by people. Slots needed is a policy choice you can change today."
      };
    },

    /* caching pays from the second use */
    cache: function (i) {
      var w = i.window === "hour" ? 2 : 1.25;
      var withC = w + 0.1 * (i.uses - 1);
      var without = i.uses;
      return {
        withc: withC.toFixed(2) + " units", without: without.toFixed(2) + " units",
        saving: { v: without > 0 ? pct(1 - withC / without) : "-",
                  tone: withC < without ? "ok" : "stop" },
        verdict: withC >= without
          ? "Caching costs more here. Below two uses it always does."
          : "Pays. Check the measured hit ratio before trusting this."
      };
    }
  };

  function runCalc(root) {
    var name = root.getAttribute("data-calc");
    var fn = CALCS[name];
    if (!fn) return;
    var inputs = {};
    $$("[data-in]", root).forEach(function (el) {
      inputs[el.getAttribute("data-in")] = el.type === "range" || el.type === "number"
        ? num(el) : el.value;
      var echo = $('[data-echo="' + el.getAttribute("data-in") + '"]', root);
      if (echo) echo.textContent = el.value;
    });
    var out = fn(inputs);
    Object.keys(out).forEach(function (k) {
      var el = $('[data-out="' + k + '"]', root);
      if (!el) return;
      var v = out[k];
      el.classList.remove("ok", "warn", "stop");
      if (v && typeof v === "object") { el.textContent = v.v; if (v.tone) el.classList.add(v.tone); }
      else { el.textContent = v; }
    });
  }

  function wireCalcs() {
    $$("[data-calc]").forEach(function (root) {
      $$("[data-in]", root).forEach(function (el) {
        el.addEventListener("input", function () { runCalc(root); });
        el.addEventListener("change", function () { runCalc(root); });
      });
      runCalc(root);
    });
  }

  /* ------------------------------------------------------------ self-check */
  function wireScores() {
    $$("[data-score]").forEach(function (root) {
      var boxes = $$('input[type="checkbox"]', root);
      var out = $("[data-score-out]", root);
      var verdict = $("[data-score-verdict]", root);
      var next = $("[data-score-next]", root);
      var bands = (root.getAttribute("data-score-bands") || "").split("|");
      function tally() {
        var got = boxes.filter(function (b) { return b.checked; });
        if (out) out.textContent = got.length + " of " + boxes.length;
        if (verdict && bands.length) {
          var i = Math.min(Math.floor((got.length / boxes.length) * bands.length), bands.length - 1);
          verdict.textContent = bands[i];
        }
        if (next) {
          var missing = boxes.filter(function (b) { return !b.checked; })[0];
          next.textContent = missing
            ? (missing.getAttribute("data-label") || "").trim()
            : "Nothing missing. Re-check in a quarter — this list goes stale.";
        }
        root.setAttribute("data-filled", String(got.length));
      }
      boxes.forEach(function (b) { b.addEventListener("change", tally); });
      tally();
    });
  }

  /* --------------------------------------------------------------- stepper */
  function wireSteppers() {
    $$("[data-stepper]").forEach(function (root) {
      var panels = $$("[data-step]", root);
      if (panels.length < 2) return;
      var dots = $("[data-step-dots]", root);
      var label = $("[data-step-label]", root);
      var i = 0;
      if (dots) {
        dots.innerHTML = "";
        panels.forEach(function (p, k) {
          var b = document.createElement("button");
          b.type = "button";
          b.className = "stp-dot";
          b.setAttribute("aria-label", "Step " + (k + 1) + ": " + (p.getAttribute("data-step") || ""));
          b.addEventListener("click", function () { i = k; draw(); });
          dots.appendChild(b);
        });
      }
      function draw() {
        panels.forEach(function (p, k) { p.hidden = k !== i; });
        if (dots) $$(".stp-dot", dots).forEach(function (d, k) {
          d.classList.toggle("on", k === i);
          d.classList.toggle("done", k < i);
        });
        if (label) label.textContent = (i + 1) + " of " + panels.length + " · " +
          (panels[i].getAttribute("data-step") || "");
        var prev = $("[data-step-prev]", root), nxt = $("[data-step-next]", root);
        if (prev) prev.disabled = i === 0;
        if (nxt) nxt.disabled = i === panels.length - 1;
      }
      var p = $("[data-step-prev]", root), n = $("[data-step-next]", root);
      if (p) p.addEventListener("click", function () { i = Math.max(0, i - 1); draw(); });
      if (n) n.addEventListener("click", function () { i = Math.min(panels.length - 1, i + 1); draw(); });
      root.addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft" && p && !p.disabled) { i--; draw(); }
        if (e.key === "ArrowRight" && n && !n.disabled) { i++; draw(); }
      });
      draw();
    });
    // Printing must not hide eight of nine panels.
    window.addEventListener("beforeprint", function () {
      $$("[data-stepper] [data-step]").forEach(function (p) { p.hidden = false; });
    });
  }

  /* ---------------------------------------------------------------- reveal */
  /* A board's parts arrive in the order they are meant to be read, because on
     these diagrams the order IS the lesson. This is the only motion on the site
     that touches content, so it is armed by script and disarmed three ways: no
     script, reduced motion, or a watchdog if the observer never fires. Content
     that script hides must be content script is certain to show. */
  function wireReveal() {
    var groups = $$("[data-reveal]");
    if (!groups.length) return;
    if (!("IntersectionObserver" in window)) return;
    try {
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    } catch (e) { return; }
    // A document that starts hidden never gets a running clock, so it never gets
    // the animation either. Nothing is armed and everything is simply present.
    if (document.hidden) return;

    groups.forEach(function (g) {
      var kids = [].slice.call(g.children);
      // a long group steps faster, so a 30-cell matrix does not take three seconds
      var step = Math.max(22, Math.min(90, 620 / Math.max(1, kids.length)));
      kids.forEach(function (k, i) {
        k.style.setProperty("--rvd", Math.round(i * step) + "ms");
      });
      g.setAttribute("data-reveal-armed", "");
    });

    // The gentle path: let the transition play.
    var show = function (g) { g.setAttribute("data-revealed", ""); };

    // The certain path. A hidden document freezes transition clocks, so simply
    // dropping the rule that hides a part is not enough — an in-flight transition
    // goes on pinning it at zero with its clock stopped. Take the declaration away
    // and finish any animation still holding the old value.
    var forceShow = function (g) {
      g.setAttribute("data-revealed", "");
      g.removeAttribute("data-reveal-armed");
      [].slice.call(g.children).forEach(function (k) {
        if (!k.getAnimations) return;
        k.getAnimations().forEach(function (a) { try { a.finish(); } catch (e) { /* done */ } });
      });
    };
    var forceAll = function () { groups.forEach(forceShow); };

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        show(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -8% 0px" });
    groups.forEach(function (g) { io.observe(g); });

    // Three ways out, because content script hides is content script must show.
    setTimeout(forceAll, 2600);
    window.addEventListener("beforeprint", forceAll);
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) forceAll();
    });
  }

  /* ---------------------------------------------------------------- matrix */
  /* Reading a cell in a five-by-four grid means holding its row and its column
     in your head. Lighting both is the whole feature. Pointer and keyboard
     both drive it; without script the grid is simply undimmed. */
  function wireMatrix() {
    $$("[data-matrix]").forEach(function (m) {
      var cells = $$("[data-row],[data-col]", m);
      function light(row, col) {
        if (row === null) {
          m.removeAttribute("data-hot");
          cells.forEach(function (el) { el.classList.remove("lit"); });
          return;
        }
        m.setAttribute("data-hot", "");
        cells.forEach(function (el) {
          var on = el.getAttribute("data-row") === row || el.getAttribute("data-col") === col;
          el.classList.toggle("lit", on);
        });
      }
      cells.forEach(function (el) {
        var hit = function () {
          light(el.getAttribute("data-row"), el.getAttribute("data-col"));
        };
        el.addEventListener("pointerenter", hit);
        el.addEventListener("focus", hit);
        el.addEventListener("blur", function () { light(null, null); });
      });
      m.addEventListener("pointerleave", function () { light(null, null); });
    });
  }

  /* ------------------------------------------------------------------ loops */
  /* A drawing and the cards that unpack it are one thing. Pointing at either
     end dims everything that is not the loop you are reading. */
  function wireLoops() {
    $$(".dgb").forEach(function (board) {
      var parts = $$("[data-loop]", board);
      if (parts.length < 2) return;
      var set = function (name) {
        if (name) board.setAttribute("data-loop-hot", name);
        else board.removeAttribute("data-loop-hot");
      };
      parts.forEach(function (el) {
        var name = el.getAttribute("data-loop");
        el.addEventListener("pointerenter", function () { set(name); });
        el.addEventListener("pointerleave", function () { set(null); });
      });
      board.addEventListener("pointerleave", function () { set(null); });
    });
  }

  function init() {
    wireLenses(); wireCalcs(); wireScores(); wireSteppers();
    wireReveal(); wireMatrix(); wireLoops();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
