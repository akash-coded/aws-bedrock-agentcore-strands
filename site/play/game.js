/* Ninety Days · the page.
   Everything a player reads or presses is real text and real buttons in the page. The two canvases are
   decoration and state: the room where today happens, and the whole building. Nothing here decides
   anything: the rules are in sim.js, and this file only asks them what is legal and shows the answer.

   A save is the list of actions taken, kept under one key in localStorage and replayed on load. */
(function () {
  "use strict";
  var src = document.getElementById("nd-data"), root = document.getElementById("nd");
  if (!src || !root || !window.ND || !window.NDArt) return;
  var data = JSON.parse(src.textContent), sim = window.ND.sim, A = window.NDArt;
  var KEY = "skyways.ninety", BEST = "skyways.ninety.best";
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var UP = root.getAttribute("data-up") || "../";

  /* ------------------------------------------------------------------ small things */
  function el(tag, attrs, kids) {
    var n = document.createElement(tag), k;
    for (k in attrs || {}) {
      if (attrs[k] == null || attrs[k] === false) continue;
      if (k === "text") n.textContent = attrs[k];
      else if (k === "html") n.innerHTML = attrs[k];
      else if (k.slice(0, 2) === "on") n.addEventListener(k.slice(2), attrs[k]);
      else n.setAttribute(k, attrs[k] === true ? "" : attrs[k]);
    }
    (kids || []).forEach(function (c) { if (c != null) n.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return n;
  }
  function days(n) { return n === 1 ? "1 day" : n + " days"; }
  function lower(s) { return /^[A-Z]{2}/.test(s) ? s : s.charAt(0).toLowerCase() + s.slice(1); }      // "QA lead" keeps its capitals
  function money(n) { return (n < 0 ? "−$" : "$") + Math.abs(n).toLocaleString("en-US"); }
  function who(key) { return data.cast[key] || { name: key }; }
  function load() { try { var s = JSON.parse(localStorage.getItem(KEY) || "null"); return s && s.v === data.v && Array.isArray(s.history) && s.opts && typeof s.opts === "object" ? s : null; } catch (e) { return null; } }
  function save() { try { if (run) localStorage.setItem(KEY, JSON.stringify({ v: data.v, opts: run.opts, history: run.state.history })); } catch (e) { /* play on in memory */ } }
  function clearSave() { try { localStorage.removeItem(KEY); } catch (e) { /* nothing to clear */ } }
  function best() { try { return JSON.parse(localStorage.getItem(BEST) || "null"); } catch (e) { return null; } }
  var RANK = { stopped: 0, paused: 1, conditional: 2, funded: 3 };

  var run = null;                 // { opts, state }
  var looking = null, lastRoom = null;   // the room whose card is open, and the chip last pressed
  var asking = false;             // a colleague's call is being challenged
  var live = el("p", { "class": "vh", "aria-live": "polite", role: "status" });

  /* ------------------------------------------------------------------ the stage: two canvases */
  var sceneCv = el("canvas", { "class": "nd-scene-cv", "aria-hidden": "true" });
  var mapCv = el("canvas", { "class": "nd-map-cv", "aria-hidden": "true" });
  var MAPW = A.BW + 10, MAPH = A.BH + 22, clock = 0, raf = 0, last = 0, planeT = -1, paused = false, seen = true;
  var enter = 1, shut = 0, flash = 0;      // people walking in, the build floors' shutters, the incident's one hard frame
  window.NDFrames = 0;            // for the acceptance gate: frames drawn by the loop

  function picture(state) {       // what the walls show: the game's state, as the art module reads it
    var i = state ? state.i : 0, st = {};
    st.day = state ? data.days[Math.min(i, data.days.length - 1)].day : 1; st.dayIndex = i;
    if (!state) { st.notes = 12; st.boxes = 3; st.bolts = 4; st.cancelled = 3; st.bill = 1; return st; }
    st.notes = sim.has(state, "register") ? 12 : (i > 0 ? 24 : 16);
    st.boxes = sim.has(state, "records") ? 3 : 0; if (sim.has(state, "matrix")) st.boxes = 5;
    st.bolts = i >= 7 ? Math.min(14, (i - 6) * 2 + (sim.has(state, "skeleton") ? 2 : 0)) : 0;
    if (i >= 8) { st.score = 0.824; st.bar = 0.8; st.lower = sim.has(state, "proof") ? 0.791 : 0; st.slices = state.live ? 3 : 0; }
    st.bill = i >= 10 ? (state.bill || (state.flags.billOpen ? 3.4 : 4.4)) : 1.2;
    st.cancelled = i >= 9 && !state.flags.frozen ? 1 : 3;
    if (state.beat === "end" || i === 12) { var l = sim.ledger(data, state); st.value = Math.min(1, l.value / 3072); st.cost = Math.min(1, l.cost / 9000 + 0.2); }
    return st;
  }
  // who is where: today's people gather in today's room, everyone else is at their own desk
  var HOME = { priya: "product", arjun: "arch", sam: "eng", maya: "qa", lena: "platform", sponsor: "board", finance: "board",
               centre: "centre", agent: "centre", agent2: "centre", ops: "centre", legal: "board" };
  function whereabouts(state) {
    var rooms = {}, here = {}, k, day;
    if (state && state.beat !== "end") { day = sim.today(data, state); rooms[day.room] = day.with.slice(); day.with.forEach(function (w) { here[w] = 1; }); }
    for (k in HOME) if (!here[k]) (rooms[HOME[k]] = rooms[HOME[k]] || []).push(k);
    return rooms;
  }
  function fit(cv, lw, lh, max, fill) {
    var box = cv.parentNode.clientWidth || lw, scale = Math.max(1, Math.min(max, Math.floor(box / lw)));
    if (fill && scale < 3) scale = Math.min(max, box / lw);          // on a narrow screen the room fills the width
    if (cv.width !== lw) { cv.width = lw; cv.height = lh; }
    // whole pixels wherever the picture fits; on a screen narrower than the picture, it shrinks to fit
    cv.style.width = Math.min(box, lw * scale) + "px"; cv.style.height = Math.round(Math.min(box, lw * scale) * lh / lw) + "px";
  }
  function draw() {
    var state = run && run.state, st = picture(state), day = state && state.beat !== "end" ? sim.today(data, state) : null;
    var rooms = whereabouts(state), speaking = day && day.scene && day.scene[0] ? day.scene[0][0] : null, g, px;
    if (still || paused) { shut = gateShut(state); enter = 1; flash = 0; planeT = -1; }
    // the room where today happens
    if (sceneCv.parentNode) {
      fit(sceneCv, A.W, A.H, 5, true);
      g = sceneCv.getContext("2d"); g.imageSmoothingEnabled = false;
      A.room(g, day ? day.room : "lobby", clock, st, true, day ? rooms[day.room] : null, speaking, enter);
      if (flash > 0) { g.fillStyle = "rgba(222,138,138," + (0.5 * flash) + ")"; g.fillRect(0, 0, A.W, A.H); }
    }
    // the whole building, the apron and the sky
    if (mapCv.parentNode) {
      fit(mapCv, MAPW, MAPH, 4);
      g = mapCv.getContext("2d"); g.imageSmoothingEnabled = false;
      A.sky(g, MAPW, MAPH, clock);
      A.horizon(g, 0, MAPW, MAPH - 9);
      if (planeT >= 0) { px = Math.round(-50 + planeT * (MAPW + 100)); g.drawImage(A.PLANE.c, px, Math.round(14 - planeT * 8)); }
      A.ground(g, MAPW, MAPH, MAPH - 9, clock);
      var mark = {}, i, d;
      if (state) for (i = 0; i < state.debts.length; i++) { d = state.debts[i]; if (d.state === "sealed") mark[data.days[sim.dayIndex(data, d.due)].room] = A.C.rose; }
      A.building(g, 5, 4, clock, st, { active: day ? day.room : null, cast: rooms, speaking: speaking, mark: mark, enter: enter,
        shut: shut > 0 ? { eng: shut, qa: shut } : null });
    }
  }
  function loop(now) {
    raf = 0;
    if (still || paused || !seen || document.hidden) return;
    if (now - last > 120) {
      clock += 8; last = now; window.NDFrames++;
      if (planeT >= 0) { planeT += 0.012; if (planeT > 1) planeT = -1; }
      if (enter < 1) enter = Math.min(1, enter + 0.09);
      if (flash > 0) flash = Math.max(0, flash - 0.34);
      var want = gateShut(run && run.state); if (shut > want) shut = Math.max(want, shut - 0.2); else shut = want;
      draw();
    }
    raf = requestAnimationFrame(loop);
  }
  function go() { if (!raf && !still && !paused && seen && !document.hidden) raf = requestAnimationFrame(loop); }
  function fly() { planeT = still ? -1 : 0; enter = still ? 1 : 0; }     // one plane a day, nose first; and today's people walk in
  // The floors where the build happens stay shuttered until the gate has been dealt with.
  function gateShut(state) { return !state || state.beat === "end" ? 0 : (state.i < 5 || (state.i === 5 && state.beat !== "done") ? 1 : 0); }
  document.addEventListener("visibilitychange", go);
  window.addEventListener("resize", function () { draw(); });
  if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { seen = en[0].isIntersecting; go(); }).observe(root);

  /* ------------------------------------------------------------------ looking in on a room */
  function roomCard(id, state) {
    var lines = [], act = null, i = state.i, b;
    var name = { board: "Boardroom", product: "Product", arch: "Architecture", eng: "Engineering", qa: "QA", platform: "Platform", centre: "Contact centre", lobby: "Lobby" }[id];
    if (id === "board") {
      lines.push(state.trust >= 5 ? "Ines has stopped asking for weekly updates." : state.trust >= 3 ? "Ines asks for an update every Friday." : "Ines has asked finance to sit in on your reviews.");
      lines.push(state.moved ? "The date has been moved once. It will not move again." : "Day 90 is the steering committee. The date can be moved once.");
    } else if (id === "product") {
      lines.push(sim.has(state, "register") ? "One list: 12 requirements and 9 quality targets, each with who asked." : "31 requirements on the wall, as they were said.");
      lines.push(sim.has(state, "spec") ? "What the build starts from: one page, signed." : i >= 5 ? "What the build starts from: thirty pages and a summary." : "What the build will start from: not written yet.");
    } else if (id === "arch") {
      lines.push(sim.has(state, "constraints") ? "Constraints sorted by kind: technical, legal, commercial." : "The constraints are in a folder.");
      lines.push(sim.has(state, "records") ? "Decision records are on the shelf." : "No decision has been written down.");
    } else if (id === "eng") {
      lines.push(i < 7 ? "Nothing is built. The gate is on Day 15." : sim.has(state, "skeleton") ? "The thin slice runs end to end. One unknown is retired each day." : "The build is under way.");
      if (state.review) lines.push("Review queue: " + state.review.queue + " days.");
    } else if (id === "qa") {
      b = sim.has(state, "bar") ? sim.bars(data, state) : null;
      lines.push(b ? "Bars on file: same-day " + b.same + ", partner " + b.code + ", refund " + b.refund + "." : "No bar is on file.");
      lines.push(i >= 8 ? "The test set: 500 real cases, 412 right." : "The test set: 500 real cases, waiting for something to test.");
    } else if (id === "platform") {
      if (i < 7) lines.push("The gateway is up. Nothing calls it yet.");
      else if (state.capInTool) lines.push("The refund tool refuses anything over $400 without a named approver.");
      else {
        lines.push("The refund tool accepts any amount.");
        lines.push(state.flags.noBudget ? "Nobody decided what the assistant may pay out alone. The code picked for them." : "The $400 limit is written in the prompt. It is not in the tool.");
        if (sim.canFix(data, state) && state.mode !== "org") act = { t: "fixcap", label: "Type the limit into the tool", days: state.flags.noBudget ? data.rules.capFix.daysNoBudget : data.rules.capFix.days };
      }
      if (i >= 10) lines.push("Model bill: " + (state.bill || (state.flags.billOpen ? "still well over" : "4.4")) + (state.bill ? " times" : "") + " the estimate.");
    } else if (id === "centre") {
      lines.push("240 stranded passengers a day. 38 minutes each, by hand.");
      lines.push(i >= 9 && state.live ? "The assistant handles the cases that shipped. People handle the rest." : "Every case is handled by a person.");
    } else lines.push("Day " + data.days[i].day + " of 90.");
    return { name: name, lines: lines, act: act };
  }

  /* ------------------------------------------------------------------ doing things */
  function act(action) {
    var before = run.state, next = sim.reduce(data, before, action);
    if (next === before) return;
    run.state = next; asking = false;
    if (action.t === "next") { fly(); looking = null; if (!still && next.events.some(function (e) { return e.kind === "incident"; })) flash = 1; }
    if (still) shut = gateShut(next);
    save();
    render(action.t === "next" || action.t === "undo" ? "day" : "out");
    var bits = [];
    if (next.slack !== before.slack) bits.push("Runway " + runwayText(next.slack) + ".");
    if (next.trust !== before.trust) bits.push("Trust " + next.trust + " of " + next.trustMax + ".");
    live.textContent = bits.join(" ");
    go();
  }
  function undoDay() {            // back to the start of today: nothing sealed has been opened, so nothing leaks
    var h = run.state.history.slice();
    while (h.length && h[h.length - 1].t !== "next") h.pop();
    run.state = sim.fold(data, run.opts, h); asking = false; save(); render("day");
  }
  function start(opts) {
    run = { opts: opts, state: sim.init(data, opts) }; looking = null; asking = false;
    shut = 1; save(); fly(); render("day"); go();
  }
  function runwayText(n) { return n >= 0 ? days(n) + " left" : days(-n) + " late"; }

  /* ------------------------------------------------------------------ pieces of the panel */
  function hud(state) {
    var strip = el("ol", { "class": "nd-strip", "aria-label": "The thirteen days" }), i, d, cls, due;
    for (i = 0; i < data.days.length; i++) {
      d = data.days[i]; cls = i < state.i || state.beat === "end" ? "was" : i === state.i ? "now" : "";
      due = state.debts.filter(function (x) { return x.due === d.id && x.state === "sealed"; }).length;
      strip.appendChild(el("li", { "class": cls + (due ? " owed" : ""), "aria-current": cls === "now" ? "step" : null, style: "--c:var(--dg-" + ["slate", "indigo", "teal", "amber"][d.phase] + ")" },
        [el("span", { text: String(d.day) }), due ? el("i", { title: due === 1 ? "Something comes due" : due + " things come due" }, [el("span", { "class": "vh", text: " (something comes due)" })]) : null]));
    }
    var pips = el("span", { "class": "nd-pips", "aria-hidden": "true" });
    for (i = 0; i < state.trustMax; i++) pips.appendChild(el("i", { "class": i < state.trust ? "on" : "" }));
    return el("div", { "class": "nd-hud" }, [strip,
      el("dl", { "class": "nd-meters" }, [
        el("div", { "class": state.slack < 0 ? "bad" : "" }, [el("dt", { text: "Runway" }), el("dd", { text: runwayText(state.slack) })]),
        el("div", {}, [el("dt", { text: "Sponsor's trust" }), el("dd", {}, [pips, el("span", { "class": "vh", text: state.trust + " of " + state.trustMax })])]),
        el("div", {}, [el("dt", { text: "On file" }), el("dd", { text: state.shelf.length + " of " + Object.keys(data.artefacts).length })])
      ])]);
  }
  function eventList(state) {
    var out = el("ul", { "class": "nd-events" }), n = 0;
    state.events.forEach(function (e) {
      if (e.kind === "choice" || e.kind === "task" || e.kind === "gate") return;
      if ((e.kind === "fix" || e.kind === "repair" || e.kind === "move") && state.beat !== "choose") return;      // then it is in the outcome
      var head = e.kind === "debt" ? "From Day " + e.from + ": " + e.tag + "." : e.kind === "pressure" ? "Outside your control." : e.kind === "incident" ? "Why it happened." : "";
      var cost = (e.days ? days(e.days) + " gone. " : "") + (e.trust > 0 ? "Trust falls by " + e.trust + "." : e.trust < 0 ? "Trust rises." : "");
      out.appendChild(el("li", { "class": "ev-" + e.kind }, [head ? el("b", { text: head + " " }) : null, e.text + " ", cost ? el("em", { text: cost }) : null])); n++;
    });
    return n ? out : null;
  }
  function sceneLines(day) {
    var box = el("div", { "class": "nd-lines" });
    var merged = [];                              // two lines from one person are one speech
    day.scene.forEach(function (l) { var m = merged[merged.length - 1]; if (m && m[0] === l[0]) m[1] += " " + l[1]; else merged.push([l[0], l[1]]); });
    merged.forEach(function (l) {
      var c = A.portrait(l[0]), cv = el("canvas", { "class": "nd-face", width: 24, height: 24, "aria-hidden": "true" });
      cv.getContext("2d").drawImage(c, 0, 0);
      box.appendChild(el("p", {}, [cv, el("b", { text: who(l[0]).name + (who(l[0]).title ? " · " + who(l[0]).title : "") }), el("span", { text: l[1] })]));
    });
    return box;
  }
  function optionButtons(state, day, handler, skip) {
    var set = el("fieldset", { "class": "nd-opts" }, [el("legend", { text: day.ask })]);
    day.options.forEach(function (o, n) {
      if (o.id === skip) return;
      var p = sim.price(data, state, day, o);
      set.appendChild(el("button", { type: "button", "class": "nd-opt", "data-key": String(n + 1), onclick: function () { handler(o); } },
        [el("span", { "class": "nd-opt-l", text: o.label }), el("span", { "class": "nd-opt-p", text: p ? days(p) : "no days" })]));
    });
    set.addEventListener("keydown", function (e) {            // 1, 2, 3 pick an option, only while the focus is in the list
      if (!/^[1-9]$/.test(e.key) || e.ctrlKey || e.metaKey || e.altKey) return;
      var b = set.querySelector('[data-key="' + e.key + '"]'); if (b) { e.preventDefault(); b.click(); }
    });
    return set;
  }
  function filedList(state) {
    if (!state.filed.length) return null;
    var ul = el("ul", { "class": "nd-filed" });
    state.filed.forEach(function (a) { var x = data.artefacts[a]; ul.appendChild(el("li", {}, [el("b", { text: x.name }), el("span", { text: x.plain })])); });
    return el("div", { "class": "nd-filedbox" }, [el("p", { "class": "nd-k", text: state.filed.length === 1 ? "On file" : "On file, " + state.filed.length + " documents" }), ul]);
  }
  function outcome(state, day) {
    var box = el("div", { "class": "nd-out", tabindex: "-1" }), sealed, last = state.debts[state.debts.length - 1];
    state.events.forEach(function (e) {
      if (e.kind === "choice") box.appendChild(el("p", { "class": "nd-you" }, [el("b", { text: e.label }), el("em", { text: e.days ? days(e.days) : "no days" })]));
      if (e.kind === "choice" || e.kind === "task" || e.kind === "gate" || e.kind === "fix" || e.kind === "repair" || e.kind === "move")
        box.appendChild(el("p", { "class": "ev-" + e.kind }, [e.text, e.kind !== "choice" && e.days ? el("em", { text: " " + days(e.days) + "." }) : null,
          e.trust > 0 ? el("em", { text: " Trust falls by " + e.trust + "." }) : e.trust < 0 ? el("em", { text: " Trust rises." }) : null]));
    });
    sealed = last && last.id === day.id && last.state === "sealed";
    if (sealed) box.appendChild(el("p", { "class": "nd-sealed" }, [el("i", { "aria-hidden": "true" }), "Something is pinned to Day " + last.dueDay + "."]));
    var f = filedList(state); if (f) box.appendChild(f);
    return box;
  }
  function deeper(day) {
    if (!day.deeper || !day.deeper.length) return null;
    var p = el("p", { "class": "nd-deeper" }, [el("span", { text: "Go deeper: " })]);
    day.deeper.forEach(function (d, i) {
      if (i) p.appendChild(document.createTextNode(" · "));
      p.appendChild(el("a", { href: d[0] === "workbench" ? UP + "workbench/" + d[1] : UP + d[1], text: d[2] }));
    });
    return p;
  }

  /* ------------------------------------------------------------------ the five tasks */
  function taskForm(state, id) {
    var t = data.tasks[id], box = el("form", { "class": "nd-task", onsubmit: function (e) { e.preventDefault(); } }), submit, status = el("p", { "class": "nd-status", role: "status" });
    box.appendChild(el("h3", { text: t.title })); box.appendChild(el("p", { "class": "nd-intro", text: t.intro }));
    function done(label, get) {
      submit = el("button", { type: "submit", "class": "btn pri", text: label });
      box.appendChild(status); box.appendChild(submit);
      box.addEventListener("submit", function () { var v = get(); if (v == null) return; act(state.beat === "choose" && state.pending ? { t: "challenge", input: v } : { t: "task", id: id, input: v }); });
    }
    if (id === "bar") {
      var hold = el("input", { type: "checkbox", id: "nd-hold" }), tb = el("tbody");
      var paint = function () {
        tb.innerHTML = "";
        t.slices.forEach(function (s) {
          var dmg = hold.checked && s.damageHeld != null ? s.damageHeld : s.damage, bar = sim.barOf(s, hold.checked);
          tb.appendChild(el("tr", {}, [el("th", { scope: "row", text: s.name }), el("td", { text: "$" + s.saving }), el("td", { text: "$" + dmg }),
            el("td", { "class": bar > 95 ? "hot" : "" }, [el("b", { text: bar + "%" }), el("i", { style: "--w:" + bar + "%" })])]));
        });
      };
      hold.addEventListener("change", paint); paint();
      box.appendChild(el("table", { "class": "nd-tb" }, [el("thead", {}, [el("tr", {}, [el("th", { scope: "col", text: "Kind of case" }), el("th", { scope: "col", text: "Right saves" }),
        el("th", { scope: "col", text: "Wrong costs" }), el("th", { scope: "col", text: "The bar" })])]), tb]));
      box.appendChild(el("label", { "class": "nd-check", "for": "nd-hold" }, [hold, el("span", { text: t.hold })]));
      done("Sign the bars", function () { return { hold: hold.checked }; });
    } else if (id === "score") {
      var bars = sim.bars(data, state);
      t.slices.forEach(function (s) {
        var st = sim.sliceStats(s), fs = el("fieldset", { "class": "nd-slice" }, [el("legend", { text: s.name })]);
        fs.appendChild(el("p", { "class": "nd-gauge" }, [
          el("span", { text: st.score + "% on " + s.n + " cases. At least " + st.lower + "%. The bar is " + bars[s.id] + "%." }),
          el("i", { "aria-hidden": "true", style: "--s:" + st.score + "%;--l:" + st.lower + "%;--b:" + bars[s.id] + "%" })]));
        t.choices.forEach(function (c) {
          fs.appendChild(el("label", { "class": "nd-radio" }, [el("input", { type: "radio", name: "sl-" + s.id, value: c[0] }), el("span", { text: c[1] })]));
        });
        box.appendChild(fs);
      });
      done("Decide", function () {
        var out = {}, ok = true;
        t.slices.forEach(function (s) { var r = box.querySelector('input[name="sl-' + s.id + '"]:checked'); if (r) out[s.id] = r.value; else ok = false; });
        if (!ok) { status.textContent = "Choose for each of the three."; return null; }
        return out;
      });
    } else if (id === "route") {
      var count = el("p", { "class": "nd-count", role: "status" });
      var tally = function () { var n = 0; box.querySelectorAll("input:checked").forEach(function (r) { n += +r.value; }); count.textContent = "Review slots used: " + n + ". Before, every change took two: 18."; };
      t.items.forEach(function (it) {
        var fs = el("fieldset", { "class": "nd-pr" }, [el("legend", { text: it.name })]);
        t.lanes.forEach(function (ln, n) {
          fs.appendChild(el("label", { "class": "nd-radio" }, [el("input", { type: "radio", name: "pr-" + it.id, value: String(n), onchange: tally }), el("span", { text: ln })]));
        });
        box.appendChild(fs);
      });
      box.appendChild(count); tally();
      done("Route them", function () {
        var out = {}, ok = true;
        t.items.forEach(function (it) { var r = box.querySelector('input[name="pr-' + it.id + '"]:checked'); if (r) out[it.id] = +r.value; else ok = false; });
        if (!ok) { status.textContent = "Route all nine."; return null; }
        return out;
      });
    } else if (id === "leak") {
      var sum = el("p", { "class": "nd-count", role: "status" });
      var calc = function () {
        var m = 4.4, d = 0; t.rows.forEach(function (r) { if (box.querySelector("#lk-" + r.id).checked) { m /= r.factor; d += r.days; } });
        sum.textContent = (d === 0 ? "Nothing chosen yet." : "Chosen: " + (d === 0.5 ? "half a day" : days(d)) + " of work.") + " The bill would be " + (Math.round(m * 100) / 100) + " times the estimate." + (d > t.budget ? " That is more than one day." : "");
        return d;
      };
      var tbl = el("tbody");
      t.rows.forEach(function (r) {
        tbl.appendChild(el("tr", {}, [
          el("th", { scope: "row" }, [el("label", { "class": "nd-check", "for": "lk-" + r.id }, [el("input", { type: "checkbox", id: "lk-" + r.id, onchange: calc }), el("span", { text: r.fix })])]),
          el("td", { text: r.name + ": " + r.was + ", now " + r.now }), el("td", { text: r.days === 0.5 ? "half a day" : days(r.days) })]));
      });
      box.appendChild(el("table", { "class": "nd-tb stack" }, [el("thead", {}, [el("tr", {}, [el("th", { scope: "col", text: "Fix" }), el("th", { scope: "col", text: "What the log shows" }), el("th", { scope: "col", text: "Takes" })])]), tbl]));
      box.appendChild(sum); calc();
      done("Start the fixes", function () {
        if (calc() > t.budget) { status.textContent = "You have one day. Untick something."; return null; }
        var out = []; t.rows.forEach(function (r) { if (box.querySelector("#lk-" + r.id).checked) out.push(r.id); });
        if (!out.length) { status.textContent = "Pick at least one fix."; return null; }
        return out;
      });
    } else if (id === "slide") {
      var L = sim.ledger(data, state), text = {
        saving: L.saving + " percent fewer person-days on stranded passengers: " + money(L.value),
        bill: "What it cost: a model bill of " + money(L.bill) + " and " + money(L.review) + " of review time",
        net: "This cycle, net: " + money(L.net) + ". Next cycle: review time under 30 hours",
        score: "82.4 percent right on 500 real cases",
        incident: state.incidents ? "One refund paid in error: $2,000" : "No money paid out in error",
        shelf: state.shelf.length + " documents on file"
      };
      t.lines.forEach(function (ln) {
        box.appendChild(el("label", { "class": "nd-check big", "for": "sd-" + ln.id }, [el("input", { type: "checkbox", id: "sd-" + ln.id, value: ln.id }), el("span", { text: text[ln.id] })]));
      });
      done("Present the slide", function () {
        var out = []; box.querySelectorAll("input:checked").forEach(function (c) { out.push(c.value); });
        if (out.length !== 3) { status.textContent = out.length < 3 ? "Pick three lines. You have " + out.length + "." : "Three lines fit. Untick " + (out.length - 3) + "."; return null; }
        return out;
      });
    }
    return box;
  }

  function gatePanel(state) {
    var miss = sim.gateMissing(state), box = el("div", { "class": "nd-gate" }), lamps = el("ul", { "class": "nd-lamps" });
    ["spec", "bar", "budget"].forEach(function (a) {
      var on = sim.has(state, a);
      lamps.appendChild(el("li", { "class": on ? "on" : "" }, [el("i", { "aria-hidden": "true" }), el("b", { text: data.artefacts[a].name }), el("span", { text: on ? "signed" : "missing" })]));
    });
    box.appendChild(el("h3", { text: "The gate" }));
    box.appendChild(el("p", { "class": "nd-intro", text: "This is the one hand-off that stops the work. Nothing is built until three documents are signed. After today, changing your mind costs a rewrite." }));
    box.appendChild(lamps);
    if (!miss.length) box.appendChild(el("div", { "class": "nd-acts" }, [el("button", { type: "button", "class": "btn pri", text: "Open the gate", onclick: function () { act({ t: "gate", how: "pass" }); } })]));
    else box.appendChild(el("div", { "class": "nd-acts" }, [
      el("button", { type: "button", "class": "nd-opt", onclick: function () { act({ t: "gate", how: "hold" }); } }, [el("span", { "class": "nd-opt-l", text: "Hold the gate and write what is missing" }), el("span", { "class": "nd-opt-p", text: days(2 * miss.length) })]),
      el("button", { type: "button", "class": "nd-opt", onclick: function () { act({ t: "gate", how: "open" }); } }, [el("span", { "class": "nd-opt-l", text: "Open the gate with what is on file" }), el("span", { "class": "nd-opt-p", text: "no days" })])]));
    return box;
  }

  /* ------------------------------------------------------------------ the side column: debts, the date, a room */
  function side(state) {
    var box = el("div", { "class": "nd-side" }), sealed = state.debts.map(function (d, i) { return { d: d, i: i }; }).filter(function (x) { return x.d.state === "sealed"; });
    if (state.mode === "role") box.appendChild(el("p", { "class": "nd-you-are" }, [el("b", { text: "You are " + who(data.roles[state.role].who).name + ", the " + lower(data.roles[state.role].name) + ". " }), data.roles[state.role].line + " " + state.tokens + (state.tokens === 1 ? " question" : " questions") + " left to ask of a colleague."]));
    if (state.mode === "org") box.appendChild(el("p", { "class": "nd-you-are" }, [el("b", { text: "You are Ines, the sponsor. " }), state.tokens + (state.tokens === 1 ? " question" : " questions") + " left to ask."]));
    if (sealed.length && state.mode !== "org") {
      var ul = el("ul", { "class": "nd-debts" });
      sealed.forEach(function (x) {
        var c = sim.repairCost(data, x.d);
        ul.appendChild(el("li", {}, [el("span", {}, [el("b", { text: "Day " + x.d.dueDay + ". " }), "From Day " + x.d.from + ": " + x.d.tag + "."]),
          el("button", { type: "button", "class": "btn ghost sm", onclick: function () { act({ t: "repair", debt: x.i }); } }, ["Go back and do it properly ", el("em", { text: days(c) })])]));
      });
      box.appendChild(el("div", { "class": "nd-owed" }, [el("p", { "class": "nd-k", text: sealed.length === 1 ? "One thing comes due" : sealed.length + " things come due" }), ul]));
    }
    if (!state.moved && state.mode !== "org" && state.beat !== "end") {
      var m = data.rules.moveDate, ok = state.shelf.length >= m.evidence;
      box.appendChild(el("div", { "class": "nd-move" }, [
        el("button", { type: "button", "class": "btn ghost sm", onclick: function () { act({ t: "move" }); } }, ["Ask Ines, the sponsor, to move the date ", el("em", { text: "+" + days(m.days) + ", once" })]),
        el("span", { text: ok ? "With " + state.shelf.length + " documents on file, she will agree without a question." : "With " + state.shelf.length + " on file, it will cost her trust. She agrees easily at " + m.evidence + "." })]));
    }
    box.appendChild(el("p", { "class": "nd-leave" }, [el("a", { href: "./", text: "Leave this run" }), " It is saved, and you can carry on later."]));
    return box;
  }
  function roomBox(state) {
    var chips = el("div", { "class": "nd-rooms", role: "group", "aria-label": "Look in on a room" });
    ["board", "product", "arch", "eng", "qa", "platform", "centre"].forEach(function (id) {
      var c = roomCard(id, state);
      chips.appendChild(el("button", { type: "button", "class": "nd-chip" + (looking === id ? " on" : ""), "aria-pressed": looking === id ? "true" : "false", "data-room": id,
        onclick: function () { looking = looking === id ? null : id; lastRoom = id; render("look"); }, text: c.name }));
    });
    var out = [el("p", { "class": "nd-k", text: "Look in on a room" }), chips];
    if (looking) {
      var c = roomCard(looking, state), card = el("div", { "class": "nd-card", tabindex: "-1" }, [el("b", { text: c.name })]);
      c.lines.forEach(function (l) { card.appendChild(el("p", { text: l })); });
      if (c.act) card.appendChild(el("button", { type: "button", "class": "nd-opt", onclick: function () { act({ t: c.act.t }); } }, [el("span", { "class": "nd-opt-l", text: c.act.label }), el("span", { "class": "nd-opt-p", text: days(c.act.days) })]));
      out.push(card);
    }
    return el("div", { "class": "nd-look" }, out);
  }

  /* ------------------------------------------------------------------ screens */
  function head(text, sub) {
    return el("div", { "class": "nd-dayhead" }, [el("h2", { tabindex: "-1", text: text }), sub ? el("p", { text: sub }) : null]);
  }
  function pauseControl() {         // one switch, shown on both pictures, kept in step
    var box = el("input", { type: "checkbox", autocomplete: "off", "data-motion-toggle": true, onchange: function (e) {
      paused = e.target.checked;
      root.querySelectorAll("[data-motion-toggle]").forEach(function (b) { b.checked = paused; });
      draw(); go();
    } });
    box.checked = paused;
    return el("label", { "class": "mpause nd-pause" }, [box, el("span", { "class": "vh", text: "Pause the animation" }), el("i", { "aria-hidden": "true" })]);
  }
  function stage() {
    return el("div", { "class": "nd-stage" }, [el("div", { "class": "nd-map" }, [mapCv, still ? null : pauseControl()])]);
  }

  function titleScreen() {
    var saved = load(), b = best(), kids = [];
    kids.push(el("div", { "class": "nd-title" }, [
      el("p", { "class": "nd-pitch", text: "Thirteen days decide the ninety. Every call has a price in days. Some prices arrive later." }),
      el("div", { "class": "nd-acts" }, [
        saved && saved.history.length ? el("button", { type: "button", "class": "btn pri", text: "Carry on from Day " + data.days[Math.min(12, saved.history.filter(function (a) { return a.t === "next"; }).length)].day,
          onclick: function () { run = { opts: saved.opts, state: sim.fold(data, saved.opts, saved.history) }; render("day"); go(); } }) : null,
        el("button", { type: "button", "class": saved && saved.history.length ? "btn ghost" : "btn pri", text: "Start at Day 1", onclick: function () { start({ mode: "team", seed: seed() }); } })]),
      b ? el("p", { "class": "nd-best", text: "Your best ending so far: " + data.verdicts[b.key].name.toLowerCase() + "." }) : null,
      el("div", { "class": "nd-ways" }, [
        el("p", { "class": "nd-k", text: "Two other ways to play" }),
        el("div", { "class": "nd-waygrid" }, [
          el("div", {}, [el("b", { text: "One role" }), el("p", { text: "Make your own calls. Watch your colleagues make theirs, and choose which " + ["no", "one", "two", "three", "four", "five"][data.rules.questions.role] + " to question." }), roleButtons()]),
          el("div", {}, [el("b", { text: "The organisation" }), el("p", { text: "You are the sponsor. Pick three rules for the programme, then watch the ninety days run." }),
            el("button", { type: "button", "class": "btn ghost sm", text: "Set the rules", onclick: function () { render("org"); } })])])])]));
    return kids;
  }
  function roleButtons() {
    var box = el("div", { "class": "nd-rolebtns" });
    Object.keys(data.roles).forEach(function (r) {
      box.appendChild(el("button", { type: "button", "class": "btn ghost sm", text: data.roles[r].name, onclick: function () { start({ mode: "role", role: r, seed: seed() }); } }));
    });
    return box;
  }
  function seed() { try { var n = +(localStorage.getItem(KEY + ".n") || 0); localStorage.setItem(KEY + ".n", String(n + 1)); return n; } catch (e) { return 0; } }

  function orgSetup() {
    var box = el("form", { "class": "nd-task nd-org", onsubmit: function (e) { e.preventDefault(); } }), status = el("p", { "class": "nd-status", role: "status" });
    box.appendChild(el("h2", { tabindex: "-1", text: "Three rules for the programme" }));
    box.appendChild(el("p", { "class": "nd-intro", text: "You cannot enforce everything: a rule that stops the work costs days, and people route around the tenth one. Pick three. The team does the rest by habit." }));
    data.policies.forEach(function (p) {
      box.appendChild(el("label", { "class": "nd-check big", "for": "po-" + p.id }, [el("input", { type: "checkbox", id: "po-" + p.id, value: p.id }), el("span", { text: p.name })]));
    });
    box.appendChild(status);
    box.appendChild(el("div", { "class": "nd-acts" }, [el("button", { type: "submit", "class": "btn pri", text: "Run the ninety days" }),
      el("button", { type: "button", "class": "btn ghost", text: "Back", onclick: function () { run = null; render("back"); } })]));
    box.addEventListener("submit", function () {
      var set = []; box.querySelectorAll("input:checked").forEach(function (c) { set.push(c.value); });
      if (set.length > 3) { status.textContent = "Three at most. Untick " + (set.length - 3) + "."; return; }
      start({ mode: "org", policies: set, seed: seed() });
    });
    return [box];
  }

  function playScreen(state) {
    var day = sim.today(data, state), ph = data.phases[day.phase], kids = [], own = who(day.owner), right, planned, o;
    kids.push(hud(state));
    kids.push(el("div", { "class": "nd-scene" }, [sceneCv, still ? null : pauseControl()]));
    kids.push(head("Day " + day.day + ". " + day.title, ph.name + " (" + ph.key + ") · " + own.name + "'s call · " + (day.track === "tech" ? "tech" : "consultancy") + " track"));
    var ev = eventList(state); if (ev) kids.push(ev);
    if (state.beat === "choose") {
      kids.push(sceneLines(day));
      if (state.pending) {                       // a colleague's call, or the team's under the sponsor
        if (day.options) { planned = day.options.filter(function (x) { return x.id === state.pending; })[0]; right = sim.rightOption(day); }
        kids.push(el("div", { "class": "nd-plan" }, [
          el("p", { "class": "nd-k", text: day.ask }),
          el("p", { "class": "nd-you" }, [el("b", { text: own.name + " plans: " + (planned ? planned.label : "the saving, large and alone, on the slide") }), planned ? el("em", { text: sim.price(data, state, day, planned) ? days(sim.price(data, state, day, planned)) : "no days" }) : null])]));
        if (asking) {
          kids.push(el("p", { "class": "nd-k", text: day.options ? "Ask for this instead. It uses one of your questions." : "Build the slide yourself. It uses one of your questions." }));
          kids.push(day.options ? optionButtons(state, day, function (opt) { act({ t: "challenge", opt: opt.id }); }, state.pending) : taskForm(state, day.task));
          kids.push(el("div", { "class": "nd-acts" }, [el("button", { type: "button", "class": "btn ghost", text: "Let it stand after all", onclick: function () { act({ t: "accept" }); } })]));
        }
        else kids.push(el("div", { "class": "nd-acts" }, [
          el("button", { type: "button", "class": "btn pri", text: "Let it stand", onclick: function () { act({ t: "accept" }); } }),
          state.tokens > 0 && !(state.mode === "org" && right && right.id === state.pending) ? el("button", { type: "button", "class": "btn ghost", onclick: function () {
            if (state.mode === "org") { if (day.options) act({ t: "challenge", opt: right.id }); else act({ t: "challenge" }); } else { asking = true; render("stay"); }
          } }, ["Ask to see the evidence ", el("em", { text: state.tokens + " left" })]) : null]));
      } else if (day.options) kids.push(optionButtons(state, day, function (opt) { act({ t: "choose", opt: opt.id }); }));
      else kids.push(taskForm(state, day.task));
    } else {
      kids.push(outcome(state, day));
      if (state.beat === "task") kids.push(taskForm(state, state.task));
      else if (state.beat === "gate") kids.push(gatePanel(state));
      else if (state.beat === "done") {
        o = deeper(day); if (o) kids.push(o);
        kids.push(el("div", { "class": "nd-acts" }, [
          el("button", { type: "button", "class": "btn pri nd-next", text: state.i === data.days.length - 1 ? "Hear the verdict" : "On to Day " + data.days[state.i + 1].day, onclick: function () { act({ t: "next" }); } }),
          state.mode === "org" && state.i < data.days.length - 1 ? el("button", { type: "button", "class": "btn ghost", text: "Run to the end", onclick: runOut }) : null,
          state.mode !== "org" ? el("button", { type: "button", "class": "btn ghost sm", text: "Undo today", onclick: undoDay }) : null]));
      }
    }
    var s = side(state); if (s) kids.push(s);
    return kids;
  }
  function runOut() {              // the sponsor lets the rest play: every remaining call stands
    var s = run.state, guard = 0, n;
    while (s.beat !== "end" && guard++ < 200) { n = sim.reduce(data, s, s.beat === "choose" ? { t: "accept" } : { t: "next" }); if (n === s) break; s = n; }
    run.state = s; save(); render("day");
  }

  function endScreen(state) {
    var v = sim.verdict(data, state), V = data.verdicts[v.key], L = sim.ledger(data, state), kids = [], b = best();
    try { if (!b || RANK[v.key] > RANK[b.key]) localStorage.setItem(BEST, JSON.stringify({ key: v.key, mode: state.mode })); } catch (e) { /* no storage */ }
    clearSave();
    kids.push(el("div", { "class": "nd-verdict v-" + v.key }, [el("p", { "class": "nd-k", text: "Day 90. The steering committee" }), el("h2", { tabindex: "-1", text: V.name }), el("p", { text: V.line })]));
    kids.push(el("dl", { "class": "nd-meters end" }, [
      el("div", { "class": v.late ? "bad" : "" }, [el("dt", { text: "The date" }), el("dd", { text: v.late ? days(v.late) + " late" : "met, " + days(state.slack) + " to spare" })]),
      el("div", {}, [el("dt", { text: "Sponsor's trust" }), el("dd", { text: state.trust + " of " + state.trustMax })]),
      el("div", {}, [el("dt", { text: "Saved" }), el("dd", { text: L.days + " person-days, " + money(L.value) })]),
      el("div", {}, [el("dt", { text: "Spent" }), el("dd", { text: money(L.cost) }), el("dd", { "class": "nd-sub", text: "model " + money(L.bill) + ", review " + money(L.review) + (L.mishaps ? ", refunds " + money(L.mishaps) : "") })]),
      el("div", { "class": L.net < 0 ? "bad" : "" }, [el("dt", { text: "Net, first cycle" }), el("dd", { text: money(L.net) })])]));
    // the thirteen calls, and what each one came back as
    var rows = el("tbody");
    data.days.forEach(function (d) {
      var form = d.variants ? d.variants[state.incidents ? "paid" : "blocked"] : d, pick = state.picks[d.id], opt = null, debt, back = "";
      if (form.options) form.options.forEach(function (o) { if (o.id === pick) opt = o; });
      debt = state.debts.filter(function (x) { return x.id === d.id; });
      debt.forEach(function (x) { back += (back ? " " : "") + (x.state === "fired" ? "Came back on Day " + x.dueDay + ": " + (x.days ? days(x.days) : "") + (x.days && x.trust ? ", " : "") + (x.trust ? "trust " + "−" + x.trust : "") + "." : x.state === "repaired" ? "Repaired before it fired." : ""); });
      if (!back && opt && opt.after) back = opt.after;
      rows.appendChild(el("tr", { "class": opt && opt.right ? "ok" : opt ? "off" : "" }, [el("th", { scope: "row", text: "Day " + d.day }),
        el("td", { text: opt ? opt.label : d.id === "d13" ? "The slide: " + (state.slide || []).length + " lines" : "" }), el("td", { text: back || (opt && opt.right ? "On file." : "") })]));
    });
    kids.push(el("div", { "class": "nd-paper" }, [el("h3", { text: "Your thirteen calls" }),
      el("table", { "class": "nd-tb calls" }, [el("thead", {}, [el("tr", {}, [el("th", { scope: "col", text: "Day" }), el("th", { scope: "col", text: "The call" }), el("th", { scope: "col", text: "What it became" })])]), rows])]));
    // three questions to take to work, and the words now earned
    kids.push(el("div", { "class": "nd-paper two" }, [
      el("div", {}, [el("h3", { text: "Three questions for Monday" }), el("ol", { "class": "nd-monday" }, [
        el("li", { text: "Is the limit in the tool, or only in the prompt?" }),
        el("li", { text: "What is the least that score could be, and on how many cases?" }),
        el("li", { text: "Which of our open decisions really stops the work?" })])]),
      el("div", {}, [el("h3", { text: "What you put on file" }), (function () {
        var ul = el("ul", { "class": "nd-terms" });
        state.shelf.forEach(function (a) { var x = data.artefacts[a]; ul.appendChild(el("li", {}, [el("b", { text: x.term }), el("span", { text: " " + x.plain })])); });
        if (!state.shelf.length) ul.appendChild(el("li", { text: "Nothing was filed." }));
        return ul;
      })()])]));
    var summary = summaryText(state, v, L), copied = el("span", { "class": "nd-status", role: "status" });
    kids.push(el("div", { "class": "nd-acts" }, [
      el("button", { type: "button", "class": "btn pri", text: "Play again", onclick: function () { start({ mode: state.mode, role: state.role, policies: state.policies, seed: seed() }); } }),
      el("button", { type: "button", "class": "btn ghost", text: "Another way to play", onclick: function () { run = null; render("back"); } }),
      el("button", { type: "button", "class": "btn ghost", text: "Copy the summary", onclick: function () {
        if (navigator.clipboard) navigator.clipboard.writeText(summary).then(function () { copied.textContent = "Copied."; }, function () { copied.textContent = "Could not copy."; });
      } }), copied]));
    kids.push(el("p", { "class": "nd-deeper" }, [el("span", { text: "The same ninety days, in depth: " }), el("a", { href: UP + "workbench/#/story", text: "the thirteen episodes" }), " · ",
      el("a", { href: UP + "workbench/#/toolkit", text: "seventeen calculators" }), " · ", el("a", { href: UP + "learn/skyways-case-study/", text: "the case as a lesson" })]));
    return kids;
  }
  function summaryText(state, v, L) {
    var out = ["Ninety Days, the SkyWays simulator: " + data.verdicts[v.key].name + ".",
      (v.late ? days(v.late) + " late" : "Date met") + ", trust " + state.trust + " of " + state.trustMax + ", " + state.shelf.length + " documents on file.",
      "Saved " + L.days + " person-days (" + money(L.value) + "), spent " + money(L.cost) + ", net " + money(L.net) + ".", ""];
    data.days.forEach(function (d) {
      var form = d.variants ? d.variants[state.incidents ? "paid" : "blocked"] : d, pick = state.picks[d.id];
      var back = state.debts.some(function (x) { return x.id === d.id && x.state === "fired"; });
      (form.options || []).forEach(function (o) { if (o.id === pick) out.push("Day " + d.day + ": " + o.label + (back ? " (it came back)" : "")); });
    });
    out.push("", "https://akash-coded.github.io/aws-bedrock-agentcore-strands/simulator/");
    return out.join("\n");
  }

  /* ------------------------------------------------------------------ render */
  var panel = el("div", { "class": "nd-panel" }), left = null;
  function render(focus) {
    var state = run && run.state, kids, f;
    if (!left) { left = stage(); root.appendChild(left); root.appendChild(panel); root.appendChild(live); }
    root.className = "nd-app " + (!state ? "at-title" : state.beat === "end" ? "at-end" : "at-play") + (focus === "org" ? " at-org" : "");
    document.documentElement.classList.toggle("nd-playing", !!state);
    kids = focus === "org" ? orgSetup() : !state ? titleScreen() : state.beat === "end" ? endScreen(state) : playScreen(state);
    panel.innerHTML = "";
    kids.forEach(function (k) { panel.appendChild(k); });
    // the room cards live under the building
    var old = left.querySelector(".nd-look"); if (old) old.remove();
    if (state && state.beat !== "end" && focus !== "org") left.appendChild(roomBox(state));
    draw();
    if (focus === "look") f = left.querySelector(".nd-card") || left.querySelector('.nd-chip[data-room="' + lastRoom + '"]');
    else if (focus === "stay") f = panel.querySelector(".nd-opts button, .nd-task input");
    else if (focus === "out") f = panel.querySelector(".nd-task h3, .nd-gate h3") || panel.querySelector(".nd-out");
    else f = panel.querySelector("h2");
    if (!f) f = panel.querySelector("h2");
    if (focus === "back") f = panel.querySelector("button");
    // a new day, or a new screen, starts at its top: bring the game into view, then put the focus on its heading
    if ((focus === "day" || focus === "back" || focus === "org") && root.getBoundingClientRect().top < 0) root.scrollIntoView({ block: "start" });
    if (f && (run || focus === "org" || focus === "back")) { if (!f.hasAttribute("tabindex") && !/^(BUTTON|INPUT|A)$/.test(f.tagName)) f.setAttribute("tabindex", "-1"); try { f.focus({ preventScroll: focus !== "look" && focus !== "out" }); } catch (e) { f.focus(); } }
    if (focus === "day" || focus === "back") live.textContent = "";
  }

  mapCv.addEventListener("click", function (e) {           // looking in by pointing at the building
    if (!run || run.state.beat === "end") return;
    var r = mapCv.getBoundingClientRect(), k = MAPW / r.width, id = A.roomAt((e.clientX - r.left) * k - 5, (e.clientY - r.top) * k - 4);
    if (id && id !== "lobby") { looking = looking === id ? null : id; lastRoom = id; render("look"); }
  });

  // the plain list was for a page without script: this script is here, so the game takes over
  var plain = document.querySelector(".nd-plain"); if (plain) plain.hidden = true;
  root.hidden = false;
  render("title");
  go();
})();
