import pandas as pd
import pytest
from pbrbiosphere.calibration import validate_parameter_record,compare_independent_dataset
def test_parameter_record_traceability():
 r={"parameter_id":"x","organism":"Synechococcus elongatus","strain":"PCC 7942","parameter":"growth_rate","unit":"h-1","evidence_class":"measured","status":"measured","source_doi":"10.x/y","notes":"condition-specific","value":0.1}
 assert validate_parameter_record(r)==[]
def test_parameter_record_missing_evidence():
 r=validate_parameter_record({"evidence_class":"measured","status":"measured","value":None})
 assert "missing:source_doi" in r and any("numeric_value" in x for x in r)
def test_holdout_metrics():
 p=pd.DataFrame({"t":[0,1,2],"y":[1.,2.,3.]}); o=pd.DataFrame({"t":[0,1,2],"y":[1.1,1.8,3.],"sd":[.1,.2,.1]})
 r=compare_independent_dataset(p,o,"t","y","sd")
 assert r["n"]==3 and r["within_1sigma_fraction"]==1.
def test_holdout_requires_matching_grid():
 p=pd.DataFrame({"t":[0,1],"y":[1.,2.]}); o=pd.DataFrame({"t":[0,2],"y":[1.,2.]})
 with pytest.raises(ValueError,match="time grids"): compare_independent_dataset(p,o,"t","y")
