from django.contrib import admin
from django.utils.html import format_html
from .models import (Membre, Theme, Collaborateur, Devenir, Invitation,
                    Presentation, ImagePresentation, Categorie, Article,
                    Temoignage, Evenement,Projet)


class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'titre', 'theme', 'est_responsable', 'est_ancien', 'date_arrivee')
    list_filter = ('est_responsable', 'est_ancien', 'theme')
    search_fields = ('user__first_name', 'user__last_name', 'titre', 'bio')
    date_hierarchy = 'date_arrivee'
    
    def nom_complet(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    nom_complet.short_description = "Nom"
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "Aucune photo"
    
    photo_preview.short_description = "Photo"
    
    fieldsets = (
        ("Informations utilisateur", {
            'fields': ('user', 'photo')
        }),
        ("Informations professionnelles", {
            'fields': ('titre', 'bio', 'theme', 'linkedin', 'github', 'portfolio')
        }),
        ("Statut", {
            'fields': ('est_responsable', 'est_ancien', 'date_arrivee', 'date_depart')
        }),
    )


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nombre_membres')
    search_fields = ('nom', 'description')
    
    def nombre_membres(self, obj):
        return Membre.objects.filter(theme=obj).count()
    
    nombre_membres.short_description = "Nombre de membres"


class CollaborateurAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'titre', 'institution')
    search_fields = ('nom', 'prenom', 'titre', 'institution')
    
    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom}"
    
    nom_complet.short_description = "Nom"
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "Aucune photo"
    
    photo_preview.short_description = "Photo"


class DevenirAdmin(admin.ModelAdmin):
    list_display = ('membre', 'entreprise', 'poste', 'type_structure', 'date_debut')
    list_filter = ('type_structure',)
    search_fields = ('membre__user__first_name', 'membre__user__last_name', 'entreprise', 'poste')
    date_hierarchy = 'date_debut'


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'inviter', 'created_at', 'expires_at', 'is_used', 'is_expired')
    list_filter = ('is_used',)
    search_fields = ('email', 'inviter__username')
    readonly_fields = ('token', 'created_at', 'expires_at')
    
    def is_expired(self, obj):
        return obj.is_expired()
    
    is_expired.boolean = True
    is_expired.short_description = "Expirée"


class ImagePresentationInline(admin.TabularInline):
    model = ImagePresentation
    extra = 3


class PresentationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'membre', 'theme', 'type_fichier', 'date_creation')
    list_filter = ('type_fichier', 'theme')
    search_fields = ('titre', 'description', 'membre__user__first_name', 'membre__user__last_name')
    date_hierarchy = 'date_creation'
    inlines = [ImagePresentationInline]


class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nombre_articles')
    search_fields = ('nom', 'description')
    
    def nombre_articles(self, obj):
        return obj.article_set.count()
    
    nombre_articles.short_description = "Nombre d'articles"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_creation', 'est_publie')
    list_filter = ('est_publie', 'categories')
    search_fields = ('titre', 'contenu', 'auteur__user__first_name', 'auteur__user__last_name')
    date_hierarchy = 'date_creation'
    filter_horizontal = ('categories',)


class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'role', 'date')
    search_fields = ('nom', 'role', 'contenu')
    date_hierarchy = 'date'
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "Aucune photo"
    
    photo_preview.short_description = "Photo"


class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_evenement', 'date_debut', 'date_fin', 'lieu')
    list_filter = ('type_evenement',)
    search_fields = ('titre', 'description', 'lieu')
    date_hierarchy = 'date_debut'

class ProjetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'responsable', 'type_projet', 'statut', 'date_debut', 'est_public')
    list_filter = ('statut', 'type_projet', 'est_public', 'date_debut')
    search_fields = ('titre', 'description', 'technologies', 'mots_cles')
    date_hierarchy = 'date_debut'
    filter_horizontal = ('participants', 'collaborateurs_externes')
    
    fieldsets = (
        ("Informations générales", {
            'fields': ('titre', 'description', 'description_courte', 'image_principale')
        }),
        ("Classification", {
            'fields': ('type_projet', 'statut')
        }),
        ("Dates", {
            'fields': ('date_debut', 'date_fin_prevue', 'date_fin_reelle')
        }),
        ("Équipe", {
            'fields': ('responsable', 'participants', 'collaborateurs_externes')
        }),
        ("Liens et ressources", {
            'fields': ('lien_solution', 'lien_github', 'lien_documentation', 'lien_publication')
        }),
        ("Métadonnées", {
            'fields': ('technologies', 'mots_cles', 'est_public')
        }),
    )

# N'oubliez pas d'enregistrer le modèle
admin.site.register(Projet, ProjetAdmin)

admin.site.register(Membre, MembreAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Collaborateur, CollaborateurAdmin)
admin.site.register(Devenir, DevenirAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Presentation, PresentationAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Temoignage, TemoignageAdmin)
admin.site.register(Evenement, EvenementAdmin)