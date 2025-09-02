### === BUILDER ===
FROM python:3.10-slim AS builder

WORKDIR /install

RUN apt-get update && apt-get install -y --no-install-recommends \
   build-essential \
   gcc \
   libpq-dev \
   && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install/deps -r requirements.txt

### === FINAL IMAGE ===
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /labo-informatique/labo_informatique

COPY --from=builder /install/deps /usr/local
COPY . /labo-informatique

EXPOSE 8000

# Solution finale : créer un script temporaire puis l'exécuter
CMD ["sh", "-c", "sleep 10 && \
    python3 fix_db.py && \
    echo 'Marquage de toutes les migrations comme appliquées...' && \
    python3 manage.py migrate --fake && \
    echo 'Exécution de migrate_themes...' && \
    python3 manage.py migrate_themes && \
    echo 'Démarrage du serveur...' && \
    python3 manage.py runserver 0.0.0.0:8000"]