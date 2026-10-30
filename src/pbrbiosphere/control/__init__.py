"""Conservative supervisory control tools; recommendations only, no hardware I/O."""
from .supervisor import ControlLimits, SensorSnapshot, ControlDecision, decide
__all__ = ["ControlLimits", "SensorSnapshot", "ControlDecision", "decide"]
