from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Membre, Presentation, ImagePresentation, Article, Devenir, Temoignage, Evenement,Projet,Collaborateur,HistoriqueTheme,Theme
import re
import socket
import dns.resolver
from django.core.exceptions import ValidationError
from datetime import date
from datetime import timedelta
from django.db.models import Q 
from .utils import validate_email_domain

class InvitationRegistrationForm(UserCreationForm):
    """Formulaire d'inscription par invitation."""
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(required=True, widget=forms.HiddenInput())
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class MembreProfileForm(forms.ModelForm):
    """Formulaire de création/édition de profil de membre."""
    class Meta:
        model = Membre
        fields = ('photo', 'titre', 'bio', 'theme', 'linkedin', 'github', 'portfolio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }


class PresentationForm(forms.ModelForm):
    """Formulaire de création/édition de présentation."""
    class Meta:
        model = Presentation
        fields = ('titre', 'description', 'fichier', 'type_fichier', 'theme')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class ImagePresentationForm(forms.ModelForm):
    """Formulaire pour ajouter des images à une présentation."""
    class Meta:
        model = ImagePresentation
        fields = ('image', 'legende')


ImagePresentationFormSet = forms.inlineformset_factory(
    Presentation, ImagePresentation,
    form=ImagePresentationForm,
    extra=3, can_delete=True
)


class ArticleForm(forms.ModelForm):
    """Formulaire de création/édition d'article."""
    class Meta:
        model = Article
        fields = ('titre', 'contenu', 'image_principale', 'categories', 'est_publie')
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'rich-text-editor'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'categories-checkbox-list'}),
        }


class DevenirForm(forms.ModelForm):
    """Formulaire pour renseigner le parcours post-laboratoire."""
    class Meta:
        model = Devenir
        fields = ('entreprise', 'poste', 'description', 'realisations', 
                 'date_debut', 'lieu', 'lien', 'domaine', 'type_structure')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'realisations': forms.Textarea(attrs={'rows': 5}),
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
        }


# 1. Validation complète dans le formulaire
class ContactForm(forms.Form):
    nom = forms.CharField(max_length=100, label="Nom")
    email = forms.EmailField(label="Email")
    sujet = forms.CharField(max_length=200, label="Sujet")
    message = forms.CharField(widget=forms.Textarea, label="Message")
    
    def clean_email(self):
        """Valide que l'adresse email existe réellement."""
        email = self.cleaned_data.get('email')
        
        # Déjà validé par EmailField (syntaxe)
        if not email:
            return email
            
        # Vérification DNS du domaine
        try:
            domain = email.split('@')[1]
            validate_email_domain(email)
            return email
        except ValidationError as e:
            raise forms.ValidationError(str(e))


class InvitationForm(forms.Form):
    """Formulaire d'envoi d'invitation."""
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=False, 
                             help_text="Message personnalisé (optionnel)")


class TemoignageForm(forms.ModelForm):
    """Formulaire d'ajout/édition de témoignage."""
    class Meta:
        model = Temoignage
        fields = ('nom', 'role', 'contenu', 'photo', 'date')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'contenu': forms.Textarea(attrs={'rows': 5}),
        }


class EvenementForm(forms.ModelForm):
    """Formulaire d'ajout/édition d'événement."""
    class Meta:
        model = Evenement
        fields = ('titre', 'description', 'type_evenement', 'date_debut', 
                 'date_fin', 'lieu', 'image')
        widgets = {
            'date_debut': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        

class UserCreateForm(forms.ModelForm):
    """Formulaire pour créer un nouvel utilisateur."""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        labels = {
            'username': 'Nom d\'utilisateur',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse email',
        }
        help_texts = {
            'username': 'Requis. 150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement.',
        }
        error_messages = {
            'username': {
                'unique': 'Ce nom d\'utilisateur est déjà utilisé.',
            },
        }
class MembreForm(forms.ModelForm):
    """Formulaire pour créer ou modifier un profil de membre."""
    class Meta:
        model = Membre
        fields = ['titre', 'theme', 'bio', 'est_responsable', 'est_ancien', 'statut_ancien', 'photo', 
                 'date_arrivee', 'date_depart', 'linkedin', 'github', 'portfolio']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre/Poste'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Biographie du membre'}),
            'est_responsable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'est_ancien': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'statut_ancien': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'date_arrivee': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_depart': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }
        labels = {
            'titre': 'Titre/Position',
            'theme': 'Thème de recherche',
            'bio': 'Biographie',
            'est_responsable': 'Est responsable',
            'est_ancien': 'Est un ancien membre',
            'statut_ancien': 'Statut de l\'ancien membre',
            'photo': 'Photo de profil',
            'date_arrivee': 'Date d\'arrivée',
            'date_depart': 'Date de départ',
            'linkedin': 'Profil LinkedIn',
            'github': 'Profil GitHub',
            'portfolio': 'Site web personnel/Portfolio',
        }
class ProjetForm(forms.ModelForm):
    """Formulaire de création/édition de projet."""
    
    class Meta:
        model = Projet
        fields = [
            'titre', 'description', 'description_courte', 'image_principale',
            'date_debut', 'date_fin_prevue', 'date_fin_reelle',
            'statut', 'type_projet', 'responsable', 'participants', 'collaborateurs_externes',
            'lien_solution', 'lien_github', 'lien_documentation', 'lien_publication',
            'technologies', 'mots_cles', 'est_public'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'description_courte': forms.Textarea(attrs={'rows': 3}),
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin_prevue': forms.DateInput(attrs={'type': 'date'}),
            'date_fin_reelle': forms.DateInput(attrs={'type': 'date'}),
            'participants': forms.CheckboxSelectMultiple(),
            'collaborateurs_externes': forms.CheckboxSelectMultiple(),
            'technologies': forms.TextInput(attrs={'placeholder': 'Python, Django, React, etc.'}),
            'mots_cles': forms.TextInput(attrs={'placeholder': 'IA, Machine Learning, Web, etc.'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrer les responsables : seuls les membres avec est_responsable=True
        # Inclure les anciens responsables qui restent comme assistants
        self.fields['responsable'].queryset = Membre.objects.filter(
            est_responsable=True
        ).filter(
            Q(est_ancien=False) |  # Membres actuels
            Q(est_ancien=True, statut_ancien='assistant')  # Anciens qui restent assistants
        ).select_related('user').order_by('user__first_name', 'user__last_name')
        
        # Tous les membres peuvent être participants (actuels et anciens assistants)
        participants_queryset = Membre.objects.filter(
            Q(est_ancien=False) |  # Membres actuels
            Q(est_ancien=True, statut_ancien='assistant')  # Anciens qui restent assistants
        ).select_related('user').order_by('user__first_name', 'user__last_name')
        
        self.fields['participants'].queryset = participants_queryset
        
        # Améliorer l'affichage des participants dans la liste déroulante
        self.fields['participants'].widget.choices = [
            (membre.id, f"{membre.user.first_name} {membre.user.last_name} ({membre.titre})")
            for membre in participants_queryset
        ]
        
        # Tous les collaborateurs externes
        collaborateurs_queryset = Collaborateur.objects.all().order_by('prenom', 'nom')
        self.fields['collaborateurs_externes'].queryset = collaborateurs_queryset
        
        # Améliorer l'affichage des collaborateurs externes dans la liste déroulante
        self.fields['collaborateurs_externes'].widget.choices = [
            (collab.id, f"{collab.prenom} {collab.nom} ({collab.institution})")
            for collab in collaborateurs_queryset
        ]
        
        # Personnaliser les labels
        self.fields['responsable'].label = "Chef de projet"
        self.fields['responsable'].help_text = "Seuls les membres responsables peuvent être chefs de projet"
        self.fields['participants'].label = "Participants"
        self.fields['participants'].help_text = "Maintenez Ctrl (ou Cmd sur Mac) pour sélectionner plusieurs participants"
        self.fields['collaborateurs_externes'].label = "Collaborateurs externes"
        self.fields['collaborateurs_externes'].help_text = "Maintenez Ctrl (ou Cmd sur Mac) pour sélectionner plusieurs collaborateurs"
        
        # Style
        self.fields['responsable'].widget.attrs.update({'class': 'form-control'})
        
        # Vérification de disponibilité
        if not self.fields['responsable'].queryset.exists():
            self.fields['responsable'].help_text = "⚠️ Aucun membre responsable disponible. Veuillez d'abord désigner des responsables."
    
    def clean(self):
        cleaned_data = super().clean()
        
        responsable = cleaned_data.get('responsable')
        participants = cleaned_data.get('participants')
        
        # Vérifier que le responsable a bien le statut de responsable
        if responsable and not responsable.est_responsable:
            raise forms.ValidationError(
                "Le membre sélectionné comme chef de projet doit avoir le statut de responsable."
            )
        
        # Éviter la redondance responsable/participant
        if responsable and participants and responsable in participants.all():
            participants = participants.exclude(id=responsable.id)
            cleaned_data['participants'] = participants
        
        return cleaned_data
    
    def save(self, commit=True):
        projet = super().save(commit=False)
        
        if commit:
            projet.save()
            # Sauvegarder les relations ManyToMany
            self.save_m2m()
        
        return projet
class HistoriqueThemeForm(forms.ModelForm):
    """Formulaire pour créer/éditer un historique de thème."""
    
    class Meta:
        model = HistoriqueTheme
        fields = ['membre', 'theme', 'date_debut', 'date_fin', 'description']
        widgets = {
            'date_debut': forms.DateInput(attrs={
                'type': 'date',
                'required': True
            }),
            'date_fin': forms.DateInput(attrs={
                'type': 'date',
                'required': False
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'required': False
            }),
        }
    
    def __init__(self, *args, **kwargs):
        membre = kwargs.pop('membre', None)
        super().__init__(*args, **kwargs)
        
        self.fields['theme'].required = True
        self.fields['date_debut'].required = True
        self.fields['date_fin'].required = False
        self.fields['description'].required = False
        
        if membre and not self.instance.pk:
            self.fields['membre'].widget = forms.HiddenInput()
            self.fields['membre'].initial = membre
            self.fields['membre'].required = False
        else:
            self.fields['membre'].required = True
            self.fields['membre'].queryset = Membre.objects.select_related('user').order_by('user__first_name', 'user__last_name')
        
        self.fields['theme'].queryset = Theme.objects.all().order_by('nom')
        
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['date_debut'].help_text = "Date de début de ce thème de recherche"
        self.fields['date_fin'].help_text = "Laissez vide pour le thème actuel"
        self.fields['description'].help_text = "Description des travaux réalisés dans ce thème"
    
    def clean(self):
        cleaned_data = super().clean()
        membre = cleaned_data.get('membre')
        theme = cleaned_data.get('theme')
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if not membre and self.instance and self.instance.membre:
            membre = self.instance.membre
            cleaned_data['membre'] = membre
        
        if not all([membre, theme, date_debut]):
            return cleaned_data
        
        # Vérifier que la date de fin est après la date de début
        if date_fin and date_fin <= date_debut:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")
        
        # ✅ NOUVELLE LOGIQUE : Gérer automatiquement les chevauchements
        queryset = HistoriqueTheme.objects.filter(membre=membre)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        # Si on crée un nouveau thème actuel (sans date_fin)
        if not date_fin:
            themes_actuels = queryset.filter(date_fin__isnull=True)
            if themes_actuels.exists():
                # On va automatiquement terminer l'ancien thème
                # Pas d'erreur ici, on le gère dans save()
                pass
        else:
            # Vérifier les chevauchements normalement pour les thèmes avec date de fin
            for historique in queryset:
                if self._periodes_chevauchent(date_debut, date_fin, historique.date_debut, historique.date_fin):
                    raise ValidationError(
                        f"Cette période chevauche avec un autre thème : "
                        f"{historique.theme.nom} ({historique.date_debut} - "
                        f"{historique.date_fin or 'Actuel'})"
                    )
        
        return cleaned_data
    
    def save(self, commit=True):
        """Sauvegarder en gérant automatiquement les thèmes actuels."""
        from datetime import date
        
        instance = super().save(commit=False)
        
        # ✅ Si on crée un nouveau thème actuel, terminer l'ancien
        if not instance.date_fin and instance.membre:  # Nouveau thème actuel
            # Trouver les thèmes actuels existants
            themes_actuels = HistoriqueTheme.objects.filter(
                membre=instance.membre,
                date_fin__isnull=True
            )
            
            # Si on modifie un existant, l'exclure
            if instance.pk:
                themes_actuels = themes_actuels.exclude(pk=instance.pk)
            
            # Terminer tous les thèmes actuels à la veille du nouveau thème
            if themes_actuels.exists():
                date_fin_ancien = instance.date_debut - timedelta(days=1)
                themes_actuels.update(date_fin=date_fin_ancien)
                print(f"Anciens thèmes terminés le {date_fin_ancien}")
        
        if commit:
            instance.save()
        
        return instance
    
    def _periodes_chevauchent(self, debut1, fin1, debut2, fin2):
        """Vérifie si deux périodes se chevauchent."""
        from datetime import date, timedelta
        fin1 = fin1 or date.today() + timedelta(days=365*10)
        fin2 = fin2 or date.today() + timedelta(days=365*10)
        return not (fin1 <= debut2 or fin2 <= debut1)