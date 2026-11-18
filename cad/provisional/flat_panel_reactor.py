#!/usr/bin/env python3
"""Parametric CadQuery model of the provisional PBR flat-panel reactor.

Units: millimetres. Origin: centre of the external rectangular envelope.
Concept geometry only; not a fabrication or pressure-vessel design.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cadquery as cq


# Keep these values synchronized with flat_panel_reactor.scad and README.md.
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


def build_reactor() -> cq.Workplane:
    """Build the closed hollow shell with four sensor and two gas ports."""
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
                PORT_BOSS_OD / 2,
                BOSS_PROJECTION,
                cq.Vector(x, y, -PANEL_DEPTH / 2),
                cq.Vector(0, 0, -1),
            )
            part = part.union(boss)

    # Two gas bosses on the top Y face; their axes point outward (+Y).
    for x in GAS_X:
        boss = cq.Solid.makeCylinder(
            PORT_BOSS_OD / 2,
            BOSS_PROJECTION,
            cq.Vector(x, PANEL_HEIGHT / 2, 0),
            cq.Vector(0, 1, 0),
        )
        part = part.union(boss)

    # Bore each sensor port from the boss tip through the wall into the cavity.
    for x in SENSOR_X:
        for y in SENSOR_Y:
            bore = cq.Solid.makeCylinder(
                PORT_BORE_D / 2,
                BOSS_PROJECTION + WALL + 2,
                cq.Vector(x, y, -PANEL_DEPTH / 2 - BOSS_PROJECTION - 1),
                cq.Vector(0, 0, 1),
            )
            part = part.cut(bore)

    # Bore each gas port from the boss tip through the top wall into the cavity.
    for x in GAS_X:
        bore = cq.Solid.makeCylinder(
            PORT_BORE_D / 2,
            BOSS_PROJECTION + WALL + 2,
            cq.Vector(x, PANEL_HEIGHT / 2 + BOSS_PROJECTION + 1, 0),
            cq.Vector(0, -1, 0),
        )
        part = part.cut(bore)

    return part


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", type=Path, default=Path("flat_panel_reactor.step"))
    parser.add_argument("--stl", type=Path, default=Path("flat_panel_reactor.stl"))
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
