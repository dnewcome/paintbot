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

## Belt routing (single-plane, motors at bottom corners)
Standard single-plane CoreXY: 2 drive pulleys (bottom corners) + corner idlers
(top corners) + 2 idlers per moving gantry end + carriage belt anchors (~8 idlers).
**Exact idler offsets/strand routing will be PORTED from a verified reference
(corexy.com R1 routing), not reinvented** — idler hole positions on the plates are
parameters, finalized once the routing is pinned against the reference.

## Open forks (need decisions before CAD)
- [ ] **Rails:** MGN12 linear (recommended — stiffness at 1.2 m) vs. R1-style
      shaft+bushing (cheaper/simpler plates, but compliant at this span).
- [ ] **Plate fab/material:** waterjet/laser **aluminum ¼–3/8″** (stiff, R1-like)
      vs. laser steel vs. acrylic/ply for a cheap first proto.
- [ ] **Routing:** single-plane (8 idlers, clean) vs. stacked-belt (fewer idlers,
      small cocking moment) — single-plane recommended to match the plate plane.
- [ ] Which of 3 ft / 4 ft is the vertical (Y) span (still open from architecture).
