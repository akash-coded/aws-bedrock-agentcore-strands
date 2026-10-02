/* The agentic manual — wayfinding. Progressive enhancement only.

   Three behaviours, none required to read the site:

     [data-menu]            the drawer: Esc closes it, so does a click on the scrim
     #tour-steps            a walkthrough the page declares as JSON — [{sel, title, body}] —
                            one highlighted element at a time, started by a [data-tour-start]
                            button: "Show me around this page" in the drawer, "Show me around"
                            in the page's folded how-to
     [data-dd]              the top bar's two short lists: one open at a time

   Nothing here reports anything, and nothing is stored. The search index is fetched from this
   site the first time the search box is used. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html) n.innerHTML = html;
    return n;
  }

  /* ------------------------------------------------------------------ drawer */
  function wireMenu() {
    var d = $("[data-menu]");
    if (!d) return;
    var close = function () { d.open = false; };
    var x = $("[data-menu-close]", d);
    if (x) x.addEventListener("click", close);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && d.open) { close(); $("summary", d).focus(); }
    });
    // the scrim is the <details>' own ::before, so a click on it lands on the element itself
    document.addEventListener("click", function (e) {
      if (!d.open) return;
      if (e.target === d || !d.contains(e.target)) close();
    });
    d.addEventListener("toggle", function () {
      document.documentElement.classList.toggle("menu-open", d.open);
      // opened by "/", the search box takes the focus; opened by hand, the first link does
      if (d.open && !d.hasAttribute("data-for-search")) { var f = $(".mp a", d); if (f) setTimeout(function () { f.focus(); }, 30); }
      d.removeAttribute("data-for-search");
    });
    // every link inside closes it, so the drawer never survives a same-page anchor
    $$(".mp a", d).forEach(function (a) { a.addEventListener("click", close); });
    if (matchMedia("(max-width: 640px)").matches) {
      $$(".mp details", d).forEach(function (g, i) { if (i > 1) g.open = false; });
    }
  }

  /* -------------------------------------------------------------------- tour */
  var steps = null, at = 0, ui = null, opener = null;

  function load() {
    var s = $("#tour-steps");
    if (!s) return null;
    try {
      return JSON.parse(s.textContent).filter(function (st) { return st && st.sel && pick(st.sel); });
    } catch (e) { return null; }
  }

  // A step's selector may match more than one thing, a lesson's guide and the folds that stand in for it
  // under 1280px: the first one on screen is shown, else the first.
  function pick(sel) {
    var all = $$(sel);
    return all.filter(function (e) { return e.getClientRects().length; })[0] || all[0];
  }

  function build() {
    ui = { spot: el("div", "tour-spot"), card: el("div", "tour-card") };
    ui.card.setAttribute("role", "dialog");
    ui.card.setAttribute("aria-live", "polite");
    ui.card.setAttribute("aria-label", "Walkthrough");
    ui.card.innerHTML = '<div class="tc-h"><span class="tc-l">The walkthrough</span><span class="tc-n"></span>' +
      '<button type="button" class="tc-x" aria-label="Close the walkthrough">×</button></div>' +
      '<h3 class="tc-t"></h3><p class="tc-b"></p>' +
      '<div class="tc-f"><button type="button" class="tc-prev">Back</button>' +
      '<button type="button" class="tc-next">Next</button></div>';
    document.body.appendChild(ui.spot);
    document.body.appendChild(ui.card);
    $(".tc-x", ui.card).addEventListener("click", end);
    $(".tc-prev", ui.card).addEventListener("click", function () { show(at - 1); });
    $(".tc-next", ui.card).addEventListener("click", function () {
      if (at >= steps.length - 1) end(); else show(at + 1);
    });
    document.addEventListener("keydown", onKey);
    window.addEventListener("resize", place);
    window.addEventListener("scroll", place, { passive: true });
    document.documentElement.classList.add("touring");
  }

  function onKey(e) {
    if (!ui) return;
    if (e.key === "Escape") end();
    else if (e.key === "ArrowRight" || e.key === "Enter") { if (at >= steps.length - 1) end(); else show(at + 1); }
    else if (e.key === "ArrowLeft") show(at - 1);
  }

  function show(n) {
    if (n < 0 || n >= steps.length) return;
    at = n;
    var st = steps[at], t = pick(st.sel);
    if (!t) { steps.splice(at, 1); if (!steps.length) return end(); return show(Math.min(at, steps.length - 1)); }
    // an element hidden inside a closed <details> is opened first, so the spotlight has something to show
    var d = t.closest("details");
    while (d) { if (!d.open && !d.classList.contains("menu")) d.open = true; d = d.parentElement && d.parentElement.closest("details"); }
    $(".tc-n", ui.card).textContent = (at + 1) + " of " + steps.length;
    $(".tc-t", ui.card).textContent = st.title;
    $(".tc-b", ui.card).innerHTML = st.body;
    $(".tc-prev", ui.card).disabled = at === 0;
    $(".tc-next", ui.card).textContent = at === steps.length - 1 ? "Done" : "Next";
    var r = t.getBoundingClientRect();
    var fixed = getComputedStyle(t).position === "fixed" || (t.closest(".hd") && r.top < 90);
    if (!fixed && (r.top < 90 || r.bottom > innerHeight - 40)) {
      // "instant", not "auto": auto defers to the page's smooth scroll-behavior, and a hidden
      // tab never finishes a smooth scroll
      var smooth = !reduce && !document.hidden;
      t.scrollIntoView({ block: "center", behavior: smooth ? "smooth" : "instant" });
      setTimeout(function () {
        var q = t.getBoundingClientRect();
        if (q.top < 90 || q.bottom > innerHeight - 40) t.scrollIntoView({ block: "center", behavior: "instant" });
        place();
      }, smooth ? 460 : 0);
    } else { place(); }
    setTimeout(function () { $(".tc-next", ui.card).focus({ preventScroll: true }); }, 60);
  }

  function place() {
    if (!ui || !steps) return;
    var t = pick(steps[at].sel);
    if (!t) return;
    var r = t.getBoundingClientRect(), pad = 8;
    var top = Math.max(r.top - pad, 4), left = Math.max(r.left - pad, 4);
    var w = Math.min(r.width + pad * 2, innerWidth - left - 4), h = Math.min(r.height + pad * 2, innerHeight - top - 4);
    ui.spot.style.top = top + "px"; ui.spot.style.left = left + "px";
    ui.spot.style.width = w + "px"; ui.spot.style.height = h + "px";
    var cw = ui.card.offsetWidth, ch = ui.card.offsetHeight;
    var below = top + h + 14, above = top - ch - 14;
    var y = below + ch <= innerHeight - 12 ? below : (above >= 12 ? above : Math.max(12, innerHeight - ch - 12));
    ui.card.classList.toggle("above", y < top);
    var x = Math.min(Math.max(left, 16), innerWidth - cw - 16);
    ui.card.style.top = y + "px"; ui.card.style.left = Math.max(8, x) + "px";
  }

  function start(from) {
    if (ui) return;
    steps = steps || load();
    if (!steps || !steps.length) return;
    opener = from || document.activeElement;
    build();
    show(0);
  }

  function end() {
    if (!ui) return;
    ui.spot.remove(); ui.card.remove(); ui = null;
    document.removeEventListener("keydown", onKey);
    window.removeEventListener("resize", place);
    window.removeEventListener("scroll", place);
    document.documentElement.classList.remove("touring");
    if (opener && opener.focus) opener.focus({ preventScroll: true });
  }

  /* A page with a walkthrough shows its way in, in the drawer, and nothing else: nothing pops up on
     arrival and nothing floats over the page. A reader who came for the page gets the page. */
  function offer() {
    steps = load();
    if (!steps || !steps.length) return;
    document.documentElement.classList.add("has-tour");   // the drawer shows its own way in to the walkthrough
  }

  function wireTour() {
    $$("[data-tour-start]").forEach(function (b) {
      b.addEventListener("click", function () {
        var m = b.closest("details.menu");            // started from the drawer: the drawer steps aside first
        if (m) m.removeAttribute("open");
        start(b);
      });
    });
    offer();
  }

  /* ------------------------------------------------------------------ search */
  /* The drawer's search box looks through search.json: every lesson, step, model and
     page, one line each. Fetched on first focus, never before. "/" opens it. */
  function wireSearch() {
    var input = $("[data-search]");
    var list = $("[data-search-results]");
    if (!input || !list) return;
    var base = input.getAttribute("data-index").replace(/search\.json$/, "");
    var rows = null, timer = null;
    function load() {
      if (rows) return Promise.resolve(rows);
      return fetch(input.getAttribute("data-index")).then(function (r) { return r.json(); })
        .then(function (j) { rows = j; return rows; }).catch(function () { rows = []; return rows; });
    }
    function href(u) { return /^https?:/.test(u) ? u : base + u; }
    function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    function run() {
      var q = input.value.trim().toLowerCase();
      if (q.length < 2) { list.hidden = true; list.innerHTML = ""; return; }
      load().then(function (all) {
        var terms = q.split(/\s+/);
        var hits = all.map(function (r) {
          var t = r.t.toLowerCase(), d = (r.d || "").toLowerCase(), k = (r.k || "").toLowerCase();
          var score = 0;
          for (var i = 0; i < terms.length; i++) {
            var w = terms[i];
            if (t.indexOf(w) === 0) score += 6; else if (t.indexOf(w) >= 0) score += 4;
            else if (k.indexOf(w) >= 0) score += 2; else if (d.indexOf(w) >= 0) score += 1;
            else return null;
          }
          return { r: r, s: score };
        }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 8);
        list.hidden = false;
        list.innerHTML = hits.length ? hits.map(function (h) {
          return '<li><a href="' + esc(href(h.r.u)) + '"><span>' + esc(h.r.k) + "</span><b>" + esc(h.r.t) + "</b>" +
            (h.r.d ? "<small>" + esc(h.r.d) + "</small>" : "") + "</a></li>";
        }).join("") : '<li class="none">Nothing matches. Try one word, or a phase like "P2".</li>';
      });
    }
    input.addEventListener("focus", function () { load(); });
    input.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(run, 70); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { var a = $("a", list); if (a) { e.preventDefault(); location.href = a.href; } }
      if (e.key === "Escape") { input.value = ""; run(); }
      if (e.key === "ArrowDown") { var f = $("a", list); if (f) { e.preventDefault(); f.focus(); } }
    });
    list.addEventListener("keydown", function (e) {
      var items = $$("a", list), i = items.indexOf(document.activeElement);
      if (e.key === "ArrowDown" && i < items.length - 1) { e.preventDefault(); items[i + 1].focus(); }
      if (e.key === "ArrowUp") { e.preventDefault(); (i > 0 ? items[i - 1] : input).focus(); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key !== "/" || e.metaKey || e.ctrlKey || e.altKey) return;
      var tag = (document.activeElement && document.activeElement.tagName || "").toLowerCase();
      if (tag === "input" || tag === "textarea" || tag === "select" || document.activeElement.isContentEditable) return;
      var d = $("[data-menu]"); if (!d) return;
      e.preventDefault(); d.setAttribute("data-for-search", ""); d.open = true; setTimeout(function () { input.focus(); }, 40);
    });
  }

  /* ------------------------------------------------------------ the top bar */
  /* Roles and Library are each a <details>: they open without script. This closes one when the
     other opens, on Esc, and on a click anywhere else. */
  function wireDrops() {
    var dds = $$("[data-dd]");
    if (!dds.length) return;
    var shut = function (but) { dds.forEach(function (d) { if (d !== but) d.open = false; }); };
    dds.forEach(function (d) {
      d.addEventListener("toggle", function () { if (d.open) shut(d); });
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest || !e.target.closest("[data-dd]")) shut(null);
    });
    // tabbing out of a list closes it, so it is never left open behind the focus
    dds.forEach(function (d) {
      d.addEventListener("focusout", function (e) {
        if (d.open && e.relatedTarget && !d.contains(e.relatedTarget)) d.open = false;
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      dds.forEach(function (d) { if (d.open) { d.open = false; $("summary", d).focus(); } });
    });
  }

  /* The tutorial's lesson list, and a lesson's two folds under its meta line, are open in the HTML so they
     work without script. On a phone the list starts closed, and under 1280px, where a lesson has no guide
     beside it, the two folds do, side by side, so the lesson itself is the first thing on screen. */
  function foldOnPhones() {
    if (!window.matchMedia) return;
    var shut = function (d) { d.removeAttribute("open"); };
    if (matchMedia("(max-width: 900px)").matches) $$(".lnav").forEach(shut);
    if (matchMedia("(max-width: 1279px)").matches) $$(".lfolds details").forEach(shut);
  }

  /* A lesson's course list opens on the lesson you are on: in the guide its own scroll is set, once, with
     no motion; under the meta line the page goes to it, as the folded rail did on a phone. */
  function wireCourse() {
    $$(".lguide details, .lfolds details").forEach(function (d) {
      d.addEventListener("toggle", function () {
        var cur = d.open && $(".ll[aria-current]", d), box = d.closest(".lguide");
        if (!cur) return;
        if (!box) cur.scrollIntoView({ block: "center" });
        else if (box.scrollHeight > box.clientHeight + 4) {
          box.scrollTop += cur.getBoundingClientRect().top - box.getBoundingClientRect().top - box.clientHeight / 2;
        }
      });
    });
  }

  /* On a short screen a long guide scrolls inside itself, so it keeps the section being read (marked by
     site.js) in its view; the page itself never moves. With the course open, the reader is browsing it. */
  function keepMark() {
    var g = $(".lguide");
    if (!g || !window.MutationObserver) return;
    new MutationObserver(function () {
      var a = $(".rl[aria-current]", g);
      if (!a || $("details[open]", g) || g.scrollHeight <= g.clientHeight + 4) return;
      var r = a.getBoundingClientRect(), b = g.getBoundingClientRect();
      if (r.top < b.top) g.scrollTop -= b.top - r.top + 8;
      else if (r.bottom > b.bottom) g.scrollTop += r.bottom - b.bottom + 8;
    }).observe(g, { subtree: true, attributes: true, attributeFilter: ["aria-current"] });
  }

  function init() { foldOnPhones(); wireCourse(); keepMark(); wireMenu(); wireDrops(); wireTour(); wireSearch(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
