"""Evidence-provenance validation for parameter-register rows."""
from math import isfinite
ALLOWED_CLASSES={"measured","literature_derived","fitted","estimated","unknown"}
REQUIRED=("parameter_id","organism","strain","parameter","unit","evidence_class","status","source_doi","notes")
def validate_parameter_record(record):
    """Return audit findings; does not determine biological validity."""
    issues=[]
    for key in REQUIRED:
        if not str(record.get(key,"")).strip(): issues.append(f"missing:{key}")
    if str(record.get("evidence_class","")).strip().lower() not in ALLOWED_CLASSES: issues.append("invalid:evidence_class")
    status=str(record.get("status","")).strip().lower()
    if status in {"measured","fitted"}:
        try:
            if not isfinite(float(record.get("value"))): raise ValueError
        except (TypeError,ValueError): issues.append("invalid:numeric_value_required_for_measured_or_fitted")
    if status in {"measured","fitted","literature-derived","literature_derived"} and not str(record.get("source_doi","")).strip(): issues.append("missing:source_for_evidence")
    if status=="missing" and record.get("value") not in (None,""): issues.append("inconsistent:missing_status_has_value")
    return issues
