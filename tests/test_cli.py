import json
from pbrbiosphere.cli import main


def test_cli_writes_manifest_and_fields(tmp_path):
    output = tmp_path / "run"
    code = main([
        "--duration-s", "10", "--output-points", "2",
        "--output", str(output), "--run-id", "cli-test",
    ])
    assert code == 0
    manifest = json.loads((output / "run-manifest.json").read_text())
    assert manifest["run_id"] == "cli-test"
    assert manifest["model"]["validation_status"] == "UNVALIDATED"
    assert (output / "fields.npz").exists()
