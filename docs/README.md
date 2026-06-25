# Paintbot — Hardware Design Docs

Physical machine that mirrors the operator's painting movements in real time
(live digital twin) and replays recorded `TwinPerformance` op streams. A raked
vertical CoreXY easel carrying a multi-stage brush head.

## Documents
- **[hardware-architecture.md](hardware-architecture.md)** — top-level concept,
  governing design drivers, work envelope, axis map & drives, subsystems.
- **[motion-sizing.md](motion-sizing.md)** — CoreXY + coarse-Z sizing: torque
  budget, stepper (open-loop, 56 V, 30T pulley) vs FOC, counterbalance.
- **[belt-resonance.md](belt-resonance.md)** — the bandwidth cap at 3×4 ft:
  belt stiffness, tension nuance, frame modes, open-loop input shaping, measuring f_n.
- **[voice-coil-actuator.md](voice-coil-actuator.md)** — custom fine-Z brush
  stroke/pressure actuator: requirements, EM design point, Path B flexure, driver.
- **[voice-coil-head.md](voice-coil-head.md)** — brush tool head built/tested on
  the existing ShopBot first: mechanical stack-up, magnetic circuit, CAD parts.
- **[voice-coil-driver.md](voice-coil-driver.md)** — single-phase current-mode
  (=force-mode) driver + nested control loop + calibration; the bench-test path.
- **[extrusion-head.md](extrusion-head.md)** — second tool head: motor-driven
  syringe pump for thick gel medium (dip-and-load, single-bore reverse-fill, fat bead).
- **[planar-corexy.md](planar-corexy.md)** — construction variant: laser/waterjet
  plates locate the motion geometry, hybridized with the 8020 frame (after corexy.com R1).
- **[coarse-z.md](coarse-z.md)** — coarse-Z stage (full machine): belt-driven MGN12
  carriage presenting a 65 mm clamp; Z is horizontal in the easel (no self-lock).
- **[bom.md](bom.md)** — consolidated bill of materials: brush head, driver, planar frame.

## Decisions locked so far
- Raked vertical CoreXY easel, **3×4 ft** work area (which dim is vertical: TBD).
- Drives: **open-loop steppers** for XY initially (56 V, high-torque NEMA23
  ≥2.5–3 N·m, low-inductance, dual-shaft, 30T 2GT pulley); upgrade path to
  closed-loop. Reserve current/force control for the voice coil.
- **Two-stage Z:** coarse belt carriage (all gross lifts) + custom voice-coil
  fine-Z (Path B flexure, ~10 mm, current = force = brush line weight).
- **Interchangeable tool heads** sharing one ShopBot/Z-plate mount: (1) voice-coil
  brush (force-controlled, live feel); (2) gel extruder (volume-metered syringe
  pump, dip-and-load, single-bore reverse-fill, ~3 mm fat-bead nozzle).
- **Y counterbalanced with constant-force / gas spring, never a counterweight.**
- Bandwidth ceiling is **belt resonance**, not motor torque → 15 mm steel-core
  belt + ≥20 mm idlers + MGN12 rails + ~50–80 N tension + input shaping.

## Top open decisions
- [ ] Bed dimension assignment: which of 3 ft / 4 ft is vertical (Y)?
- [ ] Wrist single-DOF axis: lean vs. azimuth/roll.
- [ ] Voice coil detailed design (magnetic circuit + flexure) → build123d parts.
