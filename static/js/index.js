// Scripts específicos para la página de inicio
(function() {
    'use strict';
    
    // Optimización para dispositivos móvil - Progressive Web App
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('Service Worker registrado exitosamente:', registration.scope);
            })
            .catch(function(error) {
                console.log('Service Worker registration failed:', error);
            });
    }
    
    // Prevenir zoom accidental en iOS durante gestos
    document.addEventListener('gesturestart', function (e) {
        e.preventDefault();
    });
    
    // Prevenir doble tap zoom en iOS
    let lastTouchEnd = 0;
    document.addEventListener('touchend', function (event) {
        const now = (new Date()).getTime();
        if (now - lastTouchEnd <= 300) {
            event.preventDefault();
        }
        lastTouchEnd = now;
    }, false);
    
    // Mejorar la experiencia de carga
    window.addEventListener('load', function() {
        // Ocultar splash screen si existe
        const splashScreen = document.querySelector('.splash-screen');
        if (splashScreen) {
            splashScreen.style.opacity = '0';
            setTimeout(() => {
                splashScreen.style.display = 'none';
            }, 300);
        }
        
        // Aplicar animaciones de entrada
        const contentBox = document.querySelector('.content-box');
        if (contentBox) {
            contentBox.classList.add('loaded');
        }
    });
    
    // Optimización de rendimiento para móviles
    if (window.innerWidth <= 768) {
        // Reducir animaciones en dispositivos móviles
        document.body.classList.add('mobile-optimized');
        
        // Lazy loading para imágenes en móvil
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
})();