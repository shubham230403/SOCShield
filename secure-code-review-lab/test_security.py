import requests

BASE_URL = "http://127.0.0.1:5003"


def print_result(name, passed, details=""):
    status = "PASS" if passed else "FAIL"

    print("=" * 70)
    print(f"{status}: {name}")

    if details:
        print(details)


# ============================================================
# 1. SQL INJECTION
# ============================================================

def test_sql_injection():

    response = requests.post(
        f"{BASE_URL}/login",
        data={
            "username": "admin' -- ",
            "password": "anything"
        }
    )

    passed = "Login successful" in response.text

    print_result(
        "SQL Injection",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Response contains successful login: {passed}"
    )


# ============================================================
# 2. COMMAND INJECTION
# ============================================================

def test_command_injection():

    response = requests.get(
        f"{BASE_URL}/ping",
        params={
            "host": "127.0.0.1 & whoami"
        }
    )

    passed = (
        "Ping Result" in response.text
        and response.status_code == 200
    )

    print_result(
        "Command Injection",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Response length: {len(response.text)}"
    )


# ============================================================
# 3. PATH TRAVERSAL
# ============================================================

def test_path_traversal():

    response = requests.get(
        f"{BASE_URL}/file",
        params={
            "name": "../app.py"
        }
    )

    passed = (
        "from flask import Flask" in response.text
    )

    print_result(
        "Path Traversal",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Application source exposed: {passed}"
    )


# ============================================================
# 4. STORED XSS
# ============================================================

def test_stored_xss():

    payload = "<script>alert('XSS')</script>"

    requests.post(
        f"{BASE_URL}/comment",
        data={
            "username": "security-tester",
            "comment": payload
        }
    )

    response = requests.get(
        f"{BASE_URL}/comment"
    )

    passed = payload in response.text

    print_result(
        "Stored XSS",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Payload returned unencoded: {passed}"
    )


# ============================================================
# 5. HARDCODED SECRET
# ============================================================

def test_hardcoded_secret():

    response = requests.get(
        f"{BASE_URL}/secret"
    )

    passed = (
        "SOCShield-Production-Secret-12345"
        in response.text
    )

    print_result(
        "Hard-coded Secret Exposure",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Secret exposed by endpoint: {passed}"
    )


# ============================================================
# 6. BROKEN ACCESS CONTROL
# ============================================================

def test_broken_access_control():

    response = requests.get(
        f"{BASE_URL}/admin"
    )

    passed = (
        response.status_code == 200
        and "Admin Panel" in response.text
    )

    print_result(
        "Broken Access Control",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Admin panel accessible without authentication: {passed}"
    )


# ============================================================
# RUN ALL TESTS
# ============================================================

print()
print("=" * 70)
print("SOCShield - Secure Code Review Security Test Suite")
print("=" * 70)
print()

test_sql_injection()
test_command_injection()
test_path_traversal()
test_stored_xss()
test_hardcoded_secret()
test_broken_access_control()

print()
print("=" * 70)
print("SECURITY VALIDATION COMPLETE")
print("=" * 70)