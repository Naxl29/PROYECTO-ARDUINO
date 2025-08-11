function createFirework() {
    const numSparks = 25; 
    const colors = ['#00ffff', '#fff', '#4dd0e1', '#80deea', '#b2ebf2', '#e1f5fe'];

    const x = Math.random() * window.innerWidth;
    const y = Math.random() * window.innerHeight;

    for (let i = 0; i < numSparks; i++) {
        const spark = document.createElement('div');
        spark.className = 'spark';

        // Colores más eléctricos
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        // Forma de chispa más realista
        const sparkLength = Math.random() * 20 + 10;
        const sparkWidth = Math.random() * 3 + 2;
        
        spark.style.width = sparkWidth + 'px';
        spark.style.height = sparkLength + 'px';
        spark.style.background = `linear-gradient(to bottom, ${color}, transparent)`;
        spark.style.borderRadius = '50px';
        
        // Efecto de brillo eléctrico
        spark.style.boxShadow = `
            0 0 ${Math.random() * 10 + 5}px ${color},
            0 0 ${Math.random() * 20 + 10}px ${color},
            0 0 ${Math.random() * 30 + 15}px ${color}
        `;

        // Movimiento más errático como chispas reales
        const angle = Math.random() * 2 * Math.PI;
        const distance = Math.random() * 200 + 30;
        const xMove = Math.cos(angle) * distance;
        const yMove = Math.sin(angle) * distance + Math.random() * 50; // Caída por gravedad
        
        // Rotación aleatoria para simular chispas volando
        const rotation = Math.random() * 720 - 360;
        
        spark.style.setProperty('--x', xMove + 'px');
        spark.style.setProperty('--y', yMove + 'px');
        spark.style.setProperty('--rotation', rotation + 'deg');

        spark.style.left = x + 'px';
        spark.style.top = y + 'px';
        
        // Animación de chispa
        spark.style.animation = `sparkFly ${Math.random() * 0.5 + 0.8}s ease-out forwards`;

        document.getElementById('glow-container').appendChild(spark);

        // Remover después de la animación
        setTimeout(() => {
            if (spark.parentNode) {
                spark.remove();
            }
        }, 1300);
        
        // Algunas chispas tienen micro-explosiones
        if (Math.random() < 0.3) {
            setTimeout(() => {
                createMicroSpark(
                    x + xMove * 0.7, 
                    y + yMove * 0.7
                );
            }, Math.random() * 600 + 200);
        }
    }
}

function createMicroSpark(x, y) {
    for (let i = 0; i < 5; i++) {
        const microSpark = document.createElement('div');
        microSpark.className = 'spark';
        
        microSpark.style.width = '1px';
        microSpark.style.height = '8px';
        microSpark.style.background = 'linear-gradient(to bottom, #fff, #00ffff, transparent)';
        microSpark.style.borderRadius = '50px';
        microSpark.style.boxShadow = '0 0 5px #00ffff, 0 0 10px #00ffff';
        
        const angle = Math.random() * 2 * Math.PI;
        const distance = Math.random() * 30 + 10;
        const xMove = Math.cos(angle) * distance;
        const yMove = Math.sin(angle) * distance;
        
        microSpark.style.setProperty('--x', xMove + 'px');
        microSpark.style.setProperty('--y', yMove + 'px');
        microSpark.style.setProperty('--rotation', Math.random() * 360 + 'deg');
        
        microSpark.style.left = x + 'px';
        microSpark.style.top = y + 'px';
        microSpark.style.animation = 'sparkFly 0.6s ease-out forwards';
        
        document.getElementById('glow-container').appendChild(microSpark);
        
        setTimeout(() => {
            if (microSpark.parentNode) {
                microSpark.remove();
            }
        }, 600);
    }
}

// Lanzar chispas eléctricas cada segundo
setInterval(createFirework, 1000);

// Chispas al hacer clic
document.addEventListener('click', function(e) {
    const x = e.clientX;
    const y = e.clientY;
    
    // Crear chispas en el punto de clic
    for (let i = 0; i < 15; i++) {
        const spark = document.createElement('div');
        spark.className = 'spark';
        
        spark.style.width = Math.random() * 3 + 1 + 'px';
        spark.style.height = Math.random() * 15 + 8 + 'px';
        spark.style.background = 'linear-gradient(to bottom, #fff, #00ffff, transparent)';
        spark.style.borderRadius = '50px';
        spark.style.boxShadow = '0 0 8px #00ffff, 0 0 15px #00ffff';
        
        const angle = Math.random() * 2 * Math.PI;
        const distance = Math.random() * 100 + 20;
        const xMove = Math.cos(angle) * distance;
        const yMove = Math.sin(angle) * distance;
        
        spark.style.setProperty('--x', xMove + 'px');
        spark.style.setProperty('--y', yMove + 'px');
        spark.style.setProperty('--rotation', Math.random() * 360 + 'deg');
        
        spark.style.left = x + 'px';
        spark.style.top = y + 'px';
        spark.style.animation = 'sparkFly 1s ease-out forwards';
        
        document.getElementById('glow-container').appendChild(spark);
        
        setTimeout(() => {
            if (spark.parentNode) {
                spark.remove();
            }
        }, 1000);
    }
});