# Planar-Plate CoreXY (hybrid with 8020)

A construction variant where **laser/waterjet planar plates locate the precise
motion geometry** and **8020 extrusion provides the large structural frame**.
Inspired by the [corexy.com Waterjet Aluminum R1](https://www.corexy.com/corexyr1/index.html).

## What the R1 teaches (borrow the philosophy, not the scale)
The R1 cuts a single 3/16″ aluminum sheet so that ONE plate locates both NEMA17s,
all 8 idlers, the drive pulleys, and the rail datums to waterjet tolerance — CoreXY
precision with no machined frame. Notable features:
- **Single-plane belt routing**, 8 idlers + 2 drive pulleys, all axes ⟂ to the
  plate, both belts coplanar (no stacked-belt cocking moment).
- Rails = 3/8″ precision shaft in epoxied bronze bushings.
- Tension by sliding the steppers in slots. Secondary parts laser-cut acrylic.

It is a **~12×14″ desktop** machine, though. The philosophy scales; the specifics
don't.

## What survives the jump to 3×4 ft vertical, and what doesn't
| R1 spec | Keep? | Paintbot choice (per earlier sizing) |
|---|---|---|
| Plate-locates-geometry | ✅ keep | the core idea — cut plates as precision jigs |
| Single-plane routing (8 idlers) | ✅ keep | pairs naturally with one plate plane |
| Motor-slot belt tensioning | ✅ keep | simple, effective |
| MXL 1/4″ belt | ❌ | **15 mm steel-core GT2/GT3** (forces + resonance) |
| 18T idlers | ❌ | **≥20 mm idlers** (steel-cord bend radius) |
| 3/8″ shaft + bronze bushing rails | ❌ | **MGN12 linear rails** (3/8″ shaft sags/whips at ~1.2 m) |
| 3/16″ single plate as whole frame | ❌ | **plates bolt to an 8020 perimeter**; thicker (¼–3/8″ Al) |

## Hybrid architecture
- **8020 perimeter frame** (raked vertical easel) = cheap, rigid bulk structure.
- **Planar plates bolt to the 8020**, carrying the *precise* motion geometry:
  - **2 top corner / motor plates** — NEMA mount + tension slots + corner idlers.
  - **2 bottom corner plates** — corner idlers + Y-rail lower ends.
  - **2 gantry-end plates (MOVING)** — MGN12 Y-carriage blocks + the gantry idlers
    + the X-rail mounts; these are the ends of the moving cross-beam.
  - **1 X-carriage plate** — MGN12 X-block + belt clamps + the shared tool-head /
    Z-plate interface (same mount the voice-coil + extruder heads bolt to).
- **Rails:** 2× MGN12 vertical (Y) on the uprights; 1× MGN12 horizontal (X) on the
  gantry beam. Plates carry the blocks / locate the rails.
- **Belt:** single-plane CoreXY, 15 mm steel-core, ≥20 mm idlers, motor-slot tension.

## Why this fits the paintbot
- Cheap precision for the fiddly belt/idler/rail geometry without machining.
- Plates are fast/cheap to iterate (re-cut a corner plate vs. re-machining).
- Marries to the big 8020 easel and keeps every stiffness decision already sized
  (steel-core belt, MGN12, counterbalance, input shaping).

## Plate ↔ 8020 marriage (to detail)
- Plates bolt to extrusion faces via T-nuts; locate against the extrusion edge or a
  pin for repeatability.
- Tool-head interface plate stays common across heads (voice-coil brush, extruder).

## Orientation: LANDSCAPE (4 ft wide × 3 ft tall)
| Axis | Span | Rail | Notes |
|---|---|---|---|
| X (horizontal, along gantry) | 4 ft / 1219 mm work | **MGN12 ~1370 mm on the moving gantry beam** | the long axis; carriage rides it |
| Y (vertical, gantry up/down) | 3 ft / 914 mm work | **2× MGN12 ~1120 mm on the uprights** | counterbalanced |
- **Motors: both at the BOTTOM corners** (weight low, wiring at the base).
- **Counterbalance:** constant-force springs pull the gantry up from the top beam.
- **Resonance note:** landscape makes the horizontal belt spans the longest
  (~1.4 m top/bottom) and the moving gantry beam the long member → keep the gantry
  beam stiff (boxed/carbon) and the belt 15 mm steel-core; this is the worst axis.

## Belt routing (single-plane, motors at bottom corners) — laid out
Reconstructed in `cad/routing.py` (emits `build/routing.svg`). Topology:
- **Belt A** (left motor): M_A → bottom edge → BR → up right upright → GR_a →
  along gantry → carriage → GL_a → down left upright → M_A.
- **Belt B** (right motor): M_B → bottom edge → BL → up left upright → GL_b →
  along gantry → carriage → GR_b → down right upright → M_B.
- The two bottom strands cross near center-bottom → **2 crossover idlers** stagger
  them (single-plane). **Top edge carries NO belt** → free for the counterbalance.
- **8 idlers:** BL, BR (bottom corners) + GL_a/GL_b/GR_a/GR_b (gantry ends) + 2
  crossover. Kinematics X=(a+b)/2, Y=(a−b)/2.
- Idler coordinates are first-pass — verify strand clearances against a reference build.

## Plate set status (laser DXF + STL fit-check)
| Plate | Carries | Status |
|---|---|---|
| `plate_xcarriage.py` | MGN12 X-block, belt clamps, tool interface | ✅ DXF |
| `plate_gantry_end.py` ×2 | MGN12 Y-block, gantry beam, 2 gantry idlers | ✅ DXF |
| `plate_motor_corner.py` ×2 | NEMA17 tension slots, bottom-corner idler, 8020 mount | ✅ DXF |
| `plate_crossover.py` | CX1/CX2 idlers (mid bottom), 8020 mount | ✅ DXF |
| (no top-corner plates) | top edge is belt-free | — |

Full-machine 3D view: `cad/assembly_corexy.py` → `build/assembly_corexy.png` — the
real flat plates at their routing positions + the **real brush head** on the carriage
reaching the canvas, with MGN12 rails / 8020 frame / NEMA23 motors as stand-ins, the
canvas slab, and the whole easel raked back. (Folds in the retired `machine.py` massing.)

## Open forks (need decisions before CAD)
- [ ] **Rails:** MGN12 linear (recommended — stiffness at 1.2 m) vs. R1-style
      shaft+bushing (cheaper/simpler plates, but compliant at this span).
- [ ] **Plate fab/material:** waterjet/laser **aluminum ¼–3/8″** (stiff, R1-like)
      vs. laser steel vs. acrylic/ply for a cheap first proto.
- [ ] **Routing:** single-plane (8 idlers, clean) vs. stacked-belt (fewer idlers,
      small cocking moment) — single-plane recommended to match the plate plane.
- [ ] Which of 3 ft / 4 ft is the vertical (Y) span (still open from architecture).
