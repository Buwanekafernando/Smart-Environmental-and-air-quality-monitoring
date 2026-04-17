import numpy as np
from datetime import datetime

class MLService:
    @staticmethod
    def analyze_trends(history_data):
        # history_data: List of dicts latest to oldest
        if len(history_data) < 5:
            return {"trend": "Stable", "forecast": "Not enough data"}
        
        # Calculate Simple Moving Average of AQI
        aqi_values = [d['air_quality'] for d in history_data]
        sma_short = np.mean(aqi_values[:3])
        sma_long = np.mean(aqi_values[:min(len(aqi_values), 10)])
        
        trend = "Stable"
        if sma_short > sma_long + 5:
            trend = "Increasing"
        elif sma_short < sma_long - 5:
            trend = "Decreasing"
            
        forecast = "Improving" if trend == "Decreasing" else "Worsening" if trend == "Increasing" else "Stable"
        
        return {
            "trend": trend,
            "forecast": forecast,
            "sma_short": round(sma_short, 2),
            "sma_long": round(sma_long, 2)
        }

    @staticmethod
    def detect_smoking(recent_data):
        # Look for sudden spikes in CO
        if len(recent_data) < 2:
            return {"smoking_detected": False, "confidence": 0}
            
        co_levels = [d.get('co_level', 0) for d in recent_data][:5] # latest 5
        max_co = max(co_levels)
        min_co = min(co_levels[1:]) if len(co_levels) > 1 else max_co
        
        # Spike detecting logic
        if max_co - min_co > 20 and max_co > 40:
            return {"smoking_detected": True, "confidence": 0.85}
            
        return {"smoking_detected": False, "confidence": 0.0}

    @staticmethod
    def classify_health_risk(current_data):
        aqi = current_data.get('air_quality', 0)
        co = current_data.get('co_level', 0)
        
        if aqi > 150 or co > 50:
            return {"status": "UNSAFE", "color": "red"}
        elif aqi > 50 or co > 20:
            return {"status": "MODERATE", "color": "yellow"}
        else:
            return {"status": "SAFE", "color": "green"}

    @staticmethod
    def get_peak_hours(history_data):
        # group by hour and average AQI
        # history_data has string or float timestamp
        hourly = {}
        for d in history_data:
            dt = datetime.fromtimestamp(d['timestamp'])
            hr = dt.strftime("%H:00")
            if hr not in hourly:
                hourly[hr] = []
            hourly[hr].append(d['air_quality'])
            
        peak_hr = None
        max_avg = -1
        for hr, vals in hourly.items():
            avg = sum(vals)/len(vals)
            if avg > max_avg:
                max_avg = avg
                peak_hr = hr
                
        return {"peak_hour": peak_hr, "peak_avg_aqi": round(max_avg, 2)}
