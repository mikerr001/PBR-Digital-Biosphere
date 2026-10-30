# PBR Digital Biosphere
Research codebase for a mechanistic algal photobioreactor and regenerative-habitat digital twin.

## Current milestone: PBR-04A scientific calibration framework
PBR-04A adds a carbonate-equilibrium prototype, parameter-provenance checks, experimental-data conventions and independent holdout comparison metrics. This is a scientific-methods/software milestone, not experimental validation.

**Carbon boundary:** PBR-02 stores total dissolved inorganic carbon (DIC); PBR-04 Henry-law transfer uses molecular dissolved CO2. The new speciation routine estimates molecular CO2 from DIC and alkalinity under a carbonate-only freshwater approximation. It is not yet suitable for direct coupling to BG-11 or marine culture because non-carbonate alkalinity, ionic-strength effects and medium-specific constants have not been characterised.

## Scientific guardrails
- Simulated values are not experimental measurements.
- Keep Synechococcus elongatus PCC 7942 and Phaeodactylum tricornutum evidence separate.
- Do not transfer KaiABC equations to P. tricornutum.
- Separate gross oxygen evolution from oxygen consumption.
- Preserve measurement basis (per cell, chlorophyll, protein or dry biomass).
- PBR-02 fixed-quota balances are reduced assumptions, not a complete reactor inventory.
- PBR-02 temperature response remains a neutral placeholder.
- A software test pass is not biological or physical validation.
- This software is not a human life-support controller or safety-certified design tool.

## Install and test
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m pbrbiosphere

Python 3.10–3.12 are supported.

## Implemented
- PBR-02 reduced biomass, DIC, O2, N and P culture model.
- PBR-03 reduced KaiABC phase/entrainment scaffold and acclimation foundations.
- PBR-04 flat-panel geometry, 1-D optics, two-phase gas transfer, lumped thermal rates and a two-compartment exchange helper.
- PBR-02/PBR-04 dynamic coupling for path-average PAR, dissolved/headspace O2 and liquid temperature.
- PBR-05 deterministic supervisory recommendations with sensor-quality fail-closed behaviour and operator confirmation; automatic actuation disabled.
- PBR-04A carbonate speciation prototype, parameter-register audit utility, data schema and independent holdout metrics.

## Remaining before habitat-scale expansion
- Audit current parameter records and verify source DOI, strain, units and conditions.
- Add medium-specific alkalinity contributors and validate carbonate speciation.
- Fit and independently validate growth, gross/net O2, O2/CO2 kLa, optics and thermal parameters.
- Establish uncertainty and model-discrepancy bounds.
- Integrate CO2 gas transfer only after chemistry is validated.

## Safety
Research simulator only. Do not use it to size, operate or certify human oxygen supply, underwater habitats or pressure vessels.
