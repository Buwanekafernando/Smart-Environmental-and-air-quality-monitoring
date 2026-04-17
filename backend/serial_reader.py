import time
import random
from db import collection

def generate_data():
    current_aqi = 50.0
    current_co = 5.0
    current_temp = 25.0
    current_humidity = 60.0

    while True:
        # Smooth random walk
        current_aqi = max(0, min(500, current_aqi + random.uniform(-15, 15)))
        current_co = max(0, min(100, current_co + random.uniform(-2, 2)))
        current_temp = max(15, min(40, current_temp + random.uniform(-0.5, 0.5)))
        current_humidity = max(30, min(90, current_humidity + random.uniform(-1, 1)))

        # Occasional smoking spike (2% chance)
        if random.random() < 0.02:
            current_co += random.uniform(20, 50)
            current_aqi += random.uniform(50, 100)

        data = {
            "air_quality": round(current_aqi, 2),
            "co_level": round(current_co, 2),
            "temperature": round(current_temp, 2),
            "humidity": round(current_humidity, 2),
            "motion_detected": random.choice([0, 1, 0, 0]), # favor no motion
            "timestamp": time.time()
        }

        collection.insert_one(data)
        print("Inserted:", data)

        time.sleep(3)  # every 3 seconds