# --- Base image avec Python 3.11 ---
FROM python:3.11-slim

# --- Installer dépendances système utiles ---
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# --- Créer le répertoire de l'application ---
WORKDIR /app

# --- Copier les fichiers requirements ---
COPY requirements.txt .

# --- Installer pip et les dépendances Python ---
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# --- Copier le reste du projet ---
COPY . .

# --- Exposer le port de l'application ---
EXPOSE 5000

# --- Commande par défaut pour lancer l'application ---
CMD ["python", "main.py"]

