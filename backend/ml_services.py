import numpy as np
import pandas as pd
from datetime import datetime
import joblib
import os

# Load model once
try:
    rf_model = joblib.load("air_quality_model.pkl")
except Exception as e:
    print("Warning: Could not load air_quality_model.pkl:", e)
    rf_model = None

class MLService:

    # ─────────────────────────────────────────────
    # 🔁 HELPER: Convert Labels → Numeric Scores
    # ─────────────────────────────────────────────
    @staticmethod
    def map_air_quality(aq):
        mapping = {
            "GOOD": 50,
            "MODERATE": 100,
            "POOR  !": 180,
            "DANGER !!": 250
        }
        return mapping.get(aq, 0)

    @staticmethod
    def map_co_level(co):
        mapping = {
            "SAFE": 10,
            "LOW CO": 30,
            "HIGH CO  !": 70,
            "DANGER CO !!": 120
        }
        return mapping.get(co, 0)

    # ─────────────────────────────────────────────
    # 📏 NUMERIC CONVERSIONS (ADC → SCALE)
    # ─────────────────────────────────────────────
    @staticmethod
    def calculate_aqi(mq135_raw):
        """
        Maps MQ135 raw ADC (0-4095) to AQI (0-500)
        Based on Arduino thresholds: 800, 1500, 2500
        """
        try:
            raw = float(mq135_raw)
            if raw < 800:
                return round((raw / 800) * 50)
            elif raw < 1500:
                return round(50 + ((raw - 800) / 700) * 50)
            elif raw < 2500:
                return round(100 + ((raw - 1500) / 1000) * 100)
            else:
                return round(200 + ((raw - 2500) / 1595) * 300)
        except:
            return 0

    @staticmethod
    def calculate_co_percent(mq7_raw):
        """
        Maps MQ7 raw ADC (0-4095) to CO % (0-100)
        """
        try:
            raw = float(mq7_raw)
            return round((raw / 4095) * 100, 1)
        except:
            return 0

    # ─────────────────────────────────────────────
    # 📊 TREND ANALYSIS (FIXED)
    # ─────────────────────────────────────────────
    @staticmethod
    def analyze_trends(history_data):
        if len(history_data) < 5:
            return {"trend": "Stable", "forecast": "Not enough data"}

        # ✅ Use numeric aqi_numeric for better precision
        aqi_values = [d.get('aqi_numeric', 0) for d in history_data]

        sma_short = np.mean(aqi_values[:3])
        sma_long = np.mean(aqi_values[:min(len(aqi_values), 10)])

        trend = "Stable"
        if sma_short > sma_long + 10:
            trend = "Increasing"
        elif sma_short < sma_long - 10:
            trend = "Decreasing"

        forecast = (
            "Improving" if trend == "Decreasing"
            else "Worsening" if trend == "Increasing"
            else "Stable"
        )

        return {
            "trend": trend,
            "forecast": forecast,
            "sma_short": round(sma_short, 2),
            "sma_long": round(sma_long, 2)
        }

    # ─────────────────────────────────────────────
    # 🚬 SMOKING DETECTION (FIXED)
    # ─────────────────────────────────────────────
    @staticmethod
    def detect_smoking(recent_data):
        if len(recent_data) < 2:
            return {"smoking_detected": False, "confidence": 0}

        co_levels = [MLService.map_co_level(d.get('co_level', "")) for d in recent_data[:5]]

        max_co = max(co_levels)
        min_co = min(co_levels[1:]) if len(co_levels) > 1 else max_co

        if max_co - min_co > 30 and max_co > 60:
            return {"smoking_detected": True, "confidence": 0.9}

        return {"smoking_detected": False, "confidence": 0.0}

    # ─────────────────────────────────────────────
    # ❤️ HEALTH RISK (FIXED)
    # ─────────────────────────────────────────────
    @staticmethod
    def classify_health_risk(current_data):
        aqi = MLService.map_air_quality(current_data.get('air_quality', ""))
        co = MLService.map_co_level(current_data.get('co_level', ""))

        if aqi > 200 or co > 100:
            return {"status": "UNSAFE", "color": "red"}
        elif aqi > 100 or co > 40:
            return {"status": "MODERATE", "color": "yellow"}
        else:
            return {"status": "SAFE", "color": "green"}

    # ─────────────────────────────────────────────
    # 💰 NEW: POLLUTION COST MODEL
    # ─────────────────────────────────────────────
    @staticmethod
    def calculate_pollution_cost(history_data):
        """
        Converts CO levels into environmental cost
        """

        if not history_data:
            return {"total_cost": 0, "avg_cost": 0}

        total_emission = 0

        for d in history_data:
            # ✅ Use numeric co_percent instead of string mapping
            co_val = d.get("co_percent", 0)
            total_emission += co_val

        # 💡 Cost model (you can tune this)
        COST_PER_UNIT = 0.05   # e.g., $0.05 per emission unit

        total_cost = total_emission * COST_PER_UNIT
        avg_cost = total_cost / len(history_data)

        return {
            "total_emission": round(total_emission, 2),
            "total_cost": round(total_cost, 2),
            "avg_cost": round(avg_cost, 2)
        }

    # ─────────────────────────────────────────────
    # 🔥 NEW: FIRE DETECTION ALERT SYSTEM
    # ─────────────────────────────────────────────
    @staticmethod
    def detect_fire_risk(current_data):
        temp = float(current_data.get("temperature", 0) or 0)
        aqi_numeric = float(current_data.get("aqi_numeric", 0) or 0)
        co_percent = float(current_data.get("co_percent", 0) or 0)

        # Numeric thresholds (user-configured)
        is_high_co   = co_percent  > 55   # > 55% CO sensor reading
        is_high_temp = temp        > 40   # > 40°C
        is_bad_air   = aqi_numeric > 80   # AQI > 80

        # CRITICAL: all three sensors simultaneously breached
        if is_high_co and is_high_temp and is_bad_air:
            return {
                "alert": True,
                "level": "CRITICAL",
                "message": "🔥 Critical: CO > 55%, Temp > 40°C and AQI > 80 detected!",
                "color": "red"
            }

        # WARNING: any two conditions are breached together
        conditions_met = sum([is_high_co, is_high_temp, is_bad_air])
        if conditions_met >= 2:
            return {
                "alert": True,
                "level": "WARNING",
                "message": "⚠️ Pollution levels rising — multiple thresholds exceeded",
                "color": "orange"
            }

        return {
            "alert": False,
            "level": "SAFE",
            "message": "Environment is stable",
            "color": "green"
        }

    # ─────────────────────────────────────────────
    # ⏱ PEAK HOURS (FIXED TIMESTAMP)
    # ─────────────────────────────────────────────
    @staticmethod
    def predict_air_quality(mq7, mq135, temp, humidity):
        if rf_model is None:
            return "Unknown"
        try:
            # Create a DataFrame to provide the valid feature names that the model expects
            data = pd.DataFrame([{
                'mq7': float(mq7),
                'mq135': float(mq135),
                'temperature': float(temp),
                'humidity': float(humidity)
            }])
            prediction = rf_model.predict(data)
            return prediction[0]
        except Exception as e:
            print("Prediction error:", e)
            return "Unknown"

    @staticmethod
    def get_peak_hours(history_data):
        hourly = {}

        for d in history_data:
            ts = d.get("timestamp")

            if isinstance(ts, datetime):
                dt = ts
            else:
                continue

            hr = dt.strftime("%H:00")

            if hr not in hourly:
                hourly[hr] = []

            hourly[hr].append(MLService.map_air_quality(d['air_quality']))

        peak_hr = None
        max_avg = -1

        for hr, vals in hourly.items():
            avg = sum(vals) / len(vals)
            if avg > max_avg:
                max_avg = avg
                peak_hr = hr

        return {
            "peak_hour": peak_hr,
            "peak_avg_aqi": round(max_avg, 2)
        }