document.addEventListener('DOMContentLoaded', function() {
    // Gestion de la galerie d'images
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const imageUrl = this.querySelector('img').src;
            const caption = this.querySelector('.image-caption p')?.textContent || '';
            
            // Création d'une lightbox pour voir l'image en grand
            const lightbox = document.createElement('div');
            lightbox.classList.add('lightbox');
            
            const lightboxContent = document.createElement('div');
            lightboxContent.classList.add('lightbox-content');
            
            const lightboxImage = document.createElement('img');
            lightboxImage.src = imageUrl;
            
            const lightboxClose = document.createElement('span');
            lightboxClose.classList.add('lightbox-close');
            lightboxClose.innerHTML = '&times;';
            
            const lightboxCaption = document.createElement('div');
            lightboxCaption.classList.add('lightbox-caption');
            lightboxCaption.textContent = caption;
            
            lightboxContent.appendChild(lightboxImage);
            lightboxContent.appendChild(lightboxClose);
            lightboxContent.appendChild(lightboxCaption);
            lightbox.appendChild(lightboxContent);
            
            document.body.appendChild(lightbox);
            
            // Empêcher le défilement du body
            document.body.style.overflow = 'hidden';
            
            // Fermeture de la lightbox
            lightboxClose.addEventListener('click', function() {
                document.body.removeChild(lightbox);
                document.body.style.overflow = '';
            });
            
            // Fermeture en cliquant en dehors de l'image
            lightbox.addEventListener('click', function(e) {
                if (e.target === lightbox) {
                    document.body.removeChild(lightbox);
                    document.body.style.overflow = '';
                }
            });
        });
    });
    
    // Animation au défilement pour les sections
    const sections = document.querySelectorAll('.presentation-content-wrapper > div, .presentation-author-info, .related-presentations');
    
    const animateOnScroll = function() {
        sections.forEach(section => {
            const sectionPosition = section.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (sectionPosition < screenPosition) {
                section.classList.add('fade-in');
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