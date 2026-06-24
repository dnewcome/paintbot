"""routing.py — single-plane CoreXY belt-routing layout (landscape, motors at bottom).
   python3 cad/routing.py -> build/routing.svg  (+ prints pulley coordinates)

Topology (motors at the two BOTTOM corners; gantry moves in Y; carriage in X):
  Belt A (left motor):  M_A -> bottom edge -> BR -> up right upright -> GR_a
                        -> along gantry -> carriage -> GL_a -> down left -> M_A
  Belt B (right motor): M_B -> bottom edge -> BL -> up left upright  -> GL_b
                        -> along gantry -> carriage -> GR_b -> down right -> M_B
The two bottom strands cross near center-bottom -> 2 crossover idlers stagger them.
Top edge carries NO belt (free for the counterbalance springs).
8 idlers total: BL, BR (bottom corners) + GL_a/GL_b/GR_a/GR_b (gantry ends) + 2 crossover.
Kinematics: X = (a+b)/2, Y = (a-b)/2  (a,b = motor A,B belt displacements).
"""
import os

# --- motion-plane layout (mm); inner pulley field, representative gantry/carriage ---
W, H   = 1300.0, 1050.0      # inner field (work area 1219x914 + clearance)
M      = 40.0                # corner inset
Y_G    = 525.0               # gantry height (mid, for the diagram)
X_C    = 650.0               # carriage X (center, for the diagram)
DZ     = 8.0                 # single-plane stagger between the two strands at a shared post

M_A = (M, M);            M_B = (W-M, M)                 # drive pulleys (bottom corners)
BL  = (M, M+50);         BR  = (W-M, M+50)              # bottom-corner idlers (turn bottom->upright)
GL_a = (M, Y_G+DZ);      GL_b = (M, Y_G-DZ)             # left gantry-end idlers
GR_a = (W-M, Y_G+DZ);    GR_b = (W-M, Y_G-DZ)           # right gantry-end idlers
C_A = (X_C-20, Y_G);     C_B = (X_C+20, Y_G)            # carriage belt clamps
CX1 = (W/2-15, M+25);    CX2 = (W/2+15, M+10)           # crossover idlers (stagger strands)

BELT_A = [M_A, BR, GR_a, C_A, GL_a, M_A]
BELT_B = [M_B, BL, GL_b, C_B, GR_b, M_B]

PULLEYS = {"M_A": M_A, "M_B": M_B, "BL": BL, "BR": BR, "GL_a": GL_a, "GL_b": GL_b,
           "GR_a": GR_a, "GR_b": GR_b, "CX1": CX1, "CX2": CX2}

def svg():
    s = 0.5; pad = 40                       # px per mm, margin
    Wp, Hp = W*s + 2*pad, H*s + 2*pad
    def p(pt): return (pt[0]*s + pad, (H-pt[1])*s + pad)   # flip Y for SVG
    def poly(pts, col, w):
        d = " ".join(f"{'M' if i==0 else 'L'}{p(q)[0]:.1f},{p(q)[1]:.1f}" for i,q in enumerate(pts))
        return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}"/>'
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wp:.0f}" height="{Hp:.0f}" '
           f'viewBox="0 0 {Wp:.0f} {Hp:.0f}" font-family="sans-serif" font-size="11">']
    # frame
    x0,y0 = p((0,H)); out.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{W*s:.1f}" '
                                 f'height="{H*s:.1f}" fill="#fafafa" stroke="#bbb"/>')
    # uprights (Y rails) + gantry (X rail)
    for xr in (M, W-M):
        a,b = p((xr,M)), p((xr,H-M)); out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" '
            f'x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#cdd" stroke-width="6"/>')
    a,b = p((M,Y_G)), p((W-M,Y_G)); out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" '
        f'x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#cdd" stroke-width="6"/>')
    # belts
    out.append(poly(BELT_A, "#1565c0", 2)); out.append(poly(BELT_B, "#c62828", 2))
    # carriage
    cx,cy = p((X_C,Y_G)); out.append(f'<rect x="{cx-14:.1f}" y="{cy-10:.1f}" width="28" '
        f'height="20" fill="#fff3" stroke="#333"/><text x="{cx-12:.1f}" y="{cy+24:.1f}">carriage</text>')
    # pulleys
    for name,pt in PULLEYS.items():
        q = p(pt); motor = name.startswith("M_")
        out.append(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="{7 if motor else 4}" '
                   f'fill="{"#333" if motor else "#888"}"/>'
                   f'<text x="{q[0]+6:.1f}" y="{q[1]-6:.1f}">{name}</text>')
    out.append(f'<text x="{pad}" y="{Hp-12:.0f}" fill="#666">single-plane CoreXY, motors '
               f'bottom, top edge free for counterbalance — verify strands vs a reference build</text>')
    out.append("</svg>")
    return "\n".join(out)

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    with open("build/routing.svg", "w") as f:
        f.write(svg())
    print("routing.svg written. Pulley coords (mm):")
    for k,v in PULLEYS.items():
        print(f"  {k:5s} ({v[0]:7.1f}, {v[1]:6.1f})")
