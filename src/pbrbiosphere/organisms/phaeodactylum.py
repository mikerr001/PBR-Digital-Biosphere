"""Evidence metadata for Phaeodactylum tricornutum.

No universal numerical parameter set is supplied. Published measurements vary
by strain, spectral quality, temperature, carbon supply and normalisation basis.
"""
ORGANISM = "Phaeodactylum tricornutum"
CLOCK_MODEL = None  # Do not transfer the Synechococcus KaiABC model.
EVIDENCE_SOURCES = {
    "blue_light_high_light_acclimation": "10.1093/jxb/ers340",
    "carbon_limitation_photon_flux_oxygen_assays": "10.3389/fpls.2019.00471",
}
PARAMETER_STATUS = "incomplete: extract strain-specific values and assay bases before simulation"
