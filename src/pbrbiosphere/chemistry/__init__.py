"""Aqueous chemistry helpers with explicit model-scope limits."""
from .carbonate import CarbonateConstants, carbonate_speciation, co2_gas_transfer_rate
__all__ = ["CarbonateConstants", "carbonate_speciation", "co2_gas_transfer_rate"]
