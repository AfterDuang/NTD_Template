from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Art" / "Sprites" / "GeneratedIndustrialOffice25D_TileSheet.png"
OUT = ROOT / "Art" / "Sprites" / "GeneratedIndustrialOffice25D_TileSheet_32px.png"
PREVIEW = ROOT / "Art" / "Sprites" / "GeneratedIndustrialOffice25D_Preview_32px.png"
TILESET = ROOT / "Art" / "GeneratedIndustrialOffice25D_TileMap_32px.tres"
TILE = 32
COLS = 16
ROWS = 12


def clear_edge_background(piece, threshold=34):
    """Remove only the near-black background connected to the crop edges."""
    piece = piece.convert("RGBA")
    w, h = piece.size
    pix = piece.load()
    seen = set()
    stack = []

    def is_bg(x, y):
        r, g, b, a = pix[x, y]
        return a > 0 and r < threshold and g < threshold and b < threshold

    for x in range(w):
        stack.append((x, 0))
        stack.append((x, h - 1))
    for y in range(h):
        stack.append((0, y))
        stack.append((w - 1, y))

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
    size = (cells[0] * TILE, cells[1] * TILE)
    return piece.resize(size, Image.Resampling.NEAREST)


def paste(atlas, piece, x, y):
    atlas.alpha_composite(piece, (x * TILE, y * TILE))


def draw_grid(img):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay, "RGBA")
    for x in range(0, img.width + 1, TILE):
        d.line((x, 0, x, img.height), fill=(160, 170, 170, 36))
    for y in range(0, img.height + 1, TILE):
        d.line((0, y, img.width, y), fill=(160, 170, 170, 36))
    img.alpha_composite(overlay)


def build_atlas():
    src = Image.open(SRC).convert("RGBA")
    atlas = Image.new("RGBA", (COLS * TILE, ROWS * TILE), (0, 0, 0, 0))

    # Row 0: full 32x32 floor tiles.
    floors = [
        (16, 18, 141, 176),
        (153, 18, 276, 176),
        (286, 18, 410, 176),
        (420, 18, 541, 176),
        (552, 18, 673, 176),
        (686, 18, 809, 176),
        (820, 18, 942, 176),
        (954, 18, 1073, 176),
        (1084, 18, 1235, 176),
    ]
    for i, box in enumerate(floors):
        paste(atlas, crop(src, box, alpha=False), i, 0)

    # Row 1: thick wall cap tiles. Row 2: matching wall face tiles.
    wall_caps = [
        (16, 199, 103, 266),
        (119, 199, 197, 266),
        (213, 199, 304, 266),
        (322, 199, 410, 266),
        (548, 199, 639, 266),
        (742, 199, 839, 266),
        (1044, 199, 1150, 266),
        (1158, 199, 1239, 266),
    ]
    wall_faces = [
        (16, 279, 103, 410),
        (119, 279, 197, 410),
        (213, 279, 304, 410),
        (322, 279, 410, 410),
        (548, 279, 639, 410),
        (742, 279, 839, 410),
        (1044, 279, 1150, 410),
        (1158, 279, 1239, 410),
    ]
    for i, box in enumerate(wall_caps):
        paste(atlas, crop(src, box), i, 1)
    for i, box in enumerate(wall_faces):
        paste(atlas, crop(src, box), i, 2)

    # Row 3: foreground lower wall lips and side/corner pieces.
    lower_edges = [
        (16, 430, 104, 520),
        (119, 430, 197, 520),
        (213, 430, 305, 520),
        (322, 430, 410, 520),
        (548, 430, 640, 520),
        (742, 430, 840, 520),
        (1044, 430, 1150, 520),
        (1158, 430, 1238, 520),
        (16, 536, 82, 650),
        (82, 536, 160, 650),
        (258, 536, 355, 650),
        (490, 536, 572, 650),
    ]
    for i, box in enumerate(lower_edges[:COLS]):
        paste(atlas, crop(src, box), i, 3)

    # Rows 4-11: props. Multi-cell source props are normalized into 32px cells here.
    props = [
        ((24, 675, 91, 800), (1, 2)),
        ((102, 670, 236, 794), (2, 2)),
        ((261, 670, 409, 795), (2, 2)),
        ((435, 671, 582, 795), (2, 2)),
        ((611, 645, 674, 799), (1, 2)),
        ((714, 647, 765, 802), (1, 2)),
        ((775, 645, 829, 802), (1, 2)),
        ((847, 671, 945, 802), (2, 2)),
        ((1017, 648, 1109, 802), (2, 2)),
        ((1126, 646, 1210, 802), (2, 2)),
        ((38, 816, 83, 901), (1, 1)),
        ((104, 814, 153, 902), (1, 1)),
        ((187, 813, 247, 903), (1, 1)),
        ((590, 838, 639, 925), (1, 1)),
        ((650, 837, 716, 927), (1, 1)),
        ((737, 838, 790, 926), (1, 1)),
        ((807, 837, 844, 927), (1, 1)),
        ((24, 933, 270, 1065), (3, 2)),
        ((292, 935, 454, 1064), (2, 2)),
        ((487, 934, 560, 1067), (1, 2)),
        ((585, 841, 641, 928), (1, 2)),
        ((650, 837, 717, 927), (1, 2)),
        ((728, 941, 785, 1007), (1, 1)),
        ((841, 964, 914, 1038), (1, 1)),
        ((922, 960, 985, 1036), (1, 1)),
        ((1017, 941, 1097, 1035), (1, 1)),
        ((1132, 954, 1207, 1050), (1, 1)),
        ((23, 1108, 100, 1187), (1, 1)),
        ((120, 1110, 195, 1185), (1, 1)),
        ((225, 1112, 275, 1188), (1, 1)),
        ((325, 1110, 373, 1188), (1, 1)),
        ((535, 1111, 596, 1191), (1, 1)),
        ((650, 1110, 760, 1195), (2, 1)),
        ((831, 1110, 881, 1188), (1, 1)),
        ((929, 1110, 979, 1187), (1, 1)),
        ((1011, 1110, 1063, 1188), (1, 1)),
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

    OUT.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(OUT)
    return atlas


def build_tileset():
    entries = []
    blocking_rows = {1, 2, 3}
    for y in range(ROWS):
        for x in range(COLS):
            entries.append(f"{x}:{y}/0 = 0")
            if y in blocking_rows or (y >= 4 and x < 12):
                entries.append(
                    f"{x}:{y}/0/physics_layer_0/polygon_0/points = "
                    "PackedVector2Array(-16, -16, 16, -16, 16, 16, -16, 16)"
                )
    atlas_entries = "\n".join(entries)
    TILESET.write_text(
        f"""[gd_resource type="TileSet" load_steps=3 format=3]

[ext_resource type="Texture2D" path="res://Art/Sprites/GeneratedIndustrialOffice25D_TileSheet_32px.png" id="1_industrial32"]

[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_industrial32"]
texture = ExtResource("1_industrial32")
texture_region_size = Vector2i(32, 32)
{atlas_entries}

[resource]
tile_size = Vector2i(32, 32)
physics_layer_0/collision_layer = 1
sources/0 = SubResource("TileSetAtlasSource_industrial32")
""",
        encoding="utf-8",
    )


def build_preview(atlas):
    w, h = 32, 18
    preview = Image.new("RGBA", (w * TILE, h * TILE), (5, 6, 7, 255))

    def t(tx, ty):
        return atlas.crop((tx * TILE, ty * TILE, tx * TILE + TILE, ty * TILE + TILE))

    def p(tx, ty, gx, gy):
        preview.alpha_composite(t(tx, ty), (gx * TILE, gy * TILE))

    def fill(tx, ty, x0, y0, x1, y1):
        for gy in range(y0, y1 + 1):
            for gx in range(x0, x1 + 1):
                p(tx + ((gx + gy) % 4), ty, gx, gy)

    fill(0, 0, 3, 5, 25, 9)
    fill(0, 0, 8, 12, 22, 15)
    for gx in range(3, 26):
        p(gx % 8, 1, gx, 3)
        p(gx % 8, 2, gx, 4)
    for gx in range(8, 23):
        p(gx % 8, 1, gx, 10)
        p(gx % 8, 2, gx, 11)
    for gx in range(3, 14):
        p(gx % 8, 3, gx, 10)
    for gx in range(17, 26):
        p(gx % 8, 3, gx, 10)
    for gx in range(8, 23):
        p(gx % 8, 3, gx, 16)

    for tx, ty, gx, gy in [
        (1, 4, 6, 6), (3, 4, 11, 6), (7, 4, 18, 6),
        (9, 4, 22, 6), (13, 4, 9, 13), (15, 4, 16, 13),
        (0, 6, 20, 13), (4, 6, 13, 14), (10, 6, 5, 8),
    ]:
        p(tx, ty, gx, gy)

    draw_grid(preview)
    preview = ImageEnhance.Contrast(preview).enhance(0.96)
    preview.save(PREVIEW)


def main():
    atlas = build_atlas()
    build_tileset()
    build_preview(atlas)
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
    print(f"Wrote {PREVIEW.relative_to(ROOT)}")
    print(f"Wrote {TILESET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
