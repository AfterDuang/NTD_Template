from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT_IMAGE = ROOT / "Art" / "Sprites" / "ModernOfficeTileSheet.png"
OUT_PREVIEW = ROOT / "Art" / "Sprites" / "ModernOfficeMapPreview.png"
OUT_TILESET = ROOT / "Art" / "ModernOfficeTileMap.tres"
TILE = 32
COLS = 10
ROWS = 9


PAL = {
    "void": (0, 0, 0, 0),
    "outline": (20, 22, 24, 255),
    "shadow": (30, 28, 30, 255),
    "carpet": (50, 49, 58, 255),
    "carpet_d": (39, 38, 46, 255),
    "carpet_l": (66, 65, 74, 255),
    "tile": (96, 93, 85, 255),
    "tile_d": (73, 70, 66, 255),
    "tile_l": (124, 119, 108, 255),
    "wood": (91, 58, 35, 255),
    "wood_d": (66, 42, 27, 255),
    "wood_l": (123, 79, 45, 255),
    "wall": (166, 160, 146, 255),
    "wall_d": (114, 110, 104, 255),
    "wall_l": (205, 198, 181, 255),
    "glass": (84, 128, 137, 150),
    "glass_l": (154, 213, 221, 210),
    "metal": (83, 91, 94, 255),
    "metal_l": (135, 145, 146, 255),
    "metal_d": (47, 53, 57, 255),
    "desk": (87, 62, 44, 255),
    "desk_l": (125, 88, 58, 255),
    "desk_d": (55, 38, 30, 255),
    "paper": (199, 202, 194, 255),
    "screen": (38, 85, 89, 255),
    "screen_l": (71, 156, 164, 255),
    "accent": (225, 176, 67, 255),
    "red": (139, 44, 39, 255),
    "plant": (62, 121, 75, 255),
    "plant_d": (35, 73, 46, 255),
    "water": (82, 142, 158, 255),
}


def cell(draw, x, y):
    return x * TILE, y * TILE


def rect(draw, x, y, xy, fill, outline=None):
    ox, oy = cell(draw, x, y)
    draw.rectangle((ox + xy[0], oy + xy[1], ox + xy[2], oy + xy[3]), fill=fill, outline=outline)


def line(draw, x, y, xy, fill, width=1):
    ox, oy = cell(draw, x, y)
    draw.line((ox + xy[0], oy + xy[1], ox + xy[2], oy + xy[3]), fill=fill, width=width)


def px(draw, x, y, points, fill):
    ox, oy = cell(draw, x, y)
    for px_, py_ in points:
        draw.point((ox + px_, oy + py_), fill=fill)


def base(draw, x, y, color):
    rect(draw, x, y, (0, 0, 31, 31), color)
    rect(draw, x, y, (0, 0, 31, 0), tuple(min(255, c + 22) for c in color[:3]) + (255,))
    px(draw, x, y, [(7, 9), (18, 5), (25, 13), (11, 23), (27, 27)], PAL["shadow"])


def carpet(draw, x, y, variant=0):
    base(draw, x, y, PAL["carpet"])
    if variant == 1:
        rect(draw, x, y, (0, 14, 31, 16), PAL["carpet_d"])
        rect(draw, x, y, (14, 0, 16, 31), PAL["carpet_d"])
    elif variant == 2:
        line(draw, x, y, (3, 27, 28, 4), PAL["carpet_d"])
        line(draw, x, y, (5, 30, 30, 5), PAL["carpet_l"])
    elif variant == 3:
        for i in range(4, 30, 8):
            line(draw, x, y, (i, 3, i, 29), PAL["carpet_d"])
    else:
        px(draw, x, y, [(6, 6), (7, 6), (19, 10), (20, 10), (13, 26), (24, 22)], PAL["carpet_l"])


def tile_floor(draw, x, y):
    base(draw, x, y, PAL["tile"])
    rect(draw, x, y, (0, 15, 31, 16), PAL["tile_d"])
    rect(draw, x, y, (15, 0, 16, 31), PAL["tile_d"])
    rect(draw, x, y, (1, 1, 14, 14), PAL["tile_l"])
    rect(draw, x, y, (17, 17, 30, 30), (86, 83, 77, 255))


def wood_floor(draw, x, y):
    base(draw, x, y, PAL["wood"])
    for yy in (7, 15, 23):
        line(draw, x, y, (1, yy, 30, yy), PAL["wood_d"])
    for xx, yy in [(6, 3), (19, 10), (12, 19), (27, 25)]:
        line(draw, x, y, (xx, yy, min(31, xx + 7), yy), PAL["wood_l"])


def wall(draw, x, y, kind):
    if kind == "top":
        rect(draw, x, y, (0, 0, 31, 31), PAL["wall"])
        rect(draw, x, y, (0, 0, 31, 4), PAL["wall_l"])
        rect(draw, x, y, (0, 27, 31, 31), PAL["wall_d"])
    elif kind == "left":
        rect(draw, x, y, (0, 0, 31, 31), PAL["wall"])
        rect(draw, x, y, (0, 0, 4, 31), PAL["wall_l"])
        rect(draw, x, y, (27, 0, 31, 31), PAL["wall_d"])
    elif kind == "right":
        rect(draw, x, y, (0, 0, 31, 31), PAL["wall"])
        rect(draw, x, y, (0, 0, 4, 31), PAL["wall_d"])
        rect(draw, x, y, (27, 0, 31, 31), PAL["wall_l"])
    elif kind == "corner":
        rect(draw, x, y, (0, 0, 31, 31), PAL["wall"])
        rect(draw, x, y, (0, 0, 31, 4), PAL["wall_l"])
        rect(draw, x, y, (0, 0, 4, 31), PAL["wall_l"])
        rect(draw, x, y, (27, 5, 31, 31), PAL["wall_d"])
        rect(draw, x, y, (5, 27, 31, 31), PAL["wall_d"])
    for i in (8, 20):
        px(draw, x, y, [(i, 8), (i + 1, 8), (i + 8, 21)], PAL["wall_d"])


def glass_wall(draw, x, y, horizontal=True):
    base(draw, x, y, PAL["tile_d"])
    if horizontal:
        rect(draw, x, y, (0, 10, 31, 21), PAL["glass"], PAL["metal_d"])
        line(draw, x, y, (0, 15, 31, 15), PAL["glass_l"])
        for xx in (10, 21):
            line(draw, x, y, (xx, 10, xx, 21), PAL["metal"])
    else:
        rect(draw, x, y, (10, 0, 21, 31), PAL["glass"], PAL["metal_d"])
        line(draw, x, y, (15, 0, 15, 31), PAL["glass_l"])
        for yy in (10, 21):
            line(draw, x, y, (10, yy, 21, yy), PAL["metal"])


def door(draw, x, y):
    base(draw, x, y, PAL["wall_d"])
    rect(draw, x, y, (5, 2, 26, 31), PAL["desk_d"], PAL["outline"])
    rect(draw, x, y, (7, 4, 24, 29), PAL["desk"])
    rect(draw, x, y, (20, 15, 22, 17), PAL["accent"])
    line(draw, x, y, (8, 8, 23, 8), PAL["desk_l"])
    line(draw, x, y, (8, 23, 23, 23), PAL["desk_d"])


def desk(draw, x, y, chair=False):
    carpet(draw, x, y, 0)
    rect(draw, x, y, (4, 8, 28, 22), PAL["desk"], PAL["outline"])
    rect(draw, x, y, (5, 9, 27, 12), PAL["desk_l"])
    rect(draw, x, y, (8, 12, 17, 19), PAL["screen"], PAL["metal_d"])
    rect(draw, x, y, (9, 13, 16, 15), PAL["screen_l"])
    rect(draw, x, y, (20, 12, 26, 17), PAL["paper"])
    rect(draw, x, y, (22, 18, 25, 20), PAL["red"])
    if chair:
        rect(draw, x, y, (10, 24, 22, 30), PAL["metal_d"], PAL["outline"])
        rect(draw, x, y, (12, 23, 20, 27), PAL["metal"])


def cubicle(draw, x, y):
    carpet(draw, x, y, 1)
    rect(draw, x, y, (0, 4, 31, 8), PAL["metal"], PAL["metal_d"])
    rect(draw, x, y, (0, 4, 4, 31), PAL["metal"], PAL["metal_d"])
    rect(draw, x, y, (9, 11, 28, 22), PAL["desk"], PAL["outline"])
    rect(draw, x, y, (13, 13, 22, 18), PAL["screen"], PAL["metal_d"])
    rect(draw, x, y, (24, 13, 28, 19), PAL["paper"])


def shelf(draw, x, y):
    carpet(draw, x, y, 0)
    rect(draw, x, y, (5, 3, 26, 29), PAL["metal_d"], PAL["outline"])
    for yy in (8, 15, 22):
        line(draw, x, y, (6, yy, 25, yy), PAL["metal_l"])
    for xx, yy, c in [(8, 5, PAL["red"]), (14, 5, PAL["paper"]), (21, 5, PAL["accent"]), (10, 17, PAL["paper"]), (18, 23, PAL["red"])]:
        rect(draw, x, y, (xx, yy, xx + 4, yy + 5), c)


def plant(draw, x, y):
    carpet(draw, x, y, 2)
    rect(draw, x, y, (12, 21, 20, 28), PAL["desk_d"], PAL["outline"])
    rect(draw, x, y, (10, 17, 22, 22), PAL["desk"], PAL["outline"])
    for xy in [(15, 8, 18, 17), (9, 12, 15, 19), (18, 12, 24, 19), (13, 5, 20, 10)]:
        rect(draw, x, y, xy, PAL["plant"], PAL["plant_d"])


def cabinets(draw, x, y):
    carpet(draw, x, y, 0)
    for xx in (3, 13, 23):
        rect(draw, x, y, (xx, 7, xx + 7, 27), PAL["metal"], PAL["outline"])
        rect(draw, x, y, (xx + 1, 9, xx + 6, 14), PAL["metal_l"])
        rect(draw, x, y, (xx + 3, 19, xx + 5, 20), PAL["accent"])


def vending(draw, x, y):
    tile_floor(draw, x, y)
    rect(draw, x, y, (6, 2, 26, 30), (35, 54, 83, 255), PAL["outline"])
    rect(draw, x, y, (8, 4, 24, 14), PAL["screen"], PAL["metal_d"])
    for xx, c in [(9, PAL["red"]), (15, PAL["accent"]), (21, PAL["water"])]:
        rect(draw, x, y, (xx, 17, xx + 3, 22), c)
    rect(draw, x, y, (9, 25, 23, 27), PAL["metal_l"])


def server(draw, x, y):
    tile_floor(draw, x, y)
    rect(draw, x, y, (6, 1, 26, 31), PAL["metal_d"], PAL["outline"])
    for yy in (4, 10, 16, 22):
        rect(draw, x, y, (8, yy, 24, yy + 3), PAL["metal"])
        px(draw, x, y, [(10, yy + 1), (14, yy + 1), (20, yy + 1)], PAL["screen_l"])
    rect(draw, x, y, (8, 27, 24, 29), PAL["outline"])


def water_cooler(draw, x, y):
    tile_floor(draw, x, y)
    rect(draw, x, y, (12, 10, 21, 29), PAL["metal_l"], PAL["outline"])
    rect(draw, x, y, (11, 4, 22, 13), PAL["water"], PAL["outline"])
    rect(draw, x, y, (14, 15, 19, 18), PAL["screen"])
    rect(draw, x, y, (14, 24, 19, 27), PAL["metal_d"])


def lamp(draw, x, y):
    carpet(draw, x, y, 0)
    rect(draw, x, y, (10, 5, 22, 10), (235, 198, 99, 255), PAL["accent"])
    for r, a in [((7, 11, 25, 13), 80), ((3, 14, 29, 16), 35)]:
        rect(draw, x, y, r, (235, 198, 99, a))
    px(draw, x, y, [(10, 22), (16, 24), (23, 20), (25, 26)], PAL["carpet_l"])


def debris(draw, x, y):
    carpet(draw, x, y, 2)
    for p in [(8, 18), (9, 18), (10, 19), (21, 13), (22, 14), (18, 24), (5, 9)]:
        px(draw, x, y, [p], PAL["paper"])
    rect(draw, x, y, (13, 14, 17, 17), PAL["wall_d"], PAL["outline"])
    line(draw, x, y, (20, 22, 27, 28), PAL["red"])
    line(draw, x, y, (21, 23, 24, 28), PAL["red"])


def conference(draw, x, y):
    wood_floor(draw, x, y)
    rect(draw, x, y, (5, 9, 27, 22), PAL["desk"], PAL["outline"])
    rect(draw, x, y, (8, 11, 24, 14), PAL["desk_l"])
    for xx, yy in [(4, 4), (15, 4), (25, 4), (4, 24), (15, 24), (25, 24)]:
        rect(draw, x, y, (xx, yy, xx + 4, yy + 5), PAL["metal_d"], PAL["outline"])
    rect(draw, x, y, (14, 15, 18, 18), PAL["water"])


def window(draw, x, y):
    wall(draw, x, y, "top")
    rect(draw, x, y, (4, 5, 27, 24), (63, 117, 131, 255), PAL["metal_d"])
    for xx in (5, 16):
        rect(draw, x, y, (xx, 6, xx + 10, 23), (122, 202, 218, 255))
        line(draw, x, y, (xx + 1, 20, xx + 8, 9), (210, 247, 250, 255))
    line(draw, x, y, (15, 5, 15, 24), PAL["metal_l"])


def draw_tiles():
    img = Image.new("RGBA", (COLS * TILE, ROWS * TILE), PAL["void"])
    draw = ImageDraw.Draw(img, "RGBA")

    layout = [
        [lambda d, x, y: carpet(d, x, y, 0), lambda d, x, y: carpet(d, x, y, 1), lambda d, x, y: carpet(d, x, y, 2), lambda d, x, y: carpet(d, x, y, 3), tile_floor, wood_floor, lambda d, x, y: wall(d, x, y, "top"), lambda d, x, y: wall(d, x, y, "left"), lambda d, x, y: wall(d, x, y, "right"), lambda d, x, y: wall(d, x, y, "corner")],
        [lambda d, x, y: glass_wall(d, x, y, True), lambda d, x, y: glass_wall(d, x, y, False), door, window, desk, lambda d, x, y: desk(d, x, y, True), cubicle, shelf, plant, cabinets],
        [vending, server, water_cooler, lamp, debris, conference, lambda d, x, y: wall(d, x, y, "top"), lambda d, x, y: wall(d, x, y, "left"), lambda d, x, y: wall(d, x, y, "right"), door],
        [lambda d, x, y: carpet(d, x, y, 0), lambda d, x, y: desk(d, x, y, True), cubicle, plant, shelf, lambda d, x, y: carpet(d, x, y, 1), glass_wall, vending, server, debris],
        [wood_floor, conference, lambda d, x, y: desk(d, x, y, False), cabinets, window, door, water_cooler, plant, lamp, debris],
        [tile_floor, lambda d, x, y: glass_wall(d, x, y, True), lambda d, x, y: glass_wall(d, x, y, False), server, vending, shelf, cabinets, water_cooler, lambda d, x, y: wall(d, x, y, "top"), lambda d, x, y: wall(d, x, y, "corner")],
        [lambda d, x, y: carpet(d, x, y, 2), lambda d, x, y: carpet(d, x, y, 3), desk, cubicle, plant, lamp, debris, conference, door, window],
        [lambda d, x, y: wall(d, x, y, "top"), lambda d, x, y: wall(d, x, y, "left"), lambda d, x, y: wall(d, x, y, "right"), lambda d, x, y: wall(d, x, y, "corner"), tile_floor, wood_floor, vending, server, shelf, cabinets],
        [lambda d, x, y: carpet(d, x, y, 0), lambda d, x, y: carpet(d, x, y, 1), lambda d, x, y: carpet(d, x, y, 2), lambda d, x, y: glass_wall(d, x, y, True), lambda d, x, y: glass_wall(d, x, y, False), water_cooler, plant, lamp, debris, conference],
    ]

    for y, row in enumerate(layout):
        for x, fn in enumerate(row):
            fn(draw, x, y)

    OUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_IMAGE)
    draw_preview(img)


def draw_preview(sheet):
    w, h = 24, 15
    preview = Image.new("RGBA", (w * TILE, h * TILE), (0, 0, 0, 255))

    def paste(tx, ty, gx, gy):
        tile = sheet.crop((tx * TILE, ty * TILE, tx * TILE + TILE, ty * TILE + TILE))
        preview.alpha_composite(tile, (gx * TILE, gy * TILE))

    def fill_room(x0, y0, x1, y1, tile):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                paste(tile[0], tile[1], xx, yy)

    def frame_room(x0, y0, x1, y1):
        for xx in range(x0, x1 + 1):
            paste(6, 0, xx, y0)
            paste(6, 0, xx, y1)
        for yy in range(y0, y1 + 1):
            paste(7, 0, x0, yy)
            paste(8, 0, x1, yy)
        paste(9, 0, x0, y0)
        paste(9, 0, x1, y0)
        paste(9, 0, x0, y1)
        paste(9, 0, x1, y1)

    # Central corridor and three functional rooms.
    fill_room(2, 6, 21, 8, (4, 0))
    fill_room(4, 2, 10, 5, (0, 0))
    fill_room(13, 2, 20, 5, (0, 0))
    fill_room(5, 9, 13, 12, (5, 4))
    frame_room(4, 2, 10, 5)
    frame_room(13, 2, 20, 5)
    frame_room(5, 9, 13, 12)

    # Door breaks and glass fronts.
    paste(2, 1, 7, 5)
    paste(0, 1, 5, 2)
    paste(0, 1, 6, 2)
    paste(0, 1, 15, 2)
    paste(0, 1, 16, 2)
    paste(2, 1, 17, 5)
    paste(2, 1, 9, 9)

    # Work area.
    for pos in [(5, 3), (8, 3), (5, 4), (8, 4)]:
        paste(6, 1, *pos)
    paste(8, 1, 10, 3)
    paste(7, 1, 10, 4)

    # Meeting room.
    paste(5, 2, 15, 3)
    paste(5, 2, 18, 3)
    paste(8, 1, 14, 4)
    paste(9, 1, 20, 4)

    # Storage / server corner.
    paste(3, 5, 6, 10)
    paste(1, 2, 8, 10)
    paste(0, 2, 11, 10)
    paste(2, 2, 12, 11)
    paste(8, 6, 7, 12)

    # Corridor detail.
    for pos in [(4, 7), (8, 6), (12, 7), (16, 6), (20, 7)]:
        paste(3, 2, *pos)
    for pos in [(3, 8), (18, 8), (21, 6)]:
        paste(4, 2, *pos)
    for pos in [(2, 6), (21, 8), (14, 8)]:
        paste(6, 4, *pos)

    preview.save(OUT_PREVIEW)


def collision_lines():
    blocking = set()
    # Wall, glass, door, large furniture, vending, server, cabinets, shelves, water cooler.
    blocking.update((x, 0) for x in range(6, 10))
    blocking.update((x, 1) for x in range(0, 10))
    blocking.update((x, 2) for x in [0, 1, 2, 3, 6, 7, 8, 9])
    blocking.update((x, 3) for x in [1, 2, 4, 7, 8])
    blocking.update((x, 4) for x in [1, 2, 3, 4, 5, 6])
    blocking.update((x, 5) for x in range(1, 10))
    blocking.update((x, 6) for x in [2, 3, 8, 9])
    blocking.update((x, 7) for x in [0, 1, 2, 3, 6, 7, 8, 9])
    blocking.update((x, 8) for x in [3, 4, 5, 9])

    lines = []
    for y in range(ROWS):
        for x in range(COLS):
            lines.append(f"{x}:{y}/0 = 0")
            if (x, y) in blocking:
                lines.append(
                    f"{x}:{y}/0/physics_layer_0/polygon_0/points = "
                    "PackedVector2Array(-16, -16, 16, -16, 16, 16, -16, 16)"
                )
    return "\n".join(lines)


def write_tileset():
    text = f"""[gd_resource type="TileSet" load_steps=3 format=3]

[ext_resource type="Texture2D" path="res://Art/Sprites/ModernOfficeTileSheet.png" id="1_modern"]

[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_modern_office"]
texture = ExtResource("1_modern")
texture_region_size = Vector2i(32, 32)
{collision_lines()}

[resource]
tile_size = Vector2i(32, 32)
physics_layer_0/collision_layer = 1
sources/0 = SubResource("TileSetAtlasSource_modern_office")
"""
    OUT_TILESET.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    draw_tiles()
    write_tileset()
    print(f"Wrote {OUT_IMAGE.relative_to(ROOT)}")
    print(f"Wrote {OUT_PREVIEW.relative_to(ROOT)}")
    print(f"Wrote {OUT_TILESET.relative_to(ROOT)}")
