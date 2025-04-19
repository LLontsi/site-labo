// Script pour l'accordéon FAQ
document.addEventListener('DOMContentLoaded', function() {
    const faqItems = document.querySelectorAll('.faq-item-accordion');
    
    faqItems.forEach(item => {
        const header = item.querySelector('.faq-question-header');
        
        header.addEventListener('click', function() {
            // Toggle l'état actif de l'élément
            item.classList.toggle('active');
            
            // Fermer les autres éléments
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });
        });
    });
    
    // Animation au défilement
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    faqItems.forEach(item => {
        observer.observe(item);
    });
    
    // Ouvrir le premier élément par défaut
    if (faqItems.length > 0) {
        faqItems[0].classList.add('active');
    }
});