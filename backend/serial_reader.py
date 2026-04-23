import serial
import json
import time
from db import insert_sensor_data

# ── SERIAL CONFIG ─────────────────────────────
SERIAL_PORT = "COM3"
BAUD_RATE = 115200

def start_serial_reader():
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

                print("✅ Stored:", data)

            except json.JSONDecodeError:
                print("⚠️ Invalid JSON skipped")

        except Exception as e:
            print("❌ Error:", e)