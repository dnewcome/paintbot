"""z_carriage.py — coarse-Z carriage plate (LASER-CUT). Rides 1x MGN12 rail on 2
blocks (spaced along Z travel), carries a bought 65 mm router clamp (tool interface),
and clamps the drive belt.
   python3 cad/z_carriage.py -> build/z_carriage.stl + .dxf

The plate's vertical axis = Z travel. MGN12 block 25 mm hole pitch runs ALONG travel;
20 mm pitch across. 65 mm-clamp mount pattern is a placeholder — set ZC_CLAMP_* to the
real bought clamp.
"""
import os
from build123d import *
from params_frame import (PLATE_T, CORNER_R, ZC_W, ZC_H, ZC_BLOCK_SP, MGN12_HOLE_X,
                          MGN12_HOLE_Y, MGN12_BOLT, ZC_CLAMP_BC_X, ZC_CLAMP_BC_Y,
                          ZC_CLAMP_BOLT, ZC_BELT_BOLT, CLAMP_PITCH)

def profile():
    with BuildSketch() as sk:
        RectangleRounded(ZC_W, ZC_H, CORNER_R)
        # 2 MGN12 blocks spaced along travel (Y); each 4 holes (20 across x 25 along)
        for by in (-ZC_BLOCK_SP/2, ZC_BLOCK_SP/2):
            with Locations(*[(x, by + y) for x in (-MGN12_HOLE_X/2, MGN12_HOLE_X/2)
                                          for y in (-MGN12_HOLE_Y/2, MGN12_HOLE_Y/2)]):
                Circle(MGN12_BOLT/2, mode=Mode.SUBTRACT)
        # 65 mm router-clamp mount (4x), centered
        with Locations(*[(x, y) for x in (-ZC_CLAMP_BC_X/2, ZC_CLAMP_BC_X/2)
                                 for y in (-ZC_CLAMP_BC_Y/2, ZC_CLAMP_BC_Y/2)]):
            Circle(ZC_CLAMP_BOLT/2, mode=Mode.SUBTRACT)
        # belt-end clamp (2 screws), near the top edge
        with Locations(*[(dx, ZC_H/2 - 10) for dx in (-CLAMP_PITCH/2, CLAMP_PITCH/2)]):
            Circle(ZC_BELT_BOLT/2, mode=Mode.SUBTRACT)
    return sk.sketch

def part():
    return extrude(profile(), amount=PLATE_T)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/z_carriage.stl")
    exporter = ExportDXF(unit=Unit.MM)
    exporter.add_shape(profile())
    exporter.write("build/z_carriage.dxf")
    import trimesh; m = trimesh.load("build/z_carriage.stl")
    print("z_carriage:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight,
          "| dxf:", os.path.exists("build/z_carriage.dxf"))
