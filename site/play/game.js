/* Ninety Days · the page. Every word and control is page text; the two canvases are the room where
   today happens and the whole building. The rules are in sim.js: this file asks them and shows the
   answer. Why each thing is as it is: site/GAME.md. */
(function () {
  "use strict";
  var src = document.getElementById("nd-data"), root = document.getElementById("nd");
  // no rules or no pictures came: the plain list comes back
  if (!src || !root || !window.ND || !window.NDArt) { document.documentElement.classList.remove("nd-js"); return; }
  var data = JSON.parse(src.textContent), sim = window.ND.sim, A = window.NDArt;
  var KEY = "skyways.ninety", BEST = "skyways.ninety.best";
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var UP = root.getAttribute("data-up") || "../";
  var MILE = (data.line && data.line.milestones) || {};     // the four milestones
  /* ------------------------------------------------------------------ small things */
  function el(tag, attrs, kids) {
    var n = document.createElement(tag), k;
    for (k in attrs || {}) {
      if (attrs[k] == null || attrs[k] === false) continue;
      if (k === "text") n.textContent = attrs[k];
      else if (k.slice(0, 2) === "on") n.addEventListener(k.slice(2), guard(attrs[k]));      // every press, through one safeguard
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
  var RANK = { stopped: 0, paused: 1, conditional: 2, funded: 3 }, NUM = ["no", "one", "two", "three", "four", "five"];

  /* ------------------------------------------------------------------ a press that fails
     A press that throws leaves the screen and the save as they were, and says so with a way to reload. */
  var renders = 0;                // screens drawn
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function restore(v) { try { if (v == null) localStorage.removeItem(KEY); else localStorage.setItem(KEY, v); } catch (e) { /* nothing to put back */ } }
  function guard(fn) {
    return function () {
      var was = { run: run, state: run && run.state, looking: looking, asking: asking, shown: shown, shut: shut, enter: enter, flash: flash, saved: stored(), n: renders };
      try { return fn.apply(this, arguments); }
      catch (err) {
        run = was.run; if (run) run.state = was.state;
        looking = was.looking; asking = was.asking; shown = was.shown; shut = was.shut; enter = was.enter; flash = was.flash; answering = false;
        restore(was.saved);
        if (renders !== was.n) { try { render("keep"); } catch (e) { /* the screen stays as the failed press left it */ } }
        outOfDate(err);
      }
    };
  }
  function outOfDate(err) {
    try { console.error("Ninety Days stopped: " + (err && err.message ? err.message : String(err))); } catch (e) { /* no console */ }
    var old = root.querySelector(".nd-broke"), again, box;
    if (old) old.remove();
    if (!renders) { document.documentElement.classList.remove("nd-js"); if (plain) plain.hidden = false; }      // the game never started: the days as text
    again = el("button", { type: "button", "class": "btn pri", text: "Reload", onclick: function () { location.reload(); } });
    box = el("div", { "class": "nd-broke", role: "alert" }, [el("p", { text: "This page is out of date. Reload to play." }), again]);
    if (!panel.parentNode) root.appendChild(panel);
    root.hidden = false;
    panel.insertBefore(box, panel.firstChild);
    try { again.focus({ preventScroll: true }); } catch (e) { again.focus(); }
    if (!inView(box)) jump(box);
  }

  var run = null;                 // { opts, state }
  var looking = null, lastRoom = null;   // the room whose card is open, and the chip last pressed
  var asking = false;             // Day 90 in one role: building the slide
  var answering = false;          // redrawn as the answer to a press
  var shown = {};                 // the small simulations played
  var live = el("p", { "class": "vh", "aria-live": "polite", role: "status" });

  /* ------------------------------------------------------------------ the stage: two canvases */
  var sceneCv = el("canvas", { "class": "nd-scene-cv", "aria-hidden": "true" });
  var mapCv = el("canvas", { "class": "nd-map-cv", "aria-hidden": "true" });
  // the building fills its column at a whole scale; OX is the sky on either side of it
  var MAPW = A.BW, MAPH = A.BH + 16, OX = 0, OY = 4, GROUND = A.BH + 4, clock = 0, raf = 0, last = 0, paused = false;
  var vis = { map: 1, scene: 1 };   // which canvas is on the screen, as the observer last said
  var enter = 1, shut = 0, flash = 0;      // walking in, the shutters, the incident's flash
  window.NDFrames = 0;            // for the acceptance gate: frames drawn by the loop

  function picture(state) {       // what the walls show
    var i = state.i, st = {};
    st.day = data.days[Math.min(i, data.days.length - 1)].day; st.dayIndex = i;
    // the sky is the phase; Day 90 is dusk, or night if the run is late
    st.phases = data.days.map(function (d) { return d.phase; });
    st.sky = ["dawn", "morning", "afternoon", "golden"][st.phases[i]];
    if (state.beat === "end" || i === data.days.length - 1) st.sky = state.slack < 0 ? "night" : "dusk";
    st.owed = data.days.map(function (d) { return state.debts.some(function (x) { return x.due === d.id && x.state === "sealed"; }); });
    st.notes = sim.has(state, "register") ? 12 : (i > 0 ? 24 : 16);
    st.boxes = sim.has(state, "records") ? 3 : 0; if (sim.has(state, "matrix")) st.boxes = 5;
    st.bolts = i >= 7 ? Math.min(14, (i - 6) * 2 + (sim.has(state, "skeleton") ? 2 : 0)) : 0;
    if (i >= 8) { st.score = 0.824; st.bar = 0.8; st.lower = sim.has(state, "proof") ? 0.791 : 0; st.slices = state.live ? 3 : 0; }
    st.bill = i >= 10 ? (state.bill || (state.flags.billOpen ? 3.4 : 4.4)) : 1.2;
    st.cancelled = i >= 9 && !state.flags.frozen ? 1 : 3;
    if (state.beat === "end" || i === 12) { var l = sim.ledger(data, state); st.value = Math.min(1, l.value / 3072); st.cost = Math.min(1, l.cost / 9000 + 0.2); }
    return st;
  }
  // today's people in today's room, the rest at their own desks
  var HOME = { priya: "product", arjun: "arch", sam: "eng", maya: "qa", lena: "platform", sponsor: "board", finance: "board",
               centre: "centre", agent: "centre", agent2: "centre", ops: "centre", legal: "board" };
  function whereabouts(state) {
    var rooms = {}, here = {}, k, day;
    if (state.beat !== "end") { day = sim.today(data, state); rooms[day.room] = day.with.slice(); day.with.forEach(function (w) { here[w] = 1; }); }
    for (k in HOME) if (!here[k]) (rooms[HOME[k]] = rooms[HOME[k]] || []).push(k);
    return rooms;
  }
  // a canvas at n screen pixels to an art pixel, never resampled
  function fit(cv, lw, lh, n) {
    if (cv.width !== lw || cv.height !== lh) { cv.width = lw; cv.height = lh; }
    cv.style.width = lw * n + "px"; cv.style.height = lh * n + "px";
    var g = cv.getContext("2d"); g.imageSmoothingEnabled = false; return g;
  }
  // the run, or on the title the day Start would open
  function now() { return run ? run.state : bookAt(chosen); }
  function draw() {
    var state = now(), st = picture(state), day = state.beat !== "end" ? sim.today(data, state) : null;
    var rooms = whereabouts(state), speaking = day && day.scene && day.scene[0] ? day.scene[0][0] : null, g, n, box, r;
    if (still || paused) { shut = gateShut(state); enter = 1; flash = 0; }
    // today's room at twice its size (on a phone its box crops it); the people walk in once
    if (sceneCv.parentNode && sceneCv.parentNode.clientWidth) {
      g = fit(sceneCv, A.W, A.H, 2);
      A.room(g, day ? day.room : "lobby", enter < 1 ? clock : 0, st, true, day ? rooms[day.room] : null, speaking, enter);
      if (flash > 0) { g.fillStyle = "rgba(222,138,138," + (0.5 * flash) + ")"; g.fillRect(0, 0, A.W, A.H); }
    }
    // the building, the apron and the sky: twice its size, or once on a phone
    if (mapCv.parentNode) {
      box = mapCv.parentNode.clientWidth || A.BW * 2;
      n = Math.max(1, Math.min(2, Math.floor(box / A.BW)));
      MAPW = Math.max(A.BW, Math.floor(box / n)); OX = (MAPW - A.BW) >> 1;
      g = fit(mapCv, MAPW, MAPH, n);
      A.sky(g, MAPW, MAPH, clock, st.sky);
      A.ground(g, MAPW, MAPH, GROUND, clock, st.sky);
      var mark = {}, i, d;
      for (i = 0; i < state.debts.length; i++) { d = state.debts[i]; if (d.state === "sealed") mark[data.days[sim.dayIndex(data, d.due)].room] = A.C.rose; }
      // on a phone a name would be five pixels tall: the key names the rooms
      A.building(g, OX, OY, clock, st, { active: day ? day.room : null, cast: rooms, speaking: speaking, mark: mark, enter: enter,
        shut: shut > 0 ? { eng: shut, qa: shut } : null, names: n > 1 });
      if (flash > 0 && day) { r = A.roomRect(day.room); g.fillStyle = "rgba(222,138,138," + (0.5 * flash) + ")"; g.fillRect(OX + r.x, OY + r.y, r.w, r.h); }
    }
  }
  // the loop rests while no canvas it would change is on the screen
  function seen() { return vis.map || (vis.scene && (enter < 1 || flash > 0)); }
  function loop(t) {
    raf = 0;
    if (still || paused || !seen() || document.hidden) return;
    if (t - last > 120) {
      clock += 8; last = t; window.NDFrames++;
      if (enter < 1) enter = Math.min(1, enter + 0.09);
      if (flash > 0) flash = Math.max(0, flash - 0.34);
      var want = gateShut(now()); if (shut > want) shut = Math.max(want, shut - 0.2); else shut = want;
      draw();
    }
    raf = requestAnimationFrame(loop);
  }
  function go() { if (!raf && !still && !paused && seen() && !document.hidden) raf = requestAnimationFrame(loop); }
  function arrive() { enter = still ? 1 : 0; }     // a day opens: today's people walk into its room, once
  // the build floors stay shut until the sign-off is dealt with
  function gateShut(state) { return state.beat === "end" ? 0 : (state.i < 5 || (state.i === 5 && state.beat !== "done") ? 1 : 0); }
  document.addEventListener("visibilitychange", go);
  window.addEventListener("resize", function () { draw(); pin(); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (en) { en.forEach(function (e) { vis[e.target === mapCv ? "map" : "scene"] = e.isIntersecting; }); go(); });
    io.observe(mapCv); io.observe(sceneCv);
  }

  /* ------------------------------------------------------------------ the building's key
     A button per room, its line of the key: the room, its person, their days. Its card opens on the person. */
  var ROOMS = ["board", "product", "arch", "eng", "qa", "platform", "centre"], CENTRE = "240 stranded passengers a day. 38 minutes each, by hand.";
  function keeper(id) { for (var k in HOME) if (HOME[k] === id && who(k).title) return k; return null; }     // whose room it is
  function list(ns) { return ns.length < 2 ? String(ns[0]) : ns.slice(0, -1).join(", ") + " and " + ns[ns.length - 1]; }
  function dayNs(ns) { return (ns.length > 1 ? "Days " : "Day ") + list(ns); }
  function held(ns, where) { return " " + dayNs(ns) + (ns.length > 1 ? " are" : " is") + " held " + where + "."; }
  function daysOf(id) { var k = keeper(id); return data.days.filter(function (d) { return d.room === id || d.owner === k; }).map(function (d) { return d.day; }); }
  function person(id) {
    var k = keeper(id), p = k && who(k), mine, away = {}, out, x;
    if (!p || !data.roles[p.role]) {
      out = !p ? CENTRE : p.name + ", the " + lower(p.title) + ", sits here with " + list(Object.keys(HOME).filter(function (j) { return HOME[j] === id && j !== k; }).map(function (j) { return "the " + lower(who(j).name); })) + ".";
      return out + held(daysOf(id), "here");
    }
    mine = data.days.filter(function (d) { return d.owner === k; });
    out = p.name + ", " + lower(p.title) + ", makes the call" + (mine.length > 1 ? "s on " : " on ") + dayNs(mine.map(function (d) { return d.day; })) + ".";
    mine.forEach(function (d) { if (d.room !== id) (away[d.room] = away[d.room] || []).push(d.day); });
    for (x in away) out += held(away[x], "in the " + lower(data.rooms[x]));
    return out;
  }
  function roomName(id) { return data.rooms[id].replace(/ room$/, ""); }
  function roomCard(id, state) {
    var lines = [person(id)], act = null, i, b;
    if (!state) return { lines: lines };
    i = state.i;
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
      lines.push(i < 7 ? "Nothing is built. The sign-off is on Day 15." : sim.has(state, "skeleton") ? "The thin slice runs end to end. One unknown is retired each day." : "The build is under way.");
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
    } else lines.push(i >= 9 && state.live ? "The assistant handles the cases that shipped. People handle the rest." : "Every case is handled by a person.");
    return { lines: lines, act: act };
  }
  // the three marks, each beside a scrap of the building
  function marks() {
    return el("ul", { "class": "nd-marks" }, ["lit", "shut", "owed"].map(function (k) {
      var cv = el("canvas", { width: 20, height: 12, "aria-hidden": "true" });
      A.mark(cv.getContext("2d"), k);
      return el("li", {}, [cv, data.building.marks[k]]);
    }));
  }
  // under the building: where today is, in words
  function where() {
    var s = now(), d;
    if (s.beat === "end") return "";
    d = sim.today(data, s);
    return (run ? "Today" : "Day " + d.day) + ": the " + lower(data.rooms[d.room]) + ", " + data.building.floors[A.PLAN.filter(function (p) { return p.id === d.room; })[0].floor];
  }

  /* ------------------------------------------------------------------ doing things */
  function act(action) {
    var before = run.state, next = sim.reduce(data, before, action);
    if (next === before) return;
    run.state = next; if (action.t !== "ask") asking = false;
    if (action.t === "next") { arrive(); looking = null; if (!still && next.events.some(function (e) { return e.kind === "incident"; })) flash = 1; }
    if (still) shut = gateShut(next);
    answering = true;             // the answer to a press
    render(action.t === "next" ? "day" : action.t === "ask" ? "ask" : "out");
    save(); unlink();             // saved only once the screen for it exists
    flyPins(next.debts.slice(before.debts.length).filter(function (d) { return d.state === "sealed"; }).map(function (d) { return d.due; }));
    answering = false;
    var bits = [];
    if (next.slack !== before.slack) bits.push("Runway " + runwayText(next.slack) + ".");
    if (next.trust !== before.trust) bits.push("Trust " + next.trust + " of " + next.trustMax + ".");
    if (next.tokens !== before.tokens) bits.push(questions(next.tokens) + " left.");
    live.textContent = bits.join(" ");
    go();
  }
  function undoDay() {            // back to the start of today
    var h = run.state.history.slice();
    while (h.length && h[h.length - 1].t !== "next") h.pop();
    run.state = sim.fold(data, run.opts, h); asking = false; render("day"); save();
  }
  function start(opts) {
    run = { opts: opts, state: sim.init(data, opts) }; looking = null; asking = false; shown = {};
    shut = 1; arrive(); render("day"); save(); go();
  }
  function questions(n) { return n === 1 ? "1 question" : n + " questions"; }
  function runwayText(n) { return n >= 0 ? days(n) + " left" : days(-n) + " late"; }

  /* ------------------------------------------------------------------ a link to a day
     #day-45 opens Day 45 on a fresh run, the days before it played by the book, never over a save unasked;
     #day-45-qa opens it in that one role. */
  function linked() {             // { i, role } or null
    var m = /^#day-(\d+)(?:-([a-z]+))?$/.exec(location.hash || ""), i;
    for (i = 0; m && i < data.days.length; i++) if (data.days[i].day === +m[1] && (!m[2] || (data.roles[m[2]] || {}).who)) return { i: i, role: m[2] };
    return null;
  }
  function unlink() { try { if (/^#day-/.test(location.hash)) history.replaceState(null, "", location.pathname + location.search); } catch (e) { /* the address stays */ } }
  function openAt(i, replace, role) {
    run = { opts: wayAt(i, role), state: bookAt(i, role) }; looking = null; asking = false; shown = {};
    shut = gateShut(run.state); arrive(); render("day");
    if (replace) { save(); unlink(); }
    go();
  }
  function resume(saved) { run = { opts: saved.opts, state: sim.fold(data, saved.opts, saved.history) }; shown = {}; render("day"); unlink(); go(); }
  function savedDay(saved) { return data.days[Math.min(data.days.length - 1, saved.history.filter(function (a) { return a.t === "next"; }).length)].day; }
  function boot() {               // on load, and when the address changes under the page
    var l = linked(), saved = load();
    run = null; looking = null; asking = false;
    if (l && !(saved && saved.history.length)) openAt(l.i, false, l.role);
    else render("title");
  }

  /* ------------------------------------------------------------------ pieces of the panel */
  // the top of the panel: the room, the thirteen days, the meters (the style sheet places the room)
  function hud(state) {
    var strip = el("ol", { "class": "nd-strip", "aria-label": "The thirteen days" }), i, d, cls, due, meters, mine, ahead = aheadLine(state);
    for (i = 0; i < data.days.length; i++) {
      d = data.days[i]; cls = i < state.i || state.beat === "end" ? "was" : i === state.i ? "now" : "";
      due = state.debts.filter(function (x) { return x.due === d.id && x.state === "sealed"; }).length;
      mine = state.mode === "role" && sim.mine(data, state, d);
      strip.appendChild(el("li", { "class": cls + (due ? " owed" : "") + (mine ? " mine" : ""), "data-day": d.id, "aria-current": cls === "now" ? "step" : null, style: "--c:var(--dg-" + HUE[d.phase] + ")" },
        [el("span", { text: String(d.day) }), mine ? el("span", { "class": "vh", text: " (your call)" }) : null,
          due ? el("i", { title: due === 1 ? "Something comes due" : due + " things come due" }, [el("span", { "class": "vh", text: " (something comes due)" })]) : null]));
    }
    var track = el("div", { "class": "nd-days" }, [phaseNames("nd-phases"), strip, ahead ? el("p", { "class": "nd-ahead", text: ahead }) : null]);
    var pips = el("span", { "class": "nd-pips", "aria-hidden": "true" });
    for (i = 0; i < state.trustMax; i++) pips.appendChild(el("i", { "class": i < state.trust ? "on" : "" }));
    meters = el("dl", { "class": "nd-meters" }, [
      el("div", { "class": state.slack < 0 ? "bad" : "" }, [el("dt", { text: "Runway" }), el("dd", { text: runwayText(state.slack) })]),
      el("div", {}, [el("dt", { text: "Sponsor's trust" }), el("dd", {}, [pips, el("span", { "class": "vh", text: state.trust + " of " + state.trustMax })])]),
      el("div", {}, [el("dt", { text: "On file" }), el("dd", { text: state.shelf.length + " of " + Object.keys(data.artefacts).length })]),
      state.mode !== "team" ? el("div", {}, [el("dt", { text: "Questions" }), el("dd", { text: state.tokens + " left" })]) : null]);
    return el("div", { "class": "nd-hud" }, [el("div", { "class": "nd-scene" }, [sceneCv]), track, meters]);
  }
  // the phases as runs of day indexes
  function runs() {
    var out = [], from = 0, i;
    for (i = 1; i <= data.days.length; i++) if (i === data.days.length || data.days[i].phase !== data.days[from].phase) { out.push({ p: data.days[from].phase, a: from, b: i - 1 }); from = i; }
    return out;
  }
  function phaseNames(cls) {
    return el("div", { "class": cls, "aria-hidden": "true" }, runs().map(function (r) {
      return el("span", { style: "grid-column:" + (r.a + 1) + "/" + (r.b + 2) + ";--a:" + r.a, text: data.phases[r.p].name });
    }));
  }
  // the next milestone from today
  function aheadLine(state) {
    for (var i = state.i; i < data.days.length; i++) {
      var m = MILE[data.days[i].id];
      if (m) return i === state.i ? "Today: " + m.name : "Next: " + m.name + ", Day " + data.days[i].day;
    }
    return "";
  }
  // in one role, and as the sponsor: who the player is
  function whoLine(state) {
    if (state.mode === "role") return el("p", { "class": "nd-you-are" }, [el("b", { text: "You are " + who(data.roles[state.role].who).name + ", the " + lower(data.roles[state.role].name) + ". " }), data.roles[state.role].line]);
    if (state.mode === "org") return el("p", { "class": "nd-you-are" }, [el("b", { text: "You are Ines, the sponsor. " }), "The team makes each call. You may ask to see the evidence behind " + NUM[data.rules.questions.org] + " of them."]);
    return null;
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
  // one answer, on the title's card and on every day: the words, and the price in plain mono
  function answer(label, price, press, key) {
    return el("button", { type: "button", "class": "nd-opt", "data-key": key, onclick: press }, [el("span", { "class": "nd-opt-l", text: label }), el("span", { "class": "nd-opt-p", text: price })]);
  }
  function optionButtons(state, day, handler, skip, legend) {
    var set = el("fieldset", { "class": "nd-opts" + (legend ? " alt" : "") }, [el("legend", { text: legend || day.ask })]);
    day.options.forEach(function (o, n) {
      if (o.id === skip) return;
      var p = sim.price(data, state, day, o);
      set.appendChild(answer(o.label, p ? days(p) : "no days", function () { handler(o); }, String(n + 1)));
    });
    set.addEventListener("keydown", function (e) {            // keys 1 to 3, while the focus is in the list
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
    var box = el("div", { "class": "nd-out", tabindex: "-1" }), sealed;
    state.events.forEach(function (e) {
      if (e.kind === "choice") box.appendChild(el("p", { "class": "nd-you" }, [el("b", { text: e.label }), el("em", { text: e.days ? days(e.days) : "no days" })]));
      if (e.kind === "choice" || e.kind === "task" || e.kind === "gate" || e.kind === "fix" || e.kind === "repair" || e.kind === "move")
        box.appendChild(el("p", { "class": "ev-" + e.kind }, [e.text, e.kind !== "choice" && e.days ? el("em", { text: " " + days(e.days) + "." }) : null,
          e.trust > 0 ? el("em", { text: " Trust falls by " + e.trust + "." }) : e.trust < 0 ? el("em", { text: " Trust rises." }) : null]));
    });
    // what today left sealed, by the day it comes due
    sealed = [];
    state.debts.forEach(function (x) { if (x.id === day.id && x.state === "sealed" && sealed.indexOf(x.dueDay) < 0) sealed.push(x.dueDay); });
    sealed.sort(function (a, b) { return a - b; });
    if (sealed.length) box.appendChild(el("p", { "class": "nd-sealed" }, [el("i", { "aria-hidden": "true" }),
      "Something is pinned to " + sealed.map(function (n, k) { return (k && k === sealed.length - 1 ? "and " : "") + "Day " + n; }).join(sealed.length > 2 ? ", " : " ") + "."]));
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

  /* ------------------------------------------------------------------ four small simulations
     Each plays once, as the answer to a press and only on screen; the timings are in game.css. */
  function once(name) {           // first time today, as the answer to a press
    var k = run.state.i + ":" + name, first = !shown[k];
    shown[k] = 1;
    return first && answering && !still;
  }
  var BAR = 60, TOP = 84;         // the foot of the site's bar; where an answer's top goes
  function inView(n) { var r = n.getBoundingClientRect(); return r.top >= BAR && r.bottom <= window.innerHeight && r.height > 0; }
  // the top of something just under the bar, at once
  function jump(n) { window.scrollTo({ top: Math.max(0, window.scrollY + n.getBoundingClientRect().top - TOP), behavior: "instant" }); }
  // a figure not whole on the screen when it would start is shown finished
  function settleFigures() {
    panel.querySelectorAll(".nd-sim.nd-go").forEach(function (f) { if (!inView(f)) f.classList.remove("nd-go"); });
  }
  // Day 45: one score becomes three columns, each as wide as its share of the cases
  function splitFigure(state, t, bars) {
    var n = 0, right = 0, plot = el("div", { "class": "nd-split-plot" }), names = el("div", { "class": "nd-split-names" });
    t.slices.forEach(function (s) { n += s.n; right += s.right; });
    t.slices.forEach(function (s, k) {
      var st = sim.sliceStats(s);
      plot.appendChild(el("div", { "class": "nd-split-col", style: "flex:" + s.n + " 0 0;--s:" + st.score + ";--l:" + st.lower + ";--b:" + bars[s.id] + ";--a:" + (100 * right / n) }, [
        el("i", { "class": "nd-split-fill" }), el("i", { "class": "nd-split-whisk" }), el("i", { "class": "nd-split-bar" }), el("b", { text: String(st.score) })]));
      names.appendChild(el("span", { style: "flex:" + s.n + " 1 0" }, [el("b", { text: s.short }), el("i", { text: s.n + " cases" })]));
    });
    plot.appendChild(el("span", { "class": "nd-split-one", style: "--a:" + (100 * right / n), text: (Math.round(1000 * right / n) / 10) + " on all " + n }));
    return el("div", { "class": "nd-sim nd-split" + (once("split") ? " nd-go" : "") }, [
      el("div", { "aria-hidden": "true" }, [plot, names]),
      el("p", { "class": "nd-cap" }, ["One score is three scores. Each column is as wide as its share of the " + n + " cases. ",
        el("i", { "class": "nd-key bar", "aria-hidden": "true" }), "the bar ", el("i", { "class": "nd-key whisk", "aria-hidden": "true" }), "the least the score could be"])]);
  }
  // Day 75: the habits multiply the bill; a fix ticked takes its factor out
  function billFigure(t) {
    var plot = el("div", { "class": "nd-bill-plot" }), labs = el("div", { "class": "nd-bill-labs" }), total = el("b"), segs = [], whole = 1, fig, rest = el("i");
    t.rows.forEach(function (r) { whole *= r.factor; });
    [{ id: "", factor: 1, name: "estimate" }].concat(t.rows).forEach(function (r, k) {
      var seg = el("i", { "class": "nd-bill-seg" + (k ? " f" + k : " est"), style: "--k:" + k }), lab = el("span", { style: "--k:" + k, text: k ? "×" + r.factor : "estimate" });
      plot.appendChild(seg); labs.appendChild(lab); segs.push({ row: r, seg: seg, lab: lab });
    });
    labs.appendChild(rest);
    fig = el("div", { "class": "nd-sim nd-bill" + (once("bill") ? " nd-go" : ""), "aria-hidden": "true" }, [
      el("p", { "class": "nd-bill-top" }, [el("span", { text: "The bill, as a multiple of the estimate" }), total]), plot, labs]);
    fig.paint = function (off) {             // `off` is the list of fixes ticked
      var at = 0;
      segs.forEach(function (x, k) {
        var gone = k && off.indexOf(x.row.id) >= 0, from = at, to = k ? (gone ? at : at * x.row.factor) : 1;
        x.seg.style.transform = "translateX(" + (100 * from / whole) + "%) scaleX(" + Math.max(0, (to - from) / whole) + ")";
        x.seg.classList.toggle("gone", !!gone); x.lab.classList.toggle("gone", !!gone);
        // a label is never narrower than itself, so no two print on each other
        x.lab.style.flex = gone ? "0 0 0" : (to - from) + " 1 0";
        at = to;
      });
      rest.style.flex = Math.max(0, whole - at) + " 1 0";
      total.textContent = (Math.round(at * 100) / 100) + " times";
    };
    fig.paint([]);
    return fig;
  }
  // Day 82: the $400 limit as paper (the prompt) or as a wall (the tool)
  function refundStrip(day) {
    var paid = day.form === "paid";
    return el("div", { "class": "nd-sim nd-pw " + (paid ? "nd-pw-paid" : "nd-pw-held") + (once("refund") ? " nd-go" : "") }, [
      el("div", { "class": "nd-pw-row", "aria-hidden": "true" }, [
        el("span", { "class": "nd-pw-end from", text: "The assistant" }),
        el("span", { "class": "nd-pw-track" }, [el("i", { "class": "nd-pw-run" }, [el("b", { text: "$2,000" })]), el("i", { "class": "nd-pw-stop" }),
          el("em", { text: paid ? "the prompt" : "the tool" })]),
        el("span", { "class": "nd-pw-end to", text: "The passenger" })]),
      el("p", { "class": "nd-cap", text: day.variants[day.form].fig })]);
  }
  // a pinned debt: a rose pin flies from the outcome line to its day on the strip
  function flyPins(due) {
    var from = panel.querySelector(".nd-sealed i"), seen = {}, n = 0, spring;
    if (still || !from || !from.animate || !due.length || !inView(from)) return;
    try { spring = getComputedStyle(root).getPropertyValue("--spring").trim() || "ease-out"; } catch (e) { spring = "ease-out"; }
    due.forEach(function (id) {
      var to = panel.querySelector('.nd-strip li[data-day="' + id + '"] i'), a, b, pin, fly;
      // only to a day on the screen
      if (seen[id] || !to || !inView(to.parentNode)) return;
      seen[id] = 1; a = from.getBoundingClientRect(); b = to.getBoundingClientRect();
      pin = el("i", { "class": "nd-pin", "aria-hidden": "true", style: "left:" + (a.left + window.scrollX) + "px;top:" + (a.top + window.scrollY) + "px;width:" + a.width + "px;height:" + a.height + "px" });
      document.body.appendChild(pin); to.classList.add("nd-wait");
      fly = pin.animate([{ transform: "translate(0,0) scale(1)", opacity: 1 }, { transform: "translate(" + (b.left - a.left + (b.width - a.width) / 2) + "px," + (b.top - a.top + (b.height - a.height) / 2) + "px) scale(" + (b.width / a.width) + ")", opacity: 1 }],
        { duration: 520, delay: n * 380, easing: "cubic-bezier(.22,1,.36,1)", fill: "both" });
      fly.onfinish = function () {
        pin.remove(); to.classList.remove("nd-wait");
        try { to.animate([{ transform: "scale(1.8)" }, { transform: "scale(1)" }], { duration: 400, easing: spring }); } catch (e) { /* an old browser: the pin is simply there */ }
      };
      n++;
    });
  }

  /* ------------------------------------------------------------------ the six tasks */
  function taskForm(state, id) {
    var t = data.tasks[id], box = el("form", { "class": "nd-task", onsubmit: function (e) { e.preventDefault(); } }), submit, status = el("p", { "class": "nd-status", role: "status" });
    box.appendChild(el("h3", { text: t.title })); box.appendChild(el("p", { "class": "nd-intro", text: t.intro }));
    function done(label, get) {
      submit = el("button", { type: "submit", "class": "btn pri", text: label });
      box.appendChild(status); box.appendChild(submit);
      box.addEventListener("submit", guard(function () { var v = get(); if (v == null) return; act(state.beat === "choose" && state.pending ? { t: "challenge", input: v } : { t: "task", id: id, input: v }); }));
    }
    if (id === "limits") {
      // as a real limit is ticked, the target it bends is shown rewritten
      var bends = el("ul", { "class": "nd-bends", "aria-live": "polite" }), rest = el("p", { "class": "nd-count" });
      var sort = function () {
        var n = 0; bends.innerHTML = "";
        t.lines.forEach(function (ln) {
          if (!box.querySelector("#lm-" + ln.id).checked) return;
          n++; if (ln.bends) bends.appendChild(el("li", {}, [el("b", { text: ln.limit + ". " }), ln.bends]));
        });
        rest.textContent = (n ? n + " ticked. " : "Nothing ticked yet. ") + (t.lines.length - n) + " of the six " + (t.lines.length - n === 1 ? "goes" : "go") + " to the Day 9 workshop.";
        status.textContent = "";
        return n;
      };
      t.lines.forEach(function (ln) {
        box.appendChild(el("label", { "class": "nd-check big", "for": "lm-" + ln.id }, [el("input", { type: "checkbox", id: "lm-" + ln.id, value: ln.id, onchange: sort }), el("span", { text: ln.text })]));
      });
      box.appendChild(el("p", { "class": "nd-k", text: "What each limit does to a target" })); box.appendChild(bends); box.appendChild(rest); sort();
      done("File the limits", function () {
        var out = []; box.querySelectorAll("input:checked").forEach(function (c) { out.push(c.value); });
        if (!out.length) { status.textContent = "Nothing is ticked. Tick each line that nobody here can change in ninety days."; return null; }
        return out;
      });
    } else if (id === "bar") {
      var hold = el("input", { type: "checkbox", id: "nd-hold" }), tb = el("tbody");
      var paint = function () {
        tb.innerHTML = "";
        t.slices.forEach(function (s) {
          var dmg = hold.checked && s.damageHeld != null ? s.damageHeld : s.damage, bar = sim.barOf(s, hold.checked);
          tb.appendChild(el("tr", {}, [el("th", { scope: "row", text: s.name }), el("td", { text: "$" + s.saving }), el("td", { text: "$" + dmg }),
            el("td", { "class": bar > 95 ? "hot" : "" }, [el("b", { text: bar + "%" }), el("i", { style: "--w:" + bar + "%" })])]));
        });
      };
      hold.addEventListener("change", guard(paint)); paint();
      box.appendChild(el("table", { "class": "nd-tb" }, [el("thead", {}, [el("tr", {}, [el("th", { scope: "col", text: "Kind of case" }), el("th", { scope: "col", text: "Right saves" }),
        el("th", { scope: "col", text: "Wrong costs" }), el("th", { scope: "col", text: "The bar" })])]), tb]));
      box.appendChild(el("label", { "class": "nd-check", "for": "nd-hold" }, [hold, el("span", { text: t.hold })]));
      done("Sign the bars", function () { return { hold: hold.checked }; });
    } else if (id === "score") {
      var bars = sim.bars(data, state);
      box.appendChild(splitFigure(state, t, bars));
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
      var sum = el("p", { "class": "nd-count", role: "status" }), bill = billFigure(t);
      var calc = function () {
        var m = 4.4, d = 0, off = []; t.rows.forEach(function (r) { if (box.querySelector("#lk-" + r.id).checked) { m /= r.factor; d += r.days; off.push(r.id); } });
        bill.paint(off);
        sum.textContent = (d === 0 ? "Nothing chosen yet." : "Chosen: " + (d === 0.5 ? "half a day" : days(d)) + " of work.") + " The bill would be " + (Math.round(m * 100) / 100) + " times the estimate." + (d > t.budget ? " That is more than one day." : "");
        return d;
      };
      var tbl = el("tbody");
      t.rows.forEach(function (r) {
        tbl.appendChild(el("tr", {}, [
          el("th", { scope: "row" }, [el("label", { "class": "nd-check", "for": "lk-" + r.id }, [el("input", { type: "checkbox", id: "lk-" + r.id, onchange: calc }), el("span", { text: r.fix })])]),
          el("td", {}, [r.name + ": " + r.was + ", now " + r.now + " ", el("b", { text: "×" + r.factor })]), el("td", { text: r.days === 0.5 ? "half a day" : days(r.days) })]));
      });
      box.appendChild(bill);
      box.appendChild(el("table", { "class": "nd-tb stack" }, [el("thead", {}, [el("tr", {}, [el("th", { scope: "col", text: "Fix" }), el("th", { scope: "col", text: "What the log shows" }), el("th", { scope: "col", text: "Takes" })])]), tbl]));
      box.appendChild(sum); calc();
      done("Start the fixes", function () {
        if (calc() > t.budget) { status.textContent = "You have one day. Untick something."; return null; }
        var out = []; t.rows.forEach(function (r) { if (box.querySelector("#lk-" + r.id).checked) out.push(r.id); });
        if (!out.length) { status.textContent = "Pick at least one fix."; return null; }
        return out;
      });
    } else if (id === "slide") {
      var text = slideLines(state);
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

  function slideLines(state) {     // what the Day 90 slide could say
    var L = sim.ledger(data, state);
    return {
      saving: L.saving + " percent fewer person-days on stranded passengers: " + money(L.value),
      bill: "What it cost: a model bill of " + money(L.bill) + " and " + money(L.review) + " of review time",
      net: "This cycle, net: " + money(L.net) + ". Next cycle: review time under 30 hours",
      score: "82.4 percent right on 500 real cases",
      incident: state.incidents ? "One refund paid in error: $2,000" : "No money paid out in error",
      shelf: state.shelf.length + " documents on file"
    };
  }

  function gatePanel(state) {
    var miss = sim.gateMissing(state), box = el("div", { "class": "nd-gate" }), lamps = el("ul", { "class": "nd-lamps" });
    ["spec", "bar", "budget"].forEach(function (a) {
      var on = sim.has(state, a);
      lamps.appendChild(el("li", { "class": on ? "on" : "" }, [el("i", { "aria-hidden": "true" }), el("b", { text: data.artefacts[a].name }), el("span", { text: on ? "signed" : "missing" })]));
    });
    box.appendChild(el("h3", { text: "The sign-off" }));
    box.appendChild(el("p", { "class": "nd-intro", text: data.days[state.i].signoff }));
    box.appendChild(lamps);
    if (!miss.length) box.appendChild(el("div", { "class": "nd-acts" }, [el("button", { type: "button", "class": "btn pri", text: "Sign and start the build", onclick: function () { act({ t: "gate", how: "pass" }); } })]));
    else box.appendChild(el("div", { "class": "nd-acts" }, [
      answer("Hold the build and write what is missing", days(2 * miss.length), function () { act({ t: "gate", how: "hold" }); }),
      answer("Start the build with what is on file", "no days", function () { act({ t: "gate", how: "open" }); })]));
    return box;
  }

  /* ------------------------------------------------------------------ the side column: debts, the date, a room */
  function side(state) {
    var box = el("div", { "class": "nd-side" }), sealed = state.debts.map(function (d, i) { return { d: d, i: i }; }).filter(function (x) { return x.d.state === "sealed"; });
    if (sealed.length && state.mode !== "org") {
      var ul = el("ul", { "class": "nd-debts" });
      var back = {};                               // one way back per day, however many things that day left
      sealed.forEach(function (x) {
        var c = sim.repairCost(data, x.d), first = !back[x.d.id]; back[x.d.id] = 1;
        ul.appendChild(el("li", {}, [el("span", {}, [el("b", { text: "Day " + x.d.dueDay + ". " }), "From Day " + x.d.from + ": " + x.d.tag + "."]),
          first ? el("button", { type: "button", "class": "btn ghost sm", onclick: function () { act({ t: "repair", debt: x.i }); } }, ["Go back to Day " + x.d.from + " and do it properly ", el("em", { text: days(c) })]) : null]));
      });
      box.appendChild(el("div", { "class": "nd-owed" }, [el("p", { "class": "nd-k", text: sealed.length === 1 ? "One thing comes due" : sealed.length + " things come due" }), ul]));
    }
    if (!state.moved && state.mode !== "org" && state.beat !== "end") {
      var m = data.rules.moveDate, ok = state.shelf.length >= m.evidence;
      box.appendChild(el("div", { "class": "nd-move" }, [
        el("button", { type: "button", "class": "btn ghost sm", onclick: function () { act({ t: "move" }); } }, ["Ask Ines, the sponsor, to move the date ", el("em", { text: "+" + days(m.days) + ", once" })]),
        el("span", { text: ok ? "With " + state.shelf.length + " documents on file, she will agree without a question." : "With " + state.shelf.length + " on file, it will cost her trust. She agrees easily at " + m.evidence + "." })]));
    }
    box.appendChild(el("p", { "class": "nd-leave" }, [el("a", { href: "./", text: "Leave this run" }), el("span", { text: " It is saved, and you can carry on later." })]));
    return box;
  }
  function roomBox(state) {
    var chips = el("div", { "class": "nd-rooms", role: "group", "aria-labelledby": "nd-key" }), c, card;
    ROOMS.forEach(function (id) {
      var k = keeper(id), ns = daysOf(id);
      chips.appendChild(el("button", { type: "button", "class": "nd-chip" + (looking === id ? " on" : ""), "aria-pressed": looking === id ? "true" : "false", "data-room": id,
        onclick: function () { looking = looking === id ? null : id; lastRoom = id; render("look"); } },
        [el("i", { "aria-hidden": "true", style: "background:" + A.paint(id).hue }), el("span", {}, [el("b", { text: roomName(id) }), k ? " · " + who(k).name : null]),
          el("span", {}, [el("span", { "class": "vh", text: " · " }), (ns.length > 1 ? "Days " : "Day ") + ns.join(", ")])]));
    });
    var out = [el("p", { "class": "nd-k", id: "nd-key", text: data.building.key }), chips];
    if (looking) {
      c = roomCard(looking, state); card = el("div", { "class": "nd-card", tabindex: "-1", style: "--rc:" + A.paint(looking).hue }, [el("b", { text: roomName(looking) })]);
      c.lines.forEach(function (l) { card.appendChild(el("p", { text: l })); });
      if (c.act) card.appendChild(answer(c.act.label, days(c.act.days), function () { act({ t: c.act.t }); }));
      out.push(card);
    }
    out.push(marks());
    return el("div", { "class": "nd-look" }, out);
  }

  /* ------------------------------------------------------------------ screens */
  // the head of a day, for a reader who has seen no other day
  var HUE = ["slate", "indigo", "teal", "amber"];
  function dayHead(state, day) {
    var so = sim.soFar(data, state), from = run.opts.from || 0;
    return el("div", { "class": "nd-dayhead", style: "--c:var(--dg-" + HUE[day.phase] + ")" }, [
      el("p", { "class": "nd-kick" }, [el("i", { "aria-hidden": "true" }), "Day " + day.day + " of 90", el("span", { text: " · " + data.phases[day.phase].name }), " · " + data.rooms[day.room]]),
      el("h2", { tabindex: "-1", text: "Day " + day.day + ". " + day.head }),
      el("p", { "class": "nd-ctx" }, [el("span", { text: data.short + " " }), day.context]),
      so.text ? el("p", { "class": "nd-sofar" }, [el("b", { text: so.label + " " }), so.text]) : null,
      from > 0 && state.i === from ? el("p", { "class": "nd-book", text: (from === 1 ? "Day 1 was " : "Days 1 to " + data.days[from - 1].day + " were ") + data.line.book +
        (state.role && bookAt(from, state.role).tokens < data.rules.questions.role ? " " + data.line.asked + (sim.mine(data, state, data.days[data.days.length - 1]) ? "" : " " + data.line.kept) : "") }) : null]);
  }
  // the header's pill: "Read the lesson" on a day with a lesson, else "The tutorial"; both labels sit
  // in it, one showing, so it never changes width
  function twoLabels(span, labels, on, icon) {
    if (!span) return;
    if (!span.querySelector(".nd-two")) {
      span.textContent = "";
      span.appendChild(el("span", { "class": "nd-two" }, labels.map(function (t) { return el("span", {}, [icon ? icon.cloneNode(true) : null, t]); })));
    }
    Array.prototype.forEach.call(span.querySelector(".nd-two").children, function (c, k) {
      c.style.visibility = k === on ? "" : "hidden";
      if (k === on) { c.removeAttribute("aria-hidden"); c.setAttribute("data-on", ""); } else { c.setAttribute("aria-hidden", "true"); c.removeAttribute("data-on"); }
    });
  }
  function pill(day) {
    var a = document.querySelector("a.play[data-ctx-lesson]"), l = null, lg, sm;
    if (!a) return;
    ((day && day.deeper) || []).forEach(function (d) { if (!l && d[0] === "lesson") l = d; });
    lg = a.querySelector(".lg"); sm = a.querySelector(".sm");
    var icon = a.querySelector(":scope > svg");
    a.setAttribute("href", UP + (l ? l[1] : "learn/"));
    if (lg || sm) { twoLabels(lg, ["The tutorial", "Read the lesson"], l ? 1 : 0, icon); twoLabels(sm, ["Tutorial", "Lesson"], l ? 1 : 0, icon); }
    else twoLabels(a.querySelector(":scope > span"), ["The tutorial", "Read the lesson"], l ? 1 : 0, icon);
    if (icon) icon.remove();
    if (l) a.setAttribute("title", l[2]); else a.removeAttribute("title");
  }
  // the one pause control: the building is the only thing that loops
  function pauseControl() {
    var box = el("input", { type: "checkbox", autocomplete: "off", "data-motion-toggle": true, onchange: function (e) { paused = e.target.checked; draw(); go(); } });
    box.checked = paused;
    return el("label", { "class": "mpause nd-pause" }, [box, el("span", { "class": "vh", text: "Pause the animation" }), el("i", { "aria-hidden": "true" })]);
  }
  // the building: a caption, the picture, where today is, the pause control
  function stage() {
    return el("div", { "class": "nd-stage" }, [el("p", { "class": "nd-over", text: data.building.caption }), el("div", { "class": "nd-map" }, [mapCv]),
      el("div", { "class": "nd-stagebar" }, [el("p", { "class": "nd-k nd-where" }), still ? null : pauseControl()])]);
  }
  function place() { if (left) left.querySelector(".nd-where").textContent = where(); }
  // sticky beside the day; taller than the window, it stops with its foot in view
  function pin() { if (left) left.style.top = Math.min(84, innerHeight - left.offsetHeight - 16) + "px"; }

  // the title: the line above it (dayLine), Day 1's card; a link and a save get a choice of the two
  function titleScreen() {
    var saved = load(), b = best(), want = linked(), n = want && data.days[want.i].day;
    if (want && saved && saved.history.length) {        // a link and a save: the player says which
      return [el("div", { "class": "nd-title" }, [
        el("p", { "class": "nd-pitch", text: "This link opens Day " + n + (want.role ? " as " + who(data.roles[want.role].who).name : "") + ". You also have a run in progress, on Day " + savedDay(saved) + "." }),
        el("div", { "class": "nd-acts" }, [
          el("button", { type: "button", "class": "btn pri", text: "Carry on from Day " + savedDay(saved), onclick: function () { resume(saved); } }),
          el("button", { type: "button", "class": "btn ghost", text: "Open Day " + n + " on a fresh run", onclick: function () { openAt(want.i, true, want.role); } })]),
        el("p", { "class": "nd-best", text: "A fresh run replaces the one you have saved." })])];
    }
    lineWanted = true;
    return [el("div", { "class": "nd-title" }, [
      dayOne(),
      b ? el("p", { "class": "nd-best", text: "Your best ending so far: " + data.verdicts[b.key].name.toLowerCase() + "." }) : null])];
  }
  /* The other ways to play: a row per role and one for the sponsor, each one press. The words are each
     role's `card` in days.json. A role's days are links that start it there, and a late first call one more. */
  function ways() {
    var rows = el("div", { "class": "nd-rolebtns" });
    Object.keys(data.roles).forEach(function (r) {
      var R = data.roles[r], p = who(R.who), mine = data.days.filter(function (d) { return d.owner === R.who; }), when = [mine.length > 1 ? "Days " : "Day "], f = mine[0].day;
      var link = function (n, t) { return el("a", { href: "#day-" + n + "-" + r, "aria-label": t ? null : "Day " + n + " as " + p.name, text: t || String(n) }); };
      mine.forEach(function (d, k) { when.push(k ? ", " : "", link(d.day)); });
      rows.appendChild(wayRow(r, R.name, p.name + " · " + mine.length + (mine.length > 1 ? " calls" : " call"), R.card, mini(mine),
        when, "Play as " + p.name, function () { start({ mode: "role", role: r, seed: seed() }); }, f > 1 ? link(f, data.line.first.replace("{day}", f)) : null));
    });
    return el("section", { "class": "nd-ways", "aria-labelledby": "nd-ways-h" }, [
      el("p", { "class": "nd-k", id: "nd-ways-h", text: "Two other ways to play" }),
      el("h3", { text: "One role" }), el("p", { text: "Make your own calls. Watch your colleagues make theirs, and choose which " + NUM[data.rules.questions.role] + " to question." }), rows,
      el("h3", { text: "The organisation" }), el("p", { text: data.org.way }),
      el("div", { "class": "nd-orgrow" }, [wayRow("org", "The sponsor", who("sponsor").name + " · " + data.rules.questions.org + " questions", data.org.card, mini([]),
        ["Every day, watched"], "Set the rules", function () { render("org"); })])]);
  }
  function wayRow(id, name, sub, card, line, when, label, press, from) {
    var t = el("div", { "class": "nd-role-t", id: "nd-r-" + id }, [
      el("p", { "class": "nd-role-who" }, [el("b", { text: name }), el("span", { text: sub })]),
      el("p", { "class": "nd-role-says" }, [el("span", { text: card.decide }), el("span", { text: card.pick })]),
      el("p", { "class": "nd-role-days" }, [line, el("span", {}, when)]),
      el("p", { "class": "nd-role-takes" }, [el("span", { text: "You leave with " }), card.leave])]);
    return el("div", { "class": "nd-role" }, [t, el("button", { type: "button", "class": "btn ghost", "aria-describedby": t.id, text: label, onclick: press }), from]);
  }
  // the ninety-day line at 180px, your days in ink
  function mini(mine) {
    var m = el("span", { "class": "nd-mini", "aria-hidden": "true" }, [bands()]);
    data.days.forEach(function (d) { m.appendChild(el("i", { "class": mine.indexOf(d) >= 0 ? "on" : null, style: "left:" + pos(at(d.day)) })); });
    return m;
  }
  // Day 1 as the home page's card: an answer starts a whole-team run with that call made
  function dayOne() {
    var d = data.days[0], cv = el("canvas", { width: A.W, height: A.H, "aria-hidden": "true" }), g = cv.getContext("2d"), ol = el("ol", { "class": "dc-o" });
    g.imageSmoothingEnabled = false;
    A.room(g, d.room, 0, picture(bookAt(0)), true, d["with"], d.scene[0][0], 1);
    d.options.forEach(function (o) {
      ol.appendChild(el("li", {}, [answer(o.label, o.days ? days(o.days) : "no days", function () { start({ mode: "team", seed: seed() }); act({ t: "choose", opt: o.id }); })]));
    });
    return el("article", { "class": "daycard nd-d1", "aria-labelledby": "nd-d1-h", style: "--c:var(--dg-" + HUE[d.phase] + ")" }, [
      el("div", { "class": "dc-pic" }, [cv]),
      el("div", { "class": "dc-b" }, [
        el("p", { "class": "dc-k", text: "Day " + d.day + " of 90 · " + data.rooms[d.room] + " · " + data.line.card }),
        el("h2", { id: "nd-d1-h", text: d.head }),
        el("p", { "class": "dc-c", text: d.context }),
        el("p", { "class": "dc-q", text: d.ask }), ol])]);
  }

  /* ------------------------------------------------------------------ the ninety days, drawn to time
     Each day at (day − 1) / 89 of the width, each stop a link to its day. Pointing at or focusing a stop
     puts its headline in the caption and makes Start open it. One Tab stop; the arrow keys move along. */
  var lineWanted = false;         // set while the title is built: the line goes above it
  var chosen = 0;                 // the day Start opens: Day 1 until a stop is pointed at
  var booked = {};
  function at(day) { return (day - 1) / 89; }
  function pos(t) { return "calc(var(--pad) + (100% - 2 * var(--pad)) * " + t + ")"; }
  function span(t) { return "calc((100% - 2 * var(--pad)) * " + t + ")"; }
  function wayAt(i, role) { return { mode: role ? "role" : "team", role: role, seed: 0, from: i }; }
  function bookAt(i, role) {      // a fresh run at this day, by the book
    var k = i + (role || ""), o = wayAt(i, role);
    if (!booked[k]) booked[k] = sim.fold(data, o, sim.book(data, o, i));
    return booked[k];
  }
  function headOf(i) { return sim.today(data, bookAt(i)).head; }
  // the phases as bands, the seams halfway between phases (10.5, 25, 67.5)
  function bands(names) {
    var R = runs(), seams = [], bar = el("span", { "class": "nd-line-bar", "aria-hidden": "true" });
    R.forEach(function (r, k) { seams.push(k ? at((data.days[r.a - 1].day + data.days[r.a].day) / 2) : 0); });
    seams.push(1);
    R.forEach(function (r, k) {
      var st = (k === R.length - 1 ? "flex:1 1 0;" : "flex:none;width:" + (k ? span(seams[k + 1] - seams[k]) : pos(seams[1])) + ";") + "--c:var(--dg-" + HUE[r.p] + ")";
      if (names) names.appendChild(el("span", { style: st + ";--l:" + (k ? pos(seams[k]) : "0px"), text: data.phases[r.p].name }));
      bar.appendChild(el("i", { style: st }));
    });
    return bar;
  }
  function dayLine() {
    var saved = load(), going = saved && saved.history.length;
    chosen = 0;
    var names = el("div", { "class": "nd-line-ph", "aria-hidden": "true" }), bar = bands(names);
    var ol = el("ol", { "class": "nd-line-stops", "aria-label": "The thirteen days you can start at", "aria-describedby": "nd-line-keys" });
    data.days.forEach(function (d, i) {
      var m = MILE[d.id], key = i === 0 || !!m;
      var link = el("a", { href: "#day-" + d.day, "data-i": String(i), tabindex: i === chosen ? "0" : "-1",
        onpointerenter: function () { choose(i); }, onfocus: function () { choose(i); } },
        [el("i", { "aria-hidden": "true" }), el("span", { "class": "vh", text: "Day " }), el("b", { text: String(d.day) }), m ? el("em", { text: m.flag }) : null]);
      ol.appendChild(el("li", { "class": [key ? "key" : "", m ? "mile" : "", d.gate ? "gate" : "", i === chosen ? "on" : ""].join(" ").trim() || null,
        style: "left:" + pos(at(d.day)) + ";--c:var(--dg-" + HUE[d.phase] + ")" },
        [link, key ? null : el("span", { "class": "mk" }, [el("i", { "aria-hidden": "true" }), el("span", { "class": "vh", text: "Day " + d.day })])]));
    });
    ol.addEventListener("keydown", guard(function (e) {        // arrow keys, Home and End
      var step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1, Home: -99, End: 99 }[e.key], links, k;
      if (!step || e.altKey || e.ctrlKey || e.metaKey) return;
      links = Array.prototype.filter.call(ol.querySelectorAll("a"), function (a) { return a.getClientRects().length; });
      k = links.indexOf(document.activeElement); if (k < 0) return;
      e.preventDefault();
      links[Math.max(0, Math.min(links.length - 1, step === -99 ? 0 : step === 99 ? links.length - 1 : k + step))].focus();
    }));
    var go = el("button", { type: "button", "class": "btn " + (going ? "ghost" : "pri") + " nd-start", text: "Start at Day 1",
      onclick: function () { if (chosen > 0) openAt(chosen, true); else start({ mode: "team", seed: seed() }); } });
    return el("div", { "class": "nd-line" }, [
      el("div", { "class": "nd-line-map" }, [names, el("div", { "class": "nd-line-track" }, [bar, ol])]),
      el("p", { "class": "vh", id: "nd-line-keys", text: "The arrow keys move from day to day." }),
      el("div", { "class": "nd-line-foot" }, [
        el("p", { "class": "nd-line-cap", "aria-live": "polite", text: data.line.caption }),
        el("div", { "class": "nd-acts" }, [going ? el("button", { type: "button", "class": "btn pri", text: "Carry on from Day " + savedDay(saved), onclick: function () { resume(saved); } }) : null, go])])]);
  }
  function choose(i) {            // a stop pointed at or focused
    var line = root.querySelector(".nd-line"), d = data.days[i];
    if (!line) return;
    var head = headOf(i);
    chosen = i;
    Array.prototype.forEach.call(line.querySelectorAll(".nd-line-stops li"), function (li, k) { li.classList.toggle("on", k === i); });
    Array.prototype.forEach.call(line.querySelectorAll(".nd-line-stops a"), function (a) { a.setAttribute("tabindex", +a.getAttribute("data-i") === i ? "0" : "-1"); });
    line.querySelector(".nd-line-cap").textContent = "Day " + d.day + ". " + head;
    line.querySelector(".nd-start").textContent = "Start at Day " + d.day;
    shut = gateShut(bookAt(i)); draw(); place();      // and the building shows that day
  }
  function seed() { try { var n = +(localStorage.getItem(KEY + ".n") || 0); localStorage.setItem(KEY + ".n", String(n + 1)); return n; } catch (e) { return 0; } }

  function orgSetup() {
    var box = el("form", { "class": "nd-task nd-org", onsubmit: function (e) { e.preventDefault(); } }), status = el("p", { "class": "nd-status", role: "status" });
    box.appendChild(el("h2", { tabindex: "-1", text: "Three rules for the programme" }));
    box.appendChild(el("p", { "class": "nd-intro", text: data.org.intro }));
    data.policies.forEach(function (p) {
      box.appendChild(el("label", { "class": "nd-check big", "for": "po-" + p.id }, [el("input", { type: "checkbox", id: "po-" + p.id, value: p.id }), el("span", { text: p.name })]));
    });
    box.appendChild(status);
    box.appendChild(el("div", { "class": "nd-acts" }, [el("button", { type: "submit", "class": "btn pri", text: "Run the ninety days" }),
      el("button", { type: "button", "class": "btn ghost", text: "Back", onclick: function () { run = null; render("back"); } })]));
    box.addEventListener("submit", guard(function () {
      var set = []; box.querySelectorAll("input:checked").forEach(function (c) { set.push(c.value); });
      if (set.length > 3) { status.textContent = "Three at most. Untick " + (set.length - 3) + "."; return; }
      start({ mode: "org", policies: set, seed: seed() });
    }));
    return [box];
  }

  // a colleague's call, or the team's under the sponsor: the question is offered on sound and unsound
  // plans alike, costs one, and shows the evidence and nothing more
  function evidenceBox(state, own, ev) {
    var box = el("div", { "class": "nd-evidence", tabindex: "-1" }, [el("p", { "class": "nd-k", text: "The evidence" })]), text, ol;
    if (ev.slide) {
      text = slideLines(state); ol = el("ol");
      ev.slide.forEach(function (id) { ol.appendChild(el("li", { text: text[id] })); });
      box.appendChild(el("p", { text: "The slide, as " + own.name + " has it:" })); box.appendChild(ol);
      return box;
    }
    if (ev.doc) box.appendChild(el("p", {}, [el("b", { text: "Working from. " }), data.artefacts[ev.doc][ev.has ? "on" : "off"]]));
    box.appendChild(el("p", {}, [el("b", { text: "After today, on file. " }), ev.files.length ? ev.files.map(function (a) { return data.artefacts[a].name; }).join(" · ") : "Nothing new."]));
    return box;
  }
  function plan(state, day, own) {
    var org = state.mode === "org", planned = null, ev = state.seen ? sim.evidence(data, state) : null, p, card, out = [];
    var stand = el("button", { type: "button", "class": "btn pri", text: "Let it stand", onclick: function () { act({ t: "accept" }); } });
    if (day.options) planned = day.options.filter(function (x) { return x.id === state.pending; })[0];
    p = planned ? sim.price(data, state, day, planned) : 0;
    card = el("div", { "class": "nd-plan" }, [
      el("p", { "class": "nd-k", text: day.ask }),
      el("p", { "class": "nd-you" }, [el("b", { text: planned ? own.name + " plans: " + planned.label : own.name + " has a slide of three lines ready." }), planned ? el("em", { text: p ? days(p) : "no days" }) : null])]);
    if (ev) card.appendChild(evidenceBox(state, own, ev));
    out.push(card);
    if (!ev) {
      out.push(el("div", { "class": "nd-acts" }, [stand,
        state.tokens > 0 ? el("button", { type: "button", "class": "btn ghost", onclick: function () { act({ t: "ask" }); } }, ["Ask to see the evidence ", el("em", { text: state.tokens + " left" })])
          : el("span", { "class": "nd-note", text: "You have no questions left." })]));
    } else if (day.options) {
      out.push(el("div", { "class": "nd-acts" }, [stand]));
      out.push(optionButtons(state, day, function (opt) { act({ t: "challenge", opt: opt.id }); }, state.pending, org ? "Or send the team back to do this instead" : "Or ask for this instead"));
    } else if (asking) {                          // Day 90, in one role: the player builds the slide
      out.push(taskForm(state, day.task));
      out.push(el("div", { "class": "nd-acts" }, [stand]));
    } else {
      out.push(el("div", { "class": "nd-acts" }, [stand,
        org ? el("button", { type: "button", "class": "btn ghost", text: "Send it back for the cost and the net", onclick: function () { act({ t: "challenge" }); } })
          : el("button", { type: "button", "class": "btn ghost", text: "Build the slide yourself", onclick: function () { asking = true; render("stay"); } })]));
    }
    return out;
  }

  // the day as one card on the home page's metrics; the debts and the date under it
  function playScreen(state) {
    var day = sim.today(data, state), top = [], kids = [], own = who(day.owner), o, w = whoLine(state);
    if (w) top.push(w);
    top.push(hud(state));
    kids.push(dayHead(state, day));
    var ev = eventList(state); if (ev) kids.push(ev);
    // Day 82's figure follows the call, so the question and its first option stay on the first screen
    var fig = day.form ? refundStrip(day) : null;
    if (state.beat === "choose") {
      kids.push(sceneLines(day));
      if (state.pending) plan(state, day, own).forEach(function (k) { kids.push(k); });
      else if (day.options) kids.push(optionButtons(state, day, function (opt) { act({ t: "choose", opt: opt.id }); }));
      else kids.push(taskForm(state, day.task));
      if (fig) kids.push(fig);
    } else {
      kids.push(outcome(state, day));
      if (fig) kids.push(fig);
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
    return top.concat(el("div", { "class": "nd-day" }, kids), side(state));
  }
  function runOut() {              // the sponsor lets the rest play
    var s = run.state, steps = 0, n;
    while (s.beat !== "end" && steps++ < 200) { n = sim.reduce(data, s, s.beat === "choose" ? { t: "accept" } : { t: "next" }); if (n === s) break; s = n; }
    run.state = s; render("day"); save();
  }

  function endScreen(state) {
    var v = sim.verdict(data, state), V = data.verdicts[v.key], L = sim.ledger(data, state), kids = [], b = best();
    try { if (!b || RANK[v.key] > RANK[b.key]) localStorage.setItem(BEST, JSON.stringify({ key: v.key, mode: state.mode })); } catch (e) { /* no storage */ }
    clearSave();
    kids.push(el("div", { "class": "nd-verdict v-" + v.key }, [el("p", { "class": "nd-k", text: "Day 90 of 90 · The committee decides" }), el("h2", { tabindex: "-1", text: V.name }), el("p", { text: V.line })]));
    // the saving is the run's own; the line under it says why
    var why = [L.liveDays ? "live for " + L.liveDays + " of " + L.of + " days" : "never live inside the ninety days"];
    if (L.off) why.push("off for a week"); if (L.held) why.push("held back for one bar");
    if (L.unshipped) why.push("same-day cases kept with people"); if (L.redone) why.push("some cases done again by people");
    kids.push(el("dl", { "class": "nd-meters end" }, [
      el("div", { "class": v.late ? "bad" : "" }, [el("dt", { text: "The date" }), el("dd", { text: v.late ? days(v.late) + " late" : "met, " + days(state.slack) + " to spare" })]),
      el("div", {}, [el("dt", { text: "Sponsor's trust" }), el("dd", { text: state.trust + " of " + state.trustMax })]),
      el("div", {}, [el("dt", { text: v.key === "stopped" ? "Saved, before it was stopped" : "Saved" }), el("dd", { text: L.days + " person-days, " + money(L.value) }), el("dd", { "class": "nd-sub", text: why.join(", ") })]),
      el("div", {}, [el("dt", { text: "Spent" }), el("dd", { text: money(L.cost) }), el("dd", { "class": "nd-sub", text: "model " + money(L.bill) + ", review " + money(L.review) + (L.mishaps ? ", refunds " + money(L.mishaps) : "") })]),
      el("div", { "class": L.net < 0 ? "bad" : "" }, [el("dt", { text: "Net, first cycle" }), el("dd", { text: money(L.net) })])]));
    // the thirteen calls, each with what it came back as
    var rows = el("tbody");
    data.days.forEach(function (d) {
      var form = d.variants ? d.variants[state.incidents ? "paid" : "blocked"] : d, pick = state.picks[d.id], opt = null, debt, back = "", ok, sl = state.slide || [];
      if (form.options) form.options.forEach(function (o) { if (o.id === pick) opt = o; });
      debt = state.debts.filter(function (x) { return x.id === d.id; });
      debt.forEach(function (x) { back += (back ? " " : "") + (x.state === "fired" ? "Came back on Day " + x.dueDay + ": " + (x.days ? days(x.days) : "") + (x.days && x.trust ? ", " : "") + (x.trust ? "trust " + "−" + x.trust : "") + "." : x.state === "repaired" ? "Repaired before it fired." : ""); });
      if (!back && opt && opt.after) back = opt.after;
      ok = opt ? !!opt.right : d.task === "slide" && sl.indexOf("saving") >= 0 && sl.indexOf("bill") >= 0 && sl.indexOf("net") >= 0;
      if (d.task === "slide") back = sl.indexOf("bill") < 0 ? "Finance found the model bill three weeks later." : sl.indexOf("saving") < 0 ? "The committee never heard what it bought." : sl.indexOf("net") < 0 ? "Someone in the room did the subtraction." : "";
      rows.appendChild(el("tr", { "class": ok ? "ok" : opt || d.task === "slide" ? "off" : "" }, [el("th", { scope: "row", text: "Day " + d.day }),
        el("td", {}, [el("span", { "class": "nd-callhead", text: form.head }),
          el("b", { text: opt ? opt.label : d.task === "slide" ? (sl.length ? "A slide of " + sl.length + " lines" : "The slide") : "" }),
          back ? el("span", { "class": "nd-became", text: back }) : ok ? el("span", { "class": "vh", text: " Done by the method." }) : null])]));
    });
    kids.push(el("div", { "class": "nd-paper" }, [el("h3", { text: "Your thirteen calls" }),
      el("table", { "class": "nd-tb calls" }, [el("thead", {}, [el("tr", {}, [el("th", { scope: "col", text: "Day" }), el("th", { scope: "col", text: "The call, and what it came back as" })])]), rows])]));
    // three questions to take to work
    kids.push(el("div", { "class": "nd-paper" }, [el("h3", { text: "Three questions for Monday" }), el("ol", { "class": "nd-monday" }, data.monday.map(function (q) { return el("li", { text: q }); }))]));
    // the words now earned: folded, so the verdict is not a glossary
    if (state.shelf.length) {
      var ul = el("ul", { "class": "nd-terms" });
      state.shelf.forEach(function (a) { var x = data.artefacts[a]; ul.appendChild(el("li", {}, [el("b", { text: x.term }), el("span", { text: " " + x.plain })])); });
      kids.push(el("details", { "class": "nd-paper nd-shelf" }, [el("summary", {}, [el("span", { text: "What you put on file" }), el("em", { text: state.shelf.length + " of " + Object.keys(data.artefacts).length + " documents, in plain words" })]), ul]));
    } else kids.push(el("p", { "class": "nd-deeper", text: "Nothing was put on file in this run." }));
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
  // after a press, bring its answer on screen; a figure about to play first
  function reveal(focus) {
    var out = panel.querySelector(focus === "ask" ? ".nd-plan" : ".nd-out") || panel.querySelector(".nd-dayhead"), task = panel.querySelector(".nd-task, .nd-gate");
    var fig = panel.querySelector(".nd-sim.nd-go"), low = window.innerHeight - 180, r;
    if (!out) return;
    r = out.getBoundingClientRect();
    if (r.top < BAR || r.top > low || (fig && !inView(fig)) || (task && task.getBoundingClientRect().top > low)) jump(out);
    if (fig && !inView(fig) && task) jump(task);
  }
  function render(focus) {
    var state = run && run.state, kids = null, line = null, more = null, look = null, today = null, f, was;
    if (!left) { left = stage(); root.appendChild(left); root.appendChild(panel); root.appendChild(live); }
    // build everything first: if any of it throws, the page is unchanged
    lineWanted = false;
    if (focus !== "look" || !panel.firstChild) kids = focus === "org" ? orgSetup() : !state ? titleScreen() : state.beat === "end" ? endScreen(state) : playScreen(state);
    if (kids && lineWanted) { line = dayLine(); more = ways(); }
    if (!(state && state.beat === "end") && focus !== "org") look = roomBox(state);
    if (state && state.beat !== "end") today = sim.today(data, state);
    picture(now()); whereabouts(now()); where();   // asked of the rules before anything changes
    was = { cls: root.className, playing: document.documentElement.classList.contains("nd-playing"), kids: kids ? Array.prototype.slice.call(panel.childNodes) : null,
            look: left.querySelector(".nd-look"), line: root.querySelector(".nd-line"), more: root.querySelector(".nd-ways") };
    try {
      root.className = "nd-app " + (!state ? "at-title" : state.beat === "end" ? "at-end" : "at-play") + (focus === "org" ? " at-org" : "");
      document.documentElement.classList.toggle("nd-playing", !!state);
      if (kids) {
        panel.innerHTML = "";
        kids.forEach(function (k) { panel.appendChild(k); });
        if (was.line) was.line.remove();
        if (was.more) was.more.remove();
        if (line) root.insertBefore(line, root.firstChild);       // the line, above the building and the panel
        if (more) root.appendChild(more);                         // and the other ways to play, under both
      }
      // the room cards live under the building
      if (was.look) was.look.remove();
      if (look) left.appendChild(look);
      pill(today);
      draw(); place(); pin();
    } catch (err) {                                  // put back what was there; the guard says so
      root.className = was.cls; document.documentElement.classList.toggle("nd-playing", was.playing);
      if (was.kids) { panel.innerHTML = ""; was.kids.forEach(function (k) { panel.appendChild(k); }); if (line) line.remove(); if (more) more.remove();
        if (was.line) root.insertBefore(was.line, root.firstChild); if (was.more) root.appendChild(was.more); }
      if (look) look.remove();
      if (was.look) left.appendChild(was.look);
      throw err;
    }
    renders++;
    if (focus === "keep") return;                   // the screen as it was, put back after a press that failed
    if (focus === "look") f = left.querySelector(".nd-card") || left.querySelector('.nd-chip[data-room="' + lastRoom + '"]');
    else if (focus === "stay") f = panel.querySelector(".nd-task input");
    else if (focus === "ask") f = panel.querySelector(".nd-evidence");
    else if (focus === "out") f = panel.querySelector(".nd-task h3, .nd-gate h3") || panel.querySelector(".nd-out");
    else f = panel.querySelector("h2");
    if (!f) f = panel.querySelector("h2");
    if (focus === "back") f = root.querySelector(".nd-line .nd-acts button") || panel.querySelector("button");
    // a new day or screen starts at the top, then the focus goes to its heading
    if ((focus === "day" || focus === "back" || focus === "org") && window.scrollY > 0) window.scrollTo({ top: 0, behavior: "instant" });
    if (f && (run || focus === "org" || focus === "back" || focus === "look")) { if (!f.hasAttribute("tabindex") && !/^(BUTTON|INPUT|A)$/.test(f.tagName)) f.setAttribute("tabindex", "-1"); try { f.focus({ preventScroll: focus !== "look" && focus !== "stay" }); } catch (e) { f.focus(); } }
    if (focus === "out" || focus === "ask") reveal(focus);
    settleFigures();
    if (focus === "day" || focus === "back") live.textContent = "";
  }

  mapCv.addEventListener("click", guard(function (e) {     // looking in by pointing at the building
    if (!run || run.state.beat === "end") return;
    var r = mapCv.getBoundingClientRect(), k = MAPW / r.width, id = A.roomAt((e.clientX - r.left) * k - OX, (e.clientY - r.top) * k - OY);
    if (id && id !== "lobby") { looking = looking === id ? null : id; lastRoom = id; render("look"); }
  }));

  // the pitch's facts, once, under the opening lines
  var top = document.querySelector(".nd-top");
  if (top && !top.querySelector(".nd-facts")) top.appendChild(el("p", { "class": "nd-facts", text: data.pitch }));
  // the plain list is for a page without script
  var plain = document.querySelector(".nd-plain"); if (plain) plain.hidden = true;
  root.hidden = false;
  window.addEventListener("hashchange", guard(function () { if (linked()) boot(); }));     // a stop on the line, or any link to a day
  guard(boot)();
  go();
})();
