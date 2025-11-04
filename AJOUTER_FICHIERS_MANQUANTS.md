# 🚀 Commandes pour Ajouter les Fichiers Manquants

## Commandes à Exécuter

```powershell
cd D:\python_work\bob-enquete

# Ajouter les fichiers modifiés et les nouveaux fichiers importants
git add .gitignore
git add requirements.txt
git add scripts/app_simulation_interactive.py
git add scripts/budget_simulator_interactive.py

# Ajouter la configuration Streamlit (important pour le déploiement)
git add .streamlit/

# Ajouter le fichier de configuration (si pas déjà présent)
git add config.yaml

# Ajouter les fichiers de documentation utiles
git add README.md
git add Procfile
git add CHECKLIST_DEPLOIEMENT.md
git add DEPLOIEMENT_RAPIDE.md
git add DEPLOIEMENT_VOTRE_PROJET.md

# Vérifier l'état avant de commit
git status

# Commit
git commit -m "Ajout des fichiers nécessaires pour déploiement Streamlit Cloud"

# Push
git push origin master
```

## 🔍 Vérification Rapide

Pour vérifier ce qui est déjà sur GitHub :

```powershell
# Voir les fichiers suivis par Git
git ls-files

# Voir si src/ est présent
git ls-files src/

# Voir si config.yaml est présent
git ls-files config.yaml
```

## 📋 Fichiers Essentiels à Vérifier

Vérifiez sur GitHub que ces fichiers sont présents :

### Code
- ✅ `scripts/app_simulation_interactive.py`
- ✅ `scripts/budget_simulator_interactive.py`
- ✅ `src/raking.py`
- ✅ `src/analysis.py`
- ✅ `src/utils.py`
- ✅ Tous les autres fichiers dans `src/`

### Configuration
- ✅ `requirements.txt`
- ✅ `config.yaml`
- ✅ `.streamlit/config.toml`

### Données
- ✅ `data/margins/margins_center.csv`
- ✅ `data/raw/enquete_all_prepared.xlsx` (via LFS)

---

## 🎯 Action Immédiate

Exécutez ces commandes dans PowerShell :

```powershell
cd D:\python_work\bob-enquete
git add .
git status
# Vérifiez que tout est bien ajouté
git commit -m "Mise à jour complète pour déploiement Streamlit Cloud"
git push origin master
```

---

**Après le push, vérifiez sur GitHub que tout est présent ! ✅**

