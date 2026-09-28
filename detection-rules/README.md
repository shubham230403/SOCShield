# SOCShield — Detection Rules

This directory contains detection logic and rule documentation developed during the SOCShield lab.

## Detection Use Cases

### 1. SSH Brute Force

**Objective:** Detect repeated failed SSH authentication attempts.

**Log Source:** Linux authentication logs / Wazuh

**Key Indicators:**

* Multiple authentication failures
* Same source IP
* Repeated attempts against an account
* Short time interval between attempts

**MITRE ATT&CK:** T1110 — Brute Force

---

### 2. Network Service Scanning

**Objective:** Detect reconnaissance involving multiple ports or services.

**Log Source:** Network/security monitoring

**Key Indicators:**

* Multiple destination ports
* Multiple connection attempts
* Same source IP
* Short time interval

**MITRE ATT&CK:** T1046 — Network Service Scanning

---

### 3. Windows Failed Authentication

**Objective:** Detect suspicious repeated Windows login failures.

**Log Source:** Windows Security Events / Wazuh

**Key Indicators:**

* Repeated failed authentication
* Targeted account
* Source information
* Abnormal frequency

---

### 4. Suspicious File Activity

**Objective:** Detect and investigate potentially suspicious file activity.

**Key Indicators:**

* Unexpected file creation
* Suspicious filename
* SHA-256 hash
* Unexpected location
* Associated process or event

---

## Rule Development Process

```text
Security Event
      ↓
Identify Pattern
      ↓
Define Detection Logic
      ↓
Generate Controlled Test Event
      ↓
Verify Alert
      ↓
Tune Rule
      ↓
Document Detection
```

## Rule Validation

Every detection will be tested against controlled activity in the SOCShield lab before being documented as a working detection.

Detection rules will be refined to reduce false positives while maintaining useful visibility.
