#!/usr/bin/env python3
"""Parametric CadQuery model of the provisional PBR flat-panel reactor.

Units: millimetres. Origin: centre of the external rectangular envelope.
Concept geometry only; not a fabrication or pressure-vessel design.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cadquery as cq


# Keep these values synchronized with flat_panel_reactor.scad.
PANEL_LENGTH = 300.0
PANEL_HEIGHT = 200.0
PANEL_DEPTH = 40.0
WALL = 3.0

PORT_BORE_D = 8.0
PORT_BOSS_OD = 16.0
BOSS_PROJECTION = 10.0

SENSOR_X = (-75.0, 75.0)
SENSOR_Y = (-50.0, 50.0)
GAS_X = (-75.0, 75.0)

# Internal fluid-domain features. Port X/Y values are measured from the
# left/front external edges, respectively; Y in this register means depth.
SPARGER_DIAMETER = 8.0
SPARGER_X = 150.0
SPARGER_Y = 20.0
DRAIN_DIAMETER = 10.0
DRAIN_X = 30.0
DRAIN_Y = 20.0
BAFFLE_COUNT = 2
BAFFLE_HEIGHT = 25.0
BAFFLE_THICKNESS = 2.0


def _edge_referenced_port(x_from_left: float, z_from_front: float) -> tuple[float, float]:
    """Convert left/front edge dimensions to centred X/Z coordinates."""
    return x_from_left - PANEL_LENGTH / 2, z_from_front - PANEL_DEPTH / 2


def build_reactor() -> cq.Workplane:
    """Build the shell, bosses, through-bores, bottom ports, and internal baffles."""
    outer = cq.Workplane("XY").box(
        PANEL_LENGTH, PANEL_HEIGHT, PANEL_DEPTH, centered=(True, True, True)
    )
    cavity = cq.Workplane("XY").box(
        PANEL_LENGTH - 2 * WALL,
        PANEL_HEIGHT - 2 * WALL,
        PANEL_DEPTH - 2 * WALL,
        centered=(True, True, True),
    )
    part = outer.cut(cavity)

    # Four sensor bosses on the rear Z face; their axes point outward (-Z).
    for x in SENSOR_X:
        for y in SENSOR_Y:
            boss = cq.Solid.makeCylinder(
                PORT_BOSS_OD / 2, BOSS_PROJECTION,
                cq.Vector(x, y, -PANEL_DEPTH / 2), cq.Vector(0, 0, -1),
            )
            part = part.union(boss)

    # Two gas bosses on the top Y face; their axes point outward (+Y).
    for x in GAS_X:
        boss = cq.Solid.makeCylinder(
            PORT_BOSS_OD / 2, BOSS_PROJECTION,
            cq.Vector(x, PANEL_HEIGHT / 2, 0), cq.Vector(0, 1, 0),
        )
        part = part.union(boss)

    # Bore each sensor port from the boss tip through the wall into the cavity.
    for x in SENSOR_X:
        for y in SENSOR_Y:
            bore = cq.Solid.makeCylinder(
                PORT_BORE_D / 2, BOSS_PROJECTION + WALL + 2,
                cq.Vector(x, y, -PANEL_DEPTH / 2 - BOSS_PROJECTION - 1),
                cq.Vector(0, 0, 1),
            )
            part = part.cut(bore)

    # Bore each gas port from the boss tip through the top wall into the cavity.
    for x in GAS_X:
        bore = cq.Solid.makeCylinder(
            PORT_BORE_D / 2, BOSS_PROJECTION + WALL + 2,
            cq.Vector(x, PANEL_HEIGHT / 2 + BOSS_PROJECTION + 1, 0),
            cq.Vector(0, -1, 0),
        )
        part = part.cut(bore)

    # Bottom ports run along +Y through the 3 mm bottom wall and 2 mm into
    # the cavity. Only the wall intersection contributes removed solid volume.
    bottom_y = -PANEL_HEIGHT / 2 - 1.0
    for diameter, x_edge, z_edge in (
        (SPARGER_DIAMETER, SPARGER_X, SPARGER_Y),
        (DRAIN_DIAMETER, DRAIN_X, DRAIN_Y),
    ):
        x, z = _edge_referenced_port(x_edge, z_edge)
        bore = cq.Solid.makeCylinder(
            diameter / 2, WALL + 2,
            cq.Vector(x, bottom_y, z), cq.Vector(0, 1, 0),
        )
        part = part.cut(bore)

    # Baffles are solid plates fused to the internal floor, not subtractive cuts.
    usable_length = PANEL_LENGTH - 2 * WALL
    floor_y = -PANEL_HEIGHT / 2 + WALL
    for index in range(BAFFLE_COUNT):
        x_from_left = WALL + usable_length * (index + 1) / (BAFFLE_COUNT + 1)
        x = x_from_left - PANEL_LENGTH / 2
        baffle = (
            cq.Workplane("XY")
            .box(BAFFLE_THICKNESS, BAFFLE_HEIGHT, PANEL_DEPTH - 2 * WALL,
                 centered=(True, True, True))
            .translate((x, floor_y + BAFFLE_HEIGHT / 2, 0))
        )
        part = part.union(baffle)

    return part


def main() -> None:
    export_dir = Path("cad/provisional/exports")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", type=Path, default=export_dir / "flat_panel_reactor.step")
    parser.add_argument("--stl", type=Path, default=export_dir / "flat_panel_reactor_cadquery.stl")
    args = parser.parse_args()

    reactor = build_reactor()
    args.step.parent.mkdir(parents=True, exist_ok=True)
    args.stl.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(reactor, str(args.step))
    cq.exporters.export(reactor, str(args.stl))
    print(f"STEP: {args.step}")
    print(f"STL:  {args.stl}")
    print("Status: GEOMETRY_EXPORTED_NOT_VALIDATED")


if __name__ == "__main__":
    main()
