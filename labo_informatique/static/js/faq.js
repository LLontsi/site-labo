// JavaScript pour la page FAQ uniquement

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation de l'accordéon FAQ uniquement
    initFaqAccordion();

    // Animation au scroll si tu en as besoin ici aussi
    initScrollAnimations(); 
});

// Fonction pour initialiser l'accordéon FAQ
function initFaqAccordion() {
    const faqItems = document.querySelectorAll('.faq-item-accordion');

    faqItems.forEach(function(item) {
        const header = item.querySelector('.faq-question-header');
        const panel = item.querySelector('.faq-answer-panel');
        const toggleIcon = item.querySelector('.faq-toggle i');

        if (header && panel) {
            // Style initial
            if (!item.classList.contains('active')) {
                panel.style.maxHeight = '0';
                if (toggleIcon) toggleIcon.classList.replace('fa-minus', 'fa-plus');
            } else {
                panel.style.maxHeight = panel.scrollHeight + 'px';
                if (toggleIcon) toggleIcon.classList.replace('fa-plus', 'fa-minus');
            }

            // Événement de clic
            header.addEventListener('click', function() {
                const isActive = item.classList.contains('active');

                // Fermer tous les autres
                faqItems.forEach(function(otherItem) {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                        const otherPanel = otherItem.querySelector('.faq-answer-panel');
                        const otherIcon = otherItem.querySelector('.faq-toggle i');
                        if (otherPanel) otherPanel.style.maxHeight = '0';
                        if (otherIcon) otherIcon.classList.replace('fa-minus', 'fa-plus');
                    }
                });

                // Basculer l'état de l'élément actuel
                if (isActive) {
                    item.classList.remove('active');
                    panel.style.maxHeight = '0';
                    if (toggleIcon) toggleIcon.classList.replace('fa-minus', 'fa-plus');
                } else {
                    item.classList.add('active');
                    panel.style.maxHeight = panel.scrollHeight + 'px';
                    if (toggleIcon) toggleIcon.classList.replace('fa-plus', 'fa-minus');
                }
            });
        }
    });
}

// Fonction pour animer les éléments au défilement (réutilisable)
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.85 &&
            rect.bottom >= 0
        );
    }

    function animateVisibleElements() {
        animatedElements.forEach(function(element) {
            if (isElementInViewport(element) && !element.classList.contains('visible')) {
                element.classList.add('visible');
            }
        });
    }

    animateVisibleElements(); // Au chargement
    window.addEventListener('scroll', animateVisibleElements); // Au scroll
}
