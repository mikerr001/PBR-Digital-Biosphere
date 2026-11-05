#!/usr/bin/env python3
"""Import a STEP vessel with Gmsh OCC, assign named boundary groups, and mesh it.

Requires the optional Gmsh Python module and a STEP file exported from CAD.
The manifest explicitly identifies each planar boundary by axis/coordinate;
no boundary is silently assigned by geometric guessing.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from pbrbiosphere.mesh_selectors import classify_surface_bbox


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--mesh-size-m", type=float, default=0.02)
    parser.add_argument("--tolerance-m", type=float, default=1e-5)
    args = parser.parse_args(argv)
    if not args.step.is_file():
        parser.error(f"STEP file does not exist: {args.step}")
    if args.mesh_size_m <= 0 or args.tolerance_m <= 0:
        parser.error("mesh size and geometric tolerance must be positive")
    manifest = json.loads(args.manifest.read_text())
    groups = manifest.get("surface_groups", [])
    if not groups:
        parser.error("manifest must define non-empty surface_groups")

    try:
        import gmsh
    except ImportError as exc:
        raise SystemExit("Gmsh Python API is required: install gmsh in this environment") from exc

    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 1)
        gmsh.model.add("pbr_cad_reactor")
        gmsh.model.occ.importShapes(str(args.step), highestDimOnly=True)
        gmsh.model.occ.synchronize()
        volumes = gmsh.model.getEntities(3)
        surfaces = gmsh.model.getEntities(2)
        if len(volumes) != 1:
            raise RuntimeError(f"Expected exactly one fluid volume, found {len(volumes)}")

        assigned = set()
        for group in groups:
            name = group["name"]
            selector = group["plane"]
            matched = []
            for _, tag in surfaces:
                bbox = gmsh.model.getBoundingBox(2, tag)
                if classify_surface_bbox(bbox, selector, args.tolerance_m):
                    matched.append(tag)
            if not matched:
                raise RuntimeError(f"No CAD faces matched named boundary '{name}'")
            overlap = assigned.intersection(matched)
            if overlap:
                raise RuntimeError(f"Boundary groups overlap on surface tags {sorted(overlap)}")
            assigned.update(matched)
            physical = gmsh.model.addPhysicalGroup(2, matched)
            gmsh.model.setPhysicalName(2, physical, name)

        unassigned = sorted({tag for _, tag in surfaces} - assigned)
        if unassigned:
            raise RuntimeError(
                "Unassigned CAD surfaces remain; add explicit surface_groups "
                f"selectors before meshing. Tags: {unassigned}"
            )
        fluid = gmsh.model.addPhysicalGroup(3, [volumes[0][1]])
        gmsh.model.setPhysicalName(3, fluid, manifest.get("fluid_region", "fluid"))
        gmsh.option.setNumber("Mesh.MeshSizeMin", args.mesh_size_m)
        gmsh.option.setNumber("Mesh.MeshSizeMax", args.mesh_size_m)
        gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
        gmsh.model.mesh.generate(3)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        gmsh.write(str(args.output))
        print(json.dumps({
            "step": str(args.step), "mesh": str(args.output),
            "fluid_region": manifest.get("fluid_region", "fluid"),
            "boundary_groups": [g["name"] for g in groups],
            "surface_count": len(surfaces), "volume_count": len(volumes),
            "mesh_format": "Gmsh 2.2; convert with gmshToFoam",
            "validation": "MESH_GENERATED_NOT_VALIDATED",
        }, indent=2))
    finally:
        gmsh.finalize()


if __name__ == "__main__":
    main()
