<?php
//Vista que contiene el formulario de para crear un nuevo usuario
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
?>
 <link rel="stylesheet" href="css/Registro.css">

    <div class="login-box">
        <p>Registrate</p>
        <form action="boton.html" method="post">
            <div class="user-box">
                <input required="" name="" type="text">
                <label>Usuario</label>
            </div>
            <div class="user-box">
                <input required="" name="" type="password">
                <label>Contraseña</label>
            </div>
            <button type="submit" class="button">
                <div class="blob1"></div>
                <div class="blob2"></div>
                <div class="inner">Registrar</div>
            </button>
        </form>
        <p>Ya tienes una cuenta?<a href="inicio_sesion.html" class="a2">   Inicia sesion</a></p>
    </div>
<?php
    require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/footer.php");
?>
