"""Reproducible spatial-reactor run output and manifest utilities.

The manifest records inputs and provenance. It does not certify a model.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_spatial_result(result: Any, output_dir: str | Path,
                         manifest: dict[str, Any]) -> tuple[Path, Path]:
    """Write compressed numerical fields and a JSON run manifest."""
    import numpy as np

    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    arrays_path = target / "fields.npz"
    np.savez_compressed(
        arrays_path, time_s=result.time_s, x_m=result.x_m,
        biomass_g_l=result.biomass_g_l, dic_mmol_l=result.dic_mmol_l,
        oxygen_mmol_l=result.oxygen_mmol_l, nitrogen_mmol_l=result.nitrogen_mmol_l,
        phosphorus_mmol_l=result.phosphorus_mmol_l, temperature_k=result.temperature_k,
        par_umol_m2_s=result.par_umol_m2_s,
    )
    payload = dict(manifest)
    payload.setdefault("results", {})
    payload["results"].update({
        "fields_file": arrays_path.name,
        "fields_sha256": sha256_file(arrays_path),
        "solver_success": bool(result.success),
        "solver_message": str(result.solver_message),
        "model_metadata": result.metadata,
    })
    manifest_path = target / "run-manifest.json"
    manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return arrays_path, manifest_path
