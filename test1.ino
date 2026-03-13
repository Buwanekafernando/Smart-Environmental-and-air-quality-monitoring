#include <DHT.h>

//SENSOR PINS
#define DHTPIN 4        
#define DHTTYPE DHT11

#define MQ135_PIN 34    
#define MQ7_PIN 35      
#define PIR_PIN 27      

// SENSOR OBJECTS 
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);

  // Initialize pins
  pinMode(MQ135_PIN, INPUT);
  pinMode(MQ7_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);

  dht.begin();

  Serial.println("ESP32 Smart Air Quality Monitoring Started...");
}

void loop() {
  // READ ANALOG SENSORS
  int airQualityRaw = analogRead(MQ135_PIN);  // 0-4095
  int coLevelRaw = analogRead(MQ7_PIN);       // 0-4095

  // READ TEMPERATURE & HUMIDITY 
  float temperature = dht.readTemperature();  // Celsius
  float humidity = dht.readHumidity();

  // Check DHT reading
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  // READ PIR MOTION SENSOR 
  int motionDetected = digitalRead(PIR_PIN);  // 1 = motion, 0 = no motion

  //PRINT JSON FORMAT 
  Serial.print("{ ");
  Serial.print("\"air_quality\": "); Serial.print(airQualityRaw);
  Serial.print(", \"co_level\": "); Serial.print(coLevelRaw);
  Serial.print(", \"temperature\": "); Serial.print(temperature);
  Serial.print(", \"humidity\": "); Serial.print(humidity);
  Serial.print(", \"motion_detected\": "); Serial.print(motionDetected);
  Serial.println(" }");

  delay(3000); // Read every 3 seconds
}