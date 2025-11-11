// Script para el menú hamburguesa móvil
(function() {
    'use strict';
    
    const mobileNavToggle = document.getElementById('mobileNavToggle');
    const mobileNavClose = document.getElementById('mobileNavClose');
    const mobileNav = document.getElementById('mobileNav');
    const mobileNavOverlay = document.getElementById('mobileNavOverlay');
    
    function openMobileNav() {
        if (mobileNav) {
            mobileNav.classList.add('active');
        }
        if (mobileNavOverlay) {
            mobileNavOverlay.style.display = 'block';
            mobileNavOverlay.classList.add('show');
        }
        document.body.classList.add('mobile-nav-open');
        
        // Accessibility
        if (mobileNavToggle) {
            mobileNavToggle.setAttribute('aria-expanded', 'true');
        }
    }
    
    function closeMobileNav() {
        if (mobileNav) {
            mobileNav.classList.remove('active');
        }
        if (mobileNavOverlay) {
            mobileNavOverlay.style.display = 'none';
            mobileNavOverlay.classList.remove('show');
        }
        document.body.classList.remove('mobile-nav-open');
        
        // Accessibility
        if (mobileNavToggle) {
            mobileNavToggle.setAttribute('aria-expanded', 'false');
        }
    }
    
    // Event listeners
    if (mobileNavToggle) {
        mobileNavToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            openMobileNav();
        });
    }
    
    if (mobileNavClose) {
        mobileNavClose.addEventListener('click', function(e) {
            e.stopPropagation();
            closeMobileNav();
        });
    }
    
    if (mobileNavOverlay) {
        mobileNavOverlay.addEventListener('click', closeMobileNav);
    }
    
    // Cerrar al hacer clic fuera del menú (mejorado)
    document.addEventListener('click', function(e) {
        if (mobileNav && mobileNav.classList.contains('active')) {
            // Si el clic no es dentro del menú ni del botón toggle
            if (!mobileNav.contains(e.target) && !mobileNavToggle.contains(e.target)) {
                closeMobileNav();
            }
        }
    });
    
    // Prevenir que clics dentro del menú lo cierren
    if (mobileNav) {
        mobileNav.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // Cerrar menú al hacer clic en un enlace
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', closeMobileNav);
    });
    
    // Cerrar menú con Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileNav && mobileNav.classList.contains('active')) {
            closeMobileNav();
        }
    });
    
    // Prevenir scroll en background cuando el menú está abierto
    let lastScrollY = 0;
    const preventScroll = (e) => {
        if (mobileNav && mobileNav.classList.contains('active')) {
            e.preventDefault();
        }
    };
    
    document.addEventListener('touchmove', preventScroll, { passive: false });
})();