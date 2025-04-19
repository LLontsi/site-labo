document.addEventListener('DOMContentLoaded', function() {
    // Animation au défilement pour les cartes d'articles
    const articleCards = document.querySelectorAll('.article-card');
    
    const animateOnScroll = function() {
        articleCards.forEach((card, index) => {
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
    articleCards.forEach(card => {
        card.classList.add('animate-card');
    });
    
    // Animation initiale
    window.addEventListener('load', animateOnScroll);
    
    // Animation au défilement
    window.addEventListener('scroll', animateOnScroll);
});