from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import threading

from db import get_latest_data
from serial_reader import start_serial_reader
from ml_services import MLService

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# 🚀 Start serial reader in background
threading.Thread(target=start_serial_reader, args=(socketio,), daemon=True).start()


# ── HELPERS ─────────────────────────────
def get_history_data(limit=20):
    data = get_latest_data(limit)
    for i, d in enumerate(data):
        d["_id"] = str(d["_id"])
        
        # ✅ Add numeric conversion layer
        raw_mq135 = d.get("mq135", 0)
        raw_mq7 = d.get("mq7", 0)
        
        d["aqi_numeric"] = MLService.calculate_aqi(raw_mq135)
        d["co_percent"] = MLService.calculate_co_percent(raw_mq7)
        
        if i == 0:
            d["ai_status"] = MLService.predict_air_quality(raw_mq7, raw_mq135, d.get("temperature", 0), d.get("humidity", 0))
        
    return data


# ── ROUTES ─────────────────────────────

@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(get_history_data(2000))


@app.route("/api/data/latest", methods=["GET"])
def get_latest():
    latest = get_history_data(1)
    return jsonify(latest[0] if latest else {})


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
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)