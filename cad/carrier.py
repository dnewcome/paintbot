"""carrier.py — moving member (3D-PRINTED). Links coil bobbin (top) to brush holder
   (bottom) and clamps the two flexure blades at center.
   python3 cad/carrier.py -> build/carrier.stl

Slim central column (so blades pass THROUGH and extend out to ground) with two
clamp bars at the blade heights, plus top/bottom attach flanges (3xM3 @ ATTACH_BC).
"""
import os, math
from build123d import *
from params import (CARRIER_OD, ATTACH_BC, SHELF_Z_LOW, SHELF_TH, SHELF_X, BLADE_W,
                    BLADE_GAP, CLAMP_BOLT_DY, HEATSET_M3, M3_TAP)

COL_OD   = 24.0          # r12 < blade-free start r13, so blades still clear it
COL_ID   = 18.0          # bore clears the stationary pole tip (Ø16 + 1mm/side) as it dips in
FL_OD    = CARRIER_OD    # attach flange OD (28)
FL_TH    = 5.0
SHELF_Z_UP = SHELF_Z_LOW + BLADE_GAP        # 36
H        = SHELF_Z_UP + FL_TH + 1.0          # 42 total

def part():
    parts = []
    col = Cylinder(COL_OD/2, H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    parts.append(col)
    parts.append(Cylinder(FL_OD/2, FL_TH, align=(Align.CENTER, Align.CENTER, Align.MIN)))           # bottom flange
    parts.append(Pos(0, 0, H - FL_TH) * Cylinder(FL_OD/2, FL_TH, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # top flange
    # clamp bars (top faces at the two blade heights)
    parts.append(Pos(0, 0, SHELF_Z_LOW - SHELF_TH) * Box(SHELF_X, BLADE_W, SHELF_TH, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    parts.append(Pos(0, 0, SHELF_Z_UP - SHELF_TH) * Box(SHELF_X, BLADE_W, SHELF_TH, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    c = parts[0].fuse(*parts[1:])

    cuts = []
    # central bore through the column (overshoot both ends)
    cuts.append(Pos(0, 0, -0.5) * Cylinder(COL_ID/2, H + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # attach holes: 3x M3 heat-set through each flange @ ATTACH_BC
    for a in (90, 210, 330):
        x = (ATTACH_BC/2) * math.cos(math.radians(a)); y = (ATTACH_BC/2) * math.sin(math.radians(a))
        cuts.append(Pos(x, y, -0.5) * Cylinder(HEATSET_M3/2, FL_TH + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        cuts.append(Pos(x, y, H - FL_TH - 0.5) * Cylinder(HEATSET_M3/2, FL_TH + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # clamp-plate tap holes: 2 per bar (straddle blade), tapped into the bar
    for z0 in (SHELF_Z_LOW - SHELF_TH, SHELF_Z_UP - SHELF_TH):
        for dy in (CLAMP_BOLT_DY/2, -CLAMP_BOLT_DY/2):
            cuts.append(Pos(0, dy, z0 - 0.5) * Cylinder(M3_TAP/2, SHELF_TH + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return c.cut(*cuts)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/carrier.stl")
    import trimesh; m = trimesh.load("build/carrier.stl")
    print("carrier:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
