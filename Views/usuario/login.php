<?php
require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
?>
    <link rel="stylesheet" href="/PROYECTO-ARDUINO/css/styles.css">

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
            <a href="boton.html">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                Iniciar
            </a>
        </form>
        <p>No tienes una cuenta?<a href="registrarse.html" class="a2">Registrate!</a></p>
    </div>
    
 

