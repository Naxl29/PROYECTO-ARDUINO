<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
?>

    <form action="store.php" method="POST" autocomplete="off">

    <div class="mb-3">
        <label for="usuario" class="form-label">Ingresar usuario:</label>
        <input type="text" class="form-control" id="usuario" name="usuario" required ="">
    </div>
    <div class="mb-3">
        <label for="contrasena" class="form-label">Ingresar contraseña:</label>
        <input type="text" class="form-control" id="contrasena" name="contrasena" required ="">
    </div>

    <button type="submit" class="btn btn-primary">Crear</button>
    <a class="btn btn-danger" href="index.php">Cancelar</a>
    </form>

<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/footer.php");
?>