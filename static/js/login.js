// Validación del formulario de login
document.getElementById('campos').addEventListener('submit', function (e) {
    const usuario = document.getElementById('usuario').value.trim();
    const contrasena = document.getElementById('contrasena').value.trim();

    if (usuario === '' || contrasena === '') {
        e.preventDefault(); 
        Swal.fire({
            icon: 'warning',
            title: 'Campos vacíos',
            text: 'Por favor, completa todos los campos.',
            background: '#2D3A5A',
            color: '#fff',
            confirmButtonColor: '#6C63FF'
        }); 
    }
});

// Función para mostrar mensaje de error desde el servidor
function showErrorMessage(errorMessage) {
    Swal.fire({
        icon: 'error',
        title: 'Error al iniciar sesión',
        text: errorMessage,
        background: '#2D3A5A',
        color: '#fff',
        confirmButtonColor: '#6C63FF'
    });
}
