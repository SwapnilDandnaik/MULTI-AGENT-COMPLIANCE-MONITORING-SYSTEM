import json
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
from core.orchestrator import Orchestrator

BASE=Path(__file__).resolve().parent
scenarios=pd.read_csv(BASE/"data/scenarios.csv")
tx_default=pd.read_csv(BASE/"data/transactions.csv")
comm_default=pd.read_csv(BASE/"data/communications.csv")

st.set_page_config(page_title="MCIP Compliance Intelligence",page_icon="🛡️",layout="wide")

st.title("🛡️ MCIP — Multi-Agent Compliance Intelligence Platform")
st.caption("Runnable educational prototype based on the supplied multi-agent compliance system specification.")

with st.sidebar:
    st.header("Navigation")
    page=st.radio("Open",["Dashboard","Scenario Arena","Data Upload","Audit Explorer","About"])
    st.divider()
    st.warning("Prototype only — human compliance/legal authorization is required for real-world action.")

orch=Orchestrator()

if page=="Dashboard":
    st.subheader("System Dashboard")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Specialist Agents","4")
    c2.metric("Scenarios","20")
    c3.metric("Critical Scenarios",int((scenarios.severity=="CRITICAL").sum()))
    c4.metric("False-Positive Test","CS-18")
    st.markdown("### Agent topology")
    st.code("""
                    MCIP Orchestrator
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   Transaction       Communication      Regulatory
     Monitor            Scanner           Tracker
          \\\\              │              //
           \\\\             │             //
                    Report Generator
                           │
                    Human Review Board
    """)
    fig=px.bar(scenarios,x="id",color="severity",title="Scenario severity distribution")
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(scenarios[["id","title","agents","complexity","severity"]],use_container_width=True,hide_index=True)

elif page=="Scenario Arena":
    st.subheader("🎯 Scenario Arena — 20 Compliance Scenarios")
    sid=st.selectbox("Select scenario",scenarios.id.tolist())
    row=scenarios[scenarios.id==sid].iloc[0].to_dict()
    st.markdown(f"### {row['id']} — {row['title']}")
    st.write(row["description"])
    a,b,c=st.columns(3)
    a.metric("Expected severity",row["severity"])
    b.metric("Required agents",row["agents"])
    c.metric("Complexity",row["complexity"])
    st.write("**Applicable regulations:**",row["regulations"])
    if st.button("▶ Run scenario",type="primary"):
        result=orch.run(row,tx_default,comm_default)
        st.session_state["last_result"]=result
        st.session_state["last_scenario"]=row
    if "last_result" in st.session_state:
        result=st.session_state["last_result"]
        cons=result["consensus"]
        st.divider()
        x,y,z=st.columns(3)
        x.metric("System decision",cons["severity"])
        y.metric("Consensus confidence",f"{cons['confidence']:.1%}")
        z.metric("Audit chain","VALID" if result["audit_valid"] else "INVALID")
        st.info(cons["finding"])
        st.write("**Human escalation / recommended action:**",cons["action"])
        st.markdown("### Agent signals")
        if result["signals"]:
            st.dataframe(pd.DataFrame([{
                "Agent":s.agent,"Severity":s.severity,"Confidence":s.confidence,
                "Finding":s.finding,"Recommendation":s.recommendation
            } for s in result["signals"]]),use_container_width=True,hide_index=True)
        else:
            st.success("No specialist signal.")
        st.markdown("### Audit trail")
        st.dataframe(pd.DataFrame(result["audit"]),use_container_width=True,hide_index=True)
        report=json.dumps(result["report"],indent=2)
        st.download_button("Download JSON report",report,f"{sid}_compliance_report.json","application/json")

elif page=="Data Upload":
    st.subheader("📥 Data Upload & Agent Analysis")
    tx=st.file_uploader("Transactions CSV",type=["csv"])
    comm=st.file_uploader("Communications CSV",type=["csv"])
    txdf=pd.read_csv(tx) if tx else tx_default
    cdf=pd.read_csv(comm) if comm else comm_default
    st.write("Transactions")
    st.dataframe(txdf,use_container_width=True)
    st.write("Communications")
    st.dataframe(cdf,use_container_width=True)
    if st.button("Analyze uploaded data",type="primary"):
        ts=orch.tm.analyze(None,txdf)
        cs=orch.cs.analyze(None,cdf)
        st.success(f"Analysis complete — {len(ts)} transaction signal(s), {len(cs)} communication signal(s).")
        signals=ts+cs
        if signals:
            st.dataframe(pd.DataFrame([s.__dict__ for s in signals]),use_container_width=True,hide_index=True)
        else:
            st.success("No threshold-based prototype alerts found.")
        if not txdf.empty and "amount" in txdf:
            vals=pd.to_numeric(txdf["amount"],errors="coerce").fillna(0)
            st.plotly_chart(px.histogram(vals,x=vals,title="Transaction amount distribution"),use_container_width=True)

elif page=="Audit Explorer":
    st.subheader("🔐 Audit Explorer")
    if "last_result" not in st.session_state:
        st.info("Run a scenario first.")
    else:
        r=st.session_state["last_result"]
        st.metric("Hash-chain verification","VALID" if r["audit_valid"] else "INVALID")
        st.dataframe(pd.DataFrame(r["audit"]),use_container_width=True,hide_index=True)

elif page=="About":
    st.subheader("About this implementation")
    st.markdown("""
This prototype implements the four-agent architecture from the supplied project material:
**Transaction Monitor, Communication Scanner, Regulatory Update Tracker, and Report Generator**.

It also demonstrates:
- inter-agent orchestration
- weighted confidence / consensus
- human-in-the-loop escalation
- false-positive suppression for CS-18
- coordinated CS-20 handling
- audit-grade hash chaining
- scenario trace-throughs
- operational dashboarding

The implementation is intentionally deterministic and uses rule-based simulation rather than
claiming production-grade legal interpretation, autonomous regulatory filing, or live regulatory feeds.
""")
    st.write("Source scenarios included:",len(scenarios))
    st.write("Project package is intended for demonstration, learning and hackathon/project use.")
