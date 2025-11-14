## Estado actual
- El sistema gestiona autenticación básica desde `BloqueController`, con rutas en `app.py` para crear y acceder a usuarios.
- No existe un módulo administrativo para listar, actualizar ni eliminar usuarios; las vistas bajo `templates/usuario/` cubren solo registro y login.

## Estado deseado
- Disponer de un módulo administrativo que permita listar usuarios, crear nuevos registros con asignación de roles, editar información básica y eliminar usuarios de forma segura.
- Integrar las capacidades de gestión en rutas protegidas para administradores, con plantillas coherentes con el resto del proyecto.

## Archivos a modificar
- `app.py`
- `Controller/bloque_controller.py`
- `Model/bloque.py`
- `templates/admin/` (nuevas vistas de usuarios)
- `templates/components/` o `templates/layouts/` si se requieren parciales
- `static/js/` para soporte dinámico (confirmaciones, fetch)

## Lista de tareas
1. Revisar y extender `Bloque` y `BloqueController` para operaciones CRUD completas de usuarios.
2. Definir rutas protegidas para administración de usuarios en `app.py`.
3. Crear vistas y recursos front-end utilizando el layout Admin existente para listar y gestionar usuarios.
4. Implementar eliminación con confirmaciones y manejo de errores.
5. Validar funcionalidad completa y actualizar documentación si aplica.

