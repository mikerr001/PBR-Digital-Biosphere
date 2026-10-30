"""PBR-04 explicit flat-panel reactor geometry."""
from dataclasses import dataclass
import math
@dataclass(frozen=True)
class FlatPanelGeometry:
    width_m: float
    height_m: float
    optical_path_m: float
    liquid_volume_l: float
    headspace_volume_l: float
    illuminated_faces: int = 1
    def validate(self):
        for name in ("width_m","height_m","optical_path_m","liquid_volume_l","headspace_volume_l"):
            v=getattr(self,name)
            if not math.isfinite(v) or v<=0: raise ValueError(f"{name} must be finite and > 0")
        if self.illuminated_faces not in (1,2): raise ValueError("illuminated_faces must be 1 or 2")
    @property
    def frontal_area_m2(self):
        self.validate(); return self.width_m*self.height_m
    @property
    def illuminated_area_m2(self): return self.frontal_area_m2*self.illuminated_faces
    @property
    def calculated_liquid_volume_l(self): return self.frontal_area_m2*self.optical_path_m*1000
    @property
    def volume_closure_relative_error(self):
        return abs(self.calculated_liquid_volume_l-self.liquid_volume_l)/self.liquid_volume_l
