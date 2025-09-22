# PROYECTO ARDUINO - Deployment Guide

## 🚀 Deploy en Render

### Configuración de Variables de Entorno en Render:

```env
DB_HOST=tu-host-railway.app
DB_PORT=26716
DB_DATABASE=railway
DB_USER=root
DB_PASSWORD=tu-password-railway
FLASK_SECRET_KEY=tu-clave-secreta-aqui
FLASK_DEBUG=False
MODEL_PATH=Model/modelo_recibo.pkl
ARDUINO_PORT=COM3
ARDUINO_BAUDRATE=9600
ARDUINO_IP=192.168.101.77
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### Comandos de Build:
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

### Base de Datos:
- Configurada para usar Railway MySQL
- Conexión con PyMySQL
- Variables de entorno configuradas

## 📋 Checklist Pre-Deploy:

✅ requirements.txt actualizado con PyMySQL
✅ Procfile creado
✅ runtime.txt configurado 
✅ Variables de entorno configuradas
✅ app.py preparado para producción
✅ Base de datos configurada con Railway
✅ Archivos estáticos en su lugar
✅ .gitignore actualizado