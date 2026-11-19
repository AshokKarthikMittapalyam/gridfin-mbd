# Design Brief: Grid Fin Deployment Mechanism

> Original brief from the start of the project. The built model is a piston-driven
> slider-crank on a full-scale fin; see the [project page](../README.md) for what was simulated.

## Objective

Simulate the deployment of four folding hexagonal grid fins on a missile body, from the
stowed position (folded flat along the body) to the locked deployed position, and size the
deployment spring and latch so that the fins deploy quickly without overloading the hinge.

## Questions the study answers

1. How long does deployment take, and how does it change with flight speed?
2. What is the impact load on the hinge and stop when a fin latches?
3. Which spring stiffness and preload balance deployment time against latch impact?
4. How much does fin and hinge flexibility change the peak loads compared with a rigid model?

## System description

| Item | Description | Initial value (to refine) |
|---|---|---|
| Missile body | Rigid cylinder, fixed or moving with constant velocity | 150 mm diameter |
| Grid fins | 4 fins, hexagonal cells, aspect ratio taken from the M.Tech thesis | Mass from CAD |
| Hinge | Revolute joint at the fin root, axis tangential to the body | 1 per fin |
| Deployment spring | Torsion spring on the hinge with preload | k = 5 to 50 N·m/rad |
| Hinge damping | Rotational damper (friction and grease) | c = 0.01 to 0.5 N·m·s/rad |
| End stop and latch | Contact force element at the deployed angle, then lock | Stiffness and damping from material |
| Aerodynamic load | Hinge moment versus deployment angle and Mach number | From thesis CFD or a simple model |

## Model build steps

1. **CAD (CATIA):** model the body section, one grid fin, hinge bracket, stop and latch.
   Export mass, centre of gravity and inertia.
2. **Kinematics:** revolute joint per fin, prescribed motion, check clearances and the
   swept volume over the full 0 to 90 degree travel.
3. **Dynamics:** add the torsion spring with preload, the damper and the end-stop contact.
   Release from stowed at t = 0 and record angle, angular velocity and hinge reaction.
4. **Aerodynamic loading:** add the hinge moment as a force element that depends on the
   deployment angle, for Mach 0.5, 0.8, 1.2 and 2.0.
5. **Flexible fin and hinge:** build an Abaqus model of the fin and bracket, run modal
   reduction, import as a flexible body, and compare with the rigid results.
6. **Parameter study:** sweep spring stiffness and preload. Plot deployment time against
   peak latch load and choose a design point.

## Outputs

- Deployment angle, angular velocity and acceleration against time
- Hinge reaction forces and moments, peak latch impact load
- Deployment time against spring stiffness, for each Mach number
- Rigid against flexible comparison of peak loads
- Video of the deployment sequence

## Checks

- Energy balance: spring energy released equals kinetic energy plus damping losses
  before the stop.
- Hand calculation of deployment time with no aerodynamic load and no damping.
- Symmetry: all four fins deploy identically in the no-crossflow case.
