"""Run a clearly labelled illustrative baseline scenario."""
from .simulate import run_simulation, save_results
from .plots import plot_results


def main():
    df = run_simulation()
    csv_path = save_results(df)
    figures = plot_results(df)
    print("Illustrative scaffold simulation complete.")
    print("WARNING: starter parameters are placeholders, not organism-validated data.")
    print(f"CSV: {csv_path}")
    for path in figures:
        print(f"Plot: {path}")


if __name__ == "__main__":
    main()
