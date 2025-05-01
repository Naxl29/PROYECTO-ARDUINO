<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
?>

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
    </form>

    <p>¿Ya tienes una cuenta? <a href="inicio_sesion.html" class="a2">Inicia sesión</a></p>
</div>

<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/footer.php");
?>
