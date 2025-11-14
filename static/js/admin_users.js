document.addEventListener('DOMContentLoaded', function () {
    const editUserModal = document.getElementById('editUserModal');
    const editForm = document.getElementById('edit-user-form');
    const usernameInput = document.getElementById('editar-usuario');
    const passwordInput = document.getElementById('editar-contrasena');
    const roleSelect = document.getElementById('editar-rol');

    if (editUserModal && editForm && usernameInput && passwordInput && roleSelect) {
        editUserModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            if (!button) {
                return;
            }
            const payload = button.getAttribute('data-user');
            if (!payload) {
                return;
            }
            try {
                const data = JSON.parse(payload);
                if (!data || typeof data !== 'object') {
                    return;
                }
                if (typeof data.usuario === 'string') {
                    usernameInput.value = data.usuario;
                }
                passwordInput.value = '';
                const targetRole = typeof data.rol === 'string' ? data.rol : '';
                if (targetRole && Array.from(roleSelect.options).some(function (option) { return option.value === targetRole; })) {
                    roleSelect.value = data.rol;
                } else {
                    roleSelect.value = '';
                }
                const updateUrl = button.getAttribute('data-update-url');
                if (updateUrl) {
                    editForm.setAttribute('action', updateUrl);
                }
            } catch (error) {
                console.error('No se pudo parsear la información del usuario', error);
            }
        });
    }

    const deleteButtons = document.querySelectorAll('.delete-user-btn');
    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const form = button.closest('form');
            if (!form) {
                return;
            }
            const username = form.getAttribute('data-username') || 'este usuario';
            Swal.fire({
                title: '¿Eliminar usuario?',
                text: `Se eliminará definitivamente ${username}.`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar',
                reverseButtons: true,
            }).then(function (result) {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    });
});

