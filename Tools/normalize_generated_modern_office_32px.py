from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Art" / "Sprites" / "GeneratedModernOffice25D_TileSheet.png"
OUT = ROOT / "Art" / "Sprites" / "GeneratedModernOffice25D_TileSheet_32px.png"
PREVIEW = ROOT / "Art" / "Sprites" / "GeneratedModernOffice25D_Preview_32px.png"
TILESET = ROOT / "Art" / "GeneratedModernOffice25D_TileMap_32px.tres"
TILE = 32
COLS = 16
ROWS = 12


def clear_edge_background(piece, threshold=42):
    piece = piece.convert("RGBA")
    w, h = piece.size
    pix = piece.load()
    seen = set()
    stack = []

    def is_bg(x, y):
        r, g, b, a = pix[x, y]
        return a > 0 and r < threshold and g < threshold and b < threshold

    for x in range(w):
        stack.extend([(x, 0), (x, h - 1)])
    for y in range(h):
        stack.extend([(0, y), (w - 1, y)])

    while stack:
        x, y = stack.pop()
        if (x, y) in seen or x < 0 or y < 0 or x >= w or y >= h:
            continue
        seen.add((x, y))
        if not is_bg(x, y):
            continue
        r, g, b, _ = pix[x, y]
        pix[x, y] = (r, g, b, 0)
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return piece


def crop(src, box, cells=(1, 1), alpha=True):
    piece = src.crop(box).convert("RGBA")
    if alpha:
        piece = clear_edge_background(piece)
    return piece.resize((cells[0] * TILE, cells[1] * TILE), Image.Resampling.NEAREST)


def paste(dst, piece, x, y):
    dst.alpha_composite(piece, (x * TILE, y * TILE))


def build_atlas():
    src = Image.open(SRC).convert("RGBA")
    atlas = Image.new("RGBA", (COLS * TILE, ROWS * TILE), (0, 0, 0, 0))

    floors = [
        (14, 14, 90, 129),
        (99, 14, 179, 129),
        (187, 14, 267, 129),
        (274, 14, 356, 129),
        (362, 14, 439, 129),
        (446, 14, 523, 129),
        (15, 139, 91, 253),
        (99, 139, 179, 253),
        (188, 139, 268, 253),
        (274, 139, 356, 253),
        (363, 139, 439, 253),
        (447, 139, 523, 253),
        (15, 263, 91, 379),
        (99, 263, 179, 379),
        (188, 263, 268, 379),
        (274, 263, 356, 379),
    ]
    for i, box in enumerate(floors):
        paste(atlas, crop(src, box, alpha=False), i, 0)

    wall_caps = [
        (535, 14, 624, 129),
        (636, 14, 725, 129),
        (737, 14, 852, 129),
        (889, 14, 981, 129),
        (988, 14, 1078, 129),
        (1089, 14, 1224, 129),
        (535, 139, 624, 253),
        (636, 139, 725, 253),
    ]
    wall_faces = [
        (535, 139, 624, 253),
        (636, 139, 725, 253),
        (737, 139, 852, 253),
        (889, 139, 981, 253),
        (988, 139, 1078, 253),
        (1089, 139, 1224, 253),
        (535, 263, 624, 379),
        (636, 263, 725, 379),
    ]
    for i, box in enumerate(wall_caps):
        paste(atlas, crop(src, box), i, 1)
    for i, box in enumerate(wall_faces):
        paste(atlas, crop(src, box), i, 2)

    edge_tiles = [
        (15, 395, 90, 545),
        (99, 395, 331, 545),
        (363, 395, 429, 545),
        (454, 395, 523, 545),
        (535, 395, 624, 545),
        (636, 395, 807, 545),
        (818, 395, 896, 545),
        (908, 395, 977, 545),
        (989, 395, 1078, 545),
        (1090, 395, 1224, 545),
    ]
    x = 0
    for box in edge_tiles:
        cells = (2, 1) if box[2] - box[0] > 120 else (1, 1)
        if x + cells[0] > COLS:
            break
        paste(atlas, crop(src, box, cells=cells), x, 3)
        x += cells[0]

    props = [
        ((16, 575, 91, 704), (1, 2)),
        ((88, 575, 180, 704), (2, 2)),
        ((187, 575, 279, 704), (2, 2)),
        ((288, 575, 410, 704), (2, 2)),
        ((432, 575, 581, 704), (2, 2)),
        ((610, 575, 674, 704), (1, 2)),
        ((712, 576, 803, 704), (2, 2)),
        ((845, 577, 944, 704), (2, 2)),
        ((954, 575, 1044, 704), (2, 2)),
        ((1055, 575, 1124, 704), (1, 2)),
        ((1138, 575, 1222, 704), (2, 2)),
        ((17, 722, 116, 831), (2, 2)),
        ((127, 722, 250, 831), (2, 2)),
        ((289, 722, 367, 831), (1, 2)),
        ((410, 724, 454, 831), (1, 1)),
        ((471, 724, 524, 831), (1, 1)),
        ((538, 724, 584, 831), (1, 1)),
        ((611, 724, 667, 831), (1, 1)),
        ((713, 722, 773, 831), (1, 2)),
        ((780, 722, 818, 831), (1, 1)),
        ((847, 722, 922, 831), (1, 1)),
        ((945, 721, 1017, 831), (1, 1)),
        ((1035, 721, 1108, 831), (1, 1)),
        ((1125, 721, 1194, 831), (1, 1)),
        ((15, 858, 66, 932), (1, 1)),
        ((75, 858, 124, 932), (1, 1)),
        ((129, 859, 202, 932), (1, 1)),
        ((217, 859, 291, 932), (1, 1)),
        ((305, 859, 373, 932), (1, 1)),
        ((393, 859, 484, 932), (1, 1)),
        ((506, 859, 594, 932), (1, 1)),
        ((628, 859, 701, 932), (1, 1)),
        ((712, 858, 773, 932), (1, 1)),
        ((787, 858, 849, 932), (1, 1)),
        ((906, 858, 983, 932), (1, 1)),
        ((999, 858, 1096, 932), (1, 1)),
        ((22, 974, 112, 1068), (1, 1)),
        ((146, 974, 227, 1068), (1, 1)),
        ((253, 974, 348, 1068), (1, 1)),
        ((412, 973, 616, 1069), (2, 1)),
        ((641, 973, 844, 1069), (2, 1)),
        ((710, 973, 803, 1069), (1, 1)),
        ((832, 973, 882, 1069), (1, 1)),
        ((892, 973, 943, 1069), (1, 1)),
        ((958, 973, 1011, 1069), (1, 1)),
        ((1054, 973, 1093, 1069), (1, 1)),
        ((1110, 973, 1161, 1069), (1, 1)),
        ((49, 1135, 113, 1225), (1, 1)),
        ((145, 1135, 212, 1225), (1, 1)),
        ((252, 1135, 323, 1225), (1, 1)),
        ((365, 1135, 453, 1225), (1, 1)),
        ((497, 1135, 564, 1225), (1, 1)),
        ((583, 1135, 654, 1225), (1, 1)),
        ((713, 1135, 793, 1225), (1, 1)),
        ((814, 1135, 885, 1225), (1, 1)),
        ((929, 1135, 979, 1225), (1, 1)),
        ((1009, 1135, 1064, 1225), (1, 1)),
        ((1116, 1135, 1175, 1225), (1, 1)),
    ]

    x, y = 0, 4
    for box, cells in props:
        if x + cells[0] > COLS:
            x = 0
            y += 2
        if y + cells[1] > ROWS:
            break
        paste(atlas, crop(src, box, cells=cells), x, y)
        x += cells[0]

    atlas.save(OUT)
    return atlas


def build_tileset():
    entries = []
    for y in range(ROWS):
        for x in range(COLS):
            entries.append(f"{x}:{y}/0 = 0")
            if y in (1, 2, 3) or (y >= 4 and x < 12):
                entries.append(
                    f"{x}:{y}/0/physics_layer_0/polygon_0/points = "
                    "PackedVector2Array(-16, -16, 16, -16, 16, 16, -16, 16)"
                )
    TILESET.write_text(
        f"""[gd_resource type="TileSet" load_steps=3 format=3]

[ext_resource type="Texture2D" path="res://Art/Sprites/GeneratedModernOffice25D_TileSheet_32px.png" id="1_modern_generated32"]

[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_modern_generated32"]
texture = ExtResource("1_modern_generated32")
texture_region_size = Vector2i(32, 32)
{chr(10).join(entries)}

[resource]
tile_size = Vector2i(32, 32)
physics_layer_0/collision_layer = 1
sources/0 = SubResource("TileSetAtlasSource_modern_generated32")
""",
        encoding="utf-8",
    )


def build_preview(atlas):
    w, h = 32, 18
    preview = Image.new("RGBA", (w * TILE, h * TILE), (7, 8, 8, 255))

    def tile(tx, ty):
        return atlas.crop((tx * TILE, ty * TILE, tx * TILE + TILE, ty * TILE + TILE))

    def p(tx, ty, gx, gy):
        preview.alpha_composite(tile(tx, ty), (gx * TILE, gy * TILE))

    for gy in range(5, 10):
        for gx in range(3, 26):
            p((gx + gy) % 6, 0, gx, gy)
    for gy in range(12, 15):
        for gx in range(8, 23):
            p((gx + gy) % 6, 0, gx, gy)
    for gx in range(3, 26):
        p(gx % 8, 1, gx, 3)
        p(gx % 8, 2, gx, 4)
    for gx in range(8, 23):
        p(gx % 8, 1, gx, 10)
        p(gx % 8, 2, gx, 11)
    for gx in range(3, 15):
        p(gx % 8, 3, gx, 10)
    for gx in range(18, 26):
        p(gx % 8, 3, gx, 10)
    for gx in range(8, 23):
        p(gx % 8, 3, gx, 15)

    for tx, ty, gx, gy in [
        (1, 4, 6, 6), (3, 4, 10, 6), (7, 4, 17, 6),
        (9, 4, 21, 6), (13, 4, 9, 13), (15, 4, 15, 13),
        (0, 6, 19, 13), (4, 6, 12, 14), (10, 6, 5, 8),
    ]:
        p(tx, ty, gx, gy)

    preview = ImageEnhance.Contrast(preview).enhance(0.96)
    preview.save(PREVIEW)


def main():
    atlas = build_atlas()
    build_tileset()
    build_preview(atlas)
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"Wrote {PREVIEW.relative_to(ROOT)}")
    print(f"Wrote {TILESET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
