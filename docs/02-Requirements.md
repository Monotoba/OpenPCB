# Requirements (MoSCoW)

## Scope & Platforms
- Platforms: Windows 10+, macOS 12+, Ubuntu 22.04+ (desktop).
- Python/GUI: Python 3.10+, PySide6/Qt 6.x.

## File I/O
- Import RS-274X Gerber, Excellon, SVG, G-code, PNG/JPEG→SVG.
- Export G-code; SVG/HPGL for plotters (should).

## Visualization & Editing
- Layered preview with visibility/lock/color/opacity, pan/zoom/rulers/grid, units, origin control, board outline.
- Geometry ops (translate/rotate/scale/mirror), boolean ops (should).
- Panelization (array, X/Y gaps, v-groove, tabs/mouse-bites, fiducials).

## CAM / Toolpath Generation
- Top/bottom traces (isolation/raster), drills, outline, solder mask (pos/neg), silkscreen (vector/raster).
- Per-op strategies (passes, isolation width, step-over, tabs, depth/power).
- Post-processors with dialect mapping (GRBL, Marlin, Smoothie, LinuxCNC, Mach3/4, FANUC subset 2.5D, HPGL).
- Optimization (merge, nearest-neighbor, smoothing).

## Sending / Machine Control
- Built-in sender; up to 4 machines; serial/TCP.
- Real-time controls, safety features, probing/auto-level (should).

## Extensibility & Data
- Plugin system; JSON/YAML profiles; deterministic jobs.

## Performance & Limits
- Resolution 0.01 mm; min trace/clearance 0.10 mm.
- Board up to 1000×1000 mm; per-machine envelope.
- GPU rendering; 1M+ segments.

## Non-functional
- Deterministic tests; cross-platform CI; autosave; 1080p responsiveness.
