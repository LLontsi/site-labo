# Image de base officielle Python
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Créer un dossier de travail
WORKDIR /app

# Copier le code source
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Changer de dossier vers l'application Django (labo_informatique)
WORKDIR /app/labo_informatique

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer le serveur avec gunicorn
CMD ["gunicorn", "labo_informatique.wsgi:application", "--bind", "0.0.0.0:8000"]

