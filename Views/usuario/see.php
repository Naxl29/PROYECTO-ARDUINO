<?php
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
    $obj = new UsuarioController();
    $rows = $obj->see();
?>

<div class="mb-3">
    <a href="/PROYECTO-ARDUINO/Views/index.php" class="btn btn-primary">Regresar</a>
</div>

<table class="table table-striped table-h">
    <thead class="table-dark">
        <tr>
            <th scope="col">ID</th>
            <th scope="col">USUARIO</th>
            <th scope="col">CONTRASEÑA</th>
        </tr>
    </thead>
    <tbody>
        <?php if($rows): ?>
            <?php foreach($rows as $row): ?>
                <tr>
                    <th><?= $row['id'] ?></th>
                    <th><?= $row['usuario'] ?></th>
                    <th><?= $row['contrasena'] ?></th>
                </tr>
            <?php endforeach; ?>
        <?php else: ?>
            <tr>
                <td colspan="6" class="text-center">No hay registros</td>
            </tr>
        <?php endif; ?>
    </tbody>
</table>