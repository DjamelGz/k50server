from flask import Flask, request

app = Flask(__name__)

# Dictionnaire ID → Nom, sera rempli automatiquement depuis le K50
users = {}

@app.route('/iclock/cdata', methods=['POST'])
def receive_data():
    data = request.data.decode(errors="ignore").strip()
    if not data:
        return "OK"

    # Identifier le type de table envoyé
    table = request.args.get("table")

    if table == "USERINFO":
        # K50 envoie les infos utilisateurs
        # Exemple de ligne : '1\tDjamel\t1\t1\t0\t0\t0\t0\t0\t0\t'
        lines = data.split('\n')
        for line in lines:
            fields = line.strip().split('\t')
            if len(fields) >= 2:
                user_id = fields[0]
                name = fields[1]
                users[user_id] = name
                print(f"📥 Utilisateur ajouté / mis à jour : {user_id} → {name}")
        return "OK"

    elif table == "ATTLOG":
        # Filtrer uniquement les vrais pointages
        # Exemple : '1\t2026-02-07 07:35:52\t0\t1\t0\t0\t0\t0\t0\t0\t'
        fields = data.split('\t')
        if len(fields) >= 2:
            user_id = fields[0]
            timestamp = fields[1]
            name = users.get(user_id, f"Utilisateur {user_id}")
            print(f"✅ Bienvenue {name} ! Heure : {timestamp}")
        else:
            print(f"Impossible de parser les données ATTLOG: {data}")
        return "OK"

    else:
        # Ignorer les autres tables comme OPERLOG
        return "OK"

@app.route('/iclock/getrequest', methods=['GET'])
def get_request():
    sn = request.args.get("SN")
    print(f"📤 COMMAND REQUEST from {sn}")

    # Demander au K50 d’envoyer tous les utilisateurs
    command = "DATA QUERY USERINFO\n"
    return command

@app.route('/')
def home():
    return "Serveur K50 actif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
