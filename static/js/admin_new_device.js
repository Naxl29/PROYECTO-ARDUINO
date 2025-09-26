// JS específico para la página de Agregar dispositivo (admin_new_device)

document.addEventListener('DOMContentLoaded', function(){
	// Pintar los puntos de color desde el atributo data-color (evitar inline style en Jinja)
	document.querySelectorAll('.device-color-dot').forEach(function(el){
		const c = el.getAttribute('data-color') || '#ffffff';
		el.style.backgroundColor = c;
	});

	// Paginación simple del listado de dispositivos (cliente)
	const list = document.getElementById('device-list');
	if (list) {
		const items = Array.from(list.children);
		const pageSize = 10; // elementos por página
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
});
