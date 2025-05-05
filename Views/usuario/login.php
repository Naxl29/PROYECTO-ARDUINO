<?php
require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/BloqueController.php");
?>
<link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">
<link rel="stylesheet" href="css/Registro.css">
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

<div class="login-box">
    <p>Iniciar sesión</p>
    <form id="campos" method="post" action="/PROYECTO-ARDUINO/Views/usuario/validation.php">
        <div class="user-box">
            <input type="text" id="usuario" name="usuario">
            <label>Usuario</label>
        </div>
        <div class="user-box">
            <input type="password" id="contrasena" name="contrasena">
            <label>Contraseña</label>
        </div>
        <button type="submit" class="button">
            <div class="blob1"></div>
            <div class="blob2"></div>
            <div class="inner">Iniciar</div>
        </button>
    </form>
    <p>¿No tienes una cuenta? <a href="/PROYECTO-ARDUINO/Views/usuario/create.php" class="a2">¡Regístrate!</a></p>
</div>

<script>
document.getElementById('campos').addEventListener('submit', function (e) {
    const usuario = document.getElementById('usuario').value.trim();
    const contrasena = document.getElementById('contrasena').value.trim();

    if (usuario === '' || contrasena === '') {
        e.preventDefault(); // Detiene el envío del formulario
        Swal.fire({
            icon: 'warning',
            title: 'Campos vacíos',
            text: 'Por favor, completa todos los campos.'
        }); 
    }
});
</script>

