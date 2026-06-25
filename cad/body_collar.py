"""body_collar.py — HDZ mount collar + steel-cup holder (3D-PRINTED).
   python3 cad/body_collar.py -> build/body_collar.stl

A Ø65 cylindrical collar that drops into the Shapeoko HDZ 65 mm router clamp. The
steel cup seats up into a bore (seats on a shoulder, floor bolts to the top), opening
DOWNWARD. The collar bottom carries 4 holes to bolt the flexure_ground U-frame.
Own frame: base z=0 at the collar bottom; cup mouth exits downward (below z=0).
"""
import os, math
from build123d import *
from params import (MOUNT_DIA, MOUNT_LEN, CUP_OD, CUP_BOLT_BC, M3_TAP, M5_CLEAR)

CUP_FIT     = CUP_OD + 0.5      # 32.5 bore for the cup body
SHLDR_DIA   = CUP_OD - 4.0      # 28: shoulder the cup floor seats on
TOPWALL     = 10.0              # top wall thickness (cup-floor bolts thread here)
POCKET_H    = MOUNT_LEN - TOPWALL
VENT_DIA    = 6.0
GROUND_BC   = MOUNT_DIA - 14.0  # 51: bolt circle to the flexure_ground frame

def part():
    c = Cylinder(MOUNT_DIA/2, MOUNT_LEN, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # cup pocket from the bottom (cup seats up, opens down)
    c = c.cut(Pos(0, 0, -0.5) * Cylinder(CUP_FIT/2, POCKET_H + 0.5,
                                         align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # shoulder bore (smaller than cup OD) through the top wall + center vent
    c = c.cut(Pos(0, 0, POCKET_H - 0.5) * Cylinder(SHLDR_DIA/2, TOPWALL + 1.0,
                                                   align=(Align.CENTER, Align.CENTER, Align.MIN)))
    c = c.cut(Pos(0, 0, MOUNT_LEN - VENT_DIA - 0.5) * Cylinder(VENT_DIA/2, VENT_DIA + 1.0,
                                                              align=(Align.CENTER, Align.CENTER, Align.MIN)))
    cuts = []
    # cup-floor bolt holes (4x M3 tap), down into the top wall from the shoulder
    for a in (45, 135, 225, 315):
        x = (CUP_BOLT_BC/2) * math.cos(math.radians(a)); y = (CUP_BOLT_BC/2) * math.sin(math.radians(a))
        cuts.append(Pos(x, y, POCKET_H - 0.5) * Cylinder(M3_TAP/2, TOPWALL + 1.0,
                                                        align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # ground-frame mount holes (4x M5), up into the collar wall from the bottom
    for a in (0, 90, 180, 270):
        x = (GROUND_BC/2) * math.cos(math.radians(a)); y = (GROUND_BC/2) * math.sin(math.radians(a))
        cuts.append(Pos(x, y, -0.5) * Cylinder(M5_CLEAR/2, 14.0,
                                              align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return c.cut(*cuts)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/body_collar.stl")
    import trimesh; m = trimesh.load("build/body_collar.stl")
    print("body_collar:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
