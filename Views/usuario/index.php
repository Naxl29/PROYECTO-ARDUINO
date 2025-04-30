<?php
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
    $obj = new UsuarioController();
    $rows = $obj->index();
?>

<div class="mb-3">
    <a href="/PROYECTO-ARDUINO/Views/usuario/create.php" class="btn btn-primary">Agregar Usuario</a>
</div>

