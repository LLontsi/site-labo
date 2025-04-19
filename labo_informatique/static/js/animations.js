document.addEventListener('DOMContentLoaded', function() {
    // Animation des éléments au défilement
    const animateElements = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            // Si l'élément est dans la fenêtre visible
            if (elementPosition < windowHeight - 100) {
                element.classList.add('animated');
            }
        });
    };
    
    // Initialiser l'animation au chargement de la page
    animateElements();
    
    // Continuer l'animation au défilement
    window.addEventListener('scroll', animateElements);
    
    // Animation spécifique pour les éléments avec un délai
    document.querySelectorAll('[class*="delay-"]').forEach(element => {
        const classes = element.className.split(' ');
        let delay = 0;
        
        classes.forEach(className => {
            if (className.startsWith('delay-')) {
                delay = parseInt(className.replace('delay-', ''));
            }
        });
        
        if (delay > 0) {
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, delay);
        }
    });

    // Animer les nombres (compteurs)
    const counters = document.querySelectorAll('.counter, .stat-number');
        
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target') || +counter.getAttribute('data-count') || 0;
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
                    
            this.style.transform = `perspective(1000px) rotateY(${x * 10}deg) rotateX(${-y * 10}deg)`;
        });
            
        image.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
        
    // Animer l'apparition des éléments de la grille
    const gridItems = document.querySelectorAll('.team-card, .news-card, .domain-card, .event-card, .testimonial-card');
        
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

    // Animation du carousel de témoignages
    const testimonials = document.querySelectorAll('.testimonial-card');
    let currentTestimonial = 0;
    
    if (testimonials.length > 1) {
        // Cache tous les témoignages sauf le premier
        testimonials.forEach((testimonial, index) => {
            if (index !== 0) {
                testimonial.style.display = 'none';
            }
        });
        
        // Fonction pour passer au témoignage suivant
        const nextTestimonial = () => {
            testimonials[currentTestimonial].style.display = 'none';
            testimonials[currentTestimonial].style.opacity = '0';
            currentTestimonial = (currentTestimonial + 1) % testimonials.length;
            testimonials[currentTestimonial].style.display = 'block';
            
            // Animation fade-in
            setTimeout(() => {
                testimonials[currentTestimonial].style.opacity = '1';
            }, 50);
        };
        
        // Change de témoignage toutes les 5 secondes
        setInterval(nextTestimonial, 5000);
    }
});