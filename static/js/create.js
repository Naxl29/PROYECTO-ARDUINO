//Esta es una validación al crear usuario, en la cual se verifica que todos los campos estén llenos y no se cree un usuario ya existente
document.getElementById('registroForm').addEventListener('submit', function (e) {
    e.preventDefault(); // 🚀 Evita el envío doble

    const usuario = document.getElementById('usuario').value.trim();
    const contrasena = document.getElementById('contrasena').value.trim();

    if (usuario === '' || contrasena === '') {
        Swal.fire({
            icon: 'warning',
            title: 'Campos vacíos',
            text: 'Por favor, completa todos los campos.',
            background: '#2D3A5A',
            color: '#fff',
            confirmButtonColor: '#8B5CF6'
        });
        return;
    }

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
                confirmButtonColor: '#8B5CF6'
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
                confirmButtonColor: '#8B5CF6'
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
            confirmButtonColor: '#8B5CF6'
        });
    });
});