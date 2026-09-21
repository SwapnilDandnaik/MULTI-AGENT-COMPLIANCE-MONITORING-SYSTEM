import pandas as pd
from core.orchestrator import Orchestrator
from core.audit import AuditTrail

def scenario(sid):
    df=pd.read_csv("data/scenarios.csv")
    return df[df.id==sid].iloc[0].to_dict()

def test_cs20_critical():
    result=Orchestrator().run(scenario("CS-20"))
    assert result["consensus"]["severity"]=="CRITICAL"
    assert result["audit_valid"]

def test_cs18_suppressed():
    result=Orchestrator().run(scenario("CS-18"))
    assert result["consensus"]["severity"]=="NO ALERT"

def test_audit_chain():
    a=AuditTrail()
    a.add("x","test",{"n":1})
    a.add("y","test",{"n":2})
    assert a.verify()
