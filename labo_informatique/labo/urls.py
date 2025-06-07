from django.urls import path
from . import views

app_name = 'labo'

urlpatterns = [
    # Pages publiques
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Pages Équipe
    path('team/', views.team, name='team'),
    path('faq/', views.faq, name='faq'),
    path('membre/<int:membre_id>/', views.membre_detail, name='membre_detail'),
    path('responsables/', views.responsables, name='responsables'),
    
    # Pages Blog
    path('blog/', views.liste_articles, name='liste_articles'),
    path('blog/categorie/<int:categorie_id>/', views.liste_articles_par_categorie, name='liste_articles_par_categorie'),
    path('blog/theme/<int:theme_id>/', views.liste_articles_par_theme, name='liste_articles_par_theme'),
    path('blog/article/<int:article_id>/', views.article_detail, name='article_detail'),
    
    # Pages Présentations
    path('presentations/', views.liste_presentations, name='liste_presentations'),
    path('presentation/<int:presentation_id>/', views.presentation_detail, name='presentation_detail'),
    
    # Page Devenir des membres
    path('devenir-membres/', views.devenir_membres, name='devenir_membres'),
    
    # Pages membres connectés
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('presentation/create/', views.create_edit_presentation, name='create_presentation'),
    path('presentation/edit/<int:presentation_id>/', views.create_edit_presentation, name='edit_presentation'),
    path('presentation/delete/<int:presentation_id>/',views.delete_presentation, name='delete_presentation'),
    path('article/create/', views.create_edit_article, name='create_article'),
    path('article/edit/<int:article_id>/', views.create_edit_article, name='edit_article'),
    path('article/delete/<int:article_id>/', views.delete_article, name='delete_article'),
    path('devenir/edit/', views.create_edit_devenir, name='edit_devenir'),
    
    # Pages administration
    path('gestion/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('gestion/membres/', views.gestion_membres, name='gestion_membres'),
    path('gestion/membre/create/', views.create_membre, name='create_membre'),
    path('gestion/membre/edit/<int:membre_id>/', views.edit_membre, name='edit_membre'),
    path('gestion/invitations/', views.gestion_invitations, name='gestion_invitations'),
    path('gestion/invitation/resend/<int:invitation_id>/', views.resend_invitation, name='resend_invitation'),
    path('gestion/invitation/cancel/<int:invitation_id>/', views.cancel_invitation, name='cancel_invitation'),
    path('gestion/collaborateurs/', views.gestion_collaborateurs, name='gestion_collaborateurs'),
    path('gestion/collaborateur/create/', views.create_edit_collaborateur, name='create_collaborateur'),
    path('gestion/collaborateur/edit/<int:collaborateur_id>/', views.create_edit_collaborateur, name='edit_collaborateur'),
    path('gestion/collaborateur/delete/<int:collaborateur_id>/', views.delete_collaborateur, name='delete_collaborateur'),
    path('gestion/contenu/<str:type_contenu>/', views.gestion_contenu, name='gestion_contenu'),
    path('gestion/temoignage/create/', views.create_edit_temoignage, name='create_temoignage'),
    path('gestion/presentation/create/', views.create_edit_presentation1, name='create_presentation1'),
    # Ajoutez cette ligne après la ligne create_presentation1
    path('gestion/presentation/edit/<int:presentation_id>/', views.create_edit_presentation1, name='edit_presentation1'),
    path('gestion/article/create/', views.create_edit_article1, name='create_article1'),
    path('gestion/temoignage/edit/<int:temoignage_id>/', views.create_edit_temoignage, name='edit_temoignage'),
    path('gestion/temoignage/delete/<int:temoignage_id>/', views.delete_temoignage, name='delete_temoignage'),
    path('gestion/evenement/create/', views.create_edit_evenement, name='create_evenement'),
    path('gestion/evenement/edit/<int:evenement_id>/', views.create_edit_evenement, name='edit_evenement'),
    path('gestion/evenement/delete/<int:evenement_id>/', views.delete_evenement, name='delete_evenement'),
    path('gestion/themes/', views.gestion_themes, name='gestion_themes'),
    path('gestion/theme/create/', views.create_edit_theme, name='create_theme'),
    path('gestion/theme/edit/<int:theme_id>/', views.create_edit_theme, name='edit_theme'),
    path('gestion/theme/delete/', views.delete_theme, name='delete_theme'),
        # URLs pour la gestion des catégories
    path('gestion/categories/', views.gestion_categories, name='gestion_categories'),
    path('gestion/categorie/create/', views.create_edit_categorie, name='create_categorie'),
    path('gestion/categorie/edit/<int:categorie_id>/', views.create_edit_categorie, name='edit_categorie'),
    path('gestion/categorie/delete/', views.delete_categorie, name='delete_categorie'),
    path('gestion/membres/delete/<int:membre_id>/', views.delete_membres, name='delete_membres'),
        # Validation des articles
    path('gestion/article/valider/<int:article_id>/', views.valider_article, name='valider_article'),
    path('gestion/articles/en-attente/', views.articles_en_attente, name='articles_en_attente'),
    
    # Pour les présentations
    path('gestion/presentation/delete/<int:presentation_id>/', views.delete_presentation, name='delete_presentation'),

    # Pour les articles
    path('gestion/article/delete/<int:article_id>/', views.delete_article, name='delete_article'),
            # Authentification
    path('register/<str:token>/', views.register_with_invitation, name='register_with_invitation'),
    
    # Pages Projets
    path('projets/', views.liste_projets, name='liste_projets'),
    path('projet/<int:projet_id>/', views.projet_detail, name='projet_detail'),
    # Ajoutez cette ligne dans urlpatterns :
    path('gestion/presentation/valider-fichier/<int:presentation_id>/', views.valider_fichier_presentation, name='valider_fichier_presentation'),
    # Administration des projets
    path('gestion/gestion-projets/', views.gestion_projets, name='gestion_projets'),
    path('gestion/projet/create/', views.create_edit_projet, name='create_projet'),
    path('gestion/projet/edit/<int:projet_id>/', views.create_edit_projet, name='edit_projet'),
    path('gestion/projet/delete/<int:projet_id>/', views.delete_projet, name='delete_projet'),
    
    # Dans urlpatterns, ajoutez ces lignes après vos URLs d'administration existantes :

    # Gestion des historiques de thèmes
    path('gestion/historique-themes/', views.gestion_historique_themes, name='gestion_historique_themes'),
    path('gestion/historique-theme/create/', views.create_edit_historique_theme, {'membre_id': None}, name='create_historique_theme_general'),
     path('gestion/historique-theme/create/<int:membre_id>/', views.create_edit_historique_theme, name='create_historique_theme'),
     path('gestion/historique-theme/edit/<int:historique_id>/', views.create_edit_historique_theme, name='edit_historique_theme'),
    path('gestion/historique-theme/delete/<int:historique_id>/', views.delete_historique_theme, name='delete_historique_theme'),
]