# Gel Extrusion Head — Motor-Driven Syringe (Dip-and-Load)

A second interchangeable tool head for the paintbot: a **positive-displacement
syringe pump** that draws thick gel-viscosity medium from a well and deposits it
as fat impasto beads. Mounts on the existing **ShopBot** like the brush head, and
later on the CoreXY frame. Complementary to — not a replacement for — the
voice-coil brush.

## Where it fits vs. the brush head
| | Voice-coil brush | Gel extruder (this) |
|---|---|---|
| Control variable | **Force** (current = line weight) | **Volume** (steps = mm³ deposited) |
| Bandwidth | high (live feel, <20 ms) | low — feedforward metering, fights ooze |
| Digital-twin role | live-feel strokes | deliberate material deposition |
| Loading | dip brush in paint | **dip nozzle, reverse-draw a charge** |

**Key mindset:** the extruder is NOT a high-bandwidth head. Thick paint is
compliant and slow to relax, so you command volume open-loop-ish with feedforward
(linear-advance-style lead) and rely on **retraction** to stop ooze at stroke end —
exactly like a 3D-printer paste extruder. Don't expect brush-like responsiveness.

## Locked decisions (2026-06-24)
- **Topology:** leadscrew-driven syringe plunger (positive displacement). Only
  topology that both *draws* (reverse) and *retracts* cleanly. Pneumatic rejected
  (air compressibility = mush + lag); progressive-cavity rejected (can't refill).
- **Refill:** **single-bore reverse-fill** — dip one moderate nozzle deep in a
  well, reverse the motor to draw a charge. No valves. (Fat-bead nozzle is large
  enough to draw through; the valve/selector complexity isn't justified.)
- **Medium / nozzle:** **heavy gel, fat bead → ~3 mm nozzle.** Low pressure, very
  forgiving. This is the easy corner of the design space.
- Mounts as a ShopBot tool head; reuses the common ShopBot interface plate.

## Sizing — why a small bore
Plunger force = nozzle pressure × plunger area. Smaller bore = less force, finer
volume resolution. Heavy gel through a fat 3 mm nozzle is low pressure (~2–4 bar):

| Syringe | Plunger ID | Area | Force @ 4 bar |
|---|---|---|---|
| 30 cc | 21.7 mm | 370 mm² | ~150 N |
| **10 cc** | **14.5 mm** | **165 mm²** | **~66 N** |

**Decision: 10 cc Luer-lock barrel.** ~66 N working force is trivial for a NEMA17 +
leadscrew. Even the 10-bar worst case (~165 N) is in reach, so there's huge margin.

### Drive train
- **NEMA17** + flexible coupling → **T8 leadscrew, 8 mm lead** (2 mm pitch ×
  4-start) with anti-backlash brass nut.
  - Force: `F = 2π·τ·η/lead ≈ 2π·0.4·0.3/0.008 ≈ 94 N` continuous — covers the
    66 N case with margin. (Drop to **2 mm lead** for ~370 N + 4× resolution if a
    finer nozzle / stiffer medium is ever wanted; costs 4× speed.)
  - 8 mm lead chosen for **retraction speed** — fast retract is what kills ooze.
  - Resolution: 8 mm × 165 mm² = 1320 mm³/rev ÷ (200 × 16 µsteps) ≈ **0.4 mm³/µstep.**
- **2× Ø8 guide rods** flank the screw → carriage can't rotate (no anti-rotation
  feature needed on the nut) and takes the plunger side load.

### Refill (draw) is flow-limited, not force-limited
Drawing gel in is capped by atmospheric pressure pushing it through the nozzle
(~1 bar over 165 mm² ≈ 16 N — nothing). The real limit is **cavitation / air
ingress** if you draw faster than gel flows through the nozzle. So: **draw slowly,
nozzle fully submerged in a deep well**, then a small forward purge to clear the
tip before painting.

## Mechanical architecture (top = ShopBot, bottom = canvas)
```
  [ ShopBot interface plate ]          ← shared with brush head (bolt pattern TBD)
  [ Motor top plate ]  NEMA17 + flex coupling
  [ Leadscrew (T8x8) + 2x Ø8 guide rods ]
  [ Plunger carriage ]                 ← brass nut + 2 linear bearings;
       C-slot CAPTURES the plunger thumb-rest  → pushes AND pulls (mandatory for draw)
  [ Syringe barrel ]  10 cc Luer-lock, held in a bottom cradle (keyhole grips finger flange)
  [ Luer nozzle ]  ~3 mm conical, printed/metal
```
**Critical detail:** the carriage must *capture* the plunger flange (a C-slot the
thumb-rest slides into), not just bear on it — otherwise reverse can't draw.

## Control / calibration
- **e-steps:** calibrate mm³/step by weighing dispensed mass (density known).
- **Retraction:** tune retract distance + speed empirically to stop ooze at stroke
  end (start ~1–3 mm of plunger travel).
- **Linear advance:** lead the extrude command vs. XY motion to mask the
  compliance/ooze lag of thick medium.
- **Driver:** same stepper driver family as the rest of the machine (open-loop
  fine; volume errors are forgiving and re-primed each load cycle).

## Dip-and-load cycle
1. Park over a **deep** paint well; lower until nozzle is fully submerged.
2. Slow reverse → draw a charge (rate-limited to avoid air ingress).
3. Small forward purge to prime the tip / expel any drawn air.
4. Move to canvas; deposit beads with linear-advance lead; retract at stroke end.
5. Re-load when the charge runs low (10 cc = many fat strokes).

## BOM split
- **Bought:** 10 cc Luer-lock syringes, T8×8 leadscrew + anti-backlash nut, flex
  coupling, 2× Ø8 hardened rod + linear bearings (LM8UU), NEMA17, fasteners,
  Luer nozzles/tips.
- **3D-printed:** motor top plate, plunger carriage (flange-capture C-slot),
  syringe cradle, nozzle (or use metal Luer tip), ShopBot interface plate (shared).
- **Machined:** none required (all-printed structure; this head is low-force).

## CAD (build123d) — `cad/`
Separate param file `cad/params_extruder.py` (imports the shared ShopBot interface
+ fastener constants from `params.py`). Stroke axis = Z, plunger pushes −Z (down).

| File | Fab | Status |
|---|---|---|
| `params_extruder.py` | shared dims | ✅ done |
| `ext_top_plate.py` | printed: NEMA17 + coupling + rod seats (68×60×8) | ✅ watertight |
| `ext_carriage.py` | printed: nut pocket + 2× LM8UU + plunger C-slot (68×52×26) | ✅ watertight |
| `ext_cradle.py` | printed: barrel channel + finger-flange capture (68×44×18) | ✅ watertight |
| `ext_nozzle.py` | printed Luer ~3 mm cone (12×12×20) | ✅ watertight |
| interface plate | shared with brush head (bolt pattern TBD) | ⏳ blocked on real Z-plate pattern |

**Layout note:** envelope is **68 mm wide** — Ø15 LM8UU bearings on 45 mm rod
spacing won't fit a narrower block. Syringe axis is offset **30 mm** in front (−Y)
of the leadscrew (coaxial would collide screw tip ↔ plunger). Both the carriage
plunger capture and the cradle flange capture are front-loading C-slots that trap
their disc/flange in Z (push *and* pull), so the syringe drops in from the front.

## Fit unknowns blocking CAD (need from operator)
- [ ] ShopBot Z-plate bolt pattern (shared with brush head).
- [ ] Confirm syringe brand/size → exact barrel OD, finger-flange + thumb-rest dims
      (10 cc varies between brands; cradle + C-slot key off these).
- [ ] NEMA17 length / pancake vs. standard (affects top-plate stack height).
