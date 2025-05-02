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

    
        
        <button type="submit" class="button">
            <div class="blob1"></div>
            <div class="blob2"></div>
            <div class="inner">Iniciar</div>
        </button>
        <button type="submit" class="button">
            <div class="blob1"></div>
            <div class="blob2"></div>
            <div class="inner">Cancelar</div>
        </button>
    </form>
<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/footer.php");
?>
