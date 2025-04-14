# labo/admin.py
from django.contrib import admin
from .models import (
    Theme, Membre, Presentation, ImagePresentation, 
    Categorie, Article, Temoignage, Contact, Evenement
)

admin.site.register(Theme)
admin.site.register(Membre)
admin.site.register(Presentation)
admin.site.register(ImagePresentation)
admin.site.register(Categorie)
admin.site.register(Article)
admin.site.register(Temoignage)
admin.site.register(Contact)
admin.site.register(Evenement)