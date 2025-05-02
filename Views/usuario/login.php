<?php
require_once("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
require_once("c://laragon/www/PROYECTO-ARDUINO/Controllers/UsuarioController.php");
?>
    <link rel="stylesheet" href="/PROYECTO-ARDUINO/css/Registro.css">

    <link rel="stylesheet" href="css/Registro.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.5/dist/sweetalert2.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.5/dist/sweetalert2.all.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.5/dist/sweetalert2.min.css">
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.10.5/dist/sweetalert2.all.min.js"></script>

    <div class="login-box">
        <p>Iniciar sesión</p>
        <form method="post">
            <div class="user-box">
                <input type="text" id="usuario" name="usuario" autocomplete="off" required>
                <label>Usuario</label>
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
        </form>
        <p>¿No tienes una cuenta?<a href="/PROYECTO-ARDUINO/Views/usuario/create.php" class="a2"> Registrate!</a></p>
    </div>

    <script>
        <?php
        session_start(); // Asegúrate de iniciar la sesión en la vista

        if (isset($_SESSION['login_error'])) {
            $error = $_SESSION['login_error'];
            echo "Swal.fire({
                icon: 'error',
                title: '¡Error al iniciar sesión!',
                text: '" . $error . "',
            });";
            unset($_SESSION['login_error']); // Limpia el error dae la sesión
        }

        if ($_SERVER["REQUEST_METHOD"] == "POST" && !isset($_SESSION['login_error'])) {
            $usuarioController = new UsuarioController();
            $usuario = $_POST['usuario'];
            $contrasena = $_POST['contrasena'];

            $usuarioController->login($usuario, $contrasena);
            // La redirección se maneja en el controlador, así que no necesitamos más lógica aquí para el éxito.
        }
        ?>
    </script>
</body>
</html>