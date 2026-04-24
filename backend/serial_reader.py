import serial
import json
import time
from db import insert_sensor_data
from ml_services import MLService

# ── SERIAL CONFIG ─────────────────────────────
SERIAL_PORT = "COM7"
BAUD_RATE = 115200

def start_serial_reader(socketio=None):
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print("✅ Connected to Serial")
    except Exception as e:
        print("❌ Serial connection error:", e)
        return

    print("📡 Listening for JSON data...\n")

    while True:
        try:
            line = ser.readline().decode("utf-8").strip()

            if not line:
                continue

            print("RAW:", line)

            # ✅ Only process JSON lines
            if not line.startswith("{"):
                continue

            try:
                data = json.loads(line)

                # Optional: clean / normalize
                data["mq7"] = min(data.get("mq7", 0), 4095)
                data["mq135"] = min(data.get("mq135", 0), 4095)

                insert_sensor_data(data)

                # Get ML prediction
                ai_status = MLService.predict_air_quality(
                    data.get("mq7", 0),
                    data.get("mq135", 0),
                    data.get("temperature", 0),
                    data.get("humidity", 0)
                )

                # Enhance data with required computed fields before emitting
                data["aqi_numeric"] = MLService.calculate_aqi(data.get("mq135", 0))
                data["co_percent"] = MLService.calculate_co_percent(data.get("mq7", 0))
                data["ai_status"] = ai_status
                
                if "_id" in data:
                    data["_id"] = str(data["_id"])

                if socketio:
                    socketio.emit('sensor_update', data)

                print("✅ Stored & Emitted:", data)

            except json.JSONDecodeError:
                print("⚠️ Invalid JSON skipped")

        except Exception as e:
            print("❌ Error:", e)