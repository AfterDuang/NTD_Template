from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT_IMAGE = ROOT / "Art" / "Sprites" / "ModernOffice25DTileSheet.png"
OUT_PREVIEW = ROOT / "Art" / "Sprites" / "ModernOffice25DMapPreview.png"
OUT_TILESET = ROOT / "Art" / "ModernOffice25DTileMap.tres"

TILE = 32
COLS = 16
ROWS = 12


C = {
    "clear": (0, 0, 0, 0),
    "ink": (16, 18, 20, 255),
    "shadow": (0, 0, 0, 86),
    "shadow_soft": (0, 0, 0, 38),
    "carpet": (42, 42, 51, 255),
    "carpet_2": (50, 49, 59, 255),
    "carpet_hi": (68, 67, 78, 255),
    "tile": (88, 85, 78, 255),
    "tile_hi": (119, 114, 103, 255),
    "tile_lo": (65, 63, 59, 255),
    "wood": (92, 58, 35, 255),
    "wood_hi": (126, 81, 48, 255),
    "wood_lo": (60, 39, 28, 255),
    "concrete": (69, 70, 67, 255),
    "wall_top": (202, 196, 180, 255),
    "wall_mid": (153, 147, 134, 255),
    "wall_low": (102, 99, 95, 255),
    "wall_dirty": (117, 110, 102, 255),
    "metal": (72, 80, 83, 255),
    "metal_hi": (133, 143, 143, 255),
    "metal_lo": (39, 45, 49, 255),
    "glass": (75, 123, 137, 140),
    "glass_hi": (155, 222, 230, 210),
    "desk": (83, 57, 40, 255),
    "desk_hi": (127, 88, 58, 255),
    "desk_lo": (47, 34, 29, 255),
    "screen": (31, 79, 86, 255),
    "screen_hi": (72, 172, 181, 255),
    "paper": (207, 208, 197, 255),
    "yellow": (226, 181, 74, 255),
    "red": (138, 42, 39, 255),
    "green": (59, 122, 73, 255),
    "green_lo": (35, 74, 47, 255),
    "water": (82, 148, 165, 255),
}


def img():
    return Image.new("RGBA", (COLS * TILE, ROWS * TILE), C["clear"])


def at(x, y):
    return x * TILE, y * TILE


def rect(d, x, y, box, fill, outline=None):
    ox, oy = at(x, y)
    d.rectangle((ox + box[0], oy + box[1], ox + box[2], oy + box[3]), fill=fill, outline=outline)


def line(d, x, y, coords, fill, width=1):
    ox, oy = at(x, y)
    d.line((ox + coords[0], oy + coords[1], ox + coords[2], oy + coords[3]), fill=fill, width=width)


def pts(d, x, y, points, fill):
    ox, oy = at(x, y)
    for px, py in points:
        d.point((ox + px, oy + py), fill=fill)


def poly(d, x, y, points, fill, outline=None):
    ox, oy = at(x, y)
    p = [(ox + px, oy + py) for px, py in points]
    d.polygon(p, fill=fill, outline=outline)


def base_floor(d, x, y, color):
    rect(d, x, y, (0, 0, 31, 31), color)


def floor_carpet(d, x, y, v=0):
    base_floor(d, x, y, C["carpet"] if v != 1 else C["carpet_2"])
    if v == 1:
        rect(d, x, y, (0, 15, 31, 16), C["carpet"])
        rect(d, x, y, (15, 0, 16, 31), C["carpet"])
    elif v == 2:
        line(d, x, y, (2, 29, 29, 2), C["carpet_hi"])
        line(d, x, y, (0, 18, 18, 0), (33, 33, 41, 255))
    elif v == 3:
        for xx in range(4, 32, 8):
            line(d, x, y, (xx, 2, xx, 29), (35, 35, 43, 255))
    pts(d, x, y, [(6, 6), (19, 9), (25, 22), (11, 25)], C["carpet_hi"])


def floor_tile(d, x, y, v=0):
    base_floor(d, x, y, C["tile"])
    if v == 0:
        for p in [15]:
            rect(d, x, y, (p, 0, p + 1, 31), C["tile_lo"])
            rect(d, x, y, (0, p, 31, p + 1), C["tile_lo"])
        rect(d, x, y, (1, 1, 14, 14), C["tile_hi"])
        rect(d, x, y, (17, 17, 30, 30), (76, 73, 67, 255))
    elif v == 1:
        for yy in (7, 15, 23):
            line(d, x, y, (1, yy, 30, yy), C["tile_lo"])
        pts(d, x, y, [(7, 4), (21, 12), (12, 25), (27, 29)], C["tile_hi"])


def floor_wood(d, x, y):
    base_floor(d, x, y, C["wood"])
    for yy in (7, 15, 23):
        line(d, x, y, (0, yy, 31, yy), C["wood_lo"])
    for sx, sy in [(4, 4), (18, 9), (9, 18), (23, 25)]:
        line(d, x, y, (sx, sy, min(31, sx + 7), sy), C["wood_hi"])


def floor_concrete(d, x, y):
    base_floor(d, x, y, C["concrete"])
    pts(d, x, y, [(5, 8), (6, 8), (18, 7), (24, 16), (10, 24), (27, 27)], (91, 92, 88, 255))
    line(d, x, y, (6, 24, 14, 20), (49, 50, 49, 255))
    line(d, x, y, (20, 9, 27, 13), (49, 50, 49, 255))


def wall_h(d, x, y, left=False, right=False):
    rect(d, x, y, (0, 5, 31, 11), C["wall_top"], C["ink"])
    rect(d, x, y, (0, 12, 31, 27), C["wall_mid"], C["ink"])
    rect(d, x, y, (0, 24, 31, 27), C["wall_low"])
    rect(d, x, y, (0, 28, 31, 31), C["shadow"])
    line(d, x, y, (2, 14, 29, 14), C["wall_dirty"])
    pts(d, x, y, [(8, 20), (19, 17), (25, 23)], C["wall_low"])
    if left:
        rect(d, x, y, (0, 5, 4, 27), C["wall_low"], C["ink"])
    if right:
        rect(d, x, y, (27, 5, 31, 27), C["wall_low"], C["ink"])


def wall_v(d, x, y, side="left"):
    x0, x1 = (4, 15) if side == "left" else (16, 27)
    rect(d, x, y, (x0, 0, x1, 31), C["wall_mid"], C["ink"])
    rect(d, x, y, (x0, 0, x1, 5), C["wall_top"], C["ink"])
    if side == "left":
        rect(d, x, y, (16, 0, 20, 31), C["shadow_soft"])
        line(d, x, y, (14, 6, 14, 29), C["wall_low"])
    else:
        rect(d, x, y, (11, 0, 15, 31), C["shadow_soft"])
        line(d, x, y, (17, 6, 17, 29), C["wall_low"])
    pts(d, x, y, [(x0 + 3, 11), (x0 + 8, 22)], C["wall_low"])


def wall_corner(d, x, y, kind=0):
    wall_h(d, x, y)
    wall_v(d, x, y, "left" if kind in (0, 2) else "right")
    rect(d, x, y, (5, 5, 26, 11), C["wall_top"], C["ink"])


def glass_h(d, x, y):
    rect(d, x, y, (0, 8, 31, 12), C["metal"], C["ink"])
    rect(d, x, y, (0, 13, 31, 25), C["glass"], C["metal_lo"])
    rect(d, x, y, (0, 26, 31, 28), C["metal_lo"])
    line(d, x, y, (2, 17, 29, 17), C["glass_hi"])
    for xx in (10, 21):
        line(d, x, y, (xx, 13, xx, 25), C["metal"])
    rect(d, x, y, (0, 29, 31, 31), C["shadow_soft"])


def glass_v(d, x, y):
    rect(d, x, y, (9, 0, 13, 31), C["metal"], C["ink"])
    rect(d, x, y, (14, 0, 25, 31), C["glass"], C["metal_lo"])
    rect(d, x, y, (26, 0, 28, 31), C["metal_lo"])
    line(d, x, y, (18, 2, 18, 29), C["glass_hi"])
    for yy in (10, 21):
        line(d, x, y, (14, yy, 25, yy), C["metal"])
    rect(d, x, y, (29, 0, 31, 31), C["shadow_soft"])


def door(d, x, y):
    rect(d, x, y, (5, 2, 26, 31), C["desk_lo"], C["ink"])
    rect(d, x, y, (7, 4, 24, 29), C["desk"])
    rect(d, x, y, (7, 4, 24, 7), C["desk_hi"])
    rect(d, x, y, (20, 16, 22, 18), C["yellow"])
    line(d, x, y, (9, 11, 22, 11), C["desk_lo"])
    line(d, x, y, (9, 23, 22, 23), C["desk_lo"])


def window(d, x, y):
    wall_h(d, x, y)
    rect(d, x, y, (4, 7, 27, 23), (55, 99, 111, 255), C["ink"])
    rect(d, x, y, (6, 9, 14, 21), (120, 208, 222, 255))
    rect(d, x, y, (17, 9, 25, 21), (120, 208, 222, 255))
    line(d, x, y, (7, 19, 14, 10), (218, 248, 250, 255))
    line(d, x, y, (18, 19, 25, 10), (218, 248, 250, 255))
    line(d, x, y, (15, 7, 15, 23), C["metal_hi"])


def object_shadow(d, x, y, box=(4, 25, 28, 30)):
    rect(d, x, y, box, C["shadow_soft"])


def desk(d, x, y, chair=False):
    object_shadow(d, x, y)
    rect(d, x, y, (3, 9, 28, 22), C["desk"], C["ink"])
    rect(d, x, y, (4, 10, 27, 13), C["desk_hi"])
    rect(d, x, y, (7, 13, 16, 19), C["screen"], C["metal_lo"])
    rect(d, x, y, (8, 14, 15, 15), C["screen_hi"])
    rect(d, x, y, (20, 13, 26, 18), C["paper"])
    if chair:
        rect(d, x, y, (10, 24, 21, 30), C["metal_lo"], C["ink"])
        rect(d, x, y, (12, 23, 19, 27), C["metal"])


def cubicle(d, x, y):
    rect(d, x, y, (0, 4, 31, 8), C["metal"], C["ink"])
    rect(d, x, y, (0, 4, 4, 31), C["metal"], C["ink"])
    rect(d, x, y, (5, 27, 30, 30), C["shadow_soft"])
    rect(d, x, y, (10, 12, 29, 22), C["desk"], C["ink"])
    rect(d, x, y, (14, 14, 22, 18), C["screen"], C["metal_lo"])
    rect(d, x, y, (24, 14, 28, 19), C["paper"])


def meeting_table(d, x, y):
    object_shadow(d, x, y, (3, 24, 29, 30))
    rect(d, x, y, (5, 8, 27, 22), C["desk"], C["ink"])
    rect(d, x, y, (8, 10, 24, 13), C["desk_hi"])
    for xx, yy in [(3, 4), (14, 4), (25, 4), (3, 24), (14, 24), (25, 24)]:
        rect(d, x, y, (xx, yy, xx + 4, yy + 5), C["metal_lo"], C["ink"])
    rect(d, x, y, (14, 15, 18, 18), C["water"])


def shelf(d, x, y):
    object_shadow(d, x, y)
    rect(d, x, y, (5, 3, 26, 29), C["metal_lo"], C["ink"])
    for yy in (8, 15, 22):
        line(d, x, y, (6, yy, 25, yy), C["metal_hi"])
    for xx, yy, col in [(8, 5, C["red"]), (14, 5, C["paper"]), (21, 5, C["yellow"]), (10, 17, C["paper"]), (18, 23, C["red"])]:
        rect(d, x, y, (xx, yy, xx + 4, yy + 5), col)


def cabinet(d, x, y):
    object_shadow(d, x, y)
    for xx in (3, 13, 23):
        rect(d, x, y, (xx, 7, xx + 7, 27), C["metal"], C["ink"])
        rect(d, x, y, (xx + 1, 9, xx + 6, 14), C["metal_hi"])
        rect(d, x, y, (xx + 3, 19, xx + 5, 20), C["yellow"])


def plant(d, x, y):
    object_shadow(d, x, y, (8, 24, 24, 29))
    rect(d, x, y, (12, 21, 20, 28), C["desk_lo"], C["ink"])
    rect(d, x, y, (10, 17, 22, 22), C["desk"], C["ink"])
    for box in [(15, 8, 18, 17), (9, 12, 15, 19), (18, 12, 24, 19), (13, 5, 20, 10)]:
        rect(d, x, y, box, C["green"], C["green_lo"])


def vending(d, x, y):
    object_shadow(d, x, y)
    rect(d, x, y, (6, 2, 26, 30), (33, 52, 82, 255), C["ink"])
    rect(d, x, y, (8, 4, 24, 14), C["screen"], C["metal_lo"])
    for xx, col in [(9, C["red"]), (15, C["yellow"]), (21, C["water"])]:
        rect(d, x, y, (xx, 17, xx + 3, 22), col)
    rect(d, x, y, (9, 25, 23, 27), C["metal_hi"])


def server(d, x, y):
    object_shadow(d, x, y)
    rect(d, x, y, (6, 1, 26, 31), C["metal_lo"], C["ink"])
    for yy in (4, 10, 16, 22):
        rect(d, x, y, (8, yy, 24, yy + 3), C["metal"])
        pts(d, x, y, [(10, yy + 1), (14, yy + 1), (20, yy + 1)], C["screen_hi"])
    rect(d, x, y, (8, 27, 24, 29), C["ink"])


def cooler(d, x, y):
    object_shadow(d, x, y, (10, 26, 23, 30))
    rect(d, x, y, (12, 10, 21, 29), C["metal_hi"], C["ink"])
    rect(d, x, y, (11, 4, 22, 13), C["water"], C["ink"])
    rect(d, x, y, (14, 15, 19, 18), C["screen"])


def copier(d, x, y):
    object_shadow(d, x, y)
    rect(d, x, y, (5, 12, 27, 27), C["metal_hi"], C["ink"])
    rect(d, x, y, (8, 7, 24, 13), C["metal"], C["ink"])
    rect(d, x, y, (10, 4, 22, 7), C["paper"], C["ink"])
    rect(d, x, y, (21, 15, 25, 18), C["screen"])


def trash(d, x, y):
    object_shadow(d, x, y, (11, 24, 22, 29))
    rect(d, x, y, (11, 12, 22, 27), C["metal"], C["ink"])
    rect(d, x, y, (10, 10, 23, 13), C["metal_hi"], C["ink"])
    pts(d, x, y, [(8, 8), (24, 10), (15, 6)], C["paper"])


def lamp(d, x, y):
    rect(d, x, y, (10, 5, 22, 10), (235, 198, 99, 255), C["yellow"])
    rect(d, x, y, (7, 11, 25, 13), (235, 198, 99, 90))
    rect(d, x, y, (4, 14, 28, 16), (235, 198, 99, 38))


def debris(d, x, y):
    pts(d, x, y, [(8, 18), (9, 18), (10, 19), (21, 13), (22, 14), (18, 24), (5, 9)], C["paper"])
    rect(d, x, y, (13, 14, 17, 17), C["wall_low"], C["ink"])
    line(d, x, y, (20, 22, 27, 28), C["red"])
    line(d, x, y, (21, 23, 24, 28), C["red"])


def chair(d, x, y):
    object_shadow(d, x, y, (9, 22, 23, 29))
    rect(d, x, y, (10, 11, 22, 18), C["metal_lo"], C["ink"])
    rect(d, x, y, (12, 18, 20, 25), C["metal"], C["ink"])
    line(d, x, y, (12, 25, 9, 29), C["metal_lo"])
    line(d, x, y, (20, 25, 23, 29), C["metal_lo"])


def sign(d, x, y):
    rect(d, x, y, (5, 8, 27, 20), C["metal_lo"], C["ink"])
    rect(d, x, y, (7, 10, 25, 18), C["screen"], C["metal"])
    rect(d, x, y, (9, 12, 13, 14), C["yellow"])
    rect(d, x, y, (16, 12, 23, 14), C["paper"])


def side_desk(d, x, y):
    object_shadow(d, x, y, (8, 24, 24, 30))
    rect(d, x, y, (8, 5, 23, 27), C["desk"], C["ink"])
    rect(d, x, y, (9, 6, 13, 26), C["desk_hi"])
    rect(d, x, y, (13, 9, 20, 18), C["screen"], C["metal_lo"])
    rect(d, x, y, (14, 10, 17, 17), C["screen_hi"])
    rect(d, x, y, (14, 20, 20, 25), C["paper"])


def reception(d, x, y):
    object_shadow(d, x, y, (2, 24, 30, 30))
    rect(d, x, y, (2, 13, 29, 27), C["desk_lo"], C["ink"])
    rect(d, x, y, (4, 10, 27, 18), C["desk"], C["ink"])
    rect(d, x, y, (7, 11, 14, 15), C["screen"], C["metal_lo"])
    rect(d, x, y, (19, 11, 25, 16), C["paper"])
    rect(d, x, y, (4, 24, 27, 26), C["desk_hi"])


def sofa(d, x, y):
    object_shadow(d, x, y, (3, 23, 29, 30))
    rect(d, x, y, (5, 11, 27, 24), (43, 67, 80, 255), C["ink"])
    rect(d, x, y, (3, 15, 8, 25), (34, 54, 65, 255), C["ink"])
    rect(d, x, y, (24, 15, 29, 25), (34, 54, 65, 255), C["ink"])
    line(d, x, y, (15, 12, 15, 23), C["metal_lo"])


def coffee_table(d, x, y):
    object_shadow(d, x, y, (6, 22, 26, 28))
    rect(d, x, y, (7, 12, 25, 23), C["desk"], C["ink"])
    rect(d, x, y, (9, 14, 23, 16), C["desk_hi"])
    rect(d, x, y, (13, 17, 18, 19), C["paper"])
    rect(d, x, y, (20, 17, 22, 20), C["water"])


def whiteboard(d, x, y):
    rect(d, x, y, (3, 7, 28, 22), C["paper"], C["ink"])
    rect(d, x, y, (3, 22, 28, 24), C["metal"])
    line(d, x, y, (7, 12, 14, 12), C["screen"])
    line(d, x, y, (8, 16, 23, 16), C["red"])
    pts(d, x, y, [(20, 11), (21, 11), (22, 12)], C["yellow"])


def lockers(d, x, y):
    object_shadow(d, x, y)
    for xx in (4, 12, 20):
        rect(d, x, y, (xx, 5, xx + 7, 28), C["metal"], C["ink"])
        rect(d, x, y, (xx + 2, 9, xx + 5, 10), C["metal_hi"])
        rect(d, x, y, (xx + 5, 17, xx + 6, 18), C["yellow"])


def boxes(d, x, y):
    object_shadow(d, x, y, (6, 22, 27, 29))
    rect(d, x, y, (7, 15, 18, 27), (118, 78, 42, 255), C["ink"])
    rect(d, x, y, (16, 10, 26, 22), (100, 67, 39, 255), C["ink"])
    line(d, x, y, (9, 17, 16, 17), C["desk_hi"])
    line(d, x, y, (18, 12, 24, 12), C["desk_hi"])


def cables(d, x, y):
    line(d, x, y, (4, 24, 11, 21), C["ink"], 2)
    line(d, x, y, (11, 21, 18, 26), C["ink"], 2)
    line(d, x, y, (18, 26, 27, 18), C["ink"], 2)
    rect(d, x, y, (24, 15, 28, 19), C["metal"], C["ink"])
    pts(d, x, y, [(7, 10), (14, 13), (20, 9)], C["paper"])


def paper_pile(d, x, y):
    rect(d, x, y, (8, 15, 18, 21), C["paper"], C["ink"])
    rect(d, x, y, (12, 11, 23, 17), (185, 187, 178, 255), C["ink"])
    rect(d, x, y, (6, 22, 14, 25), C["paper"], C["ink"])
    line(d, x, y, (14, 13, 20, 13), C["metal"])
    line(d, x, y, (10, 17, 16, 17), C["metal"])


def blood_smear(d, x, y):
    rect(d, x, y, (12, 18, 19, 23), C["red"])
    rect(d, x, y, (18, 21, 25, 25), (105, 29, 31, 255))
    pts(d, x, y, [(8, 15), (23, 16), (27, 24), (14, 27), (6, 23)], C["red"])


def broken_glass(d, x, y):
    for a, b in [((8, 9), (14, 18)), ((14, 18), (22, 12)), ((17, 7), (17, 24)), ((7, 23), (24, 23))]:
        line(d, x, y, (a[0], a[1], b[0], b[1]), C["glass_hi"])
    pts(d, x, y, [(5, 18), (25, 9), (23, 27), (12, 25)], C["glass"])


def vent(d, x, y):
    rect(d, x, y, (5, 11, 27, 22), C["metal_lo"], C["ink"])
    for xx in range(8, 25, 4):
        line(d, x, y, (xx, 13, xx, 20), C["metal_hi"])


def rug(d, x, y):
    rect(d, x, y, (3, 8, 28, 25), (62, 37, 45, 255), C["ink"])
    rect(d, x, y, (6, 11, 25, 22), (87, 47, 53, 255))
    line(d, x, y, (8, 15, 23, 15), C["yellow"])
    line(d, x, y, (8, 18, 23, 18), C["yellow"])


def kitchen_counter(d, x, y):
    object_shadow(d, x, y)
    rect(d, x, y, (3, 9, 29, 25), C["metal"], C["ink"])
    rect(d, x, y, (4, 9, 28, 13), C["metal_hi"])
    rect(d, x, y, (8, 14, 15, 20), C["water"], C["ink"])
    rect(d, x, y, (20, 14, 26, 19), C["screen"], C["ink"])


def microwave(d, x, y):
    object_shadow(d, x, y, (8, 22, 25, 28))
    rect(d, x, y, (7, 10, 25, 23), C["metal"], C["ink"])
    rect(d, x, y, (9, 12, 18, 20), C["screen"], C["metal_lo"])
    rect(d, x, y, (21, 13, 23, 15), C["yellow"])
    rect(d, x, y, (21, 17, 23, 19), C["red"])


def plant_large(d, x, y):
    object_shadow(d, x, y, (6, 25, 26, 30))
    rect(d, x, y, (11, 21, 21, 29), C["desk"], C["ink"])
    for box in [(13, 5, 18, 19), (7, 10, 15, 20), (17, 9, 25, 20), (10, 3, 23, 10)]:
        rect(d, x, y, box, C["green"], C["green_lo"])


def monitor_bank(d, x, y):
    object_shadow(d, x, y)
    for xx in (3, 12, 21):
        rect(d, x, y, (xx, 9, xx + 8, 17), C["screen"], C["ink"])
        rect(d, x, y, (xx + 1, 10, xx + 7, 12), C["screen_hi"])
        line(d, x, y, (xx + 4, 17, xx + 4, 21), C["metal"])
    rect(d, x, y, (5, 22, 26, 25), C["desk"], C["ink"])


def draw_atlas():
    sheet = img()
    d = ImageDraw.Draw(sheet, "RGBA")
    funcs = {}

    floors = [
        lambda: floor_carpet(d, 0, 0, 0),
        lambda: floor_carpet(d, 1, 0, 1),
        lambda: floor_carpet(d, 2, 0, 2),
        lambda: floor_carpet(d, 3, 0, 3),
        lambda: floor_tile(d, 4, 0, 0),
        lambda: floor_tile(d, 5, 0, 1),
        lambda: floor_wood(d, 6, 0),
        lambda: floor_concrete(d, 7, 0),
    ]
    for fn in floors:
        fn()
    # Extra damaged/dark floor variants.
    floor_concrete(d, 8, 0)
    line(d, 8, 0, (7, 23, 16, 18), (42, 43, 42, 255))
    floor_carpet(d, 9, 0, 0)
    debris(d, 9, 0)
    floor_tile(d, 10, 0, 0)
    debris(d, 10, 0)
    floor_wood(d, 11, 0)
    floor_carpet(d, 12, 0, 0)
    floor_tile(d, 13, 0, 1)
    floor_concrete(d, 14, 0)
    floor_carpet(d, 15, 0, 1)

    wall_draws = [
        lambda: wall_h(d, 0, 1),
        lambda: wall_h(d, 1, 1, left=True),
        lambda: wall_h(d, 2, 1, right=True),
        lambda: wall_corner(d, 3, 1, 0),
        lambda: wall_v(d, 4, 1, "left"),
        lambda: wall_v(d, 5, 1, "right"),
        lambda: glass_h(d, 6, 1),
        lambda: glass_v(d, 7, 1),
        lambda: door(d, 8, 1),
        lambda: window(d, 9, 1),
    ]
    for fn in wall_draws:
        fn()
    for x in range(10, 16):
        wall_h(d, x, 1)
        if x in (12, 14):
            rect(d, x, 1, (8, 16, 23, 20), C["wall_dirty"])

    prop_funcs = [
        desk, lambda dd, x, y: desk(dd, x, y, True), cubicle, meeting_table,
        shelf, cabinet, plant, vending, server, cooler, copier, trash,
        lamp, debris, chair, sign,
        side_desk, reception, sofa, coffee_table, whiteboard, lockers, boxes, cables,
        paper_pile, blood_smear, broken_glass, vent, rug, kitchen_counter, microwave, plant_large,
        monitor_bank, lambda dd, x, y: desk(dd, x, y, False), lambda dd, x, y: desk(dd, x, y, True), cubicle,
        meeting_table, shelf, cabinet, vending, server, cooler, copier, trash,
        plant, plant_large, boxes, cables, paper_pile, blood_smear,
        broken_glass, vent, rug, kitchen_counter, microwave, monitor_bank,
    ]
    for row in range(2, 12):
        for col in range(16):
            fn = prop_funcs[(row - 2) * 16 + col] if (row - 2) * 16 + col < len(prop_funcs) else None
            if fn:
                fn(d, col, row)

    OUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT_IMAGE)
    draw_preview(sheet)


def tile(sheet, tx, ty):
    return sheet.crop((tx * TILE, ty * TILE, tx * TILE + TILE, ty * TILE + TILE))


def draw_preview(sheet):
    w, h = 28, 18
    out = Image.new("RGBA", (w * TILE, h * TILE), (0, 0, 0, 255))

    def paste(tx, ty, gx, gy):
        out.alpha_composite(tile(sheet, tx, ty), (gx * TILE, gy * TILE))

    def fill(x0, y0, x1, y1, tx, ty):
        for gy in range(y0, y1 + 1):
            for gx in range(x0, x1 + 1):
                paste(tx, ty, gx, gy)

    # Base layer: rooms and corridor.
    fill(2, 7, 25, 10, 4, 0)
    fill(4, 3, 11, 6, 0, 0)
    fill(14, 3, 23, 6, 0, 0)
    fill(5, 11, 13, 15, 7, 0)
    fill(17, 11, 23, 15, 6, 0)

    # Wall layer, transparent over floors.
    for gx in range(4, 12):
        paste(0, 1, gx, 2)
        paste(0, 1, gx, 6)
    for gx in range(14, 24):
        paste(0, 1, gx, 2)
        paste(0, 1, gx, 6)
    for gx in range(5, 14):
        paste(0, 1, gx, 10)
        paste(0, 1, gx, 15)
    for gx in range(17, 24):
        paste(0, 1, gx, 10)
        paste(0, 1, gx, 15)
    for gy in range(3, 7):
        paste(4, 1, 3, gy)
        paste(5, 1, 12, gy)
        paste(4, 1, 13, gy)
        paste(5, 1, 24, gy)
    for gy in range(11, 16):
        paste(4, 1, 4, gy)
        paste(5, 1, 14, gy)
        paste(4, 1, 16, gy)
        paste(5, 1, 24, gy)

    for gx in (6, 7, 17, 18, 19):
        paste(6, 1, gx, 2)
    paste(8, 1, 8, 6)
    paste(8, 1, 18, 6)
    paste(8, 1, 9, 10)
    paste(9, 1, 21, 2)

    # Props layer, transparent over floor/walls.
    for gx, gy in [(5, 4), (9, 4), (5, 5), (9, 5)]:
        paste(2, 2, gx, gy)
    paste(6, 2, 11, 4)
    paste(4, 2, 11, 5)
    for gx, gy in [(16, 4), (20, 4)]:
        paste(3, 2, gx, gy)
    paste(6, 2, 14, 5)
    paste(5, 2, 23, 5)
    paste(8, 2, 6, 12)
    paste(10, 2, 8, 12)
    paste(9, 2, 12, 13)
    paste(7, 2, 18, 12)
    paste(11, 2, 22, 14)
    for gx, gy in [(4, 8), (9, 8), (15, 8), (20, 8), (24, 8)]:
        paste(12, 2, gx, gy)
    for gx, gy in [(3, 10), (12, 9), (25, 10), (19, 10)]:
        paste(13, 2, gx, gy)
    for gx, gy in [(2, 7), (25, 10)]:
        paste(9, 2, gx, gy)

    out.save(OUT_PREVIEW)


def write_tileset():
    # Full-tile collision is intentionally simple. Floors are passable; walls and large props block.
    blocking = set()
    blocking.update((x, 1) for x in range(16))
    blocking.update((x, 2) for x in range(0, 12))
    blocking.update([(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (7, 3), (8, 3), (9, 3), (10, 3)])

    entries = []
    for y in range(ROWS):
        for x in range(COLS):
            entries.append(f"{x}:{y}/0 = 0")
            if (x, y) in blocking:
                entries.append(
                    f"{x}:{y}/0/physics_layer_0/polygon_0/points = "
                    "PackedVector2Array(-16, -16, 16, -16, 16, 16, -16, 16)"
                )

    atlas_entries = "\n".join(entries)
    text = f"""[gd_resource type="TileSet" load_steps=3 format=3]

[ext_resource type="Texture2D" path="res://Art/Sprites/ModernOffice25DTileSheet.png" id="1_office25d"]

[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_office25d"]
texture = ExtResource("1_office25d")
texture_region_size = Vector2i(32, 32)
{atlas_entries}

[resource]
tile_size = Vector2i(32, 32)
physics_layer_0/collision_layer = 1
sources/0 = SubResource("TileSetAtlasSource_office25d")
"""
    OUT_TILESET.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    draw_atlas()
    write_tileset()
    print(f"Wrote {OUT_IMAGE.relative_to(ROOT)}")
    print(f"Wrote {OUT_PREVIEW.relative_to(ROOT)}")
    print(f"Wrote {OUT_TILESET.relative_to(ROOT)}")
