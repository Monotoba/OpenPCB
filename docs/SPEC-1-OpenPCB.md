# SPEC-1 - One-Stop PCB CAM & Sender (PySide6, Python 3.10+)

## Background

Hobbyists and small fabrication shops often juggle multiple tools to take a PCB from design files to a finished board: CAM for toolpath generation (e.g., FlatCAM), separate G-code senders (e.g., Candle/UGS), and machine-specific utilities for mills, lasers, drills, and plotters. This fragmentation increases setup time, risk of errors (unit mismatches, origins, tool diameters, controller dialects), and complicates running multiple machines in parallel.

This project proposes a single cross-platform desktop application built with Python 3.10+ and PySide6 (Qt for Python) that integrates:

- Multi-format import (Gerber/Excellon, G-code, SVG, PNG→SVG conversion) onto distinct, toggleable layers with a preview canvas.
- CAM operations to generate positive/negative isolation or raster toolpaths for: top/bottom copper traces, drills, solder mask, and silkscreen.
- A built-in, queue-aware, multi-port sender that can concurrently drive up to 4 machines (mills/routers, lasers: diode/fiber/CO₂, drills, and HPGL plotters/printers), with controller dialect mapping (M/S/G-codes, HPGL).
- Asset import for logos and imagery (vector and raster) with configurable preprocessing (thresholding, vectorization, scaling, registration to board origin).

Key drivers:
- Reduce toolchain friction and human error by unifying CAM + sender + job management.
- Ensure predictable, reproducible outputs across heterogeneous hobby-grade machines.
- Offer a pragmatic MVP that is production-ready yet extendable (plugin architecture, controller profiles, post-processors).

## Requirements

### Scope & Platforms
- **Platforms (must):** Windows 10+, macOS 12+, Ubuntu 22.04+ (desktop only; Android dropped).
- **Python/GUI (must):** Python 3.10+, PySide6/Qt 6.x.

### File I/O
- **Must:** Import RS-274X Gerber and Excellon drill; parse & render to vector layers.
- **Must:** Import SVG; **Should:** DXF (later).
- **Must:** Import G-code; syntax highlighting & preview.
- **Must:** Import PNG/JPEG and **auto-vectorize to SVG** (Potrace-equivalent) with thresholding.
- **Should:** Export SVG/HPGL for plotters; **Must:** Export G-code for mills/lasers/drills.

### Visualization & Editing
- **Must:** Layered preview (top/bottom copper, drills, outline, mask, silkscreen, images, guides). Toggle visibility/lock, per-layer color, opacity.
- **Must:** Pan/zoom, rulers, grid, units (mm/in), origin control (G54/G92), board outline definition.
- **Should:** Geometry ops (translate/rotate/scale/mirror), boolean ops for mask/silk prep.
- **Must:** **Panelization** (array, step-and-repeat, v-groove/route tabs, mouse bites, fiducials) incl. X/Y gaps between boards.

### CAM / Toolpath Generation
- **Must:** Generate top/bottom traces (isolation or raster), drills, outline cut, solder mask (positive/negative), silkscreen (vector hatch/raster engrave for lasers).
- **Must:** Per-operation strategies: isolation width (N passes), tool diameter, step-over, climb/conventional, lead-in/out, tabs (for outlines), depth/laser power.
- **Must:** Post-processors for controller dialects and HPGL. **Map** M/S/G codes appropriately per machine profile.
  - **Controllers (MVP must):** GRBL 1.1, Marlin (CNC), Smoothieware, LinuxCNC, **Mach3/4**, **FANUC** (subset for 2.5D engraving/drilling), **HPGL** plotters.
- **Should:** Path optimization: segment merge, nearest-neighbor sort, corner smoothing.

### Sending / Machine Control
- **Must:** Built-in sender with serial/USB-CDC and network (TCP) backends; send to up to **4** machines concurrently; per-port queues.
- **Must:** Real-time support equivalent to GRBL: status, feed hold, resume, soft reset, settings; comparable features for Marlin/Smoothie/Mach/LinuxCNC; HPGL streaming for plotters.
- **Must:** Safety: dry-run, bounding-box preview, door/limit alarm handling, soft limits, tool-change prompts.
- **Should:** Probing/auto-level (height map) for mills; jog UI; macros.

### Extensibility & Data
- **Must:** Plugin system for importers, CAM ops, and post-processors; JSON/YAML controller profiles.
- **Must:** Deterministic jobs: project file captures inputs, parameters, machine profile, seeds, and produces reproducible outputs.

### Performance & Limits
- **Must:** **Resolution:** internal geometry tolerance **0.01 mm**; **Minimum trace/clearance:** **0.10 mm**.
- **Must:** **Board size up to 1000×1000 mm**; each **machine profile defines its own work envelope** and soft limits.
- **Must:** GPU-accelerated rendering via Qt Scene Graph where available; handle 1M+ path segments.

### Non-functional
- **Must:** Deterministic geometry/kernel tests; cross-platform CI builds; crash-safe autosave; responsive on 1080p displays.
- **Could:** Scriptable CLI for headless batch CAM using the same engine.

## Method

### High-level Architecture

- **Frontend (PySide6/Qt 6)**: viewer, inspectors, job composer.
- **Core Engine (Python)**: geometry kernel (Shapely 2.x), svgpathtools, scikit-image, potrace/potracer; importers; CAM modules; panelization; post-processors; optimizers.
- **Sender & Device Layer**: asyncio + pyserial/TCP, up to 4 concurrent devices; real-time status parsers; ring buffers & flow control.
- **Persistence**: JSON project file; SQLite for job history & height maps; YAML/JSON for profiles.

#### Component Diagram (PlantUML)
```plantuml
@startuml
skinparam componentStyle rectangle
component "UI (PySide6)" as UI
component "Viewer (QtQuick)" as VIEW
component "Importers" as IMP
component "Geometry Kernel
(Shapely, svgpathtools)" as GEO
component "CAM Engine" as CAM
component "Post-Processor" as POST
component "Sender/IO" as IO
component "Profiles (YAML/JSON)" as PROF
component "Storage (SQLite/JSON)" as DB

UI --> VIEW
UI --> CAM
VIEW --> GEO
UI --> IMP
IMP --> GEO
CAM --> GEO
CAM --> POST
POST --> IO
UI --> IO
UI --> DB
CAM --> DB
IO --> DB
IO --> PROF
CAM --> PROF
IMP --> PROF
@enduml
```

### Data Model

**Project (.onestop.json)**
```json
{
  "schema": 1,
  "meta": {"name": "my-board", "created": "2026-01-22T00:00:00Z"},
  "units": "mm",
  "layers": [
    {"id": "top_copper", "source": "gerber", "path": "gerbers/top.gbr", "visible": true},
    {"id": "bottom_copper", "source": "gerber", "path": "gerbers/bot.gbr", "visible": false},
    {"id": "drill", "source": "excellon", "path": "gerbers/drill.xln"},
    {"id": "outline", "source": "gerber", "path": "gerbers/edge.gbr"},
    {"id": "silk_top", "source": "svg", "path": "assets/silk_top.svg"}
  ],
  "panel": {
    "mode": "grid",
    "rows": 3, "cols": 2,
    "gap": {"x": 2.0, "y": 2.0},
    "mouse_bites": {"diam": 0.8, "pitch": 1.6, "count": 6},
    "v_groove": false
  },
  "cam": {
    "resolution": 0.01,
    "min_trace": 0.10,
    "ops": [
      {"type": "isolation", "layer": "top_copper", "tool": "vbit_30_0.1",
       "passes": 2, "isolation": 0.2, "depth": -0.05, "clearance_height": 1.0},
      {"type": "drill", "layer": "drill", "tools": [{"diam": 0.8, "depth": -1.7}]},
      {"type": "outline", "layer": "outline", "tabs": [{"w":3,"h":1,"count":4}]}
    ],
    "autolevel": {"enabled": true, "method": "bilinear", "cap_mm": 0.3}
  },
  "machines": ["m_grbl_mill", "m_diode_laser"],
  "post": {"controller": "grbl_1_1", "units": "mm", "dialect_flags": {"laser_mode": true}},
  "jobs": [
    {"op": 0, "machine": "m_grbl_mill"},
    {"op": 1, "machine": "m_grbl_mill"},
    {"op": 2, "machine": "m_grbl_mill"}
  ]
}
```

**Machine Profile (YAML)**
```yaml
id: m_grbl_mill
name: Shop Mill
controller: grbl_1_1
work_envelope: { x: 300, y: 180, z: 50 }
units: mm
spindle: { min_rpm: 0, max_rpm: 12000 }
probe: { enabled: true, pin: zmin }
feed_limits: { xy: 1500, z: 300 }
laser: { enabled: false }
mapping:
  gcodes:
    absolute: G90
    incremental: G91
    units_mm: G21
    units_in: G20
    spindle_on: M3
    spindle_off: M5
    coolant_on: M8
    coolant_off: M9
  specials:
    status: "?"
    hold: "!"
    resume: "~"
```

**Controller Dialects (subset)**
```yaml
controllers:
  grbl_1_1: { arc: {cw: G2, ccw: G3, mode: ij}, s: S, m3: M3, m5: M5 }
  marlin_cnc: { arc: {cw: G2, ccw: G3, mode: ij}, s: S, m3: M3, m5: M5 }
  smoothie: { arc: {cw: G2, ccw: G3, mode: ij}, s: S }
  linuxcnc: { arc: {cw: G2, ccw: G3, mode: ijk}, g54: G54 }
  mach3: { arc: {cw: G2, ccw: G3, mode: ijk}, m7: M7 }
  mach4: { arc: {cw: G2, ccw: G3, mode: ijk} }
  fanuc_subset: { arc: {cw: G02, ccw: G03, mode: ijk}, prep: [G17, G40, G49, G80, G90] }
  hpgl: { pen_up: PU, pen_down: PD, select_pen: SP }
```

### Core Algorithms (highlights)
- Isolation routing, raster/hatch, drilling & peck cycles, outline & tabs, panelization with **X/Y gap**, **auto-leveling** (bilinear/IDW/RBF), toolpath optimization, dialect mapping, and sender concurrency (asyncio).

### Auto-Leveling (Deep Dive)
- Probing grid, SQLite schema for `heightmap` and `heightmap_points`, interpolation methods (bilinear/IDW/RBF), offline vs online warping with `dz_max` and `lmax`, transform-aware reuse of maps, safety caps, probing sequence PlantUML, pseudocode for online correction.

### Laser Raster/Vector Engraving
- Parameters (resolution/beam/stover/overscan), PWM mapping per controller, scanline generation (bidirectional with overscan), dithering, vector hatch/outline, safety notes.

### Mouse-Bite Generator
- Parameters, placement algorithm, DRC, strength heuristic, pseudocode, V-groove vs tabs, viewer UX.

### V-Groove Generator & Panel Rails/Fiducials
- V-bit parameters, kerf math, path extraction, toolpath emission, operation sequencing.
- Rails & fiducials: parameters, rail generation, placement, pseudocode, DRC, viewer UX.

## Implementation

### Tech Stack
Python 3.10+, PySide6, Shapely 2.x, svgpathtools, Pillow, scikit-image, potracer (MIT), pyserial, SQLite, PyInstaller.

### Module Layout
```
app/
  ui/ (Qt .ui or QML, widgets, models)
  viewer/ (Qt Quick scene, layer renderers)
  importers/ (gerber, excellon, svg, gcode, raster)
  cam/
    isolation.py
    raster.py
    drill.py
    outline.py
    panelize.py
    optimize.py
    autolevel.py
  post/
    grbl.py marlin.py smoothie.py linuxcnc.py mach3.py mach4.py fanuc.py hpgl.py
  sender/
    device.py parser_grbl.py parser_marlin.py ...
  models/
    project.py machine_profile.py job.py
  storage/
    db.py (sqlite), fs.py
  tests/
```

### Key Classes
`Project`, `Layer`, `Operation` (`IsolationOp`, `DrillOp`, `OutlineOp`, `RasterOp`, `MaskOp`, `SilkOp`), `PostProcessor`, `DeviceSession`.

### Testing & QA
Golden-output tests, virtual controller fuzzing, performance tests (1M segments at ≥45 FPS), probing repeatability checks.

## Milestones

1. **M0 — Skeleton & Viewer**: app shell, persistence, viewer, Gerber/SVG/PNG import (vectorize).
2. **M1 — CAM Core**: isolation, drill, outline, raster/hatch; optimizer; panelization grid with X/Y gaps.
3. **M2 — Post & Sender**: GRBL/Marlin/Smoothie/LinuxCNC posts; async sender (2 devices); probing & height map.
4. **M3 — Controllers Expansion**: Mach3/4, FANUC subset, HPGL; 4 concurrent devices; safety checks.
5. **M4 — UX/Perf & Packaging**: estimator, dry-run, crash recovery, CI builds (Win/macOS/Linux).
6. **M5 — Extended Panelization & Polish**: mouse bites, V-grooves, manual placement; presets.

## Gathering Results

- Functional acceptance, quality metrics (±0.02 mm isolation accuracy), performance, and stability metrics as defined earlier.

## Compliance Checklist (LGPL/Qt & Third-Party)
- Dynamic linking, relinking, notices, platform specifics (Windows/macOS/Linux), and distribution guidance.

## Qt Deployment Checklist
- PyInstaller spec skeleton, plugin sets, Windows code-sign, macOS rpath/notarization, Linux AppImage.

## Serial/USB Setup Guide
- Drivers (FTDI/CP210x/CH340), macOS/Linux permissions & udev, controller specifics, safety/preflight.

## Post-Processors — GRBL vs Mach3
- Dialect table, preambles, arc emission examples, post class sketches.

## CLI Smoke Test (Headless)
- Example commands and Python skeleton for isolation + autolevel pipelines.

## Risk Register (MVP)
- Top risks with mitigations (geometry robustness, licensing, dialect variance, DNC reliability, serial quirks, performance, probing noise, panelization collisions, laser mapping, large-envelope checks).

## Need Professional Help in Developing Your Architecture?
Please contact me at https://sammuti.com :)
