# PBR-02 Model Specification v0.1

## Purpose
Build a reproducible, evidence-traceable model of a single well-mixed algal culture. This is a research model, not a life-support design.

## Organism configurations
1. Primary clock research organism: *Synechococcus elongatus* PCC 7942 (cyanobacterium).
2. Marine comparison: *Phaeodactylum tricornutum* (diatom).

Their parameters and biological mechanisms remain separate. The KaiABC oscillator belongs only in the *Synechococcus* configuration unless direct evidence supports another organism's clock mechanism.

## State vector
- X: biomass concentration, g dry weight L-1.
- C: dissolved inorganic carbon, mmol C L-1.
- O: dissolved oxygen, mmol O2 L-1.
- N: available nitrogen, mmol N L-1.
- P: available phosphorus, mmol P L-1.

## Initial equations
Light saturation:
fI = I / (KI + I)

Monod nutrient limitation:
fN = N / (KN + N); fP = P / (KP + P)

DIC limitation (temporary simplification):
fC = C / (KC + C)

Growth:
mu = mu_max * fI * min(fN, fP) * fC * fT
dX/dt = (mu - rd) X

Carbon and oxygen:
Rfix = mu X Y_C
Rresp = m_O2 X
dC/dt = -Rfix + Rresp,C
dO/dt = P_O2,gross - R_O2,resp

In the starter implementation, carbon respiration is provisionally set equal to oxygen respiration using a one-to-one molar assumption. This is not generally valid and must be replaced by a measured respiratory quotient and explicit carbon/oxygen stoichiometry.

Nutrient uptake:
dN/dt = -qN mu X
dP/dt = -qP mu X

## Critical model limitations
- The current code uses illustrative defaults solely to test software plumbing. They are not organism-specific measured parameters.
- Temperature response is a neutral placeholder (factor 1), not a validated thermal response.
- DIC is represented as one pool; pH, alkalinity, bicarbonate/carbonate speciation and CO2 hydration are absent.
- The provisional 1:1 carbon fixation-to-oxygen ratio is not a universal biological law.
- No gas phase or gas-liquid transfer is implemented.
- No photoinhibition, acclimation, spatial light attenuation, mixing, thermal balance or cell-cycle/clock module.
- Nutrient uptake stoichiometry is illustrative.
- The model does not yet conserve a fully closed elemental inventory because carbon/oxygen stoichiometry is provisional and biomass elemental composition is simplified.

## Development sequence
1. Replace placeholder parameter values with traceable experimental data.
2. Implement gross photosynthesis and respiration as separately parameterised rates.
3. Implement explicit biomass C/N/P composition and elemental balances.
4. Add DIC carbonate chemistry and pH/alkalinity state.
5. Add gas headspace and kLa transfer terms with equal-and-opposite phase fluxes.
6. Fit and validate against independent experiments.
7. Only then add acclimation and circadian regulation.

## Validation gates
- Units/dimensional consistency.
- Non-negative state handling without silently hiding material solver errors.
- Zero biomass gives zero biomass-dependent rates.
- Zero light gives zero light-driven gross photosynthesis.
- Carbon, oxygen, nitrogen and phosphorus inventories close within numerical tolerance after all relevant pools are represented.
- Parameter and validation datasets are separated.
- Report MAE/RMSE and residual plots against independent experimental observations.

## Safety boundary
Do not use this software to size, operate or certify human oxygen supply, underwater habitats, pressure vessels or life-support systems.
