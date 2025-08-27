document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".estado_led").forEach((checkbox) => {
        checkbox.addEventListener("change", function () {
            const estado = this.checked ? '1' : '0';
            const led_id = this.getAttribute("data-led");

            const formDataLed = new FormData();
            formDataLed.append("estado", estado);
            formDataLed.append("led_id", led_id);

            fetch(urlEstadoLed, {   // se usa la variable global
                method: "POST",
                body: formDataLed
            })
            .then(r => r.json())
            .then(data => console.log(`LED ${led_id} →`, data))
            .catch(err => console.error("Error LED:", err));

            const formDataGuardar = new FormData();
            formDataGuardar.append("estado", estado);
            formDataGuardar.append("led_id", led_id);

            fetch(urlGuardarEstado, {   // acá tambien se usa la variable global
                method: "POST",
                body: formDataGuardar
            })
            .then(r => r.json())
            .then(data => console.log("Estado guardado:", data))
            .catch(err => console.error("Error al guardar:", err));
        });
    });
});
