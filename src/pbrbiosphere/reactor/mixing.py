"""Two-compartment exchange driven by a measured mixing time."""
import math
def two_compartment_exchange_rate(concentration_a,concentration_b,compartment_volume_l,mixing_time_s):
    """Signed A-to-B transfer rate (amount units/s).

    Assumes equal-volume compartments and defines mixing_time_s as the
    exponential decay time constant of the concentration difference.
    """
    vals=(concentration_a,concentration_b,compartment_volume_l,mixing_time_s)
    if not all(math.isfinite(v) for v in vals): raise ValueError("mixing inputs must be finite")
    if concentration_a<0 or concentration_b<0 or compartment_volume_l<=0 or mixing_time_s<=0:
        raise ValueError("concentrations must be >= 0; volume and mixing time > 0")
    return compartment_volume_l*(concentration_a-concentration_b)/(2*mixing_time_s)
