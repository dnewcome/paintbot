# Voice Coil Driver + Control Loop

Single-phase, bidirectional, **current-mode (= force-mode)** driver for the brush
voice coil. This is the electronics/firmware that makes the head testable: the
flexure gives ~zero friction, so `F ≈ k_f·I` holds and **commanded current is brush
force** — line weight straight out of the current loop.

## Requirements (from the actuator sizing)
| Quantity | Value | Source |
|---|---|---|
| Coil resistance R | ~1.3 Ω | `docs/voice-coil-actuator.md` |
| Coil inductance L | ~0.5–2 mH (measure) | est. (160 T, steel-cored gap) |
| Force constant k_f | ~3.3–4.2 N/A | depends on built gap B (0.35–0.45 T) |
| Peak force / current | 20 N → ~5–6 A (burst) | fast dabs |
| Continuous force / current | 3–5 N → ~1.2–1.5 A | brush pressure |
| Current-loop bandwidth | ~1–2 kHz | well above the ~17 Hz suspension mode |
| Force/pressure update | ~1 kHz from host | live mirroring |

## Topology
```
  24V ──┬─[bulk cap]─┐
        │            │
        │      ┌───H-bridge───┐        ┌──── voice coil ────┐
   MCU ─┼─PWM─▶│ DRV8874-class│──OUT1──┤  (single coil)     │
        │      │ (IN1/IN2 PWM)│──OUT2──┤                    │
        │      └──────┬───────┘        └────────┬───────────┘
        │             │  inline shunt 10 mΩ ────┘
        │        INA240 (×50, bidirectional) ──▶ MCU ADC (signed I)
        │
        └─ host link: USB-serial or CAN-FD ◀── pressure/position setpoints
   (optional) AS5311 linear encoder on carrier ──▶ MCU (position x)
```
- **Power stage:** full H-bridge, **DRV8874-class** (4.5–37 V, ~6 A peak, ~3 A cont).
  Covers bursts to ~20 N; if sustained 20 N is ever needed, step up to DRV8701 +
  external MOSFETs or a DRV8412. Supply **24 V** for current-slew headroom
  (di/dt = V/L ≈ 24 A/ms at 1 mH → reaches 5 A in ~0.2 ms).
- **Drive mode:** IN1/IN2 PWM (NOT the driver's internal current chopper) so the
  **MCU closes the current loop** — needed for clean bidirectional force control.
  ~20–40 kHz PWM, with deadtime.
- **Current sense:** inline 10 mΩ shunt + **INA240** (PWM-rejecting, bidirectional,
  gain ×50): 5 A → 50 mV → 2.5 V about a Vref/2 bias → MCU ADC. Sample
  **synchronized to PWM center** to reject ripple.
- **MCU:** **STM32G4** (motor-control timers + fast ADC + CORDIC) for the real
  thing; **Teensy 4** for a fast first proto. Current loop in the PWM ISR (20 kHz).

## Control architecture (nested)
```
 host pressure setpoint ─▶ [force model] ─▶ I_cmd ─▶ [PI current loop @20kHz] ─▶ PWM
                              ▲                          ▲
              x (if encoder) ─┘            sensed I (INA240, synchronous) ┘
```
- **Inner: PI current loop** (the only fast loop). Plant = R + sL. Pole-zero
  cancel: `Kp = L·ω_bw`, `Ki = R·ω_bw`, ω_bw = 2π·1.5 kHz. With L≈1 mH, R≈1.3 Ω →
  Kp ≈ 9.4 V/A, Ki ≈ 1.2e4 V/A/s (starting points; tune on the bench).
- **Force model** (feedforward, converts desired brush force to coil current):
  `I_cmd = (F_brush + k_flex·x − m·g·ĝ) / k_f`
  - `k_flex·x` — flexure spring (needs x; if no encoder, fold the near-constant
    contact-region term into calibration).
  - `m·g·ĝ` — gravity bias; `ĝ = +1` on the ShopBot (brush DOWN, gravity along the
    stroke) vs ~0 on the final vertical easel. **Don't hard-code — it's a parameter.**
- **Outer loop (optional v1):** with an AS5311 encoder, a position PID can do clean
  lift/standoff moves (output = I_cmd); without it, the ShopBot's coarse-Z does
  lifts and this head runs pure force control.

## Calibration (bench, one-time + per-build)
1. **k_f:** clamp the head over a scale, command stepped currents, fit force vs I.
2. **k_flex:** push the carrier known deflections, read force on the scale (≈0.41 N/mm).
3. **Gravity offset:** at zero current, read the rest force (orientation-dependent).
4. **Coil R, L:** LCR meter (sets the current-loop gains).
Assemble into the force model; verify a commanded force matches a measured force.

## Protection / safety
- Driver overcurrent + thermal (built-in); firmware **continuous-current limit**
  (~2 A) to protect the coil thermally (I²R ≈ few W).
- **Host-timeout watchdog:** if setpoints stop streaming, ramp force to zero (and
  let coarse-Z lift) — never leave the coil energized into the canvas.
- Bulk cap + body-diode freewheeling for the inductive load; deadtime to avoid
  shoot-through.

## Host interface
- **Prototype:** PC streams pressure setpoints over USB-serial (or CAN) at ~1 kHz;
  MCU runs the 20 kHz current loop. USB latency ~1 ms — negligible vs. the loop.
- **Final machine:** this MCU joins the **CAN-FD** bus with the moteus axes, taking
  synchronized setpoints from the pi3hat host (single real-time timeline).

## BOM (driver board)
- DRV8874 (or DRV8412 / DRV8701+MOSFETs for more headroom)
- INA240A2 + 10 mΩ ≥1 W shunt
- STM32G474 (or Teensy 4.0)
- 24 V supply, bulk cap (≥470 µF low-ESR), gate/decoupling caps
- CAN-FD transceiver (final) or USB (proto)
- optional: AS5311 + 2 mm-pole magnetic strip (position)

## Next
- KiCad schematic + board (fits the project's existing ngspice→pcbnew→build123d
  toolchain) — deferred until the topology is bench-confirmed on a dev board.
