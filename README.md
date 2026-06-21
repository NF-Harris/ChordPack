
# ChordPack 🎸🎹

**ChordPack** est une application web full-stack conçue pour collecter, gérer, nettoyer et afficher des partitions de chansons au format **ChordPro**. L'application intègre un outil de scraping automatisé ainsi qu'un module de correction intelligent basé sur l'IA pour normaliser la mise en page des accords.

---

## 🌍 Déploiement & Disponibilité

L'application est configurée pour être déployée de manière fluide sur **Render**.

> ⏳ **Note sur l'accès à l'application :** > L'application étant hébergée sur l'offre gratuite de Render, les serveurs entrent en veille après une période d'inactivité. Lors de votre première visite, **le chargement initial peut prendre entre 30 secondes et 1 minute** (cumulant le délai de réveil du frontend et le délai de réveil du backend). Merci pour votre patience !

---

## 🚀 Fonctionnalités Clés

* **Scraping de Données Dédié :** Un module robuste intégré directement au backend Django a permis de scraper un site cible de référence, collectant une base initiale de **97 titres** parfaitement fonctionnels.
* **Mise en page Dynamique :** Rendu fluide des grilles d'accords sur le frontend grâce au composant de conversion.
* **Architecture Full-Stack Moderne :** Backend Django REST Framework (DRF) couplé à une interface React réactive et dynamique.

---

## 🤖 Une IA Dédiée au Nettoyage (Pas à la Génération)

> ⚠️ **IMPORTANT – GESTION DES QUOTAS :** > La fonctionnalité de rectification utilise l'offre gratuite de l'API Google Gemini. **Merci de ne pas abuser du bouton "Rectifier"**. 

Dans ChordPack, l'Intelligence Artificielle **ne génère pas d'accords et ne modifie pas la structure musicale** des morceaux. Elle intervient uniquement pour **rectifier les erreurs de mise en page causées par le processus de scraping**.

### Le problème du Scraping :
Lors de l'extraction automatisée depuis le site source, les notations d'accords textuelles se décalent fréquemment, se mélangent aux paroles de manière illisible ou incluent des diagrammes numériques bruts (comme `[x32310]`).

### La solution ChordPack :
En cliquant sur le bouton **Rectifier**, le backend isole le texte brut et demande à l'IA d'appliquer des règles de formatage strictes :
1. **Intégration ChordPro standard :** Insérer proprement les accords au cœur des mots (`tal[Ab]oha`, `vavov[Fm7]ao`).
2. **Nettoyage instrumental :** Nettoyer intégralement les lignes de Solo, d'Intro ou de transitions en enlevant les crochets superflus pour une lecture directe.
3. **Extraction de dictionnaire :** Isoler proprement les diagrammes de dictionnaire d'accords (ex: `C7: x32310`) en début de fichier.

Dès que l'IA a traité le texte, le statut du morceau passe instantanément à `verified: true` : il vous suffit après de rafraîchir la page, rechercher la chanson pour voir le résultat.

---

## 🛠️ Stack Technique

### Backend (Django REST Framework)
* **Django & DRF :** Gestion des API, de l'authentification (JWT), et de la logique métier.
* **BeautifulSoup4 & Requests :** Moteur de scraping interne ayant permis d'extraire les 97 titres initiaux.
* **Google Generative AI :** Tokenisation et requêtage ciblé pour le nettoyage structurel.
* **PostgreSQL + PGVector(bientôt) :** Base de données relationnelle obligatoire pour le stockage (configurable via l'URL de connexion ou directement dans les `settings.py`).
Préparée pour la vectorisation et la recherche via des *embeddings* (dimensions 768) pour permettre une recherche plus intelligente (dans les possible versions futurs).
* **Docker :** Conteneurisation de l'application pour faciliter le déploiement et standardiser l'environnement.

### Frontend (React)
* **React (Vite) :** Interface utilisateur rapide, légère et modulaire.
* **Axios :** Gestion optimisée des requêtes HTTP avec interception des erreurs de quota.

---

## 📦 Installation et Lancement

### Prérequis
* Python 3.10+
* Node.js & npm
* Une base de données PostgreSQL active

---

### Méthode 1 : Lancement en Local

#### 1. Configuration du Backend
1. Rendez-vous dans le dossier backend :
   ```bash
   cd backend

```

2. Créez un environnement virtuel et activez-le :
```bash
python -m venv venv
# Sur Windows:
venv\Scripts\activate
# Sur Linux/macOS:
source venv/bin/activate

```


3. Installez les dépendances adaptées pour le déploiement :
```bash
pip install -r requirements.txt

```


4. Créez un fichier `.env` à la racine du dossier backend et ajoutez vos clés :
```env
SECRET_KEY=ton_secret_django
GEMINI_API_KEY=ta_cle_google_gemini
DATABASE_URL=ton_url_postgres

```


5. Appliquez les migrations, lancez le serveur et remplissez la base de données en scrapant :
```bash
python manage.py migrate
python manage.py runserver
python manage.py scrap

```



#### 2. Configuration du Frontend

1. Rendez-vous dans le dossier frontend :
```bash
cd ../frontend

```


2. Installez les packages :
```bash
npm install

```


3. Lancez l'application en mode développement :
```bash
npm run dev

```



---

### Méthode 2 : Alternative avec Docker 🐳

Si vous préférez ne pas installer Python et Node en local, le projet inclut un `Dockerfile` pour le backend.

1. **Configuration de la Base de Données :**
Avant de lancer le conteneur, assurez-vous d'avoir une base de données **PostgreSQL** active. Vous devez l'associer au projet de deux manières possibles :
* **Option recommandée (.env) :** Renseignez la variable `DATABASE_URL=postgres://user:password@host:port/dbname` dans votre fichier `.env`.
* **Option manuelle (settings.py) :** Modifiez directement le dictionnaire `DATABASES` dans `backend/settings.py` avec vos accès.


2. **Build et Lancement du conteneur :**
```bash
# Build de l'image Docker
docker build -t chordpack-backend ./backend

# Lancement du conteneur avec transfert du fichier .env
docker run -d -p 8000:8000 --env-file ./backend/.env chordpack-backend

```



---

## ⚙️ Configuration Git (Recommandée pour Windows/Render)

Pour éviter les conflits de fins de lignes entre votre environnement de développement Windows (CRLF) et les serveurs Linux de **Render** (LF), activez la configuration automatique de Git avant votre premier commit :

```bash
git config --global core.autocrlf true

```

```

```
