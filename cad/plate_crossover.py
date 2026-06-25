"""plate_crossover.py — crossover idler bracket (LASER-CUT acrylic/ply).
Holds the 2 crossover idlers (CX1/CX2) mid-bottom; bolts to the bottom 8020 rail.
The two crossing belt strands are separated in Z by shoulder-screw length / spacers
(not in-plane), so they pass without rubbing.
   python3 cad/plate_crossover.py -> build/plate_crossover.stl + .dxf
"""
import os
from build123d import *
from params_frame import (PLATE_T, CORNER_R, CX_W, CX_H, CX_IDLER_1, CX_IDLER_2,
                          IDLER_BOLT, M5_CLEAR)

def profile():
    with BuildSketch() as sk:
        RectangleRounded(CX_W, CX_H, CORNER_R)
        with Locations(CX_IDLER_1, CX_IDLER_2):
            Circle(IDLER_BOLT/2, mode=Mode.SUBTRACT)
        # 2x M5 mounts to the bottom 8020 rail (lower edge)
        with Locations((-CX_W/2 + 12, -CX_H/2 + 8), (CX_W/2 - 12, -CX_H/2 + 8)):
            Circle(M5_CLEAR/2, mode=Mode.SUBTRACT)
    return sk.sketch

def part():
    return extrude(profile(), amount=PLATE_T)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/plate_crossover.stl")
    exporter = ExportDXF(unit=Unit.MM)
    exporter.add_shape(profile())
    exporter.write("build/plate_crossover.dxf")
    import trimesh; m = trimesh.load("build/plate_crossover.stl")
    print("plate_crossover:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight,
          "| dxf:", os.path.exists("build/plate_crossover.dxf"))
