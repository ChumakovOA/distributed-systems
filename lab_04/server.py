from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import ssl
import sys
import secrets

app = Flask(__name__)

# загрузка ключа
with open("encryption_key.txt", "rb") as f:
    key = f.read()

fernet = Fernet(key)

# список токенов
valid_tokens = []

# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():

    token = secrets.token_hex(16)

    valid_tokens.append(token)

    return jsonify({
        "token": token
    })

# =========================
# API
# =========================

@app.route("/api/data", methods=["POST"])
def handle():

    token = request.headers.get("Authorization")

    if token not in valid_tokens:

        return jsonify({
            "error": "unauthorized"
        }), 401

    encrypted = request.json["data"]

    try:

        decrypted = fernet.decrypt(
            encrypted.encode()
        ).decode()

        print("Decrypted:", decrypted)

        return jsonify({
            "status": "ok",
            "message": decrypted
        })

    except:

        return jsonify({
            "error": "decryption failed"
        }), 400

# =========================
# TLS
# =========================

if __name__ == "__main__":

    port = int(sys.argv[1])

    context = ssl.SSLContext(
        ssl.PROTOCOL_TLS_SERVER
    )

    context.load_cert_chain(
        "server_cert.pem",
        "server_key.pem"
    )

    context.load_verify_locations(
        "ca_cert.pem"
    )

    context.verify_mode = ssl.CERT_REQUIRED

    app.run(
        host="0.0.0.0",
        port=port,
        ssl_context=context
    )