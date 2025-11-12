## Estado actual
- El servidor Flask se comunica con Arduino vía peticiones HTTP directas (`requests`) desde `ArduinoService`, lo que falla cuando la app corre en Render porque no puede alcanzar el dispositivo en red local.
- No existe soporte para conexiones persistentes ni canales inversos desde el Arduino hacia el servidor.

## Estado final
- El servidor expone un endpoint WebSocket que permite al Arduino iniciar la conexión saliente.
- `ArduinoService` envía comandos a través de la sesión WebSocket activa y gestiona confirmaciones/errores explícitos.
- Se eliminan las llamadas HTTP directas, evitando dependencias de red directa y permitiendo funcionamiento detrás de NAT.

## Archivos a modificar
- `requirements.txt`
- `app.py`
- `config/arduino_service.py`
- `Controller/led_controller.py`
- `Controller/led_device_controller.py`
- Posible archivo nuevo para utilidades de WebSocket según necesidad.

## Tareas
1. Añadir dependencias WebSocket (Flask-Sock / simple-websocket) y preparar estructuras compartidas para conexiones activas.
2. Implementar en `app.py` la ruta WebSocket para que Arduino se registre, mantenga latidos y reciba comandos.
3. Actualizar `ArduinoService` para publicar comandos por la conexión WebSocket y reportar errores claros si no hay sesión.
4. Ajustar controladores que envían comandos para utilizar el nuevo flujo y validar respuestas.

