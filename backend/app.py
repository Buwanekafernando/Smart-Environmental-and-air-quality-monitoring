from flask import Flask, jsonify, request
from flask_cors import CORS
import threading

from db import get_latest_data
from serial_reader import start_serial_reader
from ml_services import MLService

app = Flask(__name__)
CORS(app)

# 🚀 Start serial reader in background
threading.Thread(target=start_serial_reader, daemon=True).start()


# ── HELPERS ─────────────────────────────
def get_history_data(limit=20):
    data = get_latest_data(limit)
    for d in data:
        d["_id"] = str(d["_id"])
    return data


# ── ROUTES ─────────────────────────────

@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(get_history_data(20))


@app.route("/api/trends", methods=["GET"])
def get_trends():
    history = get_history_data(50)
    return jsonify(MLService.analyze_trends(history))


@app.route("/api/co-analysis", methods=["GET"])
def get_co_analysis():
    history = get_history_data(10)
    return jsonify(MLService.detect_smoking(history))


@app.route("/api/health-risk", methods=["GET"])
def get_health_risk():
    latest = get_history_data(1)
    if not latest:
        return jsonify({"status": "UNKNOWN"})
    return jsonify(MLService.classify_health_risk(latest[0]))


@app.route("/api/peak-hours", methods=["GET"])
def get_peak_hours_api():
    history = get_history_data(200)
    return jsonify(MLService.get_peak_hours(history))


@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    req = request.get_json() or {}
    message = req.get("message", "").lower()

    latest = get_history_data(1)
    current = latest[0] if latest else {}

    # ⚠️ NOTE: co_level is STRING from Arduino
    co_level = current.get("co_level", "UNKNOWN")

    if "safe" in message or "health" in message:
        risk = MLService.classify_health_risk(current)
        return jsonify({"reply": f"The current health risk is {risk['status']}."})

    elif "co" in message or "smoking" in message:
        return jsonify({"reply": f"Current CO condition is {co_level}."})

    else:
        return jsonify({
            "reply": "I am monitoring the environment. Try asking 'Is the air safe?'"
        })

@app.route("/api/pollution-cost", methods=["GET"])
def get_pollution_cost():
    history = get_history_data(100)
    return jsonify(MLService.calculate_pollution_cost(history))


@app.route("/api/fire-alert", methods=["GET"])
def get_fire_alert():
    latest = get_history_data(1)
    if not latest:
        return jsonify({"alert": False})

    return jsonify(MLService.detect_fire_risk(latest[0]))


# ── MAIN ─────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)