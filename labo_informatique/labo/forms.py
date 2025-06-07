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
            'bio': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control'}),
        }

class PresentationForm(forms.ModelForm):
    """Formulaire de création/édition de présentation."""
    class Meta:
        model = Presentation
        # Pas de fichier_public dans le formulaire
        fields = ('titre', 'description', 'fichier', 'type_fichier', 'theme')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'type_fichier': forms.Select(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
        }

class ImagePresentationForm(forms.ModelForm):
    """Formulaire pour ajouter des images à une présentation."""
    class Meta:
        model = ImagePresentation
        fields = ('image', 'legende')
        widgets = {
            'legende': forms.TextInput(attrs={'class': 'form-control'}),
        }


ImagePresentationFormSet = forms.inlineformset_factory(
    Presentation, ImagePresentation,
    form=ImagePresentationForm,
    extra=3, can_delete=True
)

class ArticleForm(forms.ModelForm):
    """Formulaire de création/édition d'article."""
    class Meta:
        model = Article
        # Enlever 'est_publie' des champs visibles
        fields = ('titre', 'contenu', 'image_principale', 'categories')
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'rich-text-editor form-control', 'rows': 10}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'categories-checkbox-list'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Marquer les champs comme requis
        self.fields['titre'].required = True
        self.fields['contenu'].required = True
        
        # Gestion des valeurs initiales pour la modification
        if self.instance and self.instance.pk:
            # Pré-remplir les champs avec les valeurs existantes
            self.fields['titre'].initial = self.instance.titre
            self.fields['contenu'].initial = self.instance.contenu
            
            # Pré-sélectionner les catégories
            self.fields['categories'].initial = self.instance.categories.all()
    
    def save(self, commit=True):
        article = super().save(commit=False)
        
        # FORCER est_publie à False par défaut
        # Sauf si c'est une modification et que l'article était déjà publié
        if not self.instance.pk:  # Nouvel article
            article.est_publie = False
        # Si c'est une modification, garder l'état actuel de est_publie
        
        if commit:
            article.save()
            # Pour les relations ManyToMany, il faut sauvegarder le formulaire après l'objet
            self.save_m2m()
        
        return article



class DevenirForm(forms.ModelForm):
    """Formulaire pour renseigner le parcours post-laboratoire."""
    class Meta:
        model = Devenir
        fields = ('entreprise', 'poste', 'description', 'realisations', 
                 'date_debut', 'lieu', 'lien', 'domaine', 'type_structure')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'realisations': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'entreprise': forms.TextInput(attrs={'class': 'form-control'}),
            'poste': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
            'lien': forms.URLInput(attrs={'class': 'form-control'}),
            'domaine': forms.TextInput(attrs={'class': 'form-control'}),
            'type_structure': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Formater les dates pour l'affichage dans les inputs HTML5
        if self.instance and self.instance.pk:
            if self.instance.date_debut:
                self.fields['date_debut'].widget.attrs['value'] = self.instance.date_debut.strftime('%Y-%m-%d')


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
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # S'assurer que les champs sont requis
        self.fields['nom'].required = True
        self.fields['role'].required = True
        self.fields['contenu'].required = True
        self.fields['date'].required = True
        
        # Formater les dates pour l'affichage dans les inputs HTML5
        if self.instance and self.instance.pk:
            if self.instance.date:
                self.fields['date'].widget.attrs['value'] = self.instance.date.strftime('%Y-%m-%d')


class EvenementForm(forms.ModelForm):
    """Formulaire d'ajout/édition d'événement."""
    class Meta:
        model = Evenement
        fields = ('titre', 'description', 'type_evenement', 'date_debut', 
                 'date_fin', 'lieu', 'image')
        widgets = {
            'date_debut': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
            'date_fin': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control'
            }),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'type_evenement': forms.Select(attrs={'class': 'form-control'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # S'assurer que les champs sont requis
        self.fields['titre'].required = True
        self.fields['description'].required = True
        self.fields['type_evenement'].required = True
        self.fields['date_debut'].required = True
        self.fields['date_fin'].required = True
        self.fields['lieu'].required = True
        
        # Formater les dates pour l'affichage dans les inputs HTML5
        if self.instance and self.instance.pk:
            if self.instance.date_debut:
                self.fields['date_debut'].widget.attrs['value'] = self.instance.date_debut.strftime('%Y-%m-%d')
            if self.instance.date_fin:
                self.fields['date_fin'].widget.attrs['value'] = self.instance.date_fin.strftime('%Y-%m-%d')
    
    def clean(self):
        """Validation personnalisée."""
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin:
            if date_debut > date_fin:
                raise forms.ValidationError(
                    "La date de début ne peut pas être postérieure à la date de fin."
                )
        
        return cleaned_data


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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Formater les dates pour l'affichage dans les inputs HTML5
        if self.instance and self.instance.pk:
            if self.instance.date_arrivee:
                self.fields['date_arrivee'].widget.attrs['value'] = self.instance.date_arrivee.strftime('%Y-%m-%d')
            if self.instance.date_depart:
                self.fields['date_depart'].widget.attrs['value'] = self.instance.date_depart.strftime('%Y-%m-%d')

class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = [
            'titre',
            'description', 
            'theme',
            'date_debut',
            'statut',
            'participants',
            'collaborateurs_externes',
            'est_public'
        ]
        
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'participants': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-list'}),
            'collaborateurs_externes': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-list'}),
            'est_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'titre': 'Titre du projet',
            'description': 'Description',
            'theme': 'Thème de recherche',
            'date_debut': 'Date de début',
            'statut': 'Statut',
            'participants': 'Participants',
            'collaborateurs_externes': 'Collaborateurs externes',
            'est_public': 'Projet public',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir les queryset pour les champs de relation
        self.fields['theme'].queryset = Theme.objects.all().order_by('nom')
        self.fields['participants'].queryset = Membre.objects.filter(
            est_ancien=False
        ).select_related('user').order_by('user__first_name', 'user__last_name')
        self.fields['collaborateurs_externes'].queryset = Collaborateur.objects.all().order_by('nom', 'prenom')
        
        # CORRECTION CRITIQUE : Ne pas remplir les valeurs dans __init__ mais utiliser la logique Django
        # Django gère automatiquement les valeurs initiales SAUF pour les cas spéciaux
        
        # 1. Pour les champs de date HTML5, forcer le format
        if self.instance and self.instance.pk and self.instance.date_debut:
            # Ne pas utiliser widget.attrs['value'], utiliser initial
            self.initial['date_debut'] = self.instance.date_debut
            # ET forcer le format dans le widget
            self.fields['date_debut'].widget.format = '%Y-%m-%d'
            self.fields['date_debut'].input_formats = ['%Y-%m-%d']

    def clean(self):
        cleaned_data = super().clean()
        
        # Validation optionnelle
        titre = cleaned_data.get('titre')
        if titre and len(titre.strip()) < 3:
            raise forms.ValidationError("Le titre doit contenir au moins 3 caractères.")
        
        return cleaned_data
    
    def save(self, commit=True):
        projet = super().save(commit=False)
        
        if commit:
            projet.save()
            # Important : sauvegarder les relations ManyToMany après l'objet principal
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
                'required': True,
                'class': 'form-control'
            }),
            'date_fin': forms.DateInput(attrs={
                'type': 'date',
                'required': False,
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'required': False,
                'class': 'form-control'
            }),
            'membre': forms.Select(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
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
        
        self.fields['date_debut'].help_text = "Date de début de ce thème de recherche"
        self.fields['date_fin'].help_text = "Laissez vide pour le thème actuel"
        self.fields['description'].help_text = "Description des travaux réalisés dans ce thème"
        
        # Formater les dates pour l'affichage dans les inputs HTML5
        if self.instance and self.instance.pk:
            if self.instance.date_debut:
                self.fields['date_debut'].widget.attrs['value'] = self.instance.date_debut.strftime('%Y-%m-%d')
            if self.instance.date_fin:
                self.fields['date_fin'].widget.attrs['value'] = self.instance.date_fin.strftime('%Y-%m-%d')
    
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