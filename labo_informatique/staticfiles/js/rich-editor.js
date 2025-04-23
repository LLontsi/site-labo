function initRichTextEditor(editor, hiddenInput, toolbar) {
    // Fonction pour exécuter une commande d'édition
    const execCommand = (command, value = null) => {
        document.execCommand(command, false, value);
        editor.focus();
    };
    
    // Ajouter les événements aux boutons de la barre d'outils
    toolbar.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            
            const command = button.getAttribute('data-command');
            
            // Traitement spécial pour certaines commandes
            if (command === 'h1' || command === 'h2' || command === 'h3') {
                execCommand('formatBlock', `<${command}>`);
            } else if (command === 'createLink') {
                const url = prompt('Entrez l\'URL du lien :', 'http://');
                if (url) execCommand(command, url);
            } else if (command === 'insertImage') {
                const url = prompt('Entrez l\'URL de l\'image :', 'http://');
                if (url) execCommand(command, url);
            } else {
                execCommand(command);
            }
            
            // Mettre à jour le contenu du champ caché
            hiddenInput.value = editor.innerHTML;
        });
    });
    
    // Mettre à jour le champ caché lorsque l'éditeur est modifié
    editor.addEventListener('input', () => {
        hiddenInput.value = editor.innerHTML;
    });
    
    // Gérer le collage de texte brut
    editor.addEventListener('paste', (e) => {
        e.preventDefault();
        
        // Récupérer le texte brut depuis le presse-papiers
        const text = (e.clipboardData || window.clipboardData).getData('text/plain');
        
        // Insérer le texte brut à la position du curseur
        document.execCommand('insertText', false, text);
        
        // Mettre à jour le champ caché
        hiddenInput.value = editor.innerHTML;
    });
}