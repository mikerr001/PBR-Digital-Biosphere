"""Independent holdout comparison; no silent interpolation."""
import numpy as np
def compare_independent_dataset(predicted,observed,time_column,value_column,uncertainty_column=None):
    """Compare exact time grids; caller must attest holdout independence."""
    for frame,label in ((predicted,"predicted"),(observed,"observed")):
        need=[time_column,value_column]+([uncertainty_column] if label=="observed" and uncertainty_column else [])
        missing=[c for c in need if c not in frame.columns]
        if missing: raise ValueError(f"{label} dataset missing columns: {missing}")
    p=predicted[[time_column,value_column]].copy()
    o=observed[[time_column,value_column]+([uncertainty_column] if uncertainty_column else [])].copy()
    if p[time_column].duplicated().any() or o[time_column].duplicated().any(): raise ValueError("time coordinates must be unique")
    m=p.merge(o,on=time_column,how="outer",suffixes=("_predicted","_observed"),indicator=True)
    if not (m["_merge"]=="both").all(): raise ValueError("prediction and observation time grids must match exactly; interpolation is disabled")
    a=m[f"{value_column}_predicted"].to_numpy(float); b=m[f"{value_column}_observed"].to_numpy(float)
    if not np.isfinite(a).all() or not np.isfinite(b).all(): raise ValueError("values must be finite")
    e=a-b
    out={"n":int(len(e)),"bias":float(np.mean(e)),"mae":float(np.mean(np.abs(e))),"rmse":float(np.sqrt(np.mean(e**2))),"max_abs_error":float(np.max(np.abs(e)))}
    if uncertainty_column:
        s=m[uncertainty_column].to_numpy(float)
        if not np.isfinite(s).all() or np.any(s<=0): raise ValueError("uncertainties must be finite and > 0")
        out["mean_absolute_normalized_error"]=float(np.mean(np.abs(e)/s))
        out["within_1sigma_fraction"]=float(np.mean(np.abs(e)<=s + 1e-12*np.maximum(1.0,s)))
    return out
