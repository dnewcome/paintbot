"""assembly_corexy.py — FULL raked CoreXY easel, real plates + real brush head (VIZ).
   python3 cad/assembly_corexy.py -> build/assembly_corexy.stl

Folds the old machine.py massing into the real planar build: the actual flat-plate
STLs at their routing positions (landscape 4x3 ft, motors bottom corners), the real
voice-coil brush head on the X-carriage reaching toward the canvas, MGN12 rails +
8020 frame + NEMA23 motors as stand-ins, the canvas slab, and the whole easel raked
back. Motion plane = z=0; canvas in front (+z); structure behind (-z).
Multi-body, not watertight — viewing only. Positions imported from routing.py.
"""
import os, numpy as np, trimesh
import routing as R

CX, CY   = R.W/2, R.H/2          # center the frame at origin
RAKE_DEG = 15.0
ROT180X  = np.diag([1.0, -1.0, -1.0, 1.0])   # 180° about X

def load(name):
    return trimesh.load(f"build/{name}.stl")

def place(m, x, y, z=0.0, mirror_x=False):
    m = m.copy()
    if mirror_x:
        m.apply_transform(np.diag([-1.0, 1.0, 1.0, 1.0]))
    m.apply_translation([x - CX, y - CY, z])
    return m

def box(w, h, d, x, y, z, col=None):
    b = trimesh.creation.box((w, h, d))
    b.apply_translation([x - CX, y - CY, z])
    if col is not None:
        b.visual.face_colors = col
    return b

def assembly():
    P = []
    # --- real flat plates, in the motion plane (z=0) ---
    P.append(place(load("plate_motor_corner"), *R.M_A))
    P.append(place(load("plate_motor_corner"), *R.M_B, mirror_x=True))
    P.append(place(load("plate_gantry_end"), R.M, R.Y_G))
    P.append(place(load("plate_gantry_end"), R.W - R.M, R.Y_G, mirror_x=True))
    P.append(place(load("plate_xcarriage"), R.X_C, R.Y_G))
    P.append(place(load("plate_crossover"), R.W/2, R.M + 25))

    # --- real brush head on the carriage, brush reaching toward the canvas (+z) ---
    head = load("assembly_brush")
    head.apply_transform(ROT180X)                 # tool axis -> +z (brush forward)
    head.apply_translation([R.X_C - CX, R.Y_G - CY, 105])   # collar at carriage, brush at +z
    P.append(head)
    HEAD_REACH = 128.0                            # ~ brush tip z

    # --- MGN12 rails (stand-ins), behind the plates ---
    RZ = -8
    rc = [120, 140, 160, 255]
    for xr in (R.M, R.W - R.M):
        P.append(box(12, R.H - 2*R.M, 8, xr, R.H/2, RZ, rc))
    P.append(box(R.W - 2*R.M, 12, 8, R.W/2, R.Y_G, RZ, rc))

    # --- NEMA23 motors (stand-ins) at the bottom corners, behind ---
    mc = [40, 40, 48, 255]
    for mx, my in (R.M_A, R.M_B):
        P.append(box(57, 57, 76, mx, my, -52, mc))

    # --- 8020 perimeter frame (stand-in), furthest back ---
    FZ = -30
    fc = [90, 90, 100, 255]
    P.append(box(R.W, 40, 40, R.W/2, R.M, FZ, fc))            # bottom
    P.append(box(R.W, 40, 40, R.W/2, R.H - R.M, FZ, fc))      # top (counterbalance beam)
    P.append(box(40, R.H, 40, R.M, R.H/2, FZ, fc))           # left upright
    P.append(box(40, R.H, 40, R.W - R.M, R.H/2, FZ, fc))     # right upright

    # --- canvas slab, just in front of the brush tip ---
    P.append(box(1219, 914, 6, R.W/2, R.H/2, HEAD_REACH + 4, [200, 195, 185, 255]))

    asm = trimesh.util.concatenate(P)
    # rake the whole easel back about the bottom frame edge (X axis at y=-CY, z=0)
    asm.apply_transform(trimesh.transformations.rotation_matrix(
        np.radians(-RAKE_DEG), [1, 0, 0], point=[0, -CY, 0]))
    return asm

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    m = assembly()
    m.export("build/assembly_corexy.stl")
    print("assembly_corexy bbox:", (m.bounds[1]-m.bounds[0]).round(0),
          "bodies:", len(m.split(only_watertight=False)))
