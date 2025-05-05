<?php
// Historial de la blockchain
require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/BlockchainController.php");

$controller = new BlockchainController(); // Cambie el nombre de las variables
$bloques = $controller->see();
?>

<link rel="stylesheet" href="/PROYECTO-ARDUINO/css/styles.css">

<div class="mb-3">
    <a href="/PROYECTO-ARDUINO/Views/usuario/button.php" class="boton-back" title="Volver al panel">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-box-arrow-in-left" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M10 3.5a.5.5 0 0 0-.5-.5h-8a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 1 1 0v2A1.5 1.5 0 0 1 9.5 14h-8A1.5 1.5 0 0 1 0 12.5v-9A1.5 1.5 0 0 1 1.5 2h8A1.5 1.5 0 0 1 11 3.5v2a.5.5 0 0 1-1 0z"/>
            <path fill-rule="evenodd" d="M4.146 8.354a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H14.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708z"/>
        </svg>
    </a>
</div>

<div class="historial-container">
    <h1 class="titulo-historial">Historial de Acceso e Interruptor</h1>

    <div class="table-responsive">
        <table class="historial-table">
            <thead>
                <tr>
                    <th>Bloque</th>
                    <th>Usuario</th>
                    <th>Fecha</th>
                    <th>Estado</th>
                    <th>Hash Anterior</th>
                    <th>Hash Actual</th>
                </tr>
            </thead>
            <tbody>
                <?php if (!empty($bloques)): ?>
                    <?php foreach ($bloques as $bloque): ?>
                        <tr>
                            <td><?= htmlspecialchars($bloque['id']) ?></td>
                            <td><?= htmlspecialchars($bloque['usuario']) ?></td>
                            <td><?= htmlspecialchars($bloque['fecha']) ?></td>
                            <td>
                            <?php if ($bloque['estado'] == 1): ?>
                                <span style="color: green;">Encendido</span>
                            <?php elseif ($bloque['estado'] == 0): ?>
                                <span style="color: red;">Apagado</span>
                            <?php else: ?>
                                <span style="color: gray;">Desconocido</span>
                            <?php endif; ?>

                            </td>
                            <td class="hash-col" title="<?= htmlspecialchars($bloque['anterior_hash']) ?>">
                                  <?= substr($bloque['anterior_hash'], 0, 20) ?>...
                            </td>
                            <td class="hash-col" title="<?= htmlspecialchars($bloque['hash']) ?>">
                                 <?= substr($bloque['hash'], 0, 20) ?>...
                            </td>

                        </tr>
                    <?php endforeach; ?>
                <?php else: ?>
                    <tr>
                        <td colspan="6" class="text-center">No hay registros disponibles</td>
                    </tr>
                <?php endif; ?>
            </tbody>
        </table>
    </div>
</div>
