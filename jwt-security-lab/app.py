from flask import Flask, jsonify, request
import jwt
import os
from functools import wraps
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# ============================================================
# JWT SECRET CONFIGURATION
# ============================================================

SECRET_KEY = os.getenv("JWT_SECRET")

if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET environment variable is not set."
    )


# ============================================================
# DEMO USERS
#
# Passwords are stored as hashes instead of plaintext.
# ============================================================

USERS = {
    "admin": {
        "password_hash": generate_password_hash("admin123"),
        "role": "admin"
    },
    "shubham": {
        "password_hash": generate_password_hash("security123"),
        "role": "user"
    }
}


# ============================================================
# LOGIN RATE LIMITING
#
# Lab implementation:
# Maximum 5 failed login attempts per username.
# The 6th failed attempt returns HTTP 429.
#
# Production systems should use a shared solution such as:
# Redis, API Gateway, WAF, or dedicated rate-limit middleware.
# ============================================================

FAILED_ATTEMPTS = {}

MAX_FAILED_ATTEMPTS = 5


def check_rate_limit(username):
    """
    Check whether the username has reached
    the maximum number of failed attempts.
    """

    count = FAILED_ATTEMPTS.get(username, 0)

    if count >= MAX_FAILED_ATTEMPTS:
        return True

    return False


def register_failed_login(username):
    """
    Increment failed login counter.
    """

    FAILED_ATTEMPTS[username] = (
        FAILED_ATTEMPTS.get(username, 0) + 1
    )

    print(
        f"[RATE LIMIT] {username}: "
        f"{FAILED_ATTEMPTS[username]}/{MAX_FAILED_ATTEMPTS}"
    )


def clear_failed_logins(username):
    """
    Reset failed login counter after
    successful authentication.
    """

    FAILED_ATTEMPTS.pop(username, None)


# ============================================================
# JWT TOKEN CREATION
# ============================================================

def create_token(username):

    payload = {
        "username": username,
        "role": USERS[username]["role"],
        "exp": (
            datetime.now(timezone.utc)
            + timedelta(minutes=30)
        )
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )


# ============================================================
# JWT AUTHENTICATION
# ============================================================

def token_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        token = request.headers.get("Authorization")

        # Authorization header missing.
        if not token:

            return jsonify({
                "error": "Authorization token required"
            }), 401

        try:

            # Support:
            # Authorization: Bearer <token>
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
                "error": "Invalid or expired token"
            }), 401

        except jwt.InvalidTokenError:

            return jsonify({
                "error": "Invalid token"
            }), 401

        return function(*args, **kwargs)

    return wrapper


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "application": "SOCShield JWT Security Lab",
        "status": "running",
        "mode": "REMEDIATED",
        "protections": [
            "Authentication rate limiting",
            "Password hashing",
            "Environment-based JWT secret",
            "JWT signature validation",
            "JWT expiration validation",
            "Generic authentication errors"
        ]
    })


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    # --------------------------------------------------------
    # Required-field validation
    # --------------------------------------------------------

    if not username or not password:

        return jsonify({
            "error": "Invalid credentials"
        }), 401


    # --------------------------------------------------------
    # Rate-limit check
    # --------------------------------------------------------

    if check_rate_limit(username):

        print(
            f"[RATE LIMIT] BLOCKED: {username}"
        )

        return jsonify({
            "error": "Too many login attempts. Try again later."
        }), 429


    # --------------------------------------------------------
    # Credential validation
    # --------------------------------------------------------

    user = USERS.get(username)

    if not user or not check_password_hash(
        user["password_hash"],
        password
    ):

        register_failed_login(username)

        # Generic response prevents
        # username enumeration.

        return jsonify({
            "error": "Invalid credentials"
        }), 401


    # --------------------------------------------------------
    # Successful authentication
    # --------------------------------------------------------

    clear_failed_logins(username)

    token = create_token(username)

    return jsonify({
        "message": "Login successful",
        "username": username,
        "role": user["role"],
        "token": token
    })


# ============================================================
# PROTECTED PROFILE API
# ============================================================

@app.route("/api/profile")
@token_required
def profile():

    return jsonify({
        "message": "Profile accessed",
        "username": request.user["username"],
        "role": request.user["role"]
    })


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SOCShield - JWT Security Lab")
    print("=" * 60)
    print("Application: http://127.0.0.1:5002")
    print("Mode: REMEDIATED")
    print(
        "Protections: JWT + Rate Limiting + Password Hashing"
    )
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5002,
        debug=False
    )