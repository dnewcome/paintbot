"""plate_xcarriage.py — X-carriage plate (LASER-CUT acrylic/ply). Rides the gantry
X-rail (MGN12 block), clamps both CoreXY belt ends, carries the tool-head interface.
   python3 cad/plate_xcarriage.py -> build/plate_xcarriage.stl + .dxf

Flat plate: profile() is the 2D laser outline+holes (DXF); part() extrudes it to
PLATE_T for an STL fit/watertight check. Placeholders flagged in params_frame.py.
"""
import os
from build123d import *
from params_frame import (PLATE_T, CORNER_R, XC_W, XC_H, MGN12_HOLE_X, MGN12_HOLE_Y,
                          MGN12_BOLT, CLAMP_BOLT, CLAMP_PITCH, TOOL_BC_X, TOOL_BC_Y,
                          TOOL_BOLT)

BELT_OFFSET_Y = XC_H/2 - 10.0     # belt clamps near the top edge, straddling center
BELT_SPAN_X   = 50.0              # the two belt ends clamp on opposite sides

def profile():
    with BuildSketch() as sk:
        RectangleRounded(XC_W, XC_H, CORNER_R)
        # MGN12 block mounting holes (4), centered
        with Locations(*[(x, y) for x in (-MGN12_HOLE_X/2, MGN12_HOLE_X/2)
                                 for y in (-MGN12_HOLE_Y/2, MGN12_HOLE_Y/2)]):
            Circle(MGN12_BOLT/2, mode=Mode.SUBTRACT)
        # tool-head interface (4x), centered
        with Locations(*[(x, y) for x in (-TOOL_BC_X/2, TOOL_BC_X/2)
                                 for y in (-TOOL_BC_Y/2, TOOL_BC_Y/2)]):
            Circle(TOOL_BOLT/2, mode=Mode.SUBTRACT)
        # two belt-end clamps (2 screws each), left + right near the top
        for sx in (-BELT_SPAN_X/2, BELT_SPAN_X/2):
            with Locations(*[(sx + dx, BELT_OFFSET_Y) for dx in (-CLAMP_PITCH/2, CLAMP_PITCH/2)]):
                Circle(CLAMP_BOLT/2, mode=Mode.SUBTRACT)
    return sk.sketch

def part():
    return extrude(profile(), amount=PLATE_T)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/plate_xcarriage.stl")
    exporter = ExportDXF(unit=Unit.MM)
    exporter.add_shape(profile())
    exporter.write("build/plate_xcarriage.dxf")
    import trimesh; m = trimesh.load("build/plate_xcarriage.stl")
    print("plate_xcarriage:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight,
          "| dxf:", os.path.exists("build/plate_xcarriage.dxf"))
