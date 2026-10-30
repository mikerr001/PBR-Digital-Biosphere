# PBR Digital Biosphere
Research codebase for a mechanistic algal photobioreactor and regenerative-habitat digital twin.

## Current milestone: PBR-02 / PBR-04 integration
The first dynamic integration now couples biomass-dependent Beer–Lambert attenuation to the PBR-02 growth model, and couples biological dissolved-oxygen sources/sinks to PBR-04 liquid/headspace oxygen transfer. The lumped thermal state is also integrated. This is a software integration milestone, not experimental validation.

**Important carbon boundary:** PBR-02 stores lumped dissolved inorganic carbon (DIC), while PBR-04's Henry-law calculation represents molecular dissolved CO2 only. The two are not interchangeable. CO2 gas transfer is intentionally disconnected until carbonate speciation and alkalinity are implemented and validated. See docs/PBR-02_PBR-04_INTEGRATION_SPEC.md and docs/PBR-02_PBR-04_VALIDATION_MATRIX.csv.

## Scientific guardrails
- Simulated values are not experimental measurements.
- Keep *Synechococcus elongatus* PCC 7942 and *Phaeodactylum tricornutum* evidence separate.
- Do not transfer KaiABC equations to *P. tricornutum*.
- Separate gross oxygen evolution from oxygen consumption.
- Preserve measurement basis (per cell, chlorophyll, protein or dry biomass).
- PBR-02 fixed-quota balances are reduced assumptions, not a complete reactor inventory.
- PBR-02 temperature response is currently a neutral placeholder; thermal feedback does not yet alter growth kinetics.
- This software is not a human life-support controller or safety-certified design tool.

## Install and test
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m pbrbiosphere
```
Python 3.10–3.12 are supported.

## Implemented
- PBR-02 reduced biomass, DIC, O2, N and P culture model.
- PBR-03 reduced KaiABC phase/entrainment scaffold and acclimation foundations.
- PBR-04 flat-panel geometry, 1-D optics, two-phase gas transfer, lumped thermal rates and a two-compartment exchange helper.
- PBR-02/PBR-04 dynamic coupling for path-average PAR, dissolved/headspace O2 and liquid temperature.
- Integration tests for phase-inventory conservation, optical attenuation and geometry closure.
- GitHub Actions verification matrix for Python 3.10–3.12.

## Remaining before PBR-05
- Source-fitted biological and reactor parameters.
- Independent validation of growth, oxygen, optics, O2 kLa and thermal transients.
- Carbonate chemistry, pH, alkalinity and validated CO2 transfer.
- Dynamic spatial mixing and measured hydrodynamics.
- Explicit model-discrepancy bounds and degraded/invalid operating regions.

## Safety
Research simulator only. Do not use it to size, operate or certify human oxygen supply, underwater habitats or pressure vessels.
