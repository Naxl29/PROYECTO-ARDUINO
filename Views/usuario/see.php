<?php
//Apartado para ver el historial
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
    $obj = new UsuarioController();
    $rows = $obj->see();
?>
<link rel="stylesheet" href="/PROYECTO-ARDUINO/css/styles.css">
<div class="mb-3">
    <a href="/PROYECTO-ARDUINO/Views/usuario/button.php" class="boton-back">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-in-left" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M10 3.5a.5.5 0 0 0-.5-.5h-8a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 1 1 0v2A1.5 1.5 0 0 1 9.5 14h-8A1.5 1.5 0 0 1 0 12.5v-9A1.5 1.5 0 0 1 1.5 2h8A1.5 1.5 0 0 1 11 3.5v2a.5.5 0 0 1-1 0z"/>
            <path fill-rule="evenodd" d="M4.146 8.354a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H14.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708z"/>
        </svg>
    </a>
</div>

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