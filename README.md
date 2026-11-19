# Multibody Dynamics Portfolio

Two multibody dynamics (MBD) simulation projects built on the 3DEXPERIENCE platform
(CATIA for geometry, SIMPACK-based multibody simulation, Abaqus for flexible bodies),
published as a public portfolio link on the resume of Mittapalyam Ashok Karthik for
MultiBody Dynamics Engineer roles (first target: Dassault Systèmes, IPS team).

## Main objectives

1. Show end-to-end MBD skills on aerospace and UAV mechanisms: kinematics, joints,
   nonlinear force elements, contact, flexible bodies, parameter studies and result
   validation.
2. Connect each project to earlier work, so it tells a single story in interviews:
   - Grid fin deployment builds on the M.Tech grid fin CFD thesis (Best Paper, ICSAST-2025).
   - Quadcopter payload deployment builds on the B.E. rescue drone project.
3. Publish a short video, plots and a 4 to 6 page report for each project at a public link.

## Projects

| Folder | Project | Brief |
|---|---|---|
| `grid-fin-deployment/` | Piston-driven pitch actuation of a full-scale hexagonal grid fin (slider-crank, one station) | [Project page and results](grid-fin-deployment/README.md) |
| `quadcopter-payload-deployment/` | Servo-actuated payload release and landing gear dynamics of a rescue quadcopter | [Design brief](quadcopter-payload-deployment/DESIGN_BRIEF.md) |

Each project folder follows the same layout as work progresses:

- `cad/` - geometry exports and drawings (only self-made or public geometry)
- `model/` - multibody model notes, parameter tables, Abaqus modal reduction inputs
- `results/` - exported time histories (CSV) and plots
- `scripts/` - Python post-processing
- `report/` - report source and final PDF

## Milestones

| # | Milestone | Grid fin | Quadcopter |
|---|---|---|---|
| 1 | Design brief and parameter table frozen | | |
| 2 | CAD geometry and mass properties | Done | |
| 3 | Rigid-body kinematic model running | Done | |
| 4 | Force elements and contact added | | |
| 5 | Flexible body from Abaqus integrated | | |
| 6 | Parameter study complete | | |
| 7 | Video, plots and report published | | |

## Ground rules

- Use only geometry created for this project or taken from public sources. No customer or
  internal Dassault Systèmes models or data.
- Confirm with the manager that publishing results produced with the company 3DEXPERIENCE
  licence is allowed before anything goes public.
- Every number on the resume must come from these results.
