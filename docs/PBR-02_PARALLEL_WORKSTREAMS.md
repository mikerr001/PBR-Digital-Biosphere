# PBR-02 Parallel Workstream Register

Status: initiated. This is a coordinated work plan, not a claim that autonomous independent agents were spawned.

## WS-01 — Organism physiology and evidence extraction
Scope: *Synechococcus elongatus* PCC 7942 and *Phaeodactylum tricornutum* kept as separate parameter sets.
Deliverables: evidence table, condition metadata, source DOI, uncertainty, evidence gaps.
Initial finding: Broddrick et al. (2019), DOI 10.1016/j.ymben.2018.11.001, reports *S. elongatus* growth and photosynthetic/respiration measurements under 60 and 600 µmol photons m-2 s-1 after 72 h acclimation at 30°C in BG-11. Growth rates: 0.047 ± 0.004 h-1 (low light) and 0.081 ± 0.015 h-1 (high light). Dark respiration: 0.15 and 0.41 mmol O2 gDW-1 h-1, respectively. Preserve original units and condition dependence.

## WS-02 — Photosynthesis and light-response model
Scope: irradiance response, gross oxygen evolution, photoinhibition, spectral effects and photoacclimation.
Deliverables: model comparison, coefficient extraction with units, limits of applicability.
Initial finding: Broddrick et al. fit a Platt photosynthesis-irradiance curve to measured oxygen evolution. The article's table reports cell-specific rates and photon fluxes; these are not directly interchangeable with biomass-specific rates without documented conversion. *P. tricornutum* light quality matters: Schellenberger Costa et al. (2013), DOI 10.1093/jxb/ers340, reports blue-light-dependent high-light acclimation and photoprotection.

## WS-03 — Respiration, carbon and elemental balances
Scope: separate gross photosynthesis, respiration, carbon fixation, biomass C/N/P quotas, dissolved inorganic carbon and gas transfer.
Deliverables: stoichiometric audit, unit-checked flux equations, unresolved measurements list.
Initial finding: never infer a universal 1:1 photosynthetic quotient or respiratory quotient. Broddrick et al. reports oxygen dark respiration for *S. elongatus* in mmol O2 gDW-1 h-1. For *P. tricornutum*, Heydarizadeh et al. (2019), DOI 10.3389/fpls.2019.00471, measured light oxygen evolution and dark respiration at 21°C and calculated gross photosynthesis assuming respiration in light equalled dark respiration; this assumption must be retained in metadata.

## WS-04 — Numerical simulation engineering
Scope: model state vector, ODE integration, parameter injection, reproducibility, solver diagnostics and scenario API.
Deliverables: modular implementation, documented interfaces, deterministic scenario runner.
Rule: no biological placeholder may be silently promoted to a measured organism parameter.

## WS-05 — Verification, validation and uncertainty
Scope: unit/dimensional checks, conservation tests, limiting cases, calibration/validation separation, residuals and sensitivity.
Deliverables: automated tests, validation data format, MAE/RMSE and uncertainty reporting.
Rule: validation must use independent observations not used for parameter fitting.

## WS-06 — Integration and technical documentation
Scope: reconcile variable names, units, parameter provenance, interfaces and limitations; integrate only after scientific review.
Deliverables: PBR-02 integrated model, model card, reproducibility instructions and milestone report.

## Integration gates
1. All rate units are explicit and mutually consistent.
2. Oxygen gross evolution and oxygen consumption are separate fluxes.
3. Carbon fixation and respiratory carbon release are distinct fluxes with measured or explicitly assumed stoichiometry.
4. Biomass elemental composition is represented before claiming closed C/N/P balances.
5. Gas-liquid transfer appears as equal-and-opposite liquid and gas phase fluxes.
6. Organism-specific parameters never cross species boundaries without evidence.
7. No life-support suitability claim is made.
