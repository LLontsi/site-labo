document.addEventListener('DOMContentLoaded', function() {
    // Filtrage des présentations par thème
    const filterButtons = document.querySelectorAll('.filter-btn');
    const presentationCards = document.querySelectorAll('.presentation-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Mise à jour des boutons actifs
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            
            presentationCards.forEach(card => {
                if (filter === 'all') {
                    card.style.display = '';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 50);
                } else {
                    const theme = card.getAttribute('data-theme');
                    if (theme === filter) {
                        card.style.display = '';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 50);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                }
            });
        });
    });
    
    // Animation au défilement
    const animateOnScroll = function() {
        presentationCards.forEach((card, index) => {
            const cardPosition = card.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (cardPosition < screenPosition) {
                setTimeout(() => {
                    card.classList.add('fade-in');
                }, index * 100); // Animation séquentielle
            }
        });
    };
    
    // Ajout des classes pour les animations
    presentationCards.forEach(card => {
        card.classList.add('animate-card');
    });
    
    // Animation initiale
    window.addEventListener('load', animateOnScroll);
    
    // Animation au défilement
    window.addEventListener('scroll', animateOnScroll);
});