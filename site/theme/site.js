/* The agentic manual — progressive enhancement only. Every page works without it. */
(function () {
  "use strict";

  /* Theme: remember the reader's choice, default to the system. */
  var KEY = "manual-theme";
  try {
    var saved = localStorage.getItem(KEY);
    if (saved) document.documentElement.setAttribute("data-theme", saved);
  } catch (e) { /* private mode */ }

  function wireTheme() {
    var b = document.querySelector("[data-theme-toggle]");
    if (!b) return;
    b.addEventListener("click", function () {
      var dark = document.documentElement.getAttribute("data-theme") === "dark" ||
        (!document.documentElement.getAttribute("data-theme") &&
          window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* ignore */ }
      b.setAttribute("aria-label", next === "dark" ? "Switch to light" : "Switch to dark");
    });
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

  /* Open the step a deep link points at, and keep the rail in step with the scroll. */
  function wireSteps() {
    var steps = [].slice.call(document.querySelectorAll("details.step"));
    if (!steps.length) return;

    function openFromHash() {
      var id = (location.hash || "").slice(1);
      if (!id) return;
      var el = document.getElementById(id);
      var d = el && el.closest ? el.closest("details.step") : null;
      if (d && !d.open) { d.open = true; setTimeout(function () { el.scrollIntoView(); }, 0); }
    }
    openFromHash();
    window.addEventListener("hashchange", openFromHash);

    var links = {};
    document.querySelectorAll(".rl[data-for]").forEach(function (a) { links[a.getAttribute("data-for")] = a; });
    if (!("IntersectionObserver" in window)) return;
    var seen = new Set();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) seen.add(en.target.id); else seen.delete(en.target.id);
      });
      Object.keys(links).forEach(function (k) { links[k].classList.remove("on"); });
      var first = steps.map(function (s) { return s.id; }).find(function (id) { return seen.has(id); });
      if (first && links[first]) links[first].classList.add("on");
    }, { rootMargin: "-80px 0px -70% 0px" });
    steps.forEach(function (s) { io.observe(s); });
  }

  /* "Open all" for printing or reading straight through. */
  function wireExpand() {
    var b = document.querySelector("[data-expand]");
    if (!b) return;
    b.addEventListener("click", function () {
      var steps = [].slice.call(document.querySelectorAll("details.step"));
      var anyClosed = steps.some(function (s) { return !s.open; });
      steps.forEach(function (s) { s.open = anyClosed; });
      b.textContent = anyClosed ? "Collapse all" : "Expand all";
    });
    window.addEventListener("beforeprint", function () {
      document.querySelectorAll("details.step").forEach(function (s) { s.open = true; });
    });
  }

  function init() { wireTheme(); wireCopy(); wireSteps(); wireExpand(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
