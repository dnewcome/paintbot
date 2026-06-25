"""assembly_brush.py — full voice-coil brush head, real parts, true z-stack (VISUALIZATION).
   python3 cad/assembly_brush.py -> build/assembly_brush.stl (+ prints clearances)

Stacks the actual CAD parts in their assembled relationship to verify the z-stack:
cup opens DOWN, magnet+pole at the back, bobbin/coil ride the gap near the mouth,
carrier hangs below to the brush holder, flexure blades at the two heights, the
flexure_ground U-frame holds the blade ends, body_collar (HDZ 65 mm) caps the cup.
Multi-body, not watertight — for viewing + clearance sanity only.
"""
import os, numpy as np, trimesh
from build123d import *
import pole, steel_cup, bobbin, brush_holder, carrier, blade, flexure_ground, body_collar
from params import (COIL_OD, CUP_ID, BOBBIN_OD, MAGNET_DIA, MAGNET_H, CUP_OD,
                    SHELF_Z_LOW, BLADE_GAP)

def b2m(solid):
    v, f = solid.tessellate(0.06)
    return trimesh.Trimesh(vertices=np.array([(p.X, p.Y, p.Z) for p in v]), faces=np.array(f))

def gm(mod):
    return mod.mesh() if hasattr(mod, "mesh") else b2m(mod.part())

def place(m, tz, rx=0):
    m = m.copy()
    if rx:
        m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(rx), [1, 0, 0]))
    m.apply_translation([0, 0, tz])
    return m

def assembly():
    P = []
    P.append(place(gm(carrier), 0))                       # carrier z[0,42]
    P.append(place(gm(brush_holder), -18))                # holder z[-18,0]
    P.append(place(gm(bobbin), 42))                       # bobbin z[42,72]
    P.append(place(gm(steel_cup), 95, rx=180))            # cup floor@95, mouth@49
    P.append(place(gm(pole), 79, rx=180))                 # pole tip@51, top@79
    P.append(place(gm(body_collar), 55))                  # collar z[55,105]
    P.append(place(gm(flexure_ground), 0))                # pads@6/36, bridge@46-56
    P.append(place(gm(blade), SHELF_Z_LOW))               # lower blade
    P.append(place(gm(blade), SHELF_Z_LOW + BLADE_GAP))   # upper blade
    # coil winding (annulus stand-in) and magnet disc
    coil = trimesh.creation.annulus(r_min=BOBBIN_OD/2, r_max=COIL_OD/2, height=16)
    P.append(place(coil, 64))                             # coil centered z=64 ([56,72])
    P.append(place(trimesh.creation.cylinder(radius=MAGNET_DIA/2, height=MAGNET_H), 84))
    return trimesh.util.concatenate(P)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    m = assembly()
    m.export("build/assembly_brush.stl")
    bb = (m.bounds[1] - m.bounds[0]).round(1)
    print("assembly_brush bbox:", bb, "bodies:", len(m.split(only_watertight=False)))
    print("clearances (design):")
    print(f"  coil OD {COIL_OD} in cup bore {CUP_ID}: {(CUP_ID-COIL_OD)/2:.2f} mm/side radial gap")
    print(f"  bobbin foot Ø32 (z~42) vs cup mouth (z=49): foot ~7 mm BELOW mouth (clears)")
    print(f"  pole tip z=51 vs coil bottom z=56 at neutral: 5 mm (coil stays in gap over ±5)")
    print(f"  flexure pads at z={SHELF_Z_LOW} and z={SHELF_Z_LOW+BLADE_GAP} match blades")
