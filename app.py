from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ✅ Clave secreta tomada desde Render (Environment Variable)
FINTOC_SECRET_KEY = os.getenv("FINTOC_SECRET_KEY")

@app.route("/", methods=["GET"])
def home():
    return "API de integración Shopify + Fintoc lista"

@app.route("/nuevo-pedido", methods=["POST"])
def nuevo_pedido():
    data = request.json
    amount = int(data.get("amount", 1000))  # en pesos chilenos
    currency = "CLP"

    # 🔐 Crear PaymentIntent en Fintoc (LIVE)
    fintoc_response = requests.post(
        "https://api.fintoc.com/v1/payment_intents",
        headers={
            # ❌ No uses "Bearer" en la clave secreta LIVE
            "Authorization": FINTOC_SECRET_KEY,
            "Content-Type": "application/json"
        },
        json={
            "amount": amount,
            "currency": currency,
            "payment_description": "Pago desde Shopify",
            "recipient_email": "juanneira43@gmail.com"  # ✅ tu correo real
        }
    )

    if fintoc_response.status_code == 201:
        payment_data = fintoc_response.json()
        return jsonify({
            # ✅ CAMBIO CLAVE AQUÍ (antes estaba .get("checkout_url"))
            "link_de_pago": payment_data.get("payment_url")
        }), 200
    else:
        return jsonify({
            "error": "Error al crear el link de pago",
            "detalle": fintoc_response.text
        }), 500
