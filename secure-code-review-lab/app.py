from flask import Flask, request, render_template_string
import sqlite3
import subprocess
import os
import html
from pathlib import Path

app = Flask(__name__)

DATABASE = "users.db"

# Security configuration
API_SECRET = os.getenv(
    "SOCSHIELD_API_SECRET",
    "development-only-secret"
)

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = (BASE_DIR / "files").resolve()


# ============================================================
# DATABASE
# ============================================================

def initialize_database():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            comment TEXT
        )
    """)

    existing = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    if existing == 0:
        conn.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            [
                ("admin", "admin123", "admin"),
                ("shubham", "security123", "user"),
                ("guest", "guest123", "user")
            ]
        )

    conn.commit()
    conn.close()


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return """
    <h1>SOCShield Secure Code Review Lab</h1>

    <ul>
        <li>/login</li>
        <li>/ping</li>
        <li>/file</li>
        <li>/comment</li>
        <li>/secret</li>
        <li>/admin</li>
    </ul>
    """


# ============================================================
# 1. SQL INJECTION — FIXED
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    result = ""

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect(DATABASE)

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

        conn.close()

        if user:
            result = (
                f"Login successful: "
                f"{user[0]} | Role: {user[1]}"
            )
        else:
            result = "Invalid credentials"

    return render_template_string("""
        <h2>Login</h2>

        <form method="POST">

            Username:
            <input name="username">

            <br><br>

            Password:
            <input name="password" type="password">

            <br><br>

            <button type="submit">Login</button>

        </form>

        <p>{{ result }}</p>

    """, result=result)


# ============================================================
# 2. COMMAND INJECTION — FIXED
# ============================================================

@app.route("/ping")
def ping():

    host = request.args.get(
        "host",
        "127.0.0.1"
    ).strip()

    if not host:
        return "Invalid host", 400

    allowed_chars = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        ".-_"
    )

    if any(
        char not in allowed_chars
        for char in host
    ):
        return "Invalid host", 400

    try:

        result = subprocess.run(
            ["ping", "-n", "1", host],
            capture_output=True,
            text=True,
            timeout=5,
            shell=False
        )

        output = (
            result.stdout +
            result.stderr
        )

    except subprocess.TimeoutExpired:

        return "Ping request timed out", 408

    return f"""
        <h2>Ping Result</h2>
        <pre>{html.escape(output)}</pre>
    """


# ============================================================
# 3. PATH TRAVERSAL — FIXED
# ============================================================

@app.route("/file")
def read_file():

    filename = request.args.get(
        "name",
        "notes.txt"
    )

    # Resolve the requested path.
    requested_path = (
        FILES_DIR / filename
    ).resolve()

    # Make sure the final path remains inside files/.
    try:
        requested_path.relative_to(FILES_DIR)
    except ValueError:
        return "Invalid file path", 403

    if not requested_path.is_file():
        return "File not found", 404

    try:

        content = requested_path.read_text(
            encoding="utf-8"
        )

        return f"""
            <h2>File Content</h2>
            <pre>{html.escape(content)}</pre>
        """

    except Exception:
        return "Unable to read file", 500


# ============================================================
# 4. STORED XSS — FIXED
# ============================================================

@app.route("/comment", methods=["GET", "POST"])
def comment():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        )

        comment_text = request.form.get(
            "comment",
            ""
        )

        conn = sqlite3.connect(DATABASE)

        conn.execute(
            """
            INSERT INTO comments
            (username, comment)
            VALUES (?, ?)
            """,
            (
                username,
                comment_text
            )
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect(DATABASE)

    comments = conn.execute(
        """
        SELECT username, comment
        FROM comments
        """
    ).fetchall()

    conn.close()

    output = "<h2>Comments</h2>"

    for username, comment_text in comments:

        # Escape user-controlled HTML before rendering.
        safe_username = html.escape(username)
        safe_comment = html.escape(comment_text)

        output += f"""
            <div>
                <b>{safe_username}</b>:
                {safe_comment}
            </div>
        """

    output += """
        <hr>

        <form method="POST">

            Username:
            <input name="username">

            <br><br>

            Comment:
            <textarea name="comment"></textarea>

            <br><br>

            <button type="submit">
                Submit Comment
            </button>

        </form>
    """

    return output


# ============================================================
# 5. HARDCODED SECRET — FIXED
# ============================================================

@app.route("/secret")
def secret():

    # Do not expose secrets through application responses.
    return """
        <h2>Application Configuration</h2>
        <p>Configuration is protected.</p>
    """


# ============================================================
# 6. BROKEN ACCESS CONTROL — FIXED
# ============================================================

@app.route("/admin")
def admin_panel():

    # Demo authorization control.
    # In a real application, identity should come
    # from a properly authenticated session/JWT.

    username = request.headers.get(
        "X-Demo-User"
    )

    if username != "admin":
        return "Forbidden", 403

    return """
        <h1>Admin Panel</h1>

        <p>
            Administrative functions available.
        </p>

        <ul>
            <li>Manage users</li>
            <li>View system configuration</li>
            <li>Manage security settings</li>
        </ul>
    """


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    initialize_database()

    FILES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    notes_file = FILES_DIR / "notes.txt"

    if not notes_file.exists():

        notes_file.write_text(
            "SOCShield Secure Code Review Lab\n"
            "This is a demo file.\n",
            encoding="utf-8"
        )

    print("=" * 60)
    print("SOCShield - Secure Code Review Lab")
    print("=" * 60)
    print("Application: http://127.0.0.1:5003")
    print("Mode: REMEDIATED")
    print("SQL Injection: FIXED")
    print("Command Injection: FIXED")
    print("Path Traversal: FIXED")
    print("Stored XSS: FIXED")
    print("Hard-coded Secret: FIXED")
    print("Broken Access Control: FIXED")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5003,
        debug=False
    )