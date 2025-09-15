document.addEventListener("DOMContentLoaded", () => {
    // Cargar el estado actual de los LEDs al iniciar la página
    loadLEDStates();

    document.querySelectorAll(".estado_led").forEach((checkbox) => {
        checkbox.addEventListener("change", function () {
            const estado = this.checked ? '1' : '0';
            const led_id = this.getAttribute("data-led");

            // Si es el botón "ALL", manejar todos los LEDs
            if (led_id === "ALL") {
                handleAllLEDs(estado);
                return;
            }

            // Manejar LED individual
            handleSingleLED(led_id, estado);
        });
    });

    function loadLEDStates() {
        // Crear FormData para obtener todos los estados
        const formData = new FormData();
        formData.append("action", "get_all_states");

        fetch('/led/get_estados', {
            method: "GET"
        })
        .then(r => r.json())
        .then(data => {
            console.log("Estados cargados:", data);
            // Aplicar los estados a los checkboxes
            if (data.estados) {
                Object.keys(data.estados).forEach(led_id => {
                    const checkbox = document.querySelector(`.estado_led[data-led="${led_id}"]`);
                    if (checkbox) {
                        checkbox.checked = data.estados[led_id] === '1' || data.estados[led_id] === 1;
                    }
                });
                
                // Verificar si todos los LEDs están encendidos para activar el botón "ALL"
                updateAllButton();
            }
        })
        .catch(err => {
            console.error("Error al cargar estados:", err);
        });
    }

    function updateAllButton() {
        const individualLEDs = document.querySelectorAll('.estado_led[data-led]:not([data-led="ALL"])');
        const allButton = document.querySelector('.estado_led[data-led="ALL"]');
        
        if (allButton) {
            const allChecked = Array.from(individualLEDs).every(led => led.checked);
            allButton.checked = allChecked;
        }
    }

    function handleAllLEDs(estado) {
        // Obtener todos los checkboxes excepto el "ALL"
        const individualLEDs = document.querySelectorAll('.estado_led[data-led]:not([data-led="ALL"])');
        
        // Activar/desactivar todos los LEDs individuales simultáneamente
        individualLEDs.forEach((ledCheckbox) => {
            ledCheckbox.checked = (estado === '1');
            // Disparar el evento change para cada LED individual
            const led_id = ledCheckbox.getAttribute("data-led");
            handleSingleLED(led_id, estado);
        });
    }

    function handleSingleLED(led_id, estado) {
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
    }
});
