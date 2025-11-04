# Solution : Gérer les Données Volumineuses pour GitHub

## ⚠️ Problème
GitHub limite les fichiers à **100 Mo** et les repositories peuvent devenir lents avec des fichiers volumineux.

## 🎯 Solutions

### Solution 1 : Utiliser Git LFS (Large File Storage) - RECOMMANDÉ

**Git LFS** permet de stocker les gros fichiers séparément tout en gardant les références dans GitHub.

#### Étapes

1. **Installer Git LFS** :
   - Téléchargez depuis [git-lfs.github.com](https://git-lfs.github.com)
   - Installez-le
   - Dans PowerShell :
   ```bash
   git lfs install
   ```

2. **Configurer Git LFS pour les fichiers de données** :
   ```bash
   cd D:\python_work\bob-enquete
   
   # Dire à Git LFS de gérer les fichiers Excel et CSV volumineux
   git lfs track "*.xlsx"
   git lfs track "*.csv"
   git lfs track "data/**/*.xlsx"
   git lfs track "data/**/*.csv"
   
   # Ajouter le fichier .gitattributes créé
   git add .gitattributes
   git commit -m "Configuration Git LFS pour les fichiers de données"
   ```

3. **Ajouter les fichiers** :
   ```bash
   git add data/
   git commit -m "Ajout des données avec Git LFS"
   git push origin main
   ```

#### Avantages
- ✅ Conserve les données dans le repository
- ✅ Fonctionne avec Streamlit Cloud
- ✅ Gratuit pour les repositories publics

#### Limites
- Plan gratuit GitHub : 1 Go de stockage LFS
- 1 Go de bande passante par mois

---

### Solution 2 : Exclure les Données et Utiliser un Stockage Externe

Si vos données sont vraiment très volumineuses, stockez-les ailleurs.

#### Option A : Stocker sur Google Drive / Dropbox

1. **Mettre les données sur Google Drive** :
   - Uploadez vos fichiers Excel/CSV sur Google Drive
   - Partagez-les en "Lien accessible à tous"
   - Obtenez l'ID du fichier

2. **Modifier le code pour télécharger les données** :

Créer un fichier `scripts/download_data.py` :

```python
"""
Télécharge les données depuis Google Drive si elles ne sont pas présentes localement.
"""
import requests
from pathlib import Path

def download_from_google_drive(file_id, destination):
    """Télécharge un fichier depuis Google Drive."""
    URL = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    response = requests.get(URL, stream=True)
    
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"✅ Fichier téléchargé : {destination}")

# IDs de vos fichiers Google Drive (à remplacer)
DATA_FILE_ID = "VOTRE_ID_FICHIER_EXCEL"
MARGINS_FILE_ID = "VOTRE_ID_FICHIER_CSV"

# Chemins de destination
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Télécharger seulement si les fichiers n'existent pas
if not (DATA_DIR / "raw" / "enquete_all_prepared.xlsx").exists():
    download_from_google_drive(
        DATA_FILE_ID,
        DATA_DIR / "raw" / "enquete_all_prepared.xlsx"
    )

if not (DATA_DIR / "margins" / "margins_center.csv").exists():
    download_from_google_drive(
        MARGINS_FILE_ID,
        DATA_DIR / "margins" / "margins_center.csv"
    )
```

3. **Modifier `budget_simulator_interactive.py`** :

```python
# Au début du fichier, avant load_data()
from scripts.download_data import download_from_google_drive

# Les données seront téléchargées automatiquement si absentes
```

4. **Exclure les données du repository** :

Ajouter dans `.gitignore` :
```
data/raw/*.xlsx
data/raw/*.csv
data/margins/*.csv
```

5. **Ajouter un fichier de données d'exemple** (optionnel) :
   - Créez une version réduite pour les tests
   - Nommez-la `data/raw/enquete_all_prepared.example.xlsx`

#### Option B : Utiliser un Service Cloud (S3, Azure Blob, etc.)

Pour des données vraiment volumineuses, utilisez un stockage cloud professionnel.

---

### Solution 3 : Compresser les Données

Si vos fichiers Excel sont volumineux, compressez-les.

1. **Créer un script de compression** :

```python
import pandas as pd
from pathlib import Path
import gzip
import pickle

def compress_data():
    """Compresse les données pour réduire la taille."""
    data_dir = Path(__file__).parent.parent / "data"
    
    # Charger et compresser le fichier Excel
    df = pd.read_excel(data_dir / "raw" / "enquete_all_prepared.xlsx")
    
    # Sauvegarder en format compressé
    with gzip.open(data_dir / "raw" / "enquete_all_prepared.pkl.gz", 'wb') as f:
        pickle.dump(df, f)
    
    print("✅ Données compressées")

if __name__ == "__main__":
    compress_data()
```

2. **Modifier le code pour décompresser** :

```python
import gzip
import pickle

def load_data():
    """Charge les données compressées."""
    data_dir = Path(__file__).parent.parent / "data"
    
    # Décompresser
    with gzip.open(data_dir / "raw" / "enquete_all_prepared.pkl.gz", 'rb') as f:
        df = pickle.load(f)
    
    return df
```

---

### Solution 4 : Utiliser des Données d'Exemple (Pour le Déploiement)

Gardez une version réduite des données dans le repository.

1. **Créer un échantillon** :

```python
import pandas as pd

# Charger les données complètes
df_full = pd.read_excel("data/raw/enquete_all_prepared.xlsx")

# Créer un échantillon (par exemple, 20% des données)
df_sample = df_full.sample(frac=0.2, random_state=42)

# Sauvegarder
df_sample.to_excel("data/raw/enquete_all_prepared.sample.xlsx", index=False)
```

2. **Modifier le code pour utiliser l'échantillon en production** :

```python
def load_data():
    """Charge les données (échantillon pour déploiement)."""
    # En production (Streamlit Cloud), utiliser l'échantillon
    # En local, utiliser les données complètes
    import os
    if os.getenv('STREAMLIT_CLOUD'):
        data_file = BASE_DIR / "data" / "raw" / "enquete_all_prepared.sample.xlsx"
    else:
        data_file = BASE_DIR / "data" / "raw" / "enquete_all_prepared.xlsx"
    
    df = pd.read_excel(data_file)
    # ...
```

---

## 🎯 Recommandation

### Pour Votre Cas

1. **Si les données font moins de 50 Mo** :
   - Utilisez **Git LFS** (Solution 1)
   - Simple et efficace

2. **Si les données font plus de 50 Mo** :
   - Utilisez **Google Drive + téléchargement automatique** (Solution 2A)
   - Stockez les données sur Drive
   - Le code les télécharge automatiquement

3. **Si les données sont vraiment énormes** :
   - Utilisez des **données d'exemple** pour le déploiement (Solution 4)
   - Gardez les données complètes localement

---

## 📋 Checklist : Quelle Solution Choisir ?

- [ ] **Taille des données** : ____ Mo
- [ ] **Besoin d'accès hors ligne** : Oui / Non
- [ ] **Données sensibles** : Oui / Non
- [ ] **Fréquence de mise à jour** : Rare / Fréquente

---

## 🚀 Guide Rapide : Git LFS (Solution Recommandée)

Si vous choisissez Git LFS :

```bash
# 1. Installer Git LFS
# Téléchargez depuis https://git-lfs.github.com

# 2. Initialiser Git LFS
cd D:\python_work\bob-enquete
git lfs install

# 3. Suivre les fichiers volumineux
git lfs track "data/**/*.xlsx"
git lfs track "data/**/*.csv"

# 4. Ajouter le fichier .gitattributes
git add .gitattributes

# 5. Ajouter les données
git add data/
git commit -m "Ajout des données avec Git LFS"
git push origin main
```

---

## ⚠️ Note Important

**Pour Streamlit Cloud** :
- Git LFS fonctionne ✅
- Google Drive fonctionne ✅ (avec modifications du code)
- Données externes fonctionnent ✅

Après avoir résolu le problème de taille, vous pourrez déployer normalement sur Streamlit Cloud !

---

**Besoin d'aide pour une solution spécifique ? Dites-moi quelle approche vous préférez !**

