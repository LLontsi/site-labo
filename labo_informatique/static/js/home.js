document.addEventListener('DOMContentLoaded', function() {
    // Animation des statistiques avec compteur
    const statNumbers = document.querySelectorAll('.stat-number');
    
    const animateCounter = (element) => {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000; // durée de l'animation en ms
        const step = target / (duration / 16); // 16ms par frame (approximatif pour 60fps)
        
        let current = 0;
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                clearInterval(timer);
                element.textContent = target;
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    };
    
    // Fonction pour vérifier si un élément est visible dans la fenêtre
    const isElementInViewport = (el) => {
        const rect = el.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.bottom >= 0
        );
    };
    
    // Animation des éléments au défilement
    const animateOnScroll = () => {
        // Animation des statistiques
        statNumbers.forEach(stat => {
            if (isElementInViewport(stat) && !stat.classList.contains('animated')) {
                stat.classList.add('animated');
                animateCounter(stat);
            }
        });
        
        // Animation des sections
        document.querySelectorAll('.animate-on-scroll').forEach(element => {
            if (isElementInViewport(element) && !element.classList.contains('animated')) {
                element.classList.add('animated', 'fade-in');
                
                // Si l'élément a un délai, ajouter la classe après le délai
                const delay = element.classList.contains('delay-200') ? 200 :
                              element.classList.contains('delay-400') ? 400 : 0;
                
                if (delay > 0) {
                    setTimeout(() => {
                        element.classList.add('visible');
                    }, delay);
                } else {
                    element.classList.add('visible');
                }
            }
        });
    };
    
    // Initialiser l'animation au chargement de la page
    animateOnScroll();
    
    // Ajouter l'événement de défilement pour continuer les animations
    window.addEventListener('scroll', animateOnScroll);
    
    // Carousel de témoignages (version simple sans dépendances)
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
            currentTestimonial = (currentTestimonial + 1) % testimonials.length;
            testimonials[currentTestimonial].style.display = 'block';
            testimonials[currentTestimonial].classList.add('fade-in');
        };
        
        // Change de témoignage toutes les 5 secondes
        setInterval(nextTestimonial, 5000);
    }
});