"""plate_motor_corner.py — bottom motor-corner plate (LASER-CUT acrylic/ply, x2 mirrored).
Mounts a NEMA17 on tension slots (slide to tension the belt), hosts the bottom-corner
idler, and bolts to the 8020 frame corner.
   python3 cad/plate_motor_corner.py -> build/plate_motor_corner.stl + .dxf

NEMA holes + pilot are obround SLOTS along X so the whole motor slides for tensioning.
Idler/frame positions are first-pass (see params_frame.py + routing.py).
"""
import os
from build123d import *
from params_frame import (PLATE_T, CORNER_R, MC_W, MC_H, NEMA17_PITCH, NEMA17_PILOT,
                          NEMA_BOLT, TENSION_TRAVEL, MC_IDLER, IDLER_BOLT, M5_CLEAR)

def profile():
    with BuildSketch() as sk:
        RectangleRounded(MC_W, MC_H, CORNER_R)
        # NEMA17 pilot — obround along X (lets the boss slide for tensioning)
        SlotOverall(NEMA17_PILOT + TENSION_TRAVEL, NEMA17_PILOT, mode=Mode.SUBTRACT)
        # 4 NEMA17 bolt slots (obround along X), 31 mm square
        for x in (-NEMA17_PITCH/2, NEMA17_PITCH/2):
            for y in (-NEMA17_PITCH/2, NEMA17_PITCH/2):
                with Locations((x, y)):
                    SlotOverall(NEMA_BOLT + TENSION_TRAVEL, NEMA_BOLT, mode=Mode.SUBTRACT)
        # bottom-corner idler (shoulder screw)
        with Locations(MC_IDLER):
            Circle(IDLER_BOLT/2, mode=Mode.SUBTRACT)
        # 8020 frame mounts (2x M5) along the bottom edge
        with Locations((-MC_W/2 + 12, -MC_H/2 + 10), (MC_W/2 - 12, -MC_H/2 + 10)):
            Circle(M5_CLEAR/2, mode=Mode.SUBTRACT)
    return sk.sketch

def part():
    return extrude(profile(), amount=PLATE_T)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/plate_motor_corner.stl")
    exporter = ExportDXF(unit=Unit.MM)
    exporter.add_shape(profile())
    exporter.write("build/plate_motor_corner.dxf")
    import trimesh; m = trimesh.load("build/plate_motor_corner.stl")
    print("plate_motor_corner:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight,
          "| dxf:", os.path.exists("build/plate_motor_corner.dxf"))
