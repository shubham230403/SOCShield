
from flask import Flask, jsonify, request
import jwt
from functools import wraps
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

SECRET_KEY = "socshield-lab-secret"

# Simulated users
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "shubham": {
        "password": "security123",
        "role": "user"
    }
}

# Simulated account records
ACCOUNTS = {
    "1001": {
        "owner": "admin",
        "balance": 150000,
        "account_type": "savings"
    },
    "1002": {
        "owner": "shubham",
        "balance": 75000,
        "account_type": "savings"
    },
    "1003": {
        "owner": "guest",
        "balance": 25000,
        "account_type": "current"
    }
}


def create_token(username):

    payload = {
        "username": username,
        "role": USERS[username]["role"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )


def token_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({
                "error": "Authorization token required"
            }), 401

        try:

            if token.startswith("Bearer "):
                token = token.split(" ", 1)[1]

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = payload

        except jwt.ExpiredSignatureError:

            return jsonify({
                "error": "Token expired"
            }), 401

        except jwt.InvalidTokenError:

            return jsonify({
                "error": "Invalid token"
            }), 401

        return function(*args, **kwargs)

    return wrapper


@app.route("/")
def home():

    return jsonify({
        "application": "SOCShield API Security Lab",
        "version": "1.0",
        "status": "running"
    })


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if username not in USERS:
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    if USERS[username]["password"] != password:
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    token = create_token(username)

    return jsonify({
        "message": "Login successful",
        "username": username,
        "role": USERS[username]["role"],
        "token": token
    })


@app.route("/api/account/<account_id>", methods=["GET"])
@token_required
def get_account(account_id):

    if account_id not in ACCOUNTS:

        return jsonify({
            "error": "Account not found"
        }), 404

    account = ACCOUNTS[account_id]

    # REMEDIATED:
    # Verify that the authenticated user owns
    # the requested account.
    if account["owner"] != request.user["username"]:

        return jsonify({
            "error": "Forbidden",
            "message": "You are not authorized to access this account"
        }), 403

    return jsonify({
        "account_id": account_id,
        "owner": account["owner"],
        "balance": account["balance"],
        "account_type": account["account_type"]
    })


@app.route("/api/profile", methods=["GET"])
@token_required
def profile():

    username = request.user["username"]

    return jsonify({
        "username": username,
        "role": request.user["role"]
    })


if __name__ == "__main__":

    print("=" * 60)
    print("SOCShield - REST API Security Lab")
    print("=" * 60)
    print("Application: http://127.0.0.1:5001")
    print("Mode: REMEDIATED")
    print("Vulnerability: BOLA / IDOR")
    print("Protection: Object-Level Authorization")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )
