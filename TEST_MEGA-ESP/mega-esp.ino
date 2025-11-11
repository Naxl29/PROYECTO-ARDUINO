#include <MemoryFree.h>
#include <EEPROM.h>

String inString;         // Para acumular datos entrantes

#if defined(HAVE_HWSERIAL3)
#define ESP_SERIAL Serial3
#elif defined(HAVE_HWSERIAL1)
#define ESP_SERIAL Serial1
#else
#define ESP_SERIAL Serial
#warning "Serial3 no disponible; se usará Serial para comunicar con el ESP8266."
#endif

// Array de pines (LED 1 controla el pin 13, LED 2 el pin 12, etc.)
byte ledPins[] = {13, 12, 11, 10, 9, 8, 7, 6, 5};
const byte numLeds = sizeof(ledPins) / sizeof(ledPins[0]);

const byte clapSensorPin = 2;          // Salida digital del KY-036
const byte clapTargetPin = 5;          // Pin a encender tras detectar dos aplausos

const unsigned long clapDebounceMs = 80;
const unsigned long clapSequenceWindowMs = 600;

bool clapIdleState = LOW;
bool clapTargetState = LOW;
bool lastClapState = LOW;

unsigned long lastClapEdgeMs = 0;
unsigned long lastClapDetectedMs = 0;
byte clapCounter = 0;

void setup() {
  Serial.begin(115200);
  ESP_SERIAL.begin(115200);

  pinMode(clapSensorPin, INPUT);  // Cambiar a INPUT_PULLUP si el módulo lo requiere
  delay(5);                       // Pequeña estabilización
  clapIdleState = digitalRead(clapSensorPin);
  lastClapState = clapIdleState;

  // Inicializamos todos los pines LED como salida
  for (byte i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  Serial.println("Listo para recibir comandos:");
  Serial.print("[ON1] [OFF1] ... [ON");
  Serial.print(numLeds);
  Serial.print("] [OFF");
  Serial.print(numLeds);
  Serial.println("]");
  Serial.println("[ONALL] [OFFALL]");
}

void loop() {
  handleClapSensor();
  handleEspSerial();
}

void handleEspSerial() {
  while (ESP_SERIAL.available()) {
    char inChar = ESP_SERIAL.read();
    Serial.write(inChar);

    unsigned long now = millis();
    static unsigned long lastByteMs = 0;
    if (now - lastByteMs > 200) {
      inString = "";
    }
    lastByteMs = now;

    if (inChar == '[') {
      inString = "[";
      continue;
    }
    if (inString.length() == 0) {
      continue;
    }

    inString += inChar;

    // Procesar al recibir un ']' (fin de comando)
    if (inChar == ']') {
      inString.trim();

      // --- Encender todos ---
      if (inString.indexOf("[ONALL]") >= 0) {
        for (byte i = 0; i < numLeds; i++) digitalWrite(ledPins[i], HIGH);
        Serial.println("Todos los LEDs encendidos");
      }
      // --- Apagar todos ---
      else if (inString.indexOf("[OFFALL]") >= 0) {
        for (byte i = 0; i < numLeds; i++) digitalWrite(ledPins[i], LOW);
        clapTargetState = false;
        Serial.println("Todos los LEDs apagados");
      }
      else {
        // --- Comando individual ---
        for (byte i = 0; i < numLeds; i++) {
          String onCmd = "[ON" + String(i + 1) + "]";
          String offCmd = "[OFF" + String(i + 1) + "]";
          if (inString.indexOf(onCmd) >= 0) {
            digitalWrite(ledPins[i], HIGH);
            if (ledPins[i] == clapTargetPin) {
              clapTargetState = true;
            }
            Serial.print("LED ");
            Serial.print(i + 1);
            Serial.print(" (pin ");
            Serial.print(ledPins[i]);
            Serial.println(") encendido");
          }
          else if (inString.indexOf(offCmd) >= 0) {
            digitalWrite(ledPins[i], LOW);
            if (ledPins[i] == clapTargetPin) {
              clapTargetState = false;
            }
            Serial.print("LED ");
            Serial.print(i + 1);
            Serial.print(" (pin ");
            Serial.print(ledPins[i]);
            Serial.println(") apagado");
          }
        }
      }

      inString = ""; // Limpiar buffer
      clapCounter = 0;
    }
  }
}

void handleClapSensor() {
  bool currentState = digitalRead(clapSensorPin);
  bool clapTriggered = (currentState != clapIdleState);
  bool lastClapTriggered = (lastClapState != clapIdleState);
  unsigned long now = millis();

  if (currentState != lastClapState) {
    Serial.print("Clap sensor: ");
    Serial.println(clapTriggered ? "SI" : "NO");
    lastClapState = currentState;
  }

  if (clapTriggered && !lastClapTriggered && (now - lastClapEdgeMs) > clapDebounceMs) {
    clapCounter = (now - lastClapDetectedMs <= clapSequenceWindowMs) ? clapCounter + 1 : 1;
    lastClapDetectedMs = now;
    lastClapEdgeMs = now;

    if (clapCounter >= 2) {
      clapTargetState = !clapTargetState;

      // Avisar al ESP/app para sincronizar el estado del botón
      if (clapTargetState) {
        ESP_SERIAL.print("[ON5]");
      } else {
        ESP_SERIAL.print("[OFF5]");
      }

      digitalWrite(clapTargetPin, clapTargetState ? HIGH : LOW);
      Serial.print("Dos aplausos detectados: pin 5 ");
      Serial.println(clapTargetState ? "encendido" : "apagado");
      clapCounter = 0;
    }
  }
  else if (!clapTriggered && lastClapTriggered) {
    lastClapEdgeMs = now;
  }

  if (clapCounter > 0 && (now - lastClapDetectedMs) > (clapSequenceWindowMs * 2)) {
    clapCounter = 0;
  }
}