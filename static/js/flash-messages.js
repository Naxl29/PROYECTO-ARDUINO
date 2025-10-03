// JavaScript compartido para mostrar mensajes Flash con SweetAlert2
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar mensajes flash con SweetAlert2
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(alert) {
        const isSuccess = alert.classList.contains('alert-success');
        const isDanger = alert.classList.contains('alert-danger');
        const isWarning = alert.classList.contains('alert-warning');
        
        let icon = 'info';
        let title = 'Información';
        
        if (isSuccess) {
            icon = 'success';
            title = 'Éxito';
        } else if (isDanger) {
            icon = 'error';
            title = 'Error';
        } else if (isWarning) {
            icon = 'warning';
            title = 'Advertencia';
        }
        
        const messageText = alert.textContent.trim();
        
        // Solo mostrar SweetAlert si el mensaje es sobre eliminaciones o acciones importantes
        if (messageText.includes('eliminad') || messageText.includes('actualizada') || messageText.includes('creada')) {
            // Ocultar el alert original
            alert.style.display = 'none';
            
            // Mostrar SweetAlert2
            Swal.fire({
                title: title,
                text: messageText,
                icon: icon,
                timer: 3000,
                timerProgressBar: true,
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                backdrop: false,
                customClass: {
                    popup: 'swal-dark-popup'
                }
            });
        }
    });
});