import time
import random
from db import collection

def generate_data():
    while True:
        data = {
            "air_quality": random.randint(100, 3000),
            "co_level": random.randint(100, 2000),
            "temperature": round(random.uniform(25, 35), 2),
            "humidity": round(random.uniform(50, 80), 2),
            "motion_detected": random.choice([0, 1]),
            "timestamp": time.time()
        }

        collection.insert_one(data)
        print("Inserted:", data)

        time.sleep(3)  # every 3 seconds