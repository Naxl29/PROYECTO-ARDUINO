// JS específico para la página de Agregar dispositivo (admin_new_device)

document.addEventListener('DOMContentLoaded', function(){
	// Pintar los puntos de color desde el atributo data-color (evitar inline style en Jinja)
	document.querySelectorAll('.device-color-dot').forEach(function(el){
		const c = el.getAttribute('data-color') || '#ffffff';
		el.style.backgroundColor = c;
	});

	// Modal para asignar/quitar sección - usar eventos nativos de Bootstrap
	const assignModal = document.getElementById('assignSectionModal');
	if (assignModal) {
		assignModal.addEventListener('show.bs.modal', function (event) {
			const button = event.relatedTarget; // Botón que activó el modal
			if (button) {
				const li = button.closest('.device-item');
				const channel = li ? (li.getAttribute('data-channel') || '') : '';
				const current = li ? (li.getAttribute('data-current-section') || '') : '';
				
				const inputChannel = document.getElementById('assign-channel');
				const selectSection = document.getElementById('assign-section');
				if (inputChannel) inputChannel.value = channel;
				if (selectSection) selectSection.value = current;
			}
		});
	}

	// Modal para editar dispositivo - usar eventos nativos de Bootstrap
	const editModal = document.getElementById('editDeviceModal');
	if (editModal) {
		editModal.addEventListener('show.bs.modal', function (event) {
			const button = event.relatedTarget; // Botón que activó el modal
			if (button && button.dataset.device) {
				const deviceData = JSON.parse(button.dataset.device || '{}');
				document.getElementById('edit-device-channel').value = deviceData.channel || '';
				document.getElementById('edit-device-nombre').value = deviceData.nombre || '';
				document.getElementById('edit-device-potencia').value = deviceData.potencia || 0;
				document.getElementById('edit-device-consumo').value = deviceData.consumo || 0;
				document.getElementById('edit-device-color').value = deviceData.color || '#ffffff';
			}
		});
	}

	// Paginación simple del listado de dispositivos (cliente)
	const list = document.getElementById('device-list');
	if (list) {
		const items = Array.from(list.children);
		const pageSize = 7; // elementos por página
		let current = 1;
		const totalPages = Math.max(1, Math.ceil(items.length / pageSize));
		const prevBtn = document.getElementById('prev-page');
		const nextBtn = document.getElementById('next-page');
		const pageInfo = document.getElementById('page-info');

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
			pageInfo.textContent = `Página ${page}/${totalPages}`;
			prevBtn.disabled = page <= 1;
			nextBtn.disabled = page >= totalPages;
		}

		prevBtn?.addEventListener('click', () => { if (current > 1) { current--; renderPage(current); } });
		nextBtn?.addEventListener('click', () => { if (current < totalPages) { current++; renderPage(current); } });

		renderPage(current);
	}

	// Asegurar que los modales se cierren correctamente
	document.querySelectorAll('.modal').forEach(function(modal) {
		modal.addEventListener('hidden.bs.modal', function () {
			// Limpiar backdrop si queda colgado
			const backdrop = document.querySelector('.modal-backdrop');
			if (backdrop) {
				backdrop.remove();
			}
			// Restaurar scroll del body
			document.body.classList.remove('modal-open');
			document.body.style.overflow = '';
			document.body.style.paddingRight = '';
		});
	});

	// SweetAlert2 para eliminar dispositivos
	document.querySelectorAll('.delete-device-btn').forEach(function(btn) {
		btn.addEventListener('click', function(e) {
			e.preventDefault();
			const form = this.closest('.delete-device-form');
			const deviceName = form.dataset.deviceName;
			const deviceChannel = form.dataset.deviceChannel;
			
			Swal.fire({
				title: '¿Eliminar dispositivo?',
				html: `Se eliminará permanentemente el dispositivo:<br><strong>${deviceName}</strong> (Canal ${deviceChannel})<br><br><span style="color: #dc3545;">Esta acción no se puede deshacer</span>`,
				icon: 'warning',
				showCancelButton: true,
				confirmButtonColor: '#dc3545',
				cancelButtonColor: '#6c757d',
				confirmButtonText: 'Sí, eliminar',
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
});
