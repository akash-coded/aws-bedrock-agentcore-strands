/* Ninety Days · the rules.
   No DOM, no clock, no randomness: a state, an action, the next state. The page draws what this
   returns, the tests in site/tools/sim.test.mjs walk every path through it, and a save is nothing but
   the list of actions, replayed.

   The economy in one paragraph. Runway is days of slack before Day 90. Doing a day properly costs
   days now and files a document. A shortcut costs less now and leaves a sealed debt on a later day,
   which fires at about three times the price, with the player's own choice quoted back. A debt can be
   repaired before it fires, at twice the price: that is the way back. Doing everything properly does
   not fit the runway, so the date has to move once, and moving it with documents on file costs no
   trust. Trust moves only on surprise. */
(function (root) {
  "use strict";

  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function dayIndex(data, id) { for (var i = 0; i < data.days.length; i++) if (data.days[i].id === id) return i; return -1; }
  function has(state, art) { return state.shelf.indexOf(art) >= 0; }
  function arts(opt) { return !opt.art ? [] : (typeof opt.art === "string" ? [opt.art] : opt.art); }
  function round(n, p) { var k = Math.pow(10, p || 0); return Math.round(n * k) / k; }

  /* ------------------------------------------------------------------ what today looks like */
  // Day 82 has two forms: the tool refused the refund, or it paid it.
  function variant(data, state, day) {
    if (!day.variants) return day;
    var v = day.variants[state.capInTool ? "blocked" : "paid"], out = {}, k;
    for (k in day) out[k] = day[k];
    out.scene = v.scene; out.ask = v.ask; out.options = v.options; out.form = state.capInTool ? "blocked" : "paid";
    return out;
  }
  function today(data, state) { return variant(data, state, data.days[state.i]); }
  function rightOption(day) {
    var o = day.options || [], i;
    for (i = 0; i < o.length; i++) if (o[i].right) return o[i];
    return null;
  }
  // what an option costs today: more if the document it leans on was never filed
  function price(data, state, day, opt) {
    var d = opt.days;
    if (opt.extraIfMissing && day.needs && !has(state, day.needs)) d += opt.extraIfMissing;
    return d;
  }
  function owner(data, day) { return data.cast[day.owner]; }
  // who makes today's call: the player, or a colleague
  function mine(data, state, day) {
    if (state.mode === "team") return true;
    if (state.mode === "org") return false;
    return data.cast[day.owner].role === state.role;
  }

  /* ------------------------------------------------------------------ colleagues
     A colleague does the day properly when the document they lean on is on file and it is not one of
     their habits. Nothing here is random: the same run always plays the same way. */
  // A habit is a day a colleague gets wrong unless someone asks. Under a sponsor's rules the team is the
  // same people, but the two craft habits (too many records, the model call first) are left to the leads.
  var HABIT = { d2: "a", d5: "a", d6: "a", d8: "a", d9: "a", d10: "a", d11: "a", d13: "x" };
  var CRAFT = { d5: 1, d8: 1 };
  function habit(state, id) { return !!HABIT[id] && !(state.mode === "org" && CRAFT[id]); }
  function forced(data, state, what) {            // the organisation lens: a rule the sponsor enforces
    var i, p;
    for (i = 0; i < data.policies.length; i++) {
      p = data.policies[i];
      if (state.policies.indexOf(p.id) >= 0 && p.forces.indexOf(what) >= 0) return true;
    }
    return false;
  }
  function botPick(data, state, day) {
    var right = rightOption(day), o = day.options, i;
    if (!right) return null;
    // a sponsor's rule settles it; otherwise habit, and whether the document they lean on exists
    if (state.mode === "org" && forced(data, state, day.id)) return right.id;
    if (!habit(state, day.id) && (!day.needs || has(state, day.needs))) return right.id;
    for (i = 0; i < o.length; i++) if (!o[i].right) return o[i].id;      // the first shortcut
    return right.id;
  }
  // how a colleague fills in a task: well if they chose well
  function botTask(data, state, id, well) {
    var t = data.tasks[id], out, i;
    if (id === "bar") return { hold: !!well };
    if (id === "score") return well ? { same: "ship", code: "hold", refund: "shadow" } : { same: "ship", code: "ship", refund: "ship" };
    if (id === "route") { out = {}; for (i = 0; i < t.items.length; i++) out[t.items[i].id] = well ? t.items[i].lane : 1; return out; }
    if (id === "leak") return well ? ["context", "tier"] : ["cache"];
    if (id === "slide") return well ? ["saving", "bill", "net"] : ["saving", "score", "shelf"];
    return null;
  }

  /* ------------------------------------------------------------------ the tasks */
  function barOf(slice, held) {
    var dmg = held && slice.damageHeld != null ? slice.damageHeld : slice.damage, n = dmg / slice.saving;
    return round(100 * n / (n + 1));
  }
  function bars(data, state) {
    var out = {}, s = data.tasks.bar.slices, i;
    for (i = 0; i < s.length; i++) out[s[i].id] = barOf(s[i], !!state.flags.hold);
    return out;
  }
  function sliceStats(slice) {
    var p = slice.right / slice.n, n = slice.n, z = 1.96, lo = p - z * Math.sqrt(p * (1 - p) / n);
    // under a hundred cases the normal bound is too kind, so the small slices take Wilson's
    if (n < 100) lo = (p + z * z / (2 * n) - z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n);
    return { score: round(100 * p, 1), lower: round(100 * lo, 1), share: slice.n };
  }
  function note(state, kind, text, days, trust) {
    state.events.push({ kind: kind, text: text, days: days || 0, trust: trust || 0 });
    if (days) state.slack -= days;
    if (trust) state.trust = Math.max(0, Math.min(state.trustMax, state.trust - trust));
  }
  function file(state, art) { if (art && state.shelf.indexOf(art) < 0) { state.shelf.push(art); state.filed.push(art); } }
  function seal(data, state, day, debt) {
    state.debts.push({ id: day.id, from: day.day, due: debt.due, dueDay: data.days[dayIndex(data, debt.due)].day,
                       days: debt.days, trust: debt.trust || 0, tag: debt.tag, text: debt.text, state: "sealed" });
  }

  function doTask(data, state, id, input) {
    var t = data.tasks[id], b, i, s, st, pick, slots, wrongMoney, over, mult, spent, has3;
    state.tasks[id] = input;
    if (id === "bar") {
      state.flags.hold = !!input.hold;
      file(state, "bar");
      note(state, "task", input.hold ? t.after.held : t.after.unheld);
    } else if (id === "score") {
      b = bars(data, state); state.live = {};
      for (i = 0; i < t.slices.length; i++) {
        s = t.slices[i]; st = sliceStats(s); pick = input[s.id] || "hold";
        state.live[s.id] = pick;
        if (pick === "ship" && st.score < b[s.id]) {
          seal(data, state, data.days[state.i], { due: "d10", days: 2, trust: 2, tag: s.name.toLowerCase() + ", shipped below its bar",
            text: s.name + " went live at " + st.score + " against a bar of " + b[s.id] + ". The complaints arrived inside a week." });
        } else if (pick === "ship" && st.lower < b[s.id]) {       // above the bar, and not yet proven
          seal(data, state, data.days[state.i], { due: "d10", days: 1, trust: 1, tag: s.name.toLowerCase() + ", shipped before it was proven",
            text: s.name + " went live on " + st.score + ", with a lower bound of " + st.lower + " against a bar of " + b[s.id] + ". The live rate fell inside the margin, and the sponsor had been told it passed." });
        }
      }
    } else if (id === "route") {
      slots = 0; wrongMoney = 0; over = 0; var under = 0;
      for (i = 0; i < t.items.length; i++) {
        pick = +input[t.items[i].id] || 0; slots += pick;
        if (t.items[i].lane === 2 && pick < 2) wrongMoney++;
        if (t.items[i].lane === 1 && pick < 1) under++;
        if (pick > t.items[i].lane) over += pick - t.items[i].lane;
      }
      state.review = { slots: slots, queue: round(4 * slots / 18, 1) };
      note(state, "task", "18 review slots become " + slots + ". The queue goes from 4 days to " + state.review.queue + ".");
      if (wrongMoney) {
        state.flags.rushed = true;
        seal(data, state, data.days[state.i], { due: "d12", days: 2, trust: 1, tag: "a money change with too few readers",
          text: "A change that touched the refund limit went out with " + (wrongMoney === 1 ? "one of the two money changes" : "both money changes") + " read by fewer than two people. It has to be pulled back and read again." });
      }
      if (under >= 2) note(state, "task", "Changes to what the assistant does went out on the automatic checks alone. One had to be pulled back.", 1);
      if (over >= 3) note(state, "task", "More readers than the risk asked for. The people who read the money changes are still tired.", 1);
    } else if (id === "leak") {
      mult = 4.4; spent = 0;
      for (i = 0; i < t.rows.length; i++) if (input.indexOf(t.rows[i].id) >= 0) { mult /= t.rows[i].factor; spent += t.rows[i].days; }
      state.bill = round(mult, 2);
      if (state.bill > 2) note(state, "task", "After a day the bill is still " + state.bill + " times the estimate. The rest takes another day to find.", 1);
      else note(state, "task", "One day of work takes the bill from 4.4 to " + state.bill + " times the estimate. The other fixes follow in order, and an alert is set at 3 times.");
    } else if (id === "slide") {
      has3 = function (k) { return input.indexOf(k) >= 0; };
      state.slide = input.slice(0, 3);
      if (!has3("bill")) note(state, "task", "Finance found the model bill three weeks later, and asked what else was left out.", 0, 3);
      else if (!has3("saving")) note(state, "task", "The committee saw what it cost and never heard what it bought.", 0, 1);
      else if (!has3("net")) note(state, "task", "Both numbers were on the slide. Someone in the room did the subtraction for you.", 0, 1);
      else { note(state, "task", "Both numbers on one line, and the loss stated. The question in the room changed from whether this is real to what you need next.", 0, -1); file(state, "report"); }
    }
  }

  /* ------------------------------------------------------------------ a day opens */
  function openDay(data, state) {
    var day = data.days[state.i], r = data.rules, i, d;
    state.events = []; state.filed = []; state.beat = "choose"; state.pending = null;
    if (r.pressure.onDay[state.seed % r.pressure.onDay.length] === day.id) note(state, "pressure", r.pressure.text, r.pressure.days);
    for (i = 0; i < state.debts.length; i++) {
      d = state.debts[i];
      if (d.state === "sealed" && d.due === day.id) { d.state = "fired"; note(state, "debt", d.text, d.days, d.trust); state.events[state.events.length - 1].from = d.from; state.events[state.events.length - 1].tag = d.tag; }
    }
    if (day.id === "d12") {
      if (state.capInTool) note(state, "good", "The refund tool refused the payment at its limit.", 0, -1);
      else note(state, "incident", state.flags.noBudget ? "Nobody ever decided what the assistant may pay out alone. The code decided by default."
        : (state.flags.rushed ? "The change that touched the refund limit got a ninety-second reading on a Friday." : "The limit was written down. It was never typed into the tool."),
        0, state.flags.noBudget ? 3 : 2);
      state.incidents = state.capInTool ? 0 : 1;
    }
    // the sponsor's lens and a colleague's day: the call is already made, and waits to be accepted
    if (!mine(data, state, day)) state.pending = day.task && !day.options ? "task" : botPick(data, state, today(data, state));
    if (state.mode === "org" && !state.capInTool && day.id === data.rules.capFix.from && forced(data, state, "cap")) applyFix(data, state);
    if (state.mode === "org" && state.slack < 0 && !state.moved && state.shelf.length >= data.rules.moveDate.evidence) applyMove(data, state);
  }

  function applyMove(data, state) {
    var m = data.rules.moveDate, ok = state.shelf.length >= m.evidence;
    state.moved = true; state.slack += m.days;
    note(state, "move", ok ? "Ines moves the date by " + m.days + " days. She has seen what is on file."
      : "Ines moves the date by " + m.days + " days, and asks what she is waiting for. There is little on file to show her.", 0, ok ? m.trustWith : m.trustWithout);
  }
  function applyFix(data, state) {
    var c = data.rules.capFix, nb = !!state.flags.noBudget;
    state.capInTool = true;
    if (nb) { delete state.flags.noBudget; file(state, "budget"); }
    note(state, "fix", nb ? "What the assistant may pay out alone is decided now, late, and typed into the refund tool: $400, with a named approver above it."
      : "The $400 limit moves out of the prompt and into the refund tool itself.", nb ? c.daysNoBudget : c.days);
  }
  function canFix(data, state) {
    var c = data.rules.capFix;
    return !state.capInTool && state.beat !== "end" && state.i >= dayIndex(data, c.from) && state.i <= dayIndex(data, c.until);
  }
  function repairCost(data, debt) {
    var day = data.days[dayIndex(data, debt.id)], r = rightOption(variant(data, { capInTool: false }, day));
    return Math.max(2, data.rules.repairFactor * (r ? r.days : 1));
  }

  function choose(data, state, optId) {
    var day = today(data, state), opt = null, i, a;
    if (!day.options) return false;
    for (i = 0; i < day.options.length; i++) if (day.options[i].id === optId) opt = day.options[i];
    if (!opt) return false;
    state.picks[day.id] = optId;
    note(state, "choice", opt.now, price(data, state, day, opt));
    state.events[state.events.length - 1].label = opt.label;
    a = arts(opt); for (i = 0; i < a.length; i++) file(state, a[i]);
    if (opt.flags) for (i = 0; i < opt.flags.length; i++) state.flags[opt.flags[i]] = true;
    if (opt.flags && opt.flags.indexOf("capInTool") >= 0) state.capInTool = true;
    if (opt.debt) seal(data, state, day, opt.debt);
    state.beat = opt.task ? "task" : (day.gate ? "gate" : "done");
    state.task = opt.task || null;
    return true;
  }

  function gateMissing(state) {
    var need = ["spec", "bar", "budget"], out = [], i;
    for (i = 0; i < need.length; i++) if (!has(state, need[i])) out.push(need[i]);
    return out;
  }

  /* ------------------------------------------------------------------ init, reduce, fold */
  function init(data, opts) {
    opts = opts || {};
    var state = { v: data.v, mode: opts.mode || "team", role: opts.role || null, policies: (opts.policies || []).slice(0, 3), seed: opts.seed || 0,
                  i: 0, beat: "choose", task: null, pending: null, slack: opts.mode === "role" ? data.rules.slackRole : data.rules.slack,
                  trust: data.rules.trust, trustMax: data.rules.trustMax,
                  moved: false, shelf: [], filed: [], debts: [], picks: {}, tasks: {}, flags: {}, events: [],
                  tokens: opts.mode === "org" ? data.rules.questions.org : (opts.mode === "role" ? data.rules.questions.role : 0),
                  capInTool: false, incidents: 0, live: null, review: null, bill: null, slide: null, history: [] };
    openDay(data, state);
    return state;
  }

  function legal(data, state) {
    var out = [], day, i, d, miss;
    if (state.beat === "end") return out;
    day = today(data, state);
    if (state.beat === "choose") {
      if (state.pending) {
        out.push({ t: "accept" });
        if (state.tokens > 0 && day.options) for (i = 0; i < day.options.length; i++) if (day.options[i].id !== state.pending) out.push({ t: "challenge", opt: day.options[i].id });
        if (state.tokens > 0 && !day.options) out.push({ t: "challenge" });
      } else if (day.options) for (i = 0; i < day.options.length; i++) out.push({ t: "choose", opt: day.options[i].id });
      else out.push({ t: "task", id: day.task });
    } else if (state.beat === "task") out.push({ t: "task", id: state.task });
    else if (state.beat === "gate") {
      miss = gateMissing(state);
      if (!miss.length) out.push({ t: "gate", how: "pass" }); else { out.push({ t: "gate", how: "hold" }); out.push({ t: "gate", how: "open" }); }
    } else if (state.beat === "done") out.push({ t: "next" });
    if (state.mode !== "org") {
      if (!state.moved) out.push({ t: "move" });
      if (canFix(data, state)) out.push({ t: "fixcap" });
      for (i = 0; i < state.debts.length; i++) { d = state.debts[i]; if (d.state === "sealed") out.push({ t: "repair", debt: i }); }
    }
    return out;
  }

  function reduce(data, prev, action) {
    var state = clone(prev), day = today(data, state), miss, i, d, r, a, well, opt;
    function finishChoice() {            // a colleague's task is done the way they chose
      if (state.beat === "task" && state.botWell != null) { doTask(data, state, state.task, botTask(data, state, state.task, state.botWell)); state.beat = day.gate ? "gate" : "done"; }
      // a colleague opens the gate with whatever is on file; only a sponsor's rule makes them hold it
      if (state.beat === "gate") { miss = gateMissing(state); gate(miss.length ? (state.mode === "org" && forced(data, state, "d6") ? "hold" : "open") : "pass"); }
      state.botWell = null;
    }
    function gate(how) {
      miss = gateMissing(state);
      if (how === "hold") {
        for (i = 0; i < miss.length; i++) file(state, miss[i]);
        if (miss.indexOf("bar") >= 0) state.flags.hold = true;
        delete state.flags.noBudget;
        note(state, "gate", "The gate holds. " + miss.length + " " + (miss.length === 1 ? "document is" : "documents are") + " written now, before anything is built.", 2 * miss.length);
      } else if (how === "open") {
        note(state, "gate", "The gate is opened without " + (miss.length === 3 ? "any of the three" : "everything") + ". The build starts.");
        seal(data, state, data.days[state.i], { due: "d8", days: 1 + miss.length, trust: 0, tag: "the gate, opened without its documents",
          text: "The build started from what there was. Every engineer asked the same three questions in the first week." });
      } else {
        note(state, "gate", "What it may do, how right it must be and its limits are signed. The gate opens.");
      }
      state.beat = "done";
    }
    switch (action.t) {
      case "choose":
        if (state.beat !== "choose" || state.pending || !choose(data, state, action.opt)) return prev;
        break;
      case "accept":
      case "challenge":
        if (state.beat !== "choose" || !state.pending) return prev;
        if (action.t === "challenge") { if (state.tokens < 1 || (day.options && action.opt === state.pending)) return prev; state.tokens--; }
        if (!day.options) {           // Day 90: the slide
          well = action.t === "challenge" || (state.mode === "org" ? forced(data, state, day.id) : !habit(state, day.id));
          if (action.t === "challenge" && action.input) { doTask(data, state, day.task, action.input); }
          else doTask(data, state, day.task, botTask(data, state, day.task, well));
          state.pending = null; state.beat = "done";
          break;
        }
        opt = action.t === "challenge" ? action.opt : state.pending;
        state.pending = null;
        if (!choose(data, state, opt)) return prev;
        r = rightOption(day);
        // In a role, a challenged call becomes the player's own, task and all. The sponsor only asks:
        // the team then does the day, and does it the way it was chosen.
        if (action.t === "accept" || state.mode === "org") { state.botWell = !!(r && r.id === opt); finishChoice(); }
        break;
      case "task":
        if (state.beat === "choose" && !day.options && !state.pending && day.task === action.id) { doTask(data, state, action.id, action.input); state.beat = "done"; break; }
        if (state.beat !== "task" || state.task !== action.id) return prev;
        doTask(data, state, action.id, action.input);
        state.beat = day.gate ? "gate" : "done";
        break;
      case "gate":
        if (state.beat !== "gate") return prev;
        miss = gateMissing(state);
        if ((action.how === "pass") !== (miss.length === 0)) return prev;
        gate(action.how);
        break;
      case "next":
        if (state.beat !== "done") return prev;
        if (state.i === data.days.length - 1) { state.beat = "end"; state.events = []; break; }
        state.i++; openDay(data, state);
        if (state.mode === "org") { /* the sponsor only watches: each day's call is accepted for her */ }
        break;
      case "move":
        if (state.moved || state.beat === "end" || state.mode === "org") return prev;
        applyMove(data, state);
        break;
      case "fixcap":
        if (!canFix(data, state) || state.mode === "org") return prev;
        applyFix(data, state);
        break;
      case "repair":
        d = state.debts[action.debt];
        if (!d || d.state !== "sealed" || state.beat === "end" || state.mode === "org") return prev;
        d.state = "repaired";
        if (d.id === "d12") state.capInTool = true;        // going back to the incident means putting the limit in the tool
        if (d.id === "d9") {                                // going back to the score means reading it slice by slice
          for (i = 0; i < state.debts.length; i++) if (state.debts[i].id === "d9" && state.debts[i].state === "sealed") state.debts[i].state = "repaired";
          state.tasks.score = botTask(data, state, "score", true); state.live = { same: "ship", code: "hold", refund: "shadow" };
        }
        r = rightOption(variant(data, { capInTool: false }, data.days[dayIndex(data, d.id)]));
        a = r ? arts(r) : []; for (i = 0; i < a.length; i++) file(state, a[i]);
        note(state, "repair", "You go back to Day " + d.from + " and do it properly.", repairCost(data, d));
        break;
      default:
        return prev;
    }
    state.history.push(action);
    return state;
  }

  function fold(data, opts, history) {
    var s = init(data, opts), i, n;
    for (i = 0; i < history.length; i++) { n = reduce(data, s, history[i]); if (n === s) break; s = n; }
    return s;
  }

  /* ------------------------------------------------------------------ the ending */
  // The case's own first cycle: 31.2 person-days saved at $320, a model bill of $4,200, and 96 hours of
  // review at $72. Net: minus $1,128. Away from that line the figures move with what the run did.
  function ledger(data, state) {
    var f = 1, t = data.tasks.score, b, i, st, live = state.live, share = 0, bill, review = 6912, mishaps, value;
    if (state.flags.heldBack) f -= 0.3;
    if (state.flags.frozen) f -= 0.2;
    if (live) {
      b = bars(data, state);
      for (i = 0; i < t.slices.length; i++) { st = sliceStats(t.slices[i]); if (live[t.slices[i].id] === "ship" && st.score >= b[t.slices[i].id]) share += t.slices[i].n; }
      if (share < 400) f -= 0.25;                  // the same-day cases, four in five, were ready and did not ship
    }
    f = Math.max(0, f);
    value = Math.round(9984 * f);
    bill = Math.round(4200 * (state.flags.billOpen ? 2.2 : (state.bill && state.bill > 2 ? 1.3 : 1)));
    mishaps = 2000 * (state.incidents || 0) + (state.debts.some(function (d) { return d.id === "d12" && d.state === "fired" && d.tag === "a name, and no control"; }) ? 2000 : 0);
    return { saving: Math.round(43 * f), days: round(31.2 * f, 1), value: value, bill: bill, review: review, mishaps: mishaps,
             cost: bill + review + mishaps, net: value - bill - review - mishaps };
  }

  function verdict(data, state) {
    var late = Math.max(0, -state.slack), key;
    if (state.trust <= 0 || late > 15) key = "stopped";
    else if (state.trust >= 5 && late === 0) key = "funded";
    else if (state.trust >= 3 && late <= 6) key = "conditional";
    else key = "paused";
    return { key: key, late: late, trust: state.trust, shelf: state.shelf.length,
             fired: state.debts.filter(function (d) { return d.state === "fired"; }).length,
             repaired: state.debts.filter(function (d) { return d.state === "repaired"; }).length };
  }

  var api = { init: init, reduce: reduce, fold: fold, legal: legal, today: today, price: price, mine: mine, owner: owner,
              rightOption: rightOption, bars: bars, barOf: barOf, sliceStats: sliceStats, gateMissing: gateMissing, canFix: canFix,
              repairCost: repairCost, ledger: ledger, verdict: verdict, botTask: botTask, botPick: botPick, dayIndex: dayIndex, has: has };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else { root.ND = root.ND || {}; root.ND.sim = api; }
})(typeof window !== "undefined" ? window : this);
