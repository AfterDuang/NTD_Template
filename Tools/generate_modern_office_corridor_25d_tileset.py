from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT_IMAGE = ROOT / "Art" / "Sprites" / "ModernOfficeCorridor25D_TileSheet.png"
OUT_PREVIEW = ROOT / "Art" / "Sprites" / "ModernOfficeCorridor25D_Preview.png"
OUT_TILESET = ROOT / "Art" / "ModernOfficeCorridor25D_TileMap.tres"

TILE = 32
COLS = 16
ROWS = 10


P = {
    "clear": (0, 0, 0, 0),
    "black": (8, 7, 6, 255),
    "ink": (31, 28, 25, 255),
    "shadow": (0, 0, 0, 118),
    "soft_shadow": (0, 0, 0, 48),
    "floor": (47, 39, 36, 255),
    "floor2": (55, 46, 42, 255),
    "floor_hi": (67, 58, 53, 255),
    "floor_lo": (34, 28, 27, 255),
    "tile": (73, 68, 61, 255),
    "tile_hi": (98, 92, 80, 255),
    "tile_lo": (52, 48, 44, 255),
    "wall_top": (154, 146, 126, 255),
    "wall_top_hi": (196, 188, 162, 255),
    "wall_face": (119, 111, 96, 255),
    "wall_face2": (93, 87, 78, 255),
    "wall_dark": (55, 50, 43, 255),
    "mortar": (83, 78, 69, 255),
    "trim": (177, 169, 143, 255),
    "door": (74, 45, 29, 255),
    "door_hi": (111, 72, 45, 255),
    "glass": (69, 116, 123, 160),
    "glass_hi": (139, 204, 207, 220),
    "metal": (72, 74, 70, 255),
    "metal_hi": (126, 127, 119, 255),
    "metal_lo": (41, 39, 36, 255),
    "desk": (72, 48, 35, 255),
    "desk_hi": (108, 75, 49, 255),
    "desk_lo": (42, 29, 24, 255),
    "screen": (32, 75, 76, 255),
    "screen_hi": (71, 145, 141, 255),
    "paper": (190, 190, 176, 255),
    "lamp": (222, 180, 83, 255),
    "red": (137, 33, 34, 255),
    "green": (55, 105, 62, 255),
    "green_lo": (33, 66, 41, 255),
    "water": (70, 134, 145, 255),
}


def new_sheet():
    return Image.new("RGBA", (COLS * TILE, ROWS * TILE), P["clear"])


def off(x, y):
    return x * TILE, y * TILE


def rect(d, x, y, box, fill, outline=None):
    ox, oy = off(x, y)
    d.rectangle((ox + box[0], oy + box[1], ox + box[2], oy + box[3]), fill=fill, outline=outline)


def line(d, x, y, xy, fill, width=1):
    ox, oy = off(x, y)
    d.line((ox + xy[0], oy + xy[1], ox + xy[2], oy + xy[3]), fill=fill, width=width)


def pts(d, x, y, ps, fill):
    ox, oy = off(x, y)
    for px, py in ps:
        d.point((ox + px, oy + py), fill=fill)


def poly(d, x, y, ps, fill, outline=None):
    ox, oy = off(x, y)
    d.polygon([(ox + px, oy + py) for px, py in ps], fill=fill, outline=outline)


def floor(d, x, y, variant=0):
    color = P["floor"] if variant != 1 else P["floor2"]
    rect(d, x, y, (0, 0, 31, 31), color)
    if variant == 1:
        line(d, x, y, (0, 15, 31, 15), (42, 35, 33, 255))
        line(d, x, y, (15, 0, 15, 31), (42, 35, 33, 255))
    elif variant == 2:
        line(d, x, y, (8, 24, 18, 19), P["floor_lo"])
        line(d, x, y, (20, 10, 26, 13), P["floor_hi"])
    elif variant == 3:
        for xx in (7, 16, 25):
            line(d, x, y, (xx, 3, xx, 28), (38, 32, 30, 255))
    pts(d, x, y, [(8, 8), (17, 11), (25, 18), (9, 24), (21, 27)], P["floor_hi"])
    pts(d, x, y, [(6, 18), (14, 5), (28, 22)], P["floor_lo"])


def lobby_tile(d, x, y, variant=0):
    rect(d, x, y, (0, 0, 31, 31), P["tile"])
    for gx in (15,):
        line(d, x, y, (gx, 0, gx, 31), P["tile_lo"])
        line(d, x, y, (0, gx, 31, gx), P["tile_lo"])
    if variant:
        rect(d, x, y, (2, 2, 13, 13), P["tile_hi"])
        rect(d, x, y, (17, 17, 30, 30), (70, 70, 66, 255))
    pts(d, x, y, [(7, 25), (24, 8), (25, 9), (11, 12)], P["tile_hi"])
    pts(d, x, y, [(4, 18), (21, 27)], P["tile_lo"])


def wall_bricks(d, x, y, y0, y1):
    rect(d, x, y, (0, y0, 31, y1), P["wall_face"])
    # Reference style is more like stained plaster/concrete than crisp brick.
    line(d, x, y, (0, y0 + 6, 31, y0 + 6), P["mortar"])
    line(d, x, y, (0, y0 + 13, 31, y0 + 13), (91, 85, 75, 255))
    for xx in (9, 21):
        line(d, x, y, (xx, y0 + 1, xx, min(y1, y0 + 6)), (89, 84, 75, 255))
    pts(d, x, y, [(5, y0 + 4), (14, y0 + 10), (26, y0 + 3), (22, y0 + 16)], P["wall_face2"])
    pts(d, x, y, [(8, y0 + 2), (18, y0 + 8), (28, y0 + 12)], (143, 134, 113, 255))


def north_wall(d, x, y, left=False, right=False, light=False):
    # This is the key 2.5D tile: top cap, visible front face, bottom trim and cast shadow.
    rect(d, x, y, (0, 2, 31, 7), P["wall_dark"], P["ink"])
    rect(d, x, y, (0, 8, 31, 12), P["wall_top"], P["ink"])
    rect(d, x, y, (1, 9, 30, 10), P["wall_top_hi"])
    wall_bricks(d, x, y, 13, 24)
    rect(d, x, y, (0, 24, 31, 27), P["trim"], P["ink"])
    rect(d, x, y, (0, 28, 31, 31), P["shadow"])
    if left:
        rect(d, x, y, (0, 2, 5, 27), P["wall_dark"], P["ink"])
    if right:
        rect(d, x, y, (26, 2, 31, 27), P["wall_dark"], P["ink"])
    if light:
        rect(d, x, y, (15, 11, 17, 13), P["lamp"])
        rect(d, x, y, (8, 14, 24, 16), (236, 198, 86, 75))
        rect(d, x, y, (4, 17, 28, 19), (236, 198, 86, 32))


def south_edge(d, x, y, drips=False):
    # South edge is seen as a foreground lip.
    rect(d, x, y, (0, 0, 31, 3), P["shadow"])
    rect(d, x, y, (0, 4, 31, 8), P["trim"], P["ink"])
    wall_bricks(d, x, y, 9, 18)
    rect(d, x, y, (0, 19, 31, 22), P["wall_dark"], P["ink"])
    rect(d, x, y, (0, 23, 31, 25), P["shadow"])
    if drips:
        for xx, ln in [(5, 8), (12, 5), (19, 9), (25, 6)]:
            line(d, x, y, (xx, 24, xx, min(31, 24 + ln)), P["wall_dark"])


def west_wall(d, x, y):
    rect(d, x, y, (0, 0, 5, 31), P["wall_dark"], P["ink"])
    rect(d, x, y, (6, 0, 13, 31), P["wall_face"], P["ink"])
    rect(d, x, y, (14, 0, 17, 31), P["shadow"])
    for yy in range(6, 31, 8):
        line(d, x, y, (6, yy, 13, yy), P["mortar"])


def east_wall(d, x, y):
    rect(d, x, y, (26, 0, 31, 31), P["wall_dark"], P["ink"])
    rect(d, x, y, (18, 0, 25, 31), P["wall_face"], P["ink"])
    rect(d, x, y, (14, 0, 17, 31), P["shadow"])
    for yy in range(6, 31, 8):
        line(d, x, y, (18, yy, 25, yy), P["mortar"])


def inner_notch(d, x, y, side="left"):
    if side == "left":
        west_wall(d, x, y)
        south_edge(d, x, y)
    else:
        east_wall(d, x, y)
        south_edge(d, x, y)


def wall_door(d, x, y):
    north_wall(d, x, y)
    rect(d, x, y, (10, 9, 22, 27), P["door"], P["ink"])
    rect(d, x, y, (12, 10, 20, 13), P["door_hi"])
    rect(d, x, y, (18, 18, 20, 20), P["lamp"])
    rect(d, x, y, (10, 27, 22, 31), P["shadow"])


def glass_wall(d, x, y):
    north_wall(d, x, y)
    rect(d, x, y, (4, 10, 27, 24), P["glass"], P["metal_lo"])
    for xx in (5, 16):
        rect(d, x, y, (xx, 11, xx + 9, 23), (112, 199, 214, 210))
        line(d, x, y, (xx + 2, 21, xx + 8, 13), (222, 249, 251, 255))
    line(d, x, y, (15, 10, 15, 24), P["metal_hi"])


def wall_panel(d, x, y):
    north_wall(d, x, y)
    rect(d, x, y, (7, 12, 24, 22), P["metal_lo"], P["ink"])
    rect(d, x, y, (9, 14, 22, 20), P["screen"], P["metal"])
    rect(d, x, y, (11, 16, 15, 17), P["lamp"])
    rect(d, x, y, (17, 16, 21, 17), P["paper"])


def thick_wall_top(d, x, y, left=False, right=False, light=False):
    # First tile of a thick 2.5D wall: the walk-blocking wall cap/depth.
    rect(d, x, y, (0, 8, 31, 12), P["wall_dark"], P["ink"])
    rect(d, x, y, (0, 13, 31, 27), P["wall_top"], P["ink"])
    rect(d, x, y, (1, 14, 30, 16), P["wall_top_hi"])
    line(d, x, y, (0, 22, 31, 22), (112, 106, 91, 255))
    for xx in (10, 22):
        line(d, x, y, (xx, 14, xx, 21), (116, 110, 96, 255))
    pts(d, x, y, [(6, 18), (17, 24), (27, 17)], (130, 123, 106, 255))
    rect(d, x, y, (0, 28, 31, 31), P["trim"], P["ink"])
    if left:
        rect(d, x, y, (0, 8, 5, 31), P["wall_dark"], P["ink"])
    if right:
        rect(d, x, y, (26, 8, 31, 31), P["wall_dark"], P["ink"])
    if light:
        rect(d, x, y, (15, 24, 17, 26), P["lamp"])
        rect(d, x, y, (8, 27, 24, 29), (222, 180, 83, 80))


def thick_wall_face(d, x, y, left=False, right=False, light=False):
    # Second tile of a thick 2.5D wall: vertical face, lower trim and cast shadow.
    rect(d, x, y, (0, 0, 31, 3), P["shadow"])
    wall_bricks(d, x, y, 4, 22)
    rect(d, x, y, (0, 23, 31, 27), P["trim"], P["ink"])
    rect(d, x, y, (0, 28, 31, 31), P["shadow"])
    if left:
        rect(d, x, y, (0, 0, 5, 27), P["wall_dark"], P["ink"])
    if right:
        rect(d, x, y, (26, 0, 31, 27), P["wall_dark"], P["ink"])
    if light:
        rect(d, x, y, (15, 2, 17, 4), P["lamp"])
        rect(d, x, y, (7, 5, 25, 8), (222, 180, 83, 85))
        rect(d, x, y, (3, 9, 29, 13), (222, 180, 83, 34))


def thick_door_top(d, x, y):
    thick_wall_top(d, x, y)
    rect(d, x, y, (9, 22, 23, 31), P["wall_dark"], P["ink"])


def thick_door_face(d, x, y):
    thick_wall_face(d, x, y)
    rect(d, x, y, (9, 0, 23, 27), P["door"], P["ink"])
    rect(d, x, y, (11, 2, 21, 6), P["door_hi"])
    rect(d, x, y, (19, 14, 21, 16), P["lamp"])
    rect(d, x, y, (9, 28, 23, 31), P["shadow"])


def thick_glass_top(d, x, y):
    thick_wall_top(d, x, y)
    rect(d, x, y, (4, 20, 27, 31), P["glass"], P["metal_lo"])
    line(d, x, y, (15, 20, 15, 31), P["metal_hi"])


def thick_glass_face(d, x, y):
    thick_wall_face(d, x, y)
    rect(d, x, y, (4, 0, 27, 21), P["glass"], P["metal_lo"])
    for xx in (5, 16):
        rect(d, x, y, (xx, 2, xx + 9, 19), (112, 199, 214, 210))
        line(d, x, y, (xx + 2, 17, xx + 8, 5), (222, 249, 251, 255))
    line(d, x, y, (15, 0, 15, 21), P["metal_hi"])


def thick_panel_top(d, x, y):
    thick_wall_top(d, x, y)
    rect(d, x, y, (8, 26, 24, 31), P["metal_lo"], P["ink"])
    rect(d, x, y, (10, 28, 22, 30), P["screen"])


def thick_panel_face(d, x, y):
    thick_wall_face(d, x, y)
    rect(d, x, y, (8, 0, 24, 12), P["metal_lo"], P["ink"])
    rect(d, x, y, (10, 2, 22, 10), P["screen"], P["metal"])
    rect(d, x, y, (12, 5, 15, 6), P["lamp"])
    rect(d, x, y, (17, 5, 20, 6), P["paper"])


def object_shadow(d, x, y, box=(4, 26, 28, 31)):
    rect(d, x, y, box, P["soft_shadow"])


def front_desk(d, x, y):
    object_shadow(d, x, y, (3, 25, 29, 31))
    rect(d, x, y, (4, 10, 28, 23), P["desk"], P["ink"])
    rect(d, x, y, (5, 10, 27, 13), P["desk_hi"])
    rect(d, x, y, (6, 21, 26, 24), P["desk_lo"])
    rect(d, x, y, (9, 14, 17, 20), P["screen"], P["metal_lo"])
    rect(d, x, y, (10, 15, 16, 16), P["screen_hi"])
    rect(d, x, y, (21, 14, 26, 19), P["paper"])


def side_desk(d, x, y):
    object_shadow(d, x, y, (9, 25, 24, 31))
    rect(d, x, y, (9, 5, 23, 26), P["desk"], P["ink"])
    rect(d, x, y, (10, 6, 13, 25), P["desk_hi"])
    rect(d, x, y, (14, 9, 21, 18), P["screen"], P["metal_lo"])
    rect(d, x, y, (15, 10, 17, 17), P["screen_hi"])
    rect(d, x, y, (14, 20, 20, 24), P["paper"])


def office_chair(d, x, y):
    object_shadow(d, x, y, (10, 24, 23, 31))
    rect(d, x, y, (11, 9, 22, 17), P["metal_lo"], P["ink"])
    rect(d, x, y, (13, 17, 20, 25), P["metal"], P["ink"])
    line(d, x, y, (13, 25, 9, 30), P["metal_lo"])
    line(d, x, y, (20, 25, 24, 30), P["metal_lo"])


def cubicle(d, x, y):
    object_shadow(d, x, y, (2, 25, 30, 31))
    rect(d, x, y, (2, 7, 29, 13), P["metal"], P["ink"])
    rect(d, x, y, (2, 13, 6, 29), P["metal"], P["ink"])
    rect(d, x, y, (10, 15, 28, 24), P["desk"], P["ink"])
    rect(d, x, y, (14, 16, 21, 20), P["screen"], P["metal_lo"])
    rect(d, x, y, (23, 17, 27, 21), P["paper"])


def meeting_table(d, x, y):
    object_shadow(d, x, y, (4, 25, 28, 31))
    rect(d, x, y, (5, 9, 27, 22), P["desk"], P["ink"])
    rect(d, x, y, (8, 10, 24, 13), P["desk_hi"])
    for xx, yy in [(4, 4), (14, 4), (24, 4), (4, 24), (14, 24), (24, 24)]:
        rect(d, x, y, (xx, yy, xx + 4, yy + 5), P["metal_lo"], P["ink"])
    rect(d, x, y, (15, 15, 18, 18), P["water"])


def cabinet(d, x, y):
    object_shadow(d, x, y)
    for xx in (4, 13, 22):
        rect(d, x, y, (xx, 6, xx + 7, 28), P["metal"], P["ink"])
        rect(d, x, y, (xx + 2, 10, xx + 5, 11), P["metal_hi"])
        rect(d, x, y, (xx + 5, 18, xx + 6, 20), P["lamp"])


def server(d, x, y):
    object_shadow(d, x, y)
    rect(d, x, y, (7, 2, 25, 31), P["metal_lo"], P["ink"])
    for yy in (5, 11, 17, 23):
        rect(d, x, y, (9, yy, 23, yy + 3), P["metal"])
        pts(d, x, y, [(11, yy + 1), (15, yy + 1), (20, yy + 1)], P["screen_hi"])


def copier(d, x, y):
    object_shadow(d, x, y)
    rect(d, x, y, (5, 13, 27, 28), P["metal_hi"], P["ink"])
    rect(d, x, y, (8, 8, 24, 14), P["metal"], P["ink"])
    rect(d, x, y, (10, 5, 22, 8), P["paper"], P["ink"])
    rect(d, x, y, (21, 16, 25, 19), P["screen"])


def water_cooler(d, x, y):
    object_shadow(d, x, y, (10, 27, 23, 31))
    rect(d, x, y, (12, 11, 21, 29), P["metal_hi"], P["ink"])
    rect(d, x, y, (11, 5, 22, 14), P["water"], P["ink"])
    rect(d, x, y, (14, 16, 19, 19), P["screen"])


def plant(d, x, y):
    object_shadow(d, x, y, (8, 25, 25, 31))
    rect(d, x, y, (12, 22, 21, 29), P["desk"], P["ink"])
    rect(d, x, y, (10, 18, 23, 23), P["desk_hi"], P["ink"])
    for box in [(15, 8, 18, 18), (9, 12, 15, 20), (18, 12, 25, 20), (13, 5, 21, 11)]:
        rect(d, x, y, box, P["green"], P["green_lo"])


def shelf(d, x, y):
    object_shadow(d, x, y)
    rect(d, x, y, (5, 5, 27, 29), P["metal_lo"], P["ink"])
    for yy in (10, 17, 24):
        line(d, x, y, (6, yy, 26, yy), P["metal_hi"])
    for xx, yy, c in [(8, 7, P["red"]), (14, 7, P["paper"]), (21, 7, P["lamp"]), (10, 19, P["paper"]), (18, 25, P["red"])]:
        rect(d, x, y, (xx, yy, xx + 4, yy + 5), c)


def sofa(d, x, y):
    object_shadow(d, x, y, (3, 25, 29, 31))
    rect(d, x, y, (5, 12, 27, 24), (40, 65, 79, 255), P["ink"])
    rect(d, x, y, (3, 16, 8, 26), (31, 51, 63, 255), P["ink"])
    rect(d, x, y, (24, 16, 29, 26), (31, 51, 63, 255), P["ink"])
    line(d, x, y, (15, 13, 15, 24), P["metal_lo"])


def trash(d, x, y):
    object_shadow(d, x, y, (11, 25, 23, 31))
    rect(d, x, y, (11, 13, 22, 28), P["metal"], P["ink"])
    rect(d, x, y, (10, 11, 23, 14), P["metal_hi"], P["ink"])


def boxes(d, x, y):
    object_shadow(d, x, y)
    rect(d, x, y, (7, 16, 18, 28), (118, 78, 42, 255), P["ink"])
    rect(d, x, y, (16, 11, 26, 23), (100, 67, 39, 255), P["ink"])
    line(d, x, y, (9, 18, 16, 18), P["desk_hi"])
    line(d, x, y, (18, 13, 24, 13), P["desk_hi"])


def lamp_tile(d, x, y):
    rect(d, x, y, (14, 10, 17, 12), P["lamp"])
    rect(d, x, y, (9, 13, 23, 15), (236, 198, 86, 90))
    rect(d, x, y, (5, 16, 27, 18), (236, 198, 86, 36))


def papers(d, x, y):
    rect(d, x, y, (7, 17, 17, 23), P["paper"], P["ink"])
    rect(d, x, y, (13, 12, 24, 18), (184, 186, 177, 255), P["ink"])
    rect(d, x, y, (6, 24, 14, 27), P["paper"], P["ink"])
    line(d, x, y, (15, 14, 21, 14), P["metal"])


def coffee_stain(d, x, y):
    # Coffee stain / dirt mark, not gore.
    rect(d, x, y, (11, 18, 18, 23), (64, 43, 31, 180))
    rect(d, x, y, (18, 21, 24, 24), (54, 36, 27, 150))
    pts(d, x, y, [(8, 15), (23, 16), (27, 24), (14, 27), (6, 23)], (70, 48, 35, 180))


def cable_clutter(d, x, y):
    # Loose office cables and small dropped papers.
    line(d, x, y, (5, 22, 12, 18), P["metal_lo"], 2)
    line(d, x, y, (12, 18, 19, 24), P["metal_lo"], 2)
    line(d, x, y, (19, 24, 27, 17), P["metal_lo"], 2)
    rect(d, x, y, (22, 14, 27, 18), P["metal"], P["ink"])
    rect(d, x, y, (8, 10, 14, 13), P["paper"], P["ink"])
    rect(d, x, y, (15, 8, 20, 10), (165, 165, 153, 255), P["ink"])


def notice_panel(d, x, y):
    # Wall-mounted office notice board / access panel.
    object_shadow(d, x, y, (7, 25, 25, 30))
    rect(d, x, y, (7, 8, 25, 23), P["metal_lo"], P["ink"])
    rect(d, x, y, (9, 10, 23, 21), P["screen"], P["metal"])
    rect(d, x, y, (11, 13, 15, 14), P["lamp"])
    rect(d, x, y, (17, 13, 21, 14), P["paper"])
    rect(d, x, y, (11, 17, 21, 18), P["metal_hi"])


def draw_atlas():
    sheet = new_sheet()
    d = ImageDraw.Draw(sheet, "RGBA")

    # Row 0: floors.
    for x in range(4):
        floor(d, x, 0, x)
    for x in range(4, 8):
        lobby_tile(d, x, 0, x % 2)
    floor(d, 8, 0, 2)
    papers(d, 8, 0)
    floor(d, 9, 0, 0)
    coffee_stain(d, 9, 0)
    floor(d, 10, 0, 0)
    cable_clutter(d, 10, 0)
    for x in range(11, 16):
        floor(d, x, 0, x % 4)

    # Row 1: first tile of thick north wall, the wall cap/depth.
    thick_wall_top(d, 0, 1)
    thick_wall_top(d, 1, 1, light=True)
    thick_wall_top(d, 2, 1, left=True)
    thick_wall_top(d, 3, 1, right=True)
    thick_door_top(d, 4, 1)
    thick_glass_top(d, 5, 1)
    thick_panel_top(d, 6, 1)
    west_wall(d, 7, 1)
    east_wall(d, 8, 1)
    inner_notch(d, 9, 1, "left")
    inner_notch(d, 10, 1, "right")
    for x in range(11, 16):
        thick_wall_top(d, x, 1, light=(x == 13))

    # Row 2: second tile of thick north wall, the visible wall face.
    thick_wall_face(d, 0, 2)
    thick_wall_face(d, 1, 2, light=True)
    thick_wall_face(d, 2, 2, left=True)
    thick_wall_face(d, 3, 2, right=True)
    thick_door_face(d, 4, 2)
    thick_glass_face(d, 5, 2)
    thick_panel_face(d, 6, 2)
    west_wall(d, 7, 2)
    east_wall(d, 8, 2)
    thick_wall_face(d, 9, 2, left=True)
    thick_wall_face(d, 10, 2, right=True)
    for x in range(11, 16):
        thick_wall_face(d, x, 2, light=(x == 13))

    # Row 3: foreground/south edge tiles.
    south_edge(d, 0, 3)
    south_edge(d, 1, 3, drips=True)
    for x in range(2, 8):
        south_edge(d, x, 3)
    west_wall(d, 8, 3)
    east_wall(d, 9, 3)
    thick_door_face(d, 10, 3)
    thick_glass_face(d, 11, 3)
    thick_panel_face(d, 12, 3)
    for x in range(13, 16):
        south_edge(d, x, 3, drips=(x == 14))

    # Rows 4-7: front/side-facing office props, all transparent.
    props = [
        front_desk, side_desk, office_chair, cubicle, meeting_table, cabinet, server, copier,
        water_cooler, plant, shelf, sofa, trash, boxes, lamp_tile, papers,
        coffee_stain, cable_clutter, notice_panel, front_desk, side_desk, cubicle, meeting_table, cabinet,
        server, copier, water_cooler, plant, shelf, sofa, boxes, trash,
        office_chair, front_desk, side_desk, cubicle, meeting_table, cabinet, server, copier,
        water_cooler, plant, shelf, sofa, boxes, lamp_tile, papers, cable_clutter,
        coffee_stain, notice_panel, front_desk, side_desk, cubicle, meeting_table, cabinet, server,
        copier, water_cooler, plant, shelf, sofa, trash, boxes, papers, cable_clutter,
    ]
    idx = 0
    for y in range(4, 8):
        for x in range(COLS):
            props[idx](d, x, y)
            idx += 1

    OUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT_IMAGE)
    draw_preview(sheet)


def crop(sheet, tx, ty):
    return sheet.crop((tx * TILE, ty * TILE, tx * TILE + TILE, ty * TILE + TILE))


def draw_preview(sheet):
    w, h = 42, 17
    out = Image.new("RGBA", (w * TILE, h * TILE), P["black"])

    def paste(tx, ty, gx, gy):
        out.alpha_composite(crop(sheet, tx, ty), (gx * TILE, gy * TILE))

    def fill(x0, y0, x1, y1, tx=0, ty=0):
        for gy in range(y0, y1 + 1):
            for gx in range(x0, x1 + 1):
                paste(tx + ((gx + gy) % 4), ty, gx, gy)

    # Main horizontal corridor with offsets and a lower corridor.
    fill(3, 4, 31, 7, 0, 0)
    fill(31, 5, 38, 7, 0, 0)
    fill(10, 11, 28, 13, 0, 0)
    fill(34, 10, 39, 12, 0, 0)

    # North wall layer. A thick wall uses two map rows: cap row, then face row.
    for gx in range(3, 31):
        paste(1 if gx in (6, 21, 29) else 0, 1, gx, 3)
        paste(1 if gx in (6, 21, 29) else 0, 2, gx, 4)
    for gx in range(31, 39):
        paste(4 if gx == 35 else 0, 1, gx, 4)
        paste(4 if gx == 35 else 0, 2, gx, 5)
    for gx in range(10, 29):
        paste(1 if gx in (16, 22) else 0, 1, gx, 10)
        paste(1 if gx in (16, 22) else 0, 2, gx, 11)
    for gx in range(34, 40):
        paste(0, 1, gx, 9)
        paste(0, 2, gx, 10)

    # Recesses/vertical walls.
    for gy in range(4, 8):
        paste(7, 1, 2, gy)
        paste(8, 1, 39, gy)
    for gy in range(11, 14):
        paste(7, 1, 9, gy)
        paste(8, 1, 29, gy)
        paste(7, 1, 33, gy)
        paste(8, 1, 40, gy)

    # South foreground lips.
    for gx in range(3, 13):
        paste(0 if gx % 3 else 1, 3, gx, 8)
    for gx in range(14, 26):
        paste(0, 3, gx, 8)
    for gx in range(27, 32):
        paste(0, 3, gx, 8)
    for gx in range(10, 29):
        paste(0 if gx % 4 else 1, 3, gx, 14)
    for gx in range(34, 40):
        paste(0, 3, gx, 13)

    # Door/glass/wall-panel details.
    for gx in (17, 23, 35):
        paste(4, 1, gx, 3 if gx != 35 else 4)
        paste(4, 2, gx, 4 if gx != 35 else 5)
    paste(5, 1, 25, 3)
    paste(5, 2, 25, 4)
    for gx, gy in [(18, 5), (22, 3), (27, 3), (36, 9)]:
        paste(6, 1, gx, gy)
        paste(6, 2, gx, gy + 1)

    # Office props placed over floor, visibly front/side-facing.
    for gx, gy, tx, ty in [
        (7, 6, 0, 4), (13, 6, 1, 4), (20, 6, 3, 4), (25, 6, 4, 4),
        (12, 12, 6, 4), (16, 12, 7, 4), (20, 12, 9, 4),
        (36, 11, 2, 5), (5, 6, 8, 4), (30, 6, 14, 4),
        (15, 7, 15, 4), (23, 7, 1, 5), (26, 7, 0, 5),
    ]:
        paste(tx, ty, gx, gy)

    add_preview_lighting(out, [(6, 4), (21, 4), (29, 4), (16, 11), (22, 11), (36, 10)])
    out.save(OUT_PREVIEW)


def add_preview_lighting(out, cells):
    glow = Image.new("RGBA", out.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(glow, "RGBA")
    for gx, gy in cells:
        cx = gx * TILE + TILE // 2
        cy = gy * TILE + 28
        for radius, alpha in [(112, 3), (96, 4), (80, 6), (64, 8), (50, 11), (38, 14), (26, 18), (14, 22)]:
            d.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(226, 180, 86, alpha))
    out.alpha_composite(glow)


def write_tileset():
    # Floors are passable. Wall/foreground edge tiles and bulky furniture block by default.
    blocking = set()
    blocking.update((x, 1) for x in range(COLS))
    blocking.update((x, 2) for x in range(COLS))
    blocking.update((x, 3) for x in range(COLS))
    blocking.update((x, y) for y in range(4, 8) for x in range(0, 14))

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

[ext_resource type="Texture2D" path="res://Art/Sprites/ModernOfficeCorridor25D_TileSheet.png" id="1_corridor25d"]

[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_corridor25d"]
texture = ExtResource("1_corridor25d")
texture_region_size = Vector2i(32, 32)
{atlas_entries}

[resource]
tile_size = Vector2i(32, 32)
physics_layer_0/collision_layer = 1
sources/0 = SubResource("TileSetAtlasSource_corridor25d")
"""
    OUT_TILESET.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    draw_atlas()
    write_tileset()
    print(f"Wrote {OUT_IMAGE.relative_to(ROOT)}")
    print(f"Wrote {OUT_PREVIEW.relative_to(ROOT)}")
    print(f"Wrote {OUT_TILESET.relative_to(ROOT)}")
