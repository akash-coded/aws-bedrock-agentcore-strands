"""Hand-drawn explainer sketches, drawn in code.

The lessons carry flow maps and boards: exact pictures of a process. A sketch is the other kind of
picture: one metaphor, a small deadpan worker doing the thing the paragraph just said, and a few words
in handwriting. The grammar is Ian's Xiaohei illustration style (MIT; see ``content/learn/sketches/README.md``
for the credit): black line on a sheet of paper, lots of empty paper, red for the point, orange for the
path, blue for the aside.

There is no image generator behind this, so the hand is simulated. Every stroke goes through
:meth:`Sk.stroke`, which bends a straight run a little and overshoots its ends. The wobble is seeded by
the sketch's name, so a build is repeatable and two sketches differ.

A sketch is a function that takes an :class:`Sk` and draws on a sheet 1200 units wide (600 high unless
it asks for another height)::

    def turnstile(s: Sk):
        s.ground(470)
        s.worker(420, 330, arms=[None, (560, 300)])
        s.note(820, 150, "one way", (700, 300), "point")

Four pens, named for their job: ``ink`` draws the scene, ``point`` (red) marks the thing that matters or
fails, ``path`` (orange) is the route or the flow, ``aside`` (blue) is a side note or the machine.
``faint`` is a pencil grey for hatching and far things.

The rules a sketch has to keep are checked in :func:`lint`: handwriting large enough to read on a phone,
six labels at most, five words a label, and a caption in real type under every one.
"""
from __future__ import annotations

import math
import random
import re
import zlib
from html import escape as _E

W = 1200
H = 600                       # the default sheet; a sketch may ask for 480 to 675
LABEL = 58                    # handwriting, in sheet units: 58 of 1200 is 14px in a phone's 288px column
LABEL_MIN = 54                # 13px on that phone, the floor
# Class names all begin with z, so nothing in the site's stylesheet can reach into a sketch by accident.
PEN = {"ink": "zk", "point": "zr", "path": "zo", "aside": "zb", "faint": "zg"}
_WIDTH = {"": "", "t": " zt", "h": " zh", "l": " zl"}     # thin, heavy, limb


def _fc(fill: str) -> str:
    """The class for a filled shape: ``p`` is paper (it covers what is behind it), else a pen."""
    return "zfp" if fill == "p" else "zf" + PEN[fill][1:]


def _seed(name: str) -> int:
    return zlib.crc32(name.encode("utf-8"))


class Sk:
    """One sheet. Drawing order is paint order: later things cover earlier ones."""

    def __init__(self, name: str, alt: str, h: int = H):
        self.name, self.alt, self.h = name, alt, h
        self.r = random.Random(_seed(name))
        self.out: list[str] = []
        self.an = 0                                  # annotations so far: the order they arrive in
        self.words: list[tuple[str, int]] = []       # every word written on the sheet, with its size

    # ------------------------------------------------------------------ the hand
    def _j(self, amp: float) -> float:
        return self.r.gauss(0, amp)

    def _wob(self, pts: list[tuple[float, float]], amp: float = 1.7, over: float = 3.0,
             closed: bool = False) -> list[tuple[float, float]]:
        """Resample a polyline every fifty units or so and nudge each sample sideways."""
        out: list[tuple[float, float]] = []
        m = len(pts)
        for i in range(m if closed else m - 1):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % m]
            d = math.hypot(x1 - x0, y1 - y0) or 1
            ux, uy = (x1 - x0) / d, (y1 - y0) / d
            steps = max(1, int(d / 52))
            for k in range(steps):
                t = k / steps
                off = self._j(amp * (0.5 if k == 0 else 1.0))
                out.append((x0 + (x1 - x0) * t - uy * off, y0 + (y1 - y0) * t + ux * off))
        if not closed:
            out.append((pts[-1][0] + self._j(amp * 0.5), pts[-1][1] + self._j(amp * 0.5)))
            if over and len(out) >= 2:               # a pen overshoots where it starts and stops
                for a, b in ((0, 1), (-1, -2)):
                    (ax, ay), (bx, by) = out[a], out[b]
                    d = math.hypot(bx - ax, by - ay) or 1
                    o = abs(self._j(over))
                    out[a] = (ax - (bx - ax) / d * o, ay - (by - ay) / d * o)
        return out

    @staticmethod
    def _smooth(pts: list[tuple[float, float]], closed: bool = False) -> str:
        """Catmull-Rom through the points, written as cubic beziers in whole units."""
        n = len(pts)
        if n < 3:
            return "M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in pts)

        def p(i: int) -> tuple[float, float]:
            return pts[i % n] if closed else pts[max(0, min(n - 1, i))]

        d = [f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"]
        for i in range(n if closed else n - 1):
            p0, p1, p2, p3 = p(i - 1), p(i), p(i + 1), p(i + 2)
            d.append(f"C{p1[0] + (p2[0] - p0[0]) / 6:.0f} {p1[1] + (p2[1] - p0[1]) / 6:.0f} "
                     f"{p2[0] - (p3[0] - p1[0]) / 6:.0f} {p2[1] - (p3[1] - p1[1]) / 6:.0f} {p2[0]:.0f} {p2[1]:.0f}")
        return "".join(d) + ("Z" if closed else "")

    def _an(self, note: bool) -> str:
        """An annotation arrives after the scene, in the order it was written."""
        if not note:
            return ""
        self.an += 1
        return f' data-an="{self.an}"'

    def _path(self, d: str, cls: str, note: bool = False) -> None:
        self.out.append(f'<path d="{d}" class="{cls}"{self._an(note)}/>')

    @staticmethod
    def _cls(pen: str, w: str = "", dash: bool = False) -> str:
        return f"z {PEN[pen]}{_WIDTH[w]}{' zd' if dash else ''}"

    def stroke(self, pts: list[tuple[float, float]], pen: str = "ink", w: str = "", closed: bool = False,
               amp: float = 1.7, dash: bool = False, raw: bool = False, note: bool = False) -> None:
        """A pen line through ``pts``. ``w``: ``t`` thin, ``h`` heavy. ``raw`` keeps the points as given
        (already curved); otherwise straight runs are wobbled."""
        q = pts if raw else self._wob(pts, amp, closed=closed)
        self._path(self._smooth(q, closed), self._cls(pen, w, dash=dash), note)

    def line(self, x0: float, y0: float, x1: float, y1: float, pen: str = "ink", w: str = "", dash: bool = False) -> None:
        self.stroke([(x0, y0), (x1, y1)], pen, w, dash=dash)

    def curve(self, pts: list[tuple[float, float]], pen: str = "ink", w: str = "", dash: bool = False,
              note: bool = False) -> None:
        """A flowing line through a few control points: one gesture, not wobbled piece by piece."""
        q = [(x + self._j(1.2), y + self._j(1.2)) for x, y in self._dense(pts)]
        self._path(self._smooth(q), self._cls(pen, w, dash=dash), note)

    def _dense(self, pts: list[tuple[float, float]], per: int = 4) -> list[tuple[float, float]]:
        n = len(pts)
        if n < 3:
            return pts
        out = []
        for i in range(n - 1):
            p0, p1, p2, p3 = pts[max(0, i - 1)], pts[i], pts[i + 1], pts[min(n - 1, i + 2)]
            for k in range(per):
                t = k / per
                t2, t3 = t * t, t * t * t
                out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2
                                        + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3) for a in (0, 1)))
        out.append(pts[-1])
        return out

    # ------------------------------------------------------------------ shapes
    def _fill(self, pts: list[tuple[float, float]], fill: str) -> None:
        p = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
        self.out.append(f'<polygon points="{p}" class="{_fc(fill)}"/>')

    def rect(self, x: float, y: float, w: float, h: float, pen: str = "ink", fill: str = "", sw: str = "",
             tilt: float = 0.0) -> None:
        """A box drawn the way a hand draws one: four sides, corners that do not quite meet.
        ``fill``: ``p`` paper (so it covers what is behind it), or a pen name."""
        cx, cy = x + w / 2, y + h / 2
        co, si = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))

        def t(px: float, py: float) -> tuple[float, float]:
            dx, dy = px - cx, py - cy
            return cx + dx * co - dy * si, cy + dx * si + dy * co

        c = [t(x, y), t(x + w, y), t(x + w, y + h), t(x, y + h)]
        if fill:
            self._fill(c, fill)
        for i in range(4):
            self.stroke([c[i], c[(i + 1) % 4]], pen, sw)

    def oval(self, cx: float, cy: float, rx: float, ry: float, pen: str = "ink", fill: str = "", w: str = "",
             rough: float = 0.03) -> None:
        """A circle that closes a little past where it began."""
        ph1, ph2, start = self.r.uniform(0, 6.28), self.r.uniform(0, 6.28), self.r.uniform(0, 6.28)
        steps = max(12, int((rx + ry) / 10))
        pts = []
        for i in range(steps + 2):                   # two extra: the overlap
            th = start + i * 6.2832 / steps
            k = 1 + rough * math.sin(2 * th + ph1) + rough * 0.7 * math.sin(3 * th + ph2) + (i / steps) * 0.02
            pts.append((cx + rx * k * math.cos(th), cy + ry * k * math.sin(th)))
        if fill:
            self.out.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" class="{_fc(fill)}"/>')
        self._path(self._smooth(pts), self._cls(pen, w))

    def poly(self, pts: list[tuple[float, float]], pen: str = "ink", fill: str = "", w: str = "") -> None:
        if fill:
            self._fill(pts, fill)
        for i in range(len(pts)):
            self.stroke([pts[i], pts[(i + 1) % len(pts)]], pen, w)

    def blob(self, cx: float, cy: float, rx: float, ry: float, pen: str = "ink", fill: str = "p", lumps: int = 5,
             depth: float = 0.14, w: str = "") -> None:
        """A lumpy closed shape: a cloud, a rock, a tangle, a puddle, a sack."""
        ph = self.r.uniform(0, 6.28)
        pts = []
        for i in range(18):
            th = i * 6.2832 / 18
            k = 1 + depth * math.sin(lumps * th + ph) + self._j(0.02)
            pts.append((cx + rx * k * math.cos(th), cy + ry * k * math.sin(th)))
        if fill:
            self._fill(pts, fill)
        self._path(self._smooth(pts, True), self._cls(pen, w))

    def hatch(self, x: float, y: float, w: float, h: float, gap: float = 16, pen: str = "faint", lean: float = 0.5) -> None:
        """Shading: slanted strokes inside a box, uneven on purpose."""
        t = x - h * lean
        while t < x + w:
            x0, y0, x1, y1 = t, y + h, t + h * lean, y
            if x0 < x:
                y0 -= (x - x0) / lean if lean else 0
                x0 = x
            if x1 > x + w:
                y1 += (x1 - (x + w)) / lean if lean else 0
                x1 = x + w
            if y0 - y1 > 8:
                self.stroke([(x0, y0 - abs(self._j(3))), (x1, y1 + abs(self._j(3)))], pen, "t", amp=0.8)
            t += gap + self._j(2)

    def arrow(self, x0: float, y0: float, x1: float, y1: float, pen: str = "path", bend: float = 0.0,
              dash: bool = False, w: str = "", head: float = 20, note: bool | None = None) -> None:
        """An arrow, bent by ``bend`` units at its middle (positive bends to the left of travel).
        An arrow in a pen other than ink is an annotation, and arrives with the labels."""
        note = pen != "ink" if note is None else note
        d = math.hypot(x1 - x0, y1 - y0) or 1
        nx, ny = -(y1 - y0) / d, (x1 - x0) / d
        mx, my = (x0 + x1) / 2 - nx * bend, (y0 + y1) / 2 - ny * bend
        if bend:
            self.curve([(x0, y0), (mx, my), (x1, y1)], pen, w, dash, note)
            ang = math.atan2(y1 - my, x1 - mx)
        else:
            self.stroke([(x0, y0), (x1, y1)], pen, w, dash=dash, note=note)
            ang = math.atan2(y1 - y0, x1 - x0)
        self.head(x1, y1, ang, pen, w, head, note)

    def head(self, x: float, y: float, ang: float, pen: str = "path", w: str = "", size: float = 20,
             note: bool = False) -> None:
        a, b = ang + 2.55 + self._j(0.06), ang - 2.55 + self._j(0.06)
        self.stroke([(x + math.cos(a) * size, y + math.sin(a) * size), (x, y), (x + math.cos(b) * size, y + math.sin(b) * size)],
                    pen, w, amp=0.5, note=note)

    def route(self, pts: list[tuple[float, float]], pen: str = "path", dash: bool = True, w: str = "h") -> None:
        """The main route: a flowing dashed line through the points, with a head at the end."""
        self.curve(pts, pen, w, dash, note=True)
        (ax, ay), (bx, by) = pts[-2], pts[-1]
        self.head(bx, by, math.atan2(by - ay, bx - ax), pen, w, 24, note=True)

    def burst(self, x: float, y: float, r: float = 30, n: int = 5, pen: str = "point", a0: float = -150, a1: float = -30) -> None:
        """Little rays: something just happened here."""
        for i in range(n):
            a = math.radians(a0 + (a1 - a0) * i / max(1, n - 1) + self._j(4))
            self.stroke([(x + math.cos(a) * r, y + math.sin(a) * r), (x + math.cos(a) * (r + 20), y + math.sin(a) * (r + 20))], pen, "t", amp=0.5)

    def ground(self, y: float, x0: float = 50, x1: float = W - 50, tufts: int = 3, pen: str = "ink") -> None:
        """A floor line with a little weather in it, and a few tufts so it reads as ground."""
        n = max(3, int((x1 - x0) / 170))
        self.curve([(x0 + (x1 - x0) * i / n, y + self._j(3.5)) for i in range(n + 1)], pen)
        for _ in range(tufts):
            tx = self.r.uniform(x0 + 40, x1 - 40)
            for dx in (-8, 0, 8):
                self.stroke([(tx + dx * 0.4, y - 1), (tx + dx, y - 14 - abs(self._j(4)))], pen, "t", amp=0.4)

    def squiggle(self, x: float, y: float, w: float, pen: str = "point") -> None:
        """An underline with a hand's impatience."""
        n = max(4, int(w / 26))
        self.curve([(x + w * i / n, y + (4 if i % 2 else -3)) for i in range(n + 1)], pen, "t", note=True)

    def ring(self, cx: float, cy: float, rx: float, ry: float, pen: str = "point") -> None:
        """A rough ring round the thing that matters."""
        self.an += 1
        n0 = len(self.out)
        self.oval(cx, cy, rx, ry, pen, rough=0.05)
        self.out[n0:] = [o.replace("/>", f' data-an="{self.an}"/>') for o in self.out[n0:]]

    def scribble(self, x: float, y: float, w: float, h: float, lines: int = 3, pen: str = "faint") -> None:
        """Writing too small to read: the lines on a document."""
        for i in range(lines):
            yy = y + h * (i + 0.5) / lines
            self.stroke([(x, yy), (x + w * (0.6 if i == lines - 1 else self.r.uniform(0.86, 1.0)), yy)], pen, "t", amp=1.0)

    # ------------------------------------------------------------------ words
    def label(self, x: float, y: float, text: str, pen: str = "point", size: int = LABEL, rot: float | None = None,
              anchor: str = "middle", note: bool = True) -> None:
        """Handwriting. One to five words; a ``|`` starts a second line. ``x, y`` is the first line's
        baseline, at its middle unless ``anchor`` says ``start`` or ``end``."""
        if rot is None:
            rot = self.r.uniform(-3.0, 1.5)
        self.words.append((text.replace("|", " "), size))
        lines = [t.strip() for t in text.split("|")]
        if len(lines) == 1:
            body = _E(lines[0])
        else:
            body = "".join(f'<tspan x="{x:.0f}" dy="{0 if i == 0 else size:.0f}">{_E(t)}</tspan>' for i, t in enumerate(lines))
        anc = {"middle": "", "start": " zs", "end": " ze"}[anchor]      # a class: a stylesheet outranks an attribute
        siz = "" if size == LABEL else f' font-size="{size}"'
        self.out.append(f'<text x="{x:.0f}" y="{y:.0f}" class="zw {PEN[pen]}{anc}"{siz} '
                        f'transform="rotate({rot:.1f} {x:.0f} {y:.0f})"{self._an(note)}>{body}</text>')

    def note(self, x: float, y: float, text: str, to: tuple[float, float], pen: str = "point", size: int = LABEL,
             anchor: str = "middle", bend: float = 16) -> None:
        """A label with a short arrow from it to the thing it names."""
        self.label(x, y, text, pen, size, anchor=anchor)
        lines = text.count("|") + 1
        tx, ty = to
        below = ty > y
        sx = x if anchor == "middle" else (x + 70 if anchor == "start" else x - 70)
        sy = y + (18 + (lines - 1) * size if below else -size * 0.84)
        d = math.hypot(tx - sx, ty - sy) or 1
        gap = min(18.0, d * 0.2)
        self.arrow(sx, sy, tx - (tx - sx) / d * gap, ty - (ty - sy) / d * gap, pen,
                   bend=bend if tx > sx else -bend, w="t", head=15, note=True)

    # ------------------------------------------------------------------ the worker
    def worker(self, x: float, y: float, s: float = 1.9, look: tuple[float, float] = (1, 0),
               arms: list[tuple[float, float] | None] | None = None, legs: str = "stand",
               lean: float = 0.0, squash: float = 1.0) -> None:
        """The small black worker, who does the thing the sketch is about.

        ``x, y`` is the middle of the body. The body is about 100*s wide and 124*s tall; the feet land
        about 106*s below ``y``. ``arms`` is two targets, left hand then right, each a point the hand
        reaches (it should be holding, pushing or carrying something there) or ``None`` for an arm at
        rest. ``legs``: ``stand``, ``walk``, ``sit``, ``none``. ``look`` points the eyes. ``lean`` tips
        the body, in degrees. ``squash`` below 1 is a body bearing a weight."""
        rx, ry = 50 * s, 62 * s * squash
        co, si = math.cos(math.radians(lean)), math.sin(math.radians(lean))
        ph1, ph2 = self.r.uniform(0, 6.28), self.r.uniform(0, 6.28)
        body = []
        for i in range(20):
            th = i * 6.2832 / 20
            k = 1 + 0.045 * math.sin(2 * th + ph1) + 0.035 * math.sin(3 * th + ph2)
            px, py = rx * k * math.cos(th), ry * k * (math.sin(th) if math.sin(th) < 0 else math.sin(th) * 0.94)
            body.append((x + px * co - py * si, y + px * si + py * co))
        foot_y = y + ry + 44 * s
        if legs != "none":                           # legs first, so the body sits on them
            spread = {"stand": (-17, 17), "walk": (-26, 22), "sit": (-14, 20)}[legs]
            for i, dx in enumerate(spread):
                hx, hy = x + dx * s * 0.9, y + ry * 0.86
                if legs == "walk":
                    fx, fy = x + dx * s * 1.5 + (10 if i else -4) * s, foot_y - (10 * s if i == 0 else 0)
                elif legs == "sit":
                    fx, fy = x + (dx + 38) * s, y + ry + 14 * s
                else:
                    fx, fy = x + dx * s + self._j(1.5), foot_y
                knee = ((hx + fx) / 2 + (6 * s if legs != "stand" else self._j(2)), (hy + fy) / 2)
                self.curve([(hx, hy), knee, (fx, fy)], "ink", "l")
                self.stroke([(fx - 3 * s, fy), (fx + 14 * s, fy)], "ink", "l", amp=0.4)
        self._path(self._smooth(body, True), "zB")
        for _ in range(3):                           # the marker's own texture across the body
            ty = y + self.r.uniform(-ry * 0.5, ry * 0.5)
            hw = rx * math.sqrt(max(0.05, 1 - ((ty - y) / ry) ** 2)) * 0.7
            self.out.append(f'<path d="M{x - hw:.0f} {ty:.0f}Q{x:.0f} {ty + self._j(5):.0f} {x + hw:.0f} {ty + self._j(3):.0f}" class="zT"/>')
        lx, ly = look                                # eyes: two white dots, set toward where it is looking
        ln = math.hypot(lx, ly) or 1
        ex, ey = x + lx / ln * rx * 0.3, y - ry * 0.3 + ly / ln * ry * 0.16
        for dx in (-rx * 0.24, rx * 0.24):
            self.out.append(f'<ellipse cx="{ex + dx:.0f}" cy="{ey:.0f}" rx="{6.2 * s:.1f}" ry="{7.4 * s:.1f}" class="zE"/>')
        arms = arms or [None, None]
        for i, hand in enumerate(arms[:2]):          # arms last, over the body
            side = -1 if i == 0 else 1
            sx, sy = x + side * rx * 0.86, y - ry * 0.02
            if hand is None:
                hx, hy = x + side * (rx + 12 * s), y + ry * 0.62
                self.curve([(sx, sy), (sx + side * 10 * s, sy + 22 * s), (hx, hy)], "ink", "l")
            else:
                hx, hy = hand
                self.curve([(sx, sy), ((sx + hx) / 2, (sy + hy) / 2 + 10 * s), (hx, hy)], "ink", "l")
            self.out.append(f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{5.2 * s:.0f}" class="zH"/>')

    # ------------------------------------------------------------------ props: paper and boxes
    def doc(self, x: float, y: float, w: float = 110, h: float = 142, tilt: float = 0, lines: int = 4,
            mark: str = "", pen: str = "ink") -> None:
        """A sheet of paper, its top left at ``x, y``. ``mark``: ``tick``, ``cross``, ``stamp`` or empty."""
        self.rect(x, y, w, h, pen, fill="p", tilt=tilt)
        self.scribble(x + 16, y + 18, w - 32, h - (70 if mark else 36), lines)
        cx, cy = x + w * 0.6, y + h * 0.72
        if mark == "tick":
            self.stroke([(cx - 20, cy), (cx - 5, cy + 16), (cx + 26, cy - 24)], "aside", "h", amp=0.6)
        elif mark == "cross":
            self.stroke([(cx - 18, cy - 18), (cx + 18, cy + 18)], "point", "h", amp=0.6)
            self.stroke([(cx + 18, cy - 18), (cx - 18, cy + 18)], "point", "h", amp=0.6)
        elif mark == "stamp":
            self.oval(cx, cy, 26, 18, "point")

    def envelope(self, x: float, y: float, w: float = 150, h: float = 96, tilt: float = 0, pen: str = "ink") -> None:
        self.rect(x, y, w, h, pen, fill="p", tilt=tilt)
        self.stroke([(x, y), (x + w / 2, y + h * 0.55), (x + w, y)], pen, "t")

    def binder(self, x: float, y: float, w: float = 200, h: float = 44, pen: str = "ink") -> None:
        """A thick folder lying flat, its top left at ``x, y``. Stack several for a pile."""
        self.rect(x, y, w, h, pen, fill="p", tilt=self._j(1.2))
        self.stroke([(x + 26, y + 6), (x + 26, y + h - 6)], pen, "t")
        self.oval(x + 13, y + h / 2, 5, 5, pen, w="t")

    def box(self, x: float, y: float, w: float = 190, h: float = 140, pen: str = "ink", open_: bool = False) -> None:
        """A cardboard box, its top left at ``x, y``, with its flaps up if open."""
        self.rect(x, y, w, h, pen, fill="p")
        if open_:
            self.stroke([(x, y), (x - 30, y - 36)], pen)
            self.stroke([(x + w, y), (x + w + 30, y - 36)], pen)
        else:
            self.stroke([(x + w * 0.5, y), (x + w * 0.5, y + h * 0.3)], pen, "t")

    def drawers(self, x: float, y: float, n: int = 3, w: float = 210, h: float = 76, open_: int = -1, pen: str = "ink") -> None:
        """A chest of drawers, its top left at ``x, y``. ``open_`` is the index of a drawer pulled out."""
        for i in range(n):
            dx = 36 if i == open_ else 0
            self.rect(x + dx, y + i * h, w, h - 7, pen, fill="p")
            self.stroke([(x + dx + w / 2 - 20, y + i * h + h * 0.46), (x + dx + w / 2 + 20, y + i * h + h * 0.46)], pen, "h", amp=0.4)

    def sack(self, x: float, y: float, w: float = 150, h: float = 170, pen: str = "ink") -> None:
        """A tied sack standing at ``x, y`` (the middle of its base)."""
        self.blob(x, y - h * 0.45, w / 2, h * 0.45, pen, lumps=4, depth=0.06)
        self.stroke([(x - 22, y - h * 0.9), (x, y - h), (x + 24, y - h * 0.92)], pen)

    def tag(self, x: float, y: float, w: float = 96, h: float = 56, tilt: float = -8, pen: str = "ink") -> None:
        """A luggage tag on a string, its string starting at ``x, y``."""
        self.curve([(x, y), (x + 14, y + 22), (x + 6, y + 44)], pen, "t")
        self.rect(x - w * 0.3, y + 44, w, h, pen, fill="p", tilt=tilt)
        self.oval(x - w * 0.3 + 14, y + 58, 5, 5, pen, w="t")

    # ------------------------------------------------------------------ props: signs and barriers
    def sign(self, x: float, y: float, text: str, pen: str = "point", post: float = 110, size: int = LABEL) -> None:
        """A board on a post, planted at ``x, y`` (the foot of the post). The words count as a label."""
        lines = text.split("|")
        w = max(len(t) for t in lines) * size * 0.46 + 56
        h = len(lines) * size + 34
        top = y - post - h
        self.stroke([(x, y), (x, y - post)], "ink", "h")
        self.rect(x - w / 2, top, w, h, "ink", fill="p", tilt=self.r.uniform(-2, 2))
        self.label(x, top + size * 0.98 + 6, text, pen, size, rot=self.r.uniform(-2, 2), note=False)

    def flag(self, x: float, y: float, text: str = "", pen: str = "point", h: float = 190, size: int = LABEL) -> None:
        """A flag on a pole planted at ``x, y``."""
        self.stroke([(x, y), (x, y - h)], "ink", "h")
        w = max(120, len(text) * size * 0.48 + 50)
        top = y - h
        self.curve([(x, top), (x + w * 0.5, top - 9), (x + w, top + 6)], "ink")
        self.curve([(x, top + 84), (x + w * 0.5, top + 76), (x + w, top + 90)], "ink")
        self.stroke([(x + w, top + 6), (x + w - 16, top + 48), (x + w, top + 90)], "ink", amp=0.6)
        if text:
            self.label(x + w * 0.46, top + 62, text, pen, size, rot=-2, note=False)

    def stamp(self, x: float, y: float, text: str, pen: str = "point", size: int = LABEL, tilt: float = -9) -> None:
        """What a rubber stamp leaves: a word in a rough frame."""
        w = len(text) * size * 0.5 + 44
        self.rect(x - w / 2, y - size * 0.9, w, size * 1.42, pen, tilt=tilt, sw="h")
        self.label(x, y + size * 0.2, text, pen, size, rot=tilt, note=False)

    def gate(self, x: float, y: float, w: float = 260, h: float = 230, shut: bool = True, pen: str = "ink") -> None:
        """Two posts and a bar. ``x, y`` is the foot of the left post."""
        for px in (x, x + w):
            self.rect(px - 11, y - h, 22, h, pen, fill="p")
        if shut:
            self.rect(x - 26, y - h * 0.62, w + 52, 26, pen, fill="p", tilt=-1)
            self.hatch(x + 10, y - h * 0.62, w - 20, 26, gap=26, pen="point")
        else:
            self.stroke([(x + 4, y - h * 0.58), (x + w * 0.62, y - h - 90)], pen, "h")
            self.stroke([(x + 14, y - h * 0.5), (x + w * 0.7, y - h - 80)], pen)

    def turnstile(self, x: float, y: float, h: float = 190, pen: str = "ink") -> tuple[float, float]:
        """A turnstile standing at ``x, y``: a post with three arms. Returns the end of the arm that bars the way."""
        self.rect(x - 16, y - h, 32, h, pen, fill="p")
        hx, hy = x, y - h * 0.72
        ends = []
        for a in (0, 120, 240):
            ex, ey = hx + math.cos(math.radians(a - 8)) * 150, hy + math.sin(math.radians(a - 8)) * 46
            self.stroke([(hx, hy), (ex, ey)], pen, "h")
            self.oval(ex, ey, 8, 8, pen, fill="p")
            ends.append((ex, ey))
        self.oval(hx, hy, 15, 15, pen, fill="p")
        return ends[0]

    def wall(self, x: float, y: float, w: float = 40, h: float = 260, pen: str = "ink") -> None:
        """A brick wall, its foot at ``x, y`` (the bottom left)."""
        self.rect(x, y - h, w, h, pen, fill="p")
        for i in range(1, int(h / 34)):
            yy = y - i * 34
            self.stroke([(x, yy), (x + w, yy)], pen, "t", amp=0.6)

    def door(self, x: float, y: float, w: float = 130, h: float = 250, ajar: bool = False, pen: str = "ink") -> None:
        """A door in its frame, the frame's foot at ``x, y`` (bottom left)."""
        self.stroke([(x, y), (x, y - h), (x + w, y - h), (x + w, y)], pen, "h")
        if ajar:
            self.poly([(x, y), (x, y - h), (x + w * 0.62, y - h + 20), (x + w * 0.62, y + 16)], pen, fill="p")
            self.oval(x + w * 0.5, y - h * 0.48, 6, 6, pen, fill="ink")
        else:
            self.oval(x + w * 0.82, y - h * 0.48, 6, 6, pen, fill="ink")

    def hatchway(self, x: float, y: float, w: float = 120, h: float = 84, pen: str = "ink") -> None:
        """A small opening in a wall, its top left at ``x, y``: a serving hatch, a slot, a cat flap."""
        self.rect(x, y, w, h, pen, fill="ink")
        self.rect(x - 9, y - 9, w + 18, h + 18, pen)

    def letterbox(self, x: float, y: float, pen: str = "ink") -> tuple[float, float]:
        """A wall letterbox, its top left at ``x, y``. Returns the mouth of its slot, for a hand to reach."""
        self.rect(x, y, 170, 220, pen, fill="p")
        self.rect(x + 26, y + 44, 118, 20, pen, fill="ink")
        self.stroke([(x + 46, y + 130), (x + 124, y + 130)], pen, "t")
        return x + 85, y + 54

    # ------------------------------------------------------------------ props: machines and measures
    def ladder(self, x: float, y: float, h: float = 300, w: float = 76, rungs: int = 5, lean: float = 40, pen: str = "ink") -> None:
        """A ladder standing at ``x, y`` (the foot of its left rail), leaning right by ``lean`` units."""
        self.stroke([(x, y), (x + lean, y - h)], pen, "h")
        self.stroke([(x + w, y), (x + w + lean, y - h)], pen, "h")
        for i in range(1, rungs + 1):
            t = i / (rungs + 1)
            self.stroke([(x + lean * t, y - h * t), (x + w + lean * t, y - h * t)], pen)

    def scale(self, x: float, y: float, tip: float = 0.0, w: float = 420, h: float = 260, pen: str = "ink") -> tuple[tuple[float, float], tuple[float, float]]:
        """A balance on a post at ``x, y``. ``tip`` from -1 (left pan down) to 1. Returns the two pan centres."""
        self.stroke([(x, y), (x, y - h)], pen, "h")
        self.stroke([(x - 56, y), (x + 56, y)], pen, "h")
        dy = tip * 56
        l, r_ = (x - w / 2, y - h - dy), (x + w / 2, y - h + dy)
        self.stroke([l, r_], pen, "h")
        pans = []
        for px, py in (l, r_):
            self.stroke([(px, py), (px - 48, py + 92)], pen, "t")
            self.stroke([(px, py), (px + 48, py + 92)], pen, "t")
            self.curve([(px - 66, py + 92), (px, py + 114), (px + 66, py + 92)], pen)
            pans.append((px, py + 92))
        return pans[0], pans[1]

    def seesaw(self, x: float, y: float, w: float = 560, tip: float = 0.0, pen: str = "ink") -> tuple[tuple[float, float], tuple[float, float]]:
        """A plank over a log, the log resting at ``x, y``. ``tip`` from -1 (left end down) to 1.
        Returns the two ends of the plank, for things to sit on."""
        self.oval(x, y - 34, 40, 34, pen, fill="p")
        dy = tip * 64
        l, r_ = (x - w / 2, y - 74 - dy), (x + w / 2, y - 74 + dy)
        self.poly([l, r_, (r_[0], r_[1] + 16), (l[0], l[1] + 16)], pen, fill="p")
        return l, r_

    def funnel(self, x: float, y: float, w: float = 280, h: float = 240, pen: str = "ink") -> tuple[float, float]:
        """A funnel whose mouth is centred at ``x, y``. Returns the point its spout pours from."""
        self.stroke([(x - w / 2, y), (x - 32, y + h * 0.62), (x - 32, y + h)], pen, "h")
        self.stroke([(x + w / 2, y), (x + 32, y + h * 0.62), (x + 32, y + h)], pen, "h")
        self.oval(x, y, w / 2, 24, pen)
        return x, y + h

    def pipe(self, pts: list[tuple[float, float]], r: float = 20, pen: str = "ink") -> None:
        """A pipe or a gutter along a polyline: two walls."""
        for side in (-1, 1):
            off = []
            for i, (px, py) in enumerate(pts):
                a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
                d = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
                off.append((px - (b[1] - a[1]) / d * r * side, py + (b[0] - a[0]) / d * r * side))
            self.stroke(off, pen)

    def dial(self, x: float, y: float, r: float = 86, at: float = 0.5, pen: str = "ink", zone: tuple[float, float] | None = None) -> None:
        """A gauge sitting on ``x, y``. ``at`` from 0 (left) to 1 (right). ``zone`` marks a red arc between two positions."""
        pts = [(x + r * math.cos(math.pi * (1 - i / 12)), y - r * math.sin(math.pi * (1 - i / 12))) for i in range(13)]
        self.stroke(pts, pen, "h", raw=True)
        self.stroke([(x - r - 8, y), (x + r + 8, y)], pen)
        for i in range(7):
            a = math.pi * (1 - i / 6)
            self.stroke([(x + (r - 16) * math.cos(a), y - (r - 16) * math.sin(a)), (x + (r - 4) * math.cos(a), y - (r - 4) * math.sin(a))], pen, "t", amp=0.3)
        if zone:
            zp = [(x + (r + 12) * math.cos(math.pi * (1 - (zone[0] + (zone[1] - zone[0]) * i / 5))),
                   y - (r + 12) * math.sin(math.pi * (1 - (zone[0] + (zone[1] - zone[0]) * i / 5)))) for i in range(6)]
            self.stroke(zp, "point", "h", raw=True)
        a = math.pi * (1 - at)
        self.stroke([(x, y - 5), (x + (r - 22) * math.cos(a), y - 5 - (r - 22) * math.sin(a))], "point", "h", amp=0.4)
        self.oval(x, y - 5, 8, 8, pen, fill="ink")

    def lever(self, x: float, y: float, on: bool = True, pen: str = "ink") -> tuple[float, float]:
        """A switch on a base at ``x, y``. Returns the knob, for a hand to hold."""
        self.rect(x - 44, y - 28, 88, 28, pen, fill="p")
        kx, ky = x + (34 if on else -34), y - 124
        self.stroke([(x, y - 28), (kx, ky)], pen, "h")
        self.oval(kx, ky, 15, 15, pen, fill="point" if on else "p")
        return kx, ky

    def crank(self, x: float, y: float, w: float = 240, h: float = 190, pen: str = "ink") -> tuple[float, float]:
        """A box of a machine with a hopper on top and a handle on its side, its bottom left at ``x, y``.
        Returns the handle, for a hand to turn."""
        self.rect(x, y - h, w, h, pen, fill="p")
        self.stroke([(x + w * 0.2, y - h), (x + w * 0.1, y - h - 60)], pen)
        self.stroke([(x + w * 0.8, y - h), (x + w * 0.9, y - h - 60)], pen)
        hx, hy = x + w + 62, y - h * 0.5 - 34
        self.stroke([(x + w, y - h * 0.5), (x + w + 34, y - h * 0.5), (hx, hy)], pen, "h")
        self.oval(hx, hy, 11, 11, pen, fill="p")
        self.rect(x + w * 0.3, y - 44, w * 0.4, 44, pen, fill="ink")
        return hx, hy

    def conveyor(self, x0: float, x1: float, y: float, pen: str = "ink") -> None:
        """A belt from ``x0`` to ``x1``, its top at ``y``."""
        self.stroke([(x0, y), (x1, y)], pen, "h")
        self.stroke([(x0, y + 38), (x1, y + 38)], pen)
        for px in (x0, x1):
            self.oval(px, y + 19, 19, 19, pen, fill="p")

    def jug(self, x: float, y: float, w: float = 150, h: float = 200, level: float = 0.0, marks: int = 4, pen: str = "ink") -> None:
        """A measuring jug standing at ``x, y`` (the middle of its base), filled to ``level``, with marks up its side."""
        self.stroke([(x - w / 2, y - h), (x - w * 0.42, y), (x + w * 0.42, y), (x + w / 2, y - h)], pen, "h")
        self.curve([(x + w / 2, y - h * 0.8), (x + w * 0.86, y - h * 0.62), (x + w * 0.5, y - h * 0.3)], pen)
        for i in range(1, marks + 1):
            yy = y - h * i / (marks + 1)
            self.stroke([(x - w * 0.36, yy), (x - w * 0.1, yy)], pen, "t", amp=0.4)
        if level:
            ly = y - h * level
            self.curve([(x - w * 0.44, ly), (x - w * 0.15, ly + 6), (x + w * 0.15, ly - 5), (x + w * 0.44, ly)], "aside")

    def bucket(self, x: float, y: float, w: float = 130, h: float = 120, level: float = 0.0, pen: str = "ink") -> None:
        """A bucket standing at ``x, y`` (the middle of its base), filled to ``level``."""
        self.stroke([(x - w / 2, y - h), (x - w * 0.36, y), (x + w * 0.36, y), (x + w / 2, y - h)], pen, "h")
        self.oval(x, y - h, w / 2, 14, pen)
        if level:
            ly, hw = y - h * level, w * (0.36 + 0.14 * level)
            self.curve([(x - hw, ly), (x - hw / 3, ly + 6), (x + hw / 3, ly - 5), (x + hw, ly)], "aside")

    def drop(self, x: float, y: float, s: float = 1.0, pen: str = "aside") -> None:
        """One drop falling."""
        self.curve([(x, y - 22 * s), (x - 11 * s, y + 4 * s), (x, y + 14 * s), (x + 11 * s, y + 4 * s), (x, y - 22 * s)], pen)

    def clock(self, x: float, y: float, r: float = 58, hour: float = 10, pen: str = "ink") -> None:
        self.oval(x, y, r, r, pen, fill="p")
        a = math.radians(hour * 30 - 90)
        self.stroke([(x, y), (x + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.5)], pen, "h", amp=0.3)
        self.stroke([(x, y), (x + r * 0.1, y - r * 0.74)], pen, amp=0.3)

    def calendar(self, x: float, y: float, w: float = 150, h: float = 150, pen: str = "ink") -> None:
        """A tear-off day, its top left at ``x, y``: a sheet with a dark bar across the top."""
        self.rect(x, y, w, h, pen, fill="p")
        self.rect(x, y, w, 28, pen, fill="ink")
        for px in (x + w * 0.26, x + w * 0.74):
            self.stroke([(px, y - 12), (px, y + 12)], pen, "h", amp=0.3)

    def magnifier(self, x: float, y: float, r: float = 58, pen: str = "ink") -> tuple[float, float]:
        """A magnifying glass centred at ``x, y``. Returns the end of its handle."""
        self.oval(x, y, r, r, pen, w="h")
        hx, hy = x + r * 1.7, y + r * 1.7
        self.stroke([(x + r * 0.72, y + r * 0.72), (hx, hy)], pen, "h", amp=0.5)
        return hx, hy

    def lock(self, x: float, y: float, s: float = 1.4, open_: bool = False, pen: str = "ink") -> None:
        self.rect(x - 28 * s, y - 20 * s, 56 * s, 46 * s, pen, fill="p")
        if open_:
            self.curve([(x - 16 * s, y - 20 * s), (x - 18 * s, y - 56 * s), (x + 10 * s, y - 62 * s), (x + 22 * s, y - 44 * s)], pen, "h")
        else:
            self.curve([(x - 16 * s, y - 20 * s), (x - 14 * s, y - 52 * s), (x + 14 * s, y - 52 * s), (x + 16 * s, y - 20 * s)], pen, "h")
        self.oval(x, y + 2 * s, 5 * s, 5 * s, pen, fill="ink")

    # ------------------------------------------------------------------ props: things lying about
    def coin(self, x: float, y: float, r: float = 28, pen: str = "ink") -> None:
        self.oval(x, y, r, r, pen, fill="p")
        self.stroke([(x, y - r * 0.5), (x, y + r * 0.5)], pen, "t", amp=0.3)

    def stack(self, x: float, y: float, n: int = 4, w: float = 96, pen: str = "ink") -> None:
        """A pile of coins or plates seen from the side, its bottom at ``x, y``."""
        for i in range(n):
            self.oval(x + self._j(3), y - i * 17, w / 2, 12, pen, fill="p")

    def rock(self, x: float, y: float, w: float = 130, h: float = 100, pen: str = "ink") -> None:
        """A rock sitting at ``x, y`` (the middle of its base)."""
        self.poly([(x - w / 2, y), (x - w * 0.36, y - h * 0.7), (x - w * 0.05, y - h), (x + w * 0.34, y - h * 0.78), (x + w / 2, y)], pen, fill="p")
        self.stroke([(x - w * 0.05, y - h), (x + w * 0.06, y - h * 0.5), (x - w * 0.12, y - h * 0.2)], pen, "t")

    def pebble(self, x: float, y: float, r: float = 22, pen: str = "ink") -> None:
        self.oval(x, y - r * 0.7, r, r * 0.7, pen, fill="p")

    def marble(self, x: float, y: float, r: float = 26, pen: str = "ink", fill: str = "p") -> None:
        self.oval(x, y, r, r, pen, fill=fill)
        self.curve([(x - r * 0.5, y - r * 0.2), (x - r * 0.2, y - r * 0.55), (x + r * 0.15, y - r * 0.55)], pen, "t")

    def cloud(self, x: float, y: float, w: float = 260, h: float = 120, pen: str = "aside") -> None:
        """A thought, a vibe, the weather: a lumpy outline centred at ``x, y``."""
        self.blob(x, y, w / 2, h / 2, pen, lumps=5, depth=0.16)

    def tangle(self, x: float, y: float, r: float = 100, pen: str = "ink") -> None:
        """A knot of yarn centred at ``x, y``: one line that crosses itself too many times."""
        pts = [(x + math.cos(i * 2.4) * r * (0.4 + 0.6 * ((i * 37) % 10) / 10), y + math.sin(i * 2.9) * r * 0.7 * (0.4 + 0.6 * ((i * 53) % 10) / 10)) for i in range(26)]
        self.curve(pts, pen, "t")

    def spool(self, x: float, y: float, s: float = 1.0, wound: bool = True, pen: str = "ink") -> None:
        """A spool of thread standing at ``x, y`` (the middle of its base)."""
        self.rect(x - 44 * s, y - 14 * s, 88 * s, 14 * s, pen, fill="p")
        self.rect(x - 30 * s, y - 104 * s, 60 * s, 90 * s, pen, fill="p")
        self.rect(x - 44 * s, y - 118 * s, 88 * s, 14 * s, pen, fill="p")
        if wound:
            for i in range(5):
                yy = y - (24 + i * 17) * s
                self.stroke([(x - 30 * s, yy), (x + 30 * s, yy + 7 * s)], pen, "t", amp=0.5)

    def string(self, x0: float, y0: float, x1: float, y1: float, sag: float = 40, pen: str = "ink") -> None:
        """A line that hangs between two points: a rope, a washing line, a cable."""
        self.curve([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + sag), (x1, y1)], pen)

    def mattress(self, x: float, y: float, w: float = 320, h: float = 60, pen: str = "ink") -> None:
        """Something soft to land on, its top left at ``x, y``."""
        self.rect(x, y, w, h, pen, fill="p", tilt=self._j(0.8))
        for i in range(1, 5):
            self.oval(x + w * i / 5, y + h / 2, 4, 4, pen, w="t")

    def sheet(self, x: float, y: float, lumps: list[tuple[float, float]], pen: str = "ink") -> None:
        """A dust sheet over things: ``lumps`` are (offset along, height) of what it covers, from ``x, y`` on the ground."""
        pts = [(x - 40, y)]
        for off, hgt in lumps:
            pts += [(x + off - 60, y - hgt * 0.45), (x + off, y - hgt), (x + off + 60, y - hgt * 0.45)]
        pts.append((x + lumps[-1][0] + 110, y))
        self._fill(pts, "p")
        self.curve(pts, pen)

    def table(self, x: float, y: float, w: float = 320, h: float = 130, pen: str = "ink") -> None:
        """A desk: a top at ``y`` starting at ``x``, and two legs down to ``y + h``."""
        self.stroke([(x - 14, y), (x + w + 14, y)], pen, "h")
        self.stroke([(x + 20, y), (x + 12, y + h)], pen)
        self.stroke([(x + w - 20, y), (x + w - 12, y + h)], pen)

    def shelf(self, x: float, y: float, w: float = 300, pen: str = "ink") -> None:
        """A shelf on two brackets, its top left at ``x, y``."""
        self.stroke([(x, y), (x + w, y)], pen, "h")
        for px in (x + 30, x + w - 30):
            self.stroke([(px, y), (px, y + 30), (px + 26, y)], pen, "t")

    def bridge(self, x0: float, x1: float, y: float, planks: int = 5, gap_at: int = -1, pen: str = "ink") -> None:
        """Planks across a gap from ``x0`` to ``x1`` at height ``y``. ``gap_at`` leaves one plank missing."""
        pw = (x1 - x0) / planks
        for i in range(planks):
            if i != gap_at:
                self.rect(x0 + i * pw + 4, y - 11, pw - 8, 22, pen, fill="p", tilt=self._j(1.2))

    def cliff(self, x: float, y: float, w: float, side: str = "left", depth: float = 220, pen: str = "ink") -> None:
        """A ledge of ground from ``x`` to ``x + w`` at height ``y``, ending in a drop. ``side`` is ``left`` when
        the ground lies to the left of its edge (edge at ``x + w``), ``right`` when the edge is at ``x``."""
        ex = x + w if side == "left" else x
        self.curve([(x, y), (x + w * 0.5, y + self._j(3)), (x + w, y)], pen)
        k = -1 if side == "left" else 1
        self.stroke([(ex, y), (ex + k * 16, y + depth * 0.5), (ex + k * 6, y + depth)], pen)
        for i in range(3):
            sx = ex + k * 26 + self._j(4)
            self.stroke([(sx, y + 34 + i * 48), (sx, y + 58 + i * 48)], pen, "t", amp=0.5)

    def plane(self, x: float, y: float, s: float = 1.6, ang: float = -8, pen: str = "ink") -> None:
        """A paper plane, nose to the right, centred near ``x, y``."""
        co, si = math.cos(math.radians(ang)), math.sin(math.radians(ang))

        def t(px: float, py: float) -> tuple[float, float]:
            return x + (px * co - py * si) * s, y + (px * si + py * co) * s

        self.poly([t(-60, -6), t(64, 0), t(-48, 30)], pen, fill="p")
        self.stroke([t(-60, -6), t(-18, 14), t(64, 0)], pen, "t")
        self.stroke([t(-18, 14), t(-30, 40)], pen, "t")

    def bot(self, x: float, y: float, s: float = 1.7, look: tuple[float, float] = (0, 0), pen: str = "aside") -> None:
        """The model, as a low-tech machine: a box with one eye and an aerial, in the blue pen because it is
        the machine in the story. ``x, y`` is the middle of the box; its feet land about 58*s below."""
        w, h = 92 * s, 78 * s
        self.rect(x - w / 2, y - h / 2, w, h, pen, fill="p")
        self.stroke([(x, y - h / 2), (x + 4 * s, y - h / 2 - 26 * s)], pen)
        self.oval(x + 4 * s, y - h / 2 - 32 * s, 6 * s, 6 * s, pen)
        self.oval(x + look[0] * 8 * s, y - 6 * s + look[1] * 6 * s, 15 * s, 15 * s, pen)
        self.oval(x + look[0] * 13 * s, y - 6 * s + look[1] * 9 * s, 5 * s, 5 * s, pen, fill="aside")
        self.stroke([(x - 20 * s, y + 22 * s), (x + 20 * s, y + 22 * s)], pen, "t")
        for dx in (-26, 26):
            self.stroke([(x + dx * s, y + h / 2), (x + dx * s, y + h / 2 + 18 * s)], pen)
            self.stroke([(x + dx * s - 9 * s, y + h / 2 + 18 * s), (x + dx * s + 9 * s, y + h / 2 + 18 * s)], pen)

    # ------------------------------------------------------------------ out
    def svg(self) -> str:
        return (f'<svg class="sk" viewBox="0 0 {W} {self.h}" role="img" aria-label="{_E(self.alt, quote=True)}">'
                f'{"".join(self.out)}</svg>')


def render(spec: dict) -> tuple[str, "Sk"]:
    """One sketch as a figure: the sheet, and its caption in real type. ``spec`` is an entry of a lesson's
    ``SKETCHES`` list: ``name``, ``alt``, ``caption``, ``draw``, and optionally ``h``."""
    s = Sk(spec["name"], spec["alt"], spec.get("h", H))
    spec["draw"](s)
    return (f'<figure class="sketch" data-sketch="{_E(spec["name"], quote=True)}">'
            f'<div class="sk-paper">{s.svg()}</div><figcaption>{_E(spec["caption"])}</figcaption></figure>'), s


# ------------------------------------------------------------------------------------ the rules
WORD = re.compile(r"[A-Za-z0-9$%'’.,&+×÷/:-]+")


def lint(spec: dict, s: "Sk", html: str) -> list[str]:
    """What a sketch must keep to. Returns the problems; an empty list is a pass."""
    out = []
    name = spec.get("name", "?")
    for k in ("name", "lesson", "idea", "verb", "prop", "alt", "caption", "draw"):
        if not spec.get(k):
            out.append(f"{name}: missing {k}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        out.append(f"{name}: the name must be lowercase-hyphenated")
    words = [(t, z) for t, z in s.words if len(re.sub(r"[^A-Za-z]", "", t)) >= 2 or len(t) > 3]
    if len(words) > 6:
        out.append(f"{name}: {len(words)} labels; six at most")
    if not words:
        out.append(f"{name}: no labels; a sketch says what it shows in two to six short ones")
    for t, z in s.words:
        if z < LABEL_MIN:
            out.append(f"{name}: '{t}' is written at {z}; {LABEL_MIN} is the floor (13px on a phone)")
        if len(WORD.findall(t)) > 5:
            out.append(f"{name}: '{t}' is more than five words")
        if "—" in t or "–" in t:
            out.append(f"{name}: '{t}' has a dash")
    cap = spec.get("caption", "")
    if cap and (len(cap.split()) > 26 or "—" in cap or "–" in cap):
        out.append(f"{name}: the caption is one plain sentence or two, 26 words at most, no dashes")
    if not 380 <= spec.get("h", H) <= 675:
        out.append(f"{name}: sheet height {spec.get('h')} is outside 380 to 675")
    if 'class="zB"' not in html:
        out.append(f"{name}: no worker; the worker does the thing the sketch is about")
    size = len(zlib.compress(html.encode("utf-8"), 9))
    if size > 6500:
        out.append(f"{name}: {size} bytes compressed; 6,500 is the budget (fewer strokes)")
    return out
