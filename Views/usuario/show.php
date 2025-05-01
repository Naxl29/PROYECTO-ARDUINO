<?php
//Acá se hará el codigo para mostrar los usuarios y sus detalles
require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");

$obj = new UsuarioController();
$data = $obj->show($_GET['id']);
?>

<link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">
<div class="container">
        <h1 class="text-center">Datos de Usuario Registrado</h1>
        <table class="table table-striped table-bordered table-hover">
            <thead>
                <tr>
                    <th>Usuario</th>
                    <th>Contraseña</th>
                </tr>
            </thead>
    </thead>
    <tbody>
        <tr>
            <td scope="col"><?= $data["usuario"] ?></td>
            <td scope="col"><?= $data["contrasena"] ?></td>
        </tr>
    </tbody>
</table>

<a href="/PROYECTO-ARDUINO/Views/usuario/button.php" class="btn btn-primary">Continuar</a>