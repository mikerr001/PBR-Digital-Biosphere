#!/usr/bin/env python3
"""Validate STEP B-rep, connected/watertight STL meshes, and analytic volumes."""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import cadquery as cq
import trimesh


EXPECTED_EXTENTS_MM = (300.0, 210.0, 50.0)
EXTENT_TOLERANCE_MM = 0.1
MESH_VOLUME_RELATIVE_TOLERANCE = 0.001
SOLID_VOLUME_RELATIVE_TOLERANCE = 0.001

PANEL_LENGTH = 300.0
PANEL_HEIGHT = 200.0
PANEL_DEPTH = 40.0
WALL = 3.0
PORT_BOSS_OD = 16.0
BOSS_PROJECTION = 10.0
PORT_BORE_D = 8.0
SPARGER_DIAMETER = 8.0
DRAIN_DIAMETER = 10.0
BAFFLE_COUNT = 2
BAFFLE_HEIGHT = 25.0
BAFFLE_THICKNESS = 2.0


def analytic_volume_accounting() -> tuple[float, float, float, float]:
    """Return baseline, port removal, baffle addition, and expected final volume."""
    shell = (
        PANEL_LENGTH * PANEL_HEIGHT * PANEL_DEPTH
        - (PANEL_LENGTH - 2 * WALL)
        * (PANEL_HEIGHT - 2 * WALL)
        * (PANEL_DEPTH - 2 * WALL)
    )
    boss_volume = 6 * math.pi * (PORT_BOSS_OD / 2) ** 2 * BOSS_PROJECTION
    existing_bore_volume = (
        6 * math.pi * (PORT_BORE_D / 2) ** 2 * (BOSS_PROJECTION + WALL + 2)
    )
    baseline = shell + boss_volume - existing_bore_volume
    port_removal = (
        math.pi * (SPARGER_DIAMETER / 2) ** 2 * WALL
        + math.pi * (DRAIN_DIAMETER / 2) ** 2 * WALL
    )
    baffle_addition = (
        BAFFLE_COUNT * BAFFLE_THICKNESS
        * (PANEL_DEPTH - 2 * WALL) * BAFFLE_HEIGHT
    )
    expected = baseline - port_removal + baffle_addition
    return baseline, port_removal, baffle_addition, expected


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
            raise RuntimeError(
                f"{path}: extents {extents} do not match expected {EXPECTED_EXTENTS_MM}"
            )
    return mesh, float(mesh.volume)


def main() -> None:
    export_dir = Path("cad/provisional/exports")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", type=Path, default=export_dir / "flat_panel_reactor.step")
    parser.add_argument(
        "--cadquery-stl", type=Path,
        default=export_dir / "flat_panel_reactor_cadquery.stl",
    )
    parser.add_argument(
        "--openscad-stl", type=Path,
        default=export_dir / "flat_panel.stl",
    )
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
            raise RuntimeError(
                f"STEP extents {step_extents} do not match expected {EXPECTED_EXTENTS_MM}"
            )

    baseline, port_removal, baffle_addition, expected_volume = analytic_volume_accounting()
    step_volume = float(step_solid.Volume())
    volume_error = abs(step_volume - expected_volume) / expected_volume
    if volume_error > SOLID_VOLUME_RELATIVE_TOLERANCE:
        raise RuntimeError(
            f"STEP volume {step_volume:.3f} mm^3 differs from analytic expectation "
            f"{expected_volume:.3f} mm^3 by {volume_error:.4%}"
        )

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
    print(f"Baseline solid volume: {baseline:.3f} mm^3")
    print(f"Port volume removed: {port_removal:.3f} mm^3")
    print(f"Baffle volume added: {baffle_addition:.3f} mm^3")
    print(f"Net volume change: {baffle_addition-port_removal:+.3f} mm^3")
    print(f"Expected final solid volume: {expected_volume:.3f} mm^3")
    print(f"STEP solid volume: {step_volume:.3f} mm^3 (error {volume_error:.4%})")
    print(f"OpenSCAD STL: watertight={scad_mesh.is_watertight}; volume={scad_volume:.3f} mm^3")
    print(f"CadQuery STL: watertight={cq_mesh.is_watertight}; volume={cq_volume:.3f} mm^3")
    print(f"Relative STL volume difference: {relative_difference:.4%}")


if __name__ == "__main__":
    main()
