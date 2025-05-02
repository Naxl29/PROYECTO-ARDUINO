<?php
require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
?>
    <link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">
    <link rel="stylesheet" href="css/Registro.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.5/dist/sweetalert2.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.5/dist/sweetalert2.all.min.js"></script>
    <div class="login-box">
        <p>Iniciar sesion</p>
        <form method="post">
            <div class="user-box">
                <input type="text" id="usuario" name="usuario" required>
                <label>Usuario</label>
            </div>
            <div class="user-box">
                <input type="password" id="contrasena" name="contrasena" required>
                <label for="contrasena">Contraseña</label>
            </div>
            <button type="submit" class="button">
                <div class="blob1"></div>
                <div class="blob2"></div>
                <div class="inner">Iniciar</div>
            </button>
        </form>
        <p>No tienes una cuenta?<a href="/PROYECTO-ARDUINO/Views/usuario/create.php" class="a2"> Registrate!</a></p>
    </div>
