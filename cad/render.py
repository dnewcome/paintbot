"""render.py — quick matplotlib PNG previews of STLs (no GPU needed)."""
import sys, numpy as np, trimesh
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def render(stl, png, elev=22, azim=-60, color="#b9c4d0", yup=False):
    m = trimesh.load(stl)
    V = m.vertices.copy()
    if yup:                       # map model Y(up) -> plot Z(up): (x,y,z)->(x,-z,y)
        V = np.column_stack((V[:, 0], -V[:, 2], V[:, 1]))
    tris = V[m.faces]
    fig = plt.figure(figsize=(7, 8))
    ax = fig.add_subplot(111, projection="3d")
    # recompute face normals from the (possibly transformed) triangles
    e1 = tris[:, 1] - tris[:, 0]; e2 = tris[:, 2] - tris[:, 0]
    n = np.cross(e1, e2); n = n/(np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
    light = np.array([0.3, 0.4, 0.85]); light = light/np.linalg.norm(light)
    shade = 0.45 + 0.55*np.clip(n @ light, 0, 1)
    base = np.array(matplotlib.colors.to_rgb(color))
    facecols = np.clip(shade[:, None]*base[None, :], 0, 1)
    pc = Poly3DCollection(tris, facecolors=facecols, edgecolors="none")
    ax.add_collection3d(pc)
    v = V
    ctr = v.mean(0); r = (v.max(0)-v.min(0)).max()/2
    for setlim, c in ((ax.set_xlim, ctr[0]), (ax.set_ylim, ctr[1]), (ax.set_zlim, ctr[2])):
        setlim(c-r, c+r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    fig.tight_layout(); fig.savefig(png, dpi=110, bbox_inches="tight"); plt.close(fig)
    print("wrote", png)

if __name__ == "__main__":
    render("build/assembly_corexy.stl", "build/assembly_corexy.png", elev=20, azim=102, yup=True)
    render("build/assembly_extruder.stl", "build/assembly_extruder.png", elev=14, azim=-70)
    render("build/assembly_brush.stl", "build/assembly_brush.png", elev=10, azim=-70)
