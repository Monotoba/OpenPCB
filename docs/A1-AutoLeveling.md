# Auto-Leveling — Deep Dive

- Probing grid (G38.2), margins, clearance, probe/retract feeds.
- SQLite: `heightmap` and `heightmap_points` tables.
- Interpolation: bilinear (MVP), IDW, RBF; Z correction caps.
- Warping: offline pre-warp vs online sender-time; `dz_max`, `lmax`; arc chord flattening.
- Transforms: reuse maps via affine; handle rotations/mirrors.
- Safety: repeatability checks, out-of-bounds behavior, hard caps, alarm handling.
- UI: heatmap overlay; planner panel; test-card macro.

Sequence & pseudocode are in SPEC and comments within `cam/autolevel.py` stub.
