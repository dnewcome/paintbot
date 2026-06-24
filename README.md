# paintbot

Hardware for a painting robot that mirrors an operator's brush movements in real
time (a live digital twin) and replays recorded stroke performances. A raked
**vertical CoreXY easel** (3×4 ft) carrying interchangeable, force-controlled tool
heads — a **voice-coil paint brush** and a **gel extruder** — prototyped first as
standalone heads on an existing ShopBot.

## Layout
- **[`docs/`](docs/README.md)** — design docs: architecture, motion sizing, belt
  resonance, the voice-coil actuator + brush head, and the extrusion head.
- **`cad/`** — parametric [build123d](https://github.com/gumyr/build123d) parts.
  Shared dimensions live in `cad/params.py` (and `cad/params_extruder.py`); each
  part file exports an STL and self-checks watertightness.

## Building the CAD
```bash
pip install build123d trimesh
python3 cad/<part>.py        # writes build/<part>.stl and prints a sanity line
```

Status, locked decisions, and open questions are tracked in
[`docs/README.md`](docs/README.md).
