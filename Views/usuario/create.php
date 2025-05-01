<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
    ?>

    <form action="/PROYECTO-ARDUINO/index.php?accion=login" method="POST" autocomplete="off">

        <div class="mb-3">
            <label for="usuario" class="form-label">Ingresar usuario:</label>
            <input type="text" class="form-control" id="usuario" name="usuario" required>
        </div>

        <div class="mb-3">
            <label for="contrasena" class="form-label">Ingresar contraseña:</label>
            <input type="password" class="form-control" id="contrasena" name="contrasena" required>
        </div>

        <button type="submit" class="btn btn-success">Iniciar Sesión</button>
        <a class="btn btn-danger" href="/PROYECTO-ARDUINO/index.php">Cancelar</a>

        <?php if (isset($_GET['error'])): ?>
            <div class="alert alert-danger mt-3" role="alert">
                Usuario o contraseña incorrectos.
            </div>
        <?php endif; ?>
    </form>

<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/footer.php");
?>