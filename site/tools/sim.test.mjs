// The rules of Ninety Days, walked without a browser.
//
//   node site/tools/sim.test.mjs            every assertion, and a summary of the economy
//
// It plays every combination of choices in whole-team mode (with each hands-on task done well or
// badly), every role, and every set of three rules in the organisation lens, and checks that the game
// cannot dead-end, that no shortcut is free, and that neither "always the cheapest" nor "always the
// most careful" gets funded. It also lints the words: a scene is forty words at most, nothing carries
// a dash, and every day opens cold: a headline that is a sentence, one sentence of context, a recap on
// every option, and a "So far" line of twenty-five words at most on every path, which quotes the one
// earlier day that today leans on and never joins two. It checks that a document waits for its task,
// that a question can be asked of a sound plan as well as an unsound one and shows only evidence, and
// that the verdict's saving follows from the run: a late run never reports the saving of one on time.
// The book that opens a day for a link plays the whole team exactly as it did before a role could start
// later, and a role's late start the same way: every earlier day done the recommended way, so the role starts
// with all its questions and nothing owed. From every start the page offers, some line still ends funded.
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
  // The title says what this is before it says its name, and a first-time visitor learns the whole of it
  // there: a game, a fictional airline's project, an AI assistant for stranded passengers, ninety days,
  // thirteen decisions, each costing days.
  plain(data.what, "what the game is"); plain(data.premise, "the title's opening lines"); plain(data.pitch, "the title's pitch");
  check(/\bgame\b/i.test(data.what) && !new RegExp(data.title, "i").test(data.what), `the line above the name does not say this is a game: "${data.what}"`);
  for (const need of [/fictional airline/, /AI assistant/, /stranded passengers/, /ninety days/, /thirteen decisions/, /costs days/])
    check(need.test(data.premise), `the title's opening lines leave out ${need}: "${data.premise}"`);
  // The title's line of the ninety days: its caption and the note on Day 1's card are plain words, and
  // the four milestones it marks are days of the game, in order, the first of them the sign-off.
  plain(data.line.caption, "the line's caption"); plain(data.line.card, "the note in Day 1's kicker");
  // the briefing before a day opened late (its heading, its section names, its buttons and the link back to it), and the link to a role's first call
  plain("Days 1 to 30 were " + data.line.book, "the briefing's heading");
  for (const [k, t] of Object.entries(data.brief)) { plain(t.replace("{day}", "45"), `the briefing's "${k}"`); check(/\{day\}/.test(t) === ["start", "back", "again"].includes(k), `the briefing's "${k}" ${/\{day\}/.test(t) ? "names a day it should not" : "does not name its day"}: "${t}"`); }
  check(/\{day\}/.test(data.line.first), `the link to a role's first call does not name its day: "${data.line.first}"`); plain(data.line.first.replace("{day}", "45"), "the link to a role's first call");
  // the other words the page shows from this file
  // the run's line over the building (GAME.md, "The run's line"): its words, filled as the page fills them, and
  // the trace it is drawn from, which must add up on every day of the recommended run
  const fill = { left: "with 4 days left", ref: "3 days late", day: "45", n: "2 days", days: "Days 1 and 30" };
  for (const [k, t] of Object.entries(data.run)) for (const one of typeof t === "string" ? [t] : Object.values(t)) plain(one.replace(/\{(\w+)\}/g, (m, x) => fill[x] || m), `the run's line, "${k}"`);
  {
    const o = { mode: "team", seed: 0, from: 0 }, tr = sim.trace(data, o, sim.book(data, o, data.days.length));
    check(tr.length === data.days.length && tr.every((r) => !r.live), `the recommended run's trace has ${tr.length} days, not ${data.days.length} closed ones`);
    for (const r of tr) check(r.before - r.events.reduce((a, e) => a + e.days, 0) + (r.events.some((e) => e.kind === "move") ? data.rules.moveDate.days : 0) === r.close, `Day ${data.days[r.i].day}'s trace does not add up`);
    const one = sim.trace(data, o, []);
    check(one.length === 1 && one[0].live && one[0].before === data.rules.slack, "a run not yet begun is not one live day that opened with the spare days");
  }
  plain(data.building.caption, "the building's caption"); plain(data.org.way, "the sponsor's way to play"); plain(data.org.intro, "the sponsor's rules screen");
  plain(data.days.find((d) => d.gate).signoff, "the sign-off's intro"); for (const [k, v] of Object.entries(data.days.find((d) => d.variants).variants)) plain(v.fig, `Day 82's figure, ${k}`);
  data.monday.forEach((q, k) => plain(q, `question ${k + 1} for Monday`));
  const miles = Object.keys(data.line.milestones);
  check(miles.length === 4 && miles.every((id, k) => sim.dayIndex(data, id) >= 0 && (!k || sim.dayIndex(data, id) > sim.dayIndex(data, miles[k - 1]))), `the milestones are not four days in order: ${miles.join(", ")}`);
  check(!!data.days[sim.dayIndex(data, miles[0])].gate, "the first milestone is not the sign-off's day");
  for (const id of miles) { const m = data.line.milestones[id]; plain(m.flag, `the milestone on ${id}`); check(/^the /.test(m.name) && m.name.split(" ").length <= 4, `the milestone on ${id} is named "${m.name}"`); }
  // A headline, a context line and a question are each read alone, as if on a poster. So each headline
  // names what it is about (the AI assistant, the project, or the people by their role), no line points
  // at something outside itself, and every question says who is to act.
  const POINTS = /\b(them|they|these|those|none|he|she|we|us|our)\b/i, ABOUT = /AI assistant|assistant's|\bproject\b|managers|engineers/;
  for (const d of data.days) {
    for (const f of d.variants ? Object.values(d.variants) : [d]) {
      check(ABOUT.test(f.head), `day ${d.day}: the headline does not name what it is about: "${f.head}"`);
      check(sentences(f.head).length <= 2, `day ${d.day}: the headline is more than two sentences`);
      for (const [what, t] of [["headline", f.head], ["context", d.context], ["question", f.ask]]) {
        check(!POINTS.test(t), `day ${d.day}: the ${what} points at someone or something it does not name: "${t}"`);
        // "it" and "its" are allowed only after the thing they stand for, inside the same sentence
        for (const one of sentences(t)) check(!/^(It|Its)\b(?! is the first week)/.test(one) && (!/\b(it|its)\b/.test(one) || /\b(assistant|agent|refund|team)\b[^.?!]*\b(it|its)\b|\bits\b[^.?!]*\b(assistant|team)\b/.test(one) || /^It is the first week/.test(one)),
          `day ${d.day}: the ${what} says "it" before saying what: "${one}"`);
      }
      check(/\?$/.test(f.ask) && /\bshould\b/.test(f.ask) && /team|managers|engineers|QA lead|review|slide/.test(f.ask), `day ${d.day}: the question does not say who is to do what: "${f.ask}"`);
    }
  }
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
  // Every day after the first says which earlier day it leans on, and which document decides what
  // that day left. Where it gives its own sentences for that, they are plain too.
  for (let i = 1; i < data.days.length; i++) {
    const d = data.days[i], l = d.leans;
    check(!!l && sim.dayIndex(data, l.day) >= 0 && sim.dayIndex(data, l.day) < i, `day ${d.day} does not say which earlier day it leans on`);
    check(!!l && !!data.artefacts[l.doc], `day ${d.day} leans on an unknown document`);
    if (!l || !data.artefacts[l.doc]) continue;
    const filed = sim.source(data, l.doc);
    check(filed >= 0 && filed < i, `day ${d.day} leans on a document that no earlier day files`);
    if (d.needs) check(sim.source(data, d.needs) >= 0 && sim.source(data, d.needs) < i, `day ${d.day} needs a document that no earlier day files`);
    for (const k of ["on", "off"]) if (l[k] != null) plain(l[k], `day ${d.day}: what the day it leans on left (${k})`);
    // "So far", at its longest: any option of the day it quotes, with any of the things it can have left
    const from = data.days[sim.dayIndex(data, l.day)], forms = from.variants ? Object.values(from.variants) : [from];
    const lefts = ["Today that choice comes back.", "Today something left from that day comes back.", "Something from that is pinned to Day 82.", "That day was done again later, properly.",
      l.on || data.artefacts[l.doc].on, l.off || data.artefacts[l.doc].off];
    for (const f of forms) for (const o of f.options || []) for (const left of lefts) {
      const n = wc(`So far: on Day ${from.day}, Priya ${o.recap}. ${left}`);
      check(n <= 25, `day ${d.day}: "So far" can run to ${n} words after day ${from.day}, option ${o.id}`);
    }
  }
  // no day is quoted by more than three others, and two days that quote the same one say different things about it
  {
    const by = {};
    for (const d of data.days.slice(1)) (by[d.leans.day] = by[d.leans.day] || []).push(d);
    for (const [k, list] of Object.entries(by)) {
      check(list.length <= 3, `${list.length} days all lean on ${k}`);
      const said = list.map((d) => d.leans.on || data.artefacts[d.leans.doc].on);
      check(new Set(said).size === said.length, `two days that lean on ${k} say the same thing about it`);
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
  const lines = o.days.map((s) => sim.soFar(data, s).text);
  check(new Set(lines).size === lines.length, `two days of the method's line open with the same "So far"`);
  check(/cost/.test(lines[10]), `Day 75's "So far" says nothing about cost on the method's line: "${lines[10]}"`);
  check(/refund/.test(lines[11]), `Day 82's "So far" says nothing about refunds on the method's line: "${lines[11]}"`);
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
  // "So far" quotes one day. It may say where that day's debt is pinned; it never brings in a second day's choice.
  o.days.slice(1).forEach((s) => {
    const so = sim.soFar(data, s), others = (so.text.match(/Day \d+/g) || []).filter((x) => x !== "Day " + so.from), d = sim.today(data, s);
    check(!/choice from Day/.test(so.text) && others.length <= (/pinned to Day/.test(so.text) ? 1 : 0), `day ${d.day}: "So far" joins two days on the cheapest line: "${so.text}"`);
    check(so.from === data.days[sim.dayIndex(data, data.days[s.i].leans.day)].day, `day ${d.day}: "So far" quotes Day ${so.from}, not the day it leans on`);
  });
  check(!o.said.some((t) => /\bgates?\b/i.test(t) || /[–—]/.test(t)), "the rules still say gate, or carry a dash");
}
check(sim.verdict(data, cheap).key !== "funded" && sim.verdict(data, cheap).key !== "conditional", "always the cheapest option does not lose");
const dear = line(dearest, {}, { fix: true, move: true });
console.log("  always the most careful:               " + show(dear));
check(sim.verdict(data, dear).key !== "funded", "always the most expensive option is funded");

// The verdict's numbers follow from the run. The case's own line is the method's: 31.2 person-days, net
// minus $1,128. A run that is late was live for fewer days and saved less; a stopped run does not report
// the funded run's saving.
{
  const L = (s) => sim.ledger(data, s);
  check(L(canon).days === 31.2 && L(canon).value === 9984 && L(canon).net === -1128, `the method's line is not the case's own ledger: ${JSON.stringify(L(canon))}`);
  check(sim.verdict(data, cheap).key === "stopped" && L(cheap).days < L(canon).days && L(cheap).value < L(canon).value, `a stopped run reports the funded run's saving: ${L(cheap).days} person-days`);
  check(noMove.slack < 0 && L(noMove).days < L(canon).days, `a late run reports the saving of one on time: ${L(noMove).days} person-days`);
  check(L(dear).days < L(canon).days, "holding everything back for one bar saved as much as shipping what was ready");
  const off = line((day) => day.id === "d11" ? "c" : right(day));
  check(L(off).days < L(canon).days, "a week switched off saved as much as a week live");
  const pass = line((day) => day.id === "d9" ? "a" : right(day));
  check(L(pass).days < L(canon).days, "shipping everything on one number saved as much as shipping what was proven");
  console.log(`  saved, in person-days: the method ${L(canon).days}, date never moved ${L(noMove).days}, always the cheapest ${L(cheap).days}, always the most careful ${L(dear).days}`);
}

// A document that an option promises and a task produces goes on file when the task is done, not before.
{
  for (const [id, docs] of [["d3", ["constraints"]], ["d6", ["spec", "budget", "bar"]], ["d9", ["proof"]], ["d10", ["lanes"]], ["d11", ["rootcause"]]]) {
    const at = canon.history.findIndex((a, k) => a.t === "task" && sim.today(data, sim.fold(data, {}, canon.history.slice(0, k))).id === id);
    check(at > 0, `the method's line has no task on ${id}`);
    if (at <= 0) continue;
    const before = sim.fold(data, {}, canon.history.slice(0, at)), after = sim.fold(data, {}, canon.history.slice(0, at + 1));
    check(before.beat === "task" && docs.every((x) => !sim.has(before, x)) && before.filed.length === 0, `${id}: a document is on file before its task is done`);
    check(docs.every((x) => sim.has(after, x)), `${id}: the task is done and its documents are not on file`);
  }
}

// A question. It can be asked of any plan, sound or not, so being able to ask tells nothing. It costs one
// question whatever it shows, it shows only what is on file and what would go on file, and after it the
// plan can be changed at no further cost.
{
  for (const opts of [{ mode: "org", policies: [] }, { mode: "org", policies: ["signed", "code", "both"] }, { mode: "role", role: "qa" }]) {
    let s = sim.init(data, opts), guard = 0, sound = 0, unsound = 0;
    while (s.beat !== "end" && guard++ < 200) {
      const day = sim.today(data, s);
      if (s.beat === "choose" && s.pending) {
        const r = day.options ? sim.rightOption(day).id : null, legal = sim.legal(data, s);
        if (s.tokens > 0) {
          check(legal.some((a) => a.t === "ask"), `${opts.mode}, day ${day.day}: a question cannot be asked of this plan`);
          if (day.options) (s.pending === r ? sound++ : unsound++);
        } else check(!legal.some((a) => a.t === "ask" || a.t === "challenge"), `${opts.mode}, day ${day.day}: a question is offered with none left`);
        check(sim.evidence(data, s) !== null, `${opts.mode}, day ${day.day}: a plan has no evidence behind it`);
      } else check(sim.evidence(data, s) === null, `${opts.mode}, day ${day.day}: evidence with no plan to ask about`);
      const n = sim.reduce(data, s, s.beat === "choose" ? (s.pending ? { t: "accept" } : day.options ? { t: "choose", opt: right(day) } : { t: "task", id: day.task, input: SLIDES[0] })
        : s.beat === "task" ? { t: "task", id: s.task, input: taskInput(s.task, true) } : s.beat === "gate" ? { t: "gate", how: sim.gateMissing(s).length ? "hold" : "pass" } : { t: "next" });
      if (n === s) break; s = n;
    }
    if (opts.mode === "org" && opts.policies.length) check(sound > 0, "under three rules no sound plan was ever open to a question");
    if (opts.mode === "org" && !opts.policies.length) check(sound > 0 && unsound > 0, `with no rules a question was open on ${sound} sound plans and ${unsound} unsound ones`);
  }
  // one question, asked of a sound plan and of an unsound one
  const org = sim.init(data, { mode: "org", policies: [] });                    // Day 1: the architect merges the list, unprompted
  check(org.pending === sim.rightOption(sim.today(data, org)).id, "Day 1 under no rules is not a sound plan");
  const asked = sim.reduce(data, org, { t: "ask" });
  check(asked !== org && asked.tokens === org.tokens - 1 && asked.seen && asked.pending === org.pending, "asking about a sound plan does not cost one question and leave the plan as it was");
  check(sim.reduce(data, asked, { t: "ask" }) === asked, "the same plan can be asked about twice");
  const ev = sim.evidence(data, asked);
  check(ev && Object.keys(ev).sort().join() === "doc,files,has" && ev.files.join() === "register", `the evidence for Day 1 is ${JSON.stringify(ev)}`);
  const other = sim.reduce(data, asked, { t: "challenge", opt: "a" });
  check(other !== asked && other.tokens === asked.tokens && other.picks.d1 === "a", "after a question, asking for something else costs a second question");
  const direct = sim.reduce(data, org, { t: "challenge", opt: "a" });
  check(direct !== org && direct.tokens === org.tokens - 1, "asking for something else without a question first is free");
  let none = asked; none = sim.reduce(data, none, { t: "accept" }); none = sim.reduce(data, none, { t: "next" });
  const spent = sim.reduce(data, none, { t: "ask" });
  check(spent.tokens === 0 && sim.reduce(data, sim.reduce(data, sim.reduce(data, spent, { t: "accept" }), { t: "next" }), { t: "ask" }).tokens === 0, "a third question can be asked with two");
  // Day 90: the evidence is the slide as planned
  const last = sim.fold(data, { mode: "org", policies: [] }, line(right, { mode: "org", policies: [] }).history.slice(0, -2));
  check(last.i === 12 && last.pending && Array.isArray(sim.evidence(data, last).slide) && sim.evidence(data, last).slide.length === 3, "on Day 90 the evidence is not the slide as planned");
}

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
    const tally = { funded: 0, conditional: 0, paused: 0, stopped: 0 }; let n = 0, minT = 9, maxT = -9, lateRich = 0; const canonDays = sim.ledger(data, canon).days;
    const byMiss = {};
    const t0 = Date.now();
    walk(sim.init(data, { seed }), habit, (s) => {
      const key = sim.verdict(data, s).key;
      n++; tally[key]++;
      if (s.slack < 0 && sim.ledger(data, s).days >= canonDays) lateRich++;
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
    check(lateRich === 0, `${lateRich} late endings report the saving of a run that met the date`);
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

console.log("\n9. a late start: every earlier day done the recommended way, in one role as in the whole team");
{
  // The whole-team book as it was before a role could start later, kept here word for word. The book must play
  // every whole-team day exactly as this did. A late start's earlier days now wait for nobody (openDay), so a role
  // that starts late is played by these very moves too, on its own runway.
  const before = (opts, upto) => {
    let s = sim.init(data, opts), day, a, n, guard = 0;
    while (s.i < upto && s.beat !== "end" && guard++ < 400) {
      day = sim.today(data, s);
      if (sim.canFix(data, s)) a = { t: "fixcap" };
      else if (s.slack < 0 && !s.moved) a = { t: "move" };
      else if (s.beat === "choose") a = day.options ? { t: "choose", opt: sim.rightOption(day).id } : { t: "task", id: day.task, input: sim.botTask(data, s, day.task, true) };
      else if (s.beat === "task") a = { t: "task", id: s.task, input: sim.botTask(data, s, s.task, true) };
      else if (s.beat === "gate") a = { t: "gate", how: sim.gateMissing(s).length ? "hold" : "pass" };
      else a = { t: "next" };
      n = sim.reduce(data, s, a); if (n === s) break; s = n;
    }
    return s.history;
  };
  const roles = Object.keys(data.roles);
  let same = 0, alike = 0;
  for (const opts of [{ seed: 0 }, { seed: 1 }, { seed: 2 }, { mode: "team", seed: 0, from: 8 }])
    for (let i = 0; i <= data.days.length; i++) { const ok = JSON.stringify(sim.book(data, opts, i)) === JSON.stringify(before(opts, i)); check(ok, `the whole-team book changed on Day ${(data.days[i] || { day: "the end" }).day}, ${JSON.stringify(opts)}`); same += ok; }
  for (const role of roles) for (let i = 0; i < data.days.length; i++) {
    const o = { mode: "role", role, seed: 0, from: i }, ok = JSON.stringify(sim.book(data, o, i)) === JSON.stringify(before(o, i));
    check(ok, `${role}: the book to Day ${data.days[i].day} is not the whole team's moves`); alike += ok;
  }
  console.log(`  the whole-team book: ${same} histories, seeds 0 to 2 and the page's own, every day and the end, the same as before; ${alike} late starts in one role, by the same moves`);
  // Without a start of its own the book stops at a colleague's first day, where a plan waits: the page always passes one.
  check(sim.fold(data, { mode: "role", role: "qa" }, sim.book(data, { mode: "role", role: "qa" }, 8)).i === 0, "the book got past a colleague's day in a run that starts at Day 1");

  // A late start opens with every earlier call the recommended option, every task done well and nothing owed. In one
  // role it also has all its questions, and opens as the whole team's late start does: the same calls, tasks,
  // documents, trust and limit, the same days spent, on a runway two days longer (so the date may not need moving).
  const cell = (s) => `${s.trust} ${String(s.slack).padStart(3)} ${String(s.shelf.length).padStart(2)}`, table = [];
  const longer = data.rules.slackRole - data.rules.slack, moveDays = data.rules.moveDate.days, spent = (s) => s.slack - (s.moved ? moveDays : 0);
  data.days.forEach((d, i) => {
    const to = { mode: "team", seed: 0, from: i }, t = sim.fold(data, to, sim.book(data, to, i));
    check(data.days.slice(0, i).every((e) => t.picks[e.id] === sim.rightOption(e.variants ? e.variants.blocked : e).id) && !t.debts.length, `the whole team's Day ${d.day}: an earlier call was not the recommended one, or something is owed`);
    let row = `  ${String(d.day).padStart(3)}   ${cell(t)}   `;
    for (const role of roles) {
      const o = { mode: "role", role, seed: 0, from: i }, h = sim.book(data, o, i), s = sim.fold(data, o, h);
      check(s.i === i && s.beat === "choose" && s.history.length === h.length, `${role}: the book does not open Day ${d.day}`);
      check(s.tokens === data.rules.questions.role && !s.seen && !s.debts.length && !h.some((a) => /^(ask|accept|challenge)$/.test(a.t)), `${role}, Day ${d.day}: a late start opens with ${s.tokens} questions and ${s.debts.length} debts, or the book questioned or let stand a plan before it`);
      check(JSON.stringify([s.picks, s.tasks, s.shelf, s.trust, s.capInTool]) === JSON.stringify([t.picks, t.tasks, t.shelf, t.trust, t.capInTool]) && spent(s) === spent(t) + longer,
        `${role}, Day ${d.day}: a late start in one role opens unlike the whole team's: ${cell(s)} against ${cell(t)}`);
      check(!!s.pending === !sim.mine(data, s, d), `${role}: Day ${d.day} opens with the wrong person to call it`);
      const so = sim.soFar(data, s), from = i ? data.days.find((x) => x.day === so.from) : null;
      check(so.text.length > 0 && wc(so.label + " " + so.text) <= 25, `${role}, Day ${d.day}: "So far" is empty or long when opened by the book`);
      if (from) check((so.who === "you") === (data.cast[from.owner].role === role), `${role}, Day ${d.day}: "So far" names the wrong person: "${so.text}"`);
      if (role === roles[0]) row += `${cell(s)} ${s.tokens}`;
    }
    table.push(row);
  });
  console.log("  at the opening of each day, by the book: trust, runway, documents on file (in one role, every role alike, and questions left)");
  console.log("  day   team       in one role");
  table.forEach((t) => console.log(t));
  // A run from Day 1 in one role is as it was: no day comes before its start, so each colleague's day opens with their plan waiting.
  for (const role of roles) for (const st of opens(line(right, { mode: "role", role }), { mode: "role", role }).days)
    check(!!st.pending === !sim.mine(data, st, data.days[st.i]), `${role}, from Day 1: Day ${data.days[st.i].day} opens with ${st.pending ? "a plan waiting on the player's own day" : "no plan waiting on a colleague's day"}`);

  // Every start the page offers, and the best ending it can still reach. The line of the ninety days offers the whole
  // team each of the thirteen days (seed 0, as its links open them) and Day 1 from Start (any seed: the vendor's freeze
  // falls on one of three days); a role's row offers its own days (seed 0) and Day 1 from its button (any seed). Measured:
  // from every one of them some line still ends funded, the best ending, so that is what is asserted.
  // The search is memoised over every move the rules offer (each option, each task done well or badly, three slides,
  // questions, repairs, the date, the limit). It tries first what a player who knows the method would do (question a plan
  // that is not the recommended way while a question is left), and drops a line that can no longer end funded (trust
  // five, the date met): trust rises twice at most (on Day 82 if the limit is in the tool or can still be put there, and
  // with Day 90's slide), a colleague's slide with no question left costs three, and every day still to come costs at
  // least its cheapest option, a freeze still ahead its two days and a sealed debt the lesser of its days and its
  // repair, with four days back if the date is still to move. A line it finds is replayed to its verdict.
  const L = data.days.length - 1, I82 = sim.dayIndex(data, "d12"), FIXTO = sim.dayIndex(data, data.rules.capFix.until), fr = data.rules.pressure;
  const cheapest = data.days.map((d) => Math.min(...(d.variants ? Object.values(d.variants) : [d]).flatMap((f) => (f.options || [{ days: 0 }]).map((o) => o.days))));
  const allMoves = (s) => sim.legal(data, s).flatMap((m) => m.t === "task" ? (m.id === "slide" ? SLIDES.map((x) => ({ t: "task", id: "slide", input: x })) : [true, false].map((w) => ({ t: "task", id: m.id, input: taskInput(m.id, w) })))
    : m.t === "challenge" && !m.opt ? [{ t: "challenge", input: SLIDES[0] }] : [m]);
  const digest = (s) => JSON.stringify([s.i, s.beat, s.task, s.pending, s.seen, s.tokens, s.slack, s.trust, s.moved, s.capInTool, s.incidents, s.shelf.slice().sort(), s.debts.map((d) => d.id + d.due + d.state + d.tag), s.flags, s.hold]);
  const knows = (s) => {
    const day = sim.today(data, s), r = sim.rightOption(day);
    if (sim.canFix(data, s)) return { t: "fixcap" };
    if (s.slack < 0 && !s.moved) return { t: "move" };
    if (s.pending) return (r && s.pending === r.id) || !(s.seen || s.tokens > 0) ? { t: "accept" } : !s.seen ? { t: "ask" } : r ? { t: "challenge", opt: r.id } : { t: "challenge", input: SLIDES[0] };
    if (s.beat === "choose") return day.options ? { t: "choose", opt: r.id } : { t: "task", id: day.task, input: SLIDES[0] };
    if (s.beat === "task") return { t: "task", id: s.task, input: s.task === "slide" ? SLIDES[0] : taskInput(s.task, true) };
    if (s.beat === "gate") return { t: "gate", how: sim.gateMissing(s).length ? "hold" : "pass" };
    return { t: "next" };
  };
  const bound = (s) => {
    let trust = s.trust, slack = s.slack + (s.moved ? 0 : moveDays);
    if (s.i < I82 && (s.capInTool || s.i <= FIXTO)) trust++;
    if (s.i < L || s.beat === "choose") trust += s.mode === "role" && !sim.mine(data, s, data.days[L]) && !s.tokens && !(s.i === L && s.seen) ? -3 : 1;
    for (let k = s.beat === "choose" ? s.i : s.i + 1; k <= L; k++) slack -= cheapest[k];
    if (sim.dayIndex(data, fr.onDay[s.seed % fr.onDay.length]) > s.i) slack -= fr.days;
    const owed = {};
    for (const d of s.debts) if (d.state === "sealed") owed[d.id] = { days: (owed[d.id] ? owed[d.id].days : 0) + d.days, back: sim.repairCost(data, d) };
    for (const o of Object.values(owed)) slack -= Math.min(o.days, o.back);
    return { trust, slack };
  };
  const reach = (s, memo) => {             // a line from s that ends funded, or null
    if (s.beat === "end") return sim.verdict(data, s).key === "funded" ? [] : null;
    const b = bound(s); if (b.trust < 5 || b.slack < 0) return null;
    const k = digest(s); if (memo.has(k)) return null;
    const first = knows(s), f = JSON.stringify(first);
    for (const m of [first].concat(allMoves(s).filter((x) => JSON.stringify(x) !== f))) {
      const n = sim.reduce(data, s, m); if (n === s) continue;
      const rest = reach(n, memo); if (rest) return [m].concat(rest);
    }
    memo.set(k, true); return null;
  };
  const starts = [];
  data.days.forEach((d, i) => starts.push({ label: `the whole team from Day ${d.day}`, o: { mode: "team", seed: 0, from: i }, i }));
  for (const seed of [1, 2]) starts.push({ label: `the whole team from Day 1, seed ${seed}`, o: { mode: "team", seed }, i: 0 });
  for (const role of roles) {
    data.days.forEach((d, i) => { if (i && d.owner === data.roles[role].who) starts.push({ label: `${role} from Day ${d.day}`, o: { mode: "role", role, seed: 0, from: i }, i }); });
    for (const seed of [0, 1, 2]) starts.push({ label: `${role} from Day 1, seed ${seed}`, o: { mode: "role", role, seed }, i: 0 });
  }
  // a memo per player and seed: a state reached from any of their starts has the same future whichever start it came from
  const memos = new Map(), t0 = Date.now(); let slow = { t: -1 };
  for (const st of starts) {
    const key = (st.o.role || "team") + st.o.seed; if (!memos.has(key)) memos.set(key, new Map());
    const s = sim.fold(data, st.o, sim.book(data, st.o, st.i)), t1 = Date.now(), found = reach(s, memos.get(key));
    const end = found ? found.reduce((x, a) => sim.reduce(data, x, a), s) : null;
    check(!!end && sim.verdict(data, end).key === "funded", `${st.label}: no line still ends funded`);
    if (Date.now() - t1 > slow.t) slow = { t: Date.now() - t1, label: st.label };
  }
  console.log(`  from each of the ${starts.length} starts the line and the rows offer, some line still ends funded (searched in ${((Date.now() - t0) / 1000).toFixed(1)}s; the longest, ${slow.label}, ${(slow.t / 1000).toFixed(1)}s)`);
}

console.log(failures ? `\n${failures} failure(s)` : "\nthe rules hold");
process.exit(failures ? 1 : 0);
