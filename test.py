import os
import sqlite3
import pickle
from flask import Flask, request

app = Flask(__name__)


SECRET_API_KEY = "AKIA1234567890EXAMPL" 
JWT_SECRET = "super_secret_key_12345"

@app.route("/api/user", methods=["GET"])
def get_user():
    username = request.args.get("username")

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()

    return {"user": result}

@app.route("/api/ping", methods=["POST"])
def ping_server():
    host = request.json.get("host")


    cmd = f"ping -c 1 {host}"
    output = os.popen(cmd).read()  # Contoh eksploitasi payload: "8.8.8.8; cat /etc/passwd"

    return {"output": output}

@app.route("/api/restore-session", methods=["POST"])
def restore_session():
    data = request.data

 
    session_object = pickle.loads(data)

    return {"status": "restored"}

if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0")
