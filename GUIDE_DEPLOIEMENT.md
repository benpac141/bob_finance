# Guide de Déploiement - Dashboard BOB en Ligne

Ce guide explique comment publier votre dashboard Streamlit gratuitement sur Internet pour le partager avec vos collègues ou le public.

## 🚀 Option 1 : Streamlit Community Cloud (RECOMMANDÉ)

**Streamlit Community Cloud** est la solution officielle, gratuite et la plus simple pour héberger des applications Streamlit.

### Avantages
- ✅ **100% gratuit** (sans limite de temps)
- ✅ **Configuration minimale** (quelques clics)
- ✅ **Déploiement automatique** depuis GitHub
- ✅ **URL publique** permanente
- ✅ **SSL/HTTPS** inclus
- ✅ **Mises à jour automatiques** à chaque commit

### Prérequis
1. Un compte **GitHub** (gratuit) - [Créer un compte](https://github.com/join)
2. Votre projet sur GitHub (ou créer un nouveau repository)

### Étapes de Déploiement

#### Étape 1 : Préparer le Projet pour GitHub

1. **Créer un fichier `.streamlit/config.toml`** (optionnel, pour la configuration) :
```bash
mkdir .streamlit
```

2. **Vérifier que votre projet est prêt** :
   - ✅ `requirements.txt` à jour
   - ✅ Fichier principal : `scripts/app_simulation_interactive.py`
   - ✅ Toutes les données nécessaires présentes

#### Étape 2 : Créer un Repository GitHub

1. **Créer un nouveau repository sur GitHub** :
   - Allez sur [github.com](https://github.com)
   - Cliquez sur "New repository"
   - Nom : `bob-enquete` (ou autre)
   - Visibilité : **Public** (requis pour la version gratuite de Streamlit Cloud)
   - Cochez "Initialize with README"

2. **Connecter votre projet local à GitHub** :
```bash
cd D:\python_work\bob-enquete
git init
git add .
git commit -m "Initial commit - Dashboard BOB"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/bob-enquete.git
git push -u origin main
```

#### Étape 3 : Déployer sur Streamlit Cloud

1. **Aller sur Streamlit Cloud** :
   - Allez sur [share.streamlit.io](https://share.streamlit.io)
   - Connectez-vous avec votre compte GitHub

2. **Créer une nouvelle application** :
   - Cliquez sur "New app"
   - Sélectionnez votre repository : `bob-enquete`
   - Sélectionnez la branche : `main`
   - **Main file path** : `scripts/app_simulation_interactive.py`
   - Cliquez sur "Deploy"

3. **Attendre le déploiement** :
   - Streamlit va installer toutes les dépendances
   - L'application sera disponible à une URL du type : `https://votre-app.streamlit.app`

### ⚠️ Points Importants

#### Fichiers à Inclure dans GitHub

Assurez-vous que ces fichiers sont dans le repository :
- ✅ `requirements.txt`
- ✅ `config.yaml`
- ✅ `scripts/app_simulation_interactive.py`
- ✅ `scripts/budget_simulator_interactive.py`
- ✅ `src/` (dossier complet)
- ✅ `data/` (dossier complet avec les données)

#### Fichiers à Exclure (via .gitignore)

- ❌ `__pycache__/`
- ❌ `outputs/` (si volumineux)
- ❌ `.env` (fichiers de secrets)
- ❌ Fichiers temporaires

#### Taille des Fichiers

- **Limite GitHub** : 100 Mo par fichier
- **Limite Streamlit Cloud** : 1 Go par application
- Si vos données sont volumineuses, utilisez Git LFS ou stockez-les ailleurs

### Configuration Avancée (Optionnel)

Créer un fichier `.streamlit/config.toml` pour personnaliser l'application :

```toml
[theme]
primaryColor = "#1f4788"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

---

## 🌐 Option 2 : Railway (Alternative Gratuite)

**Railway** offre également un plan gratuit avec des limites généreuses.

### Avantages
- ✅ Plan gratuit (500$ de crédit/mois)
- ✅ Déploiement simple depuis GitHub
- ✅ Support de variables d'environnement
- ✅ Logs en temps réel

### Étapes

1. **Créer un compte** sur [railway.app](https://railway.app)

2. **Créer un fichier `Procfile`** :
```
web: streamlit run scripts/app_simulation_interactive.py --server.port $PORT --server.address 0.0.0.0
```

3. **Créer un fichier `runtime.txt`** (optionnel) :
```
python-3.11.0
```

4. **Connecter GitHub** et déployer automatiquement

---

## 🔧 Option 3 : Render (Alternative Gratuite)

**Render** offre un plan gratuit avec certaines limitations.

### Avantages
- ✅ Plan gratuit disponible
- ✅ Déploiement depuis GitHub
- ⚠️ L'application se met en veille après 15 min d'inactivité (plan gratuit)

### Étapes

1. **Créer un compte** sur [render.com](https://render.com)

2. **Créer un "Web Service"** :
   - Connectez votre repository GitHub
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `streamlit run scripts/app_simulation_interactive.py --server.port $PORT --server.address 0.0.0.0`
   - **Environment** : `Python 3`

3. **Déployer** et obtenir votre URL

---

## 📋 Checklist de Déploiement

Avant de déployer, vérifiez :

- [ ] **requirements.txt** est à jour avec toutes les dépendances
- [ ] Les **chemins de fichiers** sont relatifs (pas de chemins absolus)
- [ ] Les **données** sont incluses dans le repository (ou accessibles)
- [ ] Le **fichier principal** est correctement identifié
- [ ] Les **imports** fonctionnent correctement
- [ ] Le **.gitignore** exclut les fichiers inutiles

## 🔒 Sécurité et Confidentialité

### Données Sensibles

Si votre application contient des données sensibles :

1. **Ne pas** mettre les données sensibles dans le repository
2. Utiliser des **variables d'environnement** :
   ```python
   import os
   API_KEY = os.getenv('API_KEY', 'default_value')
   ```
3. Configurer les secrets dans Streamlit Cloud :
   - Settings → Secrets → Ajouter vos variables

### Accès Public vs Privé

- **Streamlit Cloud Gratuit** : Applications publiques uniquement
- **Streamlit Cloud Teams** (payant) : Applications privées
- **Railway/Render** : Permettent des applications privées même en gratuit

## 🐛 Dépannage

### Problème : Application ne démarre pas

**Solutions** :
1. Vérifier les logs dans Streamlit Cloud
2. Vérifier que `requirements.txt` contient toutes les dépendances
3. Vérifier que le chemin du fichier principal est correct

### Problème : Données non trouvées

**Solutions** :
1. Vérifier que les fichiers de données sont dans le repository
2. Utiliser des chemins relatifs (pas absolus)
3. Vérifier les permissions des fichiers

### Problème : Application trop lente

**Solutions** :
1. Optimiser le chargement des données (cache Streamlit)
2. Réduire la taille des fichiers de données
3. Utiliser des fichiers compressés si nécessaire

## 📊 Comparaison des Solutions

| Solution | Gratuit | Privé | Déploiement | Limites |
|----------|---------|-------|-------------|---------|
| **Streamlit Cloud** | ✅ | ❌ (public uniquement) | ⭐⭐⭐⭐⭐ | 1 Go |
| **Railway** | ✅ (500$/mois crédit) | ✅ | ⭐⭐⭐⭐ | Limites douces |
| **Render** | ✅ | ⚠️ (payant) | ⭐⭐⭐⭐ | Veille après 15 min |

## 🎯 Recommandation Finale

Pour votre cas d'usage (dashboard BOB pour collègues) :

**👉 Utilisez Streamlit Community Cloud** :
- Le plus simple
- Le plus rapide à déployer
- Gratuit et sans limite de temps
- Parfait pour partager avec des collègues

---

## 📞 Support

- **Streamlit Cloud Docs** : [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- **GitHub Issues** : En cas de problème, créez une issue sur votre repository

---

**Bon déploiement ! 🚀**


