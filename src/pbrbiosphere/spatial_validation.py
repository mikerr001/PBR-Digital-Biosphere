"""Post-run integrity and numerical-comparison diagnostics for spatial PBR runs.

These checks establish file integrity and numerical consistency only. They do
not establish physical or biological validation.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from .run_artifacts import sha256_file

FIELDS = (
    "biomass_g_l", "dic_mmol_l", "oxygen_mmol_l",
    "nitrogen_mmol_l", "phosphorus_mmol_l", "temperature_k",
)


def load_run(run_dir: str | Path):
    root = Path(run_dir)
    fields_path = root / "fields.npz"
    manifest_path = root / "run-manifest.json"
    if not fields_path.is_file() or not manifest_path.is_file():
        raise FileNotFoundError("Run directory must contain fields.npz and run-manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest.get("results", {}).get("fields_sha256")
    actual = sha256_file(fields_path)
    if not expected or expected != actual:
        raise ValueError("Field archive SHA-256 does not match the run manifest")
    with np.load(fields_path, allow_pickle=False) as archive:
        arrays = {name: archive[name].copy() for name in archive.files}
    return arrays, manifest


def validate_run(run_dir: str | Path) -> dict:
    """Check archive integrity, array structure, finite values and basic bounds."""
    arrays, manifest = load_run(run_dir)
    required = {"time_s", "x_m", *FIELDS}
    missing = sorted(required - arrays.keys())
    if missing:
        raise ValueError(f"Missing required arrays: {missing}")

    time = arrays["time_s"]
    x = arrays["x_m"]
    if time.ndim != 1 or time.size < 2 or not np.all(np.diff(time) > 0):
        raise ValueError("time_s must be a strictly increasing 1-D array")
    if x.ndim != 1 or x.size < 3 or not np.all(np.diff(x) > 0):
        raise ValueError("x_m must be a strictly increasing 1-D array")

    field_report = {}
    for name in FIELDS:
        field = arrays[name]
        if field.shape != (time.size, x.size):
            raise ValueError(f"{name} shape {field.shape} != {(time.size, x.size)}")
        if not np.isfinite(field).all():
            raise ValueError(f"{name} contains NaN or infinite values")
        minimum = float(np.min(field))
        if name == "temperature_k":
            if minimum <= 0:
                raise ValueError("temperature_k must remain above absolute zero")
        elif minimum < -1e-10:
            raise ValueError(f"{name} contains materially negative concentrations")
        field_report[name] = {
            "minimum": minimum,
            "maximum": float(np.max(field)),
            "initial_mean": float(np.mean(field[0])),
            "final_mean": float(np.mean(field[-1])),
        }

    return {
        "run_id": manifest.get("run_id", "unknown"),
        "integrity": "PASS",
        "structural_checks": "PASS",
        "finite_value_checks": "PASS",
        "basic_bounds": "PASS",
        "time_points": int(time.size),
        "spatial_cells": int(x.size),
        "duration_s": float(time[-1] - time[0]),
        "fields": field_report,
        "solver_success": bool(manifest.get("results", {}).get("solver_success", False)),
        "physical_validation": "NOT_ESTABLISHED",
        "notes": [
            "These checks do not prove conservation or physical accuracy.",
            "A successful solver status is not a validation result.",
        ],
    }


def compare_spatial_runs(reference_dir: str | Path, refined_dir: str | Path) -> dict:
    """Compare two spatial grids at common output times using linear interpolation.

    The reference grid is interpolated onto the refined grid. The returned
    relative L2 differences are diagnostics, not a formal GCI uncertainty.
    """
    a, ma = load_run(reference_dir)
    b, mb = load_run(refined_dir)
    if not np.array_equal(a["time_s"], b["time_s"]):
        raise ValueError("Runs must use identical output time arrays")
    if b["x_m"].size <= a["x_m"].size:
        raise ValueError("The second run must have a strictly finer spatial grid")
    if not (np.isclose(a["x_m"][0], b["x_m"][0]) and
            np.isclose(a["x_m"][-1], b["x_m"][-1])):
        raise ValueError("Runs must cover the same spatial domain")

    metrics = {}
    for name in FIELDS:
        ref = a[name]
        fine = b[name]
        mapped = np.vstack([
            np.interp(b["x_m"], a["x_m"], row) for row in ref
        ])
        scale = max(float(np.linalg.norm(fine.ravel())), 1e-14)
        rel_l2 = float(np.linalg.norm((fine - mapped).ravel()) / scale)
        metrics[name] = {"relative_l2_difference": rel_l2}
    return {
        "reference_run": ma.get("run_id", "unknown"),
        "refined_run": mb.get("run_id", "unknown"),
        "reference_cells": int(a["x_m"].size),
        "refined_cells": int(b["x_m"].size),
        "relative_l2_difference": metrics,
        "interpretation": "GRID_SENSITIVITY_DIAGNOSTIC_ONLY",
        "formal_gci": False,
        "physical_validation": "NOT_ESTABLISHED",
    }
