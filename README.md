# Site du Laboratoire d'Informatique

## 📋 Description
Application web Django pour la gestion du laboratoire d'informatique, conteneurisée avec Docker et déployable via GitHub Actions.

## 🚀 Fonctionnalités
- Gestion des utilisateurs et des autorisations
- Base de données PostgreSQL pour le stockage des données
- Interface d'administration Django
- Conteneurisation avec Docker
- Déploiement automatisé avec GitHub Actions
- Configuration Nginx pour le reverse proxy

## 🛠 Prérequis
- Docker 20.10+
- Docker Compose 1.29+
- Python 3.8+
- PostgreSQL 15 (géré via Docker)

## 🚀 Installation ZAZ

### 1. Cloner le dépôt
```bash
git clone https://github.com/lontsi/site-labo.git
cd site-labo
```

### 2. Configuration de l'environnement
Créer un fichier `.env` à la racine du projet avec les variables d'environnement nécessaires :
```
POSTGRES_DB=labo_informatique_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

### 3. Démarrer les services avec Docker Compose
```bash
docker-compose up -d
```

Les services seront accessibles aux adresses suivantes :
- Application : http://localhost:8022
- Base de données PostgreSQL : localhost:54321

## 🔧 Configuration

### Base de données
La configuration de la base de données est gérée dans `docker-compose.yml`. Une sauvegarde initiale est chargée automatiquement depuis `dump_labo_informatique.sql`.

### Nginx
Le fichier de configuration Nginx se trouve dans `deploy_config/nginx.conf`. Il est configuré pour :
- Rediriger le trafic HTTP vers HTTPS (commenté par défaut)
- Configurer le reverse proxy vers l'application Django
- Gérer les en-têtes HTTP nécessaires

## 🚀 Déploiement

### Déploiement manuel
1. Construire l'image Docker :
```bash
docker-compose build
```

2. Démarrer les services :
```bash
docker-compose up -d
```

### Déploiement automatisé
Le déploiement est configuré via GitHub Actions (`.github/workflows/deploy.yml`). Pour activer le déploiement automatique :
1. Configurer les secrets dans les paramètres du dépôt GitHub :
   - `SERVER_IP` : Adresse IP du serveur de production
   - `SSH_USER` : Utilisateur SSH pour la connexion
   - `SSH_PRIVATE_KEY` : Clé privée SSH pour l'authentification

2. Pousser les modifications sur la branche `Deployment` pour déclencher le déploiement.

## 📂 Structure du projet
```
site-labo/
├── .github/                 # Configuration GitHub Actions
│   └── workflows/
│       └── deploy.yml      # Workflow de déploiement
├── deploy_config/           # Fichiers de configuration pour le déploiement
│   └── nginx.conf          # Configuration Nginx
├── labo_informatique/       # Projet Django principal
├── docker-compose.yml       # Configuration Docker Compose
├── Dockerfile              # Configuration de l'image Docker
├── requirements.txt        # Dépendances Python
└── dump_labo_informatique.sql # Dump initial de la base de données
```

## 🔒 Sécurité
- Les mots de passe et informations sensibles doivent être gérés via des variables d'environnement
- La configuration HTTPS est commentée dans le fichier Nginx et peut être activée en production
- L'accès à l'interface d'administration Django est protégé par authentification

## 🤝 Contribution
1. Créer une branche pour votre fonctionnalité : `git checkout -b feature/nouvelle-fonctionnalite`
2. Committer vos modifications : `git commit -m 'Ajouter une nouvelle fonctionnalité'`
3. Pousser la branche : `git push origin feature/nouvelle-fonctionnalite`
4. Créer une Pull Request

## 📝 Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
le site du labo

Le readme final sera mis a jour lorsque l'implementation sera termine.
