"""bobbin.py — coil winding former (3D-PRINTED, then hand-wound).
   python3 cad/bobbin.py -> build/bobbin.stl

Flangeless former (like a speaker voice coil): coil epoxies onto the UPPER 16 mm,
riding the magnetic gap near the cup mouth. A thin top lip (clears the Ø22.5 bore)
stops the winding. The former extends down to a Ø32 FOOT flange that sits BELOW the
cup mouth and bolts to the moving carrier (3x M3 @ FOOT_BC). Lead-wire hole in foot.
"""
import os, math
from build123d import *
from params import (BOBBIN_ID, BOBBIN_OD, BOBBIN_TUBE_LEN, LIP_OD, LIP_TH,
                    FLANGE_THK, M3_CLEAR)

FOOT_OD   = 32.0          # bottom attach flange — sits BELOW the cup mouth
FOOT_BC   = 26.0          # carrier attach bolt circle (matches ATTACH_BC)
LEAD_D    = 2.5           # lead-wire pass hole in the foot

def part():
    parts = []
    tube = Cylinder(BOBBIN_OD/2, BOBBIN_TUBE_LEN, align=(Align.CENTER, Align.CENTER, Align.MIN))
    parts.append(tube)
    parts.append(Cylinder(FOOT_OD/2, FLANGE_THK, align=(Align.CENTER, Align.CENTER, Align.MIN)))   # foot
    parts.append(Pos(0, 0, BOBBIN_TUBE_LEN - LIP_TH) *
                 Cylinder(LIP_OD/2, LIP_TH, align=(Align.CENTER, Align.CENTER, Align.MIN)))         # top lip
    b = parts[0].fuse(*parts[1:])
    # central bore (clears the pole) — overshoot both ends
    b = b.cut(Pos(0, 0, -0.5) * Cylinder(BOBBIN_ID/2, BOBBIN_TUBE_LEN + 1.0,
                                         align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # carrier attach holes in the foot (3x M3 clearance)
    holes = []
    for a in (90, 210, 330):
        x = (FOOT_BC/2) * math.cos(math.radians(a)); y = (FOOT_BC/2) * math.sin(math.radians(a))
        holes.append(Pos(x, y, -0.5) * Cylinder(M3_CLEAR/2, FLANGE_THK + 1.0,
                                                align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # lead-wire hole through the foot, just outside the bore
    holes.append(Pos(BOBBIN_ID/2 + 2.0, 0, -0.5) * Cylinder(LEAD_D/2, FLANGE_THK + 1.0,
                                                            align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return b.cut(*holes)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/bobbin.stl")
    import trimesh; m = trimesh.load("build/bobbin.stl")
    print("bobbin:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
