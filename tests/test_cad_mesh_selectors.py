from pbrbiosphere.mesh_selectors import classify_surface_bbox


def test_planar_selector_matches_exact_plane():
    assert classify_surface_bbox((0, 0, 0, 0, 1, 1),
                                 {"axis": "x", "coordinate_m": 0}, 1e-6)


def test_planar_selector_rejects_nonmatching_plane():
    assert not classify_surface_bbox((0.1, 0, 0, 0.2, 1, 1),
                                     {"axis": "x", "coordinate_m": 0}, 1e-6)


def test_selector_checks_both_bbox_faces_are_on_plane():
    assert not classify_surface_bbox((0, 0, 0, 0.01, 1, 1),
                                     {"axis": "x", "coordinate_m": 0}, 1e-6)
