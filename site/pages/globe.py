"""The home page's hero scene: the Earth, a fine spiral around it, and one flight through the four phases.

Two halves. ``theme/hero.js`` draws the moving picture in one canvas on one clock: the Earth turning, the
spiral, and the flight staged like a launch, the aircraft changing form and hue at each phase and carrying a
tag that names the phase, until it rests in one named still. This module gives it what is fixed: the land as
a lattice of dots (:func:`land`), the markup (:func:`scene`), and a paused frame with nothing to run it
(:func:`still`), for the social card. The geometry constants below are the script's, kept in step by hand;
``still`` and the script draw the same spiral from them.

Without script the stylesheet draws a plain shaded disc and the names under it still read; with reduced
motion the script draws its rest frame once: the four forms parked in their phases, each named.

The coastlines are coarse on purpose. At one dot every two degrees a continent is a few hundred dots,
so a polygon with forty corners is already finer than the picture can show. They are drawn by hand and
are a picture of the Earth, not a map of it.
"""
from __future__ import annotations

import json
import math

# (lon, lat) rings, clockwise or not: the test below does not care.
LAND: dict[str, list[tuple[float, float]]] = {
    "north-america": [
        (-168, 65.5), (-162, 70), (-156, 71.3), (-141, 69.6), (-128, 70), (-115, 68.5), (-108, 68), (-96, 68),
        (-94, 72), (-88, 68.5), (-85, 69.5), (-81, 68), (-86, 66), (-87, 64), (-94, 61), (-94, 58.7),
        (-88, 56.5), (-82, 55), (-82, 52.5), (-79, 51.5), (-79, 54.5), (-77, 57), (-78, 60), (-77.5, 62.5),
        (-72, 61.5), (-68, 58.5), (-64, 60.3), (-61, 56), (-56, 52.5), (-60, 50), (-66, 50.2), (-64.5, 46),
        (-60.5, 46), (-66, 43.8), (-70, 43.5), (-70.5, 41.7), (-74, 40.5), (-75.5, 37.8), (-76, 35),
        (-78.5, 33.8), (-81, 31.5), (-80, 27), (-80.5, 25.2), (-82, 27), (-82.7, 29.5), (-85, 29.7),
        (-89, 30.2), (-90, 29.2), (-94, 29.5), (-97.3, 27.5), (-97.7, 22.5), (-96, 19), (-94.5, 18.2),
        (-91, 18.7), (-90.5, 21), (-87, 21.5), (-87.5, 18), (-88.8, 15.8), (-84, 15.8), (-83.3, 11),
        (-81, 8.8), (-77.5, 8.7), (-77.3, 7.5), (-80.5, 7.2), (-83, 8.3), (-85.7, 10), (-87.5, 13),
        (-91.5, 14), (-94.5, 16.2), (-99, 16.7), (-105, 19.8), (-105.5, 22.5), (-109, 25.5), (-112.5, 30),
        (-114.5, 31), (-112, 27), (-109.5, 23.2), (-112, 24.5), (-115, 29.5), (-117.2, 32.5), (-120.5, 34.5),
        (-122.5, 37.5), (-124.2, 40.5), (-124, 46), (-124.7, 48.3), (-127.5, 50.5), (-130.5, 54.5),
        (-134, 58), (-139, 59.8), (-146, 60.5), (-151.5, 59.3), (-154, 57.5), (-158, 56.5), (-162, 55),
        (-158, 58.5), (-162, 60), (-165.5, 61.5), (-164, 63.5), (-161, 64.5), (-166, 64.5)],
    "baffin": [(-80, 73.5), (-71, 71), (-62, 66.5), (-66, 62.5), (-72, 64), (-78, 65), (-73, 68), (-84, 70), (-88, 73.5)],
    "victoria": [(-125, 72), (-115, 73.5), (-105, 73), (-102, 69.5), (-110, 69), (-117, 70.5)],
    "ellesmere": [(-90, 76.5), (-80, 76), (-63, 82), (-75, 83), (-92, 81)],
    "greenland": [(-73, 78.2), (-61, 76), (-55, 70), (-51, 64), (-45, 60), (-41.5, 63), (-32, 68), (-22, 70),
                  (-19, 75), (-18, 80), (-30, 83.5), (-50, 82.5), (-62, 81.5)],
    "cuba": [(-85, 22), (-80, 23.2), (-74.3, 20.2), (-77.5, 19.9), (-82, 21.5)],
    "hispaniola": [(-74.4, 18.5), (-68.5, 18.3), (-69.8, 19.8), (-72.8, 19.9)],
    "south-america": [
        (-77.3, 8), (-75.5, 10.8), (-72, 12), (-68, 11.2), (-62, 10.7), (-60, 8.4), (-57, 6), (-52, 4.8),
        (-50, 1), (-48.5, -1), (-44.5, -2.5), (-39.5, -3), (-35.2, -5.5), (-35, -8.5), (-38.5, -13),
        (-39, -17.5), (-41, -22), (-45, -23.8), (-48.5, -26.5), (-51, -30.5), (-53.5, -34), (-57.5, -35),
        (-57.5, -38), (-62, -39), (-65, -41), (-64.5, -43), (-67.5, -46), (-66, -48), (-69, -51),
        (-68.5, -53), (-66, -55), (-71, -54.5), (-74.5, -51.5), (-75, -47), (-73.5, -43), (-73.5, -37.5),
        (-71.5, -31), (-70.5, -24), (-70.3, -18.4), (-75.5, -15), (-78.5, -8.5), (-81, -5.5), (-80, -2.5),
        (-80.8, -0.8), (-78.8, 1.5), (-77.3, 4)],
    "eurasia": [
        (-9.3, 38.7), (-8.8, 43.2), (-1.8, 43.4), (-1.2, 46), (-4.6, 48.4), (-1.6, 49.2), (1.8, 50.9),
        (4, 52), (8.2, 53.7), (8.6, 57), (10.6, 57.7), (10.2, 55), (12.5, 54.2), (14.2, 53.9), (18.5, 54.7),
        (21, 55.2), (21.3, 57.2), (24.2, 57.6), (23.5, 59.3), (28.5, 59.8), (30, 60), (23, 60), (22.5, 60.2),
        (21.3, 61.5), (25, 65.2), (22, 65.7), (21.3, 63.5), (17.3, 62), (18.5, 60), (16.5, 56.5), (13, 55.5),
        (11.5, 58.5), (10.5, 59.3), (8, 58.1), (5.5, 59), (5, 61.8), (8.5, 63.6), (13, 66.3), (15.7, 68.8),
        (21, 70), (26, 71.1), (31, 70.3), (33.5, 69.3), (41, 67.5), (44, 66.2), (44.5, 68.3), (54, 68.3),
        (60.5, 69.5), (68.5, 68.5), (67, 71.5), (72.5, 73), (74.5, 68), (74, 72.2), (80.5, 73.5), (87, 74),
        (98, 76), (104.5, 77.7), (113, 74), (113.5, 76), (127, 73), (130, 71), (140, 72.8), (152, 71),
        (160, 69.7), (170, 70), (180, 68.8), (180, 65), (177.5, 64.6), (179, 62.5), (170.5, 60), (163.5, 58),
        (162.8, 54.8), (156.8, 51.2), (155.8, 57), (159, 61.8), (152, 59), (143, 59.4), (136, 55), (141, 53),
        (140.5, 48), (135.5, 43.5), (130.8, 42.6), (127.5, 39.8), (129.3, 37), (127, 34.7), (126.3, 37.5),
        (125, 39.5), (121.5, 39), (121.9, 40.5), (117.8, 39), (119, 37.3), (122.5, 37), (119.3, 35),
        (121.8, 31.5), (121.8, 29), (119.5, 25.5), (116.5, 23), (113.5, 22.3), (110.5, 21.3), (108.5, 21.6),
        (106, 19), (108.8, 15.3), (109.3, 11.6), (106.8, 10.3), (105, 8.7), (104.8, 10), (102.5, 12.2),
        (100.9, 13.4), (100, 11), (99.2, 9.2), (101.3, 6.8), (103.4, 4), (104.2, 1.4), (103.4, 1.3),
        (101.3, 2.8), (100.3, 5.8), (98.3, 8), (98.7, 10.5), (97.7, 16.3), (95.3, 15.8), (94.3, 18.5),
        (92, 21.5), (90.5, 22.3), (88.7, 21.7), (86.8, 20.6), (82.3, 16.5), (80.2, 15.3), (80.1, 13.2),
        (79.8, 10.3), (77.5, 8.1), (76.2, 10), (74.8, 13), (73.3, 17), (72.8, 19.5), (72.6, 21.2), (70, 20.9),
        (68.9, 22.3), (67.2, 24.6), (62, 25.1), (57.3, 25.6), (56.5, 27), (54, 26.6), (51.5, 27.8), (50.2, 30),
        (48.9, 30.3), (48, 29.9), (50.1, 26.7), (51.5, 24.5), (54.5, 24.2), (56.3, 26.2), (56.6, 24.5),
        (59.8, 22.5), (58.5, 20.4), (55.3, 17.4), (52.2, 16.2), (48.7, 14), (45, 12.8), (43.3, 13),
        (42.7, 16.3), (39.2, 21.3), (36.9, 25.5), (35, 28), (34.9, 29.5), (34.3, 31.3), (35.6, 34.5),
        (36, 36.8), (32.5, 36.1), (30.6, 36.8), (27.4, 37), (26.3, 39.3), (29, 41), (31.5, 41.2), (35.2, 42),
        (38.5, 40.9), (41.6, 41.6), (41, 43.2), (37.4, 45.2), (39.3, 47.2), (35, 46.2), (33.6, 44.5),
        (32.5, 45.4), (33.6, 46.1), (30.7, 46.5), (28.9, 44.8), (27.9, 42.5), (28.1, 41.2), (26, 40.8),
        (23.8, 40.3), (22.7, 39.2), (24, 37.7), (22.8, 36.5), (21.7, 36.9), (21.1, 38.4), (19.4, 40.3),
        (19.6, 41.8), (16.2, 43.5), (13.7, 45.6), (12.3, 45.3), (12.4, 44.1), (14.2, 42.4), (16, 41.9),
        (18.5, 40.1), (16.9, 40.4), (16.5, 38.9), (15.7, 38), (16, 39.8), (12.3, 41.7), (10.4, 43),
        (8.8, 44.4), (7.5, 43.8), (4.8, 43.4), (3.1, 42.5), (3.2, 41.8), (0.2, 39.9), (-0.5, 38.3),
        (-2.2, 36.7), (-5.4, 36.1), (-6.4, 36.8), (-8.9, 37)],
    "africa": [
        (-5.9, 35.8), (-2, 35.1), (3, 36.9), (10.2, 37.2), (11, 33.6), (15.2, 32.4), (19.9, 30.8), (20.1, 32.5),
        (23.2, 32.5), (29, 30.9), (32.3, 31.3), (32.6, 29.9), (35.5, 24), (37.2, 21), (37.4, 18.8), (39.5, 15.5),
        (43.2, 12.5), (43.3, 11.4), (47, 11.2), (51.2, 11.9), (50.8, 9.5), (47.5, 4.5), (44, 1), (41.5, -1.8),
        (39.3, -5), (39.5, -8.5), (40.5, -11), (40.7, -15), (37, -17.8), (35, -20), (35.5, -24), (32.8, -26),
        (32.5, -28.7), (30.5, -31), (27.5, -33.5), (25, -34), (20, -34.8), (18.3, -34), (18, -32), (15.2, -27),
        (14.5, -22.5), (11.8, -17.5), (13.5, -12.5), (12.2, -6), (9.3, -1), (9.6, 2.5), (8.6, 4.5), (5.5, 4.5),
        (4.3, 6.3), (1.2, 6), (-2, 5), (-4.7, 5.2), (-7.5, 4.4), (-9.3, 5.8), (-11.5, 6.9), (-13.3, 9),
        (-15, 10.8), (-16.8, 12.5), (-17.5, 14.7), (-16.5, 16.2), (-16.2, 19), (-17, 21), (-15.8, 23.8),
        (-14.5, 26.2), (-13, 27.8), (-10, 29.4), (-9.7, 31.5), (-6.8, 34)],
    "madagascar": [(49.3, -12), (50.4, -15.5), (49.5, -17.5), (47.6, -24.5), (45.2, -25.5), (43.6, -23),
                   (44.3, -20), (44, -16.5), (46.3, -15.8), (48, -13.5)],
    "australia": [
        (113.5, -22), (114.2, -26.5), (115.7, -31.5), (115, -34.3), (118, -35), (123.5, -34), (126, -32.3),
        (131, -31.5), (134.2, -33), (135.8, -34.8), (138, -33), (137.7, -35.2), (139.7, -37), (141.5, -38.3),
        (144.5, -38), (146.3, -39), (149.9, -37.5), (151.2, -34), (153, -30.5), (153.3, -27.5), (152.8, -25.3),
        (150.8, -23), (149, -20.3), (146.2, -19), (145.4, -15), (143.5, -14.3), (142.7, -11), (141.7, -13),
        (141.5, -16), (140.8, -17.6), (139, -17.5), (135.8, -15), (136.7, -12.2), (132.5, -11.4), (130.5, -12.6),
        (129.5, -15), (126.5, -14), (124.3, -16.3), (122.2, -18), (121, -19.7), (118.5, -20.4), (116, -21)],
    "tasmania": [(144.7, -40.8), (148.2, -40.9), (148, -43.3), (146, -43.5), (145.2, -42.2)],
    "nz-north": [(172.7, -34.5), (175, -36.3), (178.3, -37.7), (177, -39.5), (175.3, -41.5), (174.8, -39.5),
                 (173.8, -39.3), (174.7, -37.3)],
    "nz-south": [(172.7, -40.6), (174.2, -41.7), (172.8, -43.7), (170.7, -45.8), (168.5, -46.6), (166.6, -46),
                 (168.3, -44.2), (171.2, -42)],
    "new-guinea": [(131, -0.8), (134, -0.9), (135, -3.3), (137.8, -1.5), (141, -2.6), (144.5, -3.9), (147.3, -6),
                   (147.7, -7.7), (150.5, -10.4), (147, -9.8), (144, -7.7), (142.5, -9.2), (139, -8.2),
                   (138, -5.8), (135.5, -4.5), (133, -4), (132.2, -2.9), (133.9, -2.3)],
    "borneo": [(109, 1.5), (110.5, 1.8), (113, 3.2), (115.5, 5), (116.8, 7), (119.2, 5.2), (118, 4.3), (117.8, 1),
               (116.5, -1.5), (116.3, -3.8), (114.5, -4), (111.8, -3.3), (110.2, -2.8), (109.2, -0.5)],
    "sumatra": [(95.3, 5.6), (97.5, 5.2), (100.4, 2.6), (103.5, -1), (106, -3), (105.8, -5.8), (104.3, -5.9),
                (102.3, -4), (100.3, -0.9), (98.7, 1.7), (96.3, 3.8)],
    "java": [(105.3, -6.8), (108.5, -6.5), (111, -6.6), (114.5, -7.7), (114.3, -8.6), (110.5, -8.2), (106.4, -7.4)],
    "sulawesi": [(119.5, -5.5), (120.5, -2.8), (119.8, 0.2), (121, 1.2), (124.8, 1.5), (123, 0.4), (121.5, -0.8),
                 (123.3, -0.9), (122.3, -3.3), (122.8, -4.8), (121.6, -4.5), (120.4, -5.6)],
    "luzon": [(120.3, 18.5), (122.2, 18.4), (122, 16), (124, 13.8), (123.8, 12.6), (121.9, 13.6), (120.6, 14.3),
              (119.8, 16.2)],
    "mindanao": [(122, 7.3), (123.5, 8.6), (125.4, 9.7), (126.5, 7.5), (125.4, 5.7), (124, 6.8)],
    "honshu": [(130.2, 31.3), (131.8, 31.4), (132, 33.5), (135, 33.5), (137, 34.6), (139.8, 35), (140.9, 36.9),
               (141.8, 39.5), (141.3, 41.4), (140, 40.6), (139.5, 38.2), (137.2, 36.9), (136, 35.9), (132.8, 35.5),
               (130.9, 34.2), (129.6, 33)],
    "hokkaido": [(140, 41.5), (141.2, 42.5), (143.3, 42), (145.5, 43.3), (144.3, 44.1), (141.9, 45.5),
                 (141.3, 43.3), (140, 43)],
    "sakhalin": [(142, 46), (143.5, 46.8), (143.2, 49.5), (144.5, 49), (143, 53.5), (141.9, 52), (142.1, 48)],
    "taiwan": [(120.1, 23), (120.9, 22), (121.8, 24.5), (121.5, 25.2)],
    "sri-lanka": [(79.8, 8.9), (81.2, 8.5), (81.9, 7), (80.6, 5.9), (79.8, 7)],
    "britain": [(-5.6, 50.1), (-3, 50.6), (1.3, 51.2), (1.7, 52.7), (0.2, 53.3), (-0.2, 54.5), (-1.7, 55.7),
                (-2.2, 57.6), (-3.3, 58.6), (-5, 58.6), (-6.2, 57.3), (-5.2, 55.8), (-4.9, 54.8), (-3.2, 54.9),
                (-3.1, 53.3), (-4.6, 53.2), (-4.3, 52.2), (-5.2, 51.8), (-3.2, 51.4), (-4.5, 51)],
    "ireland": [(-10, 51.6), (-8, 51.7), (-6.2, 52.3), (-6, 54), (-5.6, 54.7), (-7.3, 55.3), (-8.5, 54.5),
                (-10, 54.2), (-9.8, 53.2)],
    "iceland": [(-24.3, 65.5), (-22, 66.4), (-18, 66.3), (-14.8, 66.2), (-13.6, 65), (-16, 63.9), (-19.5, 63.5),
                (-22.5, 63.9)],
    "svalbard": [(11, 79), (16, 77), (21, 78.5), (27, 80), (18, 80.2)],
    "novaya-zemlya": [(52, 71), (56, 71), (60, 75), (68, 77), (60, 76.5), (54, 73.5)],
    "sicily": [(12.5, 38), (15.5, 38.2), (15.1, 36.7), (12.6, 37.6)],
    "sardinia": [(8.3, 41), (9.7, 41), (9.6, 39.2), (8.5, 39)],
}

STEP = 2.0            # degrees between dots along a meridian
LAT0, LAT1 = -56.0, 82.0


def _inside(lon: float, lat: float, ring: list[tuple[float, float]]) -> bool:
    hit = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            hit = not hit
        j = i
    return hit


_BOXES = {k: (min(x for x, _ in r), max(x for x, _ in r), min(y for _, y in r), max(y for _, y in r))
          for k, r in LAND.items()}


def is_land(lon: float, lat: float) -> bool:
    for k, ring in LAND.items():
        x0, x1, y0, y1 = _BOXES[k]
        if x0 <= lon <= x1 and y0 <= lat <= y1 and _inside(lon, lat, ring):
            return True
    return False


def land() -> dict:
    """The land as rows of runs. Each row is a latitude; its dots are spaced evenly along it, fewer
    toward the poles, so the lattice has the same density everywhere. A run is (first dot, count)."""
    rows = []
    n_lat = int(round((LAT1 - LAT0) / STEP)) + 1
    for k in range(n_lat):
        lat = LAT0 + k * STEP
        n = max(1, int(round(360 * math.cos(math.radians(lat)) / STEP)))
        runs, start = [], None
        for j in range(n + 1):
            on = j < n and is_land(-180 + (j + 0.5) * 360 / n, lat)
            if on and start is None:
                start = j
            elif not on and start is not None:
                runs += [start, j - start]
                start = None
        rows.append([n, runs])
    return {"lat0": LAT0, "step": STEP, "rows": rows}


def land_json() -> str:
    return json.dumps(land(), separators=(",", ":"))


# ------------------------------------------------------------------------------------ the spiral
# In Earth radii, and the same numbers as theme/hero.js. The front of each turn is the journey, P0 to P3, an
# eighth of a turn a phase, with the sign-off a quarter of the way round; the back of the turn, behind the
# Earth, is the way back to Frame; each turn sits PITCH above the last.
RHO = 1.3             # the spiral's radius
ALPHA = 15.0          # degrees its plane tips toward the reader
ROLL = 14.0           # degrees it rises to the right
PITCH = 0.17          # one turn climbs this much
PAST, AHEAD = 2.3, 0.6
STILL_AT = 0.29       # the social card's moment: just past the sign-off, built. The hero's own still (reduced
                      # motion, and where the flight comes to rest) is its rest frame, drawn by theme/hero.js

LEGS = [("P0", "Frame", "slate"), ("P1", "Design &amp; Spec", "indigo"),
        ("P2", "Build &amp; Prove", "teal"), ("P3", "Run &amp; Learn", "amber")]

# One aircraft, three shapes. Fourteen corners in the same order (nose, wing root, wingtip fore and aft,
# wing root aft, tail root, tail tip, tail centre, and back up the other side), so one shape can be
# eased into the next: a paper dart while the idea is framed, an airliner while it is designed and built,
# a jet when it is flying for real. Until the sign-off it is an outline; after it, solid. In the hero each
# form also wears its phase's hue: slate, indigo, teal, amber.
_DART = [(16, 0), (5, -2.3), (-12.2, -10.8), (-13.8, -9.4), (-7.8, -2.6), (-11, -2.1), (-13.4, -1.5), (-11.8, 0)]
_LINER = [(15.5, 0), (3.5, -2.7), (-5.5, -14), (-9.5, -14), (-3.5, -2.7), (-10.5, -2.3), (-15.5, -7.2), (-13.5, 0)]
_JET = [(18, 0), (4, -2.3), (-9.5, -10.5), (-13, -10.5), (-8.5, -3.1), (-11.5, -2.7), (-16.5, -6.2), (-12.5, 0)]


def _shape(half: list[tuple[float, float]]) -> str:
    pts = half + [(x, -y) for x, y in reversed(half[1:-1])]
    return "M" + " L".join(f"{x:g} {y:g}" for x, y in pts) + " Z"


SHAPES = {"dart": _shape(_DART), "liner": _shape(_LINER), "jet": _shape(_JET)}
# what the aircraft is in each phase: (shape, how it is drawn)
CRAFT = [("dart", "drawn"), ("liner", "drawn"), ("liner", "built"), ("jet", "built")]


def scene(pause: str = "") -> str:
    """The hero's picture. A screen reader gets one sentence for it; the bands below say the rest in words.
    ``pause`` is the control that stills it: with script it sits in the stage's corner and the line of names
    goes, because the picture names its own phases; without script the names stay under the disc."""
    names = "".join(
        f'<li style="--c:var(--dg-{hue})"><b>{key}</b>{name}</li>' + ('<li class="gate">sign-off</li>' if key == "P1" else "")
        for key, name, hue in LEGS)
    names += '<li class="back">then back to Frame, one level up</li>'
    says = ("A paper dart flies round the Earth through four phases and becomes, in turn, a drawing, a built "
            "airliner and a jet. It stops at a sign-off before it is built. Then it comes back to Frame, one level "
            "higher.")
    return (f'<div class="scene"><div class="sc-stage" role="img" aria-label="{says}">'
            '<canvas class="sc-cv" data-globe width="1168" height="984"></canvas></div>'
            f'<div class="sc-foot"><ol class="sc-rail" data-globe-rail aria-hidden="true">{names}</ol>{pause}</div></div>')


# ------------------------------------------------------------------------------------ a still
# The same scene with nothing to run it: the Earth projected once, here, and written out as dots, with
# the spiral and the aircraft where a paused frame would have them. The social card uses it, because a
# card is a picture and has no script. Colours are literal for the same reason: a card has one look.
STILL = {"slate": "#8FA8BE", "indigo": "#8E9BF0", "teal": "#4FBDB6", "amber": "#D9A94A", "rose": "#DE8A8A",
         "dot": "#4F7BAA", "lit": "#EEF6FF", "a": "#24487A", "m": "#0F2038", "b": "#060A12", "air": "#4C8FD8",
         "ink": "#ECEAE4", "paper": "#181A1E", "bone": "#121316", "soft": "#93908A"}
CX, CY, R = 500.0, 500.0, 318.0


def _spot(u: float, up: float) -> tuple[float, float, float]:
    """The point ``u`` turns along the spiral when the aircraft is at ``up``: x, y on the 1000 box, and depth."""
    sa, ca = math.sin(math.radians(ALPHA)), math.cos(math.radians(ALPHA))
    sr, cr = math.sin(math.radians(ROLL)), math.cos(math.radians(ROLL))
    ph = u * 2 * math.pi
    x, z, y = -RHO * math.cos(ph), RHO * math.sin(ph), PITCH * (u - up)
    y1 = y * ca - z * sa
    return CX + R * (x * cr - y1 * sr), CY - R * (x * sr + y1 * cr), y * sa + z * ca


def _fade(d: float) -> float:
    if d <= 0:
        q = -d
        if q < 0.55:
            return 1 - q * 0.55
        if q < 1.3:
            return 0.7 - (q - 0.55) / 0.75 * 0.42
        return 0.28 * max(0.0, 1 - (q - 1.3) / (PAST - 1.3))
    return 0.62 * max(0.0, 1 - d / AHEAD) ** 0.8


def _track(up: float, front: bool, c: dict) -> str:
    """One half of the spiral as short strokes, each with its own strength."""
    out, step = [], 1 / 90
    n0, n1 = math.ceil((up - PAST) / step), math.floor((up + AHEAD) / step)
    prev = None
    for i in range(n0, n1 + 1):
        u = i * step
        x, y, z = _spot(u, up)
        if prev is not None:
            mid = u - step / 2
            if ((z + prev[2]) / 2 >= 0) == front:
                f = mid - math.floor(mid)
                leg = int(f * 8) if f < 0.5 else 4
                a = _fade(mid - up) * (1 if front else 0.62) * (0.75 if leg == 4 else 1)
                if a > 0.02:
                    out.append(f'<path d="M{prev[0]:.1f} {prev[1]:.1f}L{x:.1f} {y:.1f}" '
                               f'stroke="{c["soft"] if leg == 4 else c[LEGS[leg][2]]}" stroke-opacity="{a:.2f}" '
                               f'stroke-width="{1.7 if leg == 4 else 2.6}"/>')
        prev = (x, y, z)
    return "".join(out)


def still(lon0: float = 58.0, tilt: float = 20.0) -> str:
    """The hero's picture as one self-contained SVG, 1000 by 1000, drawn as a paused frame."""
    c = STILL
    st, ct = math.sin(math.radians(tilt)), math.cos(math.radians(tilt))
    lx, ly, lz = -0.46, 0.56, 0.69
    dots = []
    d = land()
    for r, (n, runs) in enumerate(d["rows"]):
        lat = math.radians(d["lat0"] + r * d["step"])
        for i in range(0, len(runs), 2):
            for j in range(runs[i + 1]):
                lon = math.radians(-180 + (runs[i] + j + 0.5) * 360 / n - lon0)
                cz = math.cos(lat) * math.cos(lon)
                z = st * math.sin(lat) + ct * cz
                if z <= 0.02:
                    continue
                x = math.cos(lat) * math.sin(lon)
                y = ct * math.sin(lat) - st * cz
                lit = x * lx + y * ly + z * lz
                a = (0.3 + 0.7 * max(0.0, lit)) * min(1.0, z * 3.2)
                dots.append(f'<circle cx="{CX + R * x:.1f}" cy="{CY - R * y:.1f}" r="{1.7 * (0.55 + 0.45 * z):.2f}" '
                            f'fill="{c["lit"] if lit > 0.6 else c["dot"]}" fill-opacity="{a:.2f}"/>')
    up = STILL_AT
    px, py, _z = _spot(up, up)
    qx, qy, _z = _spot(up + 0.003, up)
    ang = math.degrees(math.atan2(qy - py, qx - px))
    plane = (f'<g transform="translate({px:.1f} {py:.1f}) rotate({ang:.1f}) scale(1.9)" fill="{c["ink"]}" '
             f'stroke="{c["ink"]}" stroke-width="1.2" stroke-linejoin="round"><path d="{SHAPES["liner"]}"/></g>')
    trail = ""
    for k in range(24):
        (x0, y0, _a), (x1, y1, _b) = _spot(up - 0.12 * k / 24, up), _spot(up - 0.12 * (k + 1) / 24, up)
        t = 1 - (k + 0.5) / 24
        trail += (f'<path d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}" stroke="{c["teal"]}" stroke-opacity="{0.25 + 0.75 * t:.2f}" '
                  f'stroke-width="{2.6 + 3.4 * t * t:.1f}"/>')
    gate = ""
    for lap in (0, -1):
        gx, gy, gz = _spot(lap + 0.25, up)
        hx, hy, _z = _spot(lap + 0.254, up)
        if gz < 0:
            continue
        l = math.hypot(hx - gx, hy - gy) or 1.0
        nx, ny = -(hy - gy) / l * 11, (hx - gx) / l * 11
        gate += (f'<path d="M{gx - nx:.1f} {gy - ny:.1f}L{gx + nx:.1f} {gy + ny:.1f}" stroke="{c["rose"]}" '
                 f'stroke-opacity="{min(1.0, _fade(lap + 0.25 - up) * 1.6) * 0.8:.2f}" stroke-width="4"/>')
    return (f'<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<defs><radialGradient id="st-g" cx="31%" cy="29%" r="80%"><stop offset="0" stop-color="{c["a"]}"/>'
            f'<stop offset=".46" stop-color="{c["m"]}"/><stop offset="1" stop-color="{c["b"]}"/></radialGradient>'
            f'<radialGradient id="st-h" cx="50%" cy="50%" r="50%"><stop offset=".62" stop-color="{c["air"]}" stop-opacity=".0"/>'
            f'<stop offset=".7" stop-color="{c["air"]}" stop-opacity=".26"/><stop offset="1" stop-color="{c["air"]}" stop-opacity="0"/>'
            f'</radialGradient></defs>'
            f'<circle cx="{CX}" cy="{CY}" r="{R * 1.45:.0f}" fill="url(#st-h)"/>'
            f'<g fill="none" stroke-linecap="round">{_track(up, False, c)}</g>'
            f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#st-g)" stroke="{c["air"]}" stroke-opacity=".5" stroke-width="1.5"/>'
            f'{"".join(dots)}<g fill="none" stroke-linecap="round">{_track(up, True, c)}{gate}{trail}</g>{plane}</svg>')
