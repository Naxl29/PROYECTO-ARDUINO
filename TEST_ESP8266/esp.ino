#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>

const char* WIFI_SSID = "Prueba";
const char* WIFI_PASSWORD = "12345678";

const char* WS_HOST = "https://domotica-lz0k.onrender.com";
const uint16_t WS_PORT = 443;
const char* HARDWARE_TOKEN = "97a2477504885f006252b4a291250e9bf8d7c44cf4c6e586ee05d072ac28632a";

WebSocketsClient webSocket;
String wsPath;

const unsigned long WIFI_RETRY_MS = 10000;
unsigned long lastWifiAttempt = 0;

void connectWiFi();
void setupWebSocket();
void webSocketEvent(WStype_t type, uint8_t* payload, size_t length);
void ensureWiFi();
void handleMessage(const String& message);
void processCommand(const String& led, const String& state);
void processCommandAll(const String& state);
String extractJsonValue(const String& json, const String& key);
bool isNumeric(const String& value);
void sendSerialCommand(const String& command);

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);

  connectWiFi();
  wsPath = String("/ws/arduino?token=") + HARDWARE_TOKEN;
  setupWebSocket();
}

void loop() {
  ensureWiFi();
  webSocket.loop();
}

void connectWiFi() {
  Serial.println("Conectando a WiFi...");
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado. IP: ");
  Serial.println(WiFi.localIP());
}

void ensureWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }
  unsigned long now = millis();
  if (now - lastWifiAttempt < WIFI_RETRY_MS) {
    return;
  }
  lastWifiAttempt = now;
  Serial.println("Reconectando a WiFi...");
  WiFi.disconnect();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

void setupWebSocket() {
  webSocket.beginSSL(WS_HOST, WS_PORT, wsPath.c_str());
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
  webSocket.enableHeartbeat(15000, 3000, 2);
  Serial.println("Intentando conexión WebSocket...");
}

void webSocketEvent(WStype_t type, uint8_t* payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.println("WebSocket desconectado.");
      break;
    case WStype_CONNECTED:
      Serial.println("WebSocket conectado.");
      break;
    case WStype_TEXT: {
      String message;
      for (size_t i = 0; i < length; i++) {
        message += static_cast<char>(payload[i]);
      }
      handleMessage(message);
      break;
    }
    case WStype_ERROR:
      Serial.println("Error en WebSocket.");
      break;
    case WStype_PING:
      Serial.println("Ping recibido.");
      break;
    case WStype_PONG:
      Serial.println("Pong recibido.");
      break;
    default:
      break;
  }
}

void handleMessage(const String& message) {
  Serial.print("Mensaje recibido: ");
  Serial.println(message);
  String type = extractJsonValue(message, "type");
  if (type == "command") {
    String led = extractJsonValue(message, "led");
    String state = extractJsonValue(message, "state");
    processCommand(led, state);
  } else if (type == "commandAll") {
    String state = extractJsonValue(message, "state");
    processCommandAll(state);
  } else if (type.length() > 0) {
    Serial.println("Tipo de mensaje no soportado.");
  }
}

void processCommand(const String& led, const String& state) {
  if (!isNumeric(led)) {
    Serial.println("LED inválido en comando.");
    return;
  }
  if (state != "0" && state != "1") {
    Serial.println("Estado inválido en comando.");
    return;
  }
  String command = "[" + String(state == "1" ? "ON" : "OFF") + led + "]";
  sendSerialCommand(command);
}

void processCommandAll(const String& state) {
  if (state != "0" && state != "1") {
    Serial.println("Estado inválido en comando global.");
    return;
  }
  String command = state == "1" ? "[ONALL]" : "[OFFALL]";
  sendSerialCommand(command);
}

String extractJsonValue(const String& json, const String& key) {
  String pattern = "\"" + key + "\":";
  int index = json.indexOf(pattern);
  if (index < 0) {
    return "";
  }
  index += pattern.length();
  while (index < static_cast<int>(json.length()) && json[index] == ' ') {
    index++;
  }
  if (index >= static_cast<int>(json.length())) {
    return "";
  }
  char terminator = json[index];
  if (terminator != '\"' && terminator != '\'') {
    return "";
  }
  index++;
  int endIndex = json.indexOf(terminator, index);
  if (endIndex < 0) {
    return "";
  }
  return json.substring(index, endIndex);
}

bool isNumeric(const String& value) {
  if (value.length() == 0) {
    return false;
  }
  for (size_t i = 0; i < value.length(); i++) {
    if (!isDigit(value[i])) {
      return false;
    }
  }
  return true;
}

void sendSerialCommand(const String& command) {
  Serial.print("Enviando a Mega: ");
  Serial.println(command);
  Serial1.print(command);
}
