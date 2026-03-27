from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/data", methods=["GET"])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

app.run(port=5000)