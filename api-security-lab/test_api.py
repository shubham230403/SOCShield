
import requests

BASE_URL = "http://127.0.0.1:5001"

USERNAME = "shubham"
PASSWORD = "security123"

OWN_ACCOUNT = "1002"
OTHER_ACCOUNT = "1001"


def print_result(test_name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {test_name}")


print("=" * 65)
print("SOCShield - API Security Automated Test")
print("=" * 65)

# --------------------------------------------------
# 1. Authentication Test
# --------------------------------------------------

print("\n[1] Testing JWT authentication...")

login_response = requests.post(
    f"{BASE_URL}/login",
    json={
        "username": USERNAME,
        "password": PASSWORD
    }
)

if login_response.status_code != 200:
    print_result("JWT authentication", False)
    print("Login failed.")
    exit()

token = login_response.json()["token"]

print_result("JWT authentication", True)


# --------------------------------------------------
# Authorization Header
# --------------------------------------------------

headers = {
    "Authorization": f"Bearer {token}"
}


# --------------------------------------------------
# 2. Authorized Object Access
# --------------------------------------------------

print("\n[2] Testing authorized account access...")

response = requests.get(
    f"{BASE_URL}/api/account/{OWN_ACCOUNT}",
    headers=headers
)

authorized_access = (
    response.status_code == 200
    and response.json().get("owner") == USERNAME
)

print_result(
    "User can access their own account",
    authorized_access
)


# --------------------------------------------------
# 3. BOLA / IDOR Test
# --------------------------------------------------

print("\n[3] Testing BOLA / IDOR protection...")

response = requests.get(
    f"{BASE_URL}/api/account/{OTHER_ACCOUNT}",
    headers=headers
)

bola_blocked = response.status_code == 403

print_result(
    "Unauthorized object access blocked",
    bola_blocked
)

if response.status_code == 403:
    print("Server response:")
    print(response.json())


# --------------------------------------------------
# 4. Security Summary
# --------------------------------------------------

print("\n" + "=" * 65)
print("SECURITY TEST SUMMARY")
print("=" * 65)

if authorized_access and bola_blocked:

    print("PASS: JWT authentication works")
    print("PASS: Authorized object access works")
    print("PASS: BOLA/IDOR protection is working")
    print("\nRESULT: API security controls verified successfully.")

else:

    print("FAIL: One or more security tests failed.")
    print("\nRESULT: Review the API authorization controls.")

print("=" * 65)
