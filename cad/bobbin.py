"""bobbin.py — coil winding former (3D-PRINTED, then hand-wound).
   python3 cad/bobbin.py -> build/bobbin.stl

Annular tube riding the magnetic gap; bore clears the stationary pole. Two end
flanges retain the winding. Larger bottom 'foot' flange (below the cup mouth)
carries 3 holes to attach the moving carrier, plus a lead-wire notch.
"""
import os, math
from build123d import *
from params import (BOBBIN_ID, BOBBIN_OD, BOBBIN_LEN, FLANGE_OD, FLANGE_THK, M3_CLEAR)

FOOT_OD   = 32.0          # bottom attach flange — sits BELOW the cup mouth (may exceed CUP_ID)
FOOT_BC   = 26.0          # carrier attach bolt circle diameter (matches ATTACH_BC)
LEAD_W    = 2.5           # lead-wire exit notch width

def part():
    parts = []
    # winding tube (annulus), base at z=0
    tube = Cylinder(BOBBIN_OD/2, BOBBIN_LEN, align=(Align.CENTER, Align.CENTER, Align.MIN))
    parts.append(tube)
    # top winding-retainer flange
    parts.append(Pos(0, 0, BOBBIN_LEN - FLANGE_THK) *
                 Cylinder(FLANGE_OD/2, FLANGE_THK, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # bottom foot flange (attaches carrier)
    parts.append(Cylinder(FOOT_OD/2, FLANGE_THK, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    b = parts[0].fuse(*parts[1:])
    # central bore (clears pole) — overshoot both ends
    b = b.cut(Pos(0, 0, -0.5) * Cylinder(BOBBIN_ID/2, BOBBIN_LEN + 1.0,
                                         align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # carrier attach holes in foot flange (3x M3 clearance)
    holes = []
    for a in (90, 210, 330):
        x = (FOOT_BC/2) * math.cos(math.radians(a))
        y = (FOOT_BC/2) * math.sin(math.radians(a))
        holes.append(Pos(x, y, -0.5) * Cylinder(M3_CLEAR/2, FLANGE_THK + 1.0,
                                                align=(Align.CENTER, Align.CENTER, Align.MIN)))
    b = b.cut(*holes)
    # lead-wire notch through the top flange (radial slot to let winding leads out)
    notch = Pos(FLANGE_OD/2 - 2, 0, BOBBIN_LEN - FLANGE_THK - 0.5) * \
            Box(6, LEAD_W, FLANGE_THK + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return b.cut(notch)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/bobbin.stl")
    import trimesh; m = trimesh.load("build/bobbin.stl")
    print("bobbin:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
