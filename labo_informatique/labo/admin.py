from django.contrib import admin
from django.utils.html import format_html
from .models import (Membre, Theme, Collaborateur, Devenir, Invitation,
                    Presentation, ImagePresentation, Categorie, Article,
                    Temoignage, Evenement, Projet, HistoriqueTheme)

# 1. DÉFINIR D'ABORD HistoriqueThemeInline (AVANT MembreAdmin)
class HistoriqueThemeInline(admin.TabularInline):
    """Inline pour gérer l'historique des thèmes depuis la page membre."""
    model = HistoriqueTheme
    extra = 0
    ordering = ['-date_debut']
    fields = ('theme', 'date_debut', 'date_fin', 'description')
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Pré-remplir la date de début avec la date d'arrivée du membre
        if obj and obj.date_arrivee:
            formset.form.base_fields['date_debut'].widget.attrs['placeholder'] = f"Ex: {obj.date_arrivee}"
        return formset

# 2. DÉFINIR ImagePresentationInline
class ImagePresentationInline(admin.TabularInline):
    model = ImagePresentation
    extra = 3

# 3. MAINTENANT MembreAdmin peut utiliser HistoriqueThemeInline
class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'titre', 'theme', 'est_responsable', 'est_ancien', 'date_arrivee')
    list_filter = ('est_responsable', 'est_ancien', 'theme')
    search_fields = ('user__first_name', 'user__last_name', 'titre', 'bio')
    date_hierarchy = 'date_arrivee'
    inlines = [HistoriqueThemeInline]  # Maintenant ça marche !
    
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
    
    def save_related(self, request, form, formsets, change):
        """Synchroniser le champ theme avec l'historique actuel."""
        super().save_related(request, form, formsets, change)
        
        # Mettre à jour le champ theme avec le thème actuel
        membre = form.instance
        theme_actuel = membre.get_theme_actuel()
        if theme_actuel != membre.theme:
            membre.theme = theme_actuel
            membre.save(update_fields=['theme'])

# 4. HistoriqueThemeAdmin
@admin.register(HistoriqueTheme)
class HistoriqueThemeAdmin(admin.ModelAdmin):
    """Administration des historiques de thèmes."""
    list_display = ['membre', 'theme', 'date_debut', 'date_fin', 'est_actuel', 'duree_mois']
    list_filter = ['theme', 'date_debut', 'membre__est_ancien']
    search_fields = ['membre__user__first_name', 'membre__user__last_name', 'theme__nom']
    ordering = ['-date_debut']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('membre', 'theme')
        }),
        ('Période', {
            'fields': ('date_debut', 'date_fin'),
            'description': 'Laissez la date de fin vide pour le thème actuel'
        }),
        ('Description', {
            'fields': ('description',),
            'description': 'Décrivez les travaux réalisés dans ce thème'
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('membre__user', 'theme')

# 5. VOS AUTRES ADMIN (restent identiques)
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
    list_display = ('titre', 'responsable', 'theme', 'statut', 'date_debut', 'est_public')
    list_filter = ('statut', 'theme', 'est_public', 'date_debut')
    search_fields = ('titre', 'description', 'responsable__user__first_name', 'responsable__user__last_name')
    date_hierarchy = 'date_debut'
    filter_horizontal = ('participants', 'collaborateurs_externes')
    
    fieldsets = (
        ("Informations générales", {
            'fields': ('titre', 'description', 'theme')
        }),
        ("Statut et date", {
            'fields': ('statut', 'date_debut')
        }),
        ("Équipe", {
            'fields': ('responsable', 'participants', 'collaborateurs_externes')
        }),
        ("Visibilité", {
            'fields': ('est_public',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'responsable__user', 'theme'
        ).prefetch_related('participants', 'collaborateurs_externes')

# 6. ENREGISTREMENTS (à la fin)
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
admin.site.register(Projet, ProjetAdmin)
# HistoriqueTheme est déjà enregistré avec @admin.register(HistoriqueTheme)