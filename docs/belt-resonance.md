# Belt Resonance — the bandwidth cap at 3×4 ft

At this scale the binding constraint on responsiveness is **not motor torque** — it's
the first mechanical resonance of the long CoreXY belt loops. The belt is a spring;
the carriage mass on that spring resonates at
`f_n = (1/2π)·√(k_eff/m)`, and you can only push the motion bandwidth to roughly
**f_n / 3** before you start exciting ringing. Estimated baseline ~20–30 Hz →
usable bandwidth ~7–10 Hz. Goal: push f_n up, and use feedforward shaping to get
effective bandwidth above arm-gesture content (<5–8 Hz) with margin.

## The levers (in order of leverage)

### 1. Belt tensile stiffness — `k ∝ E·A` (biggest mechanical lever)
- Axial (longitudinal) stiffness of a span = `E·A / L` — set by **cord modulus ×
  cross-section**, NOT by tension (see tension note).
- **Steel cord (E ≈ 200 GPa) ≫ fiberglass (≈ 70 GPa) ≫ polyester.**
- Width: 15 mm ≈ 2.5× the section of 6 mm.
- Combined **15 mm steel-core vs 6 mm glass-core ≈ 3–7× stiffer** → f_n up √(3–7)
  ≈ **1.7–2.7×** → roughly **40–55 Hz**, lifting usable bandwidth ~7→~15 Hz.
  This single change roughly doubles your responsiveness ceiling. Non-negotiable.
- Cost of steel cord: a **minimum bend radius** → idlers must be larger (≥ ~20 mm
  toothed; avoid 16 mm/625-class idlers) or the cord fatigues.

### 2. Free-span length — `k ∝ 1/L`
- Shorten the unsupported belt run between the carriage and the nearest pulley.
- Can't beat CoreXY topology, but place motors/idlers to keep carriage-to-pulley
  runs short; add an idler to break the single longest span if needed.

### 3. Moving mass — `f_n ∝ 1/√m`
- Halving moving mass raises f_n by 41%. Every gram on the head helps here too —
  reinforces the light coarse-Z motor and a light (carbon/boxed) gantry beam.

### 4. Belt tension — a nuance, NOT a stiffness knob
- Tension does **not** meaningfully raise *axial* cord stiffness.
- It matters for two other reasons:
  - Keeps the **slack side from going slack** under peak accel force (slack side
    going loose = lost stiffness + backlash). Peak carriage force ~70 N → slack
    side stays taut if preload `T > F/2 ≈ 35 N`; use **~50–80 N/belt** for margin.
  - Raises the **transverse "guitar-string" mode** of long spans (stops them
    singing). That mode rises with tension; axial stretch does not.
- Don't over-tension beyond this — no stiffness gain, just bearing load + fatigue.

## Compliance the belt formula ignores — frame & gantry modes
- **Use linear rails (MGN12), not V-wheels** — wheels are a major compliance source.
- **Rigid gantry beam** (carbon tube or boxed extrusion): a flexing/twisting beam
  is its own low mode.
- **Anti-rack:** CoreXY can twist the gantry out of square because the two belt
  forces act at separated points. Keep the beam torsionally stiff and the bearing
  spacing wide.

## Control-side — works WITH open-loop steppers
- **Input shaping (ZV / ZVD / EI shaper) on the commanded trajectory is
  feedforward** → it works open-loop (this is exactly how fast CoreXY printers hit
  high accel without ringing). Tune the shaper to the measured f_n.
- This is the cheapest, highest-leverage single move. It raises *effective*
  bandwidth without changing the mechanics.

## MEASURE, don't guess
- Mount an **accelerometer (ADXL345)** on the carriage; impulse/sweep test to read
  the actual resonance peak(s) (Klipper-style resonance measurement, or a quick
  belt-twang FFT). Design the input shaper around the measured peak.
- Re-measure after the steel-core belt + rail upgrades to confirm the new f_n.

## Recommended config & actions
- Belt: **Gates 2GT/3GT, 15 mm, STEEL core.**
- Idlers: **≥ 20 mm toothed** (steel cord bend-radius limit); minimize longest span.
- Tension: **~50–80 N/belt**, set by twang frequency or a tension gauge.
- Guides: **MGN12 rails**; rigid carbon/boxed gantry beam; wide bearing spacing.
- Control: **input shaper tuned to measured f_n**; instrument with ADXL345 first.
- Order of operations: build → measure f_n → steel belt + rails → re-measure →
  tune input shaper to the final peak.
