// JavaScript para confirmación de cierre de sesión
document.addEventListener('DOMContentLoaded', function() {
    console.log('Logout script cargado'); // Debug
    
    // Buscar todos los enlaces de logout
    const logoutLinks = document.querySelectorAll('a[href*="logout"]');
    console.log('Enlaces de logout encontrados:', logoutLinks.length); // Debug
    
    logoutLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Prevenir la navegación inmediata
            console.log('Click en logout detectado'); // Debug
            
            // Mostrar confirmación con SweetAlert2 si está disponible
            if (typeof Swal !== 'undefined') {
                console.log('Usando SweetAlert2'); // Debug
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
                        window.location.href = link.href;
                    }
                });
            } else {
                console.log('Usando confirm nativo'); // Debug
                // Fallback a confirm nativo si no hay SweetAlert2
                const confirmed = confirm('¿Estás seguro de que quieres cerrar tu sesión?');
                if (confirmed) {
                    window.location.href = link.href;
                }
            }
        });
    });
});

