document.addEventListener('DOMContentLoaded', function () {
    // Animation des éléments au défilement
    initScrollAnimations();

    // Amélioration des champs de formulaire
    enhanceFormFields();
});

// Fonction pour animer les éléments au défilement
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
        animatedElements.forEach(function (element) {
            if (isElementInViewport(element) && !element.classList.contains('visible')) {
                element.classList.add('visible');
            }
        });
    }

    animateVisibleElements();
    window.addEventListener('scroll', animateVisibleElements);
}

// Fonction pour améliorer les champs de formulaire
function enhanceFormFields() {
    const formFields = document.querySelectorAll('input[type="text"], input[type="email"], textarea');

    formFields.forEach(function (field) {
        field.addEventListener('focus', function () {
            this.parentNode.classList.add('field-focused');
        });

        field.addEventListener('blur', function () {
            this.parentNode.classList.remove('field-focused');
            if (this.value.trim() !== '') {
                this.parentNode.classList.add('field-filled');
            } else {
                this.parentNode.classList.remove('field-filled');
            }
        });

        if (field.value.trim() !== '') {
            field.parentNode.classList.add('field-filled');
        }
    });

    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            let isValid = true;

            formFields.forEach(function (field) {
                if (field.hasAttribute('required') && field.value.trim() === '') {
                    isValid = false;
                    field.classList.add('field-error');
                } else {
                    field.classList.remove('field-error');
                }
            });

            const emailField = contactForm.querySelector('input[type="email"]');
            if (emailField && emailField.value.trim() !== '') {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailField.value)) {
                    isValid = false;
                    emailField.classList.add('field-error');
                }
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    }
}
