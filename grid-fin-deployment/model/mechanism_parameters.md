# Grid fin mechanism, design v2: parameter table (DRAFT, not frozen)

Own design inspired by public Falcon 9 grid fin photos (turntable bearing on the body, hinge fitting,
hydraulic actuator at the fin root, closed outer frame). No value here is SpaceX data. Every value is an
assumption until the engineer confirms it.

Drawings and renders: `cad/v2/` and `cad/v2/mechanism/`. Regenerate with the scripts in `.agent-scripts/`:
`design_v2.py` (geometry, kinematics, 1 g check), `make_drawings_v2.py` (sheets 1 to 5),
`make_render_v2.py` (3D renders), `make_mechanism_detail.py` (mechanism close-ups and part details),
`check_hinge_clearance.py` (fin against bracket clearance over 0 to 90°).

## How the fin moves

| Joint | Between | Axis | Range | Driven by | Used for |
|---|---|---|---|---|---|
| J1 steering | Body to turntable | Radial (along the fin span when deployed) | ±20° | Sync ring (all four together) | Roll |
| J2 deploy | Turntable bracket to fin | Tangential hinge pin | 0° stowed, 60 to 90° in flight | One piston per fin, under the fin | Pitch and yaw (differential) |

- Stowed (0°), the fin hangs down from the hinge along the body. The piston under the fin pushes it
  up and out to the flight angle. This is the opposite of the earlier draft (tip up), and it follows from
  putting the piston below the fin.
- Roll: all four fins steer by the same angle in the same sense about their own axes.
- Pitch: F1 and F4 (+X side) open more than F2 and F3. Yaw: F1 and F2 (+Y side) open more than F3 and F4.
- Equal deployment on all four fins gives no pitch or yaw moment.
- Fins: F1 at 45°, F2 at 135°, F3 at 225°, F4 at 315°.

## Fin (Sheet 1)

| Parameter | Value | Basis |
|---|---|---|
| Span | 1500 mm | Falcon fin size |
| Chord (depth along the flow) | 125 mm | Span / 12 (aspect ratio 12) |
| Tip height | 944.8 mm | 4 cell heights |
| Root height | 400 mm, 45° taper over 272.4 mm | Tapered root like the Falcon fin |
| Hexagon side / flats / column pitch | 136.4 / 236.2 / 204.5 mm | Thesis AR12 cell scaled |
| Cell web | 5 mm | Thesis 0.2 mm × 25 |
| Outer frame | 15 mm | Closes the open edges |
| Root rib | 30 mm | Carries the hinge lugs |
| Hinge lugs | 2 × 40 mm thick, 290 mm apart; block 110 along the span × 145 across the chord | 25 mm wall round the pin bore |
| Hinge axis to root face | 90 mm | Must exceed the cheek boss radius (75) plus clearance |
| Horn clevis (rod eye) | 180 mm from the root face, pin 30 mm below the fin's lower face; 2 plates 18 thick, 38 apart | From the actuator layout search |
| Material | Ti-6Al-4V, 4430 kg/m³ | Engineer's choice |
| Mass estimate | 79.2 kg (lattice 31.5, frame 34.8, root rib 6.6, lugs 6.3) | Hand estimate; take the final value from CATIA |
| CG from the hinge | 851 mm along the span | Hand estimate |

The lattice now fills the closed frame, so the fin has more cells than the 16-cell thesis fin. The
thesis CFD coefficients are therefore an approximation for this fin.

## Root pivot (Sheet 2, parts sheet `mechanism/deploy_4_parts_2d.png`)

| Parameter | Value |
|---|---|
| Steering turntable | 600 mm diameter, 80 mm proud of the wall |
| Steering axis | Radial, 62.5 mm above the hinge (mid-chord of the deployed fin) |
| Steering shaft | 100 mm diameter, passes 150 mm inside the wall |
| Deploy hinge axis | 200 mm from the wall |
| Hinge pin | 60 mm diameter, 444 mm long with collars and retaining nuts; flanged bushings, 5 mm wall |
| Bracket base plate | 30 thick on the turntable face |
| Bracket cheeks | 30 thick, 340 inside / 400 outside, round boss R 75 at the hinge, 815 tall down to the tail |
| Bracket tail | Inside the stowed fin (r < 190 from the wall), carries the anchor pin |
| Lug to cheek side gap | 5 mm (thrust washer) |
| Smallest clearance, fin parts to bracket, 0 to 90° | 8.6 mm (lug corner to base plate at 47.5°) |

## Deployment (Sheet 3, `mechanism/deploy_*`)

| Parameter | Value |
|---|---|
| Piston anchor | Bracket tail, 80 mm from the wall, 790 mm below the hinge; pin 30 mm diameter |
| Piston | Linear hydraulic, 60 mm barrel, pushes to open |
| Cylinder length / rod | 478 mm from the anchor pin / rod 30 mm diameter, 50 mm out stowed, 376 mm out at 90° |
| Pin-to-pin length | 528 mm stowed, 588 at 30°, 714 at 60°, 785 at 75°, 854 at 90° |
| Stroke | 326 mm |
| Lever arm about the hinge | 16.5 mm stowed (smallest), 197 at 30°, 269 at 60°, 270 at 75°, 254 at 90° |
| Nominal deploy angle | 75° (operating range 60 to 90°) |
| Fin tip radius | 3640 mm from the booster axis when deployed |
| Bore / supply pressure | 48 mm / 207 bar (3000 psi): push 37.5 kN, pull 22.8 kN |

1 g check (booster upright, fin weight only, not a flight load):

| Deploy angle | Hinge moment | Piston force |
|---|---|---|
| 0° | 49 N·m | 2.95 kN |
| 30° | 373 N·m | 1.89 kN |
| 60° | 597 N·m | 2.22 kN |
| 75° | 652 N·m | 2.42 kN |
| 90° | 662 N·m | 2.61 kN |

Notes on the piston-below layout:

- The space between the wall and the stowed fin is 200 mm, so the piston starts almost in line with the
  hinge. A lever arm larger than 16.5 mm at stowed is not reachable with the hinge at 200 mm from the
  wall; moving the hinge to 250 mm gives about 21 mm. The starting moment is small (49 N·m at 1 g), but
  pin clearance at the start should be kept tight.
- In descent the air load pushes the fin tip up, past 90°. The piston then works mostly in tension and
  holds the fin against the air load; it pushes only while deploying.

## Roll sync ring (Sheet 4)

| Parameter | Value |
|---|---|
| Ring mean radius | 1600 mm, box section 120 × 80 mm |
| Ring support | 8 guide rollers (radius 40) on the ring inner face, hung from a ring frame |
| Ring frame | Flange 40 thick, from R 1440 to the inner wall, 100 mm above the ring centre plane (clear of the levers) |
| Steering shaft inner bearing | Housing 180 × 180, 70 deep, on the inner wall face |
| Lever on each steering shaft | 150 mm, at 1700 mm radius |
| Link | 250 mm, spherical joints at both ends |
| Ring rotation for ±20° steer | ∓1.72 to 1.73° (±51 mm of travel at the lever radius); positive steer needs negative ring rotation |
| Ring drive | 2 tangential actuators at 0° and 180° |

## Still to check

- Hinge moment and steering moment at peak dynamic pressure (from public Falcon telemetry),
  then size the pistons, pins, cheeks, shaft and turntable bearing. The bore and pressure above are
  placeholders until then.
- Sign and size of the pitch moment from differential deployment, using the thesis
  angle-of-attack data (confirm which axis the thesis angle of attack was measured about).
- Hanging stow (fin tip down along the interstage) and the 60 to 90° operating range.
