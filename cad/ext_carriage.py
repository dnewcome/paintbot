"""ext_carriage.py — plunger carriage (3D-PRINTED). THE critical part.
   python3 cad/ext_carriage.py -> build/ext_carriage.stl

Rides the T8 leadscrew (anti-backlash nut on top) between two LM8UU bearings on the
guide rods. An arm reaches forward (-Y, off the screw axis) to a C-SLOT that
CAPTURES the plunger thumb-rest disc: the disc slides in from the front and is
trapped in Z between a floor (pushes the plunger down = dispense) and a ceiling
(pulls it up = draw). Capture is mandatory — a pusher that only bears on top of the
disc cannot reverse-fill. Screw is OFFSET from the plunger so the screw tip can
never collide with the plunger top.
"""
import os, math
from build123d import *
from params_extruder import (
    BODY_W, GUIDE_SPACING, GUIDE_BEARING_OD, SCREW_OD,
    NUT_FLANGE_OD, NUT_FLANGE_BC, SYR_PLUNGER_OD, SYR_PLUNGER_THK,
    M3_CLEAR, M3_TAP,
)

CARR_H     = 26.0                 # rear block height (>= LM8UU length 24)
ARM_H      = 12.0                 # forward arm height
SYR_OFFSET = 30.0                 # plunger axis ahead of (-Y) the screw axis
SCREW_CLR  = SCREW_OD + 1.0       # 9.0 screw through-bore
NUT_POCKET = 4.0                  # anti-backlash nut flange register depth (top)
DISC_SLOT  = SYR_PLUNGER_OD + 1.5 # 16.0 capture-slot width (X)
DISC_GAP   = SYR_PLUNGER_THK + 0.6# 3.6 Z gap that traps the disc
ROD_CH     = 6.0 + 1.0            # 7.0 plunger-rod clearance channel
FLOOR      = 4.0                  # material below the capture slot (push face)

def part():
    # rear block: spans both guide rods + the central screw
    rear = Box(BODY_W, 24.0, CARR_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # forward arm: overlaps rear (y -12..8) and reaches to the plunger at y=-30
    arm = Pos(0, -16, 0) * Box(24.0, 48.0, ARM_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    p = rear.fuse(arm)

    # central screw through-bore
    p = p.cut(Pos(0, 0, -0.5) * Cylinder(SCREW_CLR/2, CARR_H + 1.0,
                                         align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # anti-backlash nut flange register pocket (top face)
    p = p.cut(Pos(0, 0, CARR_H - NUT_POCKET) *
              Cylinder(NUT_FLANGE_OD/2 + 0.3, NUT_POCKET + 0.5,
                       align=(Align.CENTER, Align.CENTER, Align.MIN)))
    cuts = []
    # nut mount holes (3x M3 tap into the top)
    for a in (90, 210, 330):
        x = (NUT_FLANGE_BC/2) * math.cos(math.radians(a))
        y = (NUT_FLANGE_BC/2) * math.sin(math.radians(a))
        cuts.append(Pos(x, y, CARR_H - 9.0) *
                    Cylinder(M3_TAP/2, 9.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # two LM8UU bearing bores (press fit) on the guide rods
    for sx in (-1, 1):
        cuts.append(Pos(sx*GUIDE_SPACING/2, 0, -0.5) *
                    Cylinder(GUIDE_BEARING_OD/2, CARR_H + 1.0,
                             align=(Align.CENTER, Align.CENTER, Align.MIN)))
    p = p.cut(*cuts)

    # --- plunger capture C-slot at (0, -SYR_OFFSET) ---
    # disc slot: horizontal gap that traps the thumb-rest disc in Z; opens at front
    p = p.cut(Pos(0, -SYR_OFFSET, FLOOR) *
              Box(DISC_SLOT, 22.0, DISC_GAP, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # rod channel: from the slot floor down through the bottom, opens at front
    p = p.cut(Pos(0, -SYR_OFFSET, -0.5) *
              Box(ROD_CH, 22.0, FLOOR + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return p

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/ext_carriage.stl")
    import trimesh; m = trimesh.load("build/ext_carriage.stl")
    print("ext_carriage:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
