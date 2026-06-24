"""assembly_extruder.py — extruder head positioned as a unit (VISUALIZATION).
   python3 cad/assembly_extruder.py -> build/assembly_extruder.stl

Places the four printed parts + a stand-in syringe, guide rods, and leadscrew in
their real relative positions so the head reads as a machine. NOT watertight and
multi-body on purpose — this is for viewing, not printing.
"""
import os
from build123d import *
from params_extruder import GUIDE_SPACING, SYR_BARREL_OD, SYR_PLUNGER_OD
import ext_top_plate, ext_carriage, ext_cradle, ext_nozzle

OFF   = 30.0           # syringe axis offset (-Y)
CRADLE_Z = 0.0
CARR_Z   = 60.0        # carriage base — drawn mid/charged
TOP_Z    = 140.0       # top plate base
ROD_Z0   = 18.0        # rods/screw start at cradle top face

def add(parts):
    t = parts[0]
    for p in parts[1:]:
        t = t + p
    return t

def assembly():
    parts = []
    # printed parts
    parts.append(Pos(0, 0, CRADLE_Z) * ext_cradle.part())
    parts.append(Pos(0, 0, CARR_Z)   * ext_carriage.part())
    parts.append(Pos(0, 0, TOP_Z)    * ext_top_plate.part())
    # guide rods + leadscrew
    L = TOP_Z - ROD_Z0
    for sx in (-1, 1):
        parts.append(Pos(sx*GUIDE_SPACING/2, 0, ROD_Z0) *
                     Cylinder(4.0, L, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    parts.append(Pos(0, 0, ROD_Z0) * Cylinder(4.0, L, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # NEMA17 stand-in on the top plate
    parts.append(Pos(0, 0, TOP_Z + 8) * Box(42.3, 42.3, 48, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # --- stand-in syringe at (0,-OFF) ---
    parts.append(Pos(0, -OFF, -53) * Cylinder(SYR_BARREL_OD/2, 65, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # barrel
    parts.append(Pos(0, -OFF, 11.5) * Box(30, 4, 3, align=(Align.CENTER, Align.CENTER, Align.MIN)))                  # finger flange
    parts.append(Pos(0, -OFF, 12) * Cylinder(3.0, CARR_Z + 4 - 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # plunger rod
    parts.append(Pos(0, -OFF, CARR_Z + 4) * Cylinder(SYR_PLUNGER_OD/2, 3, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # thumb disc
    # nozzle, tip pointing down below the barrel
    parts.append(Pos(0, -OFF, -53) * Rot(180, 0, 0) * ext_nozzle.part())
    return add(parts)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(assembly(), "build/assembly_extruder.stl")
    import trimesh; m = trimesh.load("build/assembly_extruder.stl")
    print("assembly_extruder:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)))
