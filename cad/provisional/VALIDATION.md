# Provisional CAD validation record

## Scope

This record covers geometry-kernel execution and exported-mesh integrity only. It is not a design verification, manufacturing approval, pressure test, CFD validation or physical experiment.

## Checks completed

| Check | Result |
|---|---|
| OpenSCAD command-line render to STL | Passed; CGAL reported a simple 3-D object |
| OpenSCAD STL watertightness | Passed |
| CadQuery script execution | Passed with CadQuery 2.8.0 |
| CadQuery STEP re-import | Passed |
| CadQuery STEP solid count | 1 |
| CadQuery STEP B-rep validity | Valid |
| CadQuery STL watertightness | Passed |
| Both STL bounding boxes | Identical: 300 × 210 × 50 mm |
| Both STL connected-component count | 1 watertight component each |

## Numerical comparison

- CadQuery STEP B-rep volume: 468,919.008 mm³.
- OpenSCAD STL mesh volume: approximately 469,114.142 mm³.
- CadQuery STL mesh volume: approximately 468,915.633 mm³.
- Difference between the two triangulated mesh volumes: approximately 0.042%.

The small mesh-volume difference is consistent with different tessellation choices. It does not establish exact B-rep equivalence. A later acceptance test should compare matched tessellation tolerances, face/edge topology, port centrelines and bore diameters.

## Interpretation

The two implementations produce one connected, watertight exported mesh with matching overall extents. This is sufficient to proceed to detailed CAD review, not to fabrication. The design still needs confirmed port specifications, material and manufacturing constraints, serviceability, internal flow design, headspace definition and an independently checked fluid-domain export.

No structural or hydrostatic pressure analysis has been performed. No leak test or biological/engineering experiment has been performed.
