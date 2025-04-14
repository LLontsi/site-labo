from django.db import models

# Create your models here.
# labo/models.py
from django.db import models
from django.contrib.auth.models import User

# Modèles pour les membres et thèmes
class Theme(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.nom

class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    photo = models.ImageField(upload_to='membres/', blank=True, null=True)
    titre = models.CharField(max_length=100)
    bio = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, related_name='membres')
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# Modèles pour les présentations
class Presentation(models.Model):
    TYPES = (
        ('PDF', 'Document PDF'),
        ('PPTX', 'Présentation PowerPoint'),
        ('IMAGE', 'Image'),
    )
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    fichier = models.FileField(upload_to='presentations/')
    type_fichier = models.CharField(max_length=10, choices=TYPES)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='presentations')
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, related_name='presentations')
    
    def __str__(self):
        return self.titre

class ImagePresentation(models.Model):
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='presentations/images/')
    legende = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"Image pour {self.presentation.titre}"

# Modèles pour le blog
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nom

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image_principale = models.ImageField(upload_to='blog/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='articles')
    categories = models.ManyToManyField(Categorie, related_name='articles')
    est_publie = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titre

# Modèles pour les fonctionnalités de base
class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    contenu = models.TextField()
    photo = models.ImageField(upload_to='temoignages/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Témoignage de {self.nom}"

class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_traite = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message de {self.nom}: {self.sujet}"

class Evenement(models.Model):
    TYPES = (
        ('HACKATHON', 'Hackathon'),
        ('SEMINAIRE', 'Séminaire'),
        ('CONFERENCE', 'Conférence'),
        ('ATELIER', 'Atelier'),
    )
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_evenement = models.CharField(max_length=20, choices=TYPES)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    image = models.ImageField(upload_to='evenements/', blank=True, null=True)
    
    def __str__(self):
        return self.titre