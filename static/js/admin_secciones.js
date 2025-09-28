// Inicialización del modal de edición de secciones
// Carga los datos (id, nombre, roles) en el formulario cuando se abre el modal

document.addEventListener('DOMContentLoaded', function(){
  const modalEditar = document.getElementById('editSectionModal');
  if (!modalEditar) return;

  modalEditar.addEventListener('show.bs.modal', function (evento) {
    const boton = evento.relatedTarget;
    try {
      const datos = JSON.parse(boton.getAttribute('data-section'));
      document.getElementById('edit-section-id').value = datos.id;
      document.getElementById('edit-section-nombre').value = datos.nombre;
      // Limpiar checks
      document.querySelectorAll('#editSectionModal input[type="checkbox"]').forEach(function(ch){ ch.checked = false; });
      (datos.roles || []).forEach(function(rol){
        const el = document.getElementById('edit-role-' + rol);
        if (el) el.checked = true;
      });
    } catch (e) {
      console.error('Error al cargar datos de sección:', e);
    }
  });
});
