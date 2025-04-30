<?php   
//Este store sirve para guardar los datos registrados en el formulario
    require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
    $obj = new UsuarioController();
    $usuario = $_POST['usuario'];
    $contrasena = $_POST['contraseña'];
    $obj->save($usuario, $contrasena);