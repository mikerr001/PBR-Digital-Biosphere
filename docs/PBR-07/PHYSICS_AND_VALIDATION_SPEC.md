# PBR-07 — Physics, Coupling and Validation Specification
**Status:** Design baseline v0.1  
**Date:** 2026-10-31

## 1. Coordinate system and units

- Right-handed Cartesian world coordinates.
- SI base units: m, kg, s, K, mol, A.
- Temperature stored in kelvin; UI may display °C.
- Pressure stored in Pa; UI may display kPa/bar.
- Flow stored in m³/s or kg/s with density explicit.
- Irradiance stored in W/m²; photon flux density stored in µmol photons m⁻² s⁻¹. Never convert these without a declared spectrum and conversion method.
- Dissolved concentration stored in mol/m³ or kg/m³ with chemical species explicit.
- Every physical property is represented as value + unit + provenance + uncertainty + valid range.

## 2. Physical domains

The geometry/domain model must distinguish:
1. External seawater/freshwater domain.
2. Internal liquid culture domain.
3. Gas headspace domain.
4. Crop/root-zone liquid or substrate domain.
5. Internal air domain.
6. Solid structures and heat-transfer boundaries.

Interfaces between domains are explicit surfaces with transfer laws. Liquid DIC is not interchangeable with molecular dissolved CO₂; carbonate speciation is required before coupling total inorganic carbon to Henry-law CO₂ transfer.

## 3. Governing model families

The exact equations and discretizations are selected per solver tier and recorded in each run. The following are model families, not claims that a particular solver has already been implemented.

### 3.1 Fluid mechanics
For incompressible Newtonian liquid at the reduced spatial tier:
- Continuity: ∇·u = 0.
- Momentum: ρ(∂u/∂t + u·∇u) = −∇p + μ∇²u + ρg + f.
- Boundary conditions: no-slip walls; specified inlet flow/velocity; pressure outlet; explicit free-surface or gas-liquid interface treatment where modelled.
- Report Reynolds number and assumptions behind laminar/turbulent treatment.
- A reduced network model may use pressure-loss correlations, but must be labelled network/reduced-order flow, not CFD.

### 3.2 Thermal transport
- Fluid energy balance: ρcp(∂T/∂t + u·∇T) = ∇·(k∇T) + Q.
- Solid conduction: ρscp,s∂T/∂t = ∇·(ks∇T) + Qs.
- Coupling at interfaces uses a stated heat-transfer boundary model.
- Sources include lamp heat, pump heat, environmental exchange, solar absorption and biological heat only when justified.
- Reduced lumped thermal model is permitted as Tier 1.

### 3.3 Optical transport
- First implementation: spectral or band-averaged attenuation with documented assumptions.
- Beer–Lambert: I(z,λ)=I0(λ) exp(−a(λ)z) only where the assumptions are defensible.
- For scattering media, a radiative-transfer approximation is required; simple Beer–Lambert is not a full radiative-transfer solution.
- Map local irradiance/PAR to biological volume elements or compartment averages.
- Preserve spectral conversion from W/m² to PAR photon flux; do not apply a universal scalar without a spectrum.

### 3.4 Gas-liquid transfer
- Transfer flux uses a species-specific driving force and volumetric transfer coefficient, e.g. N_i = kLa_i(C_i*−C_i).
- CO₂ transfer requires carbonate speciation, pH and alkalinity model or a clearly declared molecular-CO₂-only assumption.
- O₂ transfer is separate from CO₂ transfer.
- Bubble hydrodynamics, bubble-size distribution and interfacial area are out of Tier 1 scope.

### 3.5 Structural mechanics
- Linear elastic baseline may use ∇·σ + b = 0, σ = C:ε, ε = 1/2(∇u + ∇uᵀ).
- Pressure, buoyancy, gravity, current drag and support reactions are load cases.
- Geometric nonlinearity, buckling, fatigue, fracture, joints, material degradation and external wave impacts are not implied by a linear elastic result.
- Never use a simplified stress field to certify a pressure shell or human-occupied structure.

### 3.6 Biological model coupling
- PBR-02 remains the biological ODE model; do not duplicate its equations in the CAD client.
- Inputs: compartment irradiance/PAR, temperature, mixing proxy, gas-transfer state and nutrient availability, only where the current model supports them.
- Outputs: biomass, DIC, dissolved O₂, nutrients and rates.
- PBR-03 phase/acclimation is analysis-only until organism-specific experimental parameterization supports stronger claims.
- PBR-06 resource inventories remain separate from any unsupported human physiology defaults.
- Biological source terms enter physical equations only when units and stoichiometry are explicit.

## 4. Coupling graph and variables

| Producer | Consumer | Exchanged variable | Requirement |
|---|---|---|---|
| Geometry | All solvers | domain surfaces, volumes, lengths | stable geometry snapshot |
| Fluid | Thermal | velocity field, mass flow | same mesh or conservative mapping |
| Fluid | Biology | mixing / mass-transfer proxy | model-specific mapping |
| Thermal | Biology | temperature field or volume mean | declared spatial averaging |
| Optical | Biology | PAR field or compartment average | spectrum and units explicit |
| Biology | Fluid/gas | O₂/CO₂/nutrient source rates | stoichiometry and phase explicit |
| Biology | Thermal | heat source | only if energy balance is supported |
| Structure | Geometry/solver | displacement and stress | one-way initially; mesh compatibility |
| Environment | Fluid/thermal/optical/structure | boundary conditions | scenario versioned |

## 5. Numerical controls
Every run must store:
- solver and version;
- spatial dimension and discretization;
- mesh type, element count and quality summary;
- time integrator and step size;
- nonlinear/linear solver tolerances;
- residual history and convergence state;
- conservation residuals;
- initialization and boundary conditions;
- parameter provenance and uncertainty;
- warnings and solver exit status.

Do not hide divergence, non-convergence, failed mesh generation or invalid inputs. A failed run is a failed run, not a partial success.

## 6. Verification plan

### Geometry and topology
- component dimension and unit tests;
- closed-volume and surface-normal checks;
- connected/disconnected port graph tests;
- mesh quality and domain leakage checks;
- round-trip save/reopen and STEP export tests.

### Physics
- hydrostatic pressure gradient against analytical ρgh;
- laminar pipe flow against Hagen–Poiseuille where assumptions apply;
- conduction against 1D slab analytical solution;
- transient lumped thermal response against analytical first-order response;
- Beer–Lambert attenuation against analytical values;
- structural simple bar/plate benchmark before complex pressure shells;
- mass, energy and species conservation tests.

### Coupling
- no-source/no-flux invariance;
- exchange-unit conversion tests;
- time-step refinement;
- mesh refinement where spatial solvers are used;
- one-way versus coupled run labels;
- reproducibility from frozen project snapshots.

## 7. Validation plan
Verification asks whether equations are solved correctly. Validation asks whether the model represents the real system adequately.

Validation sequence:
1. Benchmark individual solvers against analytical or published benchmark cases.
2. Calibrate only on designated calibration experiments.
3. Freeze parameters.
4. Validate against independent experiments or publications not used in fitting.
5. Report bias, MAE, RMSE, maximum error, uncertainty coverage and residual plots.
6. State the operating envelope and where validation does not apply.
7. Preserve raw observations, provenance, instrument uncertainty and exclusion rationale.

Do not randomly split time points from the same experiment into train/test sets. Hold out whole experiments or publications where possible.

## 8. Initial vertical slice
The first useful end-to-end vertical slice should be deliberately narrow:
- Parametric transparent cylindrical culture vessel with gas headspace and inlet/outlet ports.
- Add a pump and a simple connected pipe loop.
- Define liquid properties and an inlet flow rate.
- Run Tier 1 pressure-drop/network-flow and lumped thermal simulations.
- Run the existing PBR-02 ODE with a clearly defined volume-averaged PAR and temperature input.
- Visualize geometry, pipe flow arrows, temperature state, and biological time series.
- Export the project manifest, run metadata and result CSV.

This proves the complete CAD→physics request→results→visualization path before attempting 3D CFD or FEA.

## 9. Deferred capabilities
- Fully transient multiphase bubble CFD.
- Free-surface and wave-structure interaction.
- High-fidelity radiative transfer with scattering.
- Nonlinear shell buckling, fatigue and fracture.
- Fully coupled fluid-thermal-optical-biological multiphysics.
- Automated control and physical actuation.
- Any human life-support or occupancy-capacity certification.

These remain future research tasks, not hidden features.
