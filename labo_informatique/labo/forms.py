# labo/forms.py
from django import forms
from .models import Contact, Membre, Article, Presentation, ImagePresentation

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['nom', 'email', 'sujet', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['photo', 'titre', 'bio', 'theme', 'linkedin', 'github']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image_principale', 'categories', 'est_publie']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 10}),
        }

class PresentationForm(forms.ModelForm):
     # Utilisation d'un champ ordinaire sans l'attribut multiple
    images_supplementaires = forms.FileField(
        required=False,
        help_text="Vous ne pouvez télécharger qu'une image à la fois. Pour ajouter plusieurs images, sauvegardez puis modifiez à nouveau."
    )
    
    class Meta:
        model = Presentation
        fields = ['titre', 'description', 'fichier', 'type_fichier', 'theme']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class ImagePresentationForm(forms.ModelForm):
    class Meta:
        model = ImagePresentation
        fields = ['image', 'legende']