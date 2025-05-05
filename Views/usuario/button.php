<?php
//Acá se muestra el apartado que contiene el botón que encenderá y apagará el bombillo
    session_start(); // Añadir inicio de sesión
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Views/head/head.php");
    require_once ("c://laragon/www/PROYECTO-ARDUINO/Controllers/BloqueController.php");

    // Verificar si el usuario está logueado
    if (!isset($_SESSION['id_usuario'])) {
        header("Location: /PROYECTO-ARDUINO/Views/usuario/login.php");
        exit;
    }
?>
<link rel="stylesheet" href="/PROYECTO-ARDUINO/css/styles.css">

<body>
    <div class="mb-3">
            <a href="/PROYECTO-ARDUINO/index.php" class="boton-back" title="Volver al inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house-door-fill" viewBox="0 0 16 16">
                    <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5"/>
                </svg>
            </a>
    </div>
    <div class="bg-gradient">
        <div class="botones">
            <a href="/PROYECTO-ARDUINO/Views/usuario/see.php" class="boton_2" title="Lista">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="bi bi-person-lines-fill" viewBox="0 0 16 16">
                    <path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m-5 6s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zM11 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5m.5 2.5a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1zm2 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1z"/>
                </svg>
            </a>
        </div>
    </div>
    <div class="switch-container">
        <label class="switch">
            <input type="checkbox" id="estado_boton">
            <span class="slider">
                <span class="star star_1"></span>
                <span class="star star_2"></span>
                <span class="star star_3"></span>
                <span class="cloud"></span>
                <svg viewBox="0 0 16 16" class="cloud_1 cloud">
                    <path
                        transform="matrix(.77976 0 0 .78395-299.99-418.63)"
                        fill="#fff"
                        d="m391.84 540.91c-.421-.329-.949-.524-1.523-.524-1.351 0-2.451 1.084-2.485 2.435-1.395.526-2.388 1.88-2.388 3.466 0 1.874 1.385 3.423 3.182 3.667v.034h12.73v-.006c1.775-.104 3.182-1.584 3.182-3.395 0-1.747-1.309-3.186-2.994-3.379.007-.106.011-.214.011-.322 0-2.707-2.271-4.901-5.072-4.901-2.073 0-3.856 1.202-4.643 2.925"
                    ></path>
                    </svg>
            </span>
        </label>
    </div>
</body>
<script>
    const id_usuario = <?php echo json_encode($_SESSION['id_usuario']); ?>;
</script>

<script>
    document.getElementById("estado_boton").addEventListener("change", function () {
        const estado = this.checked ? '1' : '0';
        console.log("Estado del botón:", estado); 

        fetch("/PROYECTO-ARDUINO/Views/usuario/estado_button.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `estado=${estado}&id_usuario=${id_usuario}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor: ' + response.status);
            }
            return response.text();
        })
        .then(data => {
            console.log("Respuesta del servidor:", data);
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
</script>