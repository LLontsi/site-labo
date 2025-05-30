from django.core.management.base import BaseCommand
from django.utils import timezone
from labo.models import Membre, HistoriqueTheme

class Command(BaseCommand):
    help = 'Migre les thèmes existants vers l\'historique'
    
    def handle(self, *args, **options):
        membres_avec_theme = Membre.objects.filter(theme__isnull=False)
        
        for membre in membres_avec_theme:
            # Vérifier si un historique existe déjà
            if not membre.historique_themes.exists():
                HistoriqueTheme.objects.create(
                    membre=membre,
                    theme=membre.theme,
                    date_debut=membre.date_arrivee,
                    description=f"Thème initial : {membre.theme.nom}"
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Historique créé pour {membre} - {membre.theme.nom}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('Migration terminée avec succès!')
        )