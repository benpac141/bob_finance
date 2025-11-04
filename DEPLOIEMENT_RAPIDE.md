# 🚀 Déploiement Rapide - Dashboard BOB

## 📦 Votre Repository GitHub
**Repository** : `https://github.com/benpac141/bob_finance.git`

## Méthode la Plus Simple : Streamlit Community Cloud

### En 3 Étapes (5 minutes)

#### 1️⃣ Vérifier GitHub (1 minute)

Vérifiez que votre repository contient tous les fichiers nécessaires :
- ✅ `requirements.txt`
- ✅ `scripts/app_simulation_interactive.py`
- ✅ `scripts/budget_simulator_interactive.py`
- ✅ `src/` (dossier complet)
- ✅ `config.yaml`
- ✅ `data/` (dossier avec les données)

Si des fichiers manquent, ajoutez-les :
```bash
cd D:\python_work\bob-enquete
git add .
git commit -m "Ajout des fichiers pour déploiement"
git push origin main
```

⚠️ **Important** : Le repository doit être **PUBLIC** pour la version gratuite de Streamlit Cloud.

#### 2️⃣ Déployer sur Streamlit Cloud (2 minutes)

1. Allez sur **[share.streamlit.io](https://share.streamlit.io)**
2. Connectez-vous avec votre compte **GitHub** (benpac141)
3. Cliquez sur **"New app"**
4. Remplissez :
   - **Repository** : `benpac141/bob_finance`
   - **Branch** : `main` (ou `master` selon votre branche)
   - **Main file path** : `scripts/app_simulation_interactive.py`
5. Cliquez sur **"Deploy"**

#### 3️⃣ Attendre et Partager (2 minutes)

- Streamlit installe automatiquement les dépendances depuis `requirements.txt`
- Votre application sera disponible à une URL du type : `https://[votre-app].streamlit.app`
- Partagez cette URL avec vos collègues !

🎉 **C'est tout ! Votre dashboard est maintenant en ligne !**

---

## ✅ Vérifications Avant Déploiement

- [ ] `requirements.txt` est présent et à jour
- [ ] Les fichiers de données sont dans le repository (ou accessibles)
- [ ] Le fichier principal est : `scripts/app_simulation_interactive.py`
- [ ] Les chemins dans le code sont relatifs (pas absolus)

---

## 📚 Documentation Complète

Pour plus de détails, consultez **`GUIDE_DEPLOIEMENT.md`**

---

## 🔗 Alternatives Gratuites

- **Railway** : [railway.app](https://railway.app) (plan gratuit avec crédit)
- **Render** : [render.com](https://render.com) (plan gratuit avec veille)

---

**Bon déploiement ! 🎉**

