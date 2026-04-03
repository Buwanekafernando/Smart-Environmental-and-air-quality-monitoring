# Smart Environmental and Air Quality Monitoring

## Overview
This project is a comprehensive smart environmental and air quality monitoring system that collects real-time data from various sensors, stores it in a MySQL database, and provides a user-friendly dashboard for visualization. It includes a chatbot and machine learning models to estimate pollution costs and provide suggestions for minimizing pollution.

## Features
- Real-time sensor data collection from Arduino-based sensors
- Data storage in MySQL database with separate tables for each sensor type
- Web-based dashboard for data visualization
- Chatbot for user interaction
- Machine learning models for pollution cost estimation and health suggestions

## Sensors Used
The system utilizes the following sensors connected to an Arduino/ESP32 board:
- **DHT22**: Measures temperature and humidity
- **MQ135**: Monitors air quality levels
- **MQ7**: Detects carbon monoxide (CO) levels
- **PIR Sensor**: Detects motion/presence in the room

## Data Collection and Storage
- Data is collected from the serial monitor output of the Arduino board
- The system stores the first 150 data points in the MySQL database
- Database structure includes four separate tables, one for each sensor type:
  - Air Quality Table
  - CO Level Table
  - Temperature/Humidity Table
  - Motion Detection Table

## Backend
- Built with Flask (Python)
- Handles serial communication and data parsing
- Manages database operations for storing and retrieving sensor data

## Frontend
- Developed using Vue.js with Vite
- Displays interactive dashboard with charts and gauges
- Components include:
  - Air Quality Chart
  - CO Gauge
  - Temperature Card
  - Smoke Alert
  - Smoking Status
  - Health Insights

## Chatbot and Machine Learning
- Integrated chatbot for user queries and assistance
- Two machine learning models:
  1. **Pollution Cost Estimator**: Calculates the economic cost of pollution based on sensor data
  2. **Pollution Minimization Suggestions**: Provides actionable recommendations to reduce pollution levels and improve air quality

## Installation and Setup
1. Clone the repository
2. Set up the Arduino sensors as per the `arduino/sensor/sensor.ino` file
3. Configure MySQL database with the required tables
4. Install backend dependencies: `pip install flask pymysql` (adjust for actual dependencies)
5. Install frontend dependencies: `npm install`
6. Run the backend server: `python app.py`
7. Run the frontend: `npm run dev`

## Usage
1. Upload the Arduino code to your ESP32 board
2. Start the backend server to begin data collection
3. Access the frontend dashboard to view real-time sensor data
4. Use the chatbot for queries and the ML models for insights

## Contributing
Contributions are welcome. Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.