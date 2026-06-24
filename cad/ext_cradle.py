"""ext_cradle.py — syringe barrel cradle (3D-PRINTED).
   python3 cad/ext_cradle.py -> build/ext_cradle.stl

Caps the bottom ends of the two guide rods + leadscrew and holds the syringe barrel
at the same -Y offset as the carriage's plunger capture. The barrel's finger flange
is trapped in a horizontal slot (Z gap) so the barrel reacts both the dispense push
(flange floor) and the draw pull (flange ceiling). Barrel slides in from the front;
its rod/plunger passes up through a clearance channel to the carriage.
"""
import os
from build123d import *
from params_extruder import (
    BODY_W, GUIDE_SPACING, GUIDE_ROD_D, SCREW_OD,
    SYR_BARREL_OD, SYR_FLANGE_W, SYR_FLANGE_THK,
)

BLK_H      = 18.0
SYR_OFFSET = 30.0                 # match ext_carriage plunger axis
BARREL_CL  = SYR_BARREL_OD + 1.0  # 17.5 barrel slide channel
FLANGE_SLOT_X = SYR_FLANGE_W + 3.0          # 33.0 admits the finger ears
FLANGE_GAP = SYR_FLANGE_THK + 0.6           # 3.6 Z gap that traps the flange
FLOOR      = 10.0                 # barrel-channel height below the flange slot
ROD_CH     = 8.0                  # plunger-rod clearance above the flange
SCREW_CL   = SCREW_OD + 2.0       # 10.0 (clearance / optional bottom bearing seat)

def part():
    blk = Pos(0, -16, 0) * Box(BODY_W, 44.0, BLK_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    p = blk
    cuts = []
    # guide-rod seats (press fit) + central screw clearance
    for sx in (-1, 1):
        cuts.append(Pos(sx*GUIDE_SPACING/2, 0, -0.5) *
                    Cylinder(GUIDE_ROD_D/2, BLK_H + 1.0,
                             align=(Align.CENTER, Align.CENTER, Align.MIN)))
    cuts.append(Pos(0, 0, -0.5) * Cylinder(SCREW_CL/2, BLK_H + 1.0,
                                           align=(Align.CENTER, Align.CENTER, Align.MIN)))
    p = p.cut(*cuts)

    # --- barrel holder at (0, -SYR_OFFSET) ---
    # barrel slide channel (front-opening) up to the flange-slot floor
    p = p.cut(Pos(0, -SYR_OFFSET, -0.5) *
              Box(BARREL_CL, 22.0, FLOOR + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # finger-flange capture slot: horizontal Z gap, opens at front
    p = p.cut(Pos(0, -SYR_OFFSET, FLOOR) *
              Box(FLANGE_SLOT_X, 22.0, FLANGE_GAP, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # plunger-rod clearance above the flange, through the top, opens at front
    p = p.cut(Pos(0, -SYR_OFFSET, FLOOR + FLANGE_GAP) *
              Box(ROD_CH, 22.0, BLK_H - FLOOR - FLANGE_GAP + 1.0,
                  align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return p

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/ext_cradle.stl")
    import trimesh; m = trimesh.load("build/ext_cradle.stl")
    print("ext_cradle:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
