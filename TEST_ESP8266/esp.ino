#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

// Configuración WiFi
const char* ssid = "Prueba";
const char* password = "12345678";

ESP8266WebServer server(80);
MDNSResponder mdns;

// Pines de la Mega que queremos controlar (LED 1 -> pin 13, LED 2 -> pin 12, etc.)
const int ledPins[] = {13, 12, 11, 10, 9, 8, 7, 6, 5};
const int numLeds = sizeof(ledPins) / sizeof(ledPins[0]);

// Página web dinámica
String webPage = "";

void setup() {
  Serial.begin(115200);      // Debug al PC
  Serial1.begin(115200);     // Comunicación con la Mega por Serial1 (TX / RX)

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  mdns.begin("esp8266", WiFi.localIP());

  // Generar la página web con estilo CSS y botones para cada pin
  webPage = "<!DOCTYPE html><html><head><meta charset='UTF-8'>";
  webPage += "<title>Control de LEDs Mega</title>";
  webPage += "<style>";
  webPage += "body { font-family: Arial; background: #f0f0f0; text-align:center; }";
  webPage += "h1 { color: #333; }";
  webPage += ".led-container { margin: 10px auto; padding: 10px; background: #fff; border-radius: 8px; width: 320px; box-shadow: 0 0 10px rgba(0,0,0,0.2); }";
  webPage += ".led-row { margin: 8px 0; }";
  webPage += "button { padding: 10px 20px; margin: 5px 5px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }";
  webPage += ".on { background-color: #4CAF50; color: white; }";
  webPage += ".off { background-color: #f44336; color: white; }";
  webPage += ".all { background-color: #2196F3; color: white; }";
  webPage += "</style></head><body>";
  webPage += "<h1>Control de LEDs Mega</h1>";

  // Botones para todos
  webPage += "<div class='led-container'>";
  webPage += "<div class='led-row'>";
  webPage += "<a href='/ONALL'><button class='all'>ON TODOS</button></a>";
  webPage += "<a href='/OFFALL'><button class='all'>OFF TODOS</button></a>";
  webPage += "</div>";
  webPage += "</div>";

  // Botones individuales
  webPage += "<div class='led-container'>";
  for (int i = 0; i < numLeds; i++) {
    int ledNumber = i + 1;
    int pin = ledPins[i];
    webPage += "<div class='led-row'>";
    webPage += "LED " + String(ledNumber) + " (pin " + String(pin) + ")";
    webPage += " <a href='/ON" + String(ledNumber) + "'><button class='on'>ON</button></a>";
    webPage += " <a href='/OFF" + String(ledNumber) + "'><button class='off'>OFF</button></a>";
    webPage += "</div>";
  }
  webPage += "</div></body></html>";

  // Manejo de la raíz
  server.on("/", []() {
    server.send(200, "text/html", webPage);
  });

  // Crear rutas dinámicas para cada pin
  for (int i = 0; i < numLeds; i++) {
    int ledNumber = i + 1;
    String onPath = "/ON" + String(ledNumber);
    server.on(onPath.c_str(), [ledNumber]() {
      String cmd = "[ON" + String(ledNumber) + "]";
      Serial.println(cmd);
      Serial1.print(cmd);
      server.send(200, "text/html", webPage);
    });

    String offPath = "/OFF" + String(ledNumber);
    server.on(offPath.c_str(), [ledNumber]() {
      String cmd = "[OFF" + String(ledNumber) + "]";
      Serial.println(cmd);
      Serial1.print(cmd);
      server.send(200, "text/html", webPage);
    });
  }

  // --- NUEVO: rutas para ONALL y OFFALL ---
  server.on("/ONALL", []() {
    Serial.println("[ONALL]");
    Serial1.print("[ONALL]");
    server.send(200, "text/html", webPage);
  });

  server.on("/OFFALL", []() {
    Serial.println("[OFFALL]");
    Serial1.print("[OFFALL]");
    server.send(200, "text/html", webPage);
  });

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
