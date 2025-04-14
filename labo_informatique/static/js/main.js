// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    // Menu hamburger mobile
    const hamburger = document.querySelector('.hamburger-menu');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            this.classList.toggle('open');
            navMenu.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });
        
        // Fermer le menu en cliquant à l'extérieur
        document.addEventListener('click', function(event) {
            if (navMenu.classList.contains('active') && 
                !event.target.closest('.nav-menu') && 
                !event.target.closest('.hamburger-menu')) {
                hamburger.classList.remove('open');
                navMenu.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });
        
        // Fermer le menu en cliquant sur un lien
        const navLinks = document.querySelectorAll('.nav-menu a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('open');
                navMenu.classList.remove('active');
                document.body.classList.remove('menu-open');
            });
        });
    }
    
    // Animation au défilement
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    function checkScroll() {
        animateElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            const windowHeight = window.innerHeight;
            
            // Si l'élément est visible dans la fenêtre
            if (elementTop < windowHeight - 100 && elementBottom > 0) {
                element.classList.add('visible');
            }
        });
    }
    
    // Vérifier au chargement initial
    checkScroll();
    
    // Écouter l'événement de défilement
    window.addEventListener('scroll', checkScroll);
    
    // Générer les particules
    generateParticles();
    
    // Filtres d'équipe ou de blog
    const filterButtons = document.querySelectorAll('.team-filter-btn, .blog-filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Retirer la classe active des autres boutons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Ajouter la classe active au bouton cliqué
            this.classList.add('active');
            
            // Filtrer les éléments
            const filter = this.getAttribute('data-filter');
            const items = document.querySelectorAll('.team-card, .blog-card, .presentation-card');
            
            items.forEach(item => {
                if (filter === 'all' || item.getAttribute('data-theme') === filter) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});

// Générer des particules aléatoires pour le header et le footer
function generateParticles() {
    const headerParticles = document.querySelector('.header .particles-container');
    const footerParticles = document.querySelector('.footer .particles-container');
    
    if (headerParticles) {
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            // Taille aléatoire
            const size = Math.random() * 10 + 5;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            // Position aléatoire
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.left = `${Math.random() * 100}%`;
            
            // Animation aléatoire
            const animationDuration = Math.random() * 20 + 10;
            particle.style.animation = `particleMove${Math.random() > 0.5 ? 1 : 2} ${animationDuration}s infinite ease-in-out`;
            
            // Délai d'animation aléatoire
            particle.style.animationDelay = `${Math.random() * 5}s`;
            
            headerParticles.appendChild(particle);
        }
    }
    
    if (footerParticles) {
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            // Taille aléatoire
            const size = Math.random() * 10 + 5;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            // Position aléatoire
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.left = `${Math.random() * 100}%`;
            
            // Animation aléatoire
            const animationDuration = Math.random() * 20 + 10;
            particle.style.animation = `particleMove${Math.random() > 0.5 ? 1 : 2} ${animationDuration}s infinite ease-in-out`;
            
            // Délai d'animation aléatoire
            particle.style.animationDelay = `${Math.random() * 5}s`;
            
            footerParticles.appendChild(particle);
        }
    }
}