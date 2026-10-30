# PBR Digital Biosphere

Research codebase for a mechanistic photobioreactor and regenerative-habitat digital twin.

## Current milestone: PBR-02

PBR-02 begins with a transparent, well-mixed algal-culture model. The first implementation is deliberately a **scaffold**: equations and units are explicit, but organism-specific kinetic values are not claimed to be validated. Replace the illustrative configuration only with traceable measurements from the parameter register.

### Scientific guardrails
- Never interpret simulated values as experimental measurements.
- Keep *Synechococcus elongatus* PCC 7942 and *Phaeodactylum tricornutum* parameterisations separate.
- Do not apply the KaiABC oscillator equations to *P. tricornutum*.
- Distinguish gross photosynthetic oxygen evolution, biological oxygen consumption, and gas-liquid transfer.
- Track carbon, oxygen, nitrogen and phosphorus inventories consistently.
- A well-mixed model is not a validated life-support system and must not be used to support human life-support decisions.

## Quick start (Python 3.10+)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
pytest
python -m pbrbiosphere
```

The simulator writes CSV output to `results/` and plots to `results/figures/`.

## Model boundary (v0.1)

The initial model includes biomass, dissolved inorganic carbon (DIC), dissolved oxygen, dissolved nitrogen and dissolved phosphorus in one idealised, well-mixed liquid culture. Light and temperature are externally prescribed. Gas transfer, pH/speciation, spatial light fields, crops, humans, underwater pressure and habitat controls are not yet implemented.

## Evidence classes
- E1: direct experimental measurement
- E2: value derived from published measurements
- E3: explicit modelling assumption
- E4: hypothetical research parameter
- E5: independently validated model result

Every numerical parameter must include organism/strain, units, experimental conditions, source and uncertainty. Missing values stay missing.

## Project layout
See `docs/PBR-02_MODEL_SPEC.md` and `data/parameter_register.csv`.

## Safety
This is research software, not a certified bioreactor controller, oxygen generator, pressure-vessel design tool or human life-support system.
