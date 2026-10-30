# PBR-02 Model Specification v0.2

## Purpose
Build a reproducible, evidence-traceable model of a single well-mixed algal culture. This is research software, not a life-support design.

## Organism configurations
1. Primary clock research organism: *Synechococcus elongatus* PCC 7942 (cyanobacterium).
2. Marine comparison: *Phaeodactylum tricornutum* (diatom).

Keep parameters and biological mechanisms separate. The KaiABC oscillator is specific to the *Synechococcus* research configuration unless direct evidence establishes a corresponding mechanism elsewhere.

## State vector
- X: biomass concentration, g dry weight L-1.
- C: dissolved inorganic carbon, mmol C L-1 (currently a single lumped pool).
- O: dissolved oxygen, mmol O2 L-1.
- N: available nitrogen, mmol N L-1.
- P: available phosphorus, mmol P L-1.

## Reduced equations
Light saturation: fI = I / (KI + I)

Monod nutrient limitation:
fN = N / (KN + N); fP = P / (KP + P); fC = C / (KC + C)

Growth:
mu = mu_max * fI * min(fN, fP) * fC * fT
dX/dt = (mu - rd) X

Carbon and oxygen rates:
C_fixed = mu X Y_C
O_consumed = m_O2 X
C_respired = RQ * O_consumed
O_gross = PQ * C_fixed

dC/dt = -C_fixed + C_respired
dO/dt = O_gross - O_consumed

RQ is the respiratory quotient (mol CO2 released / mol O2 consumed). PQ is the photosynthetic quotient (mol O2 evolved / mol inorganic carbon fixed). Neither is universal; both depend on organism, substrate and conditions and must be sourced or measured. Starter defaults of 1.0 are software placeholders only.

Nutrient uptake:
dN/dt = -qN mu X
dP/dt = -qP mu X

## Critical limitations
- Starter defaults are illustrative software-test values, not measured organism-specific parameters.
- Temperature response is a neutral placeholder (factor 1), not a validated thermal response.
- DIC is one lumped pool; pH, alkalinity, bicarbonate/carbonate speciation and CO2 hydration are absent.
- Fixed biomass elemental quotas and constant PQ/RQ are placeholders requiring measured data.
- No gas headspace or gas-liquid transfer.
- No photoinhibition, acclimation, spatial light attenuation, mixing, thermal balance or clock module.
- No external validation has yet been completed.
- The simplified model is not a closed elemental inventory: biomass elemental pools and all relevant dissolved/gas pools are not yet represented explicitly.

## Development sequence
1. Replace placeholder values with traceable experimental data and uncertainty.
2. Add organism-specific gross photosynthesis and respiration response functions.
3. Represent biomass C/N/P composition and elemental inventories explicitly.
4. Add DIC carbonate chemistry, pH and alkalinity.
5. Add gas headspace and kLa transfer terms with equal-and-opposite phase fluxes.
6. Verify mass conservation and validate against independent experiments.
7. Add acclimation and circadian regulation only after baseline validation.

## Validation gates
- Dimensional consistency.
- Zero biomass gives zero biomass-dependent rates.
- Zero light gives zero light-driven gross photosynthesis.
- Carbon, oxygen, nitrogen and phosphorus inventories close after all relevant pools are represented.
- Separate calibration and validation datasets.
- Report MAE/RMSE, residual plots and uncertainty against independent observations.

## Safety boundary
Do not use this software to size, operate or certify human oxygen supply, underwater habitats, pressure vessels or life-support systems.
