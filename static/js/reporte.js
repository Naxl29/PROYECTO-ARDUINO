// Script para funcionalidades del reporte
document.addEventListener('DOMContentLoaded', function() {
    // Formatear precios en el reporte
    formatearPrecios();
});

/**
 * Formatea todos los precios en el reporte usando el mismo formato del modal ML
 */
function formatearPrecios() {
    const preciosFormateados = document.querySelectorAll('.precio-formateado');
    
    preciosFormateados.forEach(function(celda) {
        const precio = parseFloat(celda.dataset.precio);
        if (!isNaN(precio)) {
            // Usar el mismo formato que en el modal ML
            celda.textContent = '$' + precio.toLocaleString('es-CO', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }) + ' COP';
        }
    });
}