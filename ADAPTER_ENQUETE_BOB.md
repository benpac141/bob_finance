# 🔄 Adapter l'enquête BOB aux marges INSEE

## 📋 Objectif

Votre enquête BOB doit contenir les mêmes variables que les marges INSEE pour permettre le redressement.

## ✅ Variables requises

### 1. **code_iris** : Code IRIS du répondant
- Format : 9 caractères (ex: `250560101`)
- Source : Adresse du répondant → géocodage → IRIS
- Les 11 IRIS du centre-ville : `250560101`, `250560102`, `250560103`, `250560104`, `250560302`, `250560303`, `250560304`, `250560401`, `250560402`, `250560501`, `250560502`

### 2. **age_group** : Tranche d'âge
- Modalités : `18-24`, `25-34`, `35-44`, `45-54`, `55-64`, `65+`
- À créer depuis l'âge du répondant

### 3. **sexe** : Sexe
- Modalités : `M` (Masculin), `F` (Féminin)
- À mapper depuis votre variable genre

### 4. **csp** : Type d'activité
- Modalités :
  - `1` : Actifs occupés (en emploi)
  - `2` : Étudiants / Chômeurs
  - `3` : Retraités / Autres inactifs
- À créer depuis votre variable d'activité professionnelle

## 🔧 Script de préparation

Créez un script `scripts/prepare_bob_data.py` pour transformer vos données :

```python
import pandas as pd
import numpy as np

# Charger votre enquête BOB
df = pd.read_excel("data/raw/enquete_bob.xlsx")

# 1. Créer age_group depuis l'âge
def create_age_group(age):
    if pd.isna(age):
        return None
    if 18 <= age <= 24:
        return '18-24'
    elif 25 <= age <= 34:
        return '25-34'
    elif 35 <= age <= 44:
        return '35-44'
    elif 45 <= age <= 54:
        return '45-54'
    elif 55 <= age <= 64:
        return '55-64'
    elif age >= 65:
        return '65+'
    else:
        return None

df['age_group'] = df['age'].apply(create_age_group)

# 2. Mapper le sexe
# Adaptez selon vos modalités
gender_map = {
    'Homme': 'M',
    'Femme': 'F',
    'Masculin': 'M',
    'Féminin': 'F',
    # Ajoutez vos modalités
}
df['sexe'] = df['genre'].map(gender_map)

# 3. Créer csp depuis l'activité
def create_csp(activite):
    if pd.isna(activite):
        return None
    activite_lower = str(activite).lower()
    
    # Actifs occupés
    if any(word in activite_lower for word in ['emploi', 'salarié', 'indépendant', 'profession']):
        return 1
    
    # Étudiants / Chômeurs
    elif any(word in activite_lower for word in ['étudiant', 'élève', 'chômeur', 'recherche emploi']):
        return 2
    
    # Retraités / Inactifs
    elif any(word in activite_lower for word in ['retraité', 'inactif', 'foyer']):
        return 3
    
    else:
        return None

df['csp'] = df['activite_professionnelle'].apply(create_csp)

# 4. Ajouter code_iris (si vous avez les adresses)
# Option A : Si vous avez déjà les codes IRIS
# df['code_iris'] = df['iris_existant']

# Option B : Si vous devez géocoder
# Utilisez une API de géocodage (BAN, etc.)
# Pour l'instant, attribuez aléatoirement un IRIS centre-ville
iris_center = ['250560101', '250560102', '250560103', '250560104',
               '250560302', '250560303', '250560304',
               '250560401', '250560402', '250560501', '250560502']
df['code_iris'] = np.random.choice(iris_center, len(df))

# 5. Filtrer les lignes valides
df_clean = df.dropna(subset=['age_group', 'sexe', 'csp', 'code_iris'])

print(f"Données préparées : {len(df_clean)} répondants sur {len(df)}")

# 6. Sauvegarder
df_clean.to_excel("data/raw/enquete.xlsx", index=False)
print("Fichier sauvegardé : data/raw/enquete.xlsx")
```

## 📊 Vérification des données

Avant de lancer le redressement, vérifiez que vos données sont cohérentes :

```python
# Vérifier les modalités
print("Age groups:", df['age_group'].unique())
print("Sexe:", df['sexe'].unique())
print("CSP:", df['csp'].unique())
print("IRIS:", df['code_iris'].unique())

# Vérifier les effectifs
print("\nRépartition age_group:")
print(df['age_group'].value_counts())

print("\nRépartition sexe:")
print(df['sexe'].value_counts())

print("\nRépartition csp:")
print(df['csp'].value_counts())
```

## ⚠️ Points d'attention

### 1. Code IRIS
- **Critique** : Le code IRIS doit être exact (9 caractères)
- Si vous n'avez pas les IRIS, vous devez géocoder les adresses
- Outils : API BAN (Base Adresse Nationale), API IGN

### 2. Tranches d'âge
- Respectez exactement les bornes : 18-24, 25-34, etc.
- Les répondants < 18 ans seront exclus

### 3. Sexe
- Uniquement M ou F (contrainte des marges INSEE)
- Si vous avez d'autres modalités, décidez comment les traiter

### 4. CSP (Type d'activité)
- Simplification en 3 catégories
- Adaptez le mapping selon vos questions

## 🔄 Workflow complet

### Étape 1 : Préparer les données BOB
```bash
python scripts/prepare_bob_data.py
```

### Étape 2 : Vérifier la configuration
Éditez `config.yaml` :
```yaml
paths:
  excel: data/raw/enquete.xlsx
  margins: data/margins/margins_center.csv

survey:
  weighting_vars:
    - "age_group"
    - "sexe"
    - "csp"
  id_column: "id_repondant"
```

### Étape 3 : Lancer le redressement
```bash
python src/cli.py run --config config.yaml
```

## 📈 Résultats attendus

Après redressement, vous obtiendrez :
- **Poids** pour chaque répondant
- **Métriques de qualité** : Deff, n_eff
- **Rapports PDF** : global + sous-groupes
- **Données pondérées** : CSV avec poids finaux

## 🆘 Problèmes courants

### "Variable non trouvée"
→ Vérifiez les noms de colonnes dans votre fichier Excel

### "Modalités incompatibles"
→ Vérifiez que vos modalités correspondent exactement : `18-24`, `M`, `F`, `1`, `2`, `3`

### "Convergence non atteinte"
→ Votre échantillon est peut-être trop différent de la population
→ Augmentez `max_iterations` ou `tolerance` dans `config.yaml`

### "Deff trop élevé"
→ Poids très dispersés
→ Vérifiez la qualité de votre échantillon
→ Envisagez de réduire le nombre de variables de redressement

## 📞 Support

Consultez :
- `README.md` : Documentation complète
- `GUIDE_UTILISATION.md` : Guide pas à pas
- `MARGES_INSEE_README.md` : Détails sur les marges
- `scripts/README.md` : Documentation des scripts

---

**Important** : Le redressement ne peut corriger que les biais d'échantillonnage, pas les biais de mesure ou de non-réponse totale.

