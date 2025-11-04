# 🚀 Déploiement Streamlit Cloud - Votre Projet

## Repository GitHub
**Votre repository** : `https://github.com/benpac141/bob_finance.git`

## ✅ Checklist Avant Déploiement

Vérifiez que ces fichiers sont dans votre repository GitHub :

- [ ] `requirements.txt` (avec toutes les dépendances)
- [ ] `scripts/app_simulation_interactive.py` (fichier principal)
- [ ] `scripts/budget_simulator_interactive.py`
- [ ] `src/` (dossier complet avec tous les modules)
- [ ] `config.yaml`
- [ ] `data/` (dossier avec les données)
- [ ] `.streamlit/config.toml` (optionnel mais recommandé)

## 🚀 Déploiement en 3 Étapes

### Étape 1 : Vérifier le Repository (2 minutes)

1. **Allez sur votre repository** : [github.com/benpac141/bob_finance](https://github.com/benpac141/bob_finance)

2. **Vérifiez que tout est présent** :
   - Ouvrez votre repository sur GitHub
   - Vérifiez que tous les fichiers nécessaires sont là
   - Si des fichiers manquent, ajoutez-les :
   ```bash
   cd D:\python_work\bob-enquete
   git add .
   git commit -m "Préparation pour déploiement Streamlit"
   git push origin main
   ```

### Étape 2 : Déployer sur Streamlit Cloud (3 minutes)

1. **Aller sur Streamlit Cloud** :
   - Allez sur **[share.streamlit.io](https://share.streamlit.io)**
   - Cliquez sur **"Sign in"** en haut à droite
   - Connectez-vous avec votre compte **GitHub** (le même que pour le repository)

2. **Créer une nouvelle application** :
   - Cliquez sur **"New app"** (bouton en haut à droite)
   - Remplissez le formulaire :
     - **Repository** : `benpac141/bob_finance`
     - **Branch** : `main` (ou `master` selon votre branche principale)
     - **Main file path** : `scripts/app_simulation_interactive.py`
   - Cliquez sur **"Deploy"**

3. **Attendre le déploiement** :
   - Streamlit va automatiquement :
     - Installer toutes les dépendances depuis `requirements.txt`
     - Lancer votre application
     - Créer une URL publique

### Étape 3 : Partager l'URL (1 minute)

- Une fois le déploiement terminé, vous obtiendrez une URL du type :
  ```
  https://bob-finance.streamlit.app
  ```
  ou
  ```
  https://share.streamlit.io/benpac141/bob_finance/main
  ```

- **Partagez cette URL** avec vos collègues !

## 🔍 Vérification du Déploiement

### Si le déploiement échoue :

1. **Vérifiez les logs** :
   - Dans Streamlit Cloud, cliquez sur votre application
   - Allez dans l'onglet "Logs"
   - Cherchez les erreurs

2. **Erreurs courantes** :

   **❌ "Module not found"** :
   - Vérifiez que toutes les dépendances sont dans `requirements.txt`
   - Ajoutez les modules manquants :
   ```bash
   pip freeze > requirements.txt
   git add requirements.txt
   git commit -m "Mise à jour requirements.txt"
   git push origin main
   ```

   **❌ "File not found"** :
   - Vérifiez que tous les fichiers de données sont dans le repository
   - Vérifiez que les chemins sont relatifs (pas absolus comme `D:\...`)

   **❌ "Import error"** :
   - Vérifiez que tous les modules dans `src/` sont présents
   - Vérifiez que les imports sont corrects

## 📝 Fichiers Importants à Vérifier

### `requirements.txt` doit contenir au minimum :

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
scipy>=1.10.0
openpyxl>=3.1.0
pyyaml>=6.0
reportlab>=4.0.0
kaleido>=0.2.1
```

### Chemins dans le code

Assurez-vous que les chemins sont **relatifs** et non absolus :

✅ **Bon** :
```python
BASE_DIR = Path(__file__).parent.parent
data_path = BASE_DIR / "data" / "raw" / "enquete_all_prepared.xlsx"
```

❌ **Mauvais** :
```python
data_path = "D:\\python_work\\bob-enquete\\data\\raw\\enquete_all_prepared.xlsx"
```

## 🔄 Mises à Jour

Chaque fois que vous modifiez votre code :

1. **Poussez les changements sur GitHub** :
   ```bash
   git add .
   git commit -m "Description des modifications"
   git push origin main
   ```

2. **Streamlit Cloud redéploie automatiquement** !
   - Attendez quelques minutes
   - L'application sera mise à jour automatiquement

## 🔒 Confidentialité

⚠️ **Important** : Avec le plan gratuit de Streamlit Cloud :
- Votre application sera **publique** (accessible à tous avec le lien)
- Le repository GitHub doit être **public** (pour le plan gratuit)

Si vous avez besoin d'une application privée :
- Utilisez Railway ou Render (voir `DEPLOIEMENT_SANS_GITHUB.md`)
- Ou passez à Streamlit Cloud Teams (payant)

## 📊 Configuration Avancée (Optionnel)

### Personnaliser l'URL

Par défaut, l'URL sera `https://[random].streamlit.app`

Pour une URL personnalisée :
- Accédez aux paramètres de votre application dans Streamlit Cloud
- Vous pouvez renommer l'application pour obtenir une URL plus claire

### Variables d'Environnement

Si vous avez besoin de variables d'environnement :

1. Dans Streamlit Cloud, allez dans **Settings** → **Secrets**
2. Ajoutez vos variables :
   ```toml
   [secrets]
   API_KEY = "votre_cle"
   DATABASE_URL = "votre_url"
   ```
3. Dans votre code Python :
   ```python
   import os
   api_key = os.getenv('API_KEY')
   ```

## 🎯 Résumé

**Votre repository** : `benpac141/bob_finance`

**Étapes** :
1. ✅ Vérifier que tout est sur GitHub
2. ✅ Aller sur [share.streamlit.io](https://share.streamlit.io)
3. ✅ Connecter le repository `benpac141/bob_finance`
4. ✅ Spécifier le fichier : `scripts/app_simulation_interactive.py`
5. ✅ Déployer et partager l'URL !

---

## 📞 Besoin d'Aide ?

Si vous rencontrez des problèmes :
1. Consultez les logs dans Streamlit Cloud
2. Vérifiez que tous les fichiers sont présents sur GitHub
3. Vérifiez que `requirements.txt` est complet

**Bon déploiement ! 🚀**

