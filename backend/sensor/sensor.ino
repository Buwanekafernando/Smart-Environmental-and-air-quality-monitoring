
#include <DHT.h>

// ── PIN DEFINITIONS ─────────────────────────────────
#define DHT_PIN     4
#define MQ135_PIN   34
#define MQ7_PIN     35
#define PIR_PIN     14

#define DHT_TYPE    DHT11
#define INTERVAL    3000  // ms between readings
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
  static int readingNum = 0;
  unsigned long now = millis();

  if (now - lastTime < INTERVAL) return;
  lastTime = now;
  readingNum++;

  // ── reading header ───────────────────────────
  Serial.print("┌── Reading #");
  Serial.print(readingNum);
  Serial.print("  (");
  Serial.print(now / 1000);
  Serial.println("s uptime) ──────────────");

  // ── 1. DHT11 ─────────────────────────────────
  float temp = dht.readTemperature();
  float humi = dht.readHumidity();
  Serial.print("│ DHT11   │ ");
  if (isnan(temp) || isnan(humi)) {
    Serial.println("ERROR — check 4.7k pull-up on P4");
  } else {
    Serial.print("Temp: ");
    Serial.print(temp, 1);
    Serial.print(" C   Humidity: ");
    Serial.print(humi, 1);
    Serial.println(" %");
  }

  // ── 2. MQ135 — Air Quality ───────────────────
  int   mq135Raw = readADC(MQ135_PIN);
  float mq135V   = toVolts(mq135Raw);
  Serial.print("│ MQ135   │ ");
  Serial.print("Raw: ");
  Serial.print(mq135Raw);
  Serial.print("   Volt: ");
  Serial.print(mq135V, 2);
  Serial.print("V   Status: ");
  Serial.println(aqLabel(mq135Raw));

  // ── 3. MQ7 — Carbon Monoxide ─────────────────
  int   mq7Raw = readADC(MQ7_PIN);
  float mq7V   = toVolts(mq7Raw);
  Serial.print("│ MQ7     │ ");
  Serial.print("Raw: ");
  Serial.print(mq7Raw);
  Serial.print("   Volt: ");
  Serial.print(mq7V, 2);
  Serial.print("V   Status: ");
  Serial.println(coLabel(mq7Raw));

  // ── 4. PIR — Motion ──────────────────────────
  bool motion = (digitalRead(PIR_PIN) == HIGH);
  Serial.print("│ PIR     │ Motion: ");
  Serial.println(motion ? "DETECTED  <<<" : "none");

  // ── smoke / CO alert logic ───────────────────
  bool smokeAlert = (mq135Raw > MQ135_WARN)
                 && (mq7Raw   > MQ7_WARN)
                 && motion;
  if (smokeAlert) {
    Serial.println("│ *** SMOKE / CO ALERT — person present ***");
  }

  Serial.println("└───────────────────────────────────────\n");
}
