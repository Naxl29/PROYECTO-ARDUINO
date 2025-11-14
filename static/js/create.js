//Esta es una validación al crear usuario, en la cual se verifica que todos los campos estén llenos y no se cree un usuario ya existente
let isSubmitting = false;

document.getElementById('registroForm').addEventListener('submit', function (e) {
    e.preventDefault();
    
    // Prevenir múltiples envíos
    if (isSubmitting) {
        return;
    }
    
    const usuario = document.getElementById('usuario').value.trim();
    const contrasena = document.getElementById('contrasena').value.trim();
    const submitButton = this.querySelector('button[type="submit"]');

    if (usuario === '' || contrasena === '') {
        Swal.fire({
            icon: 'warning',
            title: 'Campos vacíos',
            text: 'Por favor, completa todos los campos.',
            background: '#2D3A5A',
            color: '#fff',
            confirmButtonColor: '#6C63FF'
        });
        return;
    }

    // Deshabilitar botón y mostrar estado de carga
    isSubmitting = true;
    const originalButtonText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = 'PROCESANDO...';
    submitButton.style.opacity = '0.6';
    submitButton.style.cursor = 'not-allowed';
    
    fetch(this.action, {
        method: this.method,
        body: new FormData(this)
    })
    .then(response => {
        // Manejar diferentes códigos de estado HTTP
        if (!response.ok) {
            return response.json().then(data => {
                throw { status: response.status, data: data };
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            Swal.fire({
                title: '¡Usuario creado!',
                icon: 'success',
                confirmButtonText: 'Ver detalles',
                background: '#2D3A5A',
                color: '#fff',
                confirmButtonColor: '#6C63FF'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = `/usuario/show/${data.id}`;
                } else {
                    // Rehabilitar botón si el usuario no quiere ver detalles
                    resetButton(submitButton, originalButtonText);
                }
            });
        } else {
            throw { status: 400, data: data };
        }
    })
    .catch(error => {
        console.error('Error:', error);
        
        // Restaurar botón
        resetButton(submitButton, originalButtonText);
        
        // Mostrar mensaje de error apropiado
        let errorMessage = 'No se pudo crear el usuario.';
        if (error.data && error.data.message) {
            errorMessage = error.data.message;
        } else if (error.message) {
            errorMessage = error.message;
        }
        
        Swal.fire({
            icon: 'error',
            title: 'Error al crear usuario',
            text: errorMessage,
            background: '#2D3A5A',
            color: '#fff',
            confirmButtonColor: '#6C63FF'
        });
    });
});

// Función para restaurar el estado del botón
function resetButton(button, originalText) {
    isSubmitting = false;
    button.disabled = false;
    button.textContent = originalText;
    button.style.opacity = '1';
    button.style.cursor = 'pointer';
}

// Función para mostrar mensaje de error desde el servidor
function showErrorMessage(message) {
    Swal.fire({
        icon: 'error',
        title: 'Error de registro',
        text: message,
        background: '#2D3A5A',
        color: '#fff',
        confirmButtonColor: '#6C63FF'
    });
}

// Función para mostrar mensaje de éxito desde el servidor
function showSuccessMessage(message) {
    Swal.fire({
        icon: 'success',
        title: 'Registro exitoso',
        text: message,
        background: '#2D3A5A',
        color: '#fff',
        confirmButtonColor: '#6C63FF'
    });
}