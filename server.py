from flask import Flask, request

app = Flask(__name__)

@app.route('/iclock/cdata', methods=['POST'])
def receive_data():
    print("📥 DATA FROM K50")
    print(request.data.decode(errors="ignore"))
    return "OK"

@app.route('/iclock/getrequest', methods=['GET'])
def get_request():
    sn = request.args.get("SN")
    print(f"📤 COMMAND REQUEST from {sn}")

    # Ask device to send ALL fingerprint templates
    command = "DATA QUERY FINGERTMP\n"
    return command

@app.route('/')
def home():
    return "Serveur K50 actif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
