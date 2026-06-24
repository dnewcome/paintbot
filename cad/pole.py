"""pole.py — center pole piece (1018 steel, LATHE part). Reference solid for machining.
   python3 cad/pole.py -> build/pole.stl

Bonds (epoxy) to the NdFeB magnet, which bonds to the cup floor. Pole OD + cup ID
set the radial magnetic gap the coil rides in.
"""
import os
from build123d import *
from params import POLE_DIA, POLE_H

REG_DIA = 6.0    # base register spigot, seats in magnet/cup-floor center hole
REG_H   = 2.0

def part():
    p = Cylinder(POLE_DIA/2, POLE_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # register spigot down at the base (overlaps the pole body -> real fuse volume)
    spig = Pos(0, 0, -REG_H) * Cylinder(REG_DIA/2, REG_H + 1.0,
                                        align=(Align.CENTER, Align.CENTER, Align.MIN))
    return p.fuse(spig)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/pole.stl")
    import trimesh; m = trimesh.load("build/pole.stl")
    print("pole:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
