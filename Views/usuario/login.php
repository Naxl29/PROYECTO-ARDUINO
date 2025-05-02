<?php
require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
?>
    <link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">
    <link rel="stylesheet" href="css/Registro.css">


    <div class="login-box">
        <p>Iniciar sesion</p>
        <form action="/PROYECTO-ARDUINO/Views/usuario/validation.php" method="post">
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
    
 

