<?php
require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
?>
    <link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">

    <div class="login-box">
        <p>Iniciar sesion</p>
        <form action="boton.html" method="post">
            <div class="user-box">
                <input required="" name="" type="text">
                <label>Usuario</label>
            </div>
            <div class="user-box">
                <input required="" name="" type="password">
                <label>Contraseña</label>
            </div>
            <button type="submit" class="button">
                <div class="blob1"></div>
                <div class="blob2"></div>
                <div class="inner">Iniciar</div>
            </button>
        </form>
        <p>No tienes una cuenta?<a href="registrarse.html" class="a2">Registrate!</a></p>
    </div>
    
 

