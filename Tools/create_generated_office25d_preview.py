from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Art" / "Sprites" / "GeneratedModernOffice25D_TileSheet.png"
OUT = ROOT / "Art" / "Sprites" / "GeneratedModernOffice25D_Preview.png"
TILE = 48


def crop(src, box, size=(TILE, TILE), make_alpha=False):
    piece = src.crop(box).convert("RGBA")
    if make_alpha:
        bg = piece.getpixel((0, 0))[:3]
        pix = piece.load()
        for y in range(piece.height):
            for x in range(piece.width):
                r, g, b, a = pix[x, y]
                dist = abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2])
                if dist < 34 and max(r, g, b) < 42:
                    pix[x, y] = (r, g, b, 0)
    return piece.resize(size, Image.Resampling.NEAREST)


def paste(canvas, piece, gx, gy):
    canvas.alpha_composite(piece, (gx * TILE, gy * TILE))


def fill(canvas, tile, x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            paste(canvas, tile, x, y)


def add_glow(canvas, cells):
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(glow, "RGBA")
    for gx, gy in cells:
        cx = gx * TILE + TILE // 2
        cy = gy * TILE + TILE // 2
        for radius, alpha in [(120, 7), (84, 10), (52, 16), (26, 22)]:
            d.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(226, 180, 90, alpha))
    canvas.alpha_composite(glow)


def main():
    src = Image.open(SRC).convert("RGBA")

    # Approximate crops from the generated atlas. The source is AI-generated and not a
    # strict 32px grid, so this preview is intentionally illustrative rather than tile-perfect.
    floor_dark = crop(src, (98, 14, 178, 128))
    floor_scuffed = crop(src, (187, 14, 267, 128))
    floor_tile = crop(src, (274, 139, 357, 253))
    wall_top = crop(src, (535, 14, 624, 128), make_alpha=True)
    wall_face = crop(src, (535, 139, 624, 253), make_alpha=True)
    wall_corner = crop(src, (889, 14, 981, 128), make_alpha=True)
    wall_door = crop(src, (887, 267, 981, 379), make_alpha=True)
    wall_glass = crop(src, (987, 267, 1079, 379), make_alpha=True)
    desk = crop(src, (88, 575, 180, 704), make_alpha=True)
    cubicle = crop(src, (16, 722, 116, 831), make_alpha=True)
    chair = crop(src, (410, 724, 454, 831), make_alpha=True)
    server = crop(src, (712, 576, 803, 704), make_alpha=True)
    copier = crop(src, (845, 577, 944, 704), make_alpha=True)
    cabinet = crop(src, (954, 575, 1044, 704), make_alpha=True)
    plant = crop(src, (945, 721, 1017, 831), make_alpha=True)
    papers = crop(src, (129, 859, 202, 932), make_alpha=True)
    boxes = crop(src, (393, 859, 484, 932), make_alpha=True)
    lamp = crop(src, (710, 973, 803, 1069), make_alpha=True)
    notice = crop(src, (412, 973, 616, 1069), size=(TILE * 2, TILE), make_alpha=True)

    w, h = 30, 18
    canvas = Image.new("RGBA", (w * TILE, h * TILE), (7, 8, 8, 255))

    fill(canvas, floor_dark, 3, 5, 24, 9)
    fill(canvas, floor_dark, 8, 12, 21, 15)
    fill(canvas, floor_tile, 24, 6, 27, 9)

    for x in range(3, 25):
        paste(canvas, wall_top, x, 3)
        paste(canvas, wall_face, x, 4)
    for x in range(8, 22):
        paste(canvas, wall_top, x, 10)
        paste(canvas, wall_face, x, 11)
    for x in range(24, 28):
        paste(canvas, wall_top, x, 4)
        paste(canvas, wall_face, x, 5)

    for y in range(5, 10):
        paste(canvas, wall_corner, 2, y)
        paste(canvas, wall_corner, 28, y)
    for y in range(12, 16):
        paste(canvas, wall_corner, 7, y)
        paste(canvas, wall_corner, 22, y)

    paste(canvas, wall_door, 14, 3)
    paste(canvas, wall_glass, 19, 3)
    paste(canvas, wall_door, 25, 4)

    paste(canvas, desk, 6, 6)
    paste(canvas, cubicle, 10, 6)
    paste(canvas, chair, 13, 7)
    paste(canvas, server, 18, 6)
    paste(canvas, copier, 21, 7)
    paste(canvas, cabinet, 25, 7)
    paste(canvas, plant, 16, 13)
    paste(canvas, boxes, 11, 14)
    paste(canvas, papers, 5, 8)
    paste(canvas, notice, 10, 11)
    paste(canvas, lamp, 6, 4)
    paste(canvas, lamp, 16, 4)
    paste(canvas, lamp, 14, 11)

    add_glow(canvas, [(6, 5), (16, 5), (14, 12)])
    canvas = ImageEnhance.Contrast(canvas).enhance(0.96)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
