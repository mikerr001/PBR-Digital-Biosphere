"""Run the baseline and standard engineering scenarios."""
from pathlib import Path
from .simulate import run_simulation, save_results
from .plots import plot_results
from .scenarios import run_standard_scenarios


def main():
    results_dir = Path("results")
    baseline = run_simulation()
    baseline_path = save_results(baseline, str(results_dir))
    figures = plot_results(baseline)

    scenario_dir = results_dir / "scenarios"
    scenario_dir.mkdir(parents=True, exist_ok=True)
    scenarios = run_standard_scenarios()
    for name, frame in scenarios.items():
        frame.to_csv(scenario_dir / f"{name}.csv", index=False)

    print("PBR-02 reduced-model runs complete.")
    print("WARNING: default parameters are illustrative software assumptions, not validated organism data.")
    print(f"Baseline CSV: {baseline_path}")
    print(f"Scenario CSVs: {scenario_dir}")
    for path in figures:
        print(f"Figure: {path}")


if __name__ == "__main__":
    main()
