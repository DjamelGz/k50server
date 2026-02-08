from flask import Flask, request
from pyzk.zk import ZK
from datetime import datetime

app = Flask(__name__)

# Dictionnaire ID → Nom, sera rempli automatiquement depuis le K50 via pyzk
users = {}

# Configuration du K50 pour pyzk
IP_K50 = "192.168.137.2"  # change avec l'IP de ton K50
PORT_K50 = 4370
TIMEOUT = 5

def update_users_from_k50():
    """Récupère tous les utilisateurs depuis le K50 et met à jour le dictionnaire users"""
    global users
    try:
        zk = ZK(IP_K50, port=PORT_K50, timeout=TIMEOUT)
        conn = zk.connect()
        conn.disable_device()
        fetched_users = conn.get_users()
        for u in fetched_users:
            users[u.user_id] = u.name
        conn.enable_device()
        conn.disconnect()
        print(f"📥 {len(fetched_users)} utilisateurs récupérés depuis le K50")
    except Exception as e:
        print("❌ Impossible de récupérer les utilisateurs :", e)

# Mettre à jour les utilisateurs au démarrage du serveur
update_users_from_k50()

@app.route('/iclock/cdata', methods=['POST'])
def receive_data():
    data = request.data.decode(errors="ignore").strip()
    if not data:
        return "OK"

    table = request.args.get("table")

    if table == "ATTLOG":
        fields = data.split('\t')
        if len(fields) >= 2:
            user_id = fields[0]
            timestamp = fields[1]
            name = users.get(user_id, f"Utilisateur {user_id}")
            print(f"✅ Bienvenue {name} ! Heure : {timestamp}")
        else:
            print(f"⚠️ Impossible de parser les données ATTLOG: {data}")
        return "OK"
    else:
        return "OK"  # Ignorer les autres tables

@app.route('/update_users', methods=['GET'])
def update_users_endpoint():
    """Endpoint pour mettre à jour manuellement les utilisateurs depuis le K50"""
    update_users_from_k50()
    return f"✅ Dictionnaire mis à jour, {len(users)} utilisateurs disponibles"

@app.route('/')
def home():
    return "Serveur K50 actif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
