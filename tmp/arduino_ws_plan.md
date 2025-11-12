## Estado actual
- El sketch `TEST_ESP8266/esp.ino` expone un servidor HTTP local que controla los LEDs mediante rutas `/ONx`, `/OFFx`, y no se conecta al backend desplegado en Render.
- No existe lógica para abrir un WebSocket, enviar el token `HARDWARE_API_TOKEN` ni procesar comandos JSON provenientes del servidor.

## Estado final
- El ESP8266 se conecta al WiFi configurado, abre una sesión WebSocket con la URL del backend (`/ws/arduino?token=TOKEN`), mantiene reconexiones y envía pings periódicos.
- El sketch convierte los mensajes JSON recibidos (`command`, `commandAll`) en comandos seriales `[ONx]/[OFFx]/[ONALL]/[OFFALL]` hacia la Mega.
- Se retira el servidor HTTP embebido, manteniendo el monitor serial para depuración.

## Archivos a modificar
- `TEST_ESP8266/esp.ino`

## Tareas
1. Añadir dependencias/librerías necesarias (WebSocketsClient) y configurar constantes para WiFi, URL del WebSocket y token.
2. Implementar conexión WebSocket con manejadores de eventos (open, message, close, reconnect, ping/pong).
3. Interpretar mensajes JSON para reenviarlos por Serial1 a la Mega y reflejarlos en el log.

