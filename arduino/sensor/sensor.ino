#include <Adafruit_Sensor.h>
#include <DHT.h>

// ---------------- SENSOR PINS ----------------
#define DHTPIN 23          // use your P23 (GPIO23)
#define DHTTYPE DHT22      // IMPORTANT

#define MQ135_PIN 34
#define MQ7_PIN 35
#define PIR_PIN 27

// ---------------- SENSOR OBJECT ----------------
DHT dht(DHTPIN, DHTTYPE);

// ---------------- HELPER FUNCTIONS ----------------

// Convert Air Quality to Category
String getAirQualityStatus(int value) {
  if (value < 800) return "Healthy";
  else if (value < 1500) return "Good";
  else if (value < 2500) return "Fair";
  else if (value < 3500) return "Bad";
  else return "Harmful";
}

// Convert CO Level to Percentage
float getCOPercentage(int value) {
  return (value / 4095.0) * 100.0;
}

// ---------------- SETUP ----------------
void setup() {
  Serial.begin(115200);

  pinMode(MQ135_PIN, INPUT);
  pinMode(MQ7_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);

  dht.begin();

  Serial.println("ESP32 Smart Air Quality Monitoring Started...");
}

// ---------------- LOOP ----------------
void loop() {

  // READ ANALOG SENSORS
  int airQualityRaw = analogRead(MQ135_PIN);
  int coLevelRaw = analogRead(MQ7_PIN);

  String airStatus = getAirQualityStatus(airQualityRaw);
  float coPercent = getCOPercentage(coLevelRaw);

  // READ DHT SENSOR
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // READ PIR SENSOR
  int motionDetected = digitalRead(PIR_PIN);

  // PRINT JSON OUTPUT
  Serial.print("{ ");

  Serial.print("\"air_quality_raw\": "); Serial.print(airQualityRaw);
  Serial.print(", \"air_quality_status\": \""); Serial.print(airStatus); Serial.print("\"");

  Serial.print(", \"co_level_raw\": "); Serial.print(coLevelRaw);
  Serial.print(", \"co_level_percent\": "); Serial.print(coPercent);

  // Handle DHT properly
  if (isnan(temperature) || isnan(humidity)) {
    Serial.print(", \"temperature\": null");
    Serial.print(", \"humidity\": null");
    Serial.print(", \"dht_status\": \"failed\"");
  } else {
    Serial.print(", \"temperature\": "); Serial.print(temperature);
    Serial.print(", \"humidity\": "); Serial.print(humidity);
    Serial.print(", \"dht_status\": \"ok\"");
  }

  Serial.print(", \"motion_detected\": "); Serial.print(motionDetected);

  Serial.println(" }");

  delay(3000);  // stable loop delay
}