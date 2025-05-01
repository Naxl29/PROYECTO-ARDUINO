<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
    ?>

<<<<<<< HEAD
<link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">


<div class="login-box">
    <p>Registrar</p>

    <form action="store.php" method="POST" autocomplete="off">
        <div class="user-box">
            <input type="text" id="usuario" name="usuario" required>
            <label for="usuario">Usuario</label>
        </div>
        <div class="user-box">
            <input type="password" id="contrasena" name="contrasena" required>
            <label for="contrasena">Contraseña</label>
        </div>

    
        <button type="submit" class="custom-button">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            Iniciar
        </button>
        <a href="/PROYECTO-ARDUINO/index.php" class="custom-cancel">Cancelar</a>
=======
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
>>>>>>> 60dcb948ac558b11fdb3cfd64d42b91c4cabcc83
    </form>

    <p>¿Ya tienes una cuenta? <a href="inicio_sesion.html" class="a2">Inicia sesión</a></p>
</div>

<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/footer.php");
?>
