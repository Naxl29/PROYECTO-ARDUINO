## Estado actual
- La inicialización de tablas se reparte entre `Model/init_db.py` y métodos auxiliares `_prepare`/`_ensure_tables` en `Model/led_device.py`, `Model/section.py` y `Model/device_flags.py`.
- Varias operaciones SQL se intentan en cada uso del modelo, con manejo amplio de excepciones que oculta errores reales.

## Estado final
- Toda la creación y migración de tablas se centraliza en `Model/init_db.py` mediante funciones puras y tipadas.
- Los modelos consumen tablas ya existentes sin ejecutar DDL en tiempo de uso ni silenciar excepciones.
- La aplicación inicializa el esquema y los datos por defecto en el arranque y detiene la ejecución si ocurre un error.

## Archivos a modificar
- `Model/init_db.py`
- `Model/led_device.py`
- `Model/section.py`
- `Model/device_flags.py`
- `app.py`

## Tareas
1. Reestructurar `Model/init_db.py` en estilo funcional, añadiendo toda la definición de tablas y migraciones con tipado estático y errores explícitos.
2. Ajustar los modelos (`led_device`, `section`, `device_flags`) para eliminar lógica de inicialización diferida y mejorar el manejo de errores.
3. Actualizar `app.py` para invocar las nuevas funciones de inicialización y propagar errores.
4. Probar manualmente rutas afectadas (mínimo smoke test) y revisar linting si aplica.

