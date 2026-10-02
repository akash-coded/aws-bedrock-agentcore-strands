/* The labs: one engine, one script per lab.

   A lab is a bench. On the left, the work, one beat after another: you assemble a prompt from parts, run it,
   read the recorded reply, mark what is wrong in it, make a call. On the right, the document you are making,
   which grows as you go and shows what changed last. The script is the JSON in #lab-data, written by
   site/pages/labs.py from site/content/labs/<slug>.py. No model is called, and the one thing ever fetched is the
   page of other models' recorded replies, when the debrief's fold for them is opened.

   A reply is a recording: a real model's answer to that exact prompt, saved when the lab was written, with
   the model's name and the date on it. It appears at once; nothing pretends to be typing.

   The page is rebuilt from the list of what the player has done (state.picks), the way the game replays its
   moves, so a reload, a link and "start again" all go through the same code. Without script the page shows
   the same lab as a document to read (the .lab-plain section), and this file leaves it alone.

   Beat kinds: note (read, go on), compose (assemble a prompt from parts, run it), run (a recorded reply to
   read), mark (a recorded reply to mark the faults in), choose (a call), compare (the same thing in two or
   three forms, pick one), file (the document joins the pack). A compose beat whose parts include some marked
   "user" sends those as the message and the rest as its system prompt, and shows and copies the two apart. */
(function () {
  "use strict";
  var src = document.getElementById("lab-data"), root = document.getElementById("lab");
  if (!src || !root) return;
  var L;
  try { L = JSON.parse(src.textContent); } catch (e) { return; }
  var KEY = "skyways.lab." + L.slug, PACK = "skyways.labs.pack", V = L.v || 1;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------ small things */
  function el(tag, cls, html) { var n = document.createElement(tag); if (cls) n.className = cls; if (html != null) n.innerHTML = html; return n; }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  // a little markdown for the lab's own words: **bold**, `code`, blank line = paragraph, "- " = list item
  function rich(s) {
    var inline = function (t) { return esc(t).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/`([^`]+)`/g, "<code>$1</code>"); };
    return String(s || "").trim().split(/\n\s*\n/).map(function (block) {
      var lines = block.split("\n");
      if (lines.every(function (l) { return /^- /.test(l); })) return "<ul>" + lines.map(function (l) { return "<li>" + inline(l.slice(2)) + "</li>"; }).join("") + "</ul>";
      return "<p>" + inline(lines.join(" ")) + "</p>";
    }).join("");
  }
  function load() { try { var s = JSON.parse(localStorage.getItem(KEY) || "null"); return s && s.v === V && s.picks ? s : null; } catch (e) { return null; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* a private window: the lab still plays */ } }
  var state = load() || { v: V, picks: {} };

  /* ------------------------------------------------------------------ what the script says, given the picks */
  function holds(when) {                         // {"p1.gaps": "flag", "c2": ["a", "b"]}: every condition must hold
    if (!when) return true;
    return Object.keys(when).every(function (k) {
      var parts = k.split("."), v = state.picks[parts[0]];
      if (v && parts[1]) v = v[parts[1]];
      var want = when[k];
      return Array.isArray(want) ? want.indexOf(v) >= 0 : v === want;
    });
  }
  function beats() { return L.beats.filter(function (b) { return holds(b.when); }); }
  function done(b) {
    var p = state.picks[b.id];
    if (b.kind === "note" || b.kind === "run") return p === true;
    if (b.kind === "mark" || b.kind === "grid" || b.kind === "zoom") return !!(p && p.checked);
    if (b.kind === "compose") return !!(p && p.ran);
    return p != null;
  }
  function replyFor(run) {                       // which recording a run shows: decided by the prompt that was assembled
    var c = state.picks[run.of] || {}, map = run.reply, k;
    if (typeof map === "string") return map;
    for (k in map) {
      if (k === "*") continue;
      if (k.split(",").every(function (cond) { var kv = cond.split("="); return c[kv[0]] === kv[1]; })) return map[k];
    }
    return map["*"];
  }
  function beatById(id) { return L.beats.filter(function (x) { return x.id === id; })[0]; }
  function markReply(b) { return L.replies[b.doc || (b.reply ? replyFor(b) : replyFor(beatById(b.of)))]; }   // the recording a mark beat is about
  function optionOf(b, id) { return (b.options || b.cols || []).filter(function (o) { return o.id === id; })[0]; }
  // the prompt a compose beat assembles; where the beat sends a message with it (parts marked "user"), the system prompt
  function promptText(b, user) {
    var c = state.picks[b.id] || {};
    return b.parts.filter(function (p) { return !p.user === !user; }).map(function (p) {
      if (p.file) return (p.lead || "") + fileBody(p.file);
      if (p.text != null) return p.text;
      var o = p.options.filter(function (x) { return x.id === (c[p.id] || p.options[0].id); })[0];
      return o.text;
    }).filter(function (t) { return t; }).join("\n\n");
  }
  function messageText(b) { return promptText(b, true); }
  function twoPart(b) { return b.parts.some(function (p) { return p.user; }); }

  /* ------------------------------------------------------------------ the document being made */
  function artefact(upto) {                       // replay every patch of every finished beat, in order
    var secs = L.artefact.sections.map(function (s) { return { id: s.id, head: s.head, body: s.body || "", state: s.state || "empty" }; });
    var version = 0, last = [];
    function apply(patches) {
      if (!patches || !patches.length) return;
      last = [];
      patches.forEach(function (p) {
        if (p.version != null) { version = p.version; return; }
        var s = secs.filter(function (x) { return x.id === p.id; })[0];
        if (!s) return;
        if (p.body != null) s.body = p.body;
        if (p.state) s.state = p.state;
        last.push(s.id);
      });
    }
    upto.forEach(function (b) {
      if (!done(b)) return;
      apply(b.patch);
      var p = state.picks[b.id];
      if (b.kind === "choose" || b.kind === "compare") { var o = optionOf(b, p); if (o) apply(o.patch); }
      if (b.kind === "run") { var r = L.replies[replyFor(b)]; if (r) apply(r.patch); }
      if (b.kind === "mark") { var m = markReply(b); if (m) apply(m.patch); }
    });
    return { sections: secs, version: version, last: last };
  }
  function artefactText(a) {
    return a.sections.filter(function (s) { return s.body; }).map(function (s) { return (s.head ? s.head + "\n" : "") + s.body; }).join("\n\n") + "\n";
  }

  /* ------------------------------------------------------------------ drawing one beat */
  var KIND = { note: "", compose: "Prompt", run: "Recorded reply", mark: "Your read", choose: "Your call", compare: "Your call", grid: "Test run", zoom: "Diagram", file: "File it" };
  function stamp(r) { return "Recorded reply · " + esc(r.model) + " · " + esc(r.date) + " · not live, yours will differ"; }
  function whole(r) {
    return r.full ? '<details class="lab-whole"><summary>The whole reply (' + r.full.length + " lines; this is part of it)</summary><div class=\"lab-lines\">" +
      r.full.map(function (ln) { return '<div class="lab-ln' + (ln.h ? " h" : "") + (ln.t === "" ? " gap" : "") + '">' + esc(ln.t) + "</div>"; }).join("") + "</div></details>" : "";
  }
  function lines(r, b, live) {                    // a reply as lines; in a live mark beat each line is a button
    var p = (b && state.picks[b.id]) || { marked: [] }, checked = p.checked;
    return '<div class="lab-lines">' + r.lines.map(function (ln, i) {
      var on = p.marked && p.marked.indexOf(i) >= 0, cls = "lab-ln" + (ln.h ? " h" : "") + (ln.t === "" ? " gap" : "");
      if (!b || ln.t === "" || ln.h) return '<div class="' + cls + '">' + esc(ln.t) + "</div>";
      if (checked) {
        var verdict = ln.flag ? (on ? " hit" : " missed") : (on ? " false" : "");
        return '<div class="' + cls + verdict + '"><span>' + esc(ln.t) + "</span>" + (ln.flag || on ? '<small>' + esc(ln.flag ? (on ? "Caught. " : "Missed. ") + ln.why : "This one is sound. " + (ln.why || "")) + "</small>" : "") + "</div>";
      }
      return live ? '<button type="button" class="' + cls + '" data-ln="' + i + '" aria-pressed="' + (on ? "true" : "false") + '">' + esc(ln.t) + "</button>"
                  : '<div class="' + cls + '">' + esc(ln.t) + "</div>";
    }).join("") + "</div>";
  }
  function draw(b, live, n) {
    // a finished beat is "past", not "done": the site's base.css draws any .done as a green flex row, and a beat
    // that took it laid its heading, its words and its prompt side by side, too narrow on a desktop, wider than a phone
    var p = state.picks[b.id], card = el("section", "lab-beat k-" + b.kind + (live ? " live" : " past")), h = "", r, o;
    card.setAttribute("data-beat", b.id);
    if (b.move) h += '<h2 class="lab-move"><span>' + n + "</span>" + esc(b.move) + "</h2>";
    if (KIND[b.kind]) h += '<p class="lab-k">' + KIND[b.kind] + "</p>";
    if (b.say) h += '<div class="lab-say">' + rich(b.say) + "</div>";
    if (b.kind === "note") {
      if (live) h += '<p class="lab-go"><button type="button" class="btn pri" data-act="ok">' + esc(b.button || "Go on") + "</button></p>";
    } else if (b.kind === "compose") {
      var c = p || {}, two = twoPart(b), was = null;
      h += '<div class="lab-prompt"><p class="lab-ph">' + esc(b.title) + (b.attach ? '<span>' + b.attach.map(function (f) { return esc(fileName(f)); }).join(", ") + " attached</span>" : "") + "</p>";
      b.parts.forEach(function (part) {
        if (two && !!part.user !== was) { was = !!part.user; h += '<p class="lab-to">' + (was ? "Message" : "System prompt") + "</p>"; }   // labs.py TO
        if (part.file) { h += '<pre class="lab-part file">' + esc((part.lead || "").trim()) + (part.lead ? " " : "") + "[ " + esc(fileName(part.file)) + ", in full ]</pre>"; return; }
        if (part.text != null) { h += '<pre class="lab-part">' + esc(part.text) + "</pre>"; return; }
        var cur = c[part.id] || (live ? null : part.options[0].id);
        h += '<fieldset class="lab-slot"' + (live ? "" : " disabled") + '><legend>' + esc(part.label) + "</legend>" + part.options.map(function (op) {
          return '<label><input type="radio" name="' + b.id + "-" + part.id + '" value="' + op.id + '"' + (cur === op.id ? " checked" : "") + "><span>" + esc(op.label) + "</span></label>";
        }).join("") + "</fieldset>";
        var chosen = part.options.filter(function (x) { return x.id === cur; })[0];
        h += '<pre class="lab-part pick' + (chosen ? "" : " none") + '" data-part="' + part.id + '">' + (chosen ? esc(chosen.text || "(nothing added)") : "Choose one above.") + "</pre>";
      });
      h += "</div>";
      if (live) h += '<p class="lab-go"><button type="button" class="btn pri" data-act="run">' + esc(b.button || "Run this prompt") + "</button>" +
        (two ? '<button type="button" class="lab-copy" data-act="copy">Copy the system prompt</button><button type="button" class="lab-copy" data-act="copy-msg">Copy the message</button>'
             : '<button type="button" class="lab-copy" data-act="copy">Copy the prompt</button>') + "</p>";
    } else if (b.kind === "run") {
      r = L.replies[replyFor(b)];
      h += '<div class="lab-reply"><p class="lab-stamp">' + stamp(r) + "</p>" + lines(r, null, false) + whole(r) + "</div>";
      if (r.after) h += '<div class="lab-say">' + rich(r.after) + "</div>";
      if (live) h += '<p class="lab-go"><button type="button" class="btn pri" data-act="ok">' + esc(b.button || "Go on") + "</button></p>";
    } else if (b.kind === "mark") {
      r = markReply(b);
      h += '<p class="lab-ask">' + esc(b.ask) + "</p>";
      h += '<div class="lab-reply mark"><p class="lab-stamp">' + stamp(r) + "</p>" + lines(r, b, live) + whole(r) + "</div>";
      if (p && p.checked) {
        var flagged = r.lines.filter(function (ln) { return ln.flag; }).length;
        var hit = r.lines.filter(function (ln, i) { return ln.flag && p.marked.indexOf(i) >= 0; }).length;
        h += '<p class="lab-score"><b>' + hit + " of " + flagged + "</b> caught." + (p.marked.length > hit ? " " + (p.marked.length - hit) + " marked that were sound." : "") + "</p>";
        if (r.read) h += '<div class="lab-say">' + rich(r.read) + "</div>";
      } else if (live) h += '<p class="lab-go"><button type="button" class="btn pri" data-act="check">Check my marks</button></p>';
    } else if (b.kind === "choose" || b.kind === "compare") {
      h += '<p class="lab-ask">' + esc(b.ask) + "</p>";
      if (b.kind === "compare") {
        h += '<div class="lab-cols">' + b.cols.map(function (col) {
          return '<div class="lab-col' + (p === col.id ? " on" : "") + '"><p class="lab-ph">' + esc(col.label) + '</p><pre class="lab-part">' + esc(col.body) + "</pre>" +
            (col.reply ? '<div class="lab-reply"><p class="lab-stamp">' + stamp(L.replies[col.reply]) + "</p>" + lines(L.replies[col.reply], null, false) + whole(L.replies[col.reply]) + "</div>" : "") +
            (live ? '<button type="button" class="btn" data-opt="' + col.id + '">' + esc(col.pick || "Use this one") + "</button>" : "") + "</div>";
        }).join("") + "</div>";
      } else {
        h += '<div class="lab-opts">' + b.options.map(function (op) {
          return '<button type="button" class="lab-opt' + (p === op.id ? " on" : "") + '" data-opt="' + op.id + '"' + (live ? "" : " disabled") + "><b>" + esc(op.label) + "</b>" + (op.detail ? "<span>" + esc(op.detail) + "</span>" : "") + "</button>";
        }).join("") + "</div>";
      }
      o = p != null && optionOf(b, p);
      if (o && o.after) h += '<div class="lab-after' + (o.right ? " ok" : o.right === false ? " no" : "") + '">' + rich(o.after) + "</div>";
    } else if (b.kind === "file") {
      var a = artefact(beats());
      h += '<div class="lab-file"><p><b>' + esc(L.artefact.name) + "</b> is ready: " + a.sections.filter(function (s) { return s.state === "decided"; }).length + " of " + a.sections.length + " parts decided by a person.</p>" +
        (live ? '<p class="lab-go"><button type="button" class="btn pri" data-act="file">Add it to your pack</button><button type="button" class="btn" data-act="download">Download ' + esc(L.artefact.name) + "</button></p>"
              : '<p class="lab-filed">Filed in your pack on this device. <button type="button" class="lab-copy" data-act="download">Download ' + esc(L.artefact.name) + "</button></p>") + "</div>";
    }
    card.innerHTML = h;
    return card;
  }
  // what is on the desk: the files the lab starts with, and any a finished beat has handed over
  function desk() {
    var out = (L.files || []).slice();
    beats().forEach(function (b) { if (done(b) && b.gives) out = out.concat(b.gives); });
    return out;
  }
  function allFiles() { var out = (L.files || []).slice(); L.beats.forEach(function (b) { if (b.gives) out = out.concat(b.gives); }); return out; }
  function fileName(id) { var f = allFiles().filter(function (x) { return x.id === id; })[0]; return f ? f.name : id; }
  function fileBody(id) { var f = allFiles().filter(function (x) { return x.id === id; })[0]; return f ? f.body : ""; }

  /* ------------------------------------------------------------------ the whole bench */
  var bench = el("div", "lab-bench"), side = el("aside", "lab-side"), firstRender = true;
  side.setAttribute("aria-label", "The document you are making");
  root.appendChild(bench); root.appendChild(side);
  function render(focusNew) {
    var all = beats(), shown = [], i, move = 0;
    for (i = 0; i < all.length; i++) { shown.push(all[i]); if (!done(all[i])) break; }
    var finished = shown.length === all.length && done(all[all.length - 1]);
    bench.innerHTML = "";
    shown.forEach(function (b, k) {
      if (b.move) move++;
      bench.appendChild(draw(b, k === shown.length - 1 && !done(b), move));
    });
    if (finished) bench.appendChild(debrief());
    var foot = el("p", "lab-foot", '<span>' + shown.filter(done).length + " of " + all.length + " steps</span>" + (Object.keys(state.picks).length ? '<button type="button" class="lab-copy" data-act="reset">Start again</button>' : ""));
    bench.appendChild(foot);
    drawSide(artefact(shown));
    root.setAttribute("data-done", finished ? "1" : "0");
    if (focusNew && !firstRender) {
      var cur = bench.querySelector(".lab-beat.live") || bench.querySelector(".lab-debrief") || bench.lastElementChild;
      if (cur) {                                   // the answer to the press: the next step comes into view and takes the focus
        cur.setAttribute("tabindex", "-1");
        cur.focus({ preventScroll: true });
        var top = cur.getBoundingClientRect().top;
        if (top > innerHeight * 0.55 || top < 80) window.scrollTo({ top: window.scrollY + top - 96, behavior: reduce ? "auto" : "smooth" });
      }
    }
    firstRender = false;
  }
  function drawSide(a) {
    var decided = a.sections.filter(function (s) { return s.state === "decided"; }).length;
    var chips = (L.artefact.versions || []).map(function (v, i) { return '<li class="' + (i === a.version ? "on" : i < a.version ? "was" : "") + '">' + esc(v) + "</li>"; }).join("");
    var wasOpen = side.querySelector("details") ? side.querySelector("details").open : window.matchMedia("(min-width: 1001px)").matches;
    side.innerHTML = '<details class="lab-doc"' + (wasOpen ? " open" : "") + '><summary><b>' + esc(L.artefact.name) + "</b><span>" + decided + " of " + a.sections.length + " decided</span></summary>" +
      (chips ? '<ol class="lab-ver" aria-label="Versions of this document">' + chips + "</ol>" : "") +
      '<div class="lab-page">' + a.sections.map(function (s) {
        var body = s.body || (s.state === "empty" ? "(empty)" : "");
        return '<div class="lab-sec s-' + s.state + (a.last.indexOf(s.id) >= 0 ? " new" : "") + '"><p class="lab-sh">' + esc(s.head) + '<i>' + ({ decided: "decided", guessed: "the model's guess", open: "not decided", draft: "draft", empty: "" })[s.state] + "</i></p><pre>" + esc(body) + "</pre></div>";
      }).join("") + "</div>" +
      (desk().length ? '<div class="lab-desk"><p>On the desk</p>' + desk().map(function (f) {
        return "<details><summary>" + esc(f.name) + (f.note ? "<span>" + esc(f.note) + "</span>" : "") + "</summary><pre>" + esc(f.body) + "</pre></details>";
      }).join("") + "</div>" : "") + "</details>";
  }
  function debrief() {
    var d = L.debrief, box = el("section", "lab-debrief");
    var calls = beats().filter(function (b) { return (b.kind === "choose" || b.kind === "compare") && optionOf(b, state.picks[b.id]) && optionOf(b, state.picks[b.id]).right != null; });
    var right = calls.filter(function (b) { return optionOf(b, state.picks[b.id]).right; }).length;
    var marks = beats().filter(function (b) { return b.kind === "mark"; }), hit = 0, flagged = 0;
    marks.forEach(function (b) {
      var r = markReply(b), p = state.picks[b.id];
      r.lines.forEach(function (ln, i) { if (ln.flag) { flagged++; if (p.marked.indexOf(i) >= 0) hit++; } });
    });
    box.innerHTML = '<p class="lab-k">What this lab was about</p><h2>' + esc(d.title) + "</h2>" + rich(d.trap) +
      '<p class="lab-tally">' + (flagged ? "You caught <b>" + hit + " of " + flagged + "</b> faults in the replies. " : "") + (calls.length ? "<b>" + right + " of " + calls.length + "</b> calls matched the book." : "") + "</p>" +
      '<h3>The habit to keep</h3>' + rich(d.habit) +
      (d.tool ? '<h3>' + esc(d.tool.title) + "</h3>" + rich(d.tool.body) + (d.tool.checked ? '<p class="lab-checked">Tool facts checked on ' + esc(d.tool.checked) + ".</p>" : "") : "") +
      (d.others ? "<h3>" + esc(d.others.title) + '</h3><div class="lab-others-at"></div>' : "") +
      '<p class="lab-next">' + (d.links || []).map(function (l, i) { return '<a class="' + (i ? "more" : "btn pri") + '" href="' + esc(l[1]) + '">' + esc(l[0]) + (i ? ' <i aria-hidden="true">→</i>' : "") + "</a>"; }).join("") + "</p>";
    others(box);
    return box;
  }
  // Other models' replies to the same prompts (debrief.others). The part is drawn once, in the reading version, and
  // copied here. The replies live on a page of their own; the fold reads them in from it the first time it is
  // opened, and if that fails its link to the page stays.
  var othersReplies = null;
  function others(box) {
    var at = box.querySelector(".lab-others-at"), part = document.querySelector(".lab-plain .lab-others");
    if (!at) return;
    if (!part) { at.remove(); return; }
    var copy = part.cloneNode(true), fold = copy.querySelector("details[data-src]");
    at.replaceWith(copy);
    if (!fold) return;
    fold.addEventListener("toggle", function () {
      var list = fold.querySelector(".lab-others-list");
      if (!fold.open || !list) return;
      othersReplies = othersReplies || fetch(fold.getAttribute("data-src")).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then(function (html) { var n = new DOMParser().parseFromString(html, "text/html").querySelector(".lab-others-replies"); if (!n) throw new Error("no replies"); return n; });
      othersReplies.then(function (n) { if (list.parentNode) list.replaceWith(document.importNode(n, true)); }, function () { othersReplies = null; });
    });
  }

  /* ------------------------------------------------------------------ what the player does */
  function current() { var all = beats(), i; for (i = 0; i < all.length; i++) if (!done(all[i])) return all[i]; return null; }
  function copy(text, btn) {
    var ok = function () { var was = btn.textContent; btn.textContent = "Copied"; setTimeout(function () { btn.textContent = was; }, 1400); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, function () {}); else {
      var t = el("textarea"); t.value = text; document.body.appendChild(t); t.select(); try { document.execCommand("copy"); ok(); } catch (e) { /* no clipboard */ } t.remove();
    }
  }
  bench.addEventListener("change", function (e) {
    var b = current(), inp = e.target;
    if (!b || b.kind !== "compose" || inp.type !== "radio") return;
    var part = inp.name.slice(b.id.length + 1), p = state.picks[b.id] || (state.picks[b.id] = {});
    p[part] = inp.value; save();
    var pre = bench.querySelector('.lab-beat.live [data-part="' + part + '"]');
    var op = b.parts.filter(function (x) { return x.id === part; })[0].options.filter(function (x) { return x.id === inp.value; })[0];
    if (pre) { pre.textContent = op.text || "(nothing added)"; pre.classList.remove("none"); }
  });
  bench.addEventListener("click", function (e) {
    var t = e.target.closest("[data-act],[data-opt],[data-ln]"), b = current();
    if (!t) return;
    var act = t.getAttribute("data-act");
    if (act === "reset") { state = { v: V, picks: {} }; save(); render(false); window.scrollTo({ top: 0, behavior: "auto" }); return; }
    if (act === "download") { download(); return; }
    if (!b) return;
    if (t.hasAttribute("data-ln") && b.kind === "mark") {
      var p = state.picks[b.id] || (state.picks[b.id] = { marked: [] }), i = +t.getAttribute("data-ln"), at = p.marked.indexOf(i);
      if (at >= 0) p.marked.splice(at, 1); else p.marked.push(i);
      t.setAttribute("aria-pressed", at >= 0 ? "false" : "true"); save(); return;
    }
    if (t.hasAttribute("data-opt") && (b.kind === "choose" || b.kind === "compare")) { state.picks[b.id] = t.getAttribute("data-opt"); save(); render(true); return; }
    if (act === "ok") { state.picks[b.id] = true; save(); render(true); return; }
    if (act === "copy" && b.kind === "compose") { copy(promptText(b), t); return; }
    if (act === "copy-msg" && b.kind === "compose") { copy(messageText(b), t); return; }
    if (act === "run" && b.kind === "compose") {
      var c = state.picks[b.id] || (state.picks[b.id] = {});
      var missing = b.parts.filter(function (x) { return x.options && !c[x.id]; });
      if (missing.length) {                       // every slot is a decision: none is made for the player
        var fs = bench.querySelector('.lab-beat.live input[name="' + b.id + "-" + missing[0].id + '"]');
        if (fs) { fs.closest("fieldset").classList.add("need"); fs.focus(); }
        return;
      }
      c.ran = true;
      save(); render(true); return;
    }
    if (act === "check" && b.kind === "mark") { (state.picks[b.id] || (state.picks[b.id] = { marked: [] })).checked = true; save(); render(true); return; }
    if (act === "file" && b.kind === "file") {
      state.picks[b.id] = true; save();
      try {
        var pack = JSON.parse(localStorage.getItem(PACK) || "{}");
        pack[L.slug] = { name: L.artefact.name, title: L.title, body: artefactText(artefact(beats())), when: new Date().toISOString().slice(0, 10) };
        localStorage.setItem(PACK, JSON.stringify(pack));
      } catch (err) { /* no storage: the download still works */ }
      render(true); return;
    }
  });
  function download() {
    var blob = new Blob([artefactText(artefact(beats()))], { type: "text/markdown" }), a = el("a");
    a.href = URL.createObjectURL(blob); a.download = L.artefact.name; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
  }

  root.hidden = false;
  document.documentElement.classList.add("lab-on");
  render(false);
  // for the tests: the script, the state and a way to read what a run would show
  window.Lab = { data: L, state: function () { return state; }, beats: beats, current: current, replyFor: replyFor,
                 artefact: function () { return artefact(beats()); }, prompt: function (id) { return promptText(beatById(id)); },
                 message: function (id) { return messageText(beatById(id)); } };
})();
