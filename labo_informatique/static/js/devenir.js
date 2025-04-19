document.addEventListener('DOMContentLoaded', function() {
    // Filtrage des membres
    const filterButtons = document.querySelectorAll('.filter-btn');
    const memberCards = document.querySelectorAll('.member-card');
    
    // Filtres actifs
    let activeFilters = {
        domaine: 'all',
        annee: 'all',
        structure: 'all'
    };
    
    // Fonction pour appliquer les filtres
    function applyFilters() {
        memberCards.forEach(card => {
            const domaine = card.getAttribute('data-domaine');
            const annee = card.getAttribute('data-annee');
            const structure = card.getAttribute('data-structure');
            
            const domaineMatch = activeFilters.domaine === 'all' || domaine === activeFilters.domaine;
            const anneeMatch = activeFilters.annee === 'all' || annee === activeFilters.annee;
            const structureMatch = activeFilters.structure === 'all' || structure === activeFilters.structure;
            
            if (domaineMatch && anneeMatch && structureMatch) {
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
        });
    }
    
    // Gestionnaire d'événement pour les boutons de filtre
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filterType = this.getAttribute('data-filter');
            const filterValue = this.getAttribute('data-value');
            
            // Mise à jour du filtre actif pour ce type
            activeFilters[filterType] = filterValue;
            
            // Mise à jour de l'UI des boutons
            document.querySelectorAll(`.filter-btn[data-filter="${filterType}"]`).forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            
            // Appliquer les filtres
            applyFilters();
        });
    });
    
    // Animation au défilement pour les cartes de membres
    const animateOnScroll = function() {
        memberCards.forEach((card, index) => {
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
    memberCards.forEach(card => {
        card.classList.add('animate-card');
    });
    
    // Animation initiale
    window.addEventListener('load', animateOnScroll);
    
    // Animation au défilement
    window.addEventListener('scroll', animateOnScroll);
    
    // Animation pour le graphique de statistiques
    const chartSegments = document.querySelectorAll('.chart-segment');
    
    setTimeout(() => {
        chartSegments.forEach(segment => {
            const width = segment.style.width;
            segment.style.width = '0';
            
            setTimeout(() => {
                segment.style.width = width;
            }, 100);
        });
    }, 500);
});