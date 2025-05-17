const int ledPin = 13;  // Pin donde está conectado el LED

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "ON" || command == "1") {
      digitalWrite(ledPin, HIGH);
      Serial.println("LED encendido");
    } 
    else if (command == "OFF" || command == "0") {
      digitalWrite(ledPin, LOW);
      Serial.println("LED apagado");
    }
  }
}
