/* Ninety Days · the art.
   Everything the game shows on its canvas is drawn here, in code. There are no image files.

   The picture is SkyWays' head office, cut open: four floors, seven rooms. It is drawn at one logical
   pixel per unit and scaled up by whole numbers, so every edge stays hard. A room is lit when
   something is happening in it and dim when not, which is how the picture says where to look.

   Colour comes from light and material. Each room's walls take a little of its owner's jacket; the sky
   outside is the phase of the project (dawn, morning, afternoon, golden hour, then dusk on Day 90, or
   night if the run is late); lamps are warm against it. Rose is kept for the sign-off and what is owed.

   People are 12 x 19 sprites made from one body and a few heads of hair, recoloured: a cast of
   twelve from one drawing. Sprites are rows of characters looked up in a small legend, then drawn
   once to an offscreen canvas with a one-pixel outline. */
(function (root) {
  "use strict";

  /* ---------------------------------------------------------------- palette */
  var C = {
    night: "#0B0D12", page: "#121316", sky0: "#10141D", sky1: "#182132", sky2: "#22304A", star: "#DDECFA",
    out: "#07080B",                       // outline and deepest shadow
    wallD: "#171A21", wall: "#20242D", wallL: "#2A303B", trim: "#39414F", floor: "#454E5E", floorL: "#59647A",
    dim: "#12151B",                       // a room with the lights off
    desk: "#5B4A3C", deskL: "#7A6450", deskD: "#3B3028", metal: "#566074", metalL: "#7C879C", metalD: "#333A47",
    glass: "#2B3A52", glassL: "#3C5273", paper: "#ECEAE4", ink: "#ECEAE4", soft: "#93908A",
    lamp: "#F2D9A0", lampD: "#C99A52", screen: "#0E1B24", screenL: "#1D3545",
    slate: "#8FA8BE", indigo: "#8E9BF0", teal: "#4FBDB6", amber: "#D9A94A", rose: "#DE8A8A", green: "#6BBE8B",
    violet: "#AE93E0", sky: "#6FB9D9", plant: "#4E9A6B", plantD: "#2F6B49", pot: "#8C5B4A", white: "#FFFFFF"
  };
  var PHASE = [C.slate, C.indigo, C.teal, C.amber];

  /* ---------------------------------------------------------------- colour, mixed
     Two helpers, so that a wall or a far roof can be said as "this much of that hue". */
  function rgb(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function hexOf(c) { var i, o = "#", v; for (i = 0; i < 3; i++) { v = Math.max(0, Math.min(255, Math.round(c[i]))).toString(16); o += v.length < 2 ? "0" + v : v; } return o; }
  function mix(a, b, k) { var x = rgb(a), y = rgb(b); return hexOf([x[0] + (y[0] - x[0]) * k, x[1] + (y[1] - x[1]) * k, x[2] + (y[2] - x[2]) * k]); }
  // keep a surface adult: cap its saturation and leave its lightness where it is
  function tame(h, cap) {
    var c = rgb(h), mx = Math.max(c[0], c[1], c[2]), mn = Math.min(c[0], c[1], c[2]), l = (mx + mn) / 2, sat = mx === mn ? 0 : (mx - mn) / (l > 127.5 ? 510 - mx - mn : mx + mn), k;
    if (sat <= cap) return h;
    k = cap / sat;
    return hexOf([l + (c[0] - l) * k, l + (c[1] - l) * k, l + (c[2] - l) * k]);
  }

  /* ---------------------------------------------------------------- the sky
     One still sky per phase. `top` is overhead and `low` is at the horizon; the rest says how the
     ground, the far roofs and the runway lights sit under it. Stars only when it is dark. */
  var SKIES = {
    dawn:      { top: "#3B4A6B", low: "#E3A587", cloud: "#C98F86", apron: "#262B38", line: "#4A5163", far: "#4A4F6B", lights: true },
    morning:   { top: "#6FA3CF", low: "#CFE3EE", cloud: "#EEF5FA", apron: "#4B525E", line: "#AEB6C2", far: "#8FAAC6", sun: [0.2, "#FBF1CF"] },
    afternoon: { top: "#4F8FC4", low: "#A9D0E6", cloud: "#E3EEF6", apron: "#474E5A", line: "#A6AEBB", far: "#7C9DBD", sun: [0.74, "#FFF6DA"] },
    golden:    { top: "#5B5F8F", low: "#F0B46A", cloud: "#E9A56B", apron: "#3A3945", line: "#6F6A74", far: "#6A5F82", lights: true },
    dusk:      { top: "#232848", low: "#B9743C", cloud: "#5B5280", apron: "#191C28", line: "#333848", far: "#262A45", lights: true, stars: 14 },
    night:     { top: C.sky0, low: C.sky2, apron: "#0D1016", line: "#2B3340", far: "#141925", lights: true, stars: 46, moon: true }
  };
  var now = SKIES.night;                    // the sky the rooms' windows look out on: set by whoever draws
  function skyOf(key) { return SKIES[key] || SKIES.night; }

  /* ---------------------------------------------------------------- sprites */
  function canvas(w, h) {
    var c = document.createElement("canvas");
    c.width = w; c.height = h;
    return c;
  }

  /* rows of characters -> an offscreen canvas, 1px larger on every side for the outline */
  function sprite(rows, legend, outline) {
    var h = rows.length, w = rows[0].length;
    var c = canvas(w + 2, h + 2), g = c.getContext("2d");
    var x, y, ch;
    if (outline !== false) {
      g.fillStyle = outline || C.out;
      for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
        if (rows[y].charAt(x) !== ".") g.fillRect(x, y, 3, 3);      // a 3x3 stamp per pixel grows it by one
      }
    }
    for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
      ch = rows[y].charAt(x);
      if (ch === ".") continue;
      g.fillStyle = legend[ch] || "#f0f";
      g.fillRect(x + 1, y + 1, 1, 1);
    }
    return { c: c, w: w + 2, h: h + 2 };
  }
  function blit(g, s, x, y, flip) {
    if (!flip) { g.drawImage(s.c, x - 1, y - 1); return; }
    g.save(); g.translate(x + s.w - 1, y - 1); g.scale(-1, 1); g.drawImage(s.c, 0, 0); g.restore();
  }

  /* ---------------------------------------------------------------- lettering
     A 3 x 5 alphabet for room signs and the day board only. Anything a player has to read is real
     text in the page, never this. */
  var GLYPH = {
    A: "010101111101101", B: "110101110101110", C: "011100100100011", D: "110101101101110", E: "111100110100111",
    F: "111100110100100", G: "011100101101011", H: "101101111101101", I: "111010010010111", J: "001001001101010",
    K: "101101110101101", L: "100100100100111", M: "101111111101101", N: "110101101101101", O: "010101101101010",
    P: "110101110100100", Q: "010101101110011", R: "110101110101101", S: "011100010001110", T: "111010010010010",
    U: "101101101101111", V: "101101101101010", W: "101101111111101", X: "101101010101101", Y: "101101010010010",
    Z: "111001010100111", "0": "111101101101111", "1": "010110010010111", "2": "110001010100111", "3": "110001010001110",
    "4": "101101111001001", "5": "111100110001110", "6": "011100111101111", "7": "111001010010010", "8": "111101111101111",
    "9": "111101111001110", ".": "000000000000010", ":": "000010000010000", "-": "000000111000000", "$": "011110010011110",
    "%": "101001010100101", " ": "000000000000000", "/": "001001010100100", "+": "000010111010000"
  };
  function text(g, str, x, y, col) {
    var i, j, gl, cx = x;
    g.fillStyle = col;
    str = String(str).toUpperCase();
    for (i = 0; i < str.length; i++) {
      gl = GLYPH[str.charAt(i)] || GLYPH[" "];
      for (j = 0; j < 15; j++) if (gl.charAt(j) === "1") g.fillRect(cx + (j % 3), y + ((j / 3) | 0), 1, 1);
      cx += 4;
    }
    return cx - x - 1;
  }
  function sign(g, str, x, y, lit) {                 // a small plate on a wall
    var w = String(str).length * 4 + 3;
    g.fillStyle = C.out; g.fillRect(x, y, w, 9);
    text(g, str, x + 2, y + 2, lit ? C.soft : C.trim);
    return w;
  }

  /* ---------------------------------------------------------------- people */
  // One adult body, 10 x 22, about four heads tall. h hair, s skin, t top, T top in shade, c collar,
  // p trousers, P trousers in shade, b shoe. No face at this size: a person is told by hair, build
  // and the colour they wear. The head is rows 0 to 5 and is swapped for the hair style.
  var HEADS = {
    short: ["...hhhh...",
            "..hhhhhh..",
            "..hssssh..",
            "..ssssss..",
            "..ssssss..",
            "...ssss..."],
    long:  ["...hhhh...",
            "..hhhhhh..",
            "..hssssh..",
            ".hhsssshh.",
            ".hhsssshh.",
            ".hh.ss.hh."],
    bun:   ["....hh.hh.",
            "..hhhhhhh.",
            "..hssssh..",
            "..ssssss..",
            "..ssssss..",
            "...ssss..."],
    bald:  ["...ssss...",
            "..ssssss..",
            "..ssssss..",
            "..ssssss..",
            "..shhhhs..",
            "...hhhh..."],                                             // a beard
    crop:  ["...hhhh...",
            "..hhhhhh..",
            "..ssssss..",
            "..ssssss..",
            "..ssssss..",
            "...ssss..."]
  };
  // j jacket, J jacket in shade, t shirt, c lanyard or tie. Hands are skin.
  var BODY = ["....ss....",
              "..jjttjJ..",
              ".jjjtcjJJ.",
              ".jjjtcjJJ.",
              ".jjjttjJJ.",
              ".sjjjjJJs.",
              ".sjjjjJJs.",
              "..jjjjJJ..",
              "..ppppPP..",
              "..ppppPP.."];
  var LEGS = [["..pp..PP..", "..pp..PP..", "..pp..PP..", "..pp..PP..", "..pp..PP..", "..bb..bb.."],     // standing
              ["..pp..PP..", "..pp..PP..", "..pp...PP.", ".pp....PP.", ".pp....PP.", ".bb....bb."],     // a step
              ["..pp..PP..", "..pp..PP..", "..pp.PP...", "..pp.PP...", "..pp.PP...", "..bb.bb..."]];    // the other step
  var SEAT = ["..ppppPPP.", "..ppppppPP", "......ppPP", "......ppPP", "......bbbb"];                     // sitting, facing right

  function person(look) {
    var legend = { h: look.hair, s: look.skin, j: look.top, J: look.topD, t: look.shirt || C.paper, c: look.collar || look.shirt || C.paper,
                   p: look.legs || "#343B4B", P: look.legsD || "#262B38", b: look.shoe || "#101216" };
    var head = HEADS[look.style || "short"];
    function frame(legs, bob) {
      var rows = head.concat(BODY, LEGS[legs]);
      // a breath: the head and shoulders sink a pixel into the body
      if (bob) rows = [".........."].concat(head, BODY.slice(0, 9), LEGS[legs]);
      return sprite(rows, legend, false);
    }
    return { idle: [frame(0, false), frame(0, true)], walk: [frame(1, false), frame(0, false), frame(2, false), frame(0, false)],
             sit: sprite(head.concat(BODY.slice(0, 8), SEAT), legend, false), look: look };
  }
  var PH = 22;                              // how tall a person is

  var SKIN = ["#F1C7A5", "#DDA57B", "#B9805A", "#8C5A3C"];
  // A jacket in the muted hue of the role, a light shirt, and the role's own accent on the lanyard.
  var CAST = {
    priya:  { name: "Priya",  role: "pm",  title: "Product manager",    skin: SKIN[2], hair: "#1B1A22", style: "long",  top: "#4C6478", topD: "#3B4F60", collar: C.slate },
    arjun:  { name: "Arjun",  role: "sa",  title: "Solution architect", skin: SKIN[2], hair: "#1B1A22", style: "bald",  top: "#7A6032", topD: "#5F4A26", collar: C.amber },
    sam:    { name: "Sam",    role: "eng", title: "Engineering lead",   skin: SKIN[0], hair: "#6B4630", style: "crop",  top: "#3F7355", topD: "#305943", shirt: "#C9D3C8", collar: C.green },
    maya:   { name: "Maya",   role: "qa",  title: "QA lead",            skin: SKIN[3], hair: "#1B1A22", style: "bun",   top: "#665490", topD: "#4F4170", collar: C.violet },
    lena:   { name: "Lena",   role: "ops", title: "Platform lead",      skin: SKIN[1], hair: "#C9B28A", style: "short", top: "#3A7690", topD: "#2C5C71", collar: C.sky },
    sponsor:{ name: "Ines",   role: "exec", title: "Sponsor",           skin: SKIN[1], hair: "#8A8F99", style: "short", top: "#2E3442", topD: "#232833", collar: C.rose },
    ops:    { name: "Operations lead",     skin: SKIN[0], hair: "#3B2A20", style: "crop",  top: "#4A5262", topD: "#3A4150", collar: "#8C97A6" },
    centre: { name: "Contact-centre head", skin: SKIN[3], hair: "#1B1A22", style: "long",  top: "#6B4F5D", topD: "#533D48", collar: "#C98CA0" },
    legal:  { name: "Compliance officer",  skin: SKIN[1], hair: "#2A2320", style: "bun",   top: "#3D4452", topD: "#2F3541", collar: C.rose },
    finance:{ name: "Finance controller",  skin: SKIN[0], hair: "#8A8F99", style: "bald",  top: "#36413B", topD: "#29322D", collar: C.amber },
    agent:  { name: "Frontline agent",     skin: SKIN[2], hair: "#5A3A28", style: "short", top: "#4E5D7A", topD: "#3C4860", shirt: "#B9C4DC" },
    agent2: { name: "Frontline agent",     skin: SKIN[0], hair: "#1B1A22", style: "bun",   top: "#4E5D7A", topD: "#3C4860", shirt: "#B9C4DC" }
  };
  var people = null;
  function cast() {
    if (people) return people;
    people = {};
    Object.keys(CAST).forEach(function (k) { people[k] = person(CAST[k]); });
    return people;
  }

  /* ---------------------------------------------------------------- props */
  function R(g, x, y, w, h, col) { g.fillStyle = col; g.fillRect(x, y, w, h); }

  function desk(g, x, y, w) {                       // y is the floor line
    R(g, x, y - 9, w, 2, C.deskL); R(g, x, y - 7, w, 1, C.deskD);
    R(g, x + 1, y - 6, 1, 6, C.desk); R(g, x + w - 2, y - 6, 1, 6, C.desk);
  }
  function monitor(g, x, y, lit, hue, t) {          // y is the desk top
    R(g, x, y - 8, 9, 7, C.metalD); R(g, x + 1, y - 7, 7, 5, lit ? C.screenL : C.screen);
    R(g, x + 4, y - 1, 1, 1, C.metalD);
    if (lit) {
      var k = (t >> 4) % 3;
      R(g, x + 2, y - 6, 3 + k, 1, hue); R(g, x + 2, y - 4, 5 - k, 1, C.soft); R(g, x + 2, y - 3, 2 + k, 1, hue);
    }
  }
  function plant(g, x, y) {
    R(g, x + 1, y - 4, 4, 4, C.pot); R(g, x, y - 5, 6, 1, C.pot);
    R(g, x + 2, y - 11, 2, 6, C.plantD); R(g, x, y - 9, 2, 3, C.plant); R(g, x + 4, y - 10, 2, 3, C.plant); R(g, x + 1, y - 12, 2, 2, C.plant);
  }
  function lampOn(g, x, y, w, floorY, lit) {        // a ceiling light and the cone under it
    R(g, x - 3, y, 7, 1, C.metalD); R(g, x - 2, y + 1, 5, 1, lit ? C.lamp : C.metalD);
    if (!lit) return;
    g.save(); g.globalAlpha = 0.075;
    g.fillStyle = C.lamp;
    g.beginPath(); g.moveTo(x - 2, y + 2); g.lineTo(x + 3, y + 2); g.lineTo(x + w, floorY); g.lineTo(x - w, floorY); g.closePath(); g.fill();
    g.restore();
  }
  // A window: the day's sky in three bands, the far roofs along its sill, and one mullion per pane.
  function windowAt(g, x, y, w, h, panes) {
    var i, third = Math.ceil(h / 3), n = panes || 2;
    R(g, x - 1, y - 1, w + 2, h + 2, C.trim);
    R(g, x, y, w, h, mix(now.top, now.low, 0.3)); R(g, x, y + third, w, h - third, mix(now.top, now.low, 0.6)); R(g, x, y + 2 * third, w, h - 2 * third, mix(now.top, now.low, 0.9));
    if (now.stars) { R(g, x + 2, y + 2, 1, 1, C.star); R(g, x + w - 4, y + 4, 1, 1, C.star); R(g, x + (w >> 1) + 2, y + 1, 1, 1, C.star); }
    for (i = 0; i < w; i += 5) R(g, x + i, y + h - 2 - ((i * 7) % 3), Math.min(4, w - i), 2 + ((i * 7) % 3), now.far);
    for (i = 1; i < n; i++) R(g, x + Math.round(i * w / n), y, 1, h, C.trim);
    R(g, x - 1, y + h, w + 2, 1, C.metalL);                              // the sill catches the light
  }
  function chair(g, x, y) { R(g, x, y - 9, 1, 9, C.metalD); R(g, x, y - 5, 5, 1, C.metal); R(g, x + 4, y - 4, 1, 4, C.metalD); }

  /* ---------------------------------------------------------------- rooms
     Every room is W x H with the floor at H - 4. `st` is what the game knows: the room draws from it,
     so the picture changes as the ninety days go by. */
  var W = 144, H = 52, FLOOR = H - 4;

  // Whose room it is shows on the walls: about a third of the owner's jacket mixed into the wall, kept
  // under a quarter saturation so it stays a wall. The boardroom is walnut. The contact centre and the
  // lobby belong to nobody on the team, and stay grey.
  var OWNER = { product: "priya", arch: "arjun", eng: "sam", qa: "maya", platform: "lena" }, paints = {};
  function paint(id) {
    if (paints[id]) return paints[id];
    var o = OWNER[id], p = { wall: C.wall, wallD: C.wallD, wallL: C.wallL, floor: C.floor, floorL: C.floorL, hue: "#6E7686" };
    if (id === "board") p = { wall: "#3A2F2A", wallD: "#2B2320", wallL: "#4B3E37", floor: "#57483F", floorL: "#6F5D51", hue: "#8A6A58" };
    else if (o) p = { wall: tame(mix(C.wall, CAST[o].top, 0.3), 0.24), wallD: tame(mix(C.wallD, CAST[o].topD, 0.3), 0.24), wallL: tame(mix(C.wallL, CAST[o].top, 0.3), 0.24),
                      floor: tame(mix(C.floor, CAST[o].top, 0.18), 0.2), floorL: tame(mix(C.floorL, CAST[o].top, 0.18), 0.2), hue: CAST[o].top };
    return (paints[id] = p);
  }
  function shell(g, lit, id) {
    var p = paint(id);
    R(g, 0, 0, W, H, lit ? p.wall : C.dim);
    if (lit) { R(g, 0, 0, W, 3, p.wallD); R(g, 0, 30, W, 1, p.wallL); R(g, 0, 31, W, FLOOR - 31, p.wallD); }
    R(g, 0, FLOOR, W, 1, lit ? p.floorL : C.wallD); R(g, 0, FLOOR + 1, W, 3, lit ? p.floor : C.out);
  }

  var ROOMS = {
    board: function (g, lit, t, st) {                 // the boardroom: a long table, a wall screen, the sky outside
      shell(g, lit, "board");
      lampOn(g, 72, 3, 44, FLOOR, lit);
      windowAt(g, 6, 8, 30, 20, 3);
      R(g, 50, 7, 46, 22, C.metalD); R(g, 51, 8, 44, 20, lit ? C.screenL : C.screen);
      if (lit) {                                        // value beside cost, as far as the team has got
        var v = Math.round(14 * (st.value || 0)), c = Math.round(14 * (st.cost || 0));
        R(g, 60, 26 - v, 8, v, C.teal); R(g, 76, 26 - c, 8, c, C.amber); R(g, 56, 26, 34, 1, C.soft);
      }
      R(g, 34, FLOOR - 10, 76, 3, C.deskL); R(g, 34, FLOOR - 7, 76, 1, C.deskD); R(g, 44, FLOOR - 6, 2, 6, C.desk); R(g, 98, FLOOR - 6, 2, 6, C.desk);
      chair(g, 24, FLOOR); chair(g, 114, FLOOR);
      plant(g, 132, FLOOR);
    },
    product: function (g, lit, t, st) {               // product: a wall of notes that fills as requirements land
      shell(g, lit, "product");
      lampOn(g, 40, 3, 34, FLOOR, lit); lampOn(g, 100, 3, 30, FLOOR, lit);
      R(g, 8, 7, 54, 22, lit ? paint("product").wallL : C.wallD);
      var n = Math.min(24, st.notes || 0), i, hues = [C.amber, C.slate, C.sky, C.teal];
      for (i = 0; i < n; i++) R(g, 11 + (i % 8) * 6, 10 + ((i / 8) | 0) * 6, 4, 4, lit ? hues[i % 4] : C.trim);
      desk(g, 78, FLOOR, 34); monitor(g, 82, FLOOR - 9, lit, C.slate, t); monitor(g, 96, FLOOR - 9, lit, C.amber, t + 20);
      chair(g, 116, FLOOR);
      plant(g, 68, FLOOR); windowAt(g, 122, 8, 16, 20, 2);
    },
    arch: function (g, lit, t, st) {                  // architecture: a whiteboard that gains boxes and lines
      shell(g, lit, "arch");
      windowAt(g, 113, 8, 24, 17, 2);
      lampOn(g, 40, 3, 36, FLOOR, lit); lampOn(g, 118, 3, 24, FLOOR, lit);
      R(g, 10, 6, 62, 24, C.metalD); R(g, 11, 7, 60, 22, lit ? "#DDDAD0" : C.trim);
      if (lit) {
        var b = Math.min(5, st.boxes || 0), k, bx = [16, 34, 52, 25, 44], by = [10, 10, 10, 20, 20];
        for (k = 0; k < b; k++) { R(g, bx[k], by[k], 12, 6, PHASE[k % 4]); if (k) R(g, bx[k - 1] + 12, by[k - 1] + 3, bx[k] - bx[k - 1] - 12 > 0 ? bx[k] - bx[k - 1] - 12 : 1, 1, C.metalD); }
      }
      R(g, 84, 10, 22, 2, C.desk); R(g, 84, 18, 22, 2, C.desk); R(g, 84, 26, 22, 2, C.desk);         // shelves
      var s; for (s = 0; s < 6; s++) { R(g, 86 + s * 3, 5, 2, 5, [C.violet, C.slate, C.amber][s % 3]); R(g, 86 + s * 3, 13, 2, 5, [C.teal, C.paper, C.indigo][s % 3]); }
      desk(g, 112, FLOOR, 26); monitor(g, 120, FLOOR - 9, lit, C.amber, t);
    },
    eng: function (g, lit, t, st) {                   // engineering: three desks and a build wall
      shell(g, lit, "eng");
      windowAt(g, 8, 8, 34, 17, 3); windowAt(g, 50, 8, 34, 17, 3);
      lampOn(g, 30, 3, 30, FLOOR, lit); lampOn(g, 86, 3, 30, FLOOR, lit);
      R(g, 94, 6, 42, 22, C.metalD); R(g, 95, 7, 40, 20, lit ? C.screenL : C.screen);
      if (lit) {
        var d = st.bolts || 0, i;
        for (i = 0; i < 14; i++) R(g, 98 + (i % 7) * 5, 10 + ((i / 7) | 0) * 7, 4, 5, i < d ? C.green : (i === d && (t >> 5) % 2 ? C.amber : C.metalD));
      }
      var x; for (x = 0; x < 3; x++) { desk(g, 6 + x * 29, FLOOR, 25); monitor(g, 8 + x * 29, FLOOR - 9, lit, C.teal, t + x * 9); monitor(g, 19 + x * 29, FLOOR - 9, lit, C.green, t + x * 13 + 5); }
    },
    qa: function (g, lit, t, st) {                    // QA: the score against the bar, with its margin
      shell(g, lit, "qa");
      windowAt(g, 84, 8, 50, 17, 4);
      lampOn(g, 40, 3, 34, FLOOR, lit); lampOn(g, 108, 3, 30, FLOOR, lit);
      R(g, 8, 6, 64, 24, C.metalD); R(g, 9, 7, 62, 22, lit ? C.screenL : C.screen);
      if (lit) {
        R(g, 12, 25, 56, 1, C.soft);
        var score = st.score || 0, lo = st.lower || 0, bar = st.bar || 0;
        if (bar) R(g, 12 + Math.round(bar * 56), 9, 1, 17, C.rose);
        if (score) { R(g, 12, 13, Math.round(score * 56), 5, C.teal); if (lo) R(g, 12 + Math.round(lo * 56), 12, Math.round((score - lo) * 112) || 1, 1, C.paper); }
        var j; for (j = 0; j < 6; j++) R(g, 14 + j * 9, 21, 7, 3, j < (st.slices || 0) ? C.green : C.metalD);
      }
      desk(g, 82, FLOOR, 26); monitor(g, 84, FLOOR - 9, lit, C.violet, t); monitor(g, 96, FLOOR - 9, lit, C.teal, t + 11);
      desk(g, 114, FLOOR, 24); monitor(g, 120, FLOOR - 9, lit, C.violet, t + 7);
    },
    platform: function (g, lit, t, st) {              // platform: racks, and the bill on the wall
      shell(g, lit, "platform");
      lampOn(g, 40, 3, 34, FLOOR, lit); lampOn(g, 112, 3, 28, FLOOR, lit);
      var r, l;
      for (r = 0; r < 4; r++) {
        R(g, 6 + r * 17, 8, 14, FLOOR - 8, C.metalD); R(g, 7 + r * 17, 9, 12, FLOOR - 10, C.out);
        for (l = 0; l < 8; l++) R(g, 8 + r * 17 + ((l * 5 + r * 3) % 9), 11 + l * 4, 1, 1, lit ? (((t >> 3) + l * 3 + r * 5) % 7 === 0 ? C.amber : C.green) : C.metalD);
      }
      R(g, 80, 6, 56, 24, C.metalD); R(g, 81, 7, 54, 22, lit ? C.screenL : C.screen);
      if (lit) {
        R(g, 84, 26, 48, 1, C.soft);
        var bill = st.bill || 1, n, hgt;
        for (n = 0; n < 8; n++) { hgt = Math.min(17, Math.round(3 + (bill - 1) * 4 * (n / 7) * (n / 7) + n * 0.3)); R(g, 85 + n * 6, 26 - hgt, 4, hgt, hgt > 9 ? "#E2824A" : C.amber); }
      }
      desk(g, 100, FLOOR, 30); monitor(g, 106, FLOOR - 9, lit, C.sky, t);
    },
    centre: function (g, lit, t, st) {                // the contact centre: the departures board, and the people it is for
      shell(g, lit, "centre");
      windowAt(g, 78, 8, 58, 17, 4);
      lampOn(g, 36, 3, 32, FLOOR, lit); lampOn(g, 108, 3, 34, FLOOR, lit);
      R(g, 6, 5, 60, 25, C.metalD); R(g, 7, 6, 58, 23, C.out);
      var row, bad = st.cancelled == null ? 3 : st.cancelled;
      for (row = 0; row < 5; row++) {
        R(g, 9, 8 + row * 4, 12, 2, lit ? C.paper : C.trim); R(g, 23, 8 + row * 4, 20, 2, lit ? C.soft : C.trim);
        R(g, 46, 8 + row * 4, 16, 2, lit ? (row < bad ? C.amber : C.green) : C.trim);
      }
      var x; for (x = 0; x < 3; x++) { desk(g, 76 + x * 22, FLOOR, 18); monitor(g, 80 + x * 22, FLOOR - 9, lit, C.sky, t + x * 17); }
    }
  };

  /* ---------------------------------------------------------------- the building */
  // Seven rooms on four floors. The contact centre takes the whole ground floor width with the lobby.
  var WALL = 3, SLAB = 9, ROOF = 38;       // SLAB: the band over each floor, where the room's name is written
  var PLAN = [
    { id: "board",    col: 0, floor: 0, name: "Boardroom" },
    { id: "product",  col: 1, floor: 0, name: "Product" },
    { id: "arch",     col: 0, floor: 1, name: "Architecture" },
    { id: "eng",      col: 1, floor: 1, name: "Engineering" },
    { id: "qa",       col: 0, floor: 2, name: "QA" },
    { id: "platform", col: 1, floor: 2, name: "Platform" },
    { id: "centre",   col: 0, floor: 3, name: "Contact centre" }
  ];
  var BW = WALL + (W + WALL) * 2, BH = ROOF + (H + SLAB) * 4 + 6;
  function roomRect(id) {
    var i, p;
    for (i = 0; i < PLAN.length; i++) if (PLAN[i].id === id) p = PLAN[i];
    return { x: WALL + p.col * (W + WALL), y: ROOF + SLAB + p.floor * (H + SLAB), w: W, h: H };
  }

  function lobby(g, lit, t, st) {                    // the right half of the ground floor: the way in, and the day
    R(g, 0, 0, W, H, lit ? C.wall : C.dim); R(g, 0, 0, W, 3, C.wallD); R(g, 0, FLOOR, W, 1, lit ? C.floorL : C.wallD); R(g, 0, FLOOR + 1, W, 3, lit ? C.floor : C.out);
    lampOn(g, 40, 3, 30, FLOOR, lit); lampOn(g, 110, 3, 24, FLOOR, lit);
    // the day board: the only place the canvas spells anything out
    R(g, 10, 8, 62, 21, C.metalD); R(g, 11, 9, 60, 19, C.out);
    // The digits and each of the thirteen days wear their phase's hue: full once played, a white core
    // on today, turned down while still to come. A rose pixel sits under a day that has something due.
    var i, n = st.dayIndex || 0, ph = st.phases || [], hue, dx, dy;
    text(g, "DAY", 15, 12, C.soft); text(g, String(st.day || 1), 31, 12, PHASE[ph[n] || 0]);
    text(g, "OF 90", 15, 20, C.trim);
    for (i = 0; i < 13; i++) {
      hue = PHASE[ph[i] || 0]; dx = 44 + (i % 7) * 4; dy = 12 + ((i / 7) | 0) * 4;
      R(g, dx, dy, 3, 3, i <= n ? hue : mix(C.metalD, hue, 0.3));
      if (i === n) R(g, dx + 1, dy + 1, 1, 1, C.white);
      if (st.owed && st.owed[i]) R(g, dx + 1, dy + 3, 1, 1, C.rose);
    }
    // reception
    R(g, 80, FLOOR - 9, 22, 9, C.deskD); R(g, 79, FLOOR - 10, 24, 2, C.deskL);
    // the doors, and the day through them
    R(g, 112, 12, 26, FLOOR - 12, C.trim); R(g, 113, 13, 11, FLOOR - 13, mix(now.top, now.low, 0.35)); R(g, 126, 13, 11, FLOOR - 13, mix(now.top, now.low, 0.35));
    R(g, 113, 26, 11, FLOOR - 26, mix(now.top, now.low, 0.75)); R(g, 126, 26, 11, FLOOR - 26, mix(now.top, now.low, 0.75));
    R(g, 113, FLOOR - 6, 11, 6, now.far); R(g, 126, FLOOR - 4, 11, 4, now.far);
    R(g, 122, 28, 1, 4, C.metalL); R(g, 127, 28, 1, 4, C.metalL);
    plant(g, 104, FLOOR);
  }

  // Where people stand in each room, left to right, clear of the furniture.
  var SPOTS = {
    board: [40, 56, 72, 88, 104, 22, 120], product: [64, 50, 36, 118], arch: [76, 62, 48, 98], eng: [94, 108, 122, 80],
    qa: [72, 58, 44, 110], platform: [84, 70, 56, 134], centre: [40, 54, 26, 66]
  };
  var off = null;
  function scratch() { if (!off) off = canvas(W, H); return off; }

  // One room with the people in it, drawn at the origin of `g`. `who` is a list of cast keys; the first
  // is the one speaking, and breathes. Frontline agents sit at their desks.
  function room(g, id, t, st, lit, who, speaking, enter) {
    var P = cast(), spots = SPOTS[id] || [40, 60, 80, 100], i, k, sp, x, n = 0, p;
    if (enter == null) enter = 1;
    now = skyOf(st && st.sky);
    var gap = Math.min(0.1, 0.45 / Math.max(1, who ? who.length : 1));     // so the last one in still arrives
    if (id === "lobby") lobby(g, lit, t, st); else ROOMS[id](g, lit, t, st);
    for (i = 0; who && i < who.length; i++) {
      k = who[i]; if (!P[k]) continue;
      if (id === "centre" && (k === "agent" || k === "agent2")) { sp = P[k].sit; x = k === "agent" ? 80 : 102; g.drawImage(sp.c, x - 1, FLOOR - sp.h + 2); continue; }
      x = spots[n % spots.length];
      // arriving: each person walks in from the left, one after another, and stops on their mark
      p = Math.max(0, Math.min(1, (enter - n * gap) / 0.55)); n++;
      if (p < 1) { sp = P[k].walk[(t >> 3) & 3]; blit(g, sp, Math.round(-12 + (x + 12) * p), FLOOR - sp.h + 2, false); continue; }
      sp = P[k].idle[k === speaking && ((t >> 5) & 1) ? 1 : 0];
      blit(g, sp, x, FLOOR - sp.h + 2, x > 72);
    }
  }

  // The whole building. `view.active` is the lit room, `view.cast` maps a room to the people in it,
  // `view.speaking` is who is talking. Rooms that are not today's are drawn and then turned down.
  function building(g, ox, oy, t, st, view) {
    view = view || {};
    var i, p, r, o = scratch(), og = o.getContext("2d"), on;
    R(g, ox, oy + ROOF, BW, BH - ROOF - 6, C.out);
    R(g, ox - 2, oy + BH - 6, BW + 4, 6, C.metalD); R(g, ox - 2, oy + BH - 6, BW + 4, 1, C.metal);
    // the roof: plant, a mast, the beacon
    R(g, ox + 8, oy + ROOF - 9, 26, 6, C.metalD); R(g, ox + 12, oy + ROOF - 12, 6, 3, C.metal);
    R(g, ox + BW - 40, oy + ROOF - 20, 1, 17, C.metal); R(g, ox + BW - 44, oy + ROOF - 15, 9, 1, C.metal);
    R(g, ox + BW - 41, oy + ROOF - 22, 3, 2, (t >> 5) % 2 ? "#E8734A" : "#6E3F30");
    var plan = PLAN.concat([{ id: "lobby", col: 1, floor: 3, name: "Lobby" }]);
    for (i = 0; i < plan.length; i++) {
      p = plan[i];
      r = { x: WALL + p.col * (W + WALL), y: ROOF + SLAB + p.floor * (H + SLAB) };
      on = !view.active || view.active === p.id || p.id === "lobby";
      og.clearRect(0, 0, W, H);
      room(og, p.id, t, st, true, view.cast && view.cast[p.id], on ? view.speaking : null, view.active === p.id ? view.enter : 1);
      g.drawImage(o, ox + r.x, oy + r.y);
      if (!on) { g.fillStyle = "rgba(9,11,16,.5)"; g.fillRect(ox + r.x, oy + r.y, W, H); }
      if (view.shut && view.shut[p.id] > 0) shutter(g, ox + r.x, oy + r.y, view.shut[p.id]);
      text(g, p.name, ox + r.x + 2, oy + r.y - 7, on ? C.ink : C.trim);
      if (view.mark && view.mark[p.id]) R(g, ox + r.x + W - 6, oy + r.y - 7, 4, 4, view.mark[p.id]);
    }
  }
  // A room nobody may work in yet: a roller shutter with a rose edge. `p` is how far down it is, 1 to 0.
  function shutter(g, x, y, p) {
    var h = Math.round(H * p), i;
    R(g, x, y, W, h, "#12151B");
    for (i = 2; i < h - 2; i += 4) R(g, x, y + i, W, 1, "#1D222B");
    if (h > 3) { R(g, x, y + h - 2, W, 2, C.rose); R(g, x + (W >> 1) - 3, y + h - 5, 6, 3, C.metal); }
  }

  function roomAt(x, y) {                           // which room a point of the building falls in
    var plan = PLAN.concat([{ id: "lobby", col: 1, floor: 3 }]), i, p, rx, ry;
    for (i = 0; i < plan.length; i++) {
      p = plan[i]; rx = WALL + p.col * (W + WALL); ry = ROOF + SLAB + p.floor * (H + SLAB);
      if (x >= rx && x < rx + W && y >= ry - SLAB && y < ry + H) return p.id;
    }
    return null;
  }

  /* ---------------------------------------------------------------- portraits
     A face for the dialogue, 24 x 24: enough to tell who is speaking, plain enough to stay adult. */
  var faces = {};
  function portrait(key) {
    if (faces[key]) return faces[key];
    var L = CAST[key], c = canvas(24, 24), g = c.getContext("2d"), hair = L.hair, st = L.style || "short";
    R(g, 0, 0, 24, 24, C.wallD); R(g, 0, 23, 24, 1, L.collar || C.trim);
    R(g, 3, 19, 18, 5, L.top); R(g, 14, 19, 7, 5, L.topD); R(g, 10, 19, 4, 5, L.shirt || C.paper); R(g, 11, 20, 2, 4, L.collar || C.paper);
    R(g, 10, 16, 4, 3, L.skin);                                              // neck
    R(g, 7, 5, 10, 12, L.skin); R(g, 6, 7, 12, 8, L.skin);                   // head
    R(g, 9, 10, 2, 2, C.out); R(g, 13, 10, 2, 2, C.out);                     // eyes
    R(g, 10, 14, 4, 1, "#7A4B3A");                                           // mouth
    if (st === "short") { R(g, 7, 3, 10, 3, hair); R(g, 6, 5, 2, 4, hair); R(g, 16, 5, 2, 4, hair); }
    else if (st === "crop") { R(g, 7, 4, 10, 2, hair); R(g, 6, 5, 1, 3, hair); R(g, 17, 5, 1, 3, hair); }
    else if (st === "long") { R(g, 7, 3, 10, 3, hair); R(g, 5, 5, 2, 13, hair); R(g, 17, 5, 2, 13, hair); R(g, 6, 5, 2, 3, hair); R(g, 16, 5, 2, 3, hair); }
    else if (st === "bun") { R(g, 7, 3, 10, 3, hair); R(g, 6, 5, 2, 3, hair); R(g, 16, 5, 2, 3, hair); R(g, 15, 0, 5, 4, hair); }
    else if (st === "bald") { R(g, 7, 14, 10, 3, hair); R(g, 6, 12, 2, 4, hair); R(g, 16, 12, 2, 4, hair); R(g, 10, 14, 4, 1, "#C9A090"); }
    faces[key] = c;
    return c;
  }

  /* ---------------------------------------------------------------- the sky, and the plane */
  // Side on, nose to the right, and it only ever flies to the right. T tail fin, F fuselage, D belly,
  // w cabin windows, C cockpit glass, W wing (swept back, so it trails toward the tail), E engine.
  var PLANE = sprite([
    ".TT...........................................",
    ".TTT..........................................",
    ".TTTT.........................................",
    "..TTTT........................................",
    "..FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF.....",
    ".FFFFwFwFwFwFwFwFwFwFwFwFwFwFwFwFwFwFFFCCFF...",
    "HFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF.",
    ".FFFFFFFFFFFFFFFFWWWWWWWWWFFFFFFFFFFFFFFFFFF..",
    "..DDDDDDDDDDDDDDWWWWWWWWWWDDDDDDDDDDDDDDDD....",
    "...............WWWWWWWWW......................",
    "..............WWWWWWW.EEE.....................",
    ".............WWWWW...EEEEE....................",
    "............WWW.......EEE....................."],
    { T: C.indigo, F: "#D7DEE8", D: "#9AA6B8", w: C.sky2, C: C.sky, W: "#B4BFCE", E: "#7C879C", H: "#B4BFCE" }, false);

  // What is outside: the apron in front of the building and its runway lights. The far roofs are in the windows.
  function ground(g, w, h, gy, t, key) {
    var k = skyOf(key), x;
    R(g, 0, gy, w, h - gy, k.apron); R(g, 0, gy, w, 1, mix(k.apron, k.low, 0.25));
    for (x = 6; x < w; x += 14) R(g, x, gy + 5, 5, 1, k.line);                              // the centre line
    // edge lights: lit and chasing when the sky is low, plain markers in daylight
    for (x = 2; x < w; x += 9) R(g, x, gy + 2, 1, 1, k.lights ? (((x + (t >> 4)) % 27) < 9 ? C.amber : "#5C4A25") : mix(k.apron, "#FFFFFF", 0.25));
  }

  // The sky in flat bands, thin at the top where it shows above the roof and broad behind the building.
  // One still sky per phase: nothing in it moves but the stars' slow blink at night.
  var BANDS = [0, 0.03, 0.06, 0.1, 0.16, 0.3, 0.5, 0.75, 1];
  function cloud(g, x, y, w, col) { R(g, x + 2, y, w - 5, 1, col); R(g, x, y + 1, w, 2, col); R(g, x + 3, y + 3, w - 7, 1, col); }
  function sky(g, w, h, t, key) {
    var k = skyOf(key), i, x, y;
    for (i = 0; i < BANDS.length - 1; i++) R(g, 0, Math.round(BANDS[i] * h), w, Math.round(BANDS[i + 1] * h) - Math.round(BANDS[i] * h), mix(k.top, k.low, i / (BANDS.length - 2)));
    if (k.stars) for (i = 0; i < k.stars; i++) { x = (i * 97 + 13) % w; y = (i * 53 + 7) % Math.max(1, (h * (k.moon ? 0.7 : 0.09)) | 0); R(g, x, y, 1, 1, (i + (t >> 6)) % 9 === 0 ? mix(k.top, C.star, 0.3) : (i % 5 ? mix(k.top, C.star, 0.45) : C.star)); }
    if (k.sun) { x = Math.round(k.sun[0] * w); R(g, x + 1, 5, 5, 7, k.sun[1]); R(g, x, 6, 7, 5, k.sun[1]); }
    if (k.moon) { x = Math.round(0.14 * w); R(g, x + 1, 6, 4, 6, C.star); R(g, x, 7, 6, 4, C.star); R(g, x + 3, 6, 3, 4, k.top); R(g, x + 4, 7, 3, 4, k.top); }
    if (k.cloud) { cloud(g, Math.round(0.42 * w), 9, 26, k.cloud); cloud(g, Math.round(0.6 * w), 20, 18, mix(k.cloud, k.low, 0.4)); cloud(g, Math.round(0.03 * w), 24, 20, mix(k.cloud, k.top, 0.3)); }
  }

  root.NDArt = { PH: PH, text: text, sign: sign, C: C, PHASE: PHASE, sprite: sprite, blit: blit, cast: cast, CAST: CAST, ROOMS: ROOMS, PLAN: PLAN,
                 W: W, H: H, FLOOR: FLOOR, BW: BW, BH: BH, paint: paint, mix: mix, SKIES: SKIES, roomRect: roomRect, roomAt: roomAt, room: room, portrait: portrait, building: building, sky: sky, ground: ground, PLANE: PLANE, canvas: canvas };
})(typeof window !== "undefined" ? window : this);
