"""params_frame.py — shared dims for the planar-plate CoreXY frame (proto: laser-cut
acrylic/ply plates + MGN12 rails + 8020). Placeholders flagged — verify vs datasheets.
All mm. See docs/planar-corexy.md.
"""
# ---- Plate stock (cheap proto) ----
PLATE_T       = 6.0     # acrylic / plywood sheet (re-cut keepers in 1/4-3/8" Al later)
CORNER_R      = 4.0     # outline corner radius (laser-friendly)

# ---- MGN12 carriage block mounting (VERIFY vs MGN12H datasheet) ----
MGN12_HOLE_X  = 20.0    # transverse mounting-hole pitch
MGN12_HOLE_Y  = 25.0    # longitudinal pitch (H block)
MGN12_BOLT    = 3.4     # M3 clearance
MGN12_BLOCK_W = 27.0    # block width (footprint guide)
MGN12_BLOCK_L = 43.6    # H block length

# ---- 8020 interface (2040 profile, M5 T-nuts) ----
EXTR_W        = 20.0    # slot face pitch reference
M5_CLEAR      = 5.5

# ---- Belt (15 mm steel-core GT2/3) + clamps ----
BELT_W        = 15.0
CLAMP_BOLT    = 3.4     # M3 clearance for belt-clamp screws
CLAMP_PITCH   = 18.0    # two screws per belt-end clamp

# ---- Tool-head interface on the carriage (PLACEHOLDER pattern) ----
TOOL_BC_X     = 40.0    # 4x bolt rectangle to the coarse-Z stage
TOOL_BC_Y     = 40.0
TOOL_BOLT     = 5.5     # M5 clearance

# ---- X-carriage plate outline ----
XC_W          = 80.0    # plate width  (X, along gantry)
XC_H          = 70.0    # plate height (motion-plane vertical)

# ---- Gantry-end plate (MOVING; MGN12 Y-block + gantry beam + 2 gantry idlers) ----
GE_W          = 100.0   # plate width
GE_H          = 100.0   # plate height
GE_BEAM_BOLT  = 5.5     # M5 clearance, gantry 2040 beam end attach
GE_BEAM_PITCH = 20.0    # 2040 end: two bolts 20 mm apart
IDLER_BOLT    = 5.5     # M5 shoulder-screw clearance for gantry idlers
# Idler positions relative to plate center — FIRST-PASS placeholders; finalized when
# the single-plane routing is ported from the corexy.com reference.
GE_IDLER_1    = ( 25.0,  30.0)
GE_IDLER_2    = ( 25.0, -30.0)
# MGN12 Y-block sits toward the upright side (-X); beam attaches toward +X (inboard).
GE_YBLOCK_CX  = -28.0   # Y-block group center X offset
GE_BEAM_CX    =  35.0   # beam-attach group center X offset
