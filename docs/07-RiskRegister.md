# Risk Register (MVP)

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---:|---:|---|
| R1 | Geometry robustness at 0.01 mm | Med | High | Shapely 2.x robust ops; snap-round; validation tests. |
| R2 | License contamination (GPL) | Med | High | Prefer MIT/BSD/Apache; avoid GPL libs; comply with LGPL for Qt. |
| R3 | Controller dialect variance | Med | High | Strict post-processors; long-hand canned cycles; conformance tests. |
| R4 | DNC/RS-232 reliability (FANUC) | Low | Med | Resumable drip-feed; flow control; retries. |
| R5 | USB serial quirks | Med | Med | Driver guidance, udev rules, notarization entitlements. |
| R6 | Performance on 1M segments | Med | Med | Qt Quick VBO batching; simplification; tiling; threading. |
| R7 | Auto-level noise | Low | Med | Median filtering; repeatability check; Z caps. |
| R8 | Panelization collisions | Low | Med | Clearance solver; DRC warnings. |
| R9 | Laser power mapping | Med | Med | Normalized power; controller S-range mapping; calibration. |
| R10 | Large envelope vs machine limits | Low | High | Preflight envelope check; tiled machining (later). |
