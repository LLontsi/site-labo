// Gérer les animations spécifiques
document.addEventListener('DOMContentLoaded', function() {
    // Animer les nombres (compteurs)
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const duration = 2000; // 2 secondes pour l'animation complète
        const step = target / (duration / 16); // 16ms = environ 60fps
        
        let count = 0;
        const updateCounter = () => {
            count += step;
            if (count < target) {
                counter.innerText = Math.ceil(count);
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target;
            }
        };
        
        // Observer l'élément pour démarrer l'animation quand il devient visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(counter);
    });
    
    // Animation des compétences (barres de progression)
    const skillBars = document.querySelectorAll('.skill-bar');
    
    skillBars.forEach(bar => {
        const progress = bar.querySelector('.skill-progress');
        const value = bar.getAttribute('data-value');
        
        // Observer l'élément pour démarrer l'animation quand il devient visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    progress.style.width = `${value}%`;
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(bar);
    });
    
    // Animation de l'image d'arrière-plan
    const heroImages = document.querySelectorAll('.hero-image, .about-image');
    
    heroImages.forEach(image => {
        image.addEventListener('mousemove', function(e) {
            const { left, top, width, height } = this.getBoundingClientRect();
            const x = (e.clientX - left) / width - 0.5;
            const y = (e.clientY - top) / height - 0.5;
            
            this.style.transform = `translateY(-50%) perspective(1000px) rotateY(${x * 10}deg) rotateX(${-y * 10}deg)`;
        });
        
        image.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-50%)';
        });
    });
    
    // Animer l'apparition des éléments de la grille
    const gridItems = document.querySelectorAll('.team-card, .blog-card, .feature-card');
    
    gridItems.forEach((item, index) => {
        // Ajouter un délai différent pour chaque élément
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = `opacity 0.5s ease, transform 0.5s ease ${index * 0.1}s`;
        
        // Observer l'élément pour démarrer l'animation quand il devient visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(item);
    });
});