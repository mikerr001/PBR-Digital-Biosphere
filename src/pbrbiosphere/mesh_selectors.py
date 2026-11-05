"""Pure geometry selector helpers for CAD-to-mesh preparation."""


def classify_surface_bbox(bbox, selector, tolerance):
    """Return True when a surface lies on the requested coordinate plane."""
    axis = {"x": 0, "y": 1, "z": 2}[selector["axis"]]
    lo, hi = bbox[axis], bbox[axis + 3]
    coordinate = float(selector["coordinate_m"])
    return abs(lo - coordinate) <= tolerance and abs(hi - coordinate) <= tolerance
