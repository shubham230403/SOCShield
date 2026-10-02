import requests
import jwt
import time
from datetime import datetime, timedelta, timezone


BASE_URL = "http://127.0.0.1:5002"

SECRET_KEY = "socshield-jwt-secret-32-bytes-long!"


# ============================================================
# HELPER
# ============================================================

def print_test(name, passed, details=""):

    status = "PASS" if passed else "FAIL"

    print("=" * 65)
    print(f"{status}: {name}")

    if details:
        print(details)


# ============================================================
# 1. USER ENUMERATION TEST
# ============================================================

def test_generic_authentication_error():

    unknown_user = requests.post(
        f"{BASE_URL}/login",
        json={
            "username": "does-not-exist",
            "password": "wrongpassword"
        }
    )

    known_user_wrong_password = requests.post(
        f"{BASE_URL}/login",
        json={
            "username": "shubham",
            "password": "wrongpassword"
        }
    )

    same_response = (
        unknown_user.status_code
        == known_user_wrong_password.status_code
        == 401
        and unknown_user.json()
        == known_user_wrong_password.json()
    )

    print_test(
        "Generic authentication error",
        same_response,
        f"Unknown user: {unknown_user.status_code} "
        f"{unknown_user.json()}\n"
        f"Known user wrong password: "
        f"{known_user_wrong_password.status_code} "
        f"{known_user_wrong_password.json()}"
    )


# ============================================================
# 2. RATE LIMITING TEST
# ============================================================

def test_rate_limiting():

    username = f"automated-rate-{int(time.time())}"

    results = []

    for _ in range(6):

        response = requests.post(
            f"{BASE_URL}/login",
            json={
                "username": username,
                "password": "wrongpassword"
            }
        )

        results.append(response.status_code)

    passed = (
        results[:5] == [401, 401, 401, 401, 401]
        and results[5] == 429
    )

    print_test(
        "Login rate limiting",
        passed,
        f"HTTP results: {results}"
    )


# ============================================================
# 3. VALID LOGIN / JWT ISSUANCE
# ============================================================

def test_valid_login():

    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "username": "shubham",
            "password": "security123"
        }
    )

    data = response.json()

    token = data.get("token")

    passed = (
        response.status_code == 200
        and token is not None
    )

    print_test(
        "Valid login and JWT issuance",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Token received: {token is not None}"
    )

    return token


# ============================================================
# 4. PROTECTED API WITHOUT TOKEN
# ============================================================

def test_missing_token():

    response = requests.get(
        f"{BASE_URL}/api/profile"
    )

    passed = response.status_code == 401

    print_test(
        "Protected API rejects missing token",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Response: {response.text}"
    )


# ============================================================
# 5. VALID JWT ACCESS
# ============================================================

def test_valid_token(token):

    response = requests.get(
        f"{BASE_URL}/api/profile",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    passed = (
        response.status_code == 200
        and response.json().get("username") == "shubham"
    )

    print_test(
        "Valid JWT grants authorized access",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Response: {response.text}"
    )


# ============================================================
# 6. JWT TAMPERING TEST
# ============================================================

def test_tampered_token(token):

    decoded = jwt.decode(
        token,
        options={
            "verify_signature": False
        }
    )

    # Attempt to change user privileges.
    decoded["role"] = "admin"

    # Sign the modified token with an attacker-controlled
    # secret. The server should reject it.
    tampered_token = jwt.encode(
        decoded,
        "attacker-controlled-test-secret-32-bytes!",
        algorithm="HS256"
    )

    response = requests.get(
        f"{BASE_URL}/api/profile",
        headers={
            "Authorization": f"Bearer {tampered_token}"
        }
    )

    passed = response.status_code == 401

    print_test(
        "Tampered JWT rejected",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Response: {response.text}"
    )


# ============================================================
# 7. EXPIRED JWT TEST
# ============================================================

def test_expired_token():

    payload = {
        "username": "shubham",
        "role": "user",
        "exp": (
            datetime.now(timezone.utc)
            - timedelta(minutes=5)
        )
    }

    expired_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    response = requests.get(
        f"{BASE_URL}/api/profile",
        headers={
            "Authorization": f"Bearer {expired_token}"
        }
    )

    passed = response.status_code == 401

    print_test(
        "Expired JWT rejected",
        passed,
        f"HTTP status: {response.status_code}\n"
        f"Response: {response.text}"
    )


# ============================================================
# MAIN
# ============================================================

print()
print("=" * 65)
print("SOCShield - JWT Security Automated Test Suite")
print("=" * 65)
print()


test_generic_authentication_error()

test_rate_limiting()

token = test_valid_login()

test_missing_token()

if token:
    test_valid_token(token)
    test_tampered_token(token)

test_expired_token()


print()
print("=" * 65)
print("JWT SECURITY TESTING COMPLETE")
print("=" * 65)