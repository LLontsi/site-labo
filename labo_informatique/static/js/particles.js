document.addEventListener('DOMContentLoaded', function() {
    const headerParticles = document.querySelector('.header .particles-container');
    const footerParticles = document.querySelector('.footer .particles-container');
    
    // Fonction pour générer des particules
    function generateParticles(container, count) {
        if (!container) return;
        
        // Supprimer les particules existantes
        container.innerHTML = '';
        
        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            // Taille aléatoire
            const size = Math.random() * 4 + 2;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            // Position aléatoire
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.left = `${Math.random() * 100}%`;
            
            // Animation aléatoire
            const animationDuration = Math.random() * 15 + 10;
            particle.style.animation = `particleFloat ${animationDuration}s infinite ease-in-out`;
            
            // Délai d'animation aléatoire
            particle.style.animationDelay = `${Math.random() * 5}s`;
            
            // Opacité aléatoire
            particle.style.opacity = Math.random() * 0.5 + 0.1;
            
            container.appendChild(particle);
        }
    }
    
    // Générer des particules dans le header et le footer
    generateParticles(headerParticles, 30);
    generateParticles(footerParticles, 30);
    
    // Ajout d'interaction pour les particules
    document.querySelectorAll('.particles-container').forEach(container => {
        container.addEventListener('mousemove', function(e) {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            document.querySelectorAll('.particle').forEach(particle => {
                const particleX = particle.offsetLeft + particle.offsetWidth / 2;
                const particleY = particle.offsetTop + particle.offsetHeight / 2;
                
                const distX = particleX - x;
                const distY = particleY - y;
                const distance = Math.sqrt(distX * distX + distY * distY);
                
                if (distance < 100) {
                    const force = (100 - distance) / 100;
                    const moveX = distX * force * 0.5;
                    const moveY = distY * force * 0.5;
                    
                    particle.style.transform = `translate(${moveX}px, ${moveY}px)`;
                    particle.style.transition = 'transform 0.3s ease-out';
                } else {
                    particle.style.transform = '';
                    particle.style.transition = 'transform 2s ease-out';
                }
            });
        });
    });
});