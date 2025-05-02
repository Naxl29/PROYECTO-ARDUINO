<?php
//Vista que contiene el formulario de para crear un nuevo
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
?>

 <link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">
 <link rel="stylesheet" href="css/Registro.css">
<div class="login-box">
    <div class="user-box">
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
            <button type="submit" class="button">
                <div class="blob1"></div>
                <div class="blob2"></div>
                <div class="inner">Registrar</div>
            </button>
        </form>
        <p>Ya tienes una cuenta?<a href="inicio_sesion.html" class="a2">Inicia sesion</a></p>
    </div>
<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/footer.php");
?>
