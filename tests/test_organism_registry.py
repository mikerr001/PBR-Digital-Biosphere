import pytest

from pbrbiosphere.organisms.registry import (
    get_organism, list_organisms, require_executable_organism,
)


def test_multi_organism_catalogue_contains_cyanobacterium_and_diatom():
    profiles = {item.organism_id: item for item in list_organisms()}
    assert "synechococcus_elongatus_pcc7942" in profiles
    assert "phaeodactylum_tricornutum" in profiles
    assert profiles["synechococcus_elongatus_pcc7942"].group == "cyanobacterium"
    assert profiles["phaeodactylum_tricornutum"].group == "diatom"


def test_evidence_profile_is_not_mistaken_for_executable_model():
    for organism_id in (
        "synechococcus_elongatus_pcc7942",
        "phaeodactylum_tricornutum",
    ):
        profile = get_organism(organism_id)
        assert profile.executable is False
        with pytest.raises(NotImplementedError, match="not run generic kinetics"):
            require_executable_organism(organism_id)


def test_generic_demo_is_explicitly_illustrative():
    profile = require_executable_organism("generic_reduced_demo")
    assert profile.executable is True
    assert profile.model_status == "ILLUSTRATIVE_UNCALIBRATED"


def test_unknown_organism_fails_with_available_ids():
    with pytest.raises(ValueError, match="Available"):
        get_organism("made_up_alga")
