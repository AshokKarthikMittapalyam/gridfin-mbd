# Reading order for the grid fin design (v2)

All current images are in `cad/v2/`. Earlier images in `cad/` and `cad/guide/` are superseded:
they show an open-sided fin and a roll pattern that cancels out.

1. `render0_overview_4views.png`: the whole mechanism in four 3D views.
2. `sheet1_fin.png`: the fin you model first in CATIA.
3. `sheet2_root_pivot.png`: turntable, bracket and hinge that join the fin to the rocket.
4. `sheet3_deployment.png`: deploy actuator and angles (pitch and yaw).
5. `sheet4_roll_sync_ring.png`: the ring inside the interstage that steers all four fins together (roll).
6. `sheet5_control_allocation.png`: which mechanism handles roll, pitch and yaw.

Mechanism close-ups in `cad/v2/mechanism/`:

- `deploy_1_sequence_3d.png`: one fin opening 0°, 30°, 60°, 90° in 3D; the piston under the fin pushes it up.
- `deploy_2_steps_2d.png`: side section of the deploy linkage at each step, piston length, lever arm and 1 g check.
- `deploy_3_from_below_3d.png`: the piston seen from below the fin, at 75° and 90°.
- `deploy_4_parts_2d.png`: part details for CATIA: cylinder section, hinge joint section, cheek profile,
  horn clevis, cylinder capacity.
- `station_exploded_3d.png`: one fin station pulled apart, with the assembly order.
- `roll_1_inside_overview_3d.png`: inside the interstage, ring, links, levers, rollers and ring drives.
- `roll_2_inside_station_3d.png`: one station from inside, steer 0° and +20°.
- `roll_3_linkage_2d.png`: section through a station, inside view at −20°, 0°, +20°, and the ring angle table.

Numbers: `mechanism_parameters.md`.

## CATIA build order

1. Fin part: sketch the outline and cell centrelines from Sheet 1, give the walls their thickness
   (web 5, frame 15, root rib 30), pad 125 mm, add the two hinge lugs and the horn clevis on the
   lower face (parts sheet, detail D).
2. Turntable and bracket part from Sheet 2 and the parts sheet (cheek profile, detail C).
3. Deploy piston: cylinder and rod as two parts (Sheet 3 and the parts sheet, detail A).
4. Sync ring, rollers, levers and links (Sheet 4).
5. Assembly: body, then turntable (radial revolute), then fin (hinge revolute); pattern to 45°,
   135°, 225° and 315°; links to the ring.
6. Export mass properties for the SIMPACK model.
