#!/usr/bin/env python3
"""Validate exported provisional CAD solids and STL mesh integrity."""
from __future__ import annotations

import argparse
from pathlib import Path

import cadquery as cq
import trimesh


EXPECTED_EXTENTS_MM = (300.0, 210.0, 50.0)
EXTENT_TOLERANCE_MM = 0.1
MESH_VOLUME_RELATIVE_TOLERANCE = 0.001


def check_mesh(path: Path) -> tuple[trimesh.Trimesh, float]:
    mesh = trimesh.load(path, force="mesh")
    if not isinstance(mesh, trimesh.Trimesh):
        raise RuntimeError(f"{path}: expected a triangular mesh")
    if not mesh.is_watertight:
        raise RuntimeError(f"{path}: mesh is not watertight")
    components = mesh.split(only_watertight=False)
    if len(components) != 1:
        raise RuntimeError(f"{path}: expected one connected component, found {len(components)}")
    extents = tuple(float(v) for v in mesh.extents)
    for actual, expected in zip(extents, EXPECTED_EXTENTS_MM):
        if abs(actual - expected) > EXTENT_TOLERANCE_MM:
            raise RuntimeError(f"{path}: extents {extents} do not match expected {EXPECTED_EXTENTS_MM}")
    return mesh, float(mesh.volume)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", type=Path, required=True)
    parser.add_argument("--cadquery-stl", type=Path, required=True)
    parser.add_argument("--openscad-stl", type=Path, required=True)
    args = parser.parse_args()

    step_model = cq.importers.importStep(str(args.step))
    step_solids = step_model.solids().vals()
    if len(step_solids) != 1:
        raise RuntimeError(f"STEP must contain one solid; found {len(step_solids)}")
    step_solid = step_solids[0]
    if not step_solid.isValid():
        raise RuntimeError("STEP B-rep is invalid")
    step_box = step_solid.BoundingBox()
    step_extents = (step_box.xlen, step_box.ylen, step_box.zlen)
    for actual, expected in zip(step_extents, EXPECTED_EXTENTS_MM):
        if abs(actual - expected) > EXTENT_TOLERANCE_MM:
            raise RuntimeError(f"STEP extents {step_extents} do not match expected {EXPECTED_EXTENTS_MM}")

    cq_mesh, cq_volume = check_mesh(args.cadquery_stl)
    scad_mesh, scad_volume = check_mesh(args.openscad_stl)
    relative_difference = abs(cq_volume - scad_volume) / max(cq_volume, scad_volume)
    if relative_difference > MESH_VOLUME_RELATIVE_TOLERANCE:
        raise RuntimeError(
            f"OpenSCAD/CadQuery mesh volumes differ by {relative_difference:.4%}; "
            f"limit is {MESH_VOLUME_RELATIVE_TOLERANCE:.2%}"
        )

    print("CAD export validation: PASS")
    print(f"STEP solid count: {len(step_solids)}; B-rep valid: {step_solid.isValid()}")
    print(f"STEP extents (mm): {step_extents}")
    print(f"OpenSCAD STL: watertight={scad_mesh.is_watertight}; volume={scad_volume:.3f} mm^3")
    print(f"CadQuery STL: watertight={cq_mesh.is_watertight}; volume={cq_volume:.3f} mm^3")
    print(f"Relative STL volume difference: {relative_difference:.4%}")


if __name__ == "__main__":
    main()
