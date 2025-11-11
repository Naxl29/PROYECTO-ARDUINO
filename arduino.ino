const int ledPin1 = 13;  // LED 1
const int ledPin2 = 12;  // LED 2
const int ledPin3 = 11;  // LED 3
const int ledPin4 = 10;  // LED 4
const int ledPin5 = 9;  // LED 5
const int ledPin6 = 8;  // LED 6
const int ledPin7 = 7;  // LED 7
const int ledPin8 = 6;  // LED 8

void setup() {
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin4, OUTPUT);
  pinMode(ledPin5, OUTPUT);
  pinMode(ledPin6, OUTPUT);
  pinMode(ledPin7, OUTPUT);
  pinMode(ledPin8, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Comandos para LED 1
    if (command == "ON1") {
      digitalWrite(ledPin1, HIGH);
      Serial.println("LED 1 encendido");
    } 
    else if (command == "OFF1") {
      digitalWrite(ledPin1, LOW);
      Serial.println("LED 1 apagado");
    } 
    // Comandos para LED 2
    else if (command == "ON2") {
      digitalWrite(ledPin2, HIGH);
      Serial.println("LED 2 encendido");
    } 
    else if (command == "OFF2") {
      digitalWrite(ledPin2, LOW);
      Serial.println("LED 2 apagado");
    }
    // Comandos para LED 3
    else if (command == "ON3") {
      digitalWrite(ledPin3, HIGH);
      Serial.println("LED 3 encendido");
    }
    else if (command == "OFF3") {
      digitalWrite(ledPin3, LOW);
      Serial.println("LED 3 apagado");
    }
    // Comandos para LED 4
    else if (command == "ON4") {
      digitalWrite(ledPin4, HIGH);
      Serial.println("LED 4 encendido");
    }
    else if (command == "OFF4") {
      digitalWrite(ledPin4, LOW);
      Serial.println("LED 4 apagado");
    }
    // Comandos para LED 5
    else if (command == "ON5") {
      digitalWrite(ledPin5, HIGH);
      Serial.println("LED 5 encendido");
    }
    else if (command == "OFF5") {
      digitalWrite(ledPin5, LOW);
      Serial.println("LED 5 apagado");
    }
    // Comandos para LED 6
    else if (command == "ON6") {
      digitalWrite(ledPin6, HIGH);
      Serial.println("LED 6 encendido");
    }
    else if (command == "OFF6") {
      digitalWrite(ledPin6, LOW);
      Serial.println("LED 6 apagado");
    }
    // Comandos para LED 7
    else if (command == "ON7") {
      digitalWrite(ledPin7, HIGH);
      Serial.println("LED 7 encendido");
    }
    else if (command == "OFF7") {
      digitalWrite(ledPin7, LOW);
      Serial.println("LED 7 apagado");
    }
    // Comandos para LED 8
    else if (command == "ON8") {
      digitalWrite(ledPin8, HIGH);
      Serial.println("LED 8 encendido");
    }
    else if (command == "OFF8") {
      digitalWrite(ledPin8, LOW);
      Serial.println("LED 8 apagado");
    }
    // Encender todos
    else if (command == "ONALL") {
      digitalWrite(ledPin1, HIGH);
      digitalWrite(ledPin2, HIGH);
      digitalWrite(ledPin3, HIGH);
      digitalWrite(ledPin4, HIGH);
      digitalWrite(ledPin5, HIGH);
      digitalWrite(ledPin6, HIGH);
      digitalWrite(ledPin7, HIGH);
      digitalWrite(ledPin8, HIGH);
      Serial.println("Todos los LEDs encendidos");
    }
    // Apagar todos
    else if (command == "OFFALL") {
      digitalWrite(ledPin1, LOW);
      digitalWrite(ledPin2, LOW);
      digitalWrite(ledPin3, LOW);
      digitalWrite(ledPin4, LOW);
      digitalWrite(ledPin5, LOW);
      digitalWrite(ledPin6, LOW);
      digitalWrite(ledPin7, LOW);
      digitalWrite(ledPin8, LOW);
      Serial.println("Todos los LEDs apagados");
    }
    else {
      Serial.println("Comando no reconocido. Usa: ON1, OFF1, ON2, OFF2, ON3, OFF3, ON4, OFF4, ON5, OFF5, ON6, OFF6, ON7, OFF7, ON8, OFF8 ONALL, OFFALL");
    }
  }
}