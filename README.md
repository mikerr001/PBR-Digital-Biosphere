# PBR Digital Biosphere

Research codebase for a mechanistic photobioreactor and regenerative-habitat digital twin.

## Current milestone: PBR-03

PBR-03 adds a separate reduced circadian phase/entrainment subsystem for *Synechococcus elongatus* PCC 7942. It is not yet biologically parameterised: default phase-response curves are zero and no clock effect is applied to PBR-02 growth or oxygen balances. See `docs/PBR-03_MODEL_SPEC.md` and `docs/PBR-03_VALIDATION_PLAN.md`.

## Previous milestone: PBR-02

PBR-02 implements a reduced, well-mixed algal-culture physiology prototype. It is executable and testable, but **not yet biologically validated**. Default values are software-demo assumptions. Only source-traceable measurements in the evidence register should be used as biological parameters.

### Scientific guardrails
- Never present simulated values as experimental measurements.
- Keep *Synechococcus elongatus* PCC 7942 and *Phaeodactylum tricornutum* evidence separate.
- Do not transfer KaiABC equations to *P. tricornutum*.
- Separate gross oxygen evolution from oxygen consumption.
- Preserve measurement basis: per cell, chlorophyll, protein or dry biomass.
- The current fixed-quota C/N/P closures are reduced-model assumptions, not a complete reactor elemental inventory.
- This software is not a human life-support controller or safety-certified design tool.

## Run locally or in a cloud notebook

Python 3.10, 3.11 or 3.12:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
pytest -q
python -m pbrbiosphere
```

The CLI writes a baseline CSV, five scenario CSVs and plots under `results/`.

## Implemented
- Monod light, DIC and nutrient response.
- Platt P-I relative-response utility.
- Separate respiration and gross oxygen conversion utilities.
- Reduced fixed-quota biomass/DIC/N/P balances.
- RK45 integration segmented at light-dark transitions.
- Scenario runner and validation metrics (MAE, RMSE, R²).
- Source metadata for the first *S. elongatus* PCC 7942 observations.
- GitHub Actions test matrix for Python 3.10–3.12, with unique SHA-labelled runs and superseded-run cancellation.

## Not yet implemented
- Fitted organism-specific Platt parameters and direct gross photosynthesis model.
- Validated temperature response and dynamic photoacclimation.
- DIC carbonate chemistry, pH and alkalinity.
- Gas headspace and gas-liquid mass transfer.
- Variable biomass elemental composition and dissolved organic pools.
- Independent biological validation.
- Circadian regulation (PBR-03), spatial PBR physics (PBR-04), controls (PBR-05) and habitat modules (PBR-06).

## Evidence and model documentation
- `docs/PBR-02_MODEL_SPEC.md`
- `docs/PBR-02_INITIAL_EVIDENCE_REVIEW.md`
- `docs/PBR-02_VALIDATION_PROTOCOL.md`
- `docs/PBR-02_IMPLEMENTATION_STATUS.md`
- `data/parameter_register.csv`

## Safety boundary
This research simulator must not be used to size, operate or certify human oxygen supply, underwater habitats, pressure vessels or life-support systems.


### PBR-03 circadian module
- Reduced phase oscillator with separate light-on/light-off empirical PRC tables.
- Free-running, regular, shifted and irregular-light experiments.
- Morning-output proxy for analysis only; no unvalidated growth/O2 multiplier.
- KaiABC equations are not assigned to *Phaeodactylum tricornutum*.
