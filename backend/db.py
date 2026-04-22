from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["iot_database"]
collection = db["sensor_data"]

def insert_sensor_data(data):
    data["created_at"] = datetime.utcnow()
    collection.insert_one(data)

def get_latest_data(limit=20):
    return list(collection.find().sort("created_at", -1).limit(limit))