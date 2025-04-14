# labo/urls.py
from django.urls import path
from . import views

app_name = 'labo'

urlpatterns = [
    # Pages principales (anciennement core)
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('temoignages/', views.temoignages, name='temoignages'),
    
    # Membres (anciennement membres)
    path('team/', views.team, name='team'),
    path('profil/<int:membre_id>/', views.profil_membre, name='profil'),
    path('profil/edit/', views.edit_profil, name='edit_profil'),
    
    # Blog (anciennement blogs)
    path('blog/', views.liste_articles, name='liste_articles'),
    path('blog/article/<int:article_id>/', views.detail_article, name='detail_article'),
    path('blog/categorie/<int:categorie_id>/', views.articles_par_categorie, name='articles_par_categorie'),
    path('blog/nouveau/', views.nouvel_article, name='nouvel_article'),
    path('blog/edit/<int:article_id>/', views.edit_article, name='edit_article'),
    
    # Présentations (anciennement presentations)
    path('presentations/', views.liste_presentations, name='liste_presentations'),
    path('presentations/detail/<int:presentation_id>/', views.detail_presentation, name='detail_presentation'),
    path('presentations/nouvelle/', views.nouvelle_presentation, name='nouvelle_presentation'),
    path('presentations/edit/<int:presentation_id>/', views.edit_presentation, name='edit_presentation'),
]