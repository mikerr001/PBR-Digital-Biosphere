# Development log

## Phase 3 provisional — internal fluid-domain geometry

- Added edge-referenced sparger and drain parameters to the provisional CadQuery and OpenSCAD models.
- Cut both bottom ports along the reactor vertical axis through the bottom wall.
- Added two positive internal baffle plates fused to the floor; retained the external envelope and existing boss/port geometry.
- Extended the validator to check STEP solid count and B-rep validity, external extents, analytic solid volume, mesh watertightness/connectivity, and cross-kernel STL volume agreement.
- Corrected analytic baseline accounting so existing bore cutter overrun in free space is not counted as removed material.
- Local CAD generation and validation passed with CadQuery 2.8.0, OpenSCAD 2021.01, and trimesh 4.11.1. See [INTERNAL_GEOMETRY.md](../cad/provisional/INTERNAL_GEOMETRY.md) for parameter values, volume accounting, results, commands, and limitations.
- Validation remains geometric only; no hydraulic, structural, biological, pressure, or life-support qualification is implied.
