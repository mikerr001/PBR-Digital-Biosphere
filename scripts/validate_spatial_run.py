#!/usr/bin/env python3
"""Validate spatial run files and optionally compare two spatial resolutions."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from pbrbiosphere.validation import validate_run, compare_spatial_runs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Directory containing fields.npz and run-manifest.json")
    parser.add_argument("--compare", type=Path, help="Optional finer-grid run directory")
    parser.add_argument("--output", type=Path, help="Write JSON report to this path")
    args = parser.parse_args(argv)

    report = validate_run(args.run_dir)
    if args.compare:
        report["grid_comparison"] = compare_spatial_runs(args.run_dir, args.compare)
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
