import serial
import json
import time
from pymongo import MongoClient
from datetime import datetime

# ── SERIAL CONFIG ─────────────────────────────
SERIAL_PORT = "COM3"      # 🔴 change this (e.g., COM3 or /dev/ttyUSB0)
BAUD_RATE = 115200

# ── MONGODB CONFIG ───────────────────────────
client = MongoClient("mongodb://localhost:27017/")
db = client["iot_db"]
collection = db["sensor_data"]

# ── CONNECT SERIAL ───────────────────────────
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # allow ESP32 reset
    print("✅ Connected to Serial")
except Exception as e:
    print("❌ Serial connection error:", e)
    exit()

print("📡 Listening for JSON data...\n")

# ── READ LOOP ────────────────────────────────
while True:
    try:
        line = ser.readline().decode("utf-8").strip()

        if not line:
            continue

        # Debug: print raw line
        print("RAW:", line)

        # ── Parse JSON ───────────────────────
        try:
            data = json.loads(line)

            # Add timestamp
            data["timestamp"] = datetime.utcnow()

            # Insert into MongoDB
            collection.insert_one(data)

            print("✅ Stored:", data)

        except json.JSONDecodeError:
            print("⚠️ Skipping invalid JSON")

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
        break

    except Exception as e:
        print("❌ Error:", e)