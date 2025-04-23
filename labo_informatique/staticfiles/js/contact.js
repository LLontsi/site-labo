// JavaScript pour les fonctionnalités de la page Contact et FAQ

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation de l'accordéon FAQ
    initFaqAccordion();
    
    // Animation des éléments au défilement
    initScrollAnimations();
    
    // Amélioration des champs de formulaire
    enhanceFormFields();
});

// Fonction pour initialiser l'accordéon FAQ
function initFaqAccordion() {
    const faqItems = document.querySelectorAll('.faq-item-accordion');
    
    faqItems.forEach(function(item) {
        const header = item.querySelector('.faq-question-header');
        const panel = item.querySelector('.faq-answer-panel');
        
        if (header && panel) {
            // Style initial
            if (!item.classList.contains('active')) {
                panel.style.maxHeight = '0';
            } else {
                panel.style.maxHeight = panel.scrollHeight + 'px';
            }
            
            // Événement de clic
            header.addEventListener('click', function() {
                // Fermer tous les autres éléments
                faqItems.forEach(function(otherItem) {
                    if (otherItem !== item && otherItem.classList.contains('active')) {
                        otherItem.classList.remove('active');
                        const otherPanel = otherItem.querySelector('.faq-answer-panel');
                        if (otherPanel) {
                            otherPanel.style.maxHeight = '0';
                        }
                    }
                });
                
                // Toggle l'élément actuel
                if (item.classList.contains('active')) {
                    item.classList.remove('active');
                    panel.style.maxHeight = '0';
                } else {
                    item.classList.add('active');
                    panel.style.maxHeight = panel.scrollHeight + 'px';
                }
            });
        }
    });
}

// Fonction pour animer les éléments au défilement
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    // Fonction pour vérifier si un élément est visible
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.85 &&
            rect.bottom >= 0
        );
    }
    
    // Fonction pour animer les éléments visibles
    function animateVisibleElements() {
        animatedElements.forEach(function(element) {
            if (isElementInViewport(element) && !element.classList.contains('visible')) {
                element.classList.add('visible');
            }
        });
    }
    
    // Animer les éléments au chargement de la page
    animateVisibleElements();
    
    // Animer les éléments au défilement
    window.addEventListener('scroll', animateVisibleElements);
}

// Fonction pour améliorer les champs de formulaire
function enhanceFormFields() {
    const formFields = document.querySelectorAll('input[type="text"], input[type="email"], textarea');
    
    formFields.forEach(function(field) {
        // Ajouter des effets au focus
        field.addEventListener('focus', function() {
            this.parentNode.classList.add('field-focused');
        });
        
        field.addEventListener('blur', function() {
            this.parentNode.classList.remove('field-focused');
            
            // Ajouter une classe si le champ a une valeur
            if (this.value.trim() !== '') {
                this.parentNode.classList.add('field-filled');
            } else {
                this.parentNode.classList.remove('field-filled');
            }
        });
        
        // Vérifier l'état initial
        if (field.value.trim() !== '') {
            field.parentNode.classList.add('field-filled');
        }
    });
    
    // Validation du formulaire à la soumission
    const contactForm = document.querySelector('.contact-form form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Vérifier les champs requis
            formFields.forEach(function(field) {
                if (field.hasAttribute('required') && field.value.trim() === '') {
                    isValid = false;
                    field.classList.add('field-error');
                } else {
                    field.classList.remove('field-error');
                }
            });
            
            // Validation de l'email
            const emailField = contactForm.querySelector('input[type="email"]');
            if (emailField && emailField.value.trim() !== '') {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailField.value)) {
                    isValid = false;
                    emailField.classList.add('field-error');
                }
            }
            
            // Empêcher la soumission si le formulaire n'est pas valide
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
}