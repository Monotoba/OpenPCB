# CLI Smoke Test

## Examples
```bash
onestop-pcb cam \
  --project tests/project_min.json \
  --op isolation:top_copper \
  --post grbl_1_1 \
  --out out/top_iso_grbl.nc

onestop-pcb cam \
  --project tests/project_min.json \
  --op isolation:top_copper \
  --autolevel tests/heightmap_demo.json \
  --dz-max 0.02 --lmax 2.0 \
  --post mach3 \
  --out out/top_iso_mach3_autolevel.nc
```
