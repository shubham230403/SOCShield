\# SOCShield – REST API Security Lab



\## Overview



This project is a controlled REST API security lab developed to demonstrate practical Application Security, API Security, VAPT, authorization testing, secure coding, and remediation validation.



The lab demonstrates a \*\*Broken Object Level Authorization (BOLA) / IDOR\*\* vulnerability in a REST API and shows how object-level authorization controls can prevent unauthorized access to another user's data.



The project follows a practical security testing workflow:



\*\*Identify → Validate → Review Code → Remediate → Retest → Automate → Document\*\*



\---



\## Objectives



\* Understand REST API authentication and authorization

\* Implement JWT-based authentication

\* Identify BOLA / IDOR vulnerabilities

\* Perform API authorization testing

\* Review vulnerable application logic

\* Implement object-level authorization

\* Validate remediation through retesting

\* Automate security regression tests

\* Document vulnerability impact, root cause, and remediation



\---



\## Technology Stack



| Technology | Purpose                    |

| ---------- | -------------------------- |

| Python     | Application development    |

| Flask      | REST API framework         |

| PyJWT      | JWT authentication         |

| Requests   | Automated security testing |

| HTTP/REST  | API communication          |

| PowerShell | Testing and execution      |

| Git/GitHub | Version control            |



\---



\## API Architecture



```text

Client / Security Test Script

&#x20;           |

&#x20;           v

&#x20;     Flask REST API

&#x20;           |

&#x20;     +-----+-----+

&#x20;     |           |

&#x20;Authentication  Authorization

&#x20;     |           |

&#x20;     v           v

&#x20;    JWT      Object Ownership

```



\---



\## Authentication



The API uses JSON Web Tokens (JWT) for authentication.



\### Login Endpoint



```http

POST /login

```



Example request:



```json

{

&#x20;   "username": "shubham",

&#x20;   "password": "security123"

}

```



A successful login returns a JWT token.



The token is then supplied through the HTTP Authorization header:



```http

Authorization: Bearer <JWT\_TOKEN>

```



\---



\# Vulnerability: BOLA / IDOR



\## What is BOLA?



Broken Object Level Authorization (BOLA) occurs when an authenticated user can access an object belonging to another user simply by changing an object identifier.



It is commonly associated with insecure API endpoints such as:



```text

/api/account/1001

/api/account/1002

/api/account/1003

```



Authentication alone does not prove that the authenticated user is authorized to access every object.



\---



\## Vulnerable Behavior



The original API verified that the requester possessed a



