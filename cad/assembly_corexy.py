"""assembly_corexy.py — planar-plate CoreXY frame, real plates placed (VISUALIZATION).
   python3 cad/assembly_corexy.py -> build/assembly_corexy.stl

Places the REAL flat-plate STLs at their routing positions (landscape 4x3 ft, motors
bottom corners) with MGN12 rails + 8020 frame as stand-in boxes, so the planar design
reads in 3D. Motion plane = z=0 (plates), rails behind, frame further behind.
Multi-body, not watertight — viewing only. Positions imported from routing.py.
"""
import os, numpy as np, trimesh
import routing as R

CX, CY = R.W/2, R.H/2          # center the frame at origin

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
    P.append(place(load("plate_motor_corner"), *R.M_A))                      # bottom-left motor
    P.append(place(load("plate_motor_corner"), *R.M_B, mirror_x=True))       # bottom-right motor
    P.append(place(load("plate_gantry_end"), R.M, R.Y_G))                    # left gantry end
    P.append(place(load("plate_gantry_end"), R.W - R.M, R.Y_G, mirror_x=True))  # right gantry end
    P.append(place(load("plate_xcarriage"), R.X_C, R.Y_G))                   # X carriage
    P.append(place(load("plate_crossover"), R.W/2, R.M + 25))                # crossover idlers
    # --- MGN12 rails (stand-in boxes), behind the plates ---
    RZ = -8
    for xr in (R.M, R.W - R.M):                                              # 2 vertical Y rails
        P.append(box(12, R.H - 2*R.M, 8, xr, R.H/2, RZ, [120, 140, 160, 255]))
    P.append(box(R.W - 2*R.M, 12, 8, R.W/2, R.Y_G, RZ, [120, 140, 160, 255]))   # gantry X rail
    # --- 8020 perimeter frame (stand-in), furthest back ---
    FZ = -28
    fc = [90, 90, 100, 255]
    P.append(box(R.W, 40, 40, R.W/2, R.M, FZ, fc))                           # bottom
    P.append(box(R.W, 40, 40, R.W/2, R.H - R.M, FZ, fc))                     # top (counterbalance beam)
    P.append(box(40, R.H, 40, R.M, R.H/2, FZ, fc))                          # left upright
    P.append(box(40, R.H, 40, R.W - R.M, R.H/2, FZ, fc))                    # right upright
    return trimesh.util.concatenate(P)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    m = assembly()
    m.export("build/assembly_corexy.stl")
    print("assembly_corexy bbox:", (m.bounds[1]-m.bounds[0]).round(0),
          "bodies:", len(m.split(only_watertight=False)))
