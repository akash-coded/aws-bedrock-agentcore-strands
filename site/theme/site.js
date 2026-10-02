/* The agentic manual — progressive enhancement only. Every page works without it. */
(function () {
  "use strict";

  /* Theme: the page opens dark. Light is the reader's choice, and it is remembered. */
  var KEY = "manual-theme";
  var root = document.documentElement;
  function isLight() { return root.getAttribute("data-theme") === "light"; }
  function paint() {      // the browser's own chrome follows the page
    var m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute("content", isLight() ? "#F7F6F2" : "#121316");
  }
  try {
    var saved = localStorage.getItem(KEY);
    if (saved) root.setAttribute("data-theme", saved);
  } catch (e) { /* private mode */ }

  function wireTheme() {
    paint();
    var b = document.querySelector("[data-theme-toggle]");
    if (!b) return;
    var name = function () { b.setAttribute("aria-label", isLight() ? "Switch to dark" : "Switch to light"); };
    name();
    b.addEventListener("click", function () {
      var next = isLight() ? "dark" : "light";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* ignore */ }
      name(); paint();
    });
  }

  /* One polite live region, made on first use, so a screen reader hears what a sighted reader sees. */
  var live = null;
  function wireLive() {      // made with the page, empty, so the first thing said in it is heard
    if (!document.querySelector("[data-copy]")) return;
    live = document.createElement("div");
    live.className = "vh"; live.setAttribute("role", "status"); live.setAttribute("aria-live", "polite");
    document.body.appendChild(live);
  }
  function say(text) {
    if (!live) return;
    live.textContent = ""; setTimeout(function () { live.textContent = text; }, 30);
  }

  /* Copy buttons on every template and prompt. */
  function wireCopy() {
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var pre = document.getElementById(btn.getAttribute("data-copy"));
        if (!pre) return;
        var text = pre.innerText;
        var done = function () {
          var was = btn.textContent;
          btn.textContent = "Copied";
          btn.classList.add("done");
          say("Copied to the clipboard");
          setTimeout(function () { btn.textContent = was; btn.classList.remove("done"); }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, fallback);
        } else { fallback(); }
        function fallback() {
          var ta = document.createElement("textarea");
          ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
          document.body.appendChild(ta); ta.select();
          try { document.execCommand("copy"); done(); } catch (e) { /* nothing to do */ }
          document.body.removeChild(ta);
        }
      });
    });
  }

  /* Open the step a deep link points at, and keep the rail in step with the scroll. The rail marks
     whatever its links point at: a role's steps, or the sections of a long page. */
  function wireSteps() {
    var steps = [].slice.call(document.querySelectorAll("details.step"));
    var root = document.documentElement;

    // Open a step and go to something inside it. The step opens at once here, with no height
    // animation: while it is still unfolding its contents cannot be scrolled to or focused.
    function reveal(d, el) {
      root.classList.add("all-open");
      d.open = true;
      setTimeout(function () {
        el.scrollIntoView();
        if (el.focus) el.focus({ preventScroll: true });
        root.classList.remove("all-open");
      }, 0);
    }
    function openFromHash() {
      var id = (location.hash || "").slice(1);
      if (!id) return;
      var el = document.getElementById(id);
      var d = el && el.closest ? el.closest("details.step") : null;
      if (d && !d.open) reveal(d, el);
    }
    if (steps.length) {
      openFromHash();
      window.addEventListener("hashchange", openFromHash);
      // the links in a step's head: open the step if it is shut, then go, even when the hash is already there
      document.querySelectorAll("[data-jump]").forEach(function (a) {
        a.addEventListener("click", function (e) {
          var el = document.getElementById(a.getAttribute("href").slice(1));
          var d = el && el.closest("details.step");
          if (!el || !d) return;
          e.preventDefault();
          if (history.replaceState) history.replaceState(null, "", a.getAttribute("href"));
          reveal(d, el);
        });
      });
    }

    // The rail marks the last thing whose top has passed the upper third of the window: the section
    // being read. Read from the layout on every scroll, so a jump lands on the right mark too.
    var links = {};
    document.querySelectorAll(".rl[data-for]").forEach(function (a) { links[a.getAttribute("data-for")] = a; });
    var marks = Object.keys(links).map(function (id) { return document.getElementById(id); }).filter(Boolean);
    if (!marks.length) return;
    var was = null, queued = false;
    function mark() {
      queued = false;
      var line = Math.max(140, innerHeight * 0.3), cur = null;
      marks.forEach(function (m) { if (m.getBoundingClientRect().top < line) cur = m; });
      var id = cur ? cur.id : null;
      if (id === was) return;
      if (was && links[was]) { links[was].classList.remove("on"); links[was].removeAttribute("aria-current"); }
      if (id) { links[id].classList.add("on"); links[id].setAttribute("aria-current", "true"); }
      was = id;
    }
    function ask() { if (!queued) { queued = true; requestAnimationFrame(mark); } }
    window.addEventListener("scroll", ask, { passive: true });
    window.addEventListener("resize", ask);
    mark();
  }

  /* "Open all" for printing or reading straight through. */
  function wireExpand() {
    var b = document.querySelector("[data-expand]");
    if (!b) return;
    b.addEventListener("click", function () {
      var steps = [].slice.call(document.querySelectorAll("details.step"));
      var anyClosed = steps.some(function (s) { return !s.open; });
      // all at once: no height animation, eight of them together would only be noise
      document.documentElement.classList.add("all-open");
      steps.forEach(function (s) { s.open = anyClosed; });
      setTimeout(function () { document.documentElement.classList.remove("all-open"); }, 50);
      b.textContent = anyClosed ? "Collapse all" : "Expand all";
    });
    window.addEventListener("beforeprint", function () {
      document.documentElement.classList.add("all-open");
      document.querySelectorAll("details.step").forEach(function (s) { s.open = true; });
    });
    window.addEventListener("afterprint", function () { document.documentElement.classList.remove("all-open"); });
  }

  /* A thin line at the top of a lesson that fills as you read it. */
  function wireProgress() {
    var art = document.querySelector(".lesson .prose");
    if (!art) return;
    var bar = document.createElement("div"); bar.className = "rp"; bar.setAttribute("aria-hidden", "true");
    var fill = document.createElement("i"); bar.appendChild(fill); document.body.appendChild(bar);
    var tick = function () {
      var r = art.getBoundingClientRect(), h = r.height - innerHeight * 0.6;
      var p = h > 0 ? Math.min(1, Math.max(0, -r.top / h)) : 1;
      fill.style.width = (p * 100).toFixed(1) + "%";
    };
    tick(); addEventListener("scroll", tick, { passive: true }); addEventListener("resize", tick);
  }

  /* The picture pack's group picker: one group, or all. */
  function wirePicks() {
    var bar = document.querySelector(".picks");
    if (!bar) return;
    bar.addEventListener("click", function (e) {
      var b = e.target.closest("[data-pick]");
      if (!b) return;
      var pick = b.getAttribute("data-pick");
      bar.querySelectorAll("[data-pick]").forEach(function (x) {
        var on = x === b; x.classList.toggle("on", on); x.setAttribute("aria-pressed", String(on));
      });
      document.querySelectorAll(".picsec").forEach(function (s) {
        s.hidden = pick !== "all" && s.getAttribute("data-group") !== pick;
      });
    });
  }

  /* A long rail opens on the page you are on, not at its top. Wide screens: the rail's own scroll is set,
     once, with no motion. Phones: the folded list scrolls to the current lesson when it is opened. */
  function wireRail() {
    var cur = document.querySelector(".rail [aria-current]");
    if (!cur) return;
    var rail = cur.closest(".rail");
    if (rail && rail.scrollHeight > rail.clientHeight + 4) {
      rail.scrollTop = Math.max(0, cur.getBoundingClientRect().top - rail.getBoundingClientRect().top + rail.scrollTop - rail.clientHeight / 2);
    }
    var fold = cur.closest("details.lnav");
    if (fold) fold.addEventListener("toggle", function () {
      if (fold.open && rail && rail.scrollHeight <= rail.clientHeight + 4) cur.scrollIntoView({ block: "center" });
    });
  }

  function init() { wireTheme(); wireLive(); wireCopy(); wireSteps(); wireExpand(); wireProgress(); wirePicks(); wireRail(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
