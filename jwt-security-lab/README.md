\# SOCShield - JWT Security Lab



A practical Application Security lab focused on identifying and remediating common authentication and JSON Web Token (JWT) security weaknesses in a Flask-based API.



\## Overview



This project demonstrates a security assessment of a JWT-based authentication system.



The lab was first evaluated for common authentication weaknesses and then remediated using secure coding practices. Automated security tests were created to validate that the implemented controls work as expected.



\## Objectives



\* Identify authentication and JWT security weaknesses

\* Test for username enumeration

\* Test resistance to automated login attempts

\* Assess JWT signature validation

\* Test JWT expiration handling

\* Test JWT tampering and role modification

\* Improve password storage

\* Remove hard-coded secrets

\* Implement authentication rate limiting

\* Validate security controls through automated testing



\## Technology Stack



\* Python

\* Flask

\* PyJWT

\* Requests

\* JWT / HS256

\* Werkzeug password hashing

\* REST API

\* PowerShell

\* Git / GitHub



\## Project Structure



```text

jwt-security-lab/

├── app.py

├── test\_jwt.py

├── requirements.txt

├── README.md

├── .gitignore

└── venv/

```



`venv/` and Python cache files are excluded from Git using `.gitignore`.



\## Security Assessment



\### 1. Username Enumeration



\#### Issue



The vulnerable implementation returned different authentication responses for different login conditions.



This can allow an attacker to determine whether a username exists.



\#### Remediation



Authentication failures now return a generic response:



```text

Invalid credentials

```



Both unknown users and existing users with an incorrect password receive the same HTTP status and response.



\### 2. Missing Brute-Force Protection



\#### Issue



The vulnerable implementation allowed repeated login attempts without enforcing a limit.



\#### Remediation



A login rate-limiting control was implemented.



The lab allows five failed attempts. The sixth attempt is rejected with:



```text

HTTP 429

Too many login attempts. Try again later.

```



Test result:



```text

Attempt 1: HTTP 401

Attempt 2: HTTP 401

Attempt 3: HTTP 401

Attempt 4: HTTP 401

Attempt 5: HTTP 401

Attempt 6: HTTP 429

Attempt 7: HTTP 429

```



> Note: The in-memory rate limiter is suitable for this lab. A production application should use a distributed mechanism such as Redis, an API gateway, WAF, or another shared rate-limiting service.



\### 3. Plaintext Password Storage



\#### Issue



The initial implementation stored demonstration passwords directly in application memory.



\#### Remediation



Passwords are now stored as hashes using Werkzeug's password hashing functions.



```python

generate\_password\_hash()

check\_password\_hash()

```



The application therefore does not compare plaintext passwords directly.



\### 4. Hard-Coded JWT Secret



\#### Issue



The vulnerable implementation contained the JWT signing secret directly in source code.



Hard-coded secrets can be exposed through source repositories, logs, backups, or accidental code disclosure.



\#### Remediation



The JWT secret is now loaded from an environment variable:



```python

SECRET\_KEY = os.getenv("JWT\_SECRET")

```



The application refuses to start if the secret is not configured.



Example PowerShell configuration:



```powershell

$env:JWT\_SECRET = "socshield-jwt-secret-32-bytes-long!"

```



\### 5. JWT Signature Validation



The API validates JWT signatures using the server-controlled secret and an explicit algorithm allowlist.



```python

jwt.decode(

&#x20;   token,

&#x20;   SECRET\_KEY,

&#x20;   algorithms=\["HS256"]

)

```



This prevents an attacker from modifying token contents and signing the modified token with an unauthorized secret.



\### 6. JWT Tampering Test



The automated test modifies the JWT role claim:



```text

user → admin

```



The modified token is signed using an attacker-controlled secret.



Expected result:



```text

HTTP 401

Invalid token

```



Actual result:



```text

PASS: Tampered JWT rejected

HTTP status: 401

```



The role modification therefore does not result in privilege escalation.



\### 7. JWT Expiration Validation



JWTs contain an expiration claim.



Expired tokens are rejected by the API.



Test result:



```text

PASS: Expired JWT rejected

HTTP status: 401

```



\## Automated Security Testing



`test\_jwt.py` contains automated tests covering:



| Test                         | Expected Result                      |

| ---------------------------- | ------------------------------------ |

| Generic authentication error | Same response for unknown/known user |

| Login rate limiting          | 5 × 401 followed by 429              |

| Valid login                  | JWT issued                           |

| Missing JWT                  | 401                                  |

| Valid JWT                    | 200                                  |

| Tampered JWT                 | 401                                  |

| Expired JWT                  | 401                                  |



\### Final Test Result



```text

PASS: Generic authentication error

PASS: Login rate limiting

PASS: Valid login and JWT issuance

PASS: Protected API rejects missing token

PASS: Valid JWT grants authorized access

PASS: Tampered JWT rejected

PASS: Expired JWT rejected



JWT SECURITY TESTING COMPLETE

```



\## Security Mapping



| Finding / Control                         | Reference                       |

| ----------------------------------------- | ------------------------------- |

| Authentication weaknesses                 | OWASP API Security              |

| Excessive authentication attempts         | CWE-307                         |

| Information disclosure / user enumeration | CWE-200                         |

| Hard-coded secret                         | CWE-798                         |

| Plaintext password storage                | CWE-256                         |

| Verbose authentication errors             | CWE-209                         |

| JWT authentication                        | OWASP API Security              |

| Password hashing                          | Secure authentication practice  |

| Rate limiting                             | Authentication security control |



\## Security Testing Methodology



The assessment followed a practical AppSec workflow:



```text

Source Review

&#x20;    ↓

Identify Authentication Weaknesses

&#x20;    ↓

Build Security Tests

&#x20;    ↓

Exploit / Validate Vulnerability

&#x20;    ↓

Implement Remediation

&#x20;    ↓

Retest

&#x20;    ↓

Document Results

```



\## Running the Lab



\### Install Dependencies



```powershell

python -m pip install -r requirements.txt

```



\### Configure JWT Secret



PowerShell:



```powershell

$env:JWT\_SECRET = "socshield-jwt-secret-32-bytes-long!"

```



\### Start the Application



```powershell

python app.py

```



The API runs at:



```text

http://127.0.0.1:5002

```



\### Run Automated Tests



Open another PowerShell window:



```powershell

cd C:\\Users\\Admin\\SOCShield\\jwt-security-lab

python test\_jwt.py

```



\## Example API Flow



\### Login



```http

POST /login

Content-Type: application/json

```



Example request:



```json

{

&#x20;   "username": "shubham",

&#x20;   "password": "security123"

}

```



The server returns a JWT after successful authentication.



\### Access Protected Endpoint



```http

GET /api/profile

Authorization: Bearer <JWT>

```



A valid token allows access.



Invalid, expired, missing, or tampered tokens are rejected.



\## Production Considerations



This project is intentionally designed as a security learning lab.



For production environments, additional controls should be considered:



\* Store secrets in a dedicated secrets-management system

\* Use strong randomly generated JWT signing keys

\* Use secure password hashing with an appropriate password-hashing algorithm

\* Implement distributed rate limiting

\* Add account lockout or progressive delays where appropriate

\* Monitor authentication failures

\* Add centralized security logging

\* Protect tokens using appropriate transport and storage controls

\* Consider token revocation/session-management requirements

\* Perform regular dependency and vulnerability scanning

\* Apply least-privilege authorization checks



\## Disclaimer



This project is intended for educational and authorized security-testing purposes only.



All testing was performed against a locally controlled application.



