/* Ninety Days · the page.
   Everything a player reads or presses is real text and real buttons in the page. The two canvases are
   decoration and state: the room where today happens, and the whole building. Nothing here decides
   anything: the rules are in sim.js, and this file only asks them what is legal and shows the answer.

   Nothing moves because it came into view. A figure animates only as the answer to the player's own
   press, and only if it is on screen when they press; otherwise it is shown finished. The one thing
   that loops is the building (monitors, the beacon, the runway lights), and the one pause control
   under it holds that.

   A save is the list of actions taken, kept under one key in localStorage and replayed on load.
   A link such as /simulator/#day-45 opens that day with the earlier days played by the book. */
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
  var asking = false;             // Day 90 in one role: the player has asked to build the slide themselves
  var answering = false;          // the page is being redrawn as the answer to a press: only then may a figure move
  var shown = {};                 // the small simulations that have played in this run: each plays once
  var live = el("p", { "class": "vh", "aria-live": "polite", role: "status" });

  /* ------------------------------------------------------------------ the stage: two canvases */
  var sceneCv = el("canvas", { "class": "nd-scene-cv", "aria-hidden": "true" });
  var mapCv = el("canvas", { "class": "nd-map-cv", "aria-hidden": "true" });
  // The building fills its picture from edge to edge: the sky shows above the roof, not down the sides.
  var MAPW = A.BW, MAPH = A.BH + 16, OX = 0, OY = 4, GROUND = A.BH + 4, clock = 0, raf = 0, last = 0, paused = false, seen = true;
  var enter = 1, shut = 0, flash = 0;      // people walking in, the build floors' shutters, the incident's one hard frame
  window.NDFrames = 0;            // for the acceptance gate: frames drawn by the loop

  function picture(state) {       // what the walls show: the game's state, as the art module reads it
    var i = state ? state.i : 0, st = {};
    st.day = state ? data.days[Math.min(i, data.days.length - 1)].day : 1; st.dayIndex = i;
    // the sky is the phase: dawn, morning, afternoon, golden hour; Day 90 is dusk, or night if the run is late
    st.phases = data.days.map(function (d) { return d.phase; });
    st.sky = ["dawn", "morning", "afternoon", "golden"][st.phases[i]];
    if (state && (state.beat === "end" || i === data.days.length - 1)) st.sky = state.slack < 0 ? "night" : "dusk";
    st.owed = data.days.map(function (d) { return !!state && state.debts.some(function (x) { return x.due === d.id && x.state === "sealed"; }); });
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
  // Size a canvas to the width it has. Where that width holds the picture at a whole number of screen
  // pixels to each art pixel, it gets exactly that, the browser scales it hard, and the frame hugs it:
  // no bars at the sides. Where it does not (a phone), the picture fills the width: it is drawn at the
  // next whole number up and the browser scales it down smoothly, so no art pixel is wider than its
  // neighbour and no letter breaks. Returns what to draw at, and how big one art pixel is on screen.
  function fit(cv, lw, lh, box, max, fill) {
    var s = Math.min(max, box / lw), whole = Math.floor(s + 0.001), k = 1, w;
    if (whole >= 1 && (!fill || s - whole < 0.02)) { w = lw * whole; cv.classList.remove("soft"); }
    else { w = Math.round(lw * s); k = Math.max(2, Math.ceil(s * (window.devicePixelRatio || 1))); cv.classList.add("soft"); }
    if (cv.width !== lw * k) { cv.width = lw * k; cv.height = lh * k; }
    cv.style.width = w + "px"; cv.style.height = Math.round(w * lh / lw) + "px";
    return { k: k, on: w / lw };
  }
  function draw() {
    var state = run && run.state, st = picture(state), day = state && state.beat !== "end" ? sim.today(data, state) : null;
    var rooms = whereabouts(state), speaking = day && day.scene && day.scene[0] ? day.scene[0][0] : null, g, f, box, r;
    if (still || paused) { shut = gateShut(state); enter = 1; flash = 0; }
    // The room where today happens, beside the day strip or above the headline. It does not loop: the
    // people walk in once, as the day opens, and then the picture is still. (At two columns the
    // building beside the panel is the picture of the room, and this one is not shown.)
    if (sceneCv.parentNode && sceneCv.parentNode.clientWidth) {
      f = fit(sceneCv, A.W, A.H, sceneCv.parentNode.clientWidth, 3, true);
      g = sceneCv.getContext("2d"); g.setTransform(f.k, 0, 0, f.k, 0, 0); g.imageSmoothingEnabled = false;
      A.room(g, day ? day.room : "lobby", enter < 1 ? clock : 0, st, true, day ? rooms[day.room] : null, speaking, enter);
      if (flash > 0) { g.fillStyle = "rgba(222,138,138," + (0.5 * flash) + ")"; g.fillRect(0, 0, A.W, A.H); }
    }
    // the whole building, the apron, and the sky above the roof
    if (mapCv.parentNode) {
      box = left ? left.clientWidth : MAPW * 2;
      f = fit(mapCv, MAPW, MAPH, box, 2, box < MAPW * 2);
      g = mapCv.getContext("2d"); g.setTransform(f.k, 0, 0, f.k, 0, 0); g.imageSmoothingEnabled = false;
      A.sky(g, MAPW, MAPH, clock, st.sky);
      A.ground(g, MAPW, MAPH, GROUND, clock, st.sky);
      var mark = {}, i, d;
      if (state) for (i = 0; i < state.debts.length; i++) { d = state.debts[i]; if (d.state === "sealed") mark[data.days[sim.dayIndex(data, d.due)].room] = A.C.rose; }
      // room names are five art pixels tall: under about eight screen pixels they are left off, and the buttons under the picture name the rooms
      A.building(g, OX, OY, clock, st, { active: day ? day.room : null, cast: rooms, speaking: speaking, mark: mark, enter: enter,
        shut: shut > 0 ? { eng: shut, qa: shut } : null, names: f.on >= 1.6 });
      if (flash > 0 && day) { r = A.roomRect(day.room); g.fillStyle = "rgba(222,138,138," + (0.5 * flash) + ")"; g.fillRect(OX + r.x, OY + r.y, r.w, r.h); }
    }
  }
  function loop(now) {
    raf = 0;
    if (still || paused || !seen || document.hidden) return;
    if (now - last > 120) {
      clock += 8; last = now; window.NDFrames++;
      if (enter < 1) enter = Math.min(1, enter + 0.09);
      if (flash > 0) flash = Math.max(0, flash - 0.34);
      var want = gateShut(run && run.state); if (shut > want) shut = Math.max(want, shut - 0.2); else shut = want;
      draw();
    }
    raf = requestAnimationFrame(loop);
  }
  function go() { if (!raf && !still && !paused && seen && !document.hidden) raf = requestAnimationFrame(loop); }
  function arrive() { enter = still ? 1 : 0; }     // a day opens: today's people walk into its room, once
  // The floors where the build happens stay shuttered until the sign-off has been dealt with.
  function gateShut(state) { return !state || state.beat === "end" ? 0 : (state.i < 5 || (state.i === 5 && state.beat !== "done") ? 1 : 0); }
  document.addEventListener("visibilitychange", go);
  window.addEventListener("resize", function () { draw(); });
  // the loop rests while the game is off the screen; nothing starts because it came back
  if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { seen = en[0].isIntersecting; go(); }).observe(root);

  /* ------------------------------------------------------------------ looking in on a room */
  function roomCard(id, state) {
    var lines = [], act = null, i = state.i, b;
    var name = data.rooms[id].replace(/ room$/, "");
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
    run.state = next; if (action.t !== "ask") asking = false;
    if (action.t === "next") { arrive(); looking = null; if (!still && next.events.some(function (e) { return e.kind === "incident"; })) flash = 1; }
    if (still) shut = gateShut(next);
    save(); unlink();
    answering = true;             // what follows is the answer to a press: a figure on screen may play, a pin may fly
    render(action.t === "next" ? "day" : action.t === "ask" ? "ask" : "out");
    flyPins(next.debts.slice(before.debts.length).filter(function (d) { return d.state === "sealed"; }).map(function (d) { return d.due; }));
    answering = false;
    var bits = [];
    if (next.slack !== before.slack) bits.push("Runway " + runwayText(next.slack) + ".");
    if (next.trust !== before.trust) bits.push("Trust " + next.trust + " of " + next.trustMax + ".");
    if (next.tokens !== before.tokens) bits.push(questions(next.tokens) + " left.");
    live.textContent = bits.join(" ");
    go();
  }
  function undoDay() {            // back to the start of today: nothing sealed has been opened, so nothing leaks
    var h = run.state.history.slice();
    while (h.length && h[h.length - 1].t !== "next") h.pop();
    run.state = sim.fold(data, run.opts, h); asking = false; save(); render("day");
  }
  function start(opts) {
    run = { opts: opts, state: sim.init(data, opts) }; looking = null; asking = false; shown = {};
    shut = 1; save(); arrive(); render("day"); go();
  }
  function questions(n) { return n === 1 ? "1 question" : n + " questions"; }
  function runwayText(n) { return n >= 0 ? days(n) + " left" : days(-n) + " late"; }

  /* ------------------------------------------------------------------ a link to a day
     #day-45 opens Day 45 on a fresh whole-team run, with the earlier days played by the book. It never
     replaces a run in progress without being asked: with a save, the title offers both. A hash that
     begins with a slash is an old workbench route, and the page's first script has forwarded it. */
  function linked() {             // the day a link asks for, as an index, or -1
    var m = /^#day-(\d+)$/.exec(location.hash || ""), i;
    for (i = 0; m && i < data.days.length; i++) if (data.days[i].day === +m[1]) return i;
    return -1;
  }
  function unlink() { try { if (/^#day-/.test(location.hash)) history.replaceState(null, "", location.pathname + location.search); } catch (e) { /* the address stays */ } }
  function openAt(i, replace) {
    var opts = { mode: "team", seed: 0, from: i };
    run = { opts: opts, state: sim.fold(data, opts, sim.book(data, opts, i)) }; looking = null; asking = false; shown = {};
    shut = gateShut(run.state); if (replace) { save(); unlink(); }
    arrive(); render("day"); go();
  }
  function resume(saved) { run = { opts: saved.opts, state: sim.fold(data, saved.opts, saved.history) }; shown = {}; unlink(); render("day"); go(); }
  function savedDay(saved) { return data.days[Math.min(data.days.length - 1, saved.history.filter(function (a) { return a.t === "next"; }).length)].day; }
  function boot() {               // on load, and when the address changes under the page
    var i = linked(), saved = load();
    run = null; looking = null; asking = false;
    if (i >= 0 && !(saved && saved.history.length)) openAt(i, false);
    else render("title");
  }

  /* ------------------------------------------------------------------ pieces of the panel */
  // The top of the panel: the room where today happens, the thirteen days, and the meters. The style
  // sheet decides where the room goes: beside the days on a tablet or a laptop, under them on a phone,
  // and nowhere at two columns, where the building beside the panel already shows it.
  function hud(state) {
    var strip = el("ol", { "class": "nd-strip", "aria-label": "The thirteen days" }), i, d, cls, due, meters;
    for (i = 0; i < data.days.length; i++) {
      d = data.days[i]; cls = i < state.i || state.beat === "end" ? "was" : i === state.i ? "now" : "";
      due = state.debts.filter(function (x) { return x.due === d.id && x.state === "sealed"; }).length;
      strip.appendChild(el("li", { "class": cls + (due ? " owed" : ""), "data-day": d.id, "aria-current": cls === "now" ? "step" : null, style: "--c:var(--dg-" + HUE[d.phase] + ")" },
        [el("span", { text: String(d.day) }), due ? el("i", { title: due === 1 ? "Something comes due" : due + " things come due" }, [el("span", { "class": "vh", text: " (something comes due)" })]) : null]));
    }
    var pips = el("span", { "class": "nd-pips", "aria-hidden": "true" });
    for (i = 0; i < state.trustMax; i++) pips.appendChild(el("i", { "class": i < state.trust ? "on" : "" }));
    meters = el("dl", { "class": "nd-meters" }, [
      el("div", { "class": state.slack < 0 ? "bad" : "" }, [el("dt", { text: "Runway" }), el("dd", { text: runwayText(state.slack) })]),
      el("div", {}, [el("dt", { text: "Sponsor's trust" }), el("dd", {}, [pips, el("span", { "class": "vh", text: state.trust + " of " + state.trustMax })])]),
      el("div", {}, [el("dt", { text: "On file" }), el("dd", { text: state.shelf.length + " of " + Object.keys(data.artefacts).length })]),
      state.mode !== "team" ? el("div", {}, [el("dt", { text: "Questions" }), el("dd", { text: state.tokens + " left" })]) : null]);
    return el("div", { "class": "nd-hud" }, [el("div", { "class": "nd-scene" }, [sceneCv]), strip, meters]);
  }
  // In one role, and as the sponsor: who the player is, said before anything else on the day.
  function whoLine(state) {
    if (state.mode === "role") return el("p", { "class": "nd-you-are" }, [el("b", { text: "You are " + who(data.roles[state.role].who).name + ", the " + lower(data.roles[state.role].name) + ". " }), data.roles[state.role].line]);
    if (state.mode === "org") return el("p", { "class": "nd-you-are" }, [el("b", { text: "You are Ines, the sponsor. " }), "The team makes each call. You may ask to see the evidence behind " + ["none", "one", "two", "three"][data.rules.questions.org] + " of them."]);
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
  function optionButtons(state, day, handler, skip, legend) {
    var set = el("fieldset", { "class": "nd-opts" + (legend ? " alt" : "") }, [el("legend", { text: legend || day.ask })]);
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
    var box = el("div", { "class": "nd-out", tabindex: "-1" }), sealed;
    state.events.forEach(function (e) {
      if (e.kind === "choice") box.appendChild(el("p", { "class": "nd-you" }, [el("b", { text: e.label }), el("em", { text: e.days ? days(e.days) : "no days" })]));
      if (e.kind === "choice" || e.kind === "task" || e.kind === "gate" || e.kind === "fix" || e.kind === "repair" || e.kind === "move")
        box.appendChild(el("p", { "class": "ev-" + e.kind }, [e.text, e.kind !== "choice" && e.days ? el("em", { text: " " + days(e.days) + "." }) : null,
          e.trust > 0 ? el("em", { text: " Trust falls by " + e.trust + "." }) : e.trust < 0 ? el("em", { text: " Trust rises." }) : null]));
    });
    // what today left sealed, by the day it comes due: a task can pin more than one thing
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
     Each shows one idea the words alone carry badly, plays once in true steps (no number counts up),
     and ends on the whole picture. With reduced motion the whole picture is simply there. They move
     only transform, opacity and clip-path; the timings are in game.css. */
  function once(name) {           // true the first time this figure is shown on this day, and only as the answer to a press
    var k = run.state.i + ":" + name, first = !shown[k];
    shown[k] = 1;
    return first && answering && !still;
  }
  var BAR = 60, TOP = 84;         // the foot of the site's bar, and where the top of an answer is put under it
  function inView(n) { var r = n.getBoundingClientRect(); return r.top >= BAR && r.bottom <= window.innerHeight && r.height > 0; }
  // Put the top of something just under the bar, at once: a figure about to play needs to be where it will be.
  function jump(n) { window.scrollTo({ top: Math.max(0, window.scrollY + n.getBoundingClientRect().top - TOP), behavior: "instant" }); }
  // A figure that is not whole on the screen when it would start does not start: it is shown finished.
  function settleFigures() {
    panel.querySelectorAll(".nd-sim.nd-go").forEach(function (f) { if (!inView(f)) f.classList.remove("nd-go"); });
  }
  // Day 45. One score becomes three: a column per kind of case, as wide as its share of the cases, each
  // with its own bar and the margin under its score. The smallest sample has the longest whisker.
  function splitFigure(state, t, bars) {
    var n = 0, right = 0, plot = el("div", { "class": "nd-split-plot" }), names = el("div", { "class": "nd-split-names" });
    t.slices.forEach(function (s) { n += s.n; right += s.right; });
    t.slices.forEach(function (s, k) {
      var st = sim.sliceStats(s);
      plot.appendChild(el("div", { "class": "nd-split-col", style: "flex:" + s.n + " 0 0;--s:" + st.score + ";--l:" + st.lower + ";--b:" + bars[s.id] + ";--a:" + (100 * right / n) }, [
        el("i", { "class": "nd-split-fill" }), el("i", { "class": "nd-split-whisk" }), el("i", { "class": "nd-split-bar" }), el("b", { text: String(st.score) })]));
      // the name sits under its column; where a column is narrower than its name, the names keep their order and close up
      names.appendChild(el("span", { style: "flex:" + s.n + " 1 0" }, [el("b", { text: s.short }), el("i", { text: s.n + " cases" })]));
    });
    plot.appendChild(el("span", { "class": "nd-split-one", style: "--a:" + (100 * right / n), text: (Math.round(1000 * right / n) / 10) + " on all " + n }));
    return el("div", { "class": "nd-sim nd-split" + (once("split") ? " nd-go" : "") }, [
      el("div", { "aria-hidden": "true" }, [plot, names]),
      el("p", { "class": "nd-cap" }, ["One score is three scores. Each column is as wide as its share of the " + n + " cases. ",
        el("i", { "class": "nd-key bar", "aria-hidden": "true" }), "the bar ", el("i", { "class": "nd-key whisk", "aria-hidden": "true" }), "the least the score could be"])]);
  }
  // Day 75. The bill is the estimate stretched four times over: the habits multiply. Ticking a fix
  // takes its factor out, and everything after it shrinks.
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
        // a label takes its segment's share of the row and never less than its own width, so two labels cannot print on each other
        x.lab.style.flex = gone ? "0 0 0" : (to - from) + " 1 0";
        at = to;
      });
      rest.style.flex = Math.max(0, whole - at) + " 1 0";
      total.textContent = (Math.round(at * 100) / 100) + " times";
    };
    fig.paint([]);
    return fig;
  }
  // Day 82. The same $2,000 refund meets the $400 limit in one of two places: a sentence in the prompt,
  // which is paper, or the refund tool itself, which is a wall.
  function refundStrip(form) {
    var paid = form === "paid";
    return el("div", { "class": "nd-sim nd-pw " + (paid ? "nd-pw-paid" : "nd-pw-held") + (once("refund") ? " nd-go" : "") }, [
      el("div", { "class": "nd-pw-row", "aria-hidden": "true" }, [
        el("span", { "class": "nd-pw-end from", text: "The assistant" }),
        el("span", { "class": "nd-pw-track" }, [el("i", { "class": "nd-pw-run" }, [el("b", { text: "$2,000" })]), el("i", { "class": "nd-pw-stop" }),
          el("em", { text: paid ? "the prompt" : "the tool" })]),
        el("span", { "class": "nd-pw-end to", text: "The passenger" })]),
      el("p", { "class": "nd-cap", text: paid ? "The $400 limit was a sentence in the prompt. That is paper, and the refund went through it."
        : "The $400 limit is in the refund tool itself. That is a wall, and the refund stopped at it." })]);
  }
  // A debt is pinned: a rose pin leaves the outcome line and lands on the day it comes due, one day
  // after another. The strip keeps the pin; this only shows where it came from.
  function flyPins(due) {
    var from = panel.querySelector(".nd-sealed i"), seen = {}, n = 0, spring;
    if (still || !from || !from.animate || !due.length || !inView(from)) return;
    try { spring = getComputedStyle(root).getPropertyValue("--spring").trim() || "ease-out"; } catch (e) { spring = "ease-out"; }
    due.forEach(function (id) {
      var to = panel.querySelector('.nd-strip li[data-day="' + id + '"] i'), a, b, pin, fly;
      // only to a day the player can see: a pin that flies off the screen is movement leaving the page
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
      box.addEventListener("submit", function () { var v = get(); if (v == null) return; act(state.beat === "choose" && state.pending ? { t: "challenge", input: v } : { t: "task", id: id, input: v }); });
    }
    if (id === "limits") {
      // six lines, six checkboxes: as a real limit is ticked, the target it bends is shown rewritten
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
      hold.addEventListener("change", paint); paint();
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

  function slideLines(state) {     // the six lines that could go on the Day 90 slide, from the run's own numbers
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
    box.appendChild(el("p", { "class": "nd-intro", text: "This is the one hand-off that stops the work. Nothing is built until three documents are signed. After today, changing your mind costs a rewrite." }));
    box.appendChild(lamps);
    if (!miss.length) box.appendChild(el("div", { "class": "nd-acts" }, [el("button", { type: "button", "class": "btn pri", text: "Sign and start the build", onclick: function () { act({ t: "gate", how: "pass" }); } })]));
    else box.appendChild(el("div", { "class": "nd-acts" }, [
      el("button", { type: "button", "class": "nd-opt", onclick: function () { act({ t: "gate", how: "hold" }); } }, [el("span", { "class": "nd-opt-l", text: "Hold the build and write what is missing" }), el("span", { "class": "nd-opt-p", text: days(2 * miss.length) })]),
      el("button", { type: "button", "class": "nd-opt", onclick: function () { act({ t: "gate", how: "open" }); } }, [el("span", { "class": "nd-opt-l", text: "Start the build with what is on file" }), el("span", { "class": "nd-opt-p", text: "no days" })])]));
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
    var chips = el("div", { "class": "nd-rooms", role: "group", "aria-label": "Look in on a room" });
    ["board", "product", "arch", "eng", "qa", "platform", "centre"].forEach(function (id) {
      var c = roomCard(id, state);
      chips.appendChild(el("button", { type: "button", "class": "nd-chip" + (looking === id ? " on" : ""), "aria-pressed": looking === id ? "true" : "false", "data-room": id,
        onclick: function () { looking = looking === id ? null : id; lastRoom = id; render("look"); } }, [el("i", { "aria-hidden": "true", style: "background:" + A.paint(id).hue }), c.name]));
    });
    var out = [chips];
    if (looking) {
      var c = roomCard(looking, state), card = el("div", { "class": "nd-card", tabindex: "-1", style: "--rc:" + A.paint(looking).hue }, [el("b", { text: c.name })]);
      c.lines.forEach(function (l) { card.appendChild(el("p", { text: l })); });
      if (c.act) card.appendChild(el("button", { type: "button", "class": "nd-opt", onclick: function () { act({ t: c.act.t }); } }, [el("span", { "class": "nd-opt-l", text: c.act.label }), el("span", { "class": "nd-opt-p", text: days(c.act.days) })]));
      out.push(card);
    }
    return el("div", { "class": "nd-look" }, out);
  }

  /* ------------------------------------------------------------------ screens */
  // The head of a day, for a reader who has seen no other day: where and when, the headline, one fixed
  // sentence on where the project is, and the earlier call that today leans on.
  var HUE = ["slate", "indigo", "teal", "amber"];
  function dayHead(state, day) {
    var so = sim.soFar(data, state), from = run.opts.from || 0;
    return el("div", { "class": "nd-dayhead", style: "--c:var(--dg-" + HUE[day.phase] + ")" }, [
      el("p", { "class": "nd-kick" }, [el("i", { "aria-hidden": "true" }), "Day " + day.day + " of 90 · " + data.phases[day.phase].name + " · " + data.rooms[day.room]]),
      el("h2", { tabindex: "-1", text: "Day " + day.day + ". " + day.head }),
      el("p", { "class": "nd-ctx" }, [el("span", { text: data.short + " " }), day.context]),
      so.text ? el("p", { "class": "nd-sofar" }, [el("b", { text: so.label + " " }), so.text]) : null,
      from > 0 && state.i === from ? el("p", { "class": "nd-book", text: (from === 1 ? "Day 1 was" : "Days 1 to " + data.days[from - 1].day + " were") + " played by the book so you can start here." }) : null]);
  }
  // The site's header carries one pill for this page, beside "The manual". While a day with a lesson
  // behind it is on screen the pill reads "Read the lesson" and goes there; on the title, the ending
  // and a day with no lesson it reads "The tutorial" and goes to the tutorial. Both labels sit in the
  // pill at once, one on the other with only one showing, so the pill is as wide as the wider of the
  // two on every screen and the bar never moves.
  function twoLabels(span, labels, on, icon) {
    if (!span) return;
    if (!span.querySelector(".nd-two")) {
      // each label carries its own copy of the icon, so icon and words stay together in the middle of the pill
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
  // One pause control for the game, under the building and clear of the picture. The building is the
  // only thing that loops, so this holds everything that does.
  function pauseControl() {
    var box = el("input", { type: "checkbox", autocomplete: "off", "data-motion-toggle": true, onchange: function (e) { paused = e.target.checked; draw(); go(); } });
    box.checked = paused;
    return el("label", { "class": "mpause nd-pause" }, [box, el("span", { "class": "vh", text: "Pause the animation" }), el("i", { "aria-hidden": "true" })]);
  }
  function stage() {
    return el("div", { "class": "nd-stage" }, [el("div", { "class": "nd-map" }, [mapCv]),
      el("div", { "class": "nd-stagebar" }, [el("p", { "class": "nd-k", text: "Look in on a room" }), still ? null : pauseControl()])]);
  }

  function titleScreen() {
    var saved = load(), b = best(), kids = [], want = linked();
    if (want >= 0 && saved && saved.history.length) {        // a link to a day, and a run in progress: the player says which
      return [el("div", { "class": "nd-title" }, [
        el("p", { "class": "nd-pitch", text: "This link opens Day " + data.days[want].day + ". You also have a run in progress, on Day " + savedDay(saved) + "." }),
        el("div", { "class": "nd-acts" }, [
          el("button", { type: "button", "class": "btn pri", text: "Carry on from Day " + savedDay(saved), onclick: function () { resume(saved); } }),
          el("button", { type: "button", "class": "btn ghost", text: "Open Day " + data.days[want].day + " on a fresh run", onclick: function () { openAt(want, true); } })]),
        el("p", { "class": "nd-best", text: "A fresh run replaces the one you have saved." })])];
    }
    kids.push(el("div", { "class": "nd-title" }, [
      el("p", { "class": "nd-pitch", text: data.pitch }),
      el("div", { "class": "nd-acts" }, [
        saved && saved.history.length ? el("button", { type: "button", "class": "btn pri", text: "Carry on from Day " + savedDay(saved), onclick: function () { resume(saved); } }) : null,
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

  // A colleague's call, or the team's under the sponsor: what they plan, and what the player may do
  // about it. The question is offered whether the plan is sound or not, so being offered tells nothing.
  // Asking costs one question and shows the evidence: what the plan is working from, and what it would
  // put on file. Then the player lets the plan stand or asks for something else, at no further cost.
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

  function playScreen(state) {
    var day = sim.today(data, state), kids = [], own = who(day.owner), o, w = whoLine(state);
    if (w) kids.push(w);
    kids.push(hud(state));
    kids.push(dayHead(state, day));
    var ev = eventList(state); if (ev) kids.push(ev);
    // Day 82's figure draws what arrived, which the line above has already said. It comes after the call,
    // so that the question and its first option are on the first screen, and it stays on the day once the
    // call is made. It plays, as every figure does, only if it is whole on the screen when the day opens.
    var fig = day.form ? refundStrip(day.form) : null;
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
    kids.push(el("div", { "class": "nd-verdict v-" + v.key }, [el("p", { "class": "nd-k", text: "Day 90 of 90 · The committee decides" }), el("h2", { tabindex: "-1", text: V.name }), el("p", { text: V.line })]));
    // The saving is the run's own: how long the assistant was live, and what was live. The line under it says why.
    var why = [L.liveDays ? "live for " + L.liveDays + " of " + L.of + " days" : "never live inside the ninety days"];
    if (L.off) why.push("off for a week"); if (L.held) why.push("held back for one bar");
    if (L.unshipped) why.push("same-day cases kept with people"); if (L.redone) why.push("some cases done again by people");
    kids.push(el("dl", { "class": "nd-meters end" }, [
      el("div", { "class": v.late ? "bad" : "" }, [el("dt", { text: "The date" }), el("dd", { text: v.late ? days(v.late) + " late" : "met, " + days(state.slack) + " to spare" })]),
      el("div", {}, [el("dt", { text: "Sponsor's trust" }), el("dd", { text: state.trust + " of " + state.trustMax })]),
      el("div", {}, [el("dt", { text: v.key === "stopped" ? "Saved, before it was stopped" : "Saved" }), el("dd", { text: L.days + " person-days, " + money(L.value) }), el("dd", { "class": "nd-sub", text: why.join(", ") })]),
      el("div", {}, [el("dt", { text: "Spent" }), el("dd", { text: money(L.cost) }), el("dd", { "class": "nd-sub", text: "model " + money(L.bill) + ", review " + money(L.review) + (L.mishaps ? ", refunds " + money(L.mishaps) : "") })]),
      el("div", { "class": L.net < 0 ? "bad" : "" }, [el("dt", { text: "Net, first cycle" }), el("dd", { text: money(L.net) })])]));
    // the thirteen calls, each with what it came back as, under it and only where there is something to say
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
    kids.push(el("div", { "class": "nd-paper" }, [el("h3", { text: "Three questions for Monday" }), el("ol", { "class": "nd-monday" }, [
      el("li", { text: "Is the limit in the tool, or only in the prompt?" }),
      el("li", { text: "What is the least that score could be, and on how many cases?" }),
      el("li", { text: "Which of our open decisions really stops the work?" })])]));
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
  // After a press, bring its answer onto the screen if it is not there: the outcome line and the task
  // it opened, or the evidence. A figure that is about to play gets the screen first.
  function reveal(focus) {
    var out = panel.querySelector(focus === "ask" ? ".nd-plan" : ".nd-out") || panel.querySelector(".nd-dayhead"), task = panel.querySelector(".nd-task, .nd-gate");
    var fig = panel.querySelector(".nd-sim.nd-go"), low = window.innerHeight - 180, r;
    if (!out) return;
    r = out.getBoundingClientRect();
    if (r.top < BAR || r.top > low || (fig && !inView(fig)) || (task && task.getBoundingClientRect().top > low)) jump(out);
    if (fig && !inView(fig) && task) jump(task);
  }
  function render(focus) {
    var state = run && run.state, kids, f;
    if (!left) { left = stage(); root.appendChild(left); root.appendChild(panel); root.appendChild(live); }
    root.className = "nd-app " + (!state ? "at-title" : state.beat === "end" ? "at-end" : "at-play") + (focus === "org" ? " at-org" : "");
    document.documentElement.classList.toggle("nd-playing", !!state);
    if (focus !== "look" || !panel.firstChild) {      // looking in on a room leaves the panel alone, and a half-filled task with it
      kids = focus === "org" ? orgSetup() : !state ? titleScreen() : state.beat === "end" ? endScreen(state) : playScreen(state);
      panel.innerHTML = "";
      kids.forEach(function (k) { panel.appendChild(k); });
    }
    // the room cards live under the building
    var old = left.querySelector(".nd-look"); if (old) old.remove();
    if (state && state.beat !== "end" && focus !== "org") left.appendChild(roomBox(state));
    pill(state && state.beat !== "end" && focus !== "org" ? sim.today(data, state) : null);
    draw();
    if (focus === "look") f = left.querySelector(".nd-card") || left.querySelector('.nd-chip[data-room="' + lastRoom + '"]');
    else if (focus === "stay") f = panel.querySelector(".nd-task input");
    else if (focus === "ask") f = panel.querySelector(".nd-evidence");
    else if (focus === "out") f = panel.querySelector(".nd-task h3, .nd-gate h3") || panel.querySelector(".nd-out");
    else f = panel.querySelector("h2");
    if (!f) f = panel.querySelector("h2");
    if (focus === "back") f = panel.querySelector("button");
    // a new day, or a new screen, starts at the top of the page, at once: then the focus goes to its heading
    if ((focus === "day" || focus === "back" || focus === "org") && window.scrollY > 0) window.scrollTo({ top: 0, behavior: "instant" });
    if (f && (run || focus === "org" || focus === "back")) { if (!f.hasAttribute("tabindex") && !/^(BUTTON|INPUT|A)$/.test(f.tagName)) f.setAttribute("tabindex", "-1"); try { f.focus({ preventScroll: focus !== "look" && focus !== "stay" }); } catch (e) { f.focus(); } }
    if (focus === "out" || focus === "ask") reveal(focus);
    settleFigures();
    if (focus === "day" || focus === "back") live.textContent = "";
  }

  mapCv.addEventListener("click", function (e) {           // looking in by pointing at the building
    if (!run || run.state.beat === "end") return;
    var r = mapCv.getBoundingClientRect(), k = MAPW / r.width, id = A.roomAt((e.clientX - r.left) * k - OX, (e.clientY - r.top) * k - OY);
    if (id && id !== "lobby") { looking = looking === id ? null : id; lastRoom = id; render("look"); }
  });

  // the plain list was for a page without script: this script is here, so the game takes over
  var plain = document.querySelector(".nd-plain"); if (plain) plain.hidden = true;
  root.hidden = false;
  window.addEventListener("hashchange", function () { if (linked() >= 0) boot(); });
  boot();
  go();
})();
