# 🚀 Déploiement Sans GitHub - Alternatives

Si vous n'avez pas de compte GitHub, voici plusieurs options pour publier votre dashboard gratuitement.

## ✅ Option 1 : Créer un Compte GitHub (5 minutes - RECOMMANDÉ)

Créer un compte GitHub est **gratuit et très simple** :

1. Allez sur [github.com/join](https://github.com/join)
2. Entrez votre email, un mot de passe et un nom d'utilisateur
3. Vérifiez votre email
4. C'est tout ! ✅

**Avantages** :
- ✅ Gratuit et permanent
- ✅ Permet d'utiliser Streamlit Cloud (le plus simple)
- ✅ Utile pour beaucoup d'autres projets
- ✅ Pas besoin de carte bancaire

**Ensuite**, suivez le guide `DEPLOIEMENT_RAPIDE.md`

---

## 🌐 Option 2 : Railway (Sans GitHub)

**Railway** permet de déployer directement depuis votre ordinateur ou depuis Dropbox/Google Drive.

### Méthode 1 : Déploiement Manuel

1. **Créer un compte** sur [railway.app](https://railway.app)
   - Connectez-vous avec Google/GitHub (même sans repo GitHub)

2. **Créer un nouveau projet**
   - Cliquez sur "New Project"
   - Choisissez "Empty Project"

3. **Configurer le déploiement**
   - Dans le projet, cliquez sur "New Service"
   - Sélectionnez "GitHub Repo" OU "Upload from computer"
   - Si vous avez les fichiers, vous pouvez les uploader

4. **Configurer les variables**
   - Ajoutez ces variables d'environnement si nécessaire
   - Le `Procfile` que j'ai créé sera utilisé automatiquement

### Méthode 2 : Utiliser Git (Sans GitHub)

Vous pouvez utiliser Git localement et pousser directement vers Railway :

```bash
# Installer Git (si pas déjà fait)
# Télécharger depuis : https://git-scm.com/downloads

# Dans votre projet
cd D:\python_work\bob-enquete
git init
git add .
git commit -m "Initial commit"

# Railway vous donnera une URL Git unique
# Vous pouvez pousser directement vers Railway
```

---

## 🔧 Option 3 : Render (Sans GitHub)

**Render** permet aussi de déployer sans GitHub.

### Étapes

1. **Créer un compte** sur [render.com](https://render.com)
   - Connectez-vous avec Google/Email

2. **Créer un nouveau Web Service**
   - Cliquez sur "New +" → "Web Service"
   - Utilisez "Public Git repository" OU "Manual Deploy"

3. **Configuration** :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `streamlit run scripts/app_simulation_interactive.py --server.port $PORT --server.address 0.0.0.0`
   - **Environment** : `Python 3`

4. **Uploader vos fichiers**
   - Render permet d'uploader un ZIP de votre projet

---

## 📦 Option 4 : PythonAnywhere (Simple)

**PythonAnywhere** est une plateforme Python hébergée, très simple pour débuter.

### Étapes

1. **Créer un compte gratuit** sur [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Limitations du plan gratuit** :
   - Applications accessibles seulement via sous-domaine : `votre-app.pythonanywhere.com`
   - Application publique uniquement
   - Doit être réactivée tous les 3 mois (clic sur un bouton)

3. **Uploader vos fichiers** :
   - Utilisez l'interface web pour uploader vos fichiers
   - Installez les dépendances via la console Bash

4. **Configurer l'application** :
   - Créez un fichier WSGI pour Streamlit
   - Ou utilisez la console pour lancer Streamlit

### Configuration PythonAnywhere

Créer un fichier `streamlit_app.py` à la racine :

```python
import sys
import os

# Ajouter le chemin du projet
sys.path.insert(0, '/home/VOTRE_USERNAME/bob-enquete')

# Lancer Streamlit
os.system('streamlit run scripts/app_simulation_interactive.py --server.port 8080')
```

---

## 🖥️ Option 5 : ngrok (Accès Local vers Internet)

**ngrok** crée un tunnel sécurisé depuis votre ordinateur vers Internet.

### Avantages
- ✅ Gratuit (avec limitations)
- ✅ Pas besoin de serveur
- ✅ Accès immédiat
- ✅ Fonctionne depuis votre machine

### Limitations
- ⚠️ L'URL change à chaque redémarrage (plan gratuit)
- ⚠️ Votre ordinateur doit être allumé
- ⚠️ Limite de connexions simultanées (plan gratuit)

### Étapes

1. **Télécharger ngrok** : [ngrok.com/download](https://ngrok.com/download)

2. **Créer un compte gratuit** sur ngrok.com

3. **Obtenir votre token** d'authentification

4. **Configurer ngrok** :
```bash
# Installer ngrok
# Windows : télécharger l'exe depuis le site

# Lancer votre application Streamlit localement
cd D:\python_work\bob-enquete
python -m streamlit run scripts/app_simulation_interactive.py

# Dans un autre terminal, lancer ngrok
ngrok http 8501
```

5. **Partager l'URL** :
   - ngrok vous donnera une URL du type : `https://abc123.ngrok.io`
   - Partagez cette URL avec vos collègues

---

## 📊 Comparaison des Solutions Sans GitHub

| Solution | Difficulté | Gratuit | Permanent | Privé |
|----------|------------|---------|-----------|-------|
| **Créer GitHub** | ⭐ Très facile | ✅ | ✅ | ✅ |
| **Railway** | ⭐⭐ Facile | ✅ | ✅ | ✅ |
| **Render** | ⭐⭐ Facile | ✅ | ⚠️ Veille | ✅ |
| **PythonAnywhere** | ⭐⭐⭐ Moyen | ✅ | ⚠️ Réactivation | ✅ |
| **ngrok** | ⭐⭐ Facile | ✅ | ❌ URL change | ✅ |

---

## 🎯 Recommandation

### Pour Vous (Sans GitHub) :

**Option A - La Plus Simple** : Créer un compte GitHub (5 minutes)
- C'est vraiment très simple
- Gratuit et permanent
- Vous permettra d'utiliser Streamlit Cloud (le plus facile)

**Option B - Sans GitHub** : Utiliser Railway
- Créer un compte Railway
- Uploader vos fichiers directement
- Déploiement automatique

**Option C - Solution Temporaire** : Utiliser ngrok
- Parfait pour tester rapidement
- Accès immédiat
- Mais URL change à chaque fois

---

## 🚀 Guide Pas-à-Pas : Railway (Sans GitHub)

### Étape 1 : Préparer le Projet

1. **Zipper votre projet** :
   - Créez un fichier ZIP de `D:\python_work\bob-enquete`
   - Incluez tous les fichiers nécessaires
   - Excluez : `__pycache__`, `venv`, `.git`, `dist`, `build`

### Étape 2 : Créer un Compte Railway

1. Allez sur [railway.app](https://railway.app)
2. Cliquez sur "Start a New Project"
3. Connectez-vous avec Google ou Email

### Étape 3 : Déployer

1. **Créer un nouveau service** :
   - Cliquez sur "New Service"
   - Choisissez "GitHub Repo" (même si vous n'avez pas GitHub, Railway peut créer un repo pour vous)
   - OU choisissez "Deploy from GitHub repo" si vous créez un repo GitHub après

2. **Alternative** : Railway CLI
   - Installez Railway CLI
   - Connectez votre projet
   - Déployez directement

### Étape 4 : Configurer

Railway détectera automatiquement :
- `requirements.txt` → Installera les dépendances
- `Procfile` → Utilisera la commande de démarrage

### Étape 5 : Obtenir l'URL

- Railway vous donnera une URL permanente
- Partagez-la avec vos collègues !

---

## 💡 Astuce : Créer GitHub en 2 Minutes

Si vous voulez vraiment la solution la plus simple :

1. Allez sur [github.com/join](https://github.com/join)
2. Entrez :
   - Email (le vôtre)
   - Mot de passe (choisissez-en un)
   - Nom d'utilisateur (par exemple : `bob-enquete` ou votre nom)
3. Vérifiez votre email
4. C'est tout !

**Aucune carte bancaire nécessaire**, c'est 100% gratuit.

Ensuite, suivez `DEPLOIEMENT_RAPIDE.md` et votre dashboard sera en ligne en 5 minutes supplémentaires !

---

## ❓ Besoin d'Aide ?

Si vous avez des questions sur l'une de ces méthodes, n'hésitez pas à me demander !


