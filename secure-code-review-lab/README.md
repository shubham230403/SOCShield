Remediation

Replaced string concatenation with parameterized SQL queries.

query = """
    SELECT username, role
    FROM users
    WHERE username = ?
    AND password = ?
"""

user = conn.execute(
    query,
    (username, password)
).fetchone()
Verification

The original SQL injection test successfully bypassed the vulnerable
authentication logic.

After remediation, the same test returned:

FAIL: SQL Injection

This indicates that the attack could no longer reproduce the vulnerability.

2. Command Injection
Root Cause

User-controlled input was inserted directly into a shell command.

Vulnerable Pattern
command = f"ping -n 1 {host}"
result = subprocess.getoutput(command)
Remediation

Implemented input validation and executed the command using a separate
argument list with shell execution disabled.

result = subprocess.run(
    ["ping", "-n", "1", host],
    capture_output=True,
    text=True,
    timeout=5,
    shell=False
)
Verification

The original command-injection test was successfully demonstrated.

After remediation:

FAIL: Command Injection
HTTP status: 400

The malicious input was rejected.

3. Path Traversal
Root Cause

The application directly combined user-controlled file names with the
application file directory.

Vulnerable Pattern
filepath = os.path.join("files", filename)
Remediation

The requested path is resolved to its canonical path and checked to ensure
that it remains inside the permitted files directory.

requested_path = (
    FILES_DIR / filename
).resolve()

requested_path.relative_to(FILES_DIR)
Verification

Before remediation:

PASS: Path Traversal
Application source exposed: True

After remediation:

FAIL: Path Traversal
HTTP status: 403
4. Stored Cross-Site Scripting
Root Cause

Stored user input was directly inserted into the generated HTML response.

Vulnerable Pattern
output += f"""
    <div>
        <b>{username}</b>:
        {comment_text}
    </div>
"""
Remediation

User-controlled values are HTML-escaped before rendering.

safe_username = html.escape(username)
safe_comment = html.escape(comment_text)
Verification

Before remediation:

PASS: Stored XSS
Payload returned unencoded: True

After remediation:

FAIL: Stored XSS
Payload returned unencoded: False
5. Hard-coded Secret
Root Cause

A sensitive application secret was embedded directly in source code and
returned through an application endpoint.

Vulnerable Pattern
API_SECRET = "SOCShield-Production-Secret-12345"
Remediation

The hard-coded production-style secret was removed from the application
response and configuration was moved toward environment-based handling.

Example:

API_SECRET = os.getenv(
    "SOCSHIELD_API_SECRET",
    "development-only-secret"
)

The application no longer exposes the secret through /secret.

Verification

Before remediation:

PASS: Hard-coded Secret Exposure
Secret exposed by endpoint: True

After remediation:

FAIL: Hard-coded Secret Exposure
Secret exposed by endpoint: False
6. Broken Access Control
Root Cause

The administrative endpoint originally had no authentication or
authorization check.

Vulnerable Behavior
GET /admin

returned the administrative interface without verifying the caller.

Remediation

The endpoint now requires an administrative identity for this demo lab.

username = request.headers.get("X-Demo-User")

if username != "admin":
    return "Forbidden", 403
Verification

Before remediation:

PASS: Broken Access Control
Admin panel accessible without authentication: True

After remediation:

FAIL: Broken Access Control
HTTP status: 403
Final Security Test Results
Before Remediation
PASS: SQL Injection
PASS: Command Injection
PASS: Path Traversal
PASS: Stored XSS
PASS: Hard-coded Secret Exposure
PASS: Broken Access Control

In the vulnerable-phase test suite, PASS means the security test successfully
reproduced the vulnerability.

After Remediation
FAIL: SQL Injection
FAIL: Command Injection
FAIL: Path Traversal
FAIL: Stored XSS
FAIL: Hard-coded Secret Exposure
FAIL: Broken Access Control

In the remediation-phase test suite, FAIL means the original attack test
could no longer reproduce the vulnerability.

Tools and Technologies
Python
Flask
SQLite
Requests
PowerShell
Secure Code Review
Dynamic Security Testing
OWASP Top 10
CWE
Key Security Concepts Demonstrated
Parameterized SQL queries
OS command execution safety
Input validation
Canonical path validation
Directory boundary enforcement
Output encoding
Secret management
Authentication and authorization
Security regression testing
Vulnerability remediation validation
Project Structure
secure-code-review-lab/
│
├── app.py
├── test_security.py
├── requirements.txt
├── README.md
├── .gitignore
├── users.db
└── files/
    └── notes.txt

users.db and other runtime/generated files are excluded from Git through
.gitignore.

Disclaimer

This project is an intentionally vulnerable local security lab created for
educational purposes and secure coding practice.

All security testing was performed against the author's own local
application.


## Step 3 — Save and check Git

After saving `README.md`, run:

```powershell
cd C:\Users\Admin\SOCShield
git status