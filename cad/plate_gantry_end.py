"""plate_gantry_end.py — gantry-end plate (LASER-CUT acrylic/ply, MOVING, x2 mirrored).
Carries the MGN12 Y-carriage block (rides the upright Y-rail), the gantry 2040 beam
end, and the 2 CoreXY gantry idlers.
   python3 cad/plate_gantry_end.py -> build/plate_gantry_end.stl + .dxf

profile() = 2D laser outline+holes (DXF); part() extrudes to PLATE_T for fit check.
Idler hole positions are FIRST-PASS placeholders (see params_frame.py) — finalized
when the single-plane routing is ported from the corexy.com reference.
"""
import os
from build123d import *
from params_frame import (PLATE_T, CORNER_R, GE_W, GE_H, MGN12_HOLE_X, MGN12_HOLE_Y,
                          MGN12_BOLT, GE_BEAM_BOLT, GE_BEAM_PITCH, IDLER_BOLT,
                          GE_IDLER_1, GE_IDLER_2, GE_YBLOCK_CX, GE_BEAM_CX)

def profile():
    with BuildSketch() as sk:
        RectangleRounded(GE_W, GE_H, CORNER_R)
        # MGN12 Y-block mounting holes (4), grouped toward the upright (-X)
        with Locations(*[(GE_YBLOCK_CX + x, y) for x in (-MGN12_HOLE_X/2, MGN12_HOLE_X/2)
                                               for y in (-MGN12_HOLE_Y/2, MGN12_HOLE_Y/2)]):
            Circle(MGN12_BOLT/2, mode=Mode.SUBTRACT)
        # gantry 2040 beam end attach (2x M5, vertical pair), inboard (+X)
        with Locations(*[(GE_BEAM_CX, dy) for dy in (-GE_BEAM_PITCH/2, GE_BEAM_PITCH/2)]):
            Circle(GE_BEAM_BOLT/2, mode=Mode.SUBTRACT)
        # 2 gantry idlers (shoulder screws)
        with Locations(GE_IDLER_1, GE_IDLER_2):
            Circle(IDLER_BOLT/2, mode=Mode.SUBTRACT)
    return sk.sketch

def part():
    return extrude(profile(), amount=PLATE_T)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/plate_gantry_end.stl")
    exporter = ExportDXF(unit=Unit.MM)
    exporter.add_shape(profile())
    exporter.write("build/plate_gantry_end.dxf")
    import trimesh; m = trimesh.load("build/plate_gantry_end.stl")
    print("plate_gantry_end:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight,
          "| dxf:", os.path.exists("build/plate_gantry_end.dxf"))
