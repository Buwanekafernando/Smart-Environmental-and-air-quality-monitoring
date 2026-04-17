from flask import Flask, jsonify, request
from flask_cors import CORS
from db import collection
import threading
from serial_reader import generate_data
from ml_services import MLService

app = Flask(__name__)
CORS(app)

# Start background data generation
threading.Thread(target=generate_data, daemon=True).start()

def get_history_data(limit=20):
    data = list(collection.find().sort("timestamp", -1).limit(limit))
    for d in data:
        d["_id"] = str(d["_id"])
    return data

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
    history = get_history_data(200) # get more data for peaks
    return jsonify(MLService.get_peak_hours(history))

@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    req = request.get_json() or {}
    message = req.get("message", "").lower()
    latest = get_history_data(1)
    current = latest[0] if latest else {}
    
    if "safe" in message or "health" in message:
        risk = MLService.classify_health_risk(current)
        return jsonify({"reply": f"The current health risk status is {risk['status']}."})
    elif "co " in message or "smoking" in message:
        return jsonify({"reply": f"Current CO level is {current.get('co_level', 0)} ppm."})
    else:
        return jsonify({"reply": "I am monitoring the environment. Try asking me 'Is the air safe?'"})

if __name__ == "__main__":
    app.run(debug=True)