# Bill of Materials (consolidated, first-pass)

Three buildable units: **(A) voice-coil brush head**, **(B) its driver**, **(C) the
planar-plate CoreXY frame**. The brush head + driver are testable on the existing
Shapeoko HDZ before the frame exists. Quantities/specs are first-pass — verify
against datasheets before ordering.

## A. Voice-coil brush head
| Item | Spec | Qty | Notes |
|---|---|---|---|
| Pole | 1018 steel, Ø16×28 + register | 1 | lathe (`pole.py`) |
| Cup | 1018 steel, Ø32×46, opens down | 1 | lathe (`steel_cup.py`) |
| Magnet | NdFeB N52 disc Ø16×10, axial | 1 | K&J-class |
| Magnet wire | AWG26 enamel | ~10 m | ~160 turns, k_f≈3.3–4.2 N/A |
| Flexure blades | spring steel shim, t=0.1, ~122×20 | 2 | etch/laser/waterjet (`blade.py`) |
| Bobbin | printed flangeless former | 1 | `bobbin.py` |
| Carrier | printed | 1 | `carrier.py` |
| Brush holder | printed, 8 mm ferrule | 1 | `brush_holder.py` |
| Clamp plates | printed | 4 | `clamp_plate.py` (2 carrier + 2 ground)* |
| Body collar | printed, Ø65 HDZ mount | 1 | `body_collar.py` |
| Flexure ground | printed U-frame | 1 | `flexure_ground.py` |
| Brush | round, 8 mm ferrule | — | the tool |
| Fasteners | M3 (attach/clamp), M5 (collar↔ground) | — | + 3× long M3 stack |
| Epoxy | for magnet/pole bond + coil-to-former | — | |
\* ground needs 4 clamp plates (2 per blade end); add 2 more if clamping both ends.

## B. Voice-coil driver
| Item | Spec | Notes |
|---|---|---|
| H-bridge | DRV8874 (or DRV8412 / DRV8701+MOSFETs) | 24 V, ~6 A peak |
| Current sense | INA240A2 + 10 mΩ ≥1 W shunt | bidirectional |
| MCU | STM32G474 (or Teensy 4.0) | 20 kHz current loop |
| Supply | 24 V, bulk cap ≥470 µF low-ESR | |
| Comms | CAN-FD transceiver (final) / USB (proto) | |
| Encoder (opt) | AS5311 + 2 mm-pole strip | position v2 |

## C. Planar-plate CoreXY frame (landscape 4×3 ft)
| Item | Spec | Qty | Notes |
|---|---|---|---|
| Steppers | NEMA23 high-torque ≥2.5–3 N·m, low-L, dual-shaft | 2 | open-loop initially |
| Stepper drivers | 4.5 A, 56 V (owned) | 2 | |
| Belt | GT2/GT3 15 mm **steel-core** | ~12 m | resonance-critical |
| Pulleys | 30T 2GT, motor bore | 2 | ~2000 rpm @ 2 m/s |
| Idlers | ≥20 mm toothed (steel-cord bend radius) | 8 | BL/BR + 4 gantry + 2 crossover |
| MGN12 rail | ~1370 mm (X gantry) | 1 | + blocks |
| MGN12 rail | ~1120 mm (Y uprights) | 2 | + blocks |
| Plates | laser acrylic/ply (Al keepers later) | — | `plate_*.py` DXFs |
| 8020 extrusion | 2040/4040, raked easel | — | perimeter + gantry beam |
| Counterbalance | constant-force spring(s) ~34 N | 1–2 | NEVER a counterweight |
| Control host | Teensy/STM32 streaming step/dir | 1 | low-latency teleop |
| Fasteners | M3 (MGN/idlers), M5 (8020 T-nuts) | — | |

## D. Existing / host
- **Shapeoko HDZ** — prototype host (provides XY + coarse-Z); brush head drops into
  its **65 mm router clamp** (no adapter — the `body_collar` IS the 65 mm collar).

## Still to spec
- Coarse-Z stage (full machine only — the Shapeoko/HDZ covers coarse-Z for the proto).
- Marry-to-8020 detail (T-nut positions, beam ends) + final idler-offset verification.
