"""ext_top_plate.py — motor + leadscrew + guide-rod top plate (3D-PRINTED).
   python3 cad/ext_top_plate.py -> build/ext_top_plate.stl

NEMA17 bolts on top (boss in a pilot recess, shaft/coupling through center). The
two Ø8 guide rods and the T8 leadscrew hang below from here; the cradle caps their
bottom ends. Corner holes bolt up to the (shared) ShopBot interface plate.
"""
import os, math
from build123d import *
from params_extruder import (
    BODY_W, PLATE_T, GUIDE_SPACING, GUIDE_ROD_D,
    NEMA17_BOLT, NEMA17_PILOT, NEMA17_BOLT_D, M3_CLEAR,
)

PLATE_Y   = 60.0
COUPLING  = 21.0          # shaft/coupling clearance through center
PILOT_DEP = 3.0           # motor-boss pilot recess depth (top face)
CORNER    = 25.0          # interface-plate bolt offset (from center, X & Y)

def part():
    p = Box(BODY_W, PLATE_Y, PLATE_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # center coupling/shaft clearance
    p = p.cut(Pos(0, 0, -0.5) * Cylinder(COUPLING/2, PLATE_T + 1.0,
                                         align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # motor-boss pilot recess in the TOP face
    p = p.cut(Pos(0, 0, PLATE_T - PILOT_DEP) *
              Cylinder(NEMA17_PILOT/2 + 0.3, PILOT_DEP + 0.5,
                       align=(Align.CENTER, Align.CENTER, Align.MIN)))
    cuts = []
    # 4 NEMA17 mount holes on the 31 mm bolt square
    h = NEMA17_BOLT/2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cuts.append(Pos(sx*h, sy*h, -0.5) *
                        Cylinder(NEMA17_BOLT_D/2, PLATE_T + 1.0,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # 2 guide-rod seats (press fit)
    for sx in (-1, 1):
        cuts.append(Pos(sx*GUIDE_SPACING/2, 0, -0.5) *
                    Cylinder(GUIDE_ROD_D/2, PLATE_T + 1.0,
                             align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # 4 corner holes up to the interface plate
    for sx in (-1, 1):
        for sy in (-1, 1):
            cuts.append(Pos(sx*CORNER, sy*CORNER, -0.5) *
                        Cylinder(M3_CLEAR/2, PLATE_T + 1.0,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return p.cut(*cuts)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/ext_top_plate.stl")
    import trimesh; m = trimesh.load("build/ext_top_plate.stl")
    print("ext_top_plate:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
