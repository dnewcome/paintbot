"""flexure_ground.py — flexure ground U-frame (3D-PRINTED). Holds the 2 blades' ENDS
at x=±GROUND_X on up-facing pads at the two blade heights; bridges over the cup mouth
and bolts up to body_collar.
   python3 cad/flexure_ground.py -> build/flexure_ground.stl

Own frame: z=0 = carrier bottom level; pads' top faces at SHELF_Z_LOW and +BLADE_GAP;
bridge on top bolts to the collar (4x M5 @ collar's GROUND_BC). Center hole clears the
cup mouth + bobbin.
"""
import os, math
from build123d import *
from params import (GROUND_X, SHELF_Z_LOW, BLADE_GAP, CUP_OD, MOUNT_DIA, BLADE_W,
                    CLAMP_BOLT_DY, M3_TAP, M5_CLEAR)

# Side rails sit OUTBOARD of the blade ends (blade reaches ±BLADE_LEN/2≈61) so the
# clamp pads' up-faces stay exposed; pads cantilever inward to the blade clamp at
# x=±GROUND_X and carry THROUGH taps (exit below -> no sealed cavity).
RAIL_CX  = 74.0          # rail center X (outboard of blade end + clamp plate)
RAIL_W   = 12.0
RAIL_Y   = 24.0
RAIL_Z   = 50.0          # rails rise to the bridge
BR_Z0    = 46.0; BR_T = 10.0   # bridge overlaps rails by 4 mm (no sliver weld)
BR_X     = 2*RAIL_CX + RAIL_W + 8
BR_Y     = 60.0
PAD_CX   = 64.0          # pad center: spans blade clamp (54) out to the rail
PAD_X    = 34.0; PAD_Y = 28.0; PAD_T = 4.0   # PAD_Y≠RAIL_Y avoids coincident faces
Z_UP     = SHELF_Z_LOW + BLADE_GAP        # 36
CTR_HOLE = CUP_OD + 2.0                   # clears cup mouth + bobbin
GROUND_BC = MOUNT_DIA - 14.0              # 51, matches body_collar

def _additive():
    parts = [Pos(0, 0, BR_Z0) * Box(BR_X, BR_Y, BR_T, align=(Align.CENTER, Align.CENTER, Align.MIN))]
    for sx in (-RAIL_CX, RAIL_CX):
        parts.append(Pos(sx, 0, 0) * Box(RAIL_W, RAIL_Y, RAIL_Z, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    for sx in (-PAD_CX, PAD_CX):
        for ztop in (SHELF_Z_LOW, Z_UP):
            parts.append(Pos(sx, 0, ztop - PAD_T) * Box(PAD_X, PAD_Y, PAD_T,
                         align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return parts

def _cuts():
    cuts = [Pos(0, 0, BR_Z0 - 0.5) * Cylinder(CTR_HOLE/2, BR_T + 1.0,
                                              align=(Align.CENTER, Align.CENTER, Align.MIN))]
    for a in (45, 135, 225, 315):
        x = (GROUND_BC/2) * math.cos(math.radians(a)); y = (GROUND_BC/2) * math.sin(math.radians(a))
        cuts.append(Pos(x, y, BR_Z0 - 0.5) * Cylinder(M5_CLEAR/2, BR_T + 1.0,
                                                      align=(Align.CENTER, Align.CENTER, Align.MIN)))
    for sx in (-GROUND_X, GROUND_X):                 # taps at the blade clamp x
        for ztop in (SHELF_Z_LOW, Z_UP):
            for dy in (CLAMP_BOLT_DY/2, -CLAMP_BOLT_DY/2):
                cuts.append(Pos(sx, dy, ztop - PAD_T - 3) * Cylinder(M3_TAP/2, PAD_T + 3.5,
                            align=(Align.CENTER, Align.CENTER, Align.MIN)))   # THROUGH (exits below)
    return cuts

def _b2m(solid):
    import numpy as np, trimesh
    v, f = solid.tessellate(0.05)
    return trimesh.Trimesh(vertices=np.array([(p.X, p.Y, p.Z) for p in v]), faces=np.array(f))

def mesh():
    # OCC keeps internal partition faces on these coplanar box unions -> use manifold
    import trimesh
    body = trimesh.boolean.union([_b2m(s) for s in _additive()], engine="manifold")
    body = trimesh.boolean.difference([body] + [_b2m(s) for s in _cuts()], engine="manifold")
    return body

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    m = mesh()
    m.export("build/flexure_ground.stl")
    print("flexure_ground:", (m.bounds[1]-m.bounds[0]).round(1),
          "bodies:", len(m.split(only_watertight=False)), "watertight:", m.is_watertight)
