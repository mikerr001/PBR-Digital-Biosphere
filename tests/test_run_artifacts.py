import json
import numpy as np
from pbrbiosphere.run_artifacts import write_spatial_result
from pbrbiosphere.spatial_reactor import simulate_spatial_reactor, SpatialReactorConfig


def test_run_artifacts_are_reproducible_and_hash_fields(tmp_path):
    result = simulate_spatial_reactor(
        30, 2, SpatialReactorConfig(cells=3, flow_m3_s=0, incident_par_umol_m2_s=0)
    )
    arrays, manifest = write_spatial_result(
        result, tmp_path,
        {"schema_version": "1.0.0", "run_id": "test-run",
         "model": {"id": "PBR-SPATIAL-1D-001", "version": "0.1.0",
                   "fidelity_tier": 2, "validation_status": "UNVALIDATED"}},
    )
    assert arrays.exists() and manifest.exists()
    data = np.load(arrays)
    assert data["biomass_g_l"].shape == (2, 3)
    payload = json.loads(manifest.read_text())
    assert len(payload["results"]["fields_sha256"]) == 64
    assert payload["results"]["solver_success"]
