# Provisional internal geometry — flat-panel reactor

**Status:** CAD-kernel geometry and export checks passed in the local validation environment. This is a provisional geometric model, not a fabrication release.

## Coordinate system and datums

All dimensions are millimetres. The external envelope is centred at the origin: X = 300, Y = 200, Z = 40. X is panel length, Y is vertical height, and Z is panel depth. The external bottom face is Y = -100; the internal floor is Y = -97. The external front edge is Z = -20.

The sparger and drain X coordinates are measured from the left external edge. Their `*_Y` parameters are measured from the front external edge (depth datum), and therefore map to centred Z coordinates. Both supplied depth offsets are 20 mm, placing the ports on the depth centreline (Z = 0); they are not offset toward the front face.

## Internal feature register

| Parameter | Value | Geometric interpretation |
|---|---:|---|
| `SPARGER_DIAMETER` | 8 mm | Sparger through-bore diameter |
| `SPARGER_X` | 150 mm | 150 mm from left edge; centred X = 0 |
| `SPARGER_Y` | 20 mm | 20 mm from front edge; centred Z = 0 |
| `DRAIN_DIAMETER` | 10 mm | Drain through-bore diameter |
| `DRAIN_X` | 30 mm | 30 mm from left edge; centred X = -120 |
| `DRAIN_Y` | 20 mm | 20 mm from front edge; centred Z = 0 |
| `BAFFLE_COUNT` | 2 | Two internal plates |
| `BAFFLE_HEIGHT` | 25 mm | Height above internal floor |
| `BAFFLE_THICKNESS` | 2 mm | Plate thickness along X |

### Port construction

Both ports are cylinders along +Y through the bottom wall. Each cutter starts 1 mm below the external bottom face and ends 1 mm into the internal cavity; only the 3 mm bottom wall contributes to removed solid volume. The sparger is centred at (X, Z) = (0, 0); the drain is centred at (-120, 0).

### Baffle construction

Baffles are positive solid plates fused to the internal floor, not subtracted cuts. Their X centre positions are -49 mm and +49 mm, derived by evenly spacing two plates within the 294 mm internal length. Each plate spans the 34 mm internal depth, extends from Y = -97 mm to Y = -72 mm, and is 2 mm thick along X.

## Analytic volume accounting

The baseline includes the shell, six external bosses, and the six existing sensor/gas bores. Existing bores remove material only across the boss and wall thickness; the extra cutter overrun lies in free space and is not subtracted from the solid-volume estimate.

| Quantity | Volume |
|---|---:|
| Baseline solid | 468,919.008 mm³ |
| Sparger + drain material removed | 386.416 mm³ |
| Two baffles added | 3,400.000 mm³ |
| Net change | +3,013.584 mm³ |
| Expected final solid | 471,932.592 mm³ |

The positive net change is intentional: the baffle material added exceeds the material removed by the two ports.

## Validation record

Executed using CadQuery 2.8.0, OpenSCAD 2021.01, and trimesh 4.11.1.

- STEP: exactly one solid; B-rep valid.
- STEP envelope: 300 × 210 × 50 mm.
- STEP solid volume: 471,932.592 mm³; analytic discrepancy 0.0000%.
- CadQuery STL: watertight, one connected component; volume 471,929.377 mm³.
- OpenSCAD STL: watertight, one connected component; volume 472,128.004 mm³.
- Relative STL volume difference: 0.0421%, below the 0.1% acceptance limit.
- Overall CAD export validation: **PASS**.

The mesh-volume difference is expected to include tessellation approximation. STEP B-rep volume is the analytic geometry comparison.

## Reproduction commands

Run from the repository root:

```bash
python cad/provisional/flat_panel_reactor.py
openscad -o cad/provisional/exports/flat_panel.stl cad/provisional/flat_panel_reactor.scad
python cad/provisional/validate_exports.py
```

The Python generator also writes the STEP and CadQuery STL files to `cad/provisional/exports/`. The validator accepts explicit paths for CI.

## Scope limits and unresolved engineering work

This geometry establishes placement and basic solid connectivity only. It does not establish hydraulic performance, flow distribution, bubble size, residence time, mixing, pressure rating, structural adequacy, fatigue life, sealing, corrosion compatibility, manufacturability, cleaning access, or biological performance. No pump, tubing, valves, diffuser internals, instrumentation insertion lengths, optical windows, headspace boundary, or full fluid-domain boundary conditions are represented. These must be specified and separately analysed before fabrication or any operational claim.

This CAD result is not biological validation, pressure-vessel certification, a life-support design, or approval for human occupancy.
