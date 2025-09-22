// Mobile helpers para mejorar la experiencia móvil
(function() {
    'use strict';
    
    // Detectar dispositivo móvil
    function isMobile() {
        return window.innerWidth <= 768 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    // Agregar clase mobile al body
    function addMobileClass() {
        if (isMobile()) {
            document.body.classList.add('is-mobile');
            document.body.classList.remove('is-desktop');
        } else {
            document.body.classList.add('is-desktop');
            document.body.classList.remove('is-mobile');
        }
    }
    
    // Prevenir zoom al hacer doble tap en iOS (mejorado)
    function preventDoubleZoom() {
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function (event) {
            const now = (new Date()).getTime();
            // Solo prevenir si es realmente un doble tap y no está en elementos scrolleables
            if (now - lastTouchEnd <= 300) {
                // No prevenir si el elemento padre es scrolleable
                const target = event.target;
                const scrollableParent = target.closest('[data-scrollable], .table-responsive, .content, .card-body, .overflow-auto, .overflow-scroll');
                
                if (!scrollableParent) {
                    event.preventDefault();
                }
            }
            lastTouchEnd = now;
        }, false);
    }
    
    // Mejorar la experiencia táctil
    function enhanceTouchExperience() {
        // Agregar feedback táctil a botones
        const buttons = document.querySelectorAll('button, .btn, input[type="submit"], input[type="button"]');
        buttons.forEach(button => {
            button.addEventListener('touchstart', function() {
                this.classList.add('touch-active');
            });
            
            button.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.classList.remove('touch-active');
                }, 150);
            });
        });
    }
    
    // Ajustar height de viewport en móviles (problema de la barra de navegación)
    function adjustViewportHeight() {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
        
        // Marcar elementos scrolleables
        const scrollableElements = document.querySelectorAll('.content, .card-body, .table-responsive');
        scrollableElements.forEach(el => {
            el.setAttribute('data-scrollable', 'true');
        });
    }
    
    // Mejorar scroll en dashboard
    function improveDashboardScroll() {
        const content = document.querySelector('.content');
        const dashboard = document.querySelector('[data-page="dashboard"], .dashboard');
        
        if (content && isMobile()) {
            // Asegurar que el contenido sea scrolleable
            content.style.overflowY = 'auto';
            content.style.webkitOverflowScrolling = 'touch';
            content.style.touchAction = 'pan-y';
            
            // Si es dashboard, agregar clase especial
            if (dashboard || window.location.pathname.includes('dashboard')) {
                content.setAttribute('data-page', 'dashboard');
                document.body.classList.add('dashboard-page');
            }
        }
    }
    
    // Ocultar sidebar en móvil al cargar
    function hideSidebarOnMobile() {
        if (isMobile()) {
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) {
                sidebar.style.display = 'none';
            }
        }
    }
    
    // Hacer tables responsive
    function makeTablesResponsive() {
        const tables = document.querySelectorAll('table');
        tables.forEach(table => {
            if (!table.closest('.table-responsive')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
        });
    }
    
    // Agregar clases helper para elementos comunes
    function addHelperClasses() {
        // Hacer forms más touch-friendly
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.classList.add('mobile-input');
        });
        
        // Agregar clases a botones para mejor UX móvil
        const buttons = document.querySelectorAll('.btn, button');
        buttons.forEach(button => {
            button.classList.add('mobile-btn');
        });
        
        // Hacer cards más touch-friendly
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.classList.add('mobile-card');
        });
    }
    
    // Inicializar cuando el DOM esté listo
    function init() {
        addMobileClass();
        
        if (isMobile()) {
            preventDoubleZoom();
            enhanceTouchExperience();
            hideSidebarOnMobile();
            improveDashboardScroll();
        }
        
        makeTablesResponsive();
        addHelperClasses();
        adjustViewportHeight();
    }
    
    // Event listeners
    window.addEventListener('resize', function() {
        addMobileClass();
        adjustViewportHeight();
    });
    
    window.addEventListener('orientationchange', function() {
        setTimeout(adjustViewportHeight, 100);
    });
    
    // Inicializar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();