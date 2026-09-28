# SOCShield — Threat Hunting

Threat hunting in SOCShield focuses on proactively searching security logs and system activity for suspicious behavior that may not have generated a high-confidence alert.

## Hunting Process

```text
Define Hypothesis
       ↓
Collect Evidence
       ↓
Search Logs
       ↓
Identify Anomalies
       ↓
Investigate
       ↓
Validate
       ↓
Document Findings
```

## Planned Hunting Activities

### Authentication Hunting

Search for:

* Repeated failed logins
* Unusual usernames
* Unusual login times
* Multiple source IPs
* Successful login following repeated failures

### Network Hunting

Search for:

* Multiple connection attempts
* Unexpected ports
* Repeated connections from a single source
* Unusual network services
* Reconnaissance patterns

### File Activity Hunting

Search for:

* Unexpected file creation
* Suspicious filenames
* Unusual file locations
* File hashes associated with investigations

## Hunting Hypotheses

### Hypothesis 1 — Brute Force

> A host generating a large number of failed authentication attempts within a short period may indicate a brute-force attack.

### Hypothesis 2 — Network Reconnaissance

> A host contacting many ports on another system within a short period may indicate network service scanning.

### Hypothesis 3 — Suspicious Authentication

> Repeated authentication failures followed by a successful login may require additional investigation.

## Evidence

Hunting results will be supported by:

* Wazuh alerts
* Authentication logs
* Windows Security Events
* Network traffic
* IP addresses
* Timestamps
* File hashes

## Documentation

Validated findings will be linked to the relevant incident report and IOC records.
