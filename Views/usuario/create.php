<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
?>
<link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">


<div class="login-box">
    <div class="user-box">
       <p>Registrar</p>

    <form action="store.php" method="POST" autocomplete="off">
             <input type="text" id="usuario" name="usuario" required>
            <label for="usuario">Usuario</label>
        </div>
        <div class="user-box">
            <input type="password" id="contrasena" name="contrasena" required>
            <label for="contrasena">Contraseña</label>
        </div>

    
        <button type="submit" class="custom-button">
            Iniciar
        </button>
        <a href="/PROYECTO-ARDUINO/index.php" class="custom-cancel">Cancelar</a>
    </form>
<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/footer.php");
?>
