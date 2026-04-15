#include <DHT.h>

// ── PIN DEFINITIONS ──────────────────────────
#define DHT_PIN     4
#define MQ135_PIN  34
#define MQ7_PIN    35
#define PIR_PIN     5
#define LED_PIN     2

#define DHT_TYPE   DHT11
#define INTERVAL   3000   // 3 seconds

// ── OBJECT ───────────────────────────────────
DHT dht(DHT_PIN, DHT_TYPE);

// ── VARIABLES ────────────────────────────────
unsigned long lastTime = 0;

// ─────────────────────────────────────────────
void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);

  dht.begin();

  Serial.println("\n===== SENSOR SYSTEM STARTED =====");

  // LED test
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }

  Serial.println("System Ready...\n");
}

// ─────────────────────────────────────────────
void loop() {

  if (millis() - lastTime < INTERVAL) return;
  lastTime = millis();

  Serial.println("================================");

  bool allSensorsOK = true;

  // ── DHT11 ────────────────────────────────
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT11   ERROR");
    allSensorsOK = false;
  } else {
    Serial.print("DHT11   Temp: ");
    Serial.print(temp);
    Serial.print(" °C | Humidity: ");
    Serial.print(hum);
    Serial.println(" %");
  }

  // ── MQ135 ────────────────────────────────
  int mq135 = analogRead(MQ135_PIN);

  Serial.print("MQ135   Value: ");
  Serial.print(mq135);

  if (mq135 > 2000) {
    Serial.println("   Air Pollution HIGH");
  } else {
    Serial.println("   Normal");
  }

  // ── MQ7 ──────────────────────────────────
  int mq7 = analogRead(MQ7_PIN);

  Serial.print("MQ7     Value: ");
  Serial.print(mq7);

  if (mq7 > 2000) {
    Serial.println("   CO Level HIGH");
  } else {
    Serial.println("  Normal");
  }

  // ── PIR ──────────────────────────────────
  int motion = digitalRead(PIR_PIN);

  Serial.print("PIR    ");
  if (motion == HIGH) {
    Serial.println(" Motion DETECTED");
  } else {
    Serial.println("No motion");
  }

  // ── LED STATUS ────────────────────────────
  if (allSensorsOK) {
    digitalWrite(LED_PIN, HIGH);   // All sensors OK
  } else {
    digitalWrite(LED_PIN, LOW);    // Something wrong (likely DHT)
  }

  Serial.println("================================\n");
}