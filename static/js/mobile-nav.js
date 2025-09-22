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
        }
        document.body.style.overflow = 'hidden';
        
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
        }
        document.body.style.overflow = '';
        
        // Accessibility
        if (mobileNavToggle) {
            mobileNavToggle.setAttribute('aria-expanded', 'false');
        }
    }
    
    // Event listeners
    if (mobileNavToggle) {
        mobileNavToggle.addEventListener('click', openMobileNav);
    }
    
    if (mobileNavClose) {
        mobileNavClose.addEventListener('click', closeMobileNav);
    }
    
    if (mobileNavOverlay) {
        mobileNavOverlay.addEventListener('click', closeMobileNav);
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