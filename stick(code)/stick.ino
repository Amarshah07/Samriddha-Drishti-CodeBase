/*
  Samriddha Drishti - Smart Blind Stick (still in prototype stage)
  Author : Team JalDrishya 
  Purpose: Read ultrasonic + IR sensors, provide haptic feedback, publish JSON over Bluetooth Serial.
  Hardware: ESP32, HC-SR04, analog IR sensor, vibration motor, SOS button.
*/

#include <Arduino.h>
#include "BluetoothSerial.h"

// ---------- CONFIG ----------
#define TRIG_PIN      18    
#define ECHO_PIN      19    
#define IR_PIN        34   
#define VIB_PIN       25   
#define SOS_PIN       14    
#define LED_PIN       2     // Status LED

#define SAMPLE_INTERVAL_MS   200    
#define HC_SR04_TIMEOUT_US   30000 

#define DIST_ALERT_CM        120    
#define DIST_CRITICAL_CM     40     
#define IR_DROP_THRESHOLD    1500   

// Vibration intensities (0-255 PWM)
#define VIB_OFF              0
#define VIB_LOW              90
#define VIB_MED              160
#define VIB_HIGH             255

// ---------- GLOBALS ----------
BluetoothSerial SerialBT;
volatile unsigned long lastSOS = 0;
const unsigned long SOS_DEBOUNCE_MS = 800;
const unsigned long SOS_LONGPRESS_MS = 1200;

unsigned long lastSample = 0;

// ---------- UTILITY ----------
long measureDistanceCM() {
  // Trigger
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Wait for echo
  unsigned long t = pulseIn(ECHO_PIN, HIGH, HC_SR04_TIMEOUT_US);
  if (t == 0) return -1; // timeout / no reading
  // distance in cm = time(us) / 58 (approx)
  long dist = t / 58;
  return dist;
}

int readIR() {
  // analogRead returns 0..4095 on ESP32 default ADC range
  return analogRead(IR_PIN);
}

void setVibration(uint8_t value) {
  // Use ledc PWM for ESP32 for smoother control
  ledcWrite(0, value);
}

void sendStatusJSON(long dist, int irVal, const char* note) {
  // Build a small JSON string and send via Bluetooth
  // Example: {"d":45,"ir":1300,"note":"ok"}
  String out = "{";
  out += "\"d\":";
  out += dist;
  out += ",\"ir\":";
  out += irVal;
  out += ",\"note\":\"";
  out += note;
  out += "\"}";

  if (SerialBT.connected()) {
    SerialBT.println(out);
  }
  // Also print on serial for debug
  Serial.println(out);
}

// ---------- SOS handler (non blocking) ----------
void checkSOS() {
  static unsigned long pressStart = 0;
  static bool pressed = false;

  bool state = digitalRead(SOS_PIN) == LOW ? false : true; // depends on wiring, assume HIGH when pressed

  if (state && !pressed) {
    pressed = true;
    pressStart = millis();
  } else if (!state && pressed) {
    unsigned long duration = millis() - pressStart;
    pressed = false;
    if (duration >= SOS_LONGPRESS_MS && (millis() - lastSOS) > SOS_DEBOUNCE_MS) {
      lastSOS = millis();
      // Send SOS message
      sendStatusJSON(-1, -1, "SOS");
      // strong vibration to notify user
      setVibration(VIB_HIGH);
      delay(700);
      setVibration(VIB_OFF);
    }
  }
}

// ---------- SETUP ----------
void setup() {
  Serial.begin(115200);
  Serial.println("[Stick] Starting...");

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(IR_PIN, INPUT);
  pinMode(VIB_PIN, OUTPUT);
  pinMode(SOS_PIN, INPUT_PULLUP); 
  pinMode(LED_PIN, OUTPUT);

  // Setup PWM (ledc) channel 0 on VIB_PIN
  ledcSetup(0, 2000, 8); 
  ledcAttachPin(VIB_PIN, 0);
  setVibration(VIB_OFF);

  // Initialize Bluetooth Serial
  if (!SerialBT.begin("Samriddha_Stick")) {
    Serial.println("[Stick] BT init failed");
  } else {
    Serial.println("[Stick] Bluetooth started: Samriddha_Stick");
  }

  digitalWrite(LED_PIN, HIGH);
  delay(200);
  digitalWrite(LED_PIN, LOW);
}

// ---------- MAIN LOOP ----------
void loop() {
  unsigned long now = millis();
  if (now - lastSample < SAMPLE_INTERVAL_MS) {
    // handle sos with every iteration
    checkSOS();
    delay(10);
    return;
  }
  lastSample = now;

  // Read sensors
  long dist = measureDistanceCM();   // -1 indicates no echo
  int irVal = readIR();

  // Decide feedback
  uint8_t vib = VIB_OFF;
  const char* note = "ok";

  // Prioritize critical distances
  if (dist > 0 && dist <= DIST_CRITICAL_CM) {
    vib = VIB_HIGH;
    note = "critical_obstacle";
  } else if (dist > 0 && dist <= DIST_ALERT_CM) {
    vib = VIB_MED;
    note = "approaching_obstacle";
  }

  // IR (downward drop) overrides with immediate alert
  if (irVal > IR_DROP_THRESHOLD) {
    vib = VIB_HIGH;
    note = "drop_detected";
  }

  // Provide light vibration if nothing critical but in proximity
  if (dist > 0 && dist <= (DIST_ALERT_CM * 1.5) && vib == VIB_OFF) {
    vib = VIB_LOW;
    note = "near_object";
  }

  // Send feedback
  setVibration(vib);
  sendStatusJSON(dist, irVal, note);

  // Visual LED flashing when connected
  if (SerialBT.connected()) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  // handle SOS button within sample interval
  checkSOS();

  // small delay to avoid CPU hogging
  delay(10);
}
