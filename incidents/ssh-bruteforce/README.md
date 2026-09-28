Incident: SSH Brute Force

Status: Planned

Objective:
Detect and investigate repeated failed SSH authentication attempts
against the Ubuntu SOC server.

Attack Source:
Kali Linux VM

Target:
Ubuntu Server / Wazuh Server

Detection:
Wazuh SSH authentication alerts

Evidence to collect:
- Source IP
- Destination IP
- Target username
- Timestamp
- Number of failed attempts
- Successful login (if any)
- Wazuh alert ID/rule
- Relevant Ubuntu authentication logs

MITRE ATT&CK:
T1110 — Brute Force

SOC Workflow:
Alert → Triage → Validate → Investigate → Identify IOC
→ Assess Severity → Contain → Eradicate → Recover → Report

Response:
- Confirm whether authentication succeeded
- Identify source IP
- Contain the source if required
- Review affected account
- Verify no persistence or additional activity
- Document findings