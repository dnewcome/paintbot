# Coarse-Z Stage (full machine)

The slow Z axis that sets canvas standoff + relief depth and does gross between-stroke
lifts. The fine voice-coil flexure only does ±5 mm, so coarse-Z covers everything
larger. **Only needed on the final machine** — on the prototype the Shapeoko/HDZ is
the coarse-Z. It rides the CoreXY X-carriage, so its motor mass is a moving-mass tax.

## Orientation insight (drives the whole design)
In the vertical easel, **Z (canvas normal) is HORIZONTAL**. Consequences:
- **Gravity is perpendicular to travel** → the motor never lifts the head against
  gravity → low holding torque, a **belt drive is fine** (no self-locking screw
  needed), and it can be back-drivable.
- The head weight becomes a **cantilever moment** on the Z rail (reacted by block
  spacing), not an axial load.

## Requirements
| Quantity | Value | Notes |
|---|---|---|
| Travel | ~100 mm | standoff (~20–50) + relief (~10) + gross lifts (~20–50) |
| Load | tool head ~0.5–0.8 kg, cantilevered ~100 mm | brush or extruder head |
| Cantilever moment | ~0.8 kg·9.81·0.1 ≈ 0.78 N·m | 2× MGN12 blocks handle easily |
| Speed | moderate (between-stroke lifts) | not on the fast/fidelity path |
| Motor mass | minimize (rides the gantry) | recurring constraint |

## Mechanism
- **Rail:** 1× **MGN12** along Z, **2 blocks spaced ~50 mm** to react the cantilever
  pitch moment (MGN12 block moment rating ≫ 0.78 N·m, so 2 blocks are ample).
- **Drive:** **2GT belt** loop along Z — light **NEMA17 pancake** (or NEMA14) at the
  gantry end, idler at the canvas end, carriage clamps the belt. Belt (not lead
  screw) per the project preference; gravity isn't along Z so no self-lock needed.
- **Tool interface:** the carriage presents a **65 mm clamp** (bore axis along Z) →
  the head's `body_collar` mounts the SAME way as on the Shapeoko HDZ. Use a **bought
  65 mm router/spindle clamp** (e.g. Carbide HD 65 mm mount or a generic OpenBuilds
  one) bolted to the carriage plate — no need to machine a clamp.
- **Fixed structure:** the Z rail mounts on a bracket that bolts to the CoreXY
  **X-carriage plate** and cantilevers toward the canvas; it also carries the motor
  (gantry end) and idler (canvas end).

## Parts
| Part | Fab | Status |
|---|---|---|
| `z_carriage.py` | laser plate: 2× MGN12 blocks + 65 mm-clamp mount + belt clamp | ✅ DXF |
| 65 mm router clamp | **bought** (Carbide HD / generic) | — |
| Z rail bracket (fixed) | laser/8020: rail mount + X-carriage join | ⏳ |
| Motor mount + idler | laser/printed | ⏳ |
| MGN12 rail + 2 blocks | bought | — |
| NEMA17 pancake + 2GT belt/pulley/idler | bought | — |

## Open
- Z rail bracket + X-carriage join (perpendicular plate join — tab/slot + angle).
- Motor/idler mounts + belt path.
- Confirm the bought 65 mm clamp's bolt pattern → set `ZC_CLAMP_*` in params_frame.
- Travel could grow if deep relief is wanted (rail length + belt scale linearly).
