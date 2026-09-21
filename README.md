# MCIP — Multi-Agent Compliance Intelligence Platform

A runnable educational/demo implementation of the MCIP architecture described in the supplied
Agentic AI - Multi-Agent Compliance Monitoring System specification.

## What is included

- Streamlit dashboard
- Four specialist agents:
  1. Transaction Monitor (TM)
  2. Communication Scanner (CS)
  3. Regulatory Update Tracker (RU)
  4. Report Generator (RG)
- Rule-based multi-agent orchestration
- Evidence/confidence scoring
- Conflict-resolution / weighted consensus
- Human-in-the-loop escalation
- Hash-chained audit trail
- 20 supplied compliance scenarios (CS-01 to CS-20)
- CSV upload for transactions and communications
- Scenario trace-through view
- Compliance metrics and downloadable JSON report
- Unit tests

> This is a runnable prototype/simulation, not a production banking compliance system and does
> not provide legal advice or autonomously file regulatory reports.

## Requirements

- Windows 10/11, macOS, or Linux
- Python 3.10+
- Internet is NOT required after packages are installed.

## Windows quick start

Open PowerShell in this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, use:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

Then open the local address Streamlit prints, normally:
http://localhost:8501

## Run tests

```powershell
.venv\Scripts\python.exe -m pytest -q
```

## Demo

1. Open the **Dashboard** tab.
2. Open **Scenario Arena**.
3. Select CS-01 through CS-20.
4. Click **Run scenario**.
5. Inspect the agent signals, consensus, escalation and audit trail.
6. Open **Data Upload** to upload CSV transaction/communication data.
7. Generate a report from the **Report** tab.

## CSV formats

Transactions can contain:

`transaction_id,customer_id,amount,country,high_risk_country,rapid_movement,side,price,quantity`

Communications can contain:

`message_id,employee_id,channel,message`

The prototype is deliberately deterministic so that a scenario can be reproduced from the same
inputs and its audit chain can be verified.
