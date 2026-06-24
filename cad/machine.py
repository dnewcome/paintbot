"""machine.py — raked CoreXY easel MASSING model (VISUALIZATION ONLY).
   python3 cad/machine.py -> build/machine.stl

A blocky, to-scale stand-in for the whole machine so the design reads in 3D:
3x4 ft work area, raked vertical easel, frame-mounted CoreXY motors, a gantry that
moves in Y, an X carriage, and a simplified tool head pointing at the canvas.
These are massing boxes, NOT real extrusion/joinery. Units mm. Canvas plane = z=0
(easel surface); machine sits in front (+z). Whole easel raked back about its base.

Coordinate frame (before rake): X = horizontal, Y = vertical (up), Z = toward operator.
"""
import os
from build123d import *

# ---- work area + frame ----
WORK_X   = 914.0    # 3 ft horizontal
WORK_Y   = 1219.0   # 4 ft vertical
MARGIN   = 250.0    # belt/motor/travel margin per side
EXT      = 40.0     # frame extrusion section (40x40 massing)
FRAME_X  = WORK_X + 2*MARGIN
FRAME_Y  = WORK_Y + 2*MARGIN
RAKE_DEG = 15.0     # lean-back angle
GANTRY_Y = 720.0    # gantry height (Y) for this view
CARR_X   = 120.0    # X-carriage position along the gantry

def add(parts):
    t = parts[0]
    for p in parts[1:]:
        t = t + p
    return t

def beam(l, w, h, x, y, z):
    return Pos(x, y, z) * Box(l, w, h, align=(Align.CENTER, Align.CENTER, Align.MIN))

def machine():
    p = []
    hx = FRAME_X/2
    # outer frame rectangle (4 members), sitting just behind the canvas plane (z<0)
    zf = -EXT
    p.append(beam(FRAME_X, EXT, EXT, 0, 0, zf))            # bottom rail
    p.append(beam(FRAME_X, EXT, EXT, 0, FRAME_Y, zf))      # top rail
    p.append(beam(EXT, FRAME_Y, EXT, -hx + EXT/2, FRAME_Y/2, zf))  # left post
    p.append(beam(EXT, FRAME_Y, EXT,  hx - EXT/2, FRAME_Y/2, zf))  # right post
    # CoreXY motors (NEMA23) fixed at the two top corners
    for sx in (-1, 1):
        p.append(Pos(sx*(hx - 40), FRAME_Y - 10, zf - 20) *
                 Box(57, 57, 80, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # corner idler pulleys
    for sx in (-1, 1):
        for yy in (40, FRAME_Y - 40):
            p.append(Pos(sx*(hx - 40), yy, zf + EXT) *
                     Cylinder(9, 16, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # gantry beam (moves in Y) spanning the width, in front of the frame
    p.append(beam(FRAME_X - 2*EXT, 50, 40, 0, GANTRY_Y, 10))
    # X carriage on the gantry
    p.append(Pos(CARR_X, GANTRY_Y, 20) * Box(90, 70, 70, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # simplified tool head on the carriage, reaching toward the canvas (-z)
    p.append(Pos(CARR_X, GANTRY_Y, -2) * Box(70, 70, 90, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    p.append(Pos(CARR_X, GANTRY_Y, -2) * Rot(180, 0, 0) * Cone(8, 1.5, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # canvas outline (thin slab) in the work area, centered
    p.append(Pos(0, FRAME_Y/2, -EXT - 6) * Box(WORK_X, WORK_Y, 6, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    asm = add(p)
    # rake the whole easel back about the bottom edge (X axis at y=0)
    return Rot(-RAKE_DEG, 0, 0) * asm

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(machine(), "build/machine.stl")
    import trimesh; m = trimesh.load("build/machine.stl")
    print("machine:", (m.bounds[1]-m.bounds[0]).round(0),
          "bodies:", len(m.split(only_watertight=False)))
