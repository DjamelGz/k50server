from flask import Flask, request
import json
import os

app = Flask(__name__)

# Charger les utilisateurs depuis le JSON
USERS_FILE = "users.json"
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

@app.route('/iclock/cdata', methods=['POST'])
def receive_data():
    data = request.data.decode(errors="ignore").strip()
    if not data:
        return "OK"

    table = request.args.get("table")
    if table == "ATTLOG":
        # Exemple : '1\t2026-02-07 07:35:52\t0\t1\t0\t0\t0\t0\t0\t0\t'
        fields = data.split('\t')
        if len(fields) >= 2:
            user_id = fields[0]
            timestamp = fields[1]
            name = users.get(user_id, f"Utilisateur {user_id}")
            print(f"✅ Bienvenue {name} ! Heure : {timestamp}")
    return "OK"

@app.route('/')
def home():
    return "Serveur K50 actif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
