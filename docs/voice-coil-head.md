# Voice Coil Brush Head — Detailed Design & ShopBot Prototype

Self-contained brush-contact tool head: moving-coil VCA + double-parallelogram
flexure + paintbrush + position sensor, mounted as a tool on an existing
**ShopBot** (ShopBot = XY gantry + coarse-Z standoff; this head = fine-Z stroke +
pressure). Proves the entire contact/pressure system before the CoreXY frame exists.

## Prototype framing
- ShopBot provides XY paths (slow is fine) and coarse-Z standoff.
- This head provides fast fine-Z + **force/pressure control** (current = line weight).
- **Orientation caveat:** brush points DOWN → gravity acts ALONG the stroke axis
  (vs. horizontal in the final easel). Gravity is a constant bias in the force
  model `F = k_f·I − k_flex·x − mg`; calibrate it out, don't hard-code it.
- Validates: k_f, flexure spring rate & straightness, force/bandwidth, brush
  loading/lift behavior on real paint, the driver + control loop.

## Mechanical stack-up (top = ShopBot, bottom = canvas)
```
  [ ShopBot tool mount ]            ← interface plate (fit TBD)
  [ Stator housing ]                ← holds magnetic circuit; flexure ground
      back-plate / magnet / center pole / front-plate  → radial gap
  [ Flexure: compound (double) parallelogram ]
      ground clamps → 2 blade stages → moving carrier
  [ Moving carrier (axial) ]
      top: coil bobbin sits IN the gap
      bottom: brush holder
  [ Brush holder / quick-change ] → paintbrush
  [ Position sensor ] reads carrier (optional for v1 — force≈current)
```

## Magnetic circuit (moving coil, speaker-motor topology)
Radial-gap field so force constant `k_f = B·L·I` is ~position-independent over the
stroke (the reason for a proper gap vs. a nonlinear solenoid).

| Part | Material | First-cut dims |
|---|---|---|
| Center pole | 1018 steel, turned | Ø16 mm × (magnet+gap height) |
| Magnet | NdFeB N52 disc, axial | Ø25 × 10 mm (K&J-class) |
| Back plate | 1018 steel | Ø30 × 6 mm |
| Front plate | 1018 steel washer | OD30 / ID21 × 6 mm |
| Radial gap | — | ~2 mm (coil ~1 mm + ~0.5 mm clearance/side) |
| Coil | AWG26, ~160 turns | mean Ø~20 mm, k_f ≈ 5 N/A, R ≈ 1.3 Ω |

Expected gap B ~0.4–0.6 T → plenty (we're force-limited, not accel-limited; even
0.3 T works, just more current). Steel parts are simple turned cylinders/washers
(lathe or machine-shop / waterjet-stack); magnets bought; coil hand-wound; rest 3D-printed.

## Flexure — compound (double) parallelogram
- Two parallelogram stages with an intermediate carrier cancel the parasitic axial
  foreshortening of a single parallelogram → straight-line motion over ~10 mm.
- Blades: spring steel or BeCu shim, ~0.15–0.25 mm thick, clamped between printed
  spacers. Pick thickness so (a) spring rate is small vs. ~3–5 N working force and
  (b) blade stress < fatigue limit at full 10 mm deflection (infinite-life).
- Flexure also carries side load → coil only pushes axially; no separate rail.
- v1 simplification: a single parallelogram is acceptable (small parasitic, brush
  is compliant); compound is the target for clean position fidelity.

## Position sensor (optional for v1)
- Force ≈ current already, and flexure makes x↔force linear, so v1 can run
  current-mode force control with NO encoder.
- When wanted: AS5311 + 2 mm-pole magnetic strip on the carrier (~µm-class), or a
  cheap linear Hall (DRV5055) reading a carrier magnet (coarse but adequate).

## Driver (single-phase current-mode)
- H-bridge (DRV8874-class) + inline current sense (INA240), current PI loop
  @ 10–20 kHz on a Teensy/STM32; brush force = commanded current.
- Buy-path alt: Maxon ESCON in current/torque mode.

## BOM split
- **Bought:** NdFeB magnet, magnet wire (AWG26), shim stock (spring steel/BeCu),
  fasteners, H-bridge + current sense + MCU, (optional encoder).
- **Machined (simple, outsourceable):** 3 steel parts (pole, back plate, front plate).
- **3D-printed:** stator housing, coil bobbin, flexure spacers/clamps, brush
  holder/quick-change, sensor mount, ShopBot interface plate.
- **Hand-wound:** the coil.

## CAD (build123d) — `cad/`
Shared dims in `cad/params.py` (single source of truth). Cup opens DOWNWARD
(-Z toward canvas); magnet+pole at the back, coil rides the annular gap and
extends out the open mouth to the carrier + brush. Common attach interface:
**3× M3 on a 22 mm bolt circle** (bobbin foot ↔ carrier ↔ brush holder).

| File | Fab | Status |
|---|---|---|
| `pole.py` | lathe 1018 steel (Ø16×28 + register) | ✅ watertight |
| `steel_cup.py` | lathe 1018 steel (Ø32×46, opens down) | ✅ watertight |
| `bobbin.py` | printed winding former | ✅ watertight — but see rework below |
| `brush_holder.py` | printed, 8 mm ferrule pinch-clamp | ✅ watertight |
| `carrier.py` | printed: column + 2 blade clamp bars + attach flanges | ✅ watertight |
| `blade.py` | bought shim steel (t=0.1) — cut drawing, ×2 | ✅ watertight |
| `clamp_plate.py` | printed blade sandwich plate, ×4 | ✅ watertight |
| `main_body.py` | printed: cup mount + flexure ground + ShopBot interface | ⏳ blocked on real Z-plate bolt pattern |

### Flexure spring rate (validated)
Symmetric 2-blade (4 guided-cantilever segments): `k = 4·E·w·t³/a³`. With spring
steel t=0.1, w=20, a=34 → **k ≈ 0.41 N/mm**; stress at 5 mm ≈ 260 MPa (infinite
life). Measured-from-CAD **mover mass ≈ 37 g** → gravity sag **0.9 mm**, accel
headroom ~55 g, suspension resonance ~17 Hz (extend via closed loop; tune k by
swapping blade-shim thickness, k ∝ t³).

### Z-stack & remaining geometry (next)
Cup opens down; magnet+pole at the back; **pole lengthened to 28 mm** so the coil
stays in the radial gap over ±5 mm travel; carrier bore opened to Ø18 to clear the
pole tip; shared attach interface widened to **3× M3 @ 26 mm BC, Ø32 flanges**.
- **bobbin rework:** coil rides the gap *near the cup mouth*; the Ø32 foot must sit
  *below* the mouth (won't fit the Ø22.5 bore). Bobbin needs a ~28 mm tube
  extension (winding on the upper 16 mm, foot below the mouth). Current bobbin is
  the short winding former only — extend next.
- **main_body:** waits on the real ShopBot Z-plate bolt pattern.

## Fit unknowns blocking CAD (need from operator)
- [ ] ShopBot tool-mount interface (spindle/router diameter to clamp, or Z-plate bolt pattern).
- [ ] Paintbrush: ferrule diameter + brush type (round/flat) for the holder.
- [ ] Steel-part fab: in-house lathe/mill vs. order-out (no-machining alt designs).
- [ ] 3D printer material + build volume (PETG/ABS/nylon; housing size).
