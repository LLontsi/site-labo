document.addEventListener('DOMContentLoaded', function() {
    // Animation au défilement pour les boîtes d'organigramme
    const orgBoxes = document.querySelectorAll('.org-box');
    
    const animateOrgBoxes = function() {
        orgBoxes.forEach((box, index) => {
            const boxPosition = box.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (boxPosition < screenPosition) {
                setTimeout(() => {
                    box.classList.add('fade-in');
                }, index * 150); // Animation séquentielle
            }
        });
    };
    
    // Animation au défilement pour les cartes de collaborateurs
    const collabCards = document.querySelectorAll('.collaborateur-card');
    
    const animateCollabCards = function() {
        collabCards.forEach((card, index) => {
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
    orgBoxes.forEach(box => {
        box.classList.add('animate-box');
    });
    
    collabCards.forEach(card => {
        card.classList.add('animate-card');
    });
    
    // Animation initiale
    window.addEventListener('load', function() {
        animateOrgBoxes();
        animateCollabCards();
    });
    
    // Animation au défilement
    window.addEventListener('scroll', function() {
        animateOrgBoxes();
        animateCollabCards();
    });
});