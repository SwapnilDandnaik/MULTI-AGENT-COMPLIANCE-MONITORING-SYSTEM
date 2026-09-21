from dataclasses import dataclass
import re
import numpy as np
import pandas as pd

@dataclass
class Signal:
    agent: str
    severity: str
    confidence: float
    finding: str
    evidence: list
    recommendation: str

SEV = {"NONE":0, "LOW":1, "MEDIUM":2, "HIGH":3, "CRITICAL":4}

def level(n):
    for k,v in sorted(SEV.items(), key=lambda x:x[1], reverse=True):
        if n >= v and v > 0:
            return k
    return "NONE"

class TransactionMonitor:
    name = "Transaction Monitor"
    def analyze(self, scenario=None, df=None):
        signals=[]
        if scenario:
            sid=scenario["id"]
            rules={
                "CS-01":("CRITICAL",.96,"Pre-announcement accumulation correlates with privileged relationship evidence."),
                "CS-02":("HIGH",.94,"Rapid order cancellation pattern is consistent with spoofing indicators."),
                "CS-03":("HIGH",.82,"Product/client suitability mismatch is indicated by age and policy restrictions."),
                "CS-04":("CRITICAL",.98,"Repeated cash deposits below a reporting threshold indicate possible structuring."),
                "CS-06":("HIGH",.95,"Repeated matched trades across accounts indicate possible wash trading."),
                "CS-09":("CRITICAL",.99,"Beneficiary relationship and recent sanctions-list addition create a sanctions alert."),
                "CS-10":("CRITICAL",.96,"Personal trading repeatedly precedes client orders with abnormal profitability."),
                "CS-12":("MEDIUM",.90,"Portfolio concentration exceeds the stated 25% limit."),
                "CS-14":("CRITICAL",.98,"Post-cutoff order entry with same-day NAV is a late-trading indicator."),
                "CS-15":("HIGH",.88,"Systematic routing to a worse-priced venue indicates possible best-execution failure."),
                "CS-16":("CRITICAL",.91,"Trading/research activity around an offering indicates a potential independence conflict."),
                "CS-17":("CRITICAL",.93,"Abnormal trading volume plus new POA is consistent with exploitation indicators."),
                "CS-18":("MEDIUM",.72,"Large block size triggers an initial concentration/anomaly signal; documentation can suppress it."),
                "CS-20":("CRITICAL",.99,"Trade-finance pricing, routing and override signals indicate coordinated AML risk.")
            }
            if sid in rules:
                s,f,e = rules[sid]
                signals.append(Signal(self.name,s,f,[scenario["description"]],"Escalate for compliance review."))
        if df is not None and not df.empty:
            d=df.copy()
            amount=pd.to_numeric(d.get("amount",0),errors="coerce").fillna(0)
            high=d.get("high_risk_country",pd.Series(0,index=d.index)).astype(int)
            rapid=d.get("rapid_movement",pd.Series(0,index=d.index)).astype(int)
            score=np.clip((amount/max(amount.quantile(.95),1))*55+high*25+rapid*20,0,100)
            d["risk_score"]=score.round(1)
            d["risk_level"]=pd.cut(score,[-1,30,60,80,101],labels=["Low","Medium","High","Critical"])
            high_rows=d[d["risk_score"]>=60]
            if not high_rows.empty:
                signals.append(Signal(self.name,"HIGH",min(0.99,0.65+len(high_rows)/100),
                    f"{len(high_rows)} transaction(s) exceed the prototype risk threshold.",
                    high_rows.head(10).to_dict("records"),"Review transaction and counterparty evidence."))
        return signals

class CommunicationScanner:
    name = "Communication Scanner"
    keywords=["urgent","bypass","off-channel","whatsapp","personal","guaranteed","safe","don't cover",
              "override","screening flag","confidential","secret"]
    def analyze(self, scenario=None, df=None):
        signals=[]
        if scenario:
            sid=scenario["id"]
            mapping={
                "CS-01":("CRITICAL",.92,"Communication evidence suggests a relationship with a pre-announcement issuer."),
                "CS-03":("HIGH",.83,"Client-facing language may conflict with suitability requirements."),
                "CS-05":("CRITICAL",.99,"Direct communication indicates a potential information-barrier breach."),
                "CS-08":("CRITICAL",.98,"Marketing language contains potentially misleading guaranteed-return claims."),
                "CS-09":("HIGH",.79,"Communication context may corroborate sanctions-routing concerns."),
                "CS-11":("HIGH",.90,"Data-transfer context indicates a potential privacy compliance issue."),
                "CS-13":("HIGH",.99,"Personal-channel business communications indicate record-keeping risk."),
                "CS-16":("CRITICAL",.92,"Research/IB communications may indicate an independence conflict."),
                "CS-17":("CRITICAL",.89,"Communications show third-party direction of client trades."),
                "CS-20":("CRITICAL",.98,"Communications include compliance-screening overrides.")
            }
            if sid in mapping:
                s,f,e=mapping[sid]
                signals.append(Signal(self.name,s,f,[scenario["description"]],"Preserve evidence and escalate for human review."))
        if df is not None and not df.empty:
            d=df.copy()
            text=d.get("message",pd.Series("",index=d.index)).fillna("").astype(str).str.lower()
            hits=text.apply(lambda x:[k for k in self.keywords if k in x])
            d["keyword_hits"]=hits.apply(len)
            d["risk_score"]=(d["keyword_hits"]*18).clip(0,100)
            suspicious=d[d["risk_score"]>=18]
            if not suspicious.empty:
                signals.append(Signal(self.name,"HIGH",min(.98,.60+len(suspicious)/100),
                    f"{len(suspicious)} communication(s) contain compliance-sensitive terms.",
                    suspicious.head(10).to_dict("records"),"Preserve communication evidence and review context."))
        return signals

class RegulatoryUpdateTracker:
    name = "Regulatory Update Tracker"
    def analyze(self, scenario=None, df=None):
        signals=[]
        if scenario:
            mapping={
                "CS-07":("MEDIUM",.97,"New margin requirements require impact assessment and deadline tracking."),
                "CS-09":("CRITICAL",.96,"A recent sanctions-list change materially affects transaction screening."),
                "CS-11":("HIGH",.95,"Cross-border data transfer requirements require legal/privacy review."),
                "CS-19":("HIGH",.99,"EU reporting and Singapore data-sharing constraints create a cross-jurisdiction conflict."),
                "CS-20":("CRITICAL",.94,"A recent enhanced-due-diligence update changes the risk context.")
            }
            if scenario["id"] in mapping:
                s,f,e=mapping[scenario["id"]]
                signals.append(Signal(self.name,s,f,[scenario["description"]],"Map the change to policies and obtain human legal validation."))
        return signals

class ReportGenerator:
    name = "Report Generator"
    def generate(self, scenario, signals, consensus, audit):
        return {
            "report_type":"Compliance Investigation Draft",
            "generated_by":self.name,
            "scenario":scenario["id"],
            "title":scenario["title"],
            "severity":consensus["severity"],
            "confidence":consensus["confidence"],
            "finding":consensus["finding"],
            "agent_signals":[s.__dict__ for s in signals],
            "recommended_action":consensus["action"],
            "regulations":scenario["regulations"],
            "audit_entries":len(audit.entries),
            "human_authorisation_required":True,
            "disclaimer":"Prototype only. Human compliance/legal approval is required before any filing, hold, customer action or regulatory communication."
        }
