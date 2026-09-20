from flask import Flask, request, jsonify
import sqlite3
import subprocess
import os

app = Flask(__name__)


def get_db():
    return sqlite3.connect("users.db")


@app.route("/user")
def get_user():
    username = request.args.get("username")

    conn = get_db()
    cursor = conn.cursor()

    # VULNERABILITY 1: SQL Injection
    query = f"SELECT id, username, email FROM users WHERE username = '{username}'"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user[0],
        "username": user[1],
        "email": user[2]
    })


@app.route("/search")
def search():
    query = request.args.get("q", "")

    # VULNERABILITY 2: Command Injection
    result = subprocess.check_output(
        f"grep -R '{query}' ./data",
        shell=True
    )

    return result.decode()


@app.route("/download")
def download():
    filename = request.args.get("file", "")

    # VULNERABILITY 3: Path Traversal
    path = os.path.join("uploads", filename)

    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


@app.route("/safe-user")
def safe_user():
    username = request.args.get("username")

    conn = get_db()
    cursor = conn.cursor()

    # SAFE: Parameterized SQL query
    cursor.execute(
        "SELECT id, username, email FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user[0],
        "username": user[1],
        "email": user[2]
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


if __name__ == "__main__":
    app.run(debug=True)
