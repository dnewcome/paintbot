# Fine-Z Voice Coil Actuator — Spec

Custom voice coil actuator (VCA) for the brush stroke + pressure axis. Built
in-house: materials ~$30–80 + encoder ~$20–40 vs. ~$300–700 off-the-shelf
(Moticont/H2W). Electromagnetics are easy here; the engineering is mechanical
(guide, encoder, force linearity, thermal).

## Role in the system
- **Fine-Z only.** Contact dynamics: pressure modulation + quick in-stroke lifts.
- Gross lift / canvas standoff / relief depth = **coarse-Z** (separate belt stage).
- Axis is **horizontal** → no gravity load along the stroke. Continuous force is
  just brush-contact pressure (small). Side load (gravity on the mover) is taken
  by the guide, NOT the coil bearings.
- Current control → force → **brush line weight**, into the software pressure channel.

## Requirements

| Spec                  | Target            | Notes                                          |
|-----------------------|-------------------|------------------------------------------------|
| Stroke                | ~20 mm (Path A) / ~8–10 mm (Path B) | See guide fork below          |
| Continuous force      | ~3–5 N            | Brush pressure only (no gravity to fight)      |
| Peak force            | ~20 N             | Snappy dabs/stipple + headroom                 |
| Small-signal BW       | 30–100 Hz         | Pressure response, brush detail                |
| Mover mass            | <60 g             | Coil + bobbin + brush holder + brush           |
| Position feedback     | linear encoder    | e.g. AS5311 + magnetic strip                   |
| Force feedback        | current (v1); load cell (optional v2) | Current = open-loop force      |

## Electromagnetic design point (moving coil, cylindrical)

Loudspeaker-style motor: center NdFeB magnet + steel return cup; coil rides the
annular gap. `F = B·L·I = k_f·I`.

| Parameter        | Value        |
|------------------|--------------|
| Gap flux B       | ~0.5 T (N52 + steel return) |
| Coil mean dia    | 20 mm        |
| Turns N          | ~160 (AWG26) |
| Force constant   | k_f ≈ 5 N/A  |
| Coil resistance  | R ≈ 1.3 Ω    |
| Copper mass      | ~12 g        |
| 20 N peak        | 4 A → ~21 W burst (fine) |
| 5 N continuous   | 1 A → ~1.3 W (trivial)   |
| Mover ~60 g      | peak accel ≈ 330 m/s² (~34 g) |

**Conclusion: force/pressure-limited, NOT acceleration-limited.** Huge accel
headroom → optimize the design for pressure fidelity, not power.

## Topology choice: moving-coil vs moving-magnet
- **Moving-coil (chosen v1):** lightest mover, simplest magnetics (one magnet
  stack + steel cup + wound bobbin), best bandwidth. Cost: flexing lead wires
  (manageable over ~20 mm with strain relief / short drag loop).
- **Moving-magnet:** coil + wires stationary (no flex, more rugged) but heavier
  mover. Revisit if lead-wire fatigue becomes a problem.

## Guide: Path B — flexure, ~8–10 mm (CHOSEN)
Parallel leaf-spring (double-parallelogram) flexure: zero friction / stiction /
backlash → best brush pressure / line-weight fidelity, which is the expressive
core. Coarse-Z handles ALL gross lifts (so coarse-Z must be reasonably quick for
between-stroke lifts and stipple > ~10 mm). The flexure adds a known linear
spring rate that gets calibrated out of the force model (F = k_f·I − k_flex·x).

Design notes for the flexure:
- Double-parallelogram (compound) flexure keeps motion straight (no arc/parasitic
  tip) over ~10 mm — important so the brush tracks a true line into the canvas.
- Pick blade material/thickness so spring rate is small vs. the ~3–5 N working
  force (e.g. spring-steel or BeCu blades), and so blade stress stays well under
  fatigue limit at full 10 mm deflection (infinite-life design).
- Flexure also provides the side-load stiffness, so the coil only pushes axially —
  no separate linear rail needed. This is the elegance of Path B.

(Rejected Path A: ~20 mm linear rail — faster big in-stroke lifts, but rail
friction corrupts open-loop force fidelity.)

## Driver (single-phase — moteus CANNOT drive this)
- H-bridge current-mode loop, NOT a 3-phase FOC controller.
- DIY path: STM32/Teensy + DRV8874-class H-bridge + inline current sense
  (INA240), current PI loop @ 10–20 kHz; AS5311 linear encoder for position;
  outer position/force loop on the host or MCU. Host-synced over the same
  real-time fabric as the CAN-FD axes.
- Buy path: Maxon ESCON / AMC analog servo drive in current/torque mode (~$150+).

## Build risks to watch
- Force linearity over stroke (coil overhang vs magnet underhang geometry).
- Guide friction corrupting force control (→ Path B flexure removes this).
- Lead-wire fatigue (moving-coil) — strain relief / consider moving-magnet.
- Coil thermal at sustained high force (low for our few-N continuous need).

## Open
- [ ] Guide fork: Path A (rail, 20 mm) vs Path B (flexure, ~10 mm).
- [ ] Brush holder / quick-change interface + brush mass measurement.
- [ ] Encoder choice + mounting datum.
