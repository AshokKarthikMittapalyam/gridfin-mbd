# Purpose: measure the hexagon layout in the thesis AR12 grid fin sketch (Fig 23) from pixels,
# to resolve what the 9.8 mm dimension refers to before scaling the fin to Falcon 9 size.
# Request: "give me web thickness and every dimension redesigned to falcon rocket so that i can
# design in 3dexperience"
import sys

from PIL import Image

img = Image.open(sys.argv[1]).convert("L")
w, h = img.size
px = img.load()
print("image size (w, h):", w, h)


def is_dark(x, y):
    return px[x, y] < 128


# Hexagon drawing region (excludes the side view, title and 3D figures)
y0, y1, x0, x1 = 205, 435, 185, 520

print("\nHorizontal segments longer than 15 px (y, x range, length):")
for y in range(y0, y1):
    x = x0
    while x < x1:
        if is_dark(x, y):
            s = x
            while x < x1 and is_dark(x, y):
                x += 1
            if x - s > 15:
                print(f"  y={y:4d}  x={s:4d}..{x - 1:4d}  len={x - s}")
        else:
            x += 1

dark_pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if is_dark(x, y)]
xs = [p[0] for p in dark_pts]
ys = [p[1] for p in dark_pts]
print("\nDark pixel extent: x", min(xs), "..", max(xs), " y", min(ys), "..", max(ys))

# Vertical dimension lines on the left (9.8 and 0.2 labels) and right (40.6 label)
for name, xa, xb in (("left dims", 150, 185), ("right dim", 525, 560)):
    rows = [y for y in range(150, 460) if any(is_dark(x, y) for x in range(xa, xb))]
    print(f"{name}: dark rows {rows[0]}..{rows[-1]}" if rows else f"{name}: none")

# Horizontal extension lines spanning the left dimension region
print("\nRows with long dark runs crossing x=160..185 (extension lines):")
for y in range(150, 460):
    if all(is_dark(x, y) for x in range(165, 180)):
        print("  y =", y)
