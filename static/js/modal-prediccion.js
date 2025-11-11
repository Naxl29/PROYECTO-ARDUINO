// Script para el modal de predicción ML
document.addEventListener('DOMContentLoaded', function() {
    const prediccionModal = document.getElementById('prediccionModal');
    const loadingDiv = document.getElementById('loadingDiv');
    const resultadoDiv = document.getElementById('resultadoDiv');
    const errorDiv = document.getElementById('errorDiv');
    const prediccionAmount = document.getElementById('prediccionAmount');

    prediccionModal.addEventListener('show.bs.modal', function () {
        // Resetear estado del modal
        loadingDiv.style.display = 'block';
        resultadoDiv.style.display = 'none';
        errorDiv.style.display = 'none';

        // Hacer la petición AJAX para obtener la predicción
        fetch('/ml/prediccion_mensual')
            .then(response => response.json())
            .then(data => {
                loadingDiv.style.display = 'none';
                
                if (data.exitoso) {
                    // Mostrar la predicción
                    prediccionAmount.textContent = '$' + data.prediccion_mensual.toLocaleString('es-CO');
                    resultadoDiv.style.display = 'block';
                } else {
                    // Mostrar error
                    errorDiv.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                loadingDiv.style.display = 'none';
                errorDiv.style.display = 'block';
            });
    });
});
