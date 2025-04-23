document.addEventListener('DOMContentLoaded', function() {
    // Filtrage des membres par thème
    const filterButtons = document.querySelectorAll('.filter-btn');
    const memberCards = document.querySelectorAll('.member-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Mise à jour des boutons actifs
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            
            memberCards.forEach(card => {
                if (filter === 'all') {
                    card.style.display = 'block';
                    // Animation d'apparition
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 50);
                } else {
                    const themes = card.getAttribute('data-themes');
                    if (themes.includes(filter)) {
                        card.style.display = 'block';
                        // Animation d'apparition
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
    
    // Animations au défilement
    const animateOnScroll = function() {
        memberCards.forEach(card => {
            const cardPosition = card.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (cardPosition < screenPosition) {
                card.classList.add('animate');
            }
        });
    };
    
    // Animation initiale
    window.addEventListener('load', animateOnScroll);
    
    // Animation au défilement
    window.addEventListener('scroll', animateOnScroll);
});