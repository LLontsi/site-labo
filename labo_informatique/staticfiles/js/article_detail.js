document.addEventListener('DOMContentLoaded', function() {
    // Personnalisation des images dans le contenu de l'article
    const articleContent = document.querySelector('.article-content');
    if (articleContent) {
        const images = articleContent.querySelectorAll('img');
        
        images.forEach(img => {
            // Wrapper l'image dans un div pour le style
            const imageWrapper = document.createElement('div');
            imageWrapper.classList.add('article-image-wrapper');
            
            // Clone l'image
            const newImg = img.cloneNode(true);
            
            // Remplacement de l'image par le wrapper + image
            imageWrapper.appendChild(newImg);
            img.parentNode.replaceChild(imageWrapper, img);
            
            // Ajout d'un événement de clic pour agrandir l'image
            imageWrapper.addEventListener('click', function() {
                const lightbox = document.createElement('div');
                lightbox.classList.add('lightbox');
                
                const lightboxContent = document.createElement('div');
                lightboxContent.classList.add('lightbox-content');
                
                const lightboxImage = document.createElement('img');
                lightboxImage.src = newImg.src;
                
                const lightboxClose = document.createElement('span');
                lightboxClose.classList.add('lightbox-close');
                lightboxClose.innerHTML = '&times;';
                
                lightboxContent.appendChild(lightboxImage);
                lightboxContent.appendChild(lightboxClose);
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
    }
    
    // Animation au défilement pour les sections
    const sections = document.querySelectorAll('.article-main > div, .related-articles');
    
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