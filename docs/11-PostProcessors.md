# Post-Processors — GRBL vs Mach3 (Diff & Examples)

## Dialect Summary
- GRBL: IJ incremental arcs; laser mode via $32; status `?`, hold `!`, resume `~`.
- Mach3: IJK absolute arcs by default; G31 probing; macros/plugins for status.

## Preambles
**GRBL**
```gcode
G90 G21 G17
G94
G54
M3 S10000
```
**Mach3**
```gcode
G90 G21 G17
G94
G54
G40 G49 G80
M3 S10000
```

## Arc Emission
**GRBL (IJ)** `G2 X.. Y.. I.. J..`  
**Mach3 (IJK)** `G2 X.. Y.. I.. J.. K0.000`

## Code Skeletons
Python class stubs for `PostGRBL` and `PostMach3` are included in `onestop/post/`.
