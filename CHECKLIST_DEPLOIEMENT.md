# ✅ Checklist de Déploiement - bob_finance

## Votre Repository
**GitHub** : `https://github.com/benpac141/bob_finance.git`

## 📋 Vérifications Avant Déploiement

Avant de déployer sur Streamlit Cloud, vérifiez que ces éléments sont présents dans votre repository GitHub :

### Fichiers Obligatoires

- [ ] **`requirements.txt`** - Contient toutes les dépendances nécessaires
- [ ] **`scripts/app_simulation_interactive.py`** - Fichier principal de l'application
- [ ] **`scripts/budget_simulator_interactive.py`** - Module de calcul
- [ ] **`config.yaml`** - Fichier de configuration
- [ ] **`src/`** - Dossier complet avec tous les modules Python
  - [ ] `src/raking.py`
  - [ ] `src/analysis.py`
  - [ ] `src/utils.py`
  - [ ] Autres modules nécessaires

### Données

- [ ] **`data/`** - Dossier avec les données
  - [ ] `data/raw/enquete_all_prepared.xlsx`
  - [ ] `data/margins/margins_center.csv`

### Fichiers Optionnels (Recommandés)

- [ ] **`.streamlit/config.toml`** - Configuration Streamlit
- [ ] **`README.md`** - Documentation du projet

## 🔍 Vérification sur GitHub

1. Allez sur [github.com/benpac141/bob_finance](https://github.com/benpac141/bob_finance)
2. Vérifiez que tous les fichiers ci-dessus sont présents
3. Si des fichiers manquent, ajoutez-les localement puis poussez sur GitHub

## 🚀 Commande pour Ajouter les Fichiers Manquants

```bash
cd D:\python_work\bob-enquete

# Vérifier l'état
git status

# Ajouter tous les fichiers
git add .

# Commit
git commit -m "Préparation pour déploiement Streamlit Cloud"

# Pousser sur GitHub
git push origin main
```

## ⚠️ Points Importants

### Visibilité du Repository

- **Public** : Requis pour Streamlit Cloud gratuit
- **Private** : Nécessite Streamlit Cloud Teams (payant)

### Chemins dans le Code

Vérifiez que tous les chemins sont **relatifs** :

✅ **Bon** :
```python
BASE_DIR = Path(__file__).parent.parent
data_path = BASE_DIR / "data" / "raw" / "fichier.xlsx"
```

❌ **Mauvais** :
```python
data_path = "D:\\python_work\\bob-enquete\\data\\fichier.xlsx"
```

### Taille des Fichiers

- **Limite GitHub** : 100 Mo par fichier
- Si vos données sont volumineuses, utilisez Git LFS ou stockez-les ailleurs

## ✅ Une fois Tout Vérifié

Suivez le guide **`DEPLOIEMENT_VOTRE_PROJET.md`** pour déployer sur Streamlit Cloud !

---

**Bon déploiement ! 🚀**

