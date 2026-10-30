# Simulator user guide

## 1. What runs today

The repository contains several research modules, but the default command runs only the reduced PBR-02 algal culture model:

```bash
python -m pbrbiosphere
```

It creates:
- `results/baseline_simulation.csv`
- `results/scenarios/dark.csv`
- `results/scenarios/constant_light.csv`
- `results/scenarios/light_dark_12_12.csv`
- `results/scenarios/low_light_12_12.csv`
- `results/scenarios/high_light_12_12.csv`
- `results/figures/biomass.png`
- `results/figures/oxygen.png`
- `results/figures/dic.png`

The default values are illustrative demonstration settings, not a calibrated strain-specific parameter set.

## 2. Install

Requirements: Python 3.10, 3.11 or 3.12.

```bash
git clone https://github.com/mikerr001/PBR-Digital-Biosphere.git
cd PBR-Digital-Biosphere
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest -q
python -m pbrbiosphere
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`. On Android, the least-friction option is to open the repository in a browser-based Python environment that supports scientific Python packages; Termux may work, but compiling/installing NumPy, SciPy and Matplotlib can be device- and package-version-dependent. The repository itself is hosted at https://github.com/mikerr001/PBR-Digital-Biosphere.

## 3. Change a PBR-02 run

Create a Python file, for example `run_my_simulation.py`:

```python
from pbrbiosphere.config import Environment, InitialState, ModelParameters
from pbrbiosphere.simulate import run_simulation, save_results
from pbrbiosphere.plots import plot_results

# These are demo values. Replace them only with traceable, compatible data.
params = ModelParameters()
initial = InitialState(
    biomass=0.10,  # g dry weight / L
    dic=2.0,       # mmol C / L
    oxygen=0.20,   # mmol O2 / L
    nitrogen=1.0,  # mmol N / L
    phosphorus=0.10 # mmol P / L
)
environment = Environment(
    temperature_c=25.0,
    irradiance=100.0,       # umol photons / m2 / s (incident PAR)
    photoperiod_hours=12.0,
    day_hours=24.0
)

df = run_simulation(
    days=10,
    points=1001,
    params=params,
    initial=initial,
    environment=environment
)
print(df.tail())
save_results(df, "my_results")
plot_results(df, "my_results/figures")
```

Run it with:

```bash
python run_my_simulation.py
```

Important: `Environment.irradiance` is incident PAR in micromoles of photons per square metre per second. It is not W/m². The PBR-02 model currently uses a neutral temperature response placeholder; changing temperature does not yet produce a validated temperature-dependent growth response.

## 4. Compare light schedules

```python
from pbrbiosphere.scenarios import run_standard_scenarios

scenarios = run_standard_scenarios(days=5, points=501)
for name, frame in scenarios.items():
    print(name, frame.iloc[-1].to_dict())
    frame.to_csv(f"{name}.csv", index=False)
```

This compares dark, constant-light, 12:12, low-light and high-light model scenarios under the same initial conditions. It is a model experiment, not a laboratory result.

## 5. Explore parameter sensitivity

```python
from pbrbiosphere.sensitivity import one_at_a_time

screen = one_at_a_time(
    "mu_max",
    values=[0.1, 0.2, 0.35, 0.5],
    days=5,
    points=201
)
print(screen)
```

This is one-at-a-time screening only. It is not global sensitivity analysis, parameter estimation, or evidence that the varied values are biologically plausible.

## 6. Other module entry points

These are separate interfaces; the default command does not automatically execute them.

### PBR-03 circadian phase model

```python
from pbrbiosphere.circadian.model import (
    CircadianParameters, LightTransition, simulate_circadian
)

trace = simulate_circadian(
    duration_hours=72,
    transitions=[
        LightTransition(0, True),
        LightTransition(12, False),
        LightTransition(24, True),
        LightTransition(36, False),
        LightTransition(48, True),
        LightTransition(60, False),
    ],
    parameters=CircadianParameters(intrinsic_period_hours=24.5)
)
print(trace.tail())
```

This is a reduced phase oscillator with empirical PRC inputs. The default PRCs are zero; the output proxy is not a validated molecular KaiABC or RpaA model, and it is not coupled to growth or oxygen production.

### PBR-04 reactor rate assembly

Use `pbrbiosphere.reactor.twin.reactor_rates` with `ReactorState`, `ReactorEnvironment`, `FlatPanelGeometry`, `GasTransferParameters` and `ThermalParameters`. It returns instantaneous optical, gas-transfer and thermal rates. It does not by itself integrate a complete reactor trajectory. Consult the corresponding module specifications for units and parameter construction.

### Coupled PBR-02/PBR-04 simulation

Use `run_coupled_simulation` from `pbrbiosphere.integration.coupled`. It requires geometry, gas-transfer parameters, thermal parameters, attenuation coefficient, incident thermal irradiance and ambient temperature. It couples biomass-dependent PAR attenuation, biological dissolved O2 and headspace O2 transfer, and lumped temperature. CO2 transfer is deliberately not coupled until validated carbonate chemistry is available. Do not equate total DIC with molecular dissolved CO2.

### PBR-04A carbonate chemistry

Use `carbonate_speciation` and `co2_gas_transfer_rate` from `pbrbiosphere.chemistry.carbonate`. This is a carbonate-only freshwater equilibrium approximation. It excludes non-carbonate alkalinity, activity corrections and salinity effects. It is not yet a validated medium-specific BG-11 or marine chemistry solver.

### PBR-05 supervisory recommendations

Use `decide` with `SensorSnapshot` and experiment-specific `ControlLimits` from `pbrbiosphere.control.supervisor`. The function returns bounded recommendations and fails closed for missing, stale, invalid or alarmed readings. It does not actuate equipment and is not a safety interlock.

### PBR-06 habitat inventory ledger

Use `simulate_habitat` with `HabitatState` and `HabitatInputs` from `pbrbiosphere.habitat.balances`. It integrates constant, explicitly supplied whole-habitat fluxes for O2, CO2, water, nitrogen and phosphorus. It does not contain validated human metabolic rates, dynamic crop/algal production, atmospheric thermodynamics or a closed-loop ecosystem.

## 7. Reproduce and inspect results

- Keep the input parameters and initial conditions with every output CSV.
- Record organism, strain, medium, temperature, irradiance, photoperiod, measurement basis and source for every experimental parameter.
- Never compare datasets with incompatible units or measurement bases.
- For independent validation, use the exact time grid required by `compare_independent_dataset`; the function deliberately refuses silent interpolation.
- Keep fitting data separate from independent holdout data. Do not tune parameters against the holdout set.

## 8. Interpretation and safety

A successful Python run means the code executed. A passing test means the tested software behaviour matched its test. Neither establishes biological validity, physical reactor performance, oxygen sufficiency, safe atmospheric composition or human occupancy capacity.

This is a research and educational simulator. Do not use it to size, operate or certify human life-support systems, underwater habitats, breathable atmospheres or pressure vessels.
