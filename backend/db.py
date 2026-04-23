from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["iot_db"]
collection = db["sensor_data"]

def insert_sensor_data(data):
    data["timestamp"] = datetime.utcnow()
    collection.insert_one(data)

def get_latest_data(limit=20):
    return list(collection.find().sort("timestamp", -1).limit(limit))