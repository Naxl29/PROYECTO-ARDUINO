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

  // SweetAlert2 para eliminar secciones
  document.querySelectorAll('.delete-section-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const form = this.closest('.delete-section-form');
      const sectionName = form.dataset.sectionName;
      const sectionId = form.dataset.sectionId;
      
      Swal.fire({
        title: '¿Eliminar sección?',
        html: `Se eliminará permanentemente la sección:<br><strong>${sectionName}</strong><br><br><span style="color: #ffc107;">⚠️ Se quitarán todas las asignaciones de dispositivos</span><br><span style="color: #dc3545;">Esta acción no se puede deshacer</span>`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, eliminar sección',
        cancelButtonText: 'Cancelar',
        backdrop: 'rgba(0,0,0,0.8)',
        customClass: {
          popup: 'swal-dark-popup'
        }
      }).then((result) => {
        if (result.isConfirmed) {
          form.submit();
        }
      });
    });
  });

  // Paginación simple del listado de secciones (cliente)
  const sectionsList = document.getElementById('sections-list');
  if (sectionsList) {
    const items = Array.from(sectionsList.children);
    const pageSize = 7; // elementos por página
    let current = 1;
    const totalPages = Math.max(1, Math.ceil(items.length / pageSize));
    const prevBtn = document.getElementById('sections-prev-page');
    const nextBtn = document.getElementById('sections-next-page');
    const pageInfo = document.getElementById('sections-page-info');

    function renderPage(page) {
      const start = (page - 1) * pageSize;
      const end = start + pageSize;
      items.forEach((li, idx) => {
        const visible = (idx >= start && idx < end);
        if (visible) {
          li.classList.remove('d-none');
        } else {
          // Usar d-none de Bootstrap porque d-flex usa display: flex !important
          li.classList.add('d-none');
        }
      });
      if (pageInfo) pageInfo.textContent = `Página ${page}/${totalPages}`;
      if (prevBtn) prevBtn.disabled = page <= 1;
      if (nextBtn) nextBtn.disabled = page >= totalPages;
    }

    prevBtn?.addEventListener('click', () => { 
      if (current > 1) { 
        current--; 
        renderPage(current); 
      } 
    });
    
    nextBtn?.addEventListener('click', () => { 
      if (current < totalPages) { 
        current++; 
        renderPage(current); 
      } 
    });

    renderPage(current);
  }
});
