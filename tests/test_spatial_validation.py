import numpy as np
import pytest

from pbrbiosphere.run_artifacts import write_spatial_result
from pbrbiosphere.spatial_reactor import SpatialReactorConfig, simulate_spatial_reactor
from pbrbiosphere.spatial_validation import validate_run, compare_spatial_runs


def make_run(path, cells, run_id):
    result = simulate_spatial_reactor(
        60, 4,
        SpatialReactorConfig(cells=cells, flow_m3_s=0, incident_par_umol_m2_s=0),
    )
    write_spatial_result(result, path, {
        "run_id": run_id,
        "results": {},
        "model": {"validation_status": "UNVALIDATED"},
    })


def test_validate_run_checks_integrity_and_structure(tmp_path):
    run = tmp_path / "coarse"
    make_run(run, 4, "coarse")
    report = validate_run(run)
    assert report["integrity"] == "PASS"
    assert report["structural_checks"] == "PASS"
    assert report["physical_validation"] == "NOT_ESTABLISHED"


def test_tampered_archive_fails_hash_check(tmp_path):
    run = tmp_path / "tampered"
    make_run(run, 4, "tampered")
    with (run / "fields.npz").open("ab") as stream:
        stream.write(b"tamper")
    with pytest.raises(ValueError, match="SHA-256"):
        validate_run(run)


def test_compare_requires_finer_grid_and_reports_metrics(tmp_path):
    coarse, fine = tmp_path / "coarse", tmp_path / "fine"
    make_run(coarse, 4, "coarse")
    make_run(fine, 8, "fine")
    report = compare_spatial_runs(coarse, fine)
    assert report["refined_cells"] == 8
    assert set(report["relative_l2_difference"]) == {
        "biomass_g_l", "dic_mmol_l", "oxygen_mmol_l",
        "nitrogen_mmol_l", "phosphorus_mmol_l", "temperature_k",
    }
    assert report["formal_gci"] is False
