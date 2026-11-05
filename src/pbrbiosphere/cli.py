"""Command-line entry point for reproducible spatial PBR runs."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

from .config import ModelParameters
from .run_artifacts import write_spatial_result
from .spatial_reactor import (
    SpatialInitialState, SpatialReactorConfig, simulate_spatial_reactor,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run the unvalidated 1-D spatial PBR model.")
    parser.add_argument("--config", type=Path, help="JSON file containing config, initial, inlet and parameters")
    parser.add_argument("--duration-s", type=float, default=3600.0)
    parser.add_argument("--output-points", type=int, default=25)
    parser.add_argument("--output", type=Path, default=Path("pbr-run"))
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args(argv)

    payload = json.loads(args.config.read_text(encoding="utf-8")) if args.config else {}
    config = SpatialReactorConfig(**payload.get("config", {}))
    initial = SpatialInitialState(**payload.get("initial", {}))
    inlet_data = payload.get("inlet")
    inlet = SpatialInitialState(**inlet_data) if inlet_data else None
    parameters = ModelParameters(**payload.get("parameters", {}))
    result = simulate_spatial_reactor(
        args.duration_s, args.output_points, config=config, initial=initial,
        inlet=inlet, parameters=parameters,
    )
    manifest = {
        "schema_version": "1.0.0",
        "run_id": args.run_id or datetime.now(timezone.utc).strftime("pbr-%Y%m%dT%H%M%SZ"),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "model": {
            "id": "PBR-SPATIAL-1D-001", "version": "0.1.0",
            "fidelity_tier": 2, "validation_status": "UNVALIDATED",
        },
        "geometry": {"source": "idealised-1d-reactor", "units": "m"},
        "numerics": {
            "method": "SciPy solve_ivp BDF / method-of-lines",
            "time_step_s": args.duration_s / (args.output_points - 1),
            "tolerance": 1e-6, "mesh_cells": config.cells,
            "converged": bool(result.success),
        },
        "initial_conditions": vars(initial),
        "boundary_conditions": {
            "inlet": vars(inlet or initial), "flow_m3_s": config.flow_m3_s,
            "axial_dispersion_m2_s": config.axial_dispersion_m2_s,
        },
        "provenance": {
            "parameter_register_revision": "PBR-02-demo-parameters",
            "datasets": [], "operator_notes": "Illustrative defaults unless independently sourced.",
        },
    }
    arrays, manifest_path = write_spatial_result(result, args.output, manifest)
    print(json.dumps({
        "success": result.success, "message": result.solver_message,
        "arrays": str(arrays), "manifest": str(manifest_path),
        "fidelity_tier": 2, "validation": "UNVALIDATED",
    }, indent=2))
    return 0 if result.success else 2


if __name__ == "__main__":
    raise SystemExit(main())
