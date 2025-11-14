<?php
session_start(); // Iniciar sesión
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/BloqueController.php");

// Obtener el estado y el id_usuario desde POST
$estado = $_POST['estado'];
$id_usuario = $_POST['id_usuario'];

// Guardar en la base de datos usando el controlador
$bloqueController = new BloqueController();
$resultado = $bloqueController->saveEstado($id_usuario, $estado);
