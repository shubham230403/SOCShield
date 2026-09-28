# SOCShield Architecture

## Lab Environment

```text
                    Windows 11 Host
                         │
                    VirtualBox
                         │
          ┌──────────────┴──────────────┐
          │                             │
     Kali Linux                    Ubuntu Server
      Attacker                       SOC / SIEM
          │                             │
          │                         Wazuh
          │                             │
          └────── Simulated ────────────┤
                 Security Events        │
                                        │
                                  Detection & Alerts
                                        │
                                        ▼
                                  Investigation
                                        │
                                        ▼
                                  Incident Response

                                  | Component     | Role                           |
## Components

| Component | Role |
|-----------|------|
| Windows 11 | Host / Endpoint |
| Kali Linux | Controlled attacker |
| Ubuntu Server | SOC/SIEM server |
| Wazuh | SIEM, detection and monitoring |
| Wireshark | Network investigation |
| Nmap | Controlled reconnaissance |
| Python | Security automation |

## SOC Workflow

Alert → Triage → Validate → Investigate → IOC Analysis → Severity → Containment → Eradication → Recovery → Documentation