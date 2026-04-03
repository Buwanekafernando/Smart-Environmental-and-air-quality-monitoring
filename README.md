# 🌿 Smart Environmental and Air Quality Monitoring

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3-green.svg)](https://vuejs.org/)
[![Arduino](https://img.shields.io/badge/Arduino-Compatible-blue.svg)](https://www.arduino.cc/)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Sensors Used](#sensors-used)
- [Data Collection and Storage](#data-collection-and-storage)
- [Architecture](#architecture)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## 🌍 Overview
Welcome to the **Smart Environmental and Air Quality Monitoring** system! This innovative project combines IoT sensors, machine learning, and a modern web interface to provide real-time insights into environmental conditions. Whether you're monitoring indoor air quality, tracking pollution costs, or getting health recommendations, this system has you covered.

The system collects data from Arduino-based sensors, stores it securely in a MySQL database, and presents it through an intuitive dashboard. Plus, our AI-powered chatbot and ML models help you understand and mitigate pollution effects.

## ✨ Features
- 🔄 **Real-time Monitoring**: Continuous data collection from multiple environmental sensors
- 💾 **Secure Storage**: MySQL database with dedicated tables for each sensor type
- 📊 **Interactive Dashboard**: Vue.js-powered web interface with charts and visualizations
- 🤖 **AI Chatbot**: Intelligent assistant for queries and guidance
- 🧠 **Machine Learning Models**:
  - Pollution cost estimation
  - Personalized health and minimization suggestions
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🔔 **Alerts**: Real-time notifications for critical air quality levels

## 🔧 Sensors Used
Our system leverages cutting-edge sensors connected to an **ESP32 microcontroller board** for comprehensive environmental monitoring. The ESP32 serves as the central processing unit, collecting data from all sensors and transmitting it via serial communication.

| Sensor | Purpose | Key Measurements | ESP32 Pin |
|--------|---------|------------------|-----------|
| **DHT22** 🌡️ | Temperature & Humidity | Temperature (°C), Humidity (%) | GPIO 23 |
| **MQ135** 🌬️ | Air Quality | Raw values, Status categories (Healthy/Good/Fair/Bad/Harmful) | GPIO 34 |
| **MQ7** ☠️ | Carbon Monoxide | Raw values, Percentage levels | GPIO 35 |
| **PIR** 👥 | Motion Detection | Presence detection for occupancy tracking | GPIO 27 |

## 💽 Data Collection and Storage
### How It Works
1. **Sensor Reading**: Arduino continuously reads sensor data every 3 seconds
2. **Serial Transmission**: Data is sent via serial communication in JSON format
3. **Backend Processing**: Python Flask server parses and validates incoming data
4. **Database Storage**: First 150 data points are stored in MySQL for analysis
5. **Frontend Display**: Real-time updates on the dashboard

### Database Structure
The MySQL database is organized into four specialized tables:

```sql
-- Example table structure
CREATE TABLE air_quality (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_value INT,
    status VARCHAR(20),
    quality_score DECIMAL(5,2)
);

-- Similar structures for co_levels, temperature_humidity, motion_detection
```

## 🏗️ Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Arduino       │    │   Backend       │    │   Frontend      │
│   Sensors       │───▶│   (Flask)      │───▶│   (Vue.js)      │
│                 │    │   MySQL DB     │    │   Dashboard     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       🤖 Chatbot & ML Models    📊 Charts & Insights
```

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL Server
- Arduino IDE
- ESP32 board

### Step-by-Step Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/smart-air-quality-monitor.git
   cd smart-air-quality-monitor
   ```

2. **Arduino Setup**
   - Open `arduino/sensor/sensor.ino` in Arduino IDE
   - Connect sensors to ESP32 pins as specified
   - Upload the code to your ESP32 board

3. **Database Configuration**
   ```sql
   CREATE DATABASE air_quality_monitor;
   -- Run the provided SQL scripts to create tables
   ```

4. **Backend Setup**
   ```bash
   cd backend
   pip install flask pymysql pyserial
   # Configure database connection in db.py
   ```

5. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

## 🎯 Usage
1. **Start the Backend Server**
   ```bash
   cd backend
   python app.py
   ```

2. **Launch the Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Dashboard**
   - Open your browser to `http://localhost:3000`
   - View real-time sensor data and insights

4. **Interact with Features**
   - Use the chatbot for questions
   - Check pollution costs and health suggestions
   - Monitor air quality trends

## 📡 API Reference
### Get Sensor Data
```http
GET /api/data
```
Returns the latest sensor readings in JSON format.

**Response Example:**
```json
{
  "air_quality": {
    "raw": 1200,
    "status": "Good",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "temperature": 25.5,
  "humidity": 60.2,
  "co_level": 0.5
}
```

## 🤝 Contributing
We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use Vue.js composition API for frontend components
- Add tests for new features
- Update documentation as needed

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for a cleaner, healthier environment**

*Have questions? Reach out via the chatbot or open an issue!*