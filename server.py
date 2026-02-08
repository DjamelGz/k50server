from flask import Flask, request
import requests

app = Flask(__name__)

# URL brute du JSON sur GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/TON_UTILISATEUR/k50-server/main/users.json"

def get_users():
    try:
        r = requests.get(GITHUB_RAW_URL)
        r.raise_for_status()
        return r.json()
    except:
        return {}

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
            users = get_users()  # récupère toujours la dernière version du JSON
            name = users.get(user_id, f"Utilisateur {user_id}")
            print(f"✅ Bienvenue {name} ! Heure : {timestamp}")
        else:
            print(f"Impossible de parser les données ATTLOG: {data}")

    return "OK"

@app.route('/iclock/getrequest', methods=['GET'])
def get_request():
    sn = request.args.get("SN")
    info = request.args.get("INFO")
    print(f"📤 COMMAND REQUEST from {sn}, INFO: {info}")

    command = "DATA QUERY USERINFO\n"
    return command

@app.route('/')
def home():
    return "Serveur K50 actif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
