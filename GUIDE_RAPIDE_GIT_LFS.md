# 🚀 Solution Rapide : Données Volumineuses sur GitHub

## ✅ Solution Recommandée : Git LFS

**Git LFS** (Large File Storage) permet de stocker les gros fichiers séparément.

### Étapes Rapides (5 minutes)

#### 1️⃣ Installer Git LFS

1. Téléchargez depuis : [git-lfs.github.com](https://git-lfs.github.com)
2. Installez-le (suivez les instructions d'installation)
3. Vérifiez l'installation :
   ```bash
   git lfs version
   ```

#### 2️⃣ Configurer Git LFS dans votre Projet

```bash
cd D:\python_work\bob-enquete

# Initialiser Git LFS
git lfs install

# Dire à Git LFS de gérer les fichiers volumineux
git lfs track "data/**/*.xlsx"
git lfs track "data/**/*.csv"
git lfs track "data/base-ic-evol-struct-pop-2022_csv/**"

# Ajouter le fichier .gitattributes créé
git add .gitattributes
git commit -m "Configuration Git LFS pour les fichiers volumineux"
```

#### 3️⃣ Ajouter les Données

```bash
# Ajouter les fichiers de données (ils seront stockés via LFS)
git add data/
git commit -m "Ajout des données avec Git LFS"
git push origin main
```

---

## 📋 Alternative : Exclure les Données Volumineuses

Si Git LFS ne convient pas, vous pouvez exclure les fichiers les plus volumineux.

### Ce qui est Maintenant Exclu (dans .gitignore)

- ❌ `data/base-ic-evol-struct-pop-2022_csv/` (dossier INSEE volumineux)
- ❌ `data/raw/*.xlsx` (fichiers Excel bruts)
- ❌ `data/raw/*.csv` (fichiers CSV bruts)

### Ce qui est Conservé (si nécessaire)

- ✅ `data/margins/margins_center.csv` (fichier essentiel pour l'application)
- ✅ `data/iris_besancon_list.csv` (si nécessaire)

### Modifier le Code pour les Données Manquantes

Si vous excluez les données, vous avez deux options :

#### Option A : Créer un Fichier de Données Minimal

Créer un script `scripts/create_minimal_data.py` :

```python
"""
Crée une version minimale des données pour le déploiement.
"""
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Charger les données complètes (localement)
df_full = pd.read_excel(BASE_DIR / "data" / "raw" / "enquete_all_prepared.xlsx")

# Créer un échantillon (par exemple, 10% des données)
df_sample = df_full.sample(frac=0.1, random_state=42)

# Sauvegarder comme données minimales
output_path = BASE_DIR / "data" / "raw" / "enquete_all_prepared.minimal.xlsx"
df_sample.to_excel(output_path, index=False)

print(f"✅ Données minimales créées : {output_path}")
print(f"   Taille originale : {len(df_full)} lignes")
print(f"   Taille minimale : {len(df_sample)} lignes")
```

Puis modifier `budget_simulator_interactive.py` :

```python
# Au lieu de :
DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_all_prepared.xlsx"

# Utiliser :
DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_all_prepared.minimal.xlsx"
```

#### Option B : Télécharger depuis Google Drive

Voir `SOLUTION_DONNEES_VOLUMINEUSES.md` pour les détails complets.

---

## 🎯 Recommandation pour Votre Cas

### Fichiers Probablement Volumineux

D'après votre structure, ces fichiers sont probablement volumineux :
- `data/base-ic-evol-struct-pop-2022_csv/base-ic-evol-struct-pop-2022.CSV` (dossier INSEE)
- `data/raw/enquete_all_prepared.xlsx`
- `data/raw/enquete_bob.xlsx`
- `data/raw/enquete_prepared.xlsx`

### Solution Immédiate

**Option 1 - Git LFS (Recommandé)** :
1. Installez Git LFS
2. Configurez-le pour suivre les fichiers Excel/CSV
3. Poussez vos données normalement

**Option 2 - Exclure les Données Volumineuses** :
1. Le `.gitignore` a été mis à jour pour exclure les gros fichiers
2. Créez une version minimale des données pour Streamlit Cloud
3. Gardez les données complètes localement

---

## ⚡ Action Immédiate

### Si vous voulez déployer rapidement :

1. **Installez Git LFS** : [git-lfs.github.com](https://git-lfs.github.com)

2. **Dans PowerShell** :
```powershell
cd D:\python_work\bob-enquete
git lfs install
git lfs track "data/**/*.xlsx"
git lfs track "data/**/*.csv"
git add .gitattributes
git add data/
git commit -m "Ajout des données avec Git LFS"
git push origin main
```

3. **C'est tout !** Vos données seront sur GitHub via LFS.

---

## 📊 Vérifier la Taille des Fichiers

Pour voir la taille de vos fichiers :

```powershell
cd D:\python_work\bob-enquete\data
Get-ChildItem -Recurse -File | Select-Object Name, @{Name='Size(MB)';Expression={[math]::Round($_.Length / 1MB, 2)}} | Sort-Object 'Size(MB)' -Descending
```

---

## ❓ Besoin d'Aide ?

Si vous avez des questions ou si vous préférez une autre solution, dites-moi :
- La taille totale de votre dossier `data/`
- Si vous préférez Git LFS ou exclure les données
- Si vous avez besoin d'aide pour configurer Git LFS

**Une fois résolu, vous pourrez déployer sur Streamlit Cloud ! 🚀**

