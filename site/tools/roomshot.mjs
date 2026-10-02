// Draw one room of the game into a PNG at one times, exactly as the game draws it on that day.
//
//   node site/tools/roomshot.mjs <room> <day> <out.png>   the room on that day, the days before it played by the book
//   node site/tools/roomshot.mjs --check                  draw every room picture the site carries again, and compare
//                                                         each with its file, pixel by pixel
//
// The home page shows two rooms as still pictures: Day 45's QA room on the day card (sim-day45.png) and the boardroom
// on Day 90 on the library's simulator card (sim-board.png). Both are drawn here by the game's own code: play/art.js
// paints the room, play/sim.js plays the days before it by the book, and what the walls show and who stands where are
// read out of play/game.js (picture, whereabouts, bookAt), so a picture is the game's own frame and never a copy of
// it. The clock is held at 0, as the game's room is once its people have walked in. Rooms: board, product, arch, eng,
// qa, platform, centre, lobby. A day is its number in the game (1, 4, 6 ... 90).
//
// Every shape in a room is opaque but the ceiling lamps' cones of light, drawn at 7.5%, and those are the only pixels
// a rasteriser can change. Chrome is started on its GPU canvas (SwiftShader, the GPU in software, the same on every
// machine), as a reader's browser draws the game and as sim-day45.png was drawn: the CPU canvas blends the 7.5% one
// unit apart inside the cones. On 3 October 2026 this tool redrew Day 45 and every pixel of sim-day45.png matched but
// 48 on the cones' slanted edges, by at most 4 units: antialiasing samples an edge differently on each GPU. So --check
// says how many pixels differ and by how much, and passes while no channel is more than 4 units out; a moved figure,
// prop or sky changes a pixel by far more.
// Chrome over the DevTools protocol, as the other tools, so there is nothing to install; CHROME names the browser.

import { spawn } from "node:child_process";
import { readFileSync, writeFileSync, existsSync, mkdtempSync, rmSync } from "node:fs";
import { inflateSync } from "node:zlib";
import { tmpdir } from "node:os";
import { join } from "node:path";

const PLAY = new URL("../play/", import.meta.url), PICTURES = new URL("../assets/pictures/", import.meta.url);
const CARRIED = [["qa", 45, "sim-day45.png"], ["board", 90, "sim-board.png"]];      // the rooms the site shows, for --check

const args = process.argv.slice(2), check = args[0] === "--check";
if (!check && args.length !== 3) {
  console.error("usage: node roomshot.mjs <room> <day> <out.png>   or   node roomshot.mjs --check");
  process.exit(2);
}

// a function or an object out of game.js, from its first line to its closing brace
const game = readFileSync(new URL("game.js", PLAY), "utf8");
function take(head) {
  const a = game.indexOf(head);
  if (a < 0) throw new Error(`play/game.js no longer has "${head}"`);
  let i = game.indexOf("{", a), depth = 0;
  for (; i < game.length; i++) if (game[i] === "{") depth++; else if (game[i] === "}" && --depth === 0) break;
  return game.slice(a, i + 1);
}
const GAME = [take("var HOME = {") + ";", take("function picture(state) {"), take("function whereabouts(state) {"),
  take("function wayAt(i, role) {"), "var booked = {};", take("function bookAt(i, role) {")].join("\n");
const DATA = readFileSync(new URL("days.json", PLAY), "utf8");

// the room as the game's own room canvas draws it: today's people in today's room, the rest at their own desks
const draw = (room, day) => `(() => { "use strict";
  var data = ${DATA}, sim = window.ND.sim, A = window.NDArt;
  ${GAME}
  var i = data.days.findIndex(function (d) { return d.day === ${+day}; });
  if (i < 0 || !(${JSON.stringify(room)} in A.ROOMS || ${JSON.stringify(room)} === "lobby")) return { error: ${JSON.stringify(`no room "${room}" on Day ${day}`)} };
  var state = bookAt(i), today = sim.today(data, state), st = picture(state), who = whereabouts(state)[${JSON.stringify(room)}] || null;
  var speaking = today.room === ${JSON.stringify(room)} && today.scene && today.scene[0] ? today.scene[0][0] : null;
  var c = document.createElement("canvas"), g;
  c.width = A.W; c.height = A.H; g = c.getContext("2d"); g.imageSmoothingEnabled = false;
  A.room(g, ${JSON.stringify(room)}, 0, st, true, who, speaking, 1);
  return { png: c.toDataURL("image/png"), who: who || [], speaking: speaking, sky: st.sky,
           name: data.rooms[${JSON.stringify(room)}].replace(/^[A-Z](?=[a-z])/, function (x) { return x.toLowerCase(); }) };
})()`;

// a PNG's pixels, decoded here (8-bit RGB or RGBA, not interlaced: what Chrome writes), so the comparison owes
// nothing to a browser's decoder or its colour management
function pixels(buf) {
  let p = 8, w = 0, h = 0, type = 0;
  const idat = [];
  while (p < buf.length) {
    const len = buf.readUInt32BE(p), kind = buf.toString("latin1", p + 4, p + 8), body = buf.subarray(p + 8, p + 8 + len);
    if (kind === "IHDR") {
      w = body.readUInt32BE(0); h = body.readUInt32BE(4); type = body[9];
      if (body[8] !== 8 || (type !== 2 && type !== 6) || body[12]) throw new Error("only 8-bit RGB or RGBA, not interlaced");
    }
    if (kind === "IDAT") idat.push(body);
    p += 12 + len;
  }
  const bpp = type === 6 ? 4 : 3, raw = inflateSync(Buffer.concat(idat)), row = w * bpp, out = Buffer.alloc(w * h * 4);
  let prev = Buffer.alloc(row);
  for (let y = 0; y < h; y++) {
    const f = raw[y * (row + 1)], line = Buffer.from(raw.subarray(y * (row + 1) + 1, (y + 1) * (row + 1)));
    for (let x = 0; x < row; x++) {
      const a = x >= bpp ? line[x - bpp] : 0, b = prev[x], c = x >= bpp ? prev[x - bpp] : 0;
      const pa = Math.abs(b - c), pb = Math.abs(a - c), pc = Math.abs(a + b - 2 * c);
      line[x] = (line[x] + [0, a, b, (a + b) >> 1, pa <= pb && pa <= pc ? a : pb <= pc ? b : c][f]) & 255;
    }
    for (let x = 0; x < w; x++) for (let k = 0; k < 4; k++) out[(y * w + x) * 4 + k] = k < bpp ? line[x * bpp + k] : 255;
    prev = line;
  }
  return { w, h, data: out };
}

const DIR = mkdtempSync(join(tmpdir(), "roomshot-"));
const chrome = spawn(process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  ["--headless=new", "--use-angle=swiftshader", "--remote-debugging-port=0", `--user-data-dir=${DIR}`, "--no-first-run",
    "--no-default-browser-check", "about:blank"],
  { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let failed = 0;
try {
  let port = 0, wsu;
  for (let i = 0; i < 80 && !port; i++) { try { port = +readFileSync(join(DIR, "DevToolsActivePort"), "utf8").split("\n")[0]; } catch { await sleep(250); } }
  for (let i = 0; i < 60 && !wsu; i++) {
    try { wsu = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === "page")?.webSocketDebuggerUrl; } catch { await sleep(250); }
  }
  if (!wsu) throw new Error("Chrome did not start");
  const ws = new WebSocket(wsu);
  await new Promise((r) => ws.addEventListener("open", r, { once: true }));
  let seq = 0;
  const waiting = new Map();
  ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); } });
  const send = (method, params = {}) => new Promise((r) => { const id = ++seq; waiting.set(id, r); ws.send(JSON.stringify({ id, method, params })); });
  const run = async (expression) => {
    const m = await send("Runtime.evaluate", { expression, returnByValue: true });
    if (m.error || m.result.exceptionDetails) throw new Error(JSON.stringify(m.error || m.result.exceptionDetails).slice(0, 400));
    return m.result.result.value;
  };
  await run(readFileSync(new URL("art.js", PLAY), "utf8") + "\n;true");
  await run(readFileSync(new URL("sim.js", PLAY), "utf8") + "\n;true");
  const shoot = async (room, day) => {
    const r = await run(draw(room, day));
    if (r.error) throw new Error(r.error);
    return { ...r, png: Buffer.from(r.png.split(",")[1], "base64") };
  };
  if (!check) {
    const [room, day, out] = args, r = await shoot(room, day);
    writeFileSync(out, r.png);
    console.log(`${out}: the ${r.name} on Day ${day}, ${r.sky} sky, ${r.who.join(", ") || "nobody"} in it` +
      `${r.speaking ? `, ${r.speaking} speaking` : ""}; ${r.png.length} bytes`);
  } else {
    for (const [room, day, file] of CARRIED) {
      const path = new URL(file, PICTURES);
      if (!existsSync(path)) { failed++; console.log(`  FAIL ${file}: no such file`); continue; }
      const r = await shoot(room, day), was = readFileSync(path), a = pixels(was), b = pixels(r.png), off = [];
      if (a.w !== b.w || a.h !== b.h) { failed++; console.log(`  FAIL ${file}: ${a.w} x ${a.h} on file, ${b.w} x ${b.h} drawn`); continue; }
      let most = 0;
      for (let k = 0; k < a.data.length; k += 4) {
        let d = 0;
        for (let c = 0; c < 4; c++) d = Math.max(d, Math.abs(a.data[k + c] - b.data[k + c]));
        if (!d) continue;
        most = Math.max(most, d);
        off.push(`(${(k / 4) % a.w}, ${Math.floor(k / 4 / a.w)}) ${[...a.data.subarray(k, k + 4)]} on file, ${[...b.data.subarray(k, k + 4)]} drawn`);
      }
      const say = `the ${r.name} on Day ${day}: `, n = a.w * a.h;
      if (most > 4) { failed++; console.log(`  FAIL ${file}: ${say}${off.length} of ${n} pixels differ, by up to ${most}: ${off.slice(0, 12).join("; ")}`); }
      else if (off.length) console.log(`  ok   ${file}: ${say}${off.length} of ${n} pixels differ, none by more than ${most}, as a rasteriser's edges do`);
      else console.log(`  ok   ${file}: ${say}all ${n} pixels as drawn${was.equals(r.png) ? ", byte for byte" : ""}`);
    }
  }
  ws.close();
} catch (e) {
  failed++;
  console.log("roomshot failed: " + e.message);
} finally {
  const exited = new Promise((r) => chrome.once("exit", r));
  chrome.kill();
  await Promise.race([exited, sleep(3000)]);
  try { rmSync(DIR, { recursive: true, force: true }); } catch { /* the profile goes with the temp folder */ }
}
process.exit(failed ? 1 : 0);
