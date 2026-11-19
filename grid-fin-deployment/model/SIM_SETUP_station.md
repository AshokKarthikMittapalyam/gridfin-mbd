# Multibody model setup: one fin station, deploy actuation (DRAFT)

Tool: 3DEXPERIENCE SIMULIA multibody (Motion Analysis app, or Multibody Analyst with Simpack). Scope: one fin station (F1) with the
booster as ground, the turntable and bracket, the fin, the deploy cylinder and the rod. Roll ring
not included yet. All values are draft assumptions until the engineer confirms them.

Reference values for every check below: `results/reference/station_reference_1g.csv` and
`results/reference/station_reference_summary.json`, written by `.agent-scripts/station_reference.py`
from `model/station_mass_properties.json`. Put the CATIA mass properties into that JSON file and rerun
the script before comparing results.

Units: CATIA in mm; the solver in SI (m, kg, s, N). Coordinates below are in mm.

## 0. Route in 3DEXPERIENCE

1. **Assembly Design**: insert the parts and fix the booster, then create the engineering connections in the
   table below.
2. **Mechanical Systems Design**: create the mechanism from the engineering connections. Check that it has 1 DOF
   with the piston-length command, move it from 0 to 326.5 mm, and run a clash check (smallest clearance expected
   8.6 mm, lug to base plate near 47.5°).
3. **Dynamics**: either **Motion Analysis** (Motion Analyst role, native in the platform) or **Multibody
   Analyst** (Simpack connector: save the product structure to Simpack and build the model there). Both take the
   joints from step 2. Add the gravity, force elements, sensors and runs below.

| Engineering connection | Parts | Built from | Type |
|---|---|---|---|
| EC0 | Booster ↔ Bracket | Turntable face on the race, steering axis | Rigid for now (revolute about the steering axis later, for K2) |
| EC1 | Bracket ↔ Fin | Hinge bores coaxial, lug face to cheek-side washer plane | Revolute, angle command 0 to 90° |
| EC2 | Bracket ↔ Cylinder | Anchor bores coaxial, eye face to the tail mid-plane | Revolute |
| EC3 | Cylinder ↔ Rod | Bore and rod coaxial, plus one plane to stop the rod spinning | Prismatic, length command 0 to 326.5 mm |
| EC4 | Rod ↔ Fin | Rod-eye bore coaxial with the horn pin | Revolute, or the reduced closure in section 4 if redundancy is reported |

## 1. Station frame

- Origin on the wall outer face, at the height of the deploy hinge axis.
- x: radial, outward from the booster axis. y: tangential, y = z × x. z: along the booster axis, up
  (towards the nose; gravity acts along −z for the ground case).
- To place the station in a booster frame, add R 1850 mm along x and rotate by the fin azimuth (F1 at 45°).

## 2. Markers

| Marker | On bodies | Position, stowed θ = 0 (x, y, z) | Position, deployed θ = 90 | Axis |
|---|---|---|---|---|
| S steering axis | Booster, Bracket | (0, 0, 62.5) | same | x |
| H hinge | Bracket, Fin | (200, 0, 0) | same | −y (so θ grows as the fin opens) |
| A anchor pin | Bracket, Cylinder | (80, 0, −790) | same | y |
| B rod eye / horn pin | Rod, Fin | (170, 0, −270) | (470, 0, −30) | y |
| P piston axis | Cylinder, Rod | at A, along A → B | along A → B | A → B |
| Fin CG (check only) | Fin | (262.5, 0, −851) | (1051, 0, 62.5) | - |

If the CATIA assembly is saved in the deployed pose, build in that pose and set the initial
state of J2 to −90° (or rebuild the markers at the stowed pose). Pin-to-pin A–B is 527.7 mm stowed and
854.2 mm deployed.

## 3. Bodies

| Body | Contains | Mass properties |
|---|---|---|
| Booster | Ground (fixed) for this model | - |
| Bracket | Turntable, base plate, cheeks, tail, inner steering shaft and lever (one rigid body) | CATIA |
| Fin | Lattice, frame, root rib, lugs, horn clevis | CATIA (estimate 79.2 kg, CG 851 mm from the hinge, I about the hinge 79.5 kg·m²) |
| Cylinder | Barrel, caps, anchor eye, ports | CATIA (estimate 5.3 kg) |
| Rod | Rod, piston, rod eye | CATIA (estimate 3.5 kg) |

Pins, bushings and collars: add their mass to the body they are pressed into.

## 4. Joints and the loop closure

The fin, cylinder and rod form a closed planar loop. Build the tree with joints J1 to J4 and close the
loop with one constraint, C1.

| ID | From → to | Type | Marker | Notes |
|---|---|---|---|---|
| J1 | Booster → Bracket | Revolute about x | S | Locked (0 DOF) for runs K1, Q1, D1; free with an excitation for K2 |
| J2 | Bracket → Fin | Revolute | H | State θ, 0 stowed to 90° open |
| J3 | Bracket → Cylinder | Revolute | A | Follows the loop |
| J4 | Cylinder → Rod | Prismatic along A → B | P | State s, 0 stowed to 326.5 mm |
| C1 | Rod ↔ Fin | Constraint at B: lock the two in-plane translations only (x and z of a marker whose y is the pin axis) | B | Closes the loop |

Why C1 locks only two directions: all pin axes are parallel, so the loop is planar. A full revolute or
spherical closure adds one to three redundant constraint equations. The solver then reports redundancy and
the pin reactions split arbitrarily. With two locked directions the model has exactly 1 DOF (with J1 locked).
Out-of-plane pin loads are then carried by J2 and J3; revisit this when steering and air loads are added.

## 5. Force elements

| ID | Acts on | Law | Values (assumptions) | Used in |
|---|---|---|---|---|
| Gravity | All bodies | −z | 9.81 m/s² (booster upright, ground deployment test) | Q1, D1 |
| FE1 actuator | J4, along the piston axis | F = F_supply − c_v · ṡ (pressure force minus flow-restriction damping) | F_supply 37.5 kN (207 bar on a 48 mm bore), c_v 150 kN·s/m (no-load speed 0.25 m/s) | D1 |
| FE2 end stops | J4 | One-sided spring-damper at s < 0 (stowed) and s > 326.5 mm (end of stroke); force only while in contact, never pulling | k 5e7 N/m, c 5e4 N·s/m | D1 (and Q1 as a safeguard) |

Hinge friction is left out of this first model.

## 6. Runs

| Run | What | Drive | End time | Output step |
|---|---|---|---|---|
| K1 kinematic | Fin angle against piston length | J4 position excitation s(t) = 326.5 mm · (1 − cos(π t / 10)) / 2, gravity off | 10 s | 10 ms |
| Q1 quasi-static 1 g | Piston force to hold the fin weight | Same drive as K1, gravity on (slow enough that inertia forces are negligible) | 10 s | 10 ms |
| D1 dynamic deploy | Deploy time, stop impact, pin loads | J4 free, FE1 and FE2 on, gravity on, start at s = 0 at rest | 2 s | 0.1 ms (the stop contact lasts about 15 ms) |
| K2 steering (later) | Steering does not change the piston length | J1 excitation ±20°, J4 held at 75° | 10 s | 10 ms |

Solver: the default SIMPACK DAE integrator with a relative tolerance of 1e-6. Limit the maximum step to
1e-4 s in D1 so the end-stop contact is resolved.

## 7. Outputs to export (CSV, SI units, time in the first column)

- J2: θ, θ̇; J4: s, ṡ.
- J4 force along the axis: the constraint force in K1 and Q1, the force from FE1 and FE2 in D1.
- J2 reaction forces and moments in the bracket frame (hinge pin load).
- J3 reaction (anchor pin load) and C1 constraint forces (rod-eye pin load).
- FE2 force and deflection.
- Energies if available: kinetic, gravity potential, FE1 work, FE2 dissipation.

Save the exports as `results/K1/`, `results/Q1/` and `results/D1/`.

## 8. Checks (pass criteria)

| Run | Check | Reference | Pass |
|---|---|---|---|
| K1 | θ against s | `station_reference_1g.csv`: s 18.0 / 59.9 / 118.7 / 186.7 / 257.7 / 326.5 mm at θ 15 / 30 / 45 / 60 / 75 / 90° | within 0.1° |
| K1 | Lever arm ds/dθ | 16.5 mm at 0°, 197 at 30°, 269 at 60°, 254 at 90° | within 1% |
| Q1 | J4 force | 2.86 kN at 0°, 1.91 at 30°, 2.25 at 60°, 2.45 at 75°, 2.64 at 90° (estimated masses; rerun the script with the CATIA masses) | within 2% |
| Q1 | J2 reaction | Fin weight plus the actuator force vector, by hand at 0° and 90° | within 2% |
| D1 | Deploy time 0 to 90° | 1.39 s (quasi-steady hand estimate) | within 5% |
| D1 | Piston speed at the stop | 0.232 m/s | within 5% |
| D1 | End stop | Penetration about 1.2 mm, peak force about 95 kN (one-mass estimate; the multibody value will differ) | same order |
| D1 | Energy balance | FE1 work = Δ gravity PE + kinetic energy + FE2 dissipation | within 1% |

A peak stop force about 2.5 times the supply force means the cylinder needs end-of-stroke cushioning.
That becomes the first design question after D1 runs.

## 9. Next

1. Send the CATIA mass properties (fin, bracket, cylinder, rod: mass, CG, inertia about the CG) to update
   `station_mass_properties.json`, then rerun `station_reference.py`.
2. After K1, Q1 and D1 are exported, a comparison script plots the multibody results against the reference.
3. Then: K2 steering, the aerodynamic hinge moment, end-of-stroke cushioning, the four-fin model, and the roll ring.
