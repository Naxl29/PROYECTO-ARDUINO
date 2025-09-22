//Esta es una validación al crear usuario, en la cual se verifica que todos los campos estén llenos y no se cree un usuario ya existente
document.getElementById('registroForm').addEventListener('submit', function (e) {
    const usuario = document.getElementById('usuario').value.trim();
    const contrasena = document.getElementById('contrasena').value.trim();

    if (usuario === '' || contrasena === '') {
        e.preventDefault(); // Prevenir envío si campos vacíos
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

    // Solo hacer fetch si todos los campos están llenos
    e.preventDefault();
    
    fetch(this.action, {
        method: this.method,
        body: new FormData(this)
    })
    .then(response => response.json())
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
                }
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error al crear usuario',
                text: 'Usuario ya existente.',
                background: '#2D3A5A',
                color: '#fff',
                confirmButtonColor: '#6C63FF'
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error de conexión',
            text: 'No se pudo conectar con el servidor.',
            background: '#2D3A5A',
            color: '#fff',
            confirmButtonColor: '#6C63FF'
        });
    });
});

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