from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Membre, Presentation, ImagePresentation, Article, Devenir, Temoignage, Evenement


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


class ContactForm(forms.Form):
    """Formulaire de contact."""
    nom = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    sujet = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


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
        fields = ['titre', 'theme', 'bio', 'est_responsable', 'est_ancien', 'photo', 
                 'date_arrivee', 'date_depart', 'linkedin', 'github', 'portfolio']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre/Poste'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Biographie du membre'}),
            'est_responsable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'est_ancien': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
            'photo': 'Photo de profil',
            'date_arrivee': 'Date d\'arrivée',
            'date_depart': 'Date de départ',
            'linkedin': 'Profil LinkedIn',
            'github': 'Profil GitHub',
            'portfolio': 'Site web personnel/Portfolio',
        }