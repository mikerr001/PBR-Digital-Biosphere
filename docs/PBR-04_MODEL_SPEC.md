# PBR-04 Photobioreactor Digital Twin — Model Specification v0.1
## Scope
PBR-04 introduces physical reactor submodels: flat-panel geometry, one-dimensional light attenuation, two-phase dissolved/headspace gas exchange and a lumped liquid thermal balance. An instantaneous assembly function exposes these calculations together. This version is not yet dynamically coupled to PBR-02 biological source terms.

## Geometry
For frontal dimensions width w and height h, frontal area A=wh. Liquid optical path is L, declared liquid volume V_L, and headspace volume V_G. Calculated geometric volume is A L (m³), converted to litres. The illumination flag supports one or two illuminated faces. Volume closure is reported, never silently forced.

## Optical field
A one-dimensional Beer–Lambert approximation is used:
I(z)=I₀ exp[-(k_X X+k_b)z].
Biomass X in gDW/L is numerically equal to kgDW/m³. Therefore k_X is specified in m²/kgDW; k_b is m⁻¹. The function returns depth-resolved irradiance, path average and transmitted fraction. This approximation omits scattering, spectral effects, bubbles, photoinhibition and non-collimated illumination.

## Gas-liquid exchange
Separate dissolved O₂ and molecular dissolved CO₂ concentrations are paired with headspace inventories. Ideal-gas partial pressure is computed from gas inventory, headspace volume and temperature. Henry equilibrium is C*=H p. Signed liquid-to-gas transfer is:
N = kLa (C_L-C*) V_L.
N is mmol/day; positive means liquid to gas, negative means absorption. The corresponding gas inventory derivative is +N and liquid inventory derivative is -N. Transfer alone therefore conserves combined phase inventory. kLa and Henry constants must be measured or sourced for the relevant reactor, medium, salinity and temperature. CO₂ here is molecular dissolved CO₂ only, not total DIC; carbonate speciation, pH and alkalinity are not implemented.

## Thermal balance
The lumped liquid temperature rate is:
dT/dt = (Q_solar+Q_metabolic-Q_loss)/(rho V_L c_p).
Solar heat is incident irradiance × illuminated area × absorbed fraction; heat loss is UA(T-T_ambient). W is converted to J/day, yielding K/day. Wall thermal mass, evaporation, latent heat, active cooling and spatial gradients are omitted.

## Mixing and coupling
A two-compartment exchange helper accepts a measured mixing-time constant and returns signed exchange between equal-volume compartments. It is not integrated into a time-dependent spatial reactor state. CFD, bubble hydrodynamics and circulation remain unimplemented. PBR-04 does not calculate photosynthesis, biomass growth, oxygen production or carbon fixation. It is not yet connected to PBR-02. Path-average irradiance must not be treated as a validated replacement for the existing PBR-02 light forcing.

## Parameter status
The software has no asserted reactor-specific default for attenuation, kLa, Henry constants, heat absorption or UA. Unit-test values are synthetic and verify equations, signs and conversions only.

## Validation gates
1. Measure internal geometry and fill/headspace volumes; set a predeclared volume-closure tolerance.
2. Measure depth-resolved PAR over biomass and path-length series; fit k_X and k_b with uncertainty.
3. Measure O₂ and CO₂ kLa separately with gas flow, sparger, mixing, medium and temperature recorded.
4. Measure dissolved molecular CO₂ and headspace CO₂; do not substitute total DIC without speciation.
5. Calibrate absorbed heat and UA against transient temperature data.
6. Measure mixing time and spatial gradients before selecting a well-mixed assumption.
7. Couple to PBR-02 only after source/sink units, inventories and independent validation datasets are reconciled.

## Safety
Research software only. It must not be used to size or operate human oxygen supply, certify a habitat or design pressure-containing hardware.
