
#include <DHT.h>

// ── PIN DEFINITIONS ─────────────────────────────────
#define DHT_PIN     4
#define MQ135_PIN   34
#define MQ7_PIN     35
#define PIR_PIN     14

#define DHT_TYPE    DHT11
#define INTERVAL    1000  // ms between readings
#define WARMUP_SEC   90   // MQ warmup time in seconds
#define ADC_SAMPLES   5   // samples averaged per ADC read

// ── ALERT THRESHOLDS ────────────────────────────────
#define MQ135_WARN  1500
#define MQ135_HIGH  2500
#define MQ7_WARN    1500
#define MQ7_HIGH    2500

// ── OBJECT ──────────────────────────────────────────
DHT dht(DHT_PIN, DHT_TYPE);

// ── HELPER: averaged analog read ────────────────────
int readADC(int pin) {
  long sum = 0;
  for (int i = 0; i < ADC_SAMPLES; i++) {
    sum += analogRead(pin);
    delay(10);
  }
  return sum / ADC_SAMPLES;
}

// ── HELPER: raw ADC → voltage ────────────────────────
float toVolts(int raw) {
  return raw * (3.3f / 4095.0f);
}

// ── HELPER: MQ135 air quality label ─────────────────
String aqLabel(int raw) {
  if (raw < 800)           return "GOOD";
  if (raw < MQ135_WARN)   return "MODERATE";
  if (raw < MQ135_HIGH)   return "POOR  !";
  return                           "DANGER !!";
}

// ── HELPER: MQ7 CO level label ───────────────────────
String coLabel(int raw) {
  if (raw < 800)         return "SAFE";
  if (raw < MQ7_WARN)   return "LOW CO";
  if (raw < MQ7_HIGH)   return "HIGH CO  !";
  return                         "DANGER CO !!";
}

// ═══════════════════════════════════════════════════
void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(PIR_PIN, INPUT);
  // P4 handled by DHT library
  // P34, P35 are input-only ADC — no pinMode needed

  dht.begin();

  // ── startup banner ───────────────────────────
  Serial.println("\n\n╔══════════════════════════════════╗");
  Serial.println("║  Air Quality & Smoke Detector    ║");
  Serial.println("║  ESP32 — USB Serial Monitor      ║");
  Serial.println("╚══════════════════════════════════╝");
  Serial.println("Pins: DHT11=P4  MQ135=P34  MQ7=P35  PIR=P14\n");

  // ── sensor self-checks ───────────────────────
  Serial.print("DHT11 check    ... ");
  delay(500);
  float testT = dht.readTemperature();
  if (isnan(testT)) {
    Serial.println("ERROR — check 4.7k pull-up on P4");
  } else {
    Serial.print("OK  (");
    Serial.print(testT, 1);
    Serial.println(" C)");
  }

  Serial.print("PIR check      ... ");
  Serial.println(digitalRead(PIR_PIN) == HIGH
    ? "OK  (motion at startup — normal)"
    : "OK  (no motion)");

  Serial.print("MQ135 raw      ... ");
  Serial.println(readADC(MQ135_PIN));

  Serial.print("MQ7   raw      ... ");
  Serial.println(readADC(MQ7_PIN));
  Serial.println();

  // ── MQ warmup countdown ──────────────────────
  Serial.println("Warming up MQ sensors (90 sec) ...");
  for (int i = WARMUP_SEC; i > 0; i--) {
    if (i % 10 == 0 || i <= 5) {
      Serial.print("  ");
      Serial.print(i);
      Serial.println("s remaining ...");
    }
    delay(1000);
  }
  Serial.println("Warmup complete! Readings start now.\n");
}

// ═══════════════════════════════════════════════════
void loop() {
  static unsigned long lastTime = 0;
  unsigned long now = millis();

  if (now - lastTime < INTERVAL) return;
  lastTime = now;

  // ── Read sensors ───────────────────────────
  float temp = dht.readTemperature();
  float humi = dht.readHumidity();

  int mq135Raw = readADC(MQ135_PIN);
  int mq7Raw   = readADC(MQ7_PIN);

  bool motion = (digitalRead(PIR_PIN) == HIGH);

  // ── Handle NaN values (important for JSON) ──
  if (isnan(temp)) temp = -1;
  if (isnan(humi)) humi = -1;

  // ── JSON Output ────────────────────────────
  Serial.print("{");

  Serial.print("\"mq7\":");
  Serial.print(mq7Raw);
  Serial.print(",");

  Serial.print("\"mq135\":");
  Serial.print(mq135Raw);
  Serial.print(",");

  Serial.print("\"temperature\":");
  Serial.print(temp);
  Serial.print(",");

  Serial.print("\"humidity\":");
  Serial.print(humi);
  Serial.print(",");

  Serial.print("\"motion\":");
  Serial.print(motion ? "true" : "false");
  Serial.print(",");

  Serial.print("\"air_quality\":\"");
  Serial.print(aqLabel(mq135Raw));
  Serial.print("\",");

  Serial.print("\"co_level\":\"");
  Serial.print(coLabel(mq7Raw));
  Serial.print("\"");

  Serial.println("}");

}
