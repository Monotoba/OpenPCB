# Backlog — One-Stop PCB CAM & Sender

## Epics
- E-01 Viewer & Persistence
- E-02 Importers & Vectorization
- E-03 CAM Core (Isolation/Drill/Outline/Raster)
- E-04 Panelization (Grid + X/Y gaps, Tabs, Mouse-bites, V-grooves)
- E-05 Post-Processors & Dialects
- E-06 Sender & Device Concurrency
- E-07 Auto-Leveling
- E-08 Packaging & Deployment
- E-09 UX/Perf & QA
- E-10 Documentation & Samples

## Stories

### E-01 Viewer & Persistence
- S-0101 Project model (.onestop.json) load/save
- S-0102 Qt Quick viewer with pan/zoom/rulers/grid
- S-0103 Layer manager (color/opacity/visibility/lock)
- S-0104 Origin control (G54/G92), units toggle

### E-02 Importers & Vectorization
- S-0201 Gerber RS-274X importer (gerbonara)
- S-0202 Excellon drill importer
- S-0203 SVG importer
- S-0204 G-code importer
- S-0205 PNG/JPEG importer + potracer vectorization with threshold UI

### E-03 CAM Core
- S-0301 Isolation routing (N-pass)
- S-0302 Drill grouping + peck emulation
- S-0303 Board outline with tabs
- S-0304 Raster/hatch for silk/mask
- S-0305 Path optimizer (merge, nearest-neighbor, 2-opt)

### E-04 Panelization
- S-0401 Grid step-and-repeat with X/Y gaps
- S-0402 Manual placement & transforms
- S-0403 Mouse-bite generator + DRC
- S-0404 V-groove generator
- S-0405 Rails & fiducials generator

### E-05 Post-Processors
- S-0501 GRBL 1.1
- S-0502 Marlin CNC
- S-0503 Smoothieware
- S-0504 LinuxCNC
- S-0505 Mach3
- S-0506 Mach4
- S-0507 FANUC subset
- S-0508 HPGL plotter

### E-06 Sender
- S-0601 Async DeviceSession (serial/TCP)
- S-0602 GRBL status/flow (ok, ?, !, ~)
- S-0603 Concurrency up to 4 devices
- S-0604 Error recovery & alarms
- S-0605 Height-map streaming hooks

### E-07 Auto-Leveling
- S-0701 Probe planner; G38.2 sequences
- S-0702 SQLite schema & persistence
- S-0703 Bilinear interpolation
- S-0704 Online (sender-time) warping
- S-0705 Offline pre-warp export
- S-0706 Heatmap visualization & QA

### E-08 Packaging & Deployment
- S-0801 PyInstaller spec (Win/macOS/Linux)
- S-0802 macOS signing & notarization
- S-0803 Linux AppImage packaging
- S-0804 Windows installer & code signing

### E-09 UX/Perf & QA
- S-0901 Time estimator & simulation/dry-run
- S-0902 Golden-output tests suite
- S-0903 Virtual controllers for fuzz testing
- S-0904 Performance profiling & GPU fallback

### E-10 Documentation & Samples
- S-1001 User guide & quickstart
- S-1002 Third-party notices & licensing
- S-1003 Sample assets (Gerber/SVG/G-code, height maps)
