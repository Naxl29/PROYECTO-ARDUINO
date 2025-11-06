# 🐳 Docker Setup - Proyecto Arduino

Guía rápida para ejecutar la aplicación con Docker.

## 📋 Requisitos Previos

- Docker instalado ([Descargar Docker](https://www.docker.com/get-started))
- Docker Compose instalado (viene incluido con Docker Desktop)

## 🚀 Inicio Rápido

### 1. Construir y ejecutar los contenedores

```bash
docker-compose up -d --build
```

Este comando:
- Construye la imagen de la aplicación Flask
- Inicia el contenedor de MySQL
- Inicia el contenedor de la aplicación web
- Ejecuta todo en segundo plano (`-d`)

### 2. Ver los logs

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs solo de la aplicación web
docker-compose logs -f web

# Ver logs solo de la base de datos
docker-compose logs -f db
```

### 3. Acceder a la aplicación

Una vez que los contenedores estén corriendo, accede a:
- **Aplicación web**: http://localhost:5000
- **Base de datos MySQL**: localhost:3306

## 🛠️ Comandos Útiles

### Detener los contenedores
```bash
docker-compose down
```

### Detener y eliminar volúmenes (⚠️ elimina la base de datos)
```bash
docker-compose down -v
```

### Reconstruir solo la aplicación web
```bash
docker-compose build web
docker-compose up -d web
```

### Ejecutar comandos dentro del contenedor
```bash
# Acceder al shell del contenedor web
docker-compose exec web bash

# Acceder a MySQL
docker-compose exec db mysql -u arduino_user -parduino_pass arduino
```

### Ver el estado de los contenedores
```bash
docker-compose ps
```

## ⚙️ Configuración

### Variables de Entorno

Las variables de entorno se pueden modificar en el archivo `docker-compose.yml`:

```yaml
environment:
  DB_HOST: db                    # Host de MySQL (usar 'db' para Docker)
  DB_PORT: 3306                  # Puerto de MySQL
  DB_DATABASE: arduino           # Nombre de la base de datos
  DB_USER: arduino_user          # Usuario de MySQL
  DB_PASSWORD: arduino_pass      # Contraseña de MySQL
  FLASK_SECRET_KEY: "..."        # Cambiar en producción
  ARDUINO_IP: "192.168.101.77"   # IP del Arduino (opcional)
```

### Usar archivo .env (opcional)

Puedes crear un archivo `.env` en la raíz del proyecto y Docker Compose lo leerá automáticamente:

```env
DB_HOST=db
DB_PORT=3306
DB_DATABASE=arduino
DB_USER=arduino_user
DB_PASSWORD=arduino_pass
FLASK_SECRET_KEY=tu-clave-secreta-aqui
```

## 📦 Estructura de Volúmenes

- `mysql_data`: Persiste los datos de MySQL
- `./static:/app/static`: Monta los archivos estáticos
- `./templates:/app/templates`: Monta las plantillas
- `./Model:/app/Model`: Monta los modelos

## 🔧 Solución de Problemas

### El contenedor no inicia
```bash
# Ver logs detallados
docker-compose logs web

# Verificar que el puerto 5000 no esté en uso
netstat -an | grep 5000
```

### La base de datos no se conecta
```bash
# Verificar que MySQL esté saludable
docker-compose ps

# Ver logs de MySQL
docker-compose logs db
```

### Reconstruir desde cero
```bash
# Detener y eliminar todo
docker-compose down -v

# Reconstruir
docker-compose up -d --build
```

## 📝 Notas

- La base de datos se inicializa automáticamente al iniciar la aplicación
- Los datos de MySQL persisten en el volumen `mysql_data`
- Para desarrollo, los cambios en `static/`, `templates/` y `Model/` se reflejan automáticamente gracias a los volúmenes montados

