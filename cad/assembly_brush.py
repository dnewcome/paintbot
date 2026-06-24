"""assembly_brush.py — voice-coil brush head positioned as a unit (VISUALIZATION).
   python3 cad/assembly_brush.py -> build/assembly_brush.stl

Stacks the existing brush-head parts in their real relationship: steel cup opens
DOWN, pole + magnet at the back, bobbin in the annular gap, carrier rod down to the
brush holder + a stand-in brush. Carrier/flexure are not yet CAD'd, shown as stand-ins.
NOT watertight / multi-body — for viewing only.
"""
import os
from build123d import *
from params import (CUP_FLOOR, CUP_WALL_H, MAGNET_DIA, MAGNET_H, POLE_DIA, POLE_H,
                    BOBBIN_LEN, COIL_OD, CARRIER_DIA)
import pole, steel_cup, bobbin, brush_holder

def add(parts):
    t = parts[0]
    for p in parts[1:]:
        t = t + p
    return t

def assembly():
    TOTAL_H = CUP_FLOOR + CUP_WALL_H            # cup height 36
    parts = []
    # cup as built has base at z=0, opens upward in its own frame; flip so it opens DOWN
    parts.append(Pos(0, 0, TOTAL_H) * Rot(180, 0, 0) * steel_cup.part())
    # magnet disc bonded under the cup floor (now at top), pole below it into the gap
    parts.append(Pos(0, 0, TOTAL_H - CUP_FLOOR - MAGNET_H) *
                 Cylinder(MAGNET_DIA/2, MAGNET_H, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    parts.append(Pos(0, 0, TOTAL_H - CUP_FLOOR - MAGNET_H - POLE_H) * Rot(180, 0, 0) * pole.part())
    # bobbin riding the annular gap (around the pole), drawn part-inserted
    parts.append(Pos(0, 0, 2) * bobbin.part())
    # winding shown as a translucent-ish ring (solid here) around the bobbin
    parts.append(Pos(0, 0, 2) * Cylinder(COIL_OD/2, BOBBIN_LEN, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # carrier stand-in: rod from bobbin foot down past the cup mouth to the brush
    parts.append(Pos(0, 0, -70) * Cylinder(CARRIER_DIA/2, 72, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # brush holder + brush below
    parts.append(Pos(0, 0, -88) * brush_holder.part())
    parts.append(Pos(0, 0, -120) * Cylinder(4.0, 34, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # brush bristle stand-in
    return add(parts)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(assembly(), "build/assembly_brush.stl")
    import trimesh; m = trimesh.load("build/assembly_brush.stl")
    print("assembly_brush:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)))
