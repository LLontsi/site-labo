document.addEventListener('DOMContentLoaded', function() {
    // Animation des statistiques avec compteur
    const statNumbers = document.querySelectorAll('.stat-value');
    
    const animateCounter = (element) => {
        const target = parseInt(element.textContent);
        const duration = 1500; // durée de l'animation en ms
        const step = target / (duration / 16); // 16ms par frame (approximatif pour 60fps)
        
        let current = 0;
        element.textContent = '0';
        
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
    
    // Animer les compteurs au chargement de la page
    statNumbers.forEach(stat => {
        animateCounter(stat);
    });
    
    // Animation d'apparition des cartes d'activité
    const activityCards = document.querySelectorAll('.activity-card');
    
    const animateCards = () => {
        activityCards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 150);
        });
    };
    
    // Préparer les cartes pour l'animation
    activityCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
    });
    
    // Déclencher l'animation
    setTimeout(animateCards, 300);
    
    // Mise en évidence des lignes de tableau au survol
    const tableRows = document.querySelectorAll('.admin-table tbody tr');
    
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.backgroundColor = 'rgba(var(--color-primary-rgb), 0.05)';
        });
        
        row.addEventListener('mouseleave', () => {
            row.style.backgroundColor = '';
        });
    });
    
    // Animation des actions du tableau
    const tableActions = document.querySelectorAll('.table-action');
    
    tableActions.forEach(action => {
        action.addEventListener('mouseenter', () => {
            action.style.transform = 'scale(1.1)';
        });
        
        action.addEventListener('mouseleave', () => {
            action.style.transform = '';
        });
    });
    
    // Filtrage des contenus dans les tableaux (si applicable)
    const filterInput = document.getElementById('filter-content');
    if (filterInput) {
        filterInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('.admin-table tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
});