"""params.py — shared dimensions for the voice-coil brush head.

Single source of truth so mating parts stay in sync. Import these into each part:
    from params import *
All units mm. Coordinate convention: primary (stroke) axis = Z, base at z=0,
brush points -Z (down, ShopBot prototype orientation).

Stack (low z -> high z): brush -> brush_holder -> carrier -> (coil in gap) ->
stator cup (lathe steel) -> main_body (printed, holds cup + flexure ground +
ShopBot interface plate on top).
"""

# ---- Magnetic circuit (LATHE STEEL + bought magnet; printed parts reference these) ----
POLE_DIA      = 16.0   # center pole OD (1018 steel, turned)
POLE_H        = 28.0   # >= coil length (16) + stroke (10): keeps coil in gap over travel
MAGNET_DIA    = 16.0   # NdFeB N52 disc, axially magnetized
MAGNET_H      = 10.0
CUP_ID        = 22.5   # stator cup inner bore (gap = (CUP_ID-POLE_DIA)/2 = 3.25 mm)
CUP_OD        = 32.0   # cup outer (wall carries return flux)
CUP_WALL_H    = 40.0   # internal depth = magnet(10)+pole(28)+margin; houses coil travel
CUP_FLOOR     = 6.0    # cup base thickness (back-iron)
GAP_RADIAL    = (CUP_ID - POLE_DIA) / 2.0   # 3.25 mm radial magnetic gap

# ---- Coil / bobbin (printed former, hand-wound) ----
POLE_CLEAR    = 0.75   # radial clearance pole OD -> bobbin bore
BOBBIN_WALL   = 0.8    # bobbin tube wall
WIND_THK      = 1.0    # radial winding build (≈2 layers AWG26)
BOBBIN_ID     = POLE_DIA + 2*POLE_CLEAR          # 17.5
BOBBIN_OD     = BOBBIN_ID + 2*BOBBIN_WALL        # 19.1 (winding surface)
COIL_OD       = BOBBIN_OD + 2*WIND_THK           # 21.1
BOBBIN_LEN    = 16.0   # bobbin tube length (winding window <= this)
FLANGE_THK    = 1.2    # bobbin end flanges that retain the winding
FLANGE_OD     = COIL_OD + 3.0                     # flange just proud of winding

# ---- Stroke / flexure ----
# Symmetric single parallelogram: 2 blades (upper+lower), each fixed at BOTH ground
# ends and guided at the carrier center => 4 guided-cantilever segments in parallel.
#   k_flex = 4*E*w*t^3 / a^3   (E_steel = 200 GPa = 2e5 N/mm^2)
#   stress at deflection d:  sigma = 3*E*t*d / a^2
# t=0.1, w=20, a=34  ->  k ~ 0.41 N/mm ;  sigma(5mm) ~ 260 MPa (infinite life).
# Parasitic lateral shift ~ d^2*(3/5a) ~ 0.33 mm @ 5 mm — negligible for a brush
# (single parallelogram; compound stage cancels this, deferred as upgrade).
STROKE        = 10.0   # full fine-Z travel (+/-5 mm from neutral)
BLADE_THK     = 0.1    # spring-steel shim thickness (bought; ~0.004")
BLADE_W       = 20.0   # blade width
BLADE_FREE    = 34.0   # free half-length a (ground clamp <-> carrier clamp)
BLADE_CC      = 26.0   # central clamp length (carrier shelf grip, X)
BLADE_GC      = 14.0   # ground clamp grip length each end (X)
BLADE_LEN     = BLADE_CC + 2*BLADE_FREE + 2*BLADE_GC   # 122 total
BLADE_GAP     = 30.0   # vertical spacing upper<->lower blade
K_FLEX        = 0.41   # N/mm (computed; calibrate empirically)
CLAMP_W       = BLADE_W + 8.0
CLAMP_PLATE_T = 4.0    # printed clamp plate thickness
CLAMP_BOLT_DY = 12.0   # 2 clamp bolts straddle the blade, spaced in Y

# ---- Moving carrier (printed; links coil bobbin top -> brush holder bottom) ----
CARRIER_OD    = 32.0   # attach-flange OD (matches bobbin foot / brush holder flange)
CARRIER_ID    = 16.0   # hollow to save moving mass
ATTACH_BC     = 26.0   # shared 3xM3 bolt circle; clears the Ø18 pole-clearance bore
SHELF_Z_LOW   = 6.0    # lower blade clamp shelf top face height
SHELF_TH      = 4.0
SHELF_X       = BLADE_CC  # shelf grip length in X (= central clamp)

# ---- Brush holder (8 mm round-brush ferrule) ----
FERRULE_DIA   = 8.0
FERRULE_CLEAR = 0.3    # slip fit before clamp pinches
BORE_DIA      = FERRULE_DIA + FERRULE_CLEAR       # 8.3
HOLDER_OD     = 18.0
HOLDER_LEN    = 18.0
SLOT_W        = 1.6    # pinch slot for the clamp screw to close

# ---- Main body (printed: cup pocket + flexure ground + interface) ----
BODY_OD       = 40.0
BODY_WALL     = 3.0

# ---- ShopBot Z-plate interface (PLACEHOLDER — set to real bolt pattern) ----
# TODO(operator): replace with the actual ShopBot Z-plate hole pattern.
IFACE_PLATE_X = 70.0
IFACE_PLATE_Y = 70.0
IFACE_PLATE_T = 8.0
IFACE_BOLT_DX = 50.0   # placeholder bolt spacing X
IFACE_BOLT_DY = 50.0   # placeholder bolt spacing Y
IFACE_BOLT_D  = 6.6    # M6 clearance (placeholder)

# ---- Fastener clearances ----
M3_CLEAR      = 3.4
M3_TAP        = 2.5
HEATSET_M3    = 4.0    # through-bore for M3 heat-set insert
