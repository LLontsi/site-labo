// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    // Menu hamburger mobile
     // Menu hamburger mobile
     const hamburger = document.querySelector('.hamburger-menu');
     const navMenu = document.querySelector('.nav-menu');
     
     // Créer l'overlay et la croix de fermeture uniquement sur mobile
     if (window.innerWidth <= 768) {
         // Créer et ajouter l'overlay
         let menuOverlay = document.createElement('div');
         menuOverlay.classList.add('menu-overlay');
         document.body.appendChild(menuOverlay);
         
         // Ajouter la croix de fermeture au menu
         const menuClose = document.createElement('div');
         menuClose.classList.add('menu-close');
         menuClose.innerHTML = '<i class="fas fa-times"></i>';
         navMenu.insertBefore(menuClose, navMenu.firstChild);
         
         // Fonction pour ouvrir le menu
         function openMenu() {
             hamburger.classList.add('open');
             navMenu.classList.add('active');
             menuOverlay.classList.add('active');
         }
         
         // Fonction pour fermer le menu
         function closeMenu() {
             hamburger.classList.remove('open');
             navMenu.classList.remove('active');
             menuOverlay.classList.remove('active');
         }
         
         // Événement pour ouvrir/fermer le menu avec le hamburger
         if (hamburger) {
             hamburger.addEventListener('click', function(e) {
                 e.stopPropagation();
                 if (navMenu.classList.contains('active')) {
                     closeMenu();
                 } else {
                     openMenu();
                 }
             });
         }
         
         // Événement pour fermer le menu avec la croix
         menuClose.addEventListener('click', function() {
             closeMenu();
         });
         
         // Fermer le menu en cliquant sur l'overlay
         menuOverlay.addEventListener('click', function() {
             closeMenu();
         });
         
         // Fermer le menu après avoir cliqué sur un lien
         const navLinks = navMenu.querySelectorAll('a');
         navLinks.forEach(link => {
             link.addEventListener('click', function() {
                 // Attendre un court instant avant de fermer le menu
                 // pour permettre à la navigation de s'effectuer
                 setTimeout(closeMenu, 100);
             });
         });
     }
     
     // Gestion du header fixe au défilement
     const header = document.querySelector('.header');
     const body = document.body;
     
     // Définir la hauteur du header comme variable CSS
     const headerHeight = header.offsetHeight;
     document.documentElement.style.setProperty('--header-height', headerHeight + 'px');
     
     function handleScroll() {
         if (window.scrollY > 100) {
             header.classList.add('scrolled');
             body.classList.add('has-fixed-header');
         } else {
             header.classList.remove('scrolled');
             body.classList.remove('has-fixed-header');
         }
     }
     
     window.addEventListener('scroll', handleScroll);
     
     // Vérifier la position initiale au chargement
     handleScroll();
     
     // Mise à jour lors du redimensionnement de la fenêtre
     window.addEventListener('resize', function() {
         // Réinitialiser si passage desktop -> mobile ou vice versa
         if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
             navMenu.classList.remove('active');
             hamburger.classList.remove('open');
             // Supprimer l'overlay s'il existe
             const existingOverlay = document.querySelector('.menu-overlay');
             if (existingOverlay) {
                 existingOverlay.classList.remove('active');
             }
         }
     });
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
