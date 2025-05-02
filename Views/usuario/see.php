<?php
//Apartado para ver el historial
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
    $obj = new UsuarioController();
    $rows = $obj->see();
?>

<div class="mb-3">
    <a href="/PROYECTO-ARDUINO/Views/usuario/button.php" class="btn btn-primary">Regresar</a>
</div>

<link rel="stylesheet" href="/PROYECTO-ARDUINO/css/styles.css">
    <div class="historial-container">
        <h1>Historial de Acceso e Interruptor</h1>
        <table class="historial-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>USUARIO</th>
                    <th>CONTRASEÑA</th>
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