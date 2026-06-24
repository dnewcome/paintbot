"""ext_nozzle.py — fat-bead gel nozzle (3D-PRINTED, or buy a metal Luer tip).
   python3 cad/ext_nozzle.py -> build/ext_nozzle.stl

Slips onto the syringe Luer tip and tapers to a ~3 mm exit for heavy gel. Built
tip-up here (z=0 is the syringe end); on the head it points -Z toward the canvas.
"""
import os
from build123d import *
from params_extruder import NOZ_BORE, NOZ_CONE_LEN, NOZ_BASE_OD

COLLAR_H  = 6.0          # base collar that grips the Luer tip
TIP_OD    = NOZ_BORE + 2.0       # 5.0 -> ~1 mm wall at the tip
SOCKET_D  = 4.5          # slip socket for a 6% male Luer tip (~4 mm)
SOCKET_H  = 6.0

def part():
    collar = Cylinder(NOZ_BASE_OD/2, COLLAR_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    cone = Pos(0, 0, COLLAR_H) * Cone(NOZ_BASE_OD/2, TIP_OD/2, NOZ_CONE_LEN,
                                      align=(Align.CENTER, Align.CENTER, Align.MIN))
    p = collar.fuse(cone)
    # through bore
    p = p.cut(Pos(0, 0, -0.5) * Cylinder(NOZ_BORE/2, COLLAR_H + NOZ_CONE_LEN + 1.0,
                                         align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # Luer-tip slip socket from the base
    p = p.cut(Pos(0, 0, -0.5) * Cylinder(SOCKET_D/2, SOCKET_H + 0.5,
                                         align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return p

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/ext_nozzle.stl")
    import trimesh; m = trimesh.load("build/ext_nozzle.stl")
    print("ext_nozzle:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
