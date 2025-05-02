<?php
 require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");

 if ($_SERVER['REQUEST_METHOD'] == 'POST') {
     $usuario = $_POST['usuario'];
     $contrasena = $_POST['contrasena'];

     $controller = new UsuarioController();
     $controller->login($usuario, $contrasena);
 }
    else {
        header("Location:button.php");
    }

