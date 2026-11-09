# Purpose: draw a dimensioned sketch (PNG) and a lattice centreline DXF of the thesis AR12 grid
# fin scaled to Falcon 9 size, for modelling in CATIA / 3DEXPERIENCE.
# Request: "generate a sketch based on generated falcon size so that i can have an idea with
# dimensions"
#
# Layout from thesis Fig 23 (measured from pixels): 16 flat-top regular hexagons in 7 columns
# with 1, 2, 3, 4, 3, 2, 1 cells. Span (vertex to vertex) = 11 x cell side.
# All values are DRAFT assumptions until the engineer confirms them.
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SPAN = 1500.0  # mm, matches the about 1.5 m Falcon fin
CHORD = SPAN / 12  # mm, aspect ratio 12
WEB = 5.0  # mm, thesis 0.2 mm x 25
ROOT_PLATE = 20.0  # mm, placeholder
BODY_D = 3700.0  # mm, Falcon 9

A = SPAN / 11  # hexagon side (wall centreline)
H = math.sqrt(3) * A  # flat-to-flat (wall centreline)
PITCH = 1.5 * A  # column pitch
CELLS_PER_COL = [1, 2, 3, 4, 3, 2, 1]
HEIGHT = 4 * H

OUT_DIR = Path(__file__).resolve().parents[1] / "cad"


def cell_centres():
    centres = []
    for i, n in enumerate(CELLS_PER_COL):
        cx = A + i * PITCH
        first = (HEIGHT - n * H) / 2 + H / 2
        centres += [(cx, first + k * H) for k in range(n)]
    return centres


def hex_vertices(cx, cy):
    return [(cx + A * math.cos(math.radians(t)), cy + A * math.sin(math.radians(t)))
            for t in range(0, 360, 60)]


def lattice_edges():
    edges = set()
    for cx, cy in cell_centres():
        v = hex_vertices(cx, cy)
        for j in range(6):
            p, q = v[j], v[(j + 1) % 6]
            key = tuple(sorted([(round(p[0], 3), round(p[1], 3)), (round(q[0], 3), round(q[1], 3))]))
            edges.add(key)
    return sorted(edges)


def font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default(size=size)


F_TITLE, F_DIM, F_NOTE, F_SMALL = font(40), font(26), font(24), font(21)
BLACK, GREY, BLUE, RED = (0, 0, 0), (150, 150, 150), (20, 70, 200), (200, 30, 30)


def arrow_head(d, tip, direction, size=14, colour=BLUE):
    ux, uy = direction
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    px, py = -uy, ux
    base = (tip[0] - ux * size, tip[1] - uy * size)
    d.polygon([tip, (base[0] + px * size * 0.4, base[1] + py * size * 0.4),
               (base[0] - px * size * 0.4, base[1] - py * size * 0.4)], fill=colour)


def dim(d, p, q, text, offset_text=(0, 0), colour=BLUE, rotate=False):
    d.line([p, q], fill=colour, width=2)
    arrow_head(d, p, (p[0] - q[0], p[1] - q[1]), colour=colour)
    arrow_head(d, q, (q[0] - p[0], q[1] - p[1]), colour=colour)
    mx, my = (p[0] + q[0]) / 2 + offset_text[0], (p[1] + q[1]) / 2 + offset_text[1]
    if rotate:
        tw, th = d.textbbox((0, 0), text, font=F_DIM)[2:]
        tmp = Image.new("RGBA", (tw + 6, th + 6), (255, 255, 255, 0))
        ImageDraw.Draw(tmp).text((3, 0), text, font=F_DIM, fill=colour)
        tmp = tmp.rotate(90, expand=True)
        d._image.paste(tmp, (int(mx - tmp.width / 2), int(my - tmp.height / 2)), tmp)
    else:
        d.text((mx, my), text, font=F_DIM, fill=colour, anchor="mm")


def ext(d, p, q):
    d.line([p, q], fill=GREY, width=1)


def dashed(d, p, q, colour=GREY, dash=12, gap=8, width=2):
    length = math.hypot(q[0] - p[0], q[1] - p[1])
    ux, uy = (q[0] - p[0]) / length, (q[1] - p[1]) / length
    s = 0.0
    while s < length:
        e = min(s + dash, length)
        d.line([(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)], fill=colour, width=width)
        s = e + gap


def draw_png(path):
    img = Image.new("RGB", (2600, 1900), "white")
    d = ImageDraw.Draw(img)
    d._image = img
    d.text((60, 30), "AR12 hexagonal grid fin, thesis Fig 23 scaled to Falcon 9 size (DRAFT, all mm)",
           font=F_TITLE, fill=BLACK)

    # Front view: looking along the flow (along the booster axis)
    s, ox, oy = 0.9, 260, 230

    def fv(x, y):
        return ox + x * s, oy + y * s

    d.text((ox, oy - 110), "FRONT VIEW (looking along the flow)", font=F_NOTE, fill=BLACK)
    d.rectangle([fv(-ROOT_PLATE, 0), fv(0, HEIGHT)], fill=(210, 210, 210), outline=BLACK, width=2)
    for p, q in lattice_edges():
        d.line([fv(*p), fv(*q)], fill=BLACK, width=max(2, round(WEB * s)))
    # Steering (angle of attack) axis through mid root height, along the span
    y_mid = HEIGHT / 2
    dashed(d, fv(-120, y_mid), fv(SPAN + 60, y_mid), colour=RED, dash=30, gap=10)
    d.text(fv(SPAN + 70, y_mid), "steering (AoA) axis", font=F_SMALL, fill=RED, anchor="lm")
    d.ellipse([fv(-ROOT_PLATE / 2 - 40, y_mid - 40), fv(-ROOT_PLATE / 2 + 40, y_mid + 40)], outline=RED, width=3)
    d.text(fv(-ROOT_PLATE - 10, HEIGHT + 40), "root plate 20 thk + steering shaft dia 80 (placeholders)",
           font=F_SMALL, fill=BLACK)
    d.text(fv(-ROOT_PLATE - 10, HEIGHT + 75), "deployment hinge axis runs along the root edge (tangential to body)",
           font=F_SMALL, fill=BLACK)

    # Span
    ext(d, fv(0, -10), fv(0, -70))
    ext(d, fv(SPAN, HEIGHT / 2 - 10), fv(SPAN, -70))
    dim(d, fv(0, -55), fv(SPAN, -55), "span 1500  (aspect ratio 1500 / 125 = 12)", offset_text=(0, -22))
    # Height
    ext(d, fv(3 * PITCH, 0), fv(-150, 0))
    ext(d, fv(3 * PITCH, HEIGHT), fv(-150, HEIGHT))
    dim(d, fv(-135, 0), fv(-135, HEIGHT), f"height {HEIGHT:.1f}", offset_text=(-28, 0), rotate=True)
    # Column pitch along the bottom between cell centres
    yb = HEIGHT + 130
    for i in (5, 6):
        ext(d, fv(A + i * PITCH, HEIGHT / 2), fv(A + i * PITCH, yb + 10))
    dim(d, fv(A + 5 * PITCH, yb), fv(A + 6 * PITCH, yb), f"pitch {PITCH:.1f}", offset_text=(0, 26))
    d.text(fv(0, HEIGHT + 200), "16 cells, columns of 1-2-3-4-3-2-1 cells", font=F_SMALL, fill=BLACK)
    d.text(fv(0, HEIGHT + 235), "OPEN ITEM: lattice meets the root plate at one vertex only; root connection "
           "(stub ribs or outer frame) to design", font=F_SMALL, fill=RED)

    # Edge view: looking at the leading edge, shows chord (lattice depth)
    ey = oy + HEIGHT * s + 330
    se = 0.9

    def ev(x, y):
        return ox + x * se, ey + y * se

    d.text((ox, ey - 75), "EDGE VIEW (flow from below during descent)", font=F_NOTE, fill=BLACK)
    d.rectangle([ev(-ROOT_PLATE, 0), ev(0, CHORD)], fill=(210, 210, 210), outline=BLACK, width=2)
    d.rectangle([ev(0, 0), ev(SPAN, CHORD)], outline=BLACK, width=3)
    xs = sorted({round(x, 1) for e in lattice_edges() for x, _ in e})
    for x in xs[1:-1]:
        dashed(d, ev(x, 0), ev(x, CHORD), dash=8, gap=6)
    ext(d, ev(SPAN, 0), ev(SPAN + 70, 0))
    ext(d, ev(SPAN, CHORD), ev(SPAN + 70, CHORD))
    dim(d, ev(SPAN + 55, 0), ev(SPAN + 55, CHORD), "chord 125", offset_text=(70, 0))
    for k in range(3):
        x = 300 + k * 450
        d.line([ev(x, CHORD + 140), ev(x, CHORD + 30)], fill=RED, width=3)
        arrow_head(d, ev(x, CHORD + 30), (0, -1), colour=RED)
    d.text(ev(SPAN / 2, CHORD + 165), "relative wind", font=F_SMALL, fill=RED, anchor="mm")

    # Cell detail
    cx0, cy0, sc = 2050, 400, 1.6
    d.text((1720, 100), "CELL DETAIL (x1.8 of front view)", font=F_NOTE, fill=BLACK)
    vin = hex_vertices(0, 0)
    pts = [(cx0 + x * sc, cy0 + y * sc) for x, y in vin]
    d.polygon(pts, outline=BLACK, width=round(WEB * sc * 2))
    # side length on top edge
    p, q = pts[5], pts[4]
    dim(d, (q[0], q[1] - 40), (p[0], p[1] - 40), f"side {A:.1f}", offset_text=(0, -22))
    ext(d, q, (q[0], q[1] - 55))
    ext(d, p, (p[0], p[1] - 55))
    # flat to flat
    xr = cx0 + A * sc + 50
    ext(d, pts[5], (xr + 15, pts[5][1]))
    ext(d, pts[1], (xr + 15, pts[1][1]))
    dim(d, (xr, pts[5][1]), (xr, pts[1][1]), f"flats {H:.1f}", offset_text=(70, 0))
    d.text((1720, 700), f"wall thickness (web) {WEB:.1f}", font=F_DIM, fill=BLUE)
    d.text((1720, 740), "dimensions to wall centrelines", font=F_SMALL, fill=BLACK)
    d.text((1720, 770), f"clear flat-to-flat inside a cell {H - WEB:.1f}", font=F_SMALL, fill=BLACK)
    d.text((1720, 800), "web / chord = 0.04 (same as thesis)", font=F_SMALL, fill=BLACK)

    # Installation on the booster (side elevation)
    si, bx, by = 0.11, 1820, 1180
    d.text((1720, 880), "ON THE BOOSTER (side elevation, x0.12)", font=F_NOTE, fill=BLACK)
    r = BODY_D / 2 * si
    dashed(d, (bx, by - 260), (bx, by + 560), colour=GREY, dash=30, gap=10, width=1)
    d.line([(bx + r, by - 260), (bx + r, by + 560)], fill=BLACK, width=3)
    d.text((bx + 8, by - 255), "booster axis", font=F_SMALL, fill=GREY)
    d.text((bx + r + 8, by - 255), "body wall", font=F_SMALL, fill=BLACK)
    dim(d, (bx, by + 520), (bx + r, by + 520), "R 1850 (dia 3700)", offset_text=(0, 26))
    hinge = (bx + r, by)
    d.rectangle([hinge, (hinge[0] + SPAN * si, hinge[1] + CHORD * si)], outline=BLACK, width=3, fill=(230, 230, 230))
    d.text((hinge[0] + SPAN * si / 2, hinge[1] + CHORD * si + 25), "deployed (90 deg)", font=F_SMALL, fill=BLACK, anchor="mm")
    d.rectangle([(hinge[0], hinge[1] - SPAN * si), (hinge[0] + CHORD * si, hinge[1])], outline=GREY, width=2)
    d.text((hinge[0] + CHORD * si + 10, hinge[1] - SPAN * si + 10), "stowed (0 deg)", font=F_SMALL, fill=GREY)
    d.arc([hinge[0] - 120, hinge[1] - 120, hinge[0] + 120, hinge[1] + 120], start=-90, end=0, fill=RED, width=3)
    d.ellipse([hinge[0] - 7, hinge[1] - 7, hinge[0] + 7, hinge[1] + 7], fill=RED)
    d.text((hinge[0] + 95, hinge[1] - 125), "hinge, 90 deg travel", font=F_SMALL, fill=RED)
    d.text((1720, by + 600), "4 fins in X pattern at the interstage.", font=F_SMALL, fill=BLACK)
    d.text((1720, by + 630), "Stow direction (tip up) is an assumption:", font=F_SMALL, fill=BLACK)
    d.text((1720, by + 660), "check against your hinge sketch.", font=F_SMALL, fill=BLACK)

    img.save(path)


def write_dxf(path):
    lines = ["0", "SECTION", "2", "HEADER", "9", "$ACADVER", "1", "AC1009", "9", "$INSUNITS", "70", "4",
             "0", "ENDSEC", "0", "SECTION", "2", "ENTITIES"]

    def line(p, q, layer):
        lines.extend(["0", "LINE", "8", layer, "10", f"{p[0]:.3f}", "20", f"{-p[1]:.3f}", "30", "0.0",
                      "11", f"{q[0]:.3f}", "21", f"{-q[1]:.3f}", "31", "0.0"])

    for p, q in lattice_edges():
        line(p, q, "LATTICE_CENTRELINES")
    corners = [(-ROOT_PLATE, 0), (0, 0), (0, HEIGHT), (-ROOT_PLATE, HEIGHT)]
    for j in range(4):
        line(corners[j], corners[(j + 1) % 4], "ROOT_PLATE")
    line((-ROOT_PLATE - 100, HEIGHT / 2), (SPAN + 100, HEIGHT / 2), "STEERING_AXIS")
    lines.extend(["0", "ENDSEC", "0", "EOF"])
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    draw_png(OUT_DIR / "fin_sketch_falcon_scale.png")
    write_dxf(OUT_DIR / "fin_lattice_falcon_scale.dxf")
    print(f"side {A:.2f}  flats {H:.2f}  pitch {PITCH:.2f}  height {HEIGHT:.2f}  chord {CHORD:.2f}")
    print("edges:", len(lattice_edges()),
          " total wall length m:", round(sum(math.dist(p, q) for p, q in lattice_edges()) / 1000, 3))
    print("written to", OUT_DIR)
