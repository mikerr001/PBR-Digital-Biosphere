# PBR-02 Model Specification v0.3

## Purpose and boundary
A reduced, well-mixed, single-liquid-culture physiology model. This is a research simulator, not a life-support controller. It does not yet model a gas headspace, gas transfer, carbonate speciation, reactor spatial gradients or organism-specific acclimation dynamics.

## Organisms
- Primary clock research configuration: *Synechococcus elongatus* PCC 7942 (cyanobacterium).
- Marine comparison: *Phaeodactylum tricornutum* (diatom).
Keep their parameter sets separate. KaiABC is not assigned to *P. tricornutum*.

## State vector
| State | Unit | Description |
|---|---|---|
| X | gDW L-1 | Suspended dry biomass |
| C | mmol C L-1 | Lumped dissolved inorganic carbon |
| O | mmol O2 L-1 | Dissolved oxygen |
| N | mmol N L-1 | Dissolved available nitrogen |
| P | mmol P L-1 | Dissolved available phosphorus |

## Kinetics
Light saturation:
fI = I / (KI + I)

Nutrient limitation:
fN = N / (KN + N); fP = P / (KP + P)

Liebig co-limitation:
fNP = min(fN, fP)

Lumped DIC limitation:
fC = C / (KC + C)

Temperature response:
fT = 1 in the current software scaffold. This is explicitly a placeholder, not a thermal response model.

Potential specific growth:
mu = mu_max * fI * fNP * fC * fT

Biomass:
dX/dt = (mu - rd) X

## Reduced elemental bookkeeping
Fixed biomass quotas:
qC [mmol C/gDW], qN [mmol N/gDW], qP [mmol P/gDW].

Dissolved carbon:
dC/dt = -qC * dX/dt

Dissolved nitrogen:
dN/dt = -qN * dX/dt

Dissolved phosphorus:
dP/dt = -qP * dX/dt

This assumes fixed biomass elemental composition and complete return of biomass-bound elements on the modelled decay term. It gives exact inventory identities C + qC X, N + qN X and P + qP X in this reduced model. It does not represent dissolved organic pools, excretion, luxury uptake, variable quotas, or incomplete remineralisation.

Respiration:
R_O2 = m_O2 X
R_C = RQ * R_O2

Gross carbon fixation is closed algebraically as:
F_C,gross = max(0, qC * dX/dt + R_C)

Gross oxygen evolution:
P_O2,gross = PQ * F_C,gross

Dissolved oxygen:
dO/dt = P_O2,gross - R_O2

RQ = mol C released per mol O2 consumed; PQ = mol O2 evolved per mol C fixed. These are organism-, substrate- and condition-dependent. The code defaults are demonstration assumptions only and must be replaced with sourced values.

## Light response options
- Monod light saturation is currently used to drive potential growth.
- A Platt P-I function is provided as a standalone dimensionless response utility. It is not yet coupled to the model or parameter-fitted.
- Spectral light quality and acclimation state are not represented yet.

## Numerical method
SciPy solve_ivp with RK45, strict tolerances and integration segmented at square-wave light transitions. The current solver checks negative excursions and returns a fixed output grid.

## Known limitations
1. Starter parameter defaults are illustrative software values, not validated organism parameters.
2. Fixed biomass C/N/P quotas are a simplification.
3. The carbon and nutrient inventory closures depend on fixed quotas and complete decay return.
4. Oxygen has no gas-phase inventory, kLa transfer or atmospheric boundary.
5. No carbonate equilibrium, pH, alkalinity or bicarbonate/carbonate speciation.
6. No photoinhibition coupling, spectrum, acclimation state, cell-cycle or circadian oscillator.
7. Temperature response is a neutral placeholder.
8. No independent biological validation has been completed.
9. No human oxygen supply, habitat, pressure-vessel or life-support suitability can be inferred.

## Next development gates
1. Populate organism-specific parameter sets with direct measurements and condition metadata.
2. Couple fitted photosynthesis-irradiance response to gross carbon fixation and oxygen evolution.
3. Replace fixed quotas where literature supports variable composition.
4. Add gas headspace, gas transfer and carbonate chemistry.
5. Validate separately against independent growth and oxygen data.
6. Add dynamic photoacclimation and clock biology only after baseline validation.
