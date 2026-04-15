from flask import Flask, jsonify
from flask_cors import CORS
from db import collection
import threading
from serial_reader import generate_data

app = Flask(__name__)
CORS(app)

# Start background data generation
threading.Thread(target=generate_data, daemon=True).start()

# API to get latest data
@app.route("/api/data", methods=["GET"])
def get_data():
    data = list(collection.find().sort("timestamp", -1).limit(20))

    for d in data:
        d["_id"] = str(d["_id"])  # convert ObjectId

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)