from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='membres/photos/', blank=True, null=True)
    titre = models.CharField(max_length=100)
    bio = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    est_responsable = models.BooleanField(default=False)
    date_arrivee = models.DateField()
    date_depart = models.DateField(blank=True, null=True)
    est_ancien = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"


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
    
    def __str__(self):
        return self.titre
    
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
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image_principale = models.ImageField(upload_to='articles/images/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(Membre, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Categorie)
    est_publie = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titre
    
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
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    image = models.ImageField(upload_to='evenements/images/', blank=True, null=True)
    
    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"