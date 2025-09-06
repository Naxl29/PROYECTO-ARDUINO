// JavaScript para confirmación de cierre de sesión
document.addEventListener('DOMContentLoaded', function() {
    // Buscar todos los enlaces de logout
    const logoutLinks = document.querySelectorAll('a[href*="logout"]');
    
    logoutLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Prevenir la navegación inmediata
            
            // Mostrar confirmación con SweetAlert2 si está disponible, sino usar confirm nativo
            if (typeof Swal !== 'undefined') {
                // Usar SweetAlert2 para una mejor experiencia
                Swal.fire({
                    title: '¿Cerrar Sesión?',
                    text: '¿Estás seguro de que quieres cerrar tu sesión?',
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonColor: '#dc3545',
                    cancelButtonColor: '#6c757d',
                    confirmButtonText: 'Sí, cerrar sesión',
                    cancelButtonText: 'Cancelar',
                    reverseButtons: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Si confirma, redirigir al logout
                        window.location.href = link.href;
                    }
                });
            } else {
                // Fallback a confirm nativo si no hay SweetAlert2
                const confirmed = confirm('¿Estás seguro de que quieres cerrar tu sesión?');
                if (confirmed) {
                    window.location.href = link.href;
                }
            }
        });
    });
});