document.addEventListener('DOMContentLoaded', function() {
    // Gestion des onglets du dashboard
    const navLinks = document.querySelectorAll('.dashboard-nav a');
    const sections = document.querySelectorAll('.dashboard-section-content');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            
            // Masquer toutes les sections
            sections.forEach(section => {
                section.classList.remove('active');
            });
            
            // Afficher la section ciblée
            document.getElementById(targetId).classList.add('active');
            
            // Mettre à jour les liens actifs
            navLinks.forEach(navLink => {
                navLink.classList.remove('active');
            });
            this.classList.add('active');
            
            // Mettre à jour l'URL avec le fragment
            window.history.replaceState(null, null, `#${targetId}`);
        });
    });
    
    // Vérifier si un fragment d'URL est présent
    const hash = window.location.hash;
    if (hash) {
        const targetLink = document.querySelector(`.dashboard-nav a[href="${hash}"]`);
        if (targetLink) {
            targetLink.click();
        }
    }
});