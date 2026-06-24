"""clamp_plate.py — flexure blade sandwich plate (3D-PRINTED, x4: 2 carrier + 2 ground).
   python3 cad/clamp_plate.py -> build/clamp_plate.stl

Pinches a spring-steel blade against a carrier shelf or a ground arm. Two M3
clearance bolts straddle the blade (spaced CLAMP_BOLT_DY in Y).
"""
import os
from build123d import *
from params import SHELF_X, BLADE_W, CLAMP_PLATE_T, CLAMP_BOLT_DY, M3_CLEAR

PLATE_X = SHELF_X
PLATE_Y = BLADE_W + 6.0   # slightly wider than blade

def part():
    p = Box(PLATE_X, PLATE_Y, CLAMP_PLATE_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    for dy in (CLAMP_BOLT_DY/2, -CLAMP_BOLT_DY/2):
        p = p.cut(Pos(0, dy, -0.5) * Cylinder(M3_CLEAR/2, CLAMP_PLATE_T + 1.0,
                                              align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return p

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/clamp_plate.stl")
    import trimesh; m = trimesh.load("build/clamp_plate.stl")
    print("clamp_plate:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
