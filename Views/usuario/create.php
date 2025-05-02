<?php
//Vista que contiene el formulario de para crear un nuvoe
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
?>
<<<<<<< HEAD
 <link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">
=======
 <link rel="stylesheet" href="css/Registro.css">

<<<<<<< HEAD

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

        <button type="submit" class="button">
            <div class="blob1"></div>
            <div class="blob2"></div>
            <div class="inner">Iniciar</div>
        </button>
        <button type="submit" class="button">
            <div class="blob1"></div>
            <div class="blob2"></div>
            <div class="inner">Cancelarr</div>
        </button>
            
        <a href="/PROYECTO-ARDUINO/index.php" class="custom-cancel">Cancelar</a>
    </form>
=======
>>>>>>> 4387e6d726e09860c2fc4635e56c7137fb0b0a55
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
                <div class="inner">Registrar</div>
            </button>
        </form>
        <p>Ya tienes una cuenta?<a href="inicio_sesion.html" class="a2">Inicia sesion</a></p>
    </div>
<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/footer.php");
?>
