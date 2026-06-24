"""params_extruder.py — shared dimensions for the gel extrusion head.

Single source of truth for the motor-driven syringe head. All units mm.
Coordinate convention: primary (plunger) axis = Z, base at z=0, plunger pushes
-Z (down, toward canvas) — same convention as the brush head.

Reuses the ShopBot interface + fastener constants from the brush head's params so
both tool heads bolt to the same Z-plate mount.

Stack (low z -> high z): nozzle -> syringe barrel -> plunger carriage ->
leadscrew + guide rods -> motor top plate -> ShopBot interface plate.
"""

# Shared ShopBot interface + fasteners (single source lives in params.py)
from params import (
    IFACE_PLATE_X, IFACE_PLATE_Y, IFACE_PLATE_T,
    IFACE_BOLT_DX, IFACE_BOLT_DY, IFACE_BOLT_D,
    M3_CLEAR, M3_TAP, HEATSET_M3,
)

# ---- Syringe (10 cc Luer-lock; NOMINAL — confirm against the brand actually used) ----
SYR_BARREL_OD   = 16.5   # barrel outer Ø (cradle clamps this)
SYR_BARREL_ID   = 14.5   # plunger bore -> area 165 mm^2 (force/volume sizing)
SYR_BARREL_LEN  = 65.0   # graduated barrel length (nominal)
SYR_FLANGE_W    = 30.0   # finger flange width (oval long axis) — keyhole grabs this
SYR_FLANGE_THK  = 3.0    # finger flange thickness
SYR_PLUNGER_OD  = 14.5   # plunger rod thumb-rest disc Ø (carriage C-slot captures)
SYR_PLUNGER_THK = 3.0    # thumb-rest disc thickness
SYR_TIP_OD      = 8.0    # Luer tip OD region (nozzle screws/press here)
PLUNGER_TRAVEL  = 55.0   # usable plunger stroke

# ---- Nozzle (fat-bead gel) ----
NOZ_BORE        = 3.0    # exit bore (heavy gel, fat impasto bead)
NOZ_CONE_LEN    = 14.0   # taper length from Luer body to tip
NOZ_BASE_OD     = 12.0   # base where it mates the Luer tip

# ---- Drive train ----
SCREW_LEAD      = 8.0    # T8x8 (2 mm pitch x 4-start); 2.0 alt for high force/res
SCREW_OD        = 8.0    # T8 leadscrew
NUT_FLANGE_OD   = 22.0   # brass anti-backlash nut flange Ø
NUT_FLANGE_BC   = 16.0   # nut flange mount bolt circle (3x M3)
GUIDE_ROD_D     = 8.0    # Ø8 hardened guide rods
GUIDE_BEARING_OD= 15.0   # LM8UU outer Ø
GUIDE_BEARING_L = 24.0   # LM8UU length
GUIDE_SPACING   = 45.0   # center-to-center of the two guide rods (flank the screw)

# ---- NEMA17 motor mount ----
NEMA17_W        = 42.3   # body width
NEMA17_BOLT     = 31.0   # bolt square spacing
NEMA17_PILOT    = 22.0   # pilot boss Ø
NEMA17_BOLT_D   = 3.4    # M3 clearance for motor screws

# ---- Carriage / plate stock ----
CARRIAGE_T      = 12.0   # plunger carriage body thickness (houses nut + bearings)
PLATE_T         = 8.0    # printed structural plate thickness
BODY_W          = 68.0   # overall head width (spans rods + Ø15 LM8UU bearings + wall)
