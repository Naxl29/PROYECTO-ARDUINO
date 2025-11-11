// Script para funcionalidades del reporte
document.addEventListener('DOMContentLoaded', function() {
    // Formatear precios en el reporte
    formatearPrecios();
    // Iniciar paginación si aplica
    initReportePagination();
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

/**
 * Paginación del listado del reporte (tabla)
 */
function initReportePagination() {
    const table = document.getElementById('tabla-reporte');
    if (!table) return;
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    // No paginar si solo hay fila "no hay registros"
    if (rows.length === 0 || (rows.length === 1 && rows[0].querySelector('.text-center'))) return;

    const pageSize = 10;
    let current = 1;
    const totalPages = Math.max(1, Math.ceil(rows.length / pageSize));
    const prev = document.getElementById('rep-prev');
    const next = document.getElementById('rep-next');
    const info = document.getElementById('rep-page-info');

    function render(page){
        const start = (page - 1) * pageSize;
        const end = start + pageSize;
        rows.forEach((tr, idx) => {
            tr.style.display = (idx >= start && idx < end) ? '' : 'none';
        });
        if (info) info.textContent = `Página ${page}/${totalPages}`;
        if (prev) prev.disabled = page <= 1;
        if (next) next.disabled = page >= totalPages;
    }

    prev?.addEventListener('click', () => { if (current > 1) { current--; render(current); } });
    next?.addEventListener('click', () => { if (current < totalPages) { current++; render(current); } });

    render(current);
}