# PBR-04A Experimental Data Schema
Raw observations are immutable and separate from simulations. One row represents one measured observation at one time point or steady-state condition.

Required metadata: dataset_id, source_doi_or_url, source_location, extraction_date, organism, strain, medium, temperature_C, salinity, pH, cultivation_mode, light_spectrum, photoperiod_h, incident_PAR_umol_m2_s, measured_PAR_umol_m2_s, reactor_type, optical_path_m, working_volume_L, mixing_description, gas_composition, gas_flow_rate, time_s, variable, value, unit, normalisation_basis, replicate_n, uncertainty_type, uncertainty_value, method, detection_limit, exclusions and transformation.

Use empty values for unavailable metadata; never infer them. Preserve original source value/unit when converting. Derived datasets must carry transformation version and parent dataset ID. Suggested variables: biomass_concentration, gross_O2_evolution, net_O2_accumulation, dark_O2_consumption, DIC, total_alkalinity, pH, dissolved_CO2, dissolved_O2, PAR, temperature, kLa_O2, kLa_CO2.
