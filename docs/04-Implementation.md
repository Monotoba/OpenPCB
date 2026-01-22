# Implementation

## Tech Stack
Python 3.10+, PySide6, Shapely 2.x, svgpathtools, Pillow, scikit-image, potracer (MIT), pyserial, SQLite, PyInstaller.

## Module Layout
```
app/
  ui/
  viewer/
  importers/
  cam/
  post/
  sender/
  models/
  storage/
  tests/
```

## Key Classes
`Project`, `Layer`, `Operation` (`IsolationOp`, `DrillOp`, `OutlineOp`, `RasterOp`, `MaskOp`, `SilkOp`), `PostProcessor`, `DeviceSession`.

## Testing & QA
Golden-output tests, virtual controller fuzzing, perf tests (1M segments ≥45 FPS), probing repeatability checks.
