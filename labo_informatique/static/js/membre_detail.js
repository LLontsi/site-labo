document.addEventListener('DOMContentLoaded', function() {
    // Animation au défilement pour les différentes sections
    const sections = document.querySelectorAll('.profile-content > div');
    
    const animateOnScroll = function() {
        sections.forEach(section => {
            const sectionPosition = section.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (sectionPosition < screenPosition) {
                section.classList.add('animate-in');
            }
        });
    };
    
    // Ajout des classes pour les animations
    sections.forEach(section => {
        section.classList.add('animate-section');
    });
    
    // Animation initiale
    window.addEventListener('load', animateOnScroll);
    
    // Animation au défilement
    window.addEventListener('scroll', animateOnScroll);
});