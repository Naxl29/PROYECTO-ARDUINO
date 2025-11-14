<?php   
session_start(); // Iniciar sesión

require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/BloqueController.php");
$obj = new BloqueController();

$usuario = $_POST['usuario'];
$contrasena = $_POST['contrasena'];
$id_usuario = $obj->save($usuario, $contrasena);

if ($id_usuario) {
    $_SESSION['id_usuario'] = $id_usuario; 
    header("Location: /PROYECTO-ARDUINO/Views/usuario/button.php");
}