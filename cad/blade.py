"""blade.py — flexure leaf-spring blade (BOUGHT spring-steel shim; reference/cut drawing).
   python3 cad/blade.py -> build/blade.stl

t=0.1 mm spring steel. Photochemical-etch / laser / waterjet 2 identical blades.
Holes only in the CLAMPED regions (center + both ground ends) — the free spans
(length a) stay solid where bending stress lives. k_flex ~ 0.41 N/mm (see params).
"""
import os
from build123d import *
from params import (BLADE_LEN, BLADE_W, BLADE_THK, BLADE_CC, BLADE_FREE, BLADE_GC,
                    CLAMP_BOLT_DY, M3_CLEAR)

END_X = BLADE_CC/2 + BLADE_FREE + BLADE_GC/2   # x of each ground-clamp hole group

def part():
    p = Box(BLADE_LEN, BLADE_W, BLADE_THK, align=(Align.CENTER, Align.CENTER, Align.MIN))
    holes = []
    for cx in (0.0, END_X, -END_X):              # center clamp + 2 ground clamps
        for dy in (CLAMP_BOLT_DY/2, -CLAMP_BOLT_DY/2):
            holes.append(Pos(cx, dy, -0.5) * Cylinder(M3_CLEAR/2, BLADE_THK + 1.0,
                                                      align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return p.cut(*holes)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/blade.stl")
    import trimesh; m = trimesh.load("build/blade.stl")
    print("blade:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
