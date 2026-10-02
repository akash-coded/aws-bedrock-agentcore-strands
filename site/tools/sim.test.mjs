// The rules of Ninety Days, walked without a browser.
//
//   node site/tools/sim.test.mjs            every assertion, and a summary of the economy
//
// It plays every combination of choices in whole-team mode (with each hands-on task done well or
// badly), every role, and every set of three rules in the organisation lens, and checks that the game
// cannot dead-end, that no shortcut is free, and that neither "always the cheapest" nor "always the
// most careful" gets funded. It also lints the words: a scene is forty words at most, nothing carries
// a dash, and every day opens cold: a headline that is a sentence, one sentence of context, a recap on
// every option, and a "So far" line of twenty-five words at most on every path.
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const sim = require(join(here, "..", "play", "sim.js"));
const data = JSON.parse(readFileSync(join(here, "..", "play", "days.json"), "utf8"));

let failures = 0;
const check = (ok, what) => { if (!ok) { failures++; console.log("  FAIL " + what); } };
const RANK = { stopped: 0, paused: 1, conditional: 2, funded: 3 };

// a task done well, or done the way a hurried team does it
const taskInput = (id, well) => sim.botTask(data, null, id, well);
const SLIDES = [["saving", "bill", "net"], ["saving", "score", "shelf"], ["saving", "bill", "shelf"]];

// one step of play under a fixed habit for the optional moves
function settle(state, habit) {
  let s = state;
  if (habit.fix && sim.canFix(data, s) && !s.capInTool && s.mode !== "org") s = sim.reduce(data, s, { t: "fixcap" });
  if (habit.move && s.slack < 0 && !s.moved && s.beat !== "end" && s.mode !== "org") s = sim.reduce(data, s, { t: "move" });
  return s;
}

// every way through the thirteen days, as a tree: each branch is visited once
function walk(state, habit, visit, depth = 0) {
  state = settle(state, habit);
  if (state.beat === "end") { visit(state); return; }
  check(depth < 80, "a path ran past 80 steps");
  const day = sim.today(data, state);
  const moves = [];
  if (state.beat === "choose") {
    if (state.pending) moves.push({ t: "accept" });
    else if (day.options) for (const o of day.options) moves.push({ t: "choose", opt: o.id });
    else for (const sl of SLIDES) moves.push({ t: "task", id: day.task, input: sl });
  } else if (state.beat === "task") {
    if (state.task === "slide") for (const sl of SLIDES) moves.push({ t: "task", id: "slide", input: sl });
    else for (const well of [true, false]) moves.push({ t: "task", id: state.task, input: taskInput(state.task, well) });
  } else if (state.beat === "gate") {
    const miss = sim.gateMissing(state);
    if (!miss.length) moves.push({ t: "gate", how: "pass" }); else moves.push({ t: "gate", how: "hold" }, { t: "gate", how: "open" });
  } else if (state.beat === "done") moves.push({ t: "next" });
  check(moves.length > 0, `no move on day ${day.day} in beat ${state.beat}`);
  const offered = sim.legal(data, state);
  for (const m of moves) {
    check(offered.some((o) => o.t === m.t && (o.opt === undefined || o.opt === m.opt) && (o.how === undefined || o.how === m.how) && (o.id === undefined || o.id === m.id)),
      `the rules do not offer ${JSON.stringify(m).slice(0, 60)} on day ${day.day}`);
    const next = sim.reduce(data, state, m);
    check(next !== state, `a legal move was refused on day ${day.day}: ${JSON.stringify(m)}`);
    if (next !== state) walk(next, habit, visit, depth + 1);
  }
}

// one fixed line of play: a function from (day, state) to an option id
function line(pick, opts = {}, habit = { fix: true, move: true }, well = true, slide = SLIDES[0], inputs = {}) {
  let s = sim.init(data, opts), guard = 0;
  while (s.beat !== "end" && guard++ < 200) {
    s = settle(s, habit);
    const day = sim.today(data, s);
    let a;
    if (s.beat === "choose") a = s.pending ? { t: "accept" } : day.options ? { t: "choose", opt: pick(day, s) } : { t: "task", id: day.task, input: slide };
    else if (s.beat === "task") a = { t: "task", id: s.task, input: s.task === "slide" ? slide : inputs[s.task] || taskInput(s.task, well) };
    else if (s.beat === "gate") a = { t: "gate", how: sim.gateMissing(s).length ? (habit.gate || "hold") : "pass" };
    else a = { t: "next" };
    const n = sim.reduce(data, s, a);
    if (n === s) { check(false, "a fixed line stalled on day " + day.day); break; }
    s = n;
  }
  return s;
}
const right = (day) => sim.rightOption(day).id;
const cheapest = (day, s) => day.options.slice().sort((a, b) => sim.price(data, s, day, a) - sim.price(data, s, day, b))[0].id;
const dearest = (day, s) => day.options.slice().sort((a, b) => sim.price(data, s, day, b) - sim.price(data, s, day, a))[0].id;
// the state at the opening of each day of a finished run, and everything the rules said on the way
function opens(end, opts = {}) {
  let s = sim.init(data, opts); const out = [s], said = [];
  for (const a of end.history) { s = sim.reduce(data, s, a); for (const e of s.events) said.push(e.text); if (a.t === "next" && s.beat !== "end") out.push(s); }
  return { days: out, said };
}
const wc = (t) => t.trim().split(/\s+/).length;
const show = (s) => { const v = sim.verdict(data, s), l = sim.ledger(data, s); return `${v.key}, trust ${v.trust}, runway ${s.slack}, ${v.shelf} on file, ${v.fired} debts fired, net $${l.net}`; };

console.log("\n1. the words");
{
  const dash = /[–—]/;
  const texts = [];
  const collect = (o) => { if (typeof o === "string") texts.push(o); else if (o && typeof o === "object") Object.values(o).forEach(collect); };
  collect(data);
  check(!texts.some((t) => dash.test(t)), "a dash in the copy");
  for (const d of data.days) {
    const forms = d.variants ? Object.values(d.variants) : [d];
    for (const f of forms) {
      const words = f.scene.map((l) => l[1]).join(" ").split(/\s+/).length;
      check(words <= 40, `day ${d.day}: the scene runs to ${words} words`);
      for (const o of f.options || []) check(o.label.split(/\s+/).length <= 14, `day ${d.day}: option "${o.label}" is long`);
      for (const o of f.options || []) if (o.debt) check(sim.dayIndex(data, o.debt.due) > sim.dayIndex(data, d.id), `day ${d.day}: a debt falls due before it is made`);
      check(!f.options || f.options.filter((o) => o.right).length === 1, `day ${d.day}: exactly one option is the method's`);
    }
    if (d.needs) check(!!data.artefacts[d.needs], `day ${d.day} leans on an unknown document`);
  }
  // Every day opens cold. The headline is a sentence with a verb or a number in it, never a noun. The
  // context is one sentence. A recap is past tense, ten words at most, and points back at nothing.
  const sentences = (t) => t.split(/(?<=[.?!])\s+/).filter(Boolean);
  const JARGON = /\b(NFRs?|ADRs?|PDLC|gates?|slices?|bolts?|lower bound|authority budget|autonomy|specs?|P[0-3])\b/i;
  const VERB = /\d|\b(is|are|was|were|has|have|must|cannot|set|starts|asks|will|tried|sent|refused|build|buy|borrow)\b/i;
  const plain = (t, what) => {
    check(typeof t === "string" && t.length > 0, `${what} is missing`); if (!t) return;
    check(!dash.test(t), `${what} carries a dash`);
    check(!JARGON.test(t), `${what} uses a word the player has not been given yet: "${t}"`);
    check(!/\bnot\b[^.?!]*\bbut\b/i.test(t), `${what} is a "not this but that"`);
    for (const one of sentences(t)) check(wc(one) <= 20, `${what} has a sentence of ${wc(one)} words`);
  };
  plain(data.short, "the premise"); check(wc(data.short) <= 12 && sentences(data.short).length === 1, "the premise on every day is longer than one short sentence");
  for (const d of data.days) {
    const forms = d.variants ? Object.values(d.variants) : [d];
    plain(d.context, `day ${d.day}: the context`);
    check(sentences(d.context || "").length === 1 && wc(d.context || "") <= 16, `day ${d.day}: the context is more than one short sentence`);
    check(!("title" in d) && !("track" in d), `day ${d.day} still carries a title or a track`);
    for (const f of forms) {
      plain(f.head, `day ${d.day}: the headline`);
      check(VERB.test(f.head || ""), `day ${d.day}: the headline "${f.head}" is a bare noun`);
      for (const o of f.options || []) {
        plain(o.recap, `day ${d.day}, option ${o.id}: the recap`);
        if (!o.recap) continue;
        check(wc(o.recap) <= 10, `day ${d.day}, option ${o.id}: the recap runs to ${wc(o.recap)} words`);
        check(/^[a-z]+ed\b|^(wrote|sent|left|let|took|built|kept|put|held|had|cut)\b/.test(o.recap) && !/[.?!]$/.test(o.recap), `day ${d.day}, option ${o.id}: the recap "${o.recap}" is not a past-tense clause`);
        check(!/\b(it|this|that|these|those|them|they)\b/i.test(o.recap), `day ${d.day}, option ${o.id}: the recap points back with a pronoun`);
      }
    }
  }
  for (const [k, a] of Object.entries(data.artefacts)) { plain(a.on, `${k}: its "on file" sentence`); plain(a.off, `${k}: its "not on file" sentence`); }
  // nothing a player reads says "gate": it is the sign-off (ids and addresses keep the old word)
  check(!texts.some((t) => /\s/.test(t) && /\bgates?\b/i.test(t)), "the copy still says gate");
  // "So far", at its longest: any option of the day it quotes, with any of the things it can have left
  for (let i = 1; i < data.days.length; i++) {
    const d = data.days[i], src = d.needs ? sim.source(data, d.needs) : i - 1;
    check(src >= 0 && src < i, `day ${d.day} leans on a document that no earlier day files`);
    if (!(src >= 0 && src < i)) continue;
    const from = data.days[src], forms = from.variants ? Object.values(from.variants) : [from];
    for (const f of forms) for (const o of f.options || []) {
      const lefts = ["Today a choice from Day 82 comes back.", "Something from that is pinned to Day 82."];
      if (d.needs) lefts.push(data.artefacts[d.needs].on, data.artefacts[d.needs].off);
      else for (const a of [].concat(o.art || [])) lefts.push(data.artefacts[a].on);
      for (const left of lefts) { const n = wc(`So far: on Day ${from.day}, Priya ${o.recap}. ${left}`); check(n <= 25, `day ${d.day}: "So far" can run to ${n} words after day ${from.day}, option ${o.id}`); }
    }
  }
}

console.log("\n2. fixed lines, whole team");
const canon = line(right);
console.log("  the method, date moved with evidence:  " + show(canon));
{
  // What a stranger reads before the scene on each day of the method's line. The premise and "So far"
  // are there only for someone who has seen no other day: under forty words, on any path (12 + 25).
  const o = opens(canon); let most = 0;
  check(o.days.length === data.days.length, "the method's line does not open thirteen days");
  o.days.forEach((s, i) => {
    const so = sim.soFar(data, s), line = so.label + " " + so.text, d = sim.today(data, s);
    check(so.text.length > 0 && wc(line) <= 25, `day ${d.day}: "So far" is empty or long on the method's line: "${line}"`);
    check(i === 0 ? /nothing yet/.test(so.text) : new RegExp("^on Day \\d+, you ").test(so.text), `day ${d.day}: "So far" does not quote an earlier call: "${line}"`);
    check(wc(data.short) + wc(line) < 40, `day ${d.day}: the premise and "So far" run to forty words`);
    most = Math.max(most, wc(data.short) + wc(d.context) + wc(line));
  });
  console.log(`  the premise, the context and "So far" together: ${most} words at most on the method's line`);
  check(most <= 48, "a day's opening lines run past forty-eight words");
  check(!o.said.some((t) => /\bgates?\b/i.test(t) || /[–—]/.test(t)), "the rules still say gate, or carry a dash");
}
check(sim.verdict(data, canon).key === "funded", "doing every day properly, and moving the date on evidence, is not funded");
const noMove = line(right, {}, { fix: true, move: false });
console.log("  the method, date never moved:          " + show(noMove));
check(sim.verdict(data, noMove).key !== "funded", "the method fits the runway without moving the date, so there is no dilemma");
const unnoticed = line(right, {}, { fix: false, move: true });
console.log("  the method, the limit never checked:   " + show(unnoticed));
check(RANK[sim.verdict(data, unnoticed).key] <= RANK[sim.verdict(data, canon).key] && unnoticed.trust < canon.trust, "never checking where the limit lives costs nothing");
const cheap = line(cheapest, {}, { fix: false, move: true, gate: "open" }, false, SLIDES[1]);
console.log("  always the cheapest:                   " + show(cheap));
{
  const o = opens(cheap);
  o.days.forEach((s) => { const so = sim.soFar(data, s), line = so.label + " " + so.text; check(so.text.length > 0 && wc(line) <= 25, `day ${sim.today(data, s).day}: "So far" is empty or long on the cheapest line: "${line}"`); });
  check(o.days.slice(1).some((s) => /pinned to Day|comes back/.test(sim.soFar(data, s).text)), "on the cheapest line \"So far\" never mentions what is owed");
  check(!o.said.some((t) => /\bgates?\b/i.test(t) || /[–—]/.test(t)), "the rules still say gate, or carry a dash");
}
check(sim.verdict(data, cheap).key !== "funded" && sim.verdict(data, cheap).key !== "conditional", "always the cheapest option does not lose");
const dear = line(dearest, {}, { fix: true, move: true });
console.log("  always the most careful:               " + show(dear));
check(sim.verdict(data, dear).key !== "funded", "always the most expensive option is funded");

console.log("\n3. no shortcut is free");
check(!canon.moved || canon.slack - data.rules.moveDate.days < 0, "the method's line fits the runway without moving the date");
for (const d of data.days) {
  const forms = d.variants ? [d.variants.blocked] : [d];
  for (const o of forms[0].options || []) {
    if (o.right) continue;
    // Days in hand before any move of the date, and trust: one of them has to be worse than the
    // method's line, or the shortcut was free. A worse ledger alone does not count, since the verdict
    // does not read it.
    const dev = line((day) => day.id === d.id ? o.id : right(day), {}, { fix: true, move: true, gate: "hold" }, true);
    const inHand = (s) => s.slack - (s.moved ? data.rules.moveDate.days : 0);
    check(inHand(dev) < inHand(canon) || dev.trust < canon.trust, `day ${d.day}, "${o.label}" costs nothing: ${show(dev)}`);
  }
}
// the incident's own wrong answer, when the refund was paid
{
  const dev = line((day) => day.id === "d12" ? "a" : right(day), {}, { fix: false, move: true });
  check(dev.trust < unnoticed.trust, "asking who approved the prompt costs nothing");
}

// The sixth task, on Day 6: what cannot be ranked comes out before anything is ranked.
{
  const lim = data.tasks.limits, real = lim.lines.filter((l) => l.miss).map((l) => l.id), wish = lim.lines.filter((l) => !l.miss).map((l) => l.id);
  const d3 = data.days.find((d) => d.id === "d3"), inHand = (s) => s.slack - (s.moved ? data.rules.moveDate.days : 0);
  check(sim.rightOption(d3).task === "limits" && d3.options.filter((o) => o.task === "limits").length === 1, "the limits task does not open behind Day 6's method option alone");
  check(real.length === 3 && wish.length === 3, "the limits task is not three limits and three wishes");
  // the method's line up to the task, then the task done one way
  const at = canon.history.findIndex((a) => a.t === "task" && a.id === "limits");
  check(at > 0, "the method's line never does the limits task");
  const before = sim.fold(data, {}, canon.history.slice(0, at));
  const done = (input) => sim.reduce(data, before, { t: "task", id: "limits", input });
  const owed = (s) => s.debts.filter((d) => d.id === "d3" && d.state === "sealed");
  check(owed(done(real)).length === 0 && done(real).slack === before.slack && done(real).trust === before.trust, "the limits task, done right, costs something");
  check(JSON.stringify(sim.botTask(data, null, "limits", true)) === JSON.stringify(real), "a colleague who does the limits task well does not tick the three limits");
  const want = { law: { due: "d6", days: 2, trust: 1 }, system: { due: "d4", days: d3.options.find((o) => o.id === "a").debt.days, trust: 0 }, cap: { due: "d8", days: 2, trust: 0 } };
  for (const r of real) {
    const o = owed(done(real.filter((x) => x !== r)));
    check(o.length === 1 && o[0].due === want[r].due && o[0].days === want[r].days && o[0].trust === want[r].trust, `the limits task: missing "${r}" does not pin ${JSON.stringify(want[r])}`);
    const end = line(right, {}, { fix: true, move: true }, true, SLIDES[0], { limits: real.filter((x) => x !== r) });
    check(end.debts.some((d) => d.id === "d3" && d.state === "fired") && (inHand(end) < inHand(canon) || end.trust < canon.trust), `the limits task: missing "${r}" is free: ${show(end)}`);
  }
  for (const input of [real.concat(wish[0]), real.concat(wish)]) {
    const o = owed(done(input));
    check(o.length === 1 && o[0].due === "d4" && o[0].days === 1 && !o[0].trust, `the limits task: ${input.length - 3} wishes ticked do not cost Day 9 one day`);
    const end = line(right, {}, { fix: true, move: true }, true, SLIDES[0], { limits: input });
    check(inHand(end) === inHand(canon) - 1 && end.trust === canon.trust, `the limits task: ticking a wish does not cost exactly a day: ${show(end)}`);
  }
  // everything it left is one trip back
  const worst = done([wish[0]]), n = owed(worst).length, back = sim.reduce(data, worst, { t: "repair", debt: worst.debts.findIndex((d) => d.id === "d3") });
  check(n === 4 && owed(back).length === 0 && back.slack === worst.slack - sim.repairCost(data, worst.debts.find((d) => d.id === "d3")), "going back to Day 6 does not repair everything the limits task left");
  const bad = line(right, {}, { fix: true, move: true }, true, SLIDES[0], { limits: sim.botTask(data, null, "limits", false) });
  console.log("  the method, the limits task done badly: " + show(bad));
  check(sim.verdict(data, bad).key !== "funded", "the limits task done badly is still funded");
}

// three lines that should not be funded
{
  const lazy = line((day) => ({ d10: "a", d11: "c" })[day.id] || (day.id === "d12" ? "a" : right(day)), {}, { fix: true, move: false });
  console.log("  the method, with three quiet shortcuts: " + show(lazy));
  check(sim.verdict(data, lazy).key !== "funded", "three shortcuts with no price are funded");
  let early = sim.reduce(data, sim.init(data, {}), { t: "move" });
  check(early.trust <= data.rules.trust - 3, "moving the date on Day 1 with nothing on file costs less than three trust");
  const noRead = line(right, {}, { fix: true, move: true }, false);
  console.log("  the method's calls, every task done badly: " + show(noRead));
  check(sim.verdict(data, noRead).key !== "funded", "doing every hands-on task badly is still funded");
}

console.log("\n4. every path, whole team");
for (const seed of process.env.FAST ? [] : process.env.SEEDS ? process.env.SEEDS.split(',').map(Number) : [0, 1, 2]) {
  for (const habit of [{ fix: true, move: true }, { fix: false, move: false }]) {
    const tally = { funded: 0, conditional: 0, paused: 0, stopped: 0 }; let n = 0, minT = 9, maxT = -9;
    const byMiss = {};
    const t0 = Date.now();
    walk(sim.init(data, { seed }), habit, (s) => {
      const key = sim.verdict(data, s).key;
      n++; tally[key]++;
      minT = Math.min(minT, s.trust); maxT = Math.max(maxT, s.trust);
      // how many of the twelve calls were not the method's
      let miss = 0;
      for (const d of data.days) if (d.options || d.variants) { const day = d.variants ? d.variants[s.picks.d12 && s.incidents ? "paid" : "blocked"] : d; const r = day.options.find((o) => o.right); if (s.picks[d.id] !== r.id) miss++; }
      (byMiss[miss] = byMiss[miss] || { funded: 0, conditional: 0, paused: 0, stopped: 0 })[key]++;
    });
    if (seed === 0 && habit.fix) for (const m of Object.keys(byMiss)) { const b = byMiss[m], t = b.funded + b.conditional + b.paused + b.stopped; console.log(`    ${String(m).padStart(2)} calls off the method: funded ${(100 * b.funded / t).toFixed(0)}%, conditional ${(100 * b.conditional / t).toFixed(0)}%, paused ${(100 * b.paused / t).toFixed(0)}%, stopped ${(100 * b.stopped / t).toFixed(0)}%`); }
    if (habit.fix) check(maxT === data.rules.trustMax && minT === 0, "trust never reaches the top or the bottom of its range");
    console.log(`  seed ${seed}, ${habit.fix ? "limit checked, date moved" : "limit never checked, date never moved"}: ${n} endings ` +
      `(${Object.entries(tally).map(([k, v]) => k + " " + v).join(", ")}) in ${Date.now() - t0}ms`);
    if (seed === 0 && habit.fix) for (const k of Object.keys(tally)) check(tally[k] > 0, `no path ends "${k}"`);
    if (habit.fix) check(tally.funded / n < 0.2, "more than one path in five is funded: too easy");
  }
}

console.log("\n5. one role");
for (const role of Object.keys(data.roles)) {
  // your own days done properly, colleagues left alone; then with three challenges spent on the first three shortcuts
  const alone = line(right, { mode: "role", role });
  let s = sim.init(data, { mode: "role", role }), guard = 0;
  while (s.beat !== "end" && guard++ < 200) {
    s = settle(s, { fix: true, move: true });
    const day = sim.today(data, s);
    let a;
    if (s.beat === "choose") {
      if (s.pending) {
        const r = day.options ? sim.rightOption(day).id : null;
        const wrong = day.options ? s.pending !== r : true;
        a = wrong && s.tokens > 0 ? (day.options ? { t: "challenge", opt: r } : { t: "challenge", input: SLIDES[0] }) : { t: "accept" };
      } else a = day.options ? { t: "choose", opt: right(day) } : { t: "task", id: day.task, input: SLIDES[0] };
    } else if (s.beat === "task") a = { t: "task", id: s.task, input: s.task === "slide" ? SLIDES[0] : taskInput(s.task, true) };
    else if (s.beat === "gate") a = { t: "gate", how: sim.gateMissing(s).length ? "hold" : "pass" };
    else a = { t: "next" };
    const n = sim.reduce(data, s, a); if (n === s) { check(false, `role ${role} stalled on day ${day.day}`); break; } s = n;
  }
  const mineDays = data.days.filter((d) => data.cast[d.owner].role === role).length;
  console.log(`  ${role.padEnd(4)} owns ${mineDays} days · colleagues left alone: ${show(alone)}`);
  console.log(`       three challenges, spent early:    ${show(s)}`);
  check(RANK[sim.verdict(data, s).key] >= RANK[sim.verdict(data, alone).key], `role ${role}: spending challenges made things worse`);
  // a colleague who sorts the limits does the task well exactly when they chose the method's option
  for (const end of [alone, s]) check(end.picks.d3 !== "b" || !end.debts.some((d) => d.id === "d3"), `role ${role}: Day 6 was done by the method and still left something`);
  for (const st of opens(alone, { mode: "role", role }).days.slice(1)) {
    const so = sim.soFar(data, st), line = so.label + " " + so.text, mine = data.days.find((d) => d.day === so.from);
    check(so.text.length > 0 && wc(line) <= 25, `role ${role}, day ${sim.today(data, st).day}: "So far" is empty or long: "${line}"`);
    check((so.who === "you") === (data.cast[mine.owner].role === role), `role ${role}, day ${sim.today(data, st).day}: "So far" names the wrong person: "${line}"`);
  }
}

console.log("\n6. the organisation lens: every set of up to three rules");
{
  const ids = data.policies.map((p) => p.id), sets = [[]];
  for (let a = 0; a < ids.length; a++) { sets.push([ids[a]]); for (let b = a + 1; b < ids.length; b++) { sets.push([ids[a], ids[b]]); for (let c = b + 1; c < ids.length; c++) sets.push([ids[a], ids[b], ids[c]]); } }
  const rows = sets.map((set) => { const s = line(right, { mode: "org", policies: set }); return { set, s, v: sim.verdict(data, s) }; });
  rows.sort((x, y) => RANK[y.v.key] - RANK[x.v.key] || y.s.trust - x.s.trust || y.s.slack - x.s.slack);
  for (const r of rows.slice(0, 4)) console.log(`  ${r.set.join(" + ").padEnd(24)} ${show(r.s)}`);
  console.log("  ...");
  for (const r of rows.slice(-2)) console.log(`  ${(r.set.join(" + ") || "no rules").padEnd(24)} ${show(r.s)}`);
  const kinds = new Set(rows.map((r) => r.v.key));
  check(kinds.size >= 3, "the organisation lens gives fewer than three different verdicts");
  check(RANK[rows.find((r) => r.set.length === 0).v.key] === 0, "enforcing nothing is not stopped");
  check(RANK[rows[0].v.key] >= 2, "no set of three rules keeps the programme alive");
  // the sponsor may also ask to see the evidence twice: with the best three rules, that is enough
  let best = null;
  for (const r of rows.filter((x) => x.set.length === 3)) {
    let s = sim.init(data, { mode: "org", policies: r.set }), guard = 0;
    while (s.beat !== "end" && guard++ < 200) {
      const day = sim.today(data, s); let a;
      if (s.beat === "choose" && s.pending) {
        const rt = day.options ? sim.rightOption(day).id : null;
        a = s.tokens > 0 && (day.options ? s.pending !== rt : !r.set.includes("both")) ? (day.options ? { t: "challenge", opt: rt } : { t: "challenge" }) : { t: "accept" };
      } else a = { t: "next" };
      const n = sim.reduce(data, s, a); if (n === s) { check(false, "the organisation lens stalled on day " + day.day); break; } s = n;
    }
    if (!best || RANK[sim.verdict(data, s).key] > RANK[sim.verdict(data, best.s).key] || (sim.verdict(data, s).key === sim.verdict(data, best.s).key && s.trust > best.s.trust)) best = { set: r.set, s };
  }
  console.log(`  best with two questions asked: ${best.set.join(" + ")}: ${show(best.s)}`);
  check(sim.verdict(data, best.s).key === "funded", "no three rules plus two questions gets the programme funded");
}

console.log("\n7. a save is its list of actions");
{
  const replay = sim.fold(data, {}, canon.history);
  check(JSON.stringify(replay) === JSON.stringify(canon), "replaying a run's actions does not rebuild the run");
  const junk = sim.fold(data, {}, [{ t: "nonsense" }, { t: "choose", opt: "zz" }]);
  check(junk.i === 0 && junk.beat === "choose", "junk actions moved the game");
}

console.log("\n8. a link to a day: the earlier days, played by the book");
for (const seed of [0, 1, 2]) {
  let words = 0;
  for (let i = 0; i < data.days.length; i++) {
    const h = sim.book(data, { seed }, i), s = sim.fold(data, { seed }, h), d = data.days[i];
    check(s.i === i && s.beat === "choose" && !s.pending && s.history.length === h.length, `seed ${seed}: the book does not open on Day ${d.day}`);
    check(data.days.slice(0, i).every((e) => s.picks[e.id] === sim.rightOption(e.variants ? e.variants.blocked : e).id), `seed ${seed}, Day ${d.day}: an earlier day was not played the method's way`);
    check(!s.debts.length && s.trust >= data.rules.trust, `seed ${seed}, Day ${d.day}: the book leaves something owed, or trust spent`);
    check(s.slack + (s.moved ? 0 : data.rules.moveDate.days) >= 0, `seed ${seed}, Day ${d.day}: the book opens the day late with the date already moved`);
    check(i <= sim.dayIndex(data, data.rules.capFix.from) || s.capInTool, `seed ${seed}, Day ${d.day}: the book never typed the limit into the tool`);
    check(s.shelf.length >= Math.min(i, 4) && Object.keys(s.tasks).length === ["d3", "d6", "d9", "d10", "d11"].filter((id) => sim.dayIndex(data, id) < i).length, `seed ${seed}, Day ${d.day}: the book skipped a task or a document`);
    const so = sim.soFar(data, s), line = so.label + " " + so.text;
    check(so.text.length > 0 && wc(data.short) + wc(line) < 40, `seed ${seed}, Day ${d.day}: opened cold, the premise and "So far" run to ${wc(data.short) + wc(line)} words`);
    words = Math.max(words, wc(data.short) + wc(sim.today(data, s).context) + wc(line));
  }
  const end = sim.fold(data, { seed }, sim.book(data, { seed }, data.days.length - 1));
  console.log(`  seed ${seed}: all thirteen days open by the book; Day 90 opens at trust ${end.trust}, runway ${end.slack}, ${end.shelf.length} on file; at most ${words} words before the scene`);
}
check(sim.book(data, {}, 0).length === 0, "the book for Day 1 is not empty");

console.log(failures ? `\n${failures} failure(s)` : "\nthe rules hold");
process.exit(failures ? 1 : 0);
