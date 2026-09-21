# MCIP Runnable Prototype Architecture

## Agents

### Transaction Monitor
Detects prototype transaction anomalies such as:
- rapid movement
- high-risk jurisdictions
- concentration
- spoofing/wash-trading/front-running scenario indicators
- structuring

### Communication Scanner
Scans supplied text for prototype indicators including:
- off-channel communication
- information leakage
- misleading claims
- screening overrides
- unsuitable recommendation language

### Regulatory Update Tracker
Represents regulatory-change events and cross-jurisdiction conflict signals from the supplied
scenario definitions.

### Report Generator
Compiles evidence, agent signals, consensus and audit metadata into a human-review draft.

## Orchestration

The orchestrator:
1. Starts an auditable workflow.
2. Dispatches the specialist agents.
3. Collects evidence and confidence.
4. Applies severity-aware consensus.
5. Applies CS-18 false-positive suppression.
6. Creates a human escalation event when required.
7. Generates a report.
8. Verifies the audit hash chain.

## Security / compliance boundary

This demo does not:
- connect to live banking systems
- access private customer data
- make legal determinations
- automatically freeze accounts
- automatically file SAR/STR or other regulatory reports
- replace qualified compliance or legal staff

It is a simulation suitable for a project/hackathon demonstration.
