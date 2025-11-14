#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

namespace {
constexpr uint32_t kMegaBaud = 115200;
constexpr uint32_t kDebugBaud = 115200;
constexpr unsigned long kMegaCommandGapMs = 250;

const char* ssid = "Prueba";
const char* password = "12345678";

ESP8266WebServer server(80);
MDNSResponder mdns;

// Pines de la Mega que queremos controlar (LED 1 -> pin 13, LED 2 -> pin 12, etc.)
const int ledPins[] = {13, 12, 11, 10, 9, 8, 7, 6, 5};
const int numLeds = sizeof(ledPins) / sizeof(ledPins[0]);
bool ledStates[numLeds] = {false};

String megaRxBuffer;
unsigned long lastMegaByteMs = 0;

#define MEGA_SERIAL Serial
#define DEBUG_SERIAL Serial1

void debugPrint(const String& message) {
#if defined(DEBUG_SERIAL)
  DEBUG_SERIAL.print(message);
#else
  (void)message;
#endif
}

void debugPrintln(const String& message) {
#if defined(DEBUG_SERIAL)
  DEBUG_SERIAL.println(message);
#else
  (void)message;
#endif
}

void sendCommandToMega(const String& command) {
  MEGA_SERIAL.print(command);
  MEGA_SERIAL.flush();
  debugPrint("-> ");
  debugPrintln(command);
}

void notifyMegaConsole(const String& message) {
  MEGA_SERIAL.print("# ");
  MEGA_SERIAL.println(message);
}

void setLedStateLocally(int index, bool state) {
  if (index < 0 || index >= numLeds) {
    return;
  }
  ledStates[index] = state;
}

void setAllLedStates(bool state) {
  for (int i = 0; i < numLeds; ++i) {
    ledStates[i] = state;
  }
}

void applyMegaCommand(const String& command) {
  debugPrint("<= ");
  debugPrintln(command);

  if (command.equalsIgnoreCase("[ONALL]")) {
    setAllLedStates(true);
    return;
  }
  if (command.equalsIgnoreCase("[OFFALL]")) {
    setAllLedStates(false);
    return;
  }

  if (command.startsWith("[ON") && command.endsWith("]")) {
    int ledNumber = command.substring(3, command.length() - 1).toInt();
    setLedStateLocally(ledNumber - 1, true);
    return;
  }

  if (command.startsWith("[OFF") && command.endsWith("]")) {
    int ledNumber = command.substring(4, command.length() - 1).toInt();
    setLedStateLocally(ledNumber - 1, false);
    return;
  }

  if (command.startsWith("[SYNC") && command.endsWith("]")) {
    const int separator = command.indexOf(':');
    if (separator > 0) {
      const int ledNumber = command.substring(5, separator).toInt();
      const int value = command.substring(separator + 1, command.length() - 1).toInt();
      setLedStateLocally(ledNumber - 1, value != 0);
    }
    return;
  }
}

void handleMegaSerial() {
  while (MEGA_SERIAL.available()) {
    char incoming = static_cast<char>(MEGA_SERIAL.read());
    unsigned long now = millis();

    if (now - lastMegaByteMs > kMegaCommandGapMs) {
      megaRxBuffer = "";
    }
    lastMegaByteMs = now;

    if (incoming == '[') {
      megaRxBuffer = "[";
      continue;
    }

    if (megaRxBuffer.length() == 0) {
      continue;
    }

    megaRxBuffer += incoming;

    if (incoming == ']') {
      applyMegaCommand(megaRxBuffer);
      megaRxBuffer = "";
    }
  }
}

String buildButton(const String& path, const String& label, const String& css) {
  String button = "<a href='" + path + "'><button class='" + css + "'>";
  button += label;
  button += "</button></a>";
  return button;
}

String buildWebPage() {
  String page;
  page.reserve(2048);

  page += "<!DOCTYPE html><html><head><meta charset='UTF-8'>";
  page += "<title>Control de LEDs Mega</title>";
  page += "<style>";
  page += "body { font-family: Arial; background: #f0f0f0; text-align:center; }";
  page += "h1 { color: #333; }";
  page += ".led-container { margin: 10px auto; padding: 14px; background: #fff; border-radius: 8px; width: 340px; box-shadow: 0 0 10px rgba(0,0,0,0.2); }";
  page += ".led-row { margin: 10px 0; display:flex; align-items:center; justify-content:space-between; }";
  page += ".led-row span { flex:1; text-align:left; padding-left:8px; }";
  page += "button { padding: 10px 18px; margin: 0 4px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }";
  page += ".on { background-color: #4CAF50; color: white; }";
  page += ".off { background-color: #f44336; color: white; }";
  page += ".all { background-color: #2196F3; color: white; width: 120px; }";
  page += ".state-on { color:#4CAF50; font-weight:bold; }";
  page += ".state-off { color:#f44336; font-weight:bold; }";
  page += "</style></head><body>";
  page += "<h1>Control de LEDs Mega</h1>";

  page += "<div class='led-container'>";
  page += "<div class='led-row' style='justify-content:center;'>";
  page += buildButton("/ONALL", "ON TODOS", "all");
  page += buildButton("/OFFALL", "OFF TODOS", "all");
  page += "</div>";
  page += "</div>";

  page += "<div class='led-container'>";
  for (int i = 0; i < numLeds; ++i) {
    const bool isOn = ledStates[i];
    const int ledNumber = i + 1;

    page += "<div class='led-row'>";
    page += "<span>LED ";
    page += String(ledNumber);
    page += " (pin ";
    page += String(ledPins[i]);
    page += ") &mdash; <span class='";
    page += isOn ? "state-on'>ON" : "state-off'>OFF";
    page += "</span></span>";

    page += buildButton("/ON" + String(ledNumber), "ON", "on");
    page += buildButton("/OFF" + String(ledNumber), "OFF", "off");
    page += "</div>";
  }
  page += "</div></body></html>";

  return page;
}

void registerRoutes() {
  server.on("/", []() {
    server.send(200, "text/html", buildWebPage());
  });

  for (int i = 0; i < numLeds; ++i) {
    const int ledNumber = i + 1;
    const String onPath = "/ON" + String(ledNumber);
    const String offPath = "/OFF" + String(ledNumber);

    server.on(onPath.c_str(), [ledNumber]() {
      setLedStateLocally(ledNumber - 1, true);
      sendCommandToMega("[ON" + String(ledNumber) + "]");
      server.send(200, "text/html", buildWebPage());
    });

    server.on(offPath.c_str(), [ledNumber]() {
      setLedStateLocally(ledNumber - 1, false);
      sendCommandToMega("[OFF" + String(ledNumber) + "]");
      server.send(200, "text/html", buildWebPage());
    });
  }

  server.on("/ONALL", []() {
    setAllLedStates(true);
    sendCommandToMega("[ONALL]");
    server.send(200, "text/html", buildWebPage());
  });

  server.on("/OFFALL", []() {
    setAllLedStates(false);
    sendCommandToMega("[OFFALL]");
    server.send(200, "text/html", buildWebPage());
  });
}

}  // namespace

void setup() {
  DEBUG_SERIAL.begin(kDebugBaud);
  MEGA_SERIAL.begin(kMegaBaud);

  debugPrintln("Iniciando ESP8266...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  debugPrint("Conectando a ");
  debugPrintln(ssid);

  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    debugPrint(".");
  }
  debugPrintln("");
  debugPrint("WiFi listo, IP: ");
  debugPrintln(WiFi.localIP().toString());
  notifyMegaConsole("WiFi listo. IP: " + WiFi.localIP().toString());

  if (mdns.begin("esp8266", WiFi.localIP())) {
    debugPrintln("mDNS responder iniciado (esp8266.local)");
  } else {
    debugPrintln("Error iniciando mDNS");
  }

  registerRoutes();
  server.begin();
  debugPrintln("Servidor HTTP iniciado");
}

void loop() {
  handleMegaSerial();
  server.handleClient();
  mdns.update();
}
