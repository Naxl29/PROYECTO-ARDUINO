<?php
//Acá se hará el codigo para mostrar los usuarios y sus detalles
require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");

$obj = new UsuarioController();
$data = $obj->show($_GET['id']);
?>

<table class="table">
    <thead class="table">
        <tr>
            <th scope="col">Id</th>
            <th scope="col">Usuario</th>
            <th scope="col">Contraseña</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td scope="col"><?= $data["id"] ?></td>
            <td scope="col"><?= $data["usuario"] ?></td>
            <td scope="col"><?= $data["contrasena"] ?></td>
        </tr>
    </tbody>
</table>

<a href="see.php" class="btn btn-primary">Continuar</a>