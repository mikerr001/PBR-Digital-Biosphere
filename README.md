# PBR Digital Biosphere
Research codebase for a mechanistic algal photobioreactor and regenerative-habitat digital twin.

## Current milestone: PBR-06 inventory scaffold; scientific validation remains active
The repository now contains PBR-02 through PBR-06 software foundations. PBR-04A provides a carbonate-equilibrium prototype, parameter provenance checks, experimental-data conventions and independent holdout metrics. PBR-06 adds a transparent habitat inventory ledger. Neither milestone constitutes biological or engineering validation.

## Evidence audit
The active parameter register is `data/parameter_register.csv`; the audit snapshot and source-verification notes are in `data/parameter_register_audit.csv`. The low/high-light *Synechococcus elongatus* PCC 7942 growth rates and dark-respiration rates are traceable to Broddrick et al. (2019), DOI 10.1016/j.ymben.2018.11.001. Gross oxygen evolution observations from that study's Table 3 have been added in their original cell-normalised units. Do not convert them to dry-mass units without a condition-matched cell dry-mass conversion and uncertainty propagation. The DOI is verified; source-level figure/table extraction and independent replication remain outstanding. Unmeasured parameters remain blank/unknown rather than being fabricated.

## Carbon chemistry boundary
PBR-02 stores total dissolved inorganic carbon (DIC); PBR-04 Henry-law transfer uses molecular dissolved CO2. They are not interchangeable. The PBR-04A routine estimates molecular CO2 from DIC and alkalinity under a carbonate-only freshwater approximation. It is not yet suitable for direct coupling to BG-11 or marine culture because non-carbonate alkalinity, ionic-strength effects and medium-specific constants have not been characterised.

## Implemented
- PBR-02 reduced biomass, DIC, O2, N and P culture model.
- PBR-03 reduced KaiABC phase/entrainment scaffold; fitted PRCs and metabolic coupling remain open.
- PBR-04 flat-panel geometry, 1-D optics, two-phase gas transfer, lumped thermal rates and two-compartment exchange helper.
- PBR-02/PBR-04 dynamic coupling for biomass-dependent PAR attenuation, dissolved/headspace O2 transfer and liquid temperature.
- PBR-05 deterministic supervisory recommendations with sensor-quality fail-closed behaviour and operator confirmation; automatic actuation disabled.
- PBR-04A carbonate speciation prototype, parameter provenance audit, data schema and independent holdout metrics.
- PBR-06 lumped habitat O2, CO2, water, nitrogen and phosphorus inventories with explicit external flux inputs.

## Run the simulator

The quickest route is to clone/download this repository and run the PBR-02 command-line demo. Use Python 3.10–3.12.

```bash
git clone https://github.com/mikerr001/PBR-Digital-Biosphere.git
cd PBR-Digital-Biosphere
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest -q
python -m pbrbiosphere
```

The command writes `results/baseline_simulation.csv`, five scenario CSVs under `results/scenarios/`, and biomass, dissolved-oxygen and DIC plots under `results/figures/`. The default run is a five-day illustrative PBR-02 run. Its default parameter values are not validated biological measurements.

To change duration, initial conditions, parameters or environment, use the Python API. For example:

```python
from pbrbiosphere.config import Environment, InitialState, ModelParameters
from pbrbiosphere.simulate import run_simulation, save_results
from pbrbiosphere.plots import plot_results

params = ModelParameters()  # replace with sourced, condition-matched values
initial = InitialState(biomass=0.10, dic=2.0, oxygen=0.20,
                       nitrogen=1.0, phosphorus=0.10)
environment = Environment(temperature_c=25.0, irradiance=100.0,
                          photoperiod_hours=12.0, day_hours=24.0)
results = run_simulation(days=10, points=1001, params=params,
                         initial=initial, environment=environment)
save_results(results, "my_results")
plot_results(results, "my_results/figures")
print(results.tail())
```

For named light-schedule comparisons, use `run_standard_scenarios()` from `pbrbiosphere.scenarios`. For exploratory one-at-a-time sensitivity screening, use `one_at_a_time()` from `pbrbiosphere.sensitivity`. See `docs/SIMULATOR_USER_GUIDE.md` for the coupled reactor, carbonate, circadian, controller and habitat interfaces and their current limits.

**Scope warning:** `python -m pbrbiosphere` currently runs PBR-02 only. It does not automatically run the coupled PBR-02/PBR-04 reactor, PBR-03 circadian model, PBR-05 supervisor or PBR-06 habitat ledger. Those are separate Python interfaces, documented in the user guide. Never use this research simulator to design or operate human life-support equipment.

## Scientific guardrails
- Simulated values are not experimental measurements.
- Keep *Synechococcus elongatus* PCC 7942 and *Phaeodactylum tricornutum* evidence separate.
- Do not transfer KaiABC equations to *P. tricornutum*.
- Separate gross oxygen evolution from oxygen consumption.
- Preserve measurement basis (per cell, chlorophyll, protein or dry biomass).
- PBR-02 fixed-quota balances are reduced assumptions, not a complete reactor inventory.
- PBR-02 temperature response remains a neutral placeholder.
- A software test pass is not biological or physical validation.
- PBR-06 does not calculate safe atmospheric composition or human occupancy capacity.

## Install and test
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m pbrbiosphere
```
Python 3.10–3.12 are supported.

## Remaining scientific gates
- Complete source extraction and parameter identifiability audit, including *Phaeodactylum* strain-specific evidence.
- Characterise medium-specific carbonate chemistry and non-carbonate alkalinity.
- Fit and independently validate growth, gross/net O2, O2/CO2 kLa, optics and thermal parameters.
- Add atmosphere thermodynamics, crop/human physiology, waste processing and water/nutrient recovery only with traceable parameters.
- Establish uncertainty, model discrepancy and independent integrated holdout validation before any performance claims.

## Safety
Research simulator only. Do not use it to size, operate or certify human oxygen supply, underwater habitats, breathable atmospheres or pressure vessels.
