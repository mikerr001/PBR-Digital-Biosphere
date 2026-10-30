# PBR-02 / PBR-04 Coupled Integration Specification v0.1

## Purpose
This milestone joins the reduced biological culture model (PBR-02) to selected physical reactor processes (PBR-04) without pretending every state is already chemically compatible. It is a research simulation interface, not a validated digital twin or life-support controller.

## Coupled states and units
| State | Unit | Source |
|---|---|---|
| Biomass X | gDW/L | PBR-02 |
| Lumped DIC | mmol C/L | PBR-02 |
| Dissolved O2 | mmol O2/L | PBR-02 + PBR-04 transfer |
| Dissolved N, P | mmol element/L | PBR-02 |
| Headspace O2 | mmol O2 | PBR-04 |
| Liquid temperature | °C | PBR-04 |

Time is days. PAR is µmol photons m⁻² s⁻¹. O2 transfer is mmol/day and is divided by liquid volume for the dissolved concentration derivative.

## Implemented feedbacks
1. Biomass attenuates incident PAR through Beer–Lambert optics.
2. Path-average PAR drives the PBR-02 Monod light limitation.
3. PBR-02 biological O2 production and respiration change dissolved O2.
4. PBR-04 gas transfer redistributes O2 between liquid and headspace.
5. PBR-04 thermal balance changes liquid temperature; this is passed to PBR-02, whose temperature response remains a neutral placeholder.

## Deliberately disconnected carbon pathway
PBR-02 DIC is a lumped dissolved inorganic carbon pool. PBR-04 Henry-law CO2 is molecular dissolved CO2 only. They are not interchangeable: bicarbonate and carbonate fractions depend on pH, alkalinity, temperature and medium chemistry. This integration therefore does not apply PBR-04 CO2 transfer to PBR-02 DIC and does not claim a closed carbon-gas balance. A later carbonate-system milestone must introduce total alkalinity, temperature-dependent equilibrium constants, CO2(aq)/HCO3-/CO3-- speciation and measured gas transfer before enabling CO2 coupling.

## Safeguards
- Reject geometry when calculated panel volume differs from declared liquid volume by more than the configured tolerance (default 5%).
- Reject non-finite/negative physical parameters and materially negative integrated inventories.
- Segment integration at day/night discontinuities.
- Report path-average PAR, O2 transfer, total liquid-plus-headspace O2 inventory and geometry closure.
- No hidden parameter fitting or interpolation of experimental measurements.

## Validation matrix
| Subsystem | Required independent measurement | Status |
|---|---|---|
| Geometry | Dimensions and gravimetric fill volume | Software-only |
| Optics | Depth-resolved PAR across biomass and path lengths | Not started |
| Biology | Biomass time series calibrated to dry weight | Not started |
| O2 evolution | Dissolved plus off-gas oxygen balance | Not started |
| O2 kLa | Dynamic gassing/re-aeration transient with mixing metadata | Not started |
| Thermal | Liquid and ambient temperature transients | Not started |
| Carbon | pH, alkalinity, DIC and dissolved molecular CO2 | Blocked by carbonate model |
| Mixing | Spatial tracer or DO/temperature gradients | Not started |
| Integrated model | Blind holdout against synchronized independent dataset | Blocked by subsystem validation |

## Known limitations
- PBR-02 growth, respiration, photosynthetic and quota parameters remain demo or incompletely sourced values.
- Gross oxygen is inferred from reduced carbon bookkeeping, not independently fitted gross O2 evolution.
- PBR-02 temperature response is 1.0; temperature does not yet change biological kinetics.
- Carbonate chemistry, CO2 gas transfer, pH/alkalinity, variable quotas and dissolved organic pools are absent.
- Optics are one-dimensional Beer–Lambert; scattering, spectrum, photoinhibition and dynamic mixing are absent.
- Mixing helper is not integrated into the dynamic state.
- No independent experimental validation has been completed.
- Not suitable for human oxygen supply, habitat operation or safety-critical control.

## Exit criteria before PBR-05
1. Populate a traceable parameter register for one organism and one defined medium/reactor configuration.
2. Validate growth and O2 trajectories against independent measurements, with uncertainty and predeclared error metrics.
3. Validate optical attenuation, O2 kLa and thermal response against independent reactor measurements.
4. Implement and validate carbonate speciation before enabling CO2 gas transfer.
5. Establish model discrepancy bounds and explicit invalid/degraded operating regions.
