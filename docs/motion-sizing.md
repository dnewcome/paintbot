# Motion Sizing — CoreXY + Coarse-Z (3×4 ft vertical easel)

First-pass sizing. Masses are estimates to refine once parts are real. Frame size
is 3×4 ft (~914×1219 mm work area); which dim is vertical (Y) is still open but
doesn't change motor torque (only belt length / resonance).

## Moving-mass budget (estimate)
| Item | Mass |
|---|---|
| X-carriage (coarse-Z + voice coil + wrist + brush + plate) | ~1.5 kg |
| Cross-beam (X span, stiff but light extrusion or carbon tube) | ~1.0–2.0 kg |
| **Y moving mass** (beam + carriage) | **~2.5–3.5 kg** |
Note: the coarse-Z **motor rides the X-carriage**, so its mass is in BOTH the X and
Y moving totals → keep the Z motor light (it's a real accel tax, unlike the
frame-mounted XY motors).

## Acceleration target
- Mimic **arm gestures**: ~2 m/s peak, **~1 g sustained (10 m/s²), ~2 g peak (20 m/s²)**.

## CoreXY torque budget
Pulley: 20T 2GT, pitch dia 12.73 mm → r = 6.37 mm. Travel = 40 mm/rev.
CoreXY force→torque mapping (per motor): pure-axis move τ = F·r/2; worst-case
diagonal τ = (|Fx|+|Fy|)·r/2.

| Move | Head force (gravity counterbalanced) | Per-motor torque |
|---|---|---|
| Pure X, 2 g (1.5 kg) | 30 N | 0.10 N·m |
| Pure Y, 2 g (3.5 kg) | 70 N | 0.22 N·m |
| Worst diagonal, 2 g | Fx 30 + Fy 70 | **0.32 N·m** |
| + friction/preload + 1.5× margin | | **~0.5 N·m peak / motor** |

**Continuous** torque is far lower (accel is transient; cruise = just friction).
Speed: 2 m/s with 40 mm/rev = 50 rev/s = **3000 rpm** (10 kHz full-step rate).

### These motors are FRAME-MOUNTED → mass doesn't matter
Unlike the head, XY motor mass is free (no accel penalty). So we can use a beefy
motor purely for torque/stiffness.

## Motor options for XY

### Option 1 — moteus/ODrive BLDC (FOC), per original plan
- mj5208-class: ~0.3 N·m continuous, ~1.7 N·m peak → covers 0.5 N·m peak easily.
- Gains: closed-loop (never loses position under aggressive mirroring), torque/
  impedance control, deterministic CAN-FD, clean low-latency setpoint streaming.

### Option 2 — STEPPERS on existing 4.5 A drivers  ← user has these
- 0.5 N·m peak @ 3000 rpm is reachable with a **high-torque NEMA23** (≥1.9 N·m
  holding) **on a high-voltage bus (48–60 V)**. Voltage is the lever for stepper
  speed: torque falls with rpm (back-EMF + winding inductance); a high bus
  voltage + low-inductance ("high-speed" wound) motor keeps torque up at 3000 rpm.
- 4.5 A drivers are plenty of current; make sure they're rated for / fed a high
  voltage. A 3 N·m holding NEMA23 at 48 V should still deliver ≥0.5 N·m near
  3000 rpm — adequate, but verify against the motor's torque-speed curve.
- **What steppers give up vs FOC:**
  1. *Open-loop* steppers can **lose steps** on the unpredictable hard reversals
     of live human mirroring → twin drifts. Fix: **closed-loop steppers**
     (stepper + encoder, e.g. integrated "iHSS"/CL drivers) — recovers position
     robustness. Strongly recommended if going stepper.
  2. **No torque/force control** — can't "feel" the canvas or be back-driven.
     BUT: the *feel* requirement lives at the **brush contact = voice coil**, not
     at XY. XY only needs to track position fast. So steppers for XY is well
     justified; keep current/force control only where it matters (voice coil,
     maybe wrist).
  3. Mid-band resonance — handled with microstepping + input shaping.

### Decision: OPEN-LOOP steppers initially (upgrade path to closed-loop)
Open-loop costs nothing on latency (step/dir is low-latency) — it only risks
**position integrity**, not responsiveness. Viable here because:
- ~4× torque margin (3 N·m motor vs ~0.72 N·m demand) IS the "poor man's closed
  loop" — keeps steps from being lost. So do NOT tune accel to the edge; keep
  commanded accel well under available torque at speed (open-loop can't recover).
- Paint is forgiving: sub-mm XY drift is visually invisible on a painting (unlike
  a 3D print) → lost steps are a soft failure.

Open-loop guardrails:
- **Home between strokes/sessions** (limit switches) to re-register against silent
  drift.
- **Mid-band resonance** (~5–15 rev/s) is stall-prone → microstep 16+, use 56 V to
  pass through quickly, don't dwell cruise speeds there.
- **Step-rate ceiling:** 30T @ 2000 rpm × 16 µstep ≈ **107 kHz/axis** — confirm the
  pulse generator (Teensy/STM32 OK) handles it while streaming live setpoints.
- **Buy dual-shaft (rear-shaft) NEMA23 now** → adding an encoder for closed-loop
  later is a bolt-on, no motor swap.

### Sizing recommendation
Run XY on the 4.5 A drivers at the full **56 V** + high-torque **NEMA23
(≥2.5–3 N·m, low-inductance, dual-shaft) + 30T 2GT pulley** (~2000 rpm @ 2 m/s,
comfortable torque margin). Reserve FOC current-control for the voice coil (and
optionally wrist).
Caveat on control firmware: live teleoperation needs **streamed setpoints at low
latency**, not a G-code look-ahead planner — Klipper is great for steppers but is
built around G-code planning; for live mirroring use a streaming-capable real-time
step generator (Teensy/STM32 from host setpoints) or closed-loop drivers fed by it.

## Coarse-Z sizing
- Horizontal travel ~150–250 mm; carries fine head ~0.5–0.8 kg; belt-driven (not
  screw, per preference). No gravity along travel; head cantilevers → side load on
  a MGN9/12 rail.
- Needs moderate speed (it now does ALL gross lifts since the flexure voice coil
  is only ~10 mm). 1 g on 0.8 kg = 8 N → trivial torque. **Use a LIGHT motor**
  (small NEMA17 closed-loop or compact BLDC) because it rides the gantry.

## Y counterbalance
- Gravity load = Y mass × g ≈ 3.5 × 9.81 ≈ **34 N**.
- Use **constant-force spring(s)** (~34 N total, ideally a pair for symmetry) or a
  ~30–40 N gas spring. NEVER a counterweight (adds inertia, kills accel).

## ⚠ Top risk at this scale: belt resonance, not motor torque
CoreXY's long diagonal belt routing makes belt stretch the dominant compliance at
~1.2 m spans. Rough first-mode estimate:
- Steel-core 9–15 mm belt, span ~1.2 m → effective k ~ 30–60 N/mm.
- f_n = (1/2π)·√(k/m), m ≈ 1.5 kg → **~20–30 Hz first resonance.**
- That caps usable servo bandwidth to ~1/3 of f_n ≈ **7–10 Hz** (with a notch).
- Arm-gesture content is mostly < 5 Hz → workable, but it's THE binding constraint.

Mitigations (do all): **15 mm steel-core GT3 belt** (not optional at this size),
high tension, minimize moving mass (f_n ∝ 1/√m), short free spans via idler
layout. Fallback if CoreXY proves too compliant: **dual-drive gantry** (independent
motor per side on the long axis) keeps belts short/stiff at the cost of one motor
riding the gantry.

## Recommended starting parts
- Belt: Gates 2GT/3GT, **15 mm, steel-core**; 20T pulleys; ≥16 mm toothed idlers.
- XY motors: high-torque NEMA23 (≥1.9 N·m) on 48–60 V + the 4.5 A drivers
  (closed-loop preferred) — OR moteus mj5208 ×2 if going FOC.
- Guides: MGN12 (Y verticals + X beam) for stiffness at this size.
- Coarse-Z: light NEMA17 closed-loop / small BLDC + 2GT belt + MGN9/12, ~200 mm.
- Counterbalance: constant-force spring pair (~34 N) or 30–40 N gas spring.
