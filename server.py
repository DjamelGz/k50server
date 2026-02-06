from flask import Flask, request

app = Flask(__name__)

# Dictionnaire ID → Nom
users = {"1": "Djamel"}

@app.route('/iclock/cdata', methods=['GET', 'POST'])
def receive_data():
    # Récupère la data selon la méthode
    if request.method == "POST":
        data = request.data.decode(errors="ignore").strip()
    else:  # GET
        data = request.query_string.decode(errors="ignore").strip()
    
    if not data:
        return "OK"

    # Essayer d’extraire l’ID et l’heure depuis les données GET/POST
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
    return ""  # rien à renvoyer

@app.route('/')
def home():
    return "Serveur K50 actif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
