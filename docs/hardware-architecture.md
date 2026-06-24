# Paintbot — Hardware Architecture

Physical realization of the paintbot software twin: a robot that mirrors the
operator's painting movements in real time (live digital twin) and can replay
recorded `TwinPerformance` op streams.

## Top-level concept

A **raked vertical CoreXY easel** carrying a multi-stage brush head. The operator
moves; the machine follows with minimal perceived lag, holding (for now) a paint
brush. Drives are robotics-grade BLDC servos under field-oriented control so the
head can be torque/impedance-controlled, not just position-commanded.

## Governing design drivers

1. **Latency is dominated by sensing/compute, not mechanics.** A well-tuned
   CoreXY tracks commands within single-digit ms. The mechanical goal is "don't
   be the bottleneck"; responsiveness is won with a predictive filter that
   extrapolates operator motion to mask camera latency.
   - Budget: **<50 ms end-to-end feels responsive, <20 ms feels truly live.**
2. **Moving mass vs. acceleration is the master tradeoff.** `a = F/m`. Every
   gram on the gantry (coarse Z, voice coil, wrist, brush) costs acceleration,
   and acceleration — not top speed — is what makes mirroring feel tight.
3. **Belt + frame stiffness set the control bandwidth.** The lowest mechanical
   resonance caps how aggressively the servo loop can be tuned. At ~1.2 m belt
   spans this is a real limit; favor wide steel-core belt, high tension, short
   free spans.

## Work envelope & orientation

| Parameter            | Value                                             |
|----------------------|---------------------------------------------------|
| Canvas / bed         | **3 × 4 ft** (~914 × 1219 mm) work area           |
| Orientation          | Vertical easel, **raked back ~10–20°** from plumb |
| X axis               | Horizontal across canvas                          |
| Y axis               | Vertical (gravity axis — counterbalanced)         |
| Z coarse             | Horizontal, brush standoff / relief depth         |
| Z fine (voice coil)  | Horizontal, brush stroke + pressure               |
| Wrist                | 1 DOF (axis TBD — lean vs. azimuth/roll)          |

### Why the rake
- Slight gravity bias holds brush toward canvas.
- Paint runs *down* the canvas, not *off* it.
- More stable base against the gantry's tipping moment.

## Axis map & drives

Platform: **moteus / ODrive-class BLDC under FOC**, daisy-chained on **CAN-FD**,
single real-time host (**Raspberry Pi + mjbots pi3hat** — real-time CAN-FD + IMU).

| Axis        | Type              | Driver                         | Notes                                              |
|-------------|-------------------|--------------------------------|----------------------------------------------------|
| X           | 3-phase BLDC      | moteus (CAN-FD)                | CoreXY motor A, frame-mounted                       |
| Y           | 3-phase BLDC      | moteus (CAN-FD)                | CoreXY motor B, frame-mounted                       |
| Z coarse    | 3-phase BLDC      | moteus (CAN-FD)                | Belt-driven carriage, NOT lead screw                |
| Wrist tilt  | 3-phase gimbal    | moteus / small FOC (CAN-FD)    | Direct-drive, backlash-free, lightweight            |
| **Z fine**  | **voice coil (1-phase)** | **dedicated current-mode H-bridge + encoder** | moteus CANNOT drive this — needs its own driver, host-synced |

**Key gotcha:** moteus/ODrive do FOC on *3-phase* motors. The voice coil is a
*single-phase* actuator, so it gets its own current-controlled driver. Payoff:
current control = force control = **brush pressure**, feeding straight into the
software's existing pressure channel.

## Motion subsystems

### XY — CoreXY
- Motors frame-mounted (only gantry + belts move).
- **Wide steel-core GT2/GT3 belt (9–15 mm).** Belt stiffness sets resonance.
- Direct-drive preferred to protect bandwidth; add small reduction only if
  torque comes up short (reduction adds reflected inertia, costs bandwidth).

### Y counterbalance — critical for a vertical machine
- Cancel the gantry's gravity load so Y motors don't burn continuous holding
  current (heat + stolen torque headroom).
- **Use a constant-force spring or gas spring — NEVER a counterweight.** A
  counterweight adds its mass to the inertia you must accelerate, roughly
  doubling effective Y moving mass and destroying acceleration.

### Z — two stages
- **Coarse:** lightweight belt-driven carriage (~100–300 mm), canvas standoff +
  relief depth. Slow path.
- **Fine:** custom voice coil (~10–30 mm stroke), brush stroke dynamics +
  pressure. High bandwidth, zero backlash, direct-drive.
  - Run in **current control → force → line weight.**
  - Mover hangs horizontally → side load. A dedicated linear guide carries the
    cantilever moment so the coil only pushes axially (coils dislike side loads
    on their own bearings). Keep brush + wrist short-coupled to carriage.

### Wrist — 1 DOF
- Lightweight gimbal-style BLDC, direct-drive, FOC.
- **Open sub-decision — which single axis:**
  - *Lean* (brush tips toward/away from canvas): brush loading/unloading; lean
    confined to one plane unless XY assists.
  - *Azimuth/roll* (spin brush about standoff axis): aligns a flat/chisel brush
    to stroke direction — better for calligraphic line-weight modulation, pairs
    well with pressure-controlled voice coil. **Current lean: azimuth/roll.**
- Consider remote-driving the wrist (belt/cable from gantry-mounted motor) to
  keep tip mass low — deferred.

## Performance targets (first pass)

| Quantity                 | Target                                  |
|--------------------------|-----------------------------------------|
| Motion to mimic          | **Arm movements** (gross gesture)       |
| Peak head velocity       | ~2 m/s                                  |
| Sustained acceleration   | ~1 g (10 m/s²)                          |
| Peak acceleration        | ~2 g (20 m/s²)                          |
| End-to-end latency       | <50 ms (target <20 ms)                  |

### Rough moving-mass budget (to refine)
- X-carriage ≈ 1.5 kg (coarse-Z + VCA + wrist + brush + plate)
- Y (beam + carriage) ≈ 2.5–3 kg
- At 2 g peak + gravity counterbalanced → ~30–60 N at the belt →
  ~0.4–0.6 N·m at a 20T GT2 pulley. Upper edge of a single mj5208-class motor
  direct-drive → choose beefier BLDC or accept a small reduction.

## Deferred / later
- Physical paint reload: dip well + dip motion (software already models reload
  events). On a vertical canvas, well sits low/side.
- Motion scaling (1:1 vs. operator-small / canvas-large) — changes accel budget.
- Frame: stiff rectangular weldment/extrusion, raked, resisting tipping moment.

## Open decisions
- [ ] Bed dimension assignment: which of 3 ft / 4 ft is vertical (Y)?
- [ ] Wrist single-DOF axis: lean vs. azimuth/roll.
- [ ] Voice coil: off-the-shelf (Moticont/H2W/Akribis) vs. custom moving-magnet.
- [ ] XY motor exact part + direct-drive vs. reduction.
