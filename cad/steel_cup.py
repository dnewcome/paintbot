"""steel_cup.py — stator return cup (1018 steel, LATHE part). Reference solid for machining.
   python3 cad/steel_cup.py -> build/steel_cup.stl

Opens DOWNWARD (-Z toward canvas). Floor (back-iron) at top; magnet bonds under the
floor center; pole rises... (in prototype orientation the cup's open mouth faces the
brush). Cup wall = flux return path. Floor has 4 bolt holes to the printed main_body
and a center hole to register the pole/magnet stack.
"""
import os
from build123d import *
from params import CUP_OD, CUP_ID, CUP_WALL_H, CUP_FLOOR, M3_CLEAR

TOTAL_H   = CUP_FLOOR + CUP_WALL_H
CENTER_D  = 6.2                 # clears pole register spigot (6.0)
BOLT_BC   = (CUP_OD + CUP_ID)/2 - 1.0   # bolt circle in the wall annulus, radius

def part():
    # solid blank, base at z=0
    cup = Cylinder(CUP_OD/2, TOTAL_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # hollow the bore from the open (top here) face, leaving CUP_FLOOR at the bottom
    bore = Pos(0, 0, CUP_FLOOR) * Cylinder(CUP_ID/2, CUP_WALL_H + 1.0,
                                           align=(Align.CENTER, Align.CENTER, Align.MIN))
    cup = cup.cut(bore)
    # center register hole through the floor (overshoot both faces)
    cup = cup.cut(Pos(0, 0, -0.5) * Cylinder(CENTER_D/2, CUP_FLOOR + 1.0,
                                             align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # 4 floor bolt holes (M3 clearance) on the wall-annulus bolt circle
    holes = []
    for a in (45, 135, 225, 315):
        import math
        x = (BOLT_BC/2) * math.cos(math.radians(a))
        y = (BOLT_BC/2) * math.sin(math.radians(a))
        holes.append(Pos(x, y, -0.5) * Cylinder(M3_CLEAR/2, CUP_FLOOR + 1.0,
                                                align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return cup.cut(*holes)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/steel_cup.stl")
    import trimesh; m = trimesh.load("build/steel_cup.stl")
    print("steel_cup:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
