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

// SOLO chispas al hacer clic - SIN animaciones automáticas
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