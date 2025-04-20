from django.urls import path
from . import views

app_name = 'labo'

urlpatterns = [
    # Pages publiques
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),


    # URL pour la page FAQ
    path('faq/', views.faq_view, name='faq'),  
    
    # Pages Équipe
    path('team/', views.team, name='team'),
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
    path('article/create/', views.create_edit_article, name='create_article'),
    path('article/edit/<int:article_id>/', views.create_edit_article, name='edit_article'),
    path('devenir/edit/', views.create_edit_devenir, name='edit_devenir'),
    
    # Pages administration
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/membres/', views.gestion_membres, name='gestion_membres'),
    path('admin/membre/edit/<int:membre_id>/', views.edit_membre, name='edit_membre'),
    path('admin/invitations/', views.gestion_invitations, name='gestion_invitations'),
    path('admin/invitation/resend/<int:invitation_id>/', views.resend_invitation, name='resend_invitation'),
    path('admin/invitation/cancel/<int:invitation_id>/', views.cancel_invitation, name='cancel_invitation'),
    path('admin/collaborateurs/', views.gestion_collaborateurs, name='gestion_collaborateurs'),
    path('admin/collaborateur/create/', views.create_edit_collaborateur, name='create_collaborateur'),
    path('admin/collaborateur/edit/<int:collaborateur_id>/', views.create_edit_collaborateur, name='edit_collaborateur'),
    path('admin/collaborateur/delete/<int:collaborateur_id>/', views.delete_collaborateur, name='delete_collaborateur'),
    path('admin/contenu/<str:type_contenu>/', views.gestion_contenu, name='gestion_contenu'),
    path('admin/temoignage/create/', views.create_edit_temoignage, name='create_temoignage'),
    path('admin/temoignage/edit/<int:temoignage_id>/', views.create_edit_temoignage, name='edit_temoignage'),
    path('admin/temoignage/delete/<int:temoignage_id>/', views.delete_temoignage, name='delete_temoignage'),
    path('admin/evenement/create/', views.create_edit_evenement, name='create_evenement'),
    path('admin/evenement/edit/<int:evenement_id>/', views.create_edit_evenement, name='edit_evenement'),
    path('admin/evenement/delete/<int:evenement_id>/', views.delete_evenement, name='delete_evenement'),
    
    # Authentification
    path('register/<str:token>/', views.register_with_invitation, name='register_with_invitation'),
]