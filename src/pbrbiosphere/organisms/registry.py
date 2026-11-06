"""Versioned organism catalogue with explicit model-readiness gates.

Evidence profiles and executable kinetic parameterisations are deliberately
separate. A species may have literature observations while still lacking the
complete, condition-matched parameter set needed by the simulator.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class OrganismProfile:
    organism_id: str
    display_name: str
    strain: str
    group: str
    evidence_module: Optional[str]
    kinetic_model_id: Optional[str]
    model_status: str
    executable: bool
    missing_parameters: tuple[str, ...]
    limitations: tuple[str, ...]


_PROFILES = {
    "synechococcus_elongatus_pcc7942": OrganismProfile(
        organism_id="synechococcus_elongatus_pcc7942",
        display_name="Synechococcus elongatus",
        strain="PCC 7942",
        group="cyanobacterium",
        evidence_module="pbrbiosphere.organisms.synechococcus_7942",
        kinetic_model_id=None,
        model_status="EVIDENCE_PROFILE_ONLY",
        executable=False,
        missing_parameters=(
            "condition-matched light response and photoinhibition",
            "elemental biomass quotas and uncertainty",
            "photosynthetic and respiratory quotients",
            "temperature response and acclimation",
            "strain/medium-specific nutrient kinetics",
        ),
        limitations=(
            "Published observations are preserved at their original measurement basis.",
            "No universal species parameter set is inferred from a small number of observations.",
        ),
    ),
    "phaeodactylum_tricornutum": OrganismProfile(
        organism_id="phaeodactylum_tricornutum",
        display_name="Phaeodactylum tricornutum",
        strain="strain-specific; not yet selected",
        group="diatom",
        evidence_module="pbrbiosphere.organisms.phaeodactylum",
        kinetic_model_id=None,
        model_status="EVIDENCE_PROFILE_ONLY",
        executable=False,
        missing_parameters=(
            "strain-resolved growth/light response",
            "carbon-concentrating and carbonate response",
            "elemental quotas",
            "gross photosynthesis and respiration on compatible bases",
            "temperature, salinity and nutrient response",
        ),
        limitations=(
            "No numerical defaults are assigned across different strains or assay bases.",
            "The Synechococcus KaiABC circadian model is not transferred to this diatom.",
        ),
    ),
    "generic_reduced_demo": OrganismProfile(
        organism_id="generic_reduced_demo",
        display_name="Generic reduced-model demonstration",
        strain="not applicable",
        group="non-organism-specific",
        evidence_module=None,
        kinetic_model_id="pbr02_monod_liebig_demo",
        model_status="ILLUSTRATIVE_UNCALIBRATED",
        executable=True,
        missing_parameters=(),
        limitations=(
            "Uses software demonstration defaults, not an organism-specific calibration.",
            "Not suitable for species prediction or scale-up claims.",
        ),
    ),
}


def list_organisms() -> tuple[OrganismProfile, ...]:
    """Return the immutable organism catalogue in stable ID order."""
    return tuple(_PROFILES[key] for key in sorted(_PROFILES))


def get_organism(organism_id: str) -> OrganismProfile:
    """Return one profile or raise a useful error for unknown identifiers."""
    try:
        return _PROFILES[organism_id]
    except KeyError as exc:
        raise ValueError(
            f"Unknown organism profile {organism_id!r}. Available profiles: " + ", ".join(sorted(_PROFILES))
        ) from exc


def require_executable_organism(organism_id: str) -> OrganismProfile:
    """Fail closed when the selected organism lacks a complete kinetic model."""
    profile = get_organism(organism_id)
    if not profile.executable:
        missing = "; ".join(profile.missing_parameters)
        raise NotImplementedError(
            f"{profile.display_name} is currently {profile.model_status}; "
            f"do not run generic kinetics as if species-specific. Missing: {missing}"
        )
    return profile
