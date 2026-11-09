from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    @app.post("/moderate")
    def moderate():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="JSON object required"), 400
        message = data.get("message")
        if not isinstance(message, str) or not message.strip():
            return jsonify(error="Invalid message"), 400
        mots = message.lower().split()
        decision = "bloquer" if "spam" in mots else "autoriser"
        return jsonify(decision=decision), 200

    return app
