from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Clave secreta de Fintoc (LIVE)
FINTOC_SECRET_KEY = os.getenv("FINTOC_SECRET_KEY")

@app.route("/", methods=["GET"])
def home():
    return "API de integración Shopify + Fintoc lista"

@app.route("/nuevo-pedido", methods=["POST"])
def nuevo_pedido():
    data = request.json
    amount = int(data.get("amount", 1000))  # en pesos chilenos
    currency = "CLP"

    # Crear un PaymentIntent en Fintoc
    fintoc_response = requests.post(
        "https://api.fintoc.com/v1/payment_intents",
        headers={
            "Authorization": f"Bearer {FINTOC_SECRET_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "amount": amount,
            "currency": currency,
            "payment_description": "Pago desde Shopify",
            "recipient_email": "cliente@ejemplo.cl"
        }
    )

    if fintoc_response.status_code == 201:
        payment_data = fintoc_response.json()
        return jsonify({
            "link_de_pago": payment_data.get("checkout_url")
        }), 200
    else:
        return jsonify({
            "error": "Error al crear el link de pago",
            "detalle": fintoc_response.text
        }), 500
