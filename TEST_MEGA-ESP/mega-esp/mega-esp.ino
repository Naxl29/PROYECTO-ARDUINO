#include <MemoryFree.h>
#include <EEPROM.h>
#include <LiquidCrystal.h>

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

const byte lcdColumns = 16;
const byte lcdRows = 2;
const byte lcdRS = 6;
const byte lcdEN = 22;
const byte lcdD4 = 23;
const byte lcdD5 = 24;
const byte lcdD6 = 27;
const byte lcdD7 = 28;
const byte lcdPowerPin = 29;

LiquidCrystal lcd(lcdRS, lcdEN, lcdD4, lcdD5, lcdD6, lcdD7);

const char lcdMessage[] = "ADSO-2923560";
const byte lcdMessageLength = sizeof(lcdMessage) - 1;
bool pin6Active = false;
bool lcdInitialized = false;
unsigned long lastLcdMoveMs = 0;
const unsigned long lcdMoveIntervalMs = 800;

const byte animationPositions[][2] = {
  {0, 0},
  {4, 1},
  {2, 0},
  {1, 1},
  {3, 0},
  {0, 1}
};
const byte numAnimationPositions = sizeof(animationPositions) / sizeof(animationPositions[0]);
byte currentAnimationIndex = 0;

bool ledStates[numLeds] = {false};

const byte clapSensorPin = 2;          // Salida digital del KY-036
const byte clapTargetPin = 5;          // Pin a encender tras detectar dos aplausos
const byte clapTargetLedNumber = 9;    // LED correspondiente al pin objetivo (en ledPins)

const unsigned long clapDebounceMs = 80;
const unsigned long clapSequenceWindowMs = 600;

bool clapIdleState = LOW;
bool clapTargetState = LOW;
bool lastClapState = LOW;

unsigned long lastClapEdgeMs = 0;
unsigned long lastClapDetectedMs = 0;
byte clapCounter = 0;

void setLedState(byte ledIndex, bool state);
void setLedStateByPin(byte pin, bool state);
void updatePin6State(bool active);
void handleLcdAnimation();
void showMessageAtCurrentPosition();

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
  }

  lcd.begin(lcdColumns, lcdRows);
  lcd.clear();
  lcdInitialized = true;
  pinMode(lcdPowerPin, OUTPUT);
  digitalWrite(lcdPowerPin, HIGH);
  lcd.noDisplay();

  for (byte i = 0; i < numLeds; i++) {
    setLedState(i, false);
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
  handleLcdAnimation();
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
        for (byte i = 0; i < numLeds; i++) setLedState(i, true);
        Serial.println("Todos los LEDs encendidos");
      }
      // --- Apagar todos ---
      else if (inString.indexOf("[OFFALL]") >= 0) {
        for (byte i = 0; i < numLeds; i++) setLedState(i, false);
        clapTargetState = false;
        Serial.println("Todos los LEDs apagados");
      }
      else {
        // --- Comando individual ---
        for (byte i = 0; i < numLeds; i++) {
          String onCmd = "[ON" + String(i + 1) + "]";
          String offCmd = "[OFF" + String(i + 1) + "]";
          if (inString.indexOf(onCmd) >= 0) {
            setLedState(i, true);
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
            setLedState(i, false);
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

void setLedState(byte ledIndex, bool state) {
  if (ledIndex >= numLeds) {
    return;
  }

  bool stateChanged = (ledStates[ledIndex] != state);
  ledStates[ledIndex] = state;
  byte pin = ledPins[ledIndex];
  if (pin != lcdRS) {
    digitalWrite(pin, state ? HIGH : LOW);
  }

  if (stateChanged && pin == lcdRS) {
    updatePin6State(state);
  }
}

void setLedStateByPin(byte pin, bool state) {
  for (byte i = 0; i < numLeds; i++) {
    if (ledPins[i] == pin) {
      setLedState(i, state);
      return;
    }
  }
}

void updatePin6State(bool active) {
  if (active) {
    pin6Active = true;
    currentAnimationIndex = 0;
    lastLcdMoveMs = millis();
    digitalWrite(lcdPowerPin, LOW);
    delay(5);
    if (!lcdInitialized) {
      lcd.begin(lcdColumns, lcdRows);
      lcdInitialized = true;
    }
    lcd.display();
    lcd.clear();
    showMessageAtCurrentPosition();
  } else if (pin6Active) {
    pin6Active = false;
    lcd.clear();
    lcd.noDisplay();
    digitalWrite(lcdPowerPin, HIGH);
    lcdInitialized = false;
  }
}

void handleLcdAnimation() {
  if (!pin6Active) {
    return;
  }

  unsigned long now = millis();
  if (now - lastLcdMoveMs < lcdMoveIntervalMs) {
    return;
  }

  lastLcdMoveMs = now;
  currentAnimationIndex = (currentAnimationIndex + 1) % numAnimationPositions;
  showMessageAtCurrentPosition();
}

void showMessageAtCurrentPosition() {
  int col = animationPositions[currentAnimationIndex][0];
  int row = animationPositions[currentAnimationIndex][1];

  if (row >= lcdRows) {
    row = lcdRows - 1;
  }
  if (row < 0) {
    row = 0;
  }

  int maxCol = lcdColumns - lcdMessageLength;
  if (maxCol < 0) {
    maxCol = 0;
  }
  if (col > maxCol) {
    col = maxCol;
  }
  if (col < 0) {
    col = 0;
  }

  lcd.clear();
  lcd.setCursor(col, row);
  lcd.print(lcdMessage);
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

      ESP_SERIAL.print("[SYNC");
      ESP_SERIAL.print(clapTargetLedNumber);
      ESP_SERIAL.print(":");
      ESP_SERIAL.print(clapTargetState ? 1 : 0);
      ESP_SERIAL.print("]");
      setLedStateByPin(clapTargetPin, clapTargetState);
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