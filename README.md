# PBR Digital Biosphere
Research codebase for a mechanistic algal photobioreactor and regenerative-habitat digital twin.

## Current milestone: PBR-04
PBR-04 adds flat-panel geometry, depth-resolved Beer–Lambert attenuation, separate dissolved/headspace O₂ and molecular CO₂ exchange, and a lumped thermal balance. The physical modules are executable and tested but are not dynamically coupled to PBR-02 biological production or experimentally validated. See the PBR-04 model specification, implementation status and validation plan.

## Scientific guardrails
- Simulated values are not experimental measurements.
- Keep *Synechococcus elongatus* PCC 7942 and *Phaeodactylum tricornutum* evidence separate.
- Do not transfer KaiABC equations to *P. tricornutum*.
- Separate gross oxygen evolution from oxygen consumption.
- Preserve measurement basis (per cell, chlorophyll, protein or dry biomass).
- PBR-02 fixed-quota balances are reduced assumptions, not a complete reactor inventory.
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
- PBR-02 reduced biomass, DIC, O₂, N and P culture model.
- PBR-03 reduced KaiABC phase/entrainment scaffold and independent acclimation state.
- PBR-04 flat-panel geometry, 1-D optics, two-phase gas transfer and lumped thermal rate models.
- GitHub Actions verification matrix for Python 3.10–3.12.

## Remaining
- Evidence-fitted biology and independent validation.
- Carbonate chemistry, pH and alkalinity.
- CFD/hydrodynamics and experimentally measured mixing.
- Dynamic PBR-02/PBR-04 coupling and spatial photosynthesis.
- PBR-05 predictive control and PBR-06 habitat resource balances.

## Safety
Research simulator only. Do not use it to size, operate or certify human oxygen supply, underwater habitats or pressure vessels.
