"""brush_holder.py — 8 mm round-brush ferrule clamp (3D-PRINTED).
   python3 cad/brush_holder.py -> build/brush_holder.stl

Axial bore takes the brush ferrule; a pinch slot + cross screw closes the bore to
grip. Top flange bolts to the moving carrier (3x M3 on FOOT_BC to match bobbin).
"""
import os, math
from build123d import *
from params import BORE_DIA, HOLDER_OD, HOLDER_LEN, SLOT_W, M3_CLEAR, M3_TAP

FLANGE_OD = 32.0
FLANGE_TH = 4.0
BC        = 26.0          # match bobbin/carrier attach circle (ATTACH_BC)
XSCREW_Z  = HOLDER_LEN/2  # cross clamp screw height

def part():
    body = Cylinder(HOLDER_OD/2, HOLDER_LEN, align=(Align.CENTER, Align.CENTER, Align.MIN))
    flange = Pos(0, 0, HOLDER_LEN - FLANGE_TH) * \
             Cylinder(FLANGE_OD/2, FLANGE_TH, align=(Align.CENTER, Align.CENTER, Align.MIN))
    p = body.fuse(flange)
    # ferrule bore from the bottom (open) face, blind near the flange
    p = p.cut(Pos(0, 0, -0.5) * Cylinder(BORE_DIA/2, HOLDER_LEN - 2.0,
                                         align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # pinch slot: thin radial slot from the bore out through one side, up most of body
    slot = Pos(HOLDER_OD/4, 0, -0.5) * Box(HOLDER_OD/2 + 1.0, SLOT_W, HOLDER_LEN - 3.0,
                                           align=(Align.CENTER, Align.CENTER, Align.MIN))
    p = p.cut(slot)
    # cross clamp screw: clearance on +Y side, tap on -Y side, perpendicular to the slot
    p = p.cut(Pos(0, HOLDER_OD/2 + 0.5, XSCREW_Z) * Rot(90, 0, 0) *
              Cylinder(M3_CLEAR/2, HOLDER_OD/2 + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    p = p.cut(Pos(0, -HOLDER_OD/2 - 0.5, XSCREW_Z) * Rot(90, 0, 0) *
              Cylinder(M3_TAP/2, HOLDER_OD/2 + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # carrier attach holes in flange
    holes = []
    for a in (90, 210, 330):
        x = (BC/2) * math.cos(math.radians(a)); y = (BC/2) * math.sin(math.radians(a))
        holes.append(Pos(x, y, HOLDER_LEN - FLANGE_TH - 0.5) *
                     Cylinder(M3_CLEAR/2, FLANGE_TH + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return p.cut(*holes)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    export_stl(part(), "build/brush_holder.stl")
    import trimesh; m = trimesh.load("build/brush_holder.stl")
    print("brush_holder:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
