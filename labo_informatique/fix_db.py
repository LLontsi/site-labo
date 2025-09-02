import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labo_informatique.settings')
django.setup()
from django.db import connection

cursor = connection.cursor()

# Ajouter les colonnes manquantes à labo_membre
try:
    cursor.execute('ALTER TABLE labo_membre ADD COLUMN IF NOT EXISTS profil_valide BOOLEAN DEFAULT FALSE')
    print('profil_valide ajouté')
except Exception as e:
    print(f'profil_valide: {e}')

try:
    cursor.execute('ALTER TABLE labo_membre ADD COLUMN IF NOT EXISTS date_validation_profil TIMESTAMP NULL')
    print('date_validation_profil ajouté')
except Exception as e:
    print(f'date_validation_profil: {e}')

try:
    cursor.execute('ALTER TABLE labo_membre ADD COLUMN IF NOT EXISTS validateur_profil_id INTEGER NULL')
    print('validateur_profil_id ajouté')
except Exception as e:
    print(f'validateur_profil_id: {e}')

# Créer la table de liaison Many-to-Many pour les thèmes
try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS labo_membre_themes (
            id SERIAL PRIMARY KEY,
            membre_id INTEGER NOT NULL REFERENCES labo_membre(id) ON DELETE CASCADE,
            theme_id INTEGER NOT NULL REFERENCES labo_theme(id) ON DELETE CASCADE,
            UNIQUE(membre_id, theme_id)
        )
    ''')
    print('Table labo_membre_themes créée')
except Exception as e:
    print(f'labo_membre_themes: {e}')

# Créer les index pour optimiser les performances
try:
    cursor.execute('CREATE INDEX IF NOT EXISTS labo_membre_themes_membre_id_idx ON labo_membre_themes(membre_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS labo_membre_themes_theme_id_idx ON labo_membre_themes(theme_id)')
    print('Index créés pour labo_membre_themes')
except Exception as e:
    print(f'Index: {e}')

print('Toutes les tables et colonnes vérifiées/ajoutées')