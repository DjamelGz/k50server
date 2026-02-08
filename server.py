from flask import Flask, request
import json
import os

app = Flask(__name__)

# Fichier JSON contenant les utilisateurs
USERS_FILE = "users.json"

# Charger les utilisateurs depuis le JSON au démarrage
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}  # vide si le fichier n'existe pas

@app.route('/iclock/cdata', methods=['POST'])
def receive_data():
    data = request.data.decode(errors="ignore").strip()
    if not data:
        return "OK"

    # Identifier le type de table envoyé
    table = request.args.get("table")

    if table == "ATTLOG":
        # Exemple : '1\t2026-02-07 07:35:52\t0\t1\t0\t0\t0\t0\t0\t0\t'
        fields = data.split('\t')
        if len(fields) >= 2:
            user_id = fields[0]
            timestamp = fields[1]
            # Chercher le nom dans le JSON
            name = users.get(user_id, f"Utilisateur {user_id}")
            print(f"✅ Bienvenue {name} ! Heure : {timestamp}")
        else:
            print(f"Impossible de parser les données ATTLOG: {data}")

    # Si d'autres tables arrivent comme OPERLOG, USERINFO, on peut les ignorer
    return "OK"

@app.route('/iclock/getrequest', methods=['GET'])
def get_request():
    sn = request.args.get("SN")
    info = request.args.get("INFO")  # certaines versions envoient ce paramètre
    print(f"📤 COMMAND REQUEST from {sn}, INFO: {info}")

    # Demander au K50 d’envoyer tous les utilisateurs si nécessaire
    command = "DATA QUERY USERINFO\n"
    return command

@app.route('/')
def home():
    return "Serveur K50 actif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
