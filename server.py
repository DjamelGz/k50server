from flask import Flask, request

app = Flask(__name__)

# Dictionnaire ID → Nom (ici juste Djamel)
users = {
    "1": "Djamel"
}

@app.route('/iclock/cdata', methods=['POST'])
def receive_data():
    data = request.data.decode(errors="ignore").strip()
    if not data:
        return "OK"

    # Exemple de data reçue : '1\t2026-02-07 07:35:52\t0\t1\t0\t0\t0\t0\t0\t0\t'
    fields = data.split('\t')
    if len(fields) >= 2:
        user_id = fields[0]
        timestamp = fields[1]
        name = users.get(user_id, f"Utilisateur {user_id}")
        print(f"Bienvenue {name} ! Heure : {timestamp}")
    else:
        print(f"Requête reçue mais impossible de parser les données: {data}")

    return "OK"

@app.route('/iclock/getrequest', methods=['GET'])
def get_request():
    sn = request.args.get("SN")
    print(f"📤 COMMAND REQUEST from {sn}")

    # On demande au K50 d’envoyer les templates si nécessaire
    command = "DATA QUERY FINGERTMP\n"
    return command

@app.route('/')
def home():
    return "Serveur K50 actif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
