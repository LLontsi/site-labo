from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import date

class Theme(models.Model):
    """Thèmes de recherche du laboratoire."""
    nom = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Thème"
        verbose_name_plural = "Thèmes"


class Membre(models.Model):
    """Profil étendu pour chaque utilisateur du laboratoire."""
    STATUT_ANCIEN_CHOICES = [
        ('parti', 'A quitté le laboratoire'),
        ('assistant', 'Reste comme assistant à l\'encadrement'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='membres/photos/', blank=True, null=True)
    titre = models.CharField(max_length=100)
    bio = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    est_responsable = models.BooleanField(default=False)
 
    date_arrivee = models.DateField(default=date(2023, 1, 1))
    date_depart = models.DateField(blank=True, null=True)
    est_ancien = models.BooleanField(default=False)
    statut_ancien = models.CharField(
        max_length=20, 
        choices=STATUT_ANCIEN_CHOICES, 
        blank=True, 
        null=True,
        help_text="Statut de l'ancien membre"
    )
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        
    def get_theme_actuel(self):
        """Retourne le thème de recherche actuel"""
        historique_actuel = self.historique_themes.filter(date_fin__isnull=True).first()
        if historique_actuel:
            return historique_actuel.theme
        return self.theme  # Fallback sur l'ancien champ
    
    def get_historique_themes_complet(self):
        """Retourne l'historique complet des thèmes"""
        return self.historique_themes.select_related('theme').order_by('-date_debut')
    
    def get_duree_theme_actuel(self):
        """Retourne la durée dans le thème actuel en mois"""
        historique_actuel = self.historique_themes.filter(date_fin__isnull=True).first()
        if historique_actuel:
            return historique_actuel.duree_mois
        return None

class Collaborateur(models.Model):
    """Personnes externes collaborant avec le laboratoire."""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    titre = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='collaborateurs/photos/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    lien = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    class Meta:
        verbose_name = "Collaborateur"
        verbose_name_plural = "Collaborateurs"


class Devenir(models.Model):
    """Parcours professionnel des anciens membres."""
    TYPE_STRUCTURE_CHOICES = [
        ('academique', 'Académique'),
        ('industrie', 'Industrie'),
        ('startup', 'Startup'),
    ]
    
    membre = models.OneToOneField(Membre, on_delete=models.CASCADE)
    entreprise = models.CharField(max_length=200)
    poste = models.CharField(max_length=200)
    description = models.TextField()
    realisations = models.TextField(blank=True, null=True)
    date_debut = models.DateField()
    lieu = models.CharField(max_length=200)
    lien = models.URLField(blank=True, null=True)
    domaine = models.CharField(max_length=100)
    type_structure = models.CharField(max_length=20, choices=TYPE_STRUCTURE_CHOICES, default='industrie')
    
    def __str__(self):
        return f"Parcours de {self.membre}"
    
    class Meta:
        verbose_name = "Devenir"
        verbose_name_plural = "Devenirs"


class Invitation(models.Model):
    """Invitations pour rejoindre la plateforme."""
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent')
    
    def __str__(self):
        return f"Invitation pour {self.email}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"


class Presentation(models.Model):
    """Présentations et documents partagés par les membres."""
    TYPE_FICHIER_CHOICES = [
        ('pdf', 'PDF'),
        ('pptx', 'PowerPoint'),
        ('docx', 'Word'),
        ('other', 'Autre'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    fichier = models.FileField(upload_to='presentations/fichiers/')
    type_fichier = models.CharField(max_length=10, choices=TYPE_FICHIER_CHOICES, default='pdf')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    
    # NOUVEAU CHAMP
    fichier_public = models.BooleanField(
        default=False,
        help_text="Le fichier est-il visible et téléchargeable publiquement ?"
    )
    
    def __str__(self):
        return self.titre
    
    def peut_voir_fichier(self, user=None):
        """Détermine si un utilisateur peut voir le fichier."""
        if self.fichier_public:
            return True
        
        if user and user.is_authenticated:
            # L'auteur peut toujours voir son fichier
            if hasattr(user, 'membre') and user.membre == self.membre:
                return True
            # Les admins peuvent toujours voir
            if user.is_staff:
                return True
        
        return False
    
    class Meta:
        verbose_name = "Présentation"
        verbose_name_plural = "Présentations"
        
class ImagePresentation(models.Model):
    """Images associées aux présentations."""
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='presentations/images/')
    legende = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"Image pour {self.presentation.titre}"
    
    class Meta:
        verbose_name = "Image de présentation"
        verbose_name_plural = "Images de présentation"


class Categorie(models.Model):
    """Catégories pour les articles de blog."""
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class Article(models.Model):
    """Articles de blog publiés par les membres."""
    STATUT_VALIDATION_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]
    
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image_principale = models.ImageField(upload_to='articles/images/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(Membre, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Categorie)
    est_publie = models.BooleanField(default=True)
    
    # Nouveaux champs pour la validation
    statut_validation = models.CharField(
        max_length=20, 
        choices=STATUT_VALIDATION_CHOICES, 
        default='en_attente',
        help_text="Statut de validation par l'administrateur"
    )
    date_validation = models.DateTimeField(blank=True, null=True)
    validateur = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='articles_valides',
        help_text="Administrateur qui a validé l'article"
    )
    def est_visible_publiquement(self):
   
        return self.est_publie and self.statut_validation == 'valide'
    commentaire_validation = models.TextField(
        blank=True, 
        null=True,
        help_text="Commentaire de l'administrateur lors de la validation/rejet"
    )
    
    def __str__(self):
        return self.titre
    
    def est_visible_publiquement(self):
        """Retourne True si l'article peut être affiché publiquement"""
        return self.est_publie and self.statut_validation == 'valide'
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

class Temoignage(models.Model):
    """Témoignages des membres ou partenaires."""
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    contenu = models.TextField()
    photo = models.ImageField(upload_to='temoignages/photos/', blank=True, null=True)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"Témoignage de {self.nom}"
    
    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"


class Evenement(models.Model):
    """Événements organisés par le laboratoire."""
    TYPE_CHOICES = [
        ('conference', 'Conférence'),
        ('seminaire', 'Séminaire'),
        ('hackathon', 'Hackathon'),
        ('atelier', 'Atelier'),
        ('autre', 'Autre'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_evenement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField()
    lieu = models.CharField(max_length=200)
    image = models.ImageField(upload_to='evenements/images/', blank=True, null=True)
    
    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        
        
# MODÈLE PROJET SIMPLIFIÉ

class Projet(models.Model):
    """Projets du laboratoire."""
    
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('suspendu', 'Suspendu'),
        ('annule', 'Annulé'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    
    # Thématique de recherche (NOUVEAU)
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        help_text="Thématique de recherche associée",
        null=True
    )
    
    # Date (CONSERVÉ)
    date_debut = models.DateField()
    
    # Statut (CONSERVÉ)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    
   
    participants = models.ManyToManyField(
        Membre,
        blank=True,
        related_name='projets_participant'
    )
    
    # Collaboration (CONSERVÉ)
    collaborateurs_externes = models.ManyToManyField(
        Collaborateur,
        blank=True,
        help_text="Collaborateurs externes au projet"
    )
    
    # Gestion (CONSERVÉ MINIMUM)
    date_creation = models.DateTimeField(auto_now_add=True)
    est_public = models.BooleanField(
        default=True,
        help_text="Le projet est-il visible publiquement ?"
    )
    
    def __str__(self):
        return self.titre
    
    def est_en_cours(self):
        """Retourne True si le projet est en cours"""
        return self.statut == 'en_cours'
    
    def est_termine(self):
        """Retourne True si le projet est terminé"""
        return self.statut == 'termine'
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-date_creation']

class HistoriqueTheme(models.Model):
    """Historique des thèmes de recherche d'un membre."""
    membre = models.ForeignKey(
        Membre, 
        on_delete=models.CASCADE, 
        related_name='historique_themes'
    )
    theme = models.ForeignKey(
        Theme, 
        on_delete=models.CASCADE
    )
    date_debut = models.DateField(
        help_text="Date de début de ce thème de recherche"
    )
    date_fin = models.DateField(
        null=True, 
        blank=True,
        help_text="Date de fin de ce thème (vide si actuel)"
    )
    description = models.TextField(
        blank=True,
        help_text="Description des travaux réalisés dans ce thème"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        fin = f" - {self.date_fin}" if self.date_fin else " - Actuel"
        return f"{self.membre} : {self.theme.nom} ({self.date_debut}{fin})"
    
    @property
    def est_actuel(self):
        """Retourne True si c'est le thème actuel du membre"""
        return self.date_fin is None
    
    @property
    def duree_mois(self):
        """Calcule la durée en mois"""
        if self.date_fin:
            fin = self.date_fin
        else:
            fin = date.today()
        
        delta = fin - self.date_debut
        return round(delta.days / 30.44)  # Moyenne de jours par mois
    
    class Meta:
        verbose_name = "Historique de thème"
        verbose_name_plural = "Historiques de thèmes"
        ordering = ['-date_debut']  # Plus récent en premier
        
        # Un membre ne peut pas avoir le même thème en même temps
        constraints = [
            models.UniqueConstraint(
                fields=['membre', 'theme'],
                condition=models.Q(date_fin__isnull=True),
                name='unique_theme_actuel_par_membre'
            )
        ]

