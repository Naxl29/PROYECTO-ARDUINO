document.querySelectorAll(".estado_led").forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
        const estado = this.checked ? '1' : '0';
        const led_id = this.getAttribute("data-led");

        const formDataLed = new FormData();
        formDataLed.append("estado", estado);
        formDataLed.append("led_id", led_id);

        fetch("{{ url_for('estado_led') }}", {
            method: "POST",
            body: formDataLed
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al controlar LED: " + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log(`LED ${led_id} →`, data);
        })
        .catch(error => {
            console.error("Error:", error);
        });

        const formDataGuardar = new FormData();
        formDataGuardar.append("estado", estado);
        formDataGuardar.append("led_id", led_id);

        fetch("/usuario/save_estado", {
            method: "POST",
            body: formDataGuardar
        })
        .then(response => response.json())
        .then(data => {
            console.log("Estado guardado:", data);
        })
        .catch(error => {
            console.error("Error al guardar estado:", error);
        });
    });
});
