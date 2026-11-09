# Grid fin geometry: thesis AR12 fin scaled to Falcon 9 size

Status: DRAFT, not frozen. Every value below is an assumption until the engineer confirms it.

## Reference data (public)

| Item | Value | Source | Reliability |
|---|---|---|---|
| Falcon 9 body diameter | 3.7 m (3.66 m commonly quoted) | SpaceX Falcon user's guide | Official |
| Aluminium grid fin, overall size | 157.5 x 123.2 x 39.4 cm (L x W x H) | [Smithsonian NASM, A20220607000](https://airandspace.si.edu/collection-objects/grid-fin-rocket-launch-vehicle-falcon-9/nasm_A20220607000) | Measured museum object; H likely includes mounting hardware |
| Titanium grid fin, size | about 1.5 x 1.2 m | [spacelaunchlive.com](https://spacelaunchlive.com/recovery/falcon-9-grid-fins/) | Secondary, unverified |
| Titanium grid fin, mass | about 70 kg | Same as above | Secondary, unverified; use only as a sanity check |
| Fins per booster | 4, X pattern, at the interstage | NASM, SpaceX press material | Official |
| Cell size, web thickness, lattice depth | Not published | - | - |

## Thesis fin (Fig 23, M.Tech thesis)

| Dimension | Thesis value |
|---|---|
| Span (root to tip, outward from body) | 60 mm |
| Height (length of root edge) | 40.6 mm |
| Chord (lattice depth along the flow) | 5 mm |
| Aspect ratio = span / chord | 60 / 5 = 12 |
| Web thickness | 0.2 mm |
| Hexagonal cell dimension (as labelled) | 9.8 mm |

Cell layout measured from the Fig 23 pixels: 16 regular flat-top hexagons in 7 columns of
1, 2, 3, 4, 3, 2, 1 cells. The 9.8 mm label is the flat-to-flat cell height. With regular
hexagons the span equals 11 cell sides and the height equals 4 flat-to-flat heights, so the
three labelled values do not agree exactly:

| Value held | Span | Height | Flat-to-flat |
|---|---|---|---|
| 60 mm span | 60 | 37.8 | 9.45 |
| 40.6 mm height | 64.5 | 40.6 | 10.15 |
| 9.8 mm cell | 62.2 | 39.2 | 9.8 |

Confirm the true values from the thesis CAD.

## Scaled fin (span 1500 mm, aspect ratio 12 held)

Span and aspect ratio are held fixed (span matches the about 1.5 m Falcon fin, aspect ratio
12 links to the thesis CFD); the cell size follows from the span. Dimensions are to wall
centrelines.

| Dimension | Thesis equivalent | Scaled | Basis |
|---|---|---|---|
| Span (vertex to vertex) | 60 mm | 1500 mm | Matches Falcon fin size |
| Chord (lattice depth) | 5 mm | 125 mm | Span / 12 |
| Hexagon side | 5.45 mm | 136.4 mm | Span / 11 |
| Flat-to-flat cell height | 9.45 mm | 236.2 mm | sqrt(3) x side |
| Column pitch | 8.18 mm | 204.5 mm | 1.5 x side |
| Height (root edge) | 37.8 mm | 944.8 mm | 4 x flat-to-flat; Falcon fin is about 1200 mm |
| Web thickness | 0.2 mm | 5.0 mm | Thesis x 25; check against aerodynamic load in Abaqus |
| Clear flat-to-flat inside a cell | - | 231.2 mm | Flat-to-flat minus web |
| Number and layout of cells | Fig 23 | Same | 16 cells, columns 1-2-3-4-3-2-1 |
| Material | - | Ti-6Al-4V, density 4430 kg/m^3 | Engineer's choice |

Ratios kept from the thesis: web thickness / chord = 0.04, span / chord = 12.

Rough mass of the lattice walls alone: density x web thickness x chord x total centreline wall
length = 4430 x 0.005 x 0.125 x 8.59 m = about 24 kg. Take the actual value from CATIA.

Drawing: `cad/fin_sketch_falcon_scale.png`. Lattice centrelines for sketch import:
`cad/fin_lattice_falcon_scale.dxf` (mm, layers LATTICE_CENTRELINES, ROOT_PLATE, STEERING_AXIS).

Open item: in the thesis layout the lattice meets the root edge at a single vertex, so the
root connection (stub ribs from the root plate or an outer frame as on Falcon) still has to
be designed.

## Root hardware (new design, placeholders to size later)

| Part | Starting value | To be sized from |
|---|---|---|
| Root plate | 944.8 x 125 mm, 20 mm thick | Hinge moment at peak dynamic pressure |
| Steering shaft (angle of attack axis, along the span, at mid root height) | 80 mm diameter | Steering moment and bending at the root |
| Deployment hinge pin (axis tangential to the body) | 60 mm diameter | Deployment actuator force and latch load |
| Deployment travel | 0 deg stowed (flat against the body) to 90 deg deployed | Engineer's hinge sketch |
| Steering range | +/-20 deg (unverified public figure) | Confirm or set as a design choice |
| Angle of attack reference | 0 deg = fin plane as drawn in the engineer's sketch | Engineer's sketch |
