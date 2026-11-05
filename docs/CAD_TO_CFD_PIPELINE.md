# CAD → mesh → CFD hand-off

This is the explicit geometry hand-off contract for the PBR workbench. ToubkalCAD
remains the parametric source of truth. The CFD pipeline consumes an exported
STEP fluid-domain solid plus a boundary manifest; it never edits the CAD model.

## Inputs

1. Export the *fluid volume*, not the vessel wall solid, as STEP in metres.
2. Create a JSON manifest with one named planar selector per boundary.
3. Run the optional Gmsh CAD mesher:
   `python scripts/generate_cad_mesh.py --step fluid-domain.step --manifest pbr-boundaries.json --output fluid.msh --mesh-size-m 0.01`
4. Convert the Gmsh 2.2 mesh with OpenFOAM's `gmshToFoam fluid.msh`.
5. Inspect patch names and run `checkMesh`; do not proceed if any boundary
   is missing, duplicated, disconnected or geometrically invalid.

Example manifest (replace coordinates and names with the actual exported CAD):

```json
{
  "fluid_region": "culture_fluid",
  "surface_groups": [
    {"name": "inlet", "plane": {"axis": "x", "coordinate_m": 0.0}},
    {"name": "outlet", "plane": {"axis": "x", "coordinate_m": 1.0}},
    {"name": "walls", "plane": {"axis": "z", "coordinate_m": 0.0}},
    {"name": "top", "plane": {"axis": "z", "coordinate_m": 0.2}}
  ]
}
```

The current script deliberately supports planar bounding-box selectors only.
It rejects unmatched, overlapping and unassigned surfaces rather than guessing.
Curved walls and multiple fluid regions require explicit CAD face labels or a
future selector extension. Do not use a bounding-box selector where distinct
faces share the same plane.

## OpenFOAM conversion and checks

```bash
gmshToFoam fluid.msh
checkMesh -allTopology -allGeometry
```

Record OpenFOAM version, Gmsh version, STEP SHA-256, manifest SHA-256, mesh
SHA-256, cell count, patch list, non-orthogonality, skewness and failed quality
checks in the run record. Mesh generation is not mesh validation.

## Current coupling boundary

The existing PBR-08 biological model is 1-D and uses a provisional PAR proxy.
This pipeline creates a 3-D geometry/mesh hand-off only; it does not claim
3-D biology or multiphase gas transfer. The next coupling implementation must
map CFD cell volumes to reaction source terms with explicit units and verify
that integrated source/sink totals match the biological inventory change.
Bubble-resolved gas-liquid transfer must wait for a defined bubble model and
measured gas holdup / bubble-size data.

## Validation gates

- Confirm the fluid volume is watertight and correctly oriented in CAD.
- Verify named patches against the CAD drawing and mesh surface areas.
- Run mesh quality checks and at least three systematic mesh resolutions.
- Validate single-phase laminar pressure drop and velocity profile against
  analytical solutions before adding reactive scalar transport.
- Perform time-step refinement and global mass/energy conservation checks.
- Keep each solver's validation status separate from biological validation.
