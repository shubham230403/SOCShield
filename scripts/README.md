# SOCShield — Security Automation

This directory contains Python scripts used to automate selected SOC investigation and documentation tasks.

## Planned Automation

### 1. IOC Extraction

Extract indicators such as:

* IP addresses
* Domains
* SHA-256 hashes
* Usernames
* Filenames

### 2. Log Analysis

Process security logs to identify patterns such as:

* Repeated authentication failures
* Suspicious source IPs
* Repeated network connections
* Unusual activity

### 3. Hash Calculation

Calculate SHA-256 hashes for files investigated during the lab.

### 4. Investigation Helpers

Automate repetitive investigation tasks and produce structured output for incident documentation.

## Automation Workflow

```text
Security Logs
     ↓
Python Script
     ↓
Parse / Filter
     ↓
Extract Indicators
     ↓
Analyze Pattern
     ↓
Structured Output
     ↓
Incident Documentation
```

## Development Principles

* Use Python standard libraries where practical
* Keep scripts modular
* Validate input data
* Avoid hard-coded sensitive information
* Document script usage
* Test scripts against controlled lab data

## Planned Scripts

| Script               | Purpose                       | Status  |
| -------------------- | ----------------------------- | ------- |
| `ioc_extractor.py`   | Extract IOCs from logs        | Planned |
| `log_analyzer.py`    | Analyze security logs         | Planned |
| `hash_checker.py`    | Calculate file hashes         | Planned |
| `incident_helper.py` | Assist incident documentation | Planned |
