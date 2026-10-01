from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

DATABASE = "users.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    existing = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    if existing == 0:
        conn.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            [
                ("admin", "admin123", "administrator"),
                ("shubham", "security123", "analyst"),
                ("guest", "guest123", "user")
            ]
        )

    conn.commit()
    conn.close()


PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SOCShield SQL Injection Lab</title>

    <style>
        body {
            font-family: Arial;
            max-width: 700px;
            margin: 50px auto;
        }

        input {
            padding: 10px;
            width: 300px;
            margin: 5px 0;
        }

        button {
            padding: 10px 20px;
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f2f2f2;
        }
    </style>
</head>

<body>

<h1>SOCShield SQL Injection Lab</h1>

<p>
Controlled application-security lab for demonstrating
SQL Injection detection and remediation.
</p>

<form method="POST">

    <label>Username</label><br>
    <input name="username" placeholder="Enter username">

    <br>

    <label>Password</label><br>
    <input name="password" type="password" placeholder="Enter password">

    <br><br>

    <button type="submit">Login</button>

</form>

{% if result %}
<div class="result">
    <strong>Result:</strong>
    <p>{{ result }}</p>
</div>
{% endif %}

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():

    result = None

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()

        # REMEDIATED: Parameterized SQL query
        query = """
            SELECT username, role
            FROM users
            WHERE username = ?
            AND password = ?
        """

        try:

            user = conn.execute(
                query,
                (username, password)
            ).fetchone()

            if user:
                result = (
                    f"Login successful. "
                    f"User: {user['username']} | "
                    f"Role: {user['role']}"
                )
            else:
                result = "Invalid credentials."

        except sqlite3.Error as error:

            result = f"Database error: {error}"

        finally:

            conn.close()

    return render_template_string(PAGE, result=result)


if __name__ == "__main__":

    initialize_database()

    print("=" * 55)
    print("SOCShield - SQL Injection Security Lab")
    print("=" * 55)
    print("Application: http://127.0.0.1:5000")
    print("Mode: REMEDIATED")
    print("Protection: Parameterized SQL Queries")
    print("=" * 55)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )