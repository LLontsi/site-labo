from django.shortcuts import render

# Create your views here.
# labo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import (
    Theme, Membre, Presentation, ImagePresentation, 
    Categorie, Article, Temoignage, Contact, Evenement
)
from .forms import (
    ContactForm, MembreForm, ArticleForm, PresentationForm, ImagePresentationForm
)

# ----- VUES POUR LES PAGES PRINCIPALES (anciennement core) -----

def home(request):
    # Récupérer les derniers articles de blog
    derniers_articles = Article.objects.filter(est_publie=True).order_by('-date_creation')[:3]
    # Récupérer les événements à venir
    evenements = Evenement.objects.filter(date_fin__gte=timezone.now()).order_by('date_debut')[:3]
    # Récupérer quelques témoignages
    temoignages = Temoignage.objects.all().order_by('?')[:3]
    # Récupérer quelques membres
    membres = Membre.objects.all().order_by('?')[:3]
    
    context = {
        'derniers_articles': derniers_articles,
        'evenements': evenements,
        'temoignages': temoignages,
        'membres': membres,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a été envoyé avec succès !')
            return redirect('labo:contact')
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})

def temoignages(request):
    temoignages = Temoignage.objects.all().order_by('-date')
    return render(request, 'pages/temoignages.html', {'temoignages': temoignages})

# ----- VUES POUR LES MEMBRES (anciennement membres) -----

def team(request):
    membres = Membre.objects.all()
    themes = Theme.objects.all()
    
    # Filtrer par thème si spécifié
    theme_id = request.GET.get('theme')
    if theme_id:
        membres = membres.filter(theme_id=theme_id)
    
    context = {
        'membres': membres,
        'themes': themes,
        'theme_selectionne': theme_id,
    }
    return render(request, 'core/team.html', context)

def profil_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    presentations = Presentation.objects.filter(membre=membre).order_by('-date_creation')
    
    context = {
        'membre': membre,
        'presentations': presentations,
    }
    return render(request, 'membres/profil.html', context)

@login_required
def edit_profil(request):
    try:
        membre = request.user.profil
    except:
        # Si l'utilisateur n'a pas encore de profil
        membre = Membre(user=request.user)
        membre.save()
    
    if request.method == 'POST':
        form = MembreForm(request.POST, request.FILES, instance=membre)
        if form.is_valid():
            profil = form.save(commit=False)
            if not membre:
                profil.user = request.user
            profil.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('labo:profil', membre_id=profil.id)
    else:
        form = MembreForm(instance=membre)
    
    return render(request, 'membres/edit_profil.html', {'form': form})

# ----- VUES POUR LE BLOG (anciennement blogs) -----

def liste_articles(request):
    articles = Article.objects.filter(est_publie=True).order_by('-date_creation')
    categories = Categorie.objects.all()
    
    context = {
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'blogs/liste.html', context)

def detail_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, est_publie=True)
    
    # Articles connexes
    articles_connexes = Article.objects.filter(
        categories__in=article.categories.all(),
        est_publie=True
    ).exclude(id=article.id).distinct()[:3]
    
    context = {
        'article': article,
        'articles_connexes': articles_connexes
    }
    return render(request, 'blogs/detail.html', context)

def articles_par_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    articles = Article.objects.filter(categories=categorie, est_publie=True).order_by('-date_creation')
    
    context = {
        'categorie': categorie,
        'articles': articles,
    }
    return render(request, 'blogs/par_categorie.html', context)

@login_required
def nouvel_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user.profil
            article.save()
            form.save_m2m()  # Pour sauvegarder les relations ManyToMany
            messages.success(request, 'Votre article a été créé avec succès !')
            return redirect('labo:detail_article', article_id=article.id)
    else:
        form = ArticleForm()
    
    return render(request, 'blogs/formulaire.html', {'form': form, 'action': 'Créer'})

@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    # Vérifier que l'utilisateur est l'auteur
    if request.user.profil != article.auteur:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cet article.")
        return redirect('labo:detail_article', article_id=article.id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre article a été modifié avec succès !')
            return redirect('labo:detail_article', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'blogs/formulaire.html', {'form': form, 'action': 'Modifier', 'article': article})

# ----- VUES POUR LES PRÉSENTATIONS (anciennement presentations) -----

def liste_presentations(request):
    presentations = Presentation.objects.all().order_by('-date_creation')
    themes = Theme.objects.all()
    
    # Filtrer par thème si spécifié
    theme_id = request.GET.get('theme')
    if theme_id:
        presentations = presentations.filter(theme_id=theme_id)
    
    context = {
        'presentations': presentations,
        'themes': themes,
        'theme_selectionne': theme_id,
    }
    return render(request, 'presentations/liste.html', context)

def detail_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    images = ImagePresentation.objects.filter(presentation=presentation)
    
    # Présentations connexes
    presentations_connexes = Presentation.objects.filter(
        theme=presentation.theme
    ).exclude(id=presentation.id)[:3]
    
    context = {
        'presentation': presentation,
        'images': images,
        'presentations_connexes': presentations_connexes
    }
    return render(request, 'presentations/detail.html', context)

@login_required
# Dans labo/views.py, modifiez les fonctions :

@login_required
def nouvelle_presentation(request):
    # Vérifier que l'utilisateur a un profil de membre
    try:
        membre = request.user.profil
    except:
        messages.error(request, "Vous devez d'abord créer votre profil de membre.")
        return redirect('labo:edit_profil')
    
    if request.method == 'POST':
        form = PresentationForm(request.POST, request.FILES)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.membre = membre
            presentation.save()
            
            # Traiter l'image supplémentaire si elle existe
            if 'images_supplementaires' in request.FILES:
                img = request.FILES['images_supplementaires']
                ImagePresentation.objects.create(
                    presentation=presentation,
                    image=img
                )
            
            messages.success(request, 'Votre présentation a été créée avec succès !')
            return redirect('labo:detail_presentation', presentation_id=presentation.id)
    else:
        form = PresentationForm()
    
    return render(request, 'presentations/formulaire.html', {'form': form, 'action': 'Créer'})

@login_required
def edit_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    
    # Vérifier que l'utilisateur est le propriétaire
    if request.user.profil != presentation.membre:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette présentation.")
        return redirect('labo:detail_presentation', presentation_id=presentation.id)
    
    if request.method == 'POST':
        form = PresentationForm(request.POST, request.FILES, instance=presentation)
        if form.is_valid():
            form.save()
            
            # Traiter l'image supplémentaire si elle existe
            if 'images_supplementaires' in request.FILES:
                img = request.FILES['images_supplementaires']
                ImagePresentation.objects.create(
                    presentation=presentation,
                    image=img
                )
            
            messages.success(request, 'Votre présentation a été modifiée avec succès !')
            return redirect('labo:detail_presentation', presentation_id=presentation.id)
    else:
        form = PresentationForm(instance=presentation)
    
    images = ImagePresentation.objects.filter(presentation=presentation)
    
    context = {
        'form': form, 
        'action': 'Modifier', 
        'presentation': presentation,
        'images': images,
    }
    return render(request, 'presentations/formulaire.html', context)
# Fonction pour supprimer une image de présentation
@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ImagePresentation, id=image_id)
    presentation = image.presentation
    
    # Vérifier que l'utilisateur est le propriétaire de la présentation
    if request.user.profil != presentation.membre:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette image.")
        return redirect('labo:detail_presentation', presentation_id=presentation.id)
    
    image.delete()
    messages.success(request, "L'image a été supprimée avec succès.")
    return redirect('labo:edit_presentation', presentation_id=presentation.id)