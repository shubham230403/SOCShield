# SOCShield — IOC Tracker

This directory contains Indicators of Compromise (IOCs) identified during SOCShield investigations.

## IOC Categories

| Type       | Description                                                         |
| ---------- | ------------------------------------------------------------------- |
| IP Address | Source or destination addresses associated with suspicious activity |
| Domain     | Suspicious or malicious domains                                     |
| Hash       | SHA-256 hashes of suspicious files                                  |
| Username   | Accounts involved in suspicious authentication activity             |
| Filename   | Suspicious or unauthorized files                                    |
| Port       | Network services involved in suspicious activity                    |
| Timestamp  | Time associated with relevant security events                       |

## IOC Record Template

| Field               | Value |
| ------------------- | ----- |
| IOC Type            |       |
| IOC Value           |       |
| First Observed      |       |
| Last Observed       |       |
| Associated Incident |       |
| Source              |       |
| Confidence          |       |
| Notes               |       |

## Investigation Notes

IOCs will only be added after validating them against the relevant logs, alerts, network evidence, or other investigation data.

No fabricated indicators will be used in incident reports.
