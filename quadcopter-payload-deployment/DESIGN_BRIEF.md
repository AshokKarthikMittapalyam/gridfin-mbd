# Design Brief: Quadcopter Payload Deployment Gear

## Objective

Simulate a rescue quadcopter that releases a payload (for example a first-aid kit) through a
servo-actuated release mechanism while hovering, and then lands on its landing gear. Size the
release mechanism and landing gear, and quantify how the release disturbs the drone.

## Questions the study answers

1. What servo torque does the release mechanism need, and how fast does it open?
2. Does the payload separate cleanly, without touching the landing gear or frame?
3. How much does the drone pitch, roll and climb when the payload mass suddenly leaves?
4. What loads reach the landing gear and frame during a hard landing?

## System description

| Item | Description | Initial value (to refine) |
|---|---|---|
| Frame | Rigid X-frame quadcopter | 450 mm motor-to-motor |
| Drone mass | Frame, motors, battery, electronics | 1.5 kg |
| Rotor thrust | Four thrust force elements, speed-controlled | Hover thrust = weight |
| Payload | Box hung below the frame | 0.3 to 1.0 kg |
| Release mechanism | Servo-driven hook or four-bar latch | Servo torque limit from datasheet |
| Landing gear | Two skids or four legs with spring and damper | k and c to size |
| Ground | Contact with friction, flat and tilted cases | 0 and 10 degree slope |

## Model build steps

1. **CAD (CATIA):** frame, arms, landing gear, release mechanism and payload box.
   Export mass properties.
2. **Release mechanism kinematics:** model the servo arm, links and hook. Check the
   opening angle, clearance and mechanical advantage over the full stroke.
3. **Hover and release:** add the rotor thrust elements with a simple attitude and
   altitude controller, hover, open the latch at t = 1 s, and track payload separation.
4. **Landing:** drop from 0.5 m at a set descent rate onto flat and tilted ground with
   leg contact. Record leg forces, frame accelerations and rebound.
5. **Flexible landing gear:** Abaqus model of one leg, modal reduction, import as a
   flexible body, and compare peak loads with the rigid leg.
6. **Parameter study:** sweep payload mass and leg stiffness. Plot the attitude
   disturbance at release and the peak landing load.

## Outputs

- Servo torque and latch opening angle against time
- Payload separation distance and clearance to the gear
- Drone attitude and altitude response after release
- Leg forces and frame acceleration during landing, rigid against flexible
- Video of release and landing

## Checks

- Static hover: total thrust equals total weight before release.
- After release, the initial upward acceleration matches the thrust surplus divided by
  the new drone mass.
- Landing: peak leg force against a hand calculation with a single spring-mass model.
