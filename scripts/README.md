# Scripts utilitaires

Ce répertoire contient des scripts utilitaires pour le projet bob-enquete.

## 📊 prepare_margins_from_insee.py

Génère les marges de référence à partir du recensement INSEE 2022.

**Usage :**
```bash
python scripts/prepare_margins_from_insee.py
```

**Source :**
- Fichier : `D:\python_work\eqasim-bfc\data\raw\census_2022.csv`
- Documentation : `D:\python_work\eqasim-bfc\data\raw\varmod_indcvi_2022.csv`

**IRIS centre-ville de Besançon :**
```
250560101, 250560102, 250560103, 250560104
250560302, 250560303, 250560304
250560401, 250560402
250560501, 250560502
```

**Sortie :**
- `data/margins/margins_center.csv` : 288 lignes, 7,341 adultes

**Variables extraites :**
- `code_iris` : Code IRIS (9 caractères)
- `age_group` : Tranche d'âge (18-24, 25-34, 35-44, 45-54, 55-64, 65+)
- `sexe` : Sexe (M/F)
- `csp` : Type d'activité (1=Actifs, 2=Étudiants/Chômeurs, 3=Retraités/Inactifs)
- `population` : Effectif

**Mapping des variables INSEE :**
- `AGED` → `age_group` (tranches d'âge)
- `SEXE` (1/2) → `sexe` (M/F)
- `TACT` (11/12/21/22/23) → `csp` (1/2/3)

## 🧪 generate_sample_data.py

Génère des données d'exemple pour tester le pipeline.

**Usage :**
```bash
python scripts/generate_sample_data.py
```

**Sortie :**
- `data/raw/enquete.xlsx` : Fichier Excel avec 200 répondants fictifs

**Variables générées :**
- `id_repondant` : Identifiant unique
- `code_iris` : Code IRIS (2 IRIS centre-ville)
- `age_group` : Groupe d'âge (6 modalités)
- `sexe` : Sexe (F/M)
- `csp` : Catégorie socio-professionnelle (1-3)
- `interet_projet` : Intérêt pour le projet BOB (Oui/Non)
- `accepte_cotisation` : Acceptation de la cotisation (Oui/Non)
- `mode_transport` : Mode de transport principal
- `distance_travail` : Distance domicile-travail (km)
- `frequence_deplacement` : Fréquence des déplacements (jours/semaine)

## 🧪 test_pipeline.py

Teste que tous les modules du pipeline sont fonctionnels.

**Usage :**
```bash
python scripts/test_pipeline.py
```

**Tests effectués :**
1. Import de tous les modules Python
2. Structure des répertoires
3. Validation du fichier de configuration
4. Présence des fichiers de données

## 📋 list_iris_besancon.py

Liste tous les IRIS de Besançon avec leur population (utilitaire).

**Usage :**
```bash
python scripts/list_iris_besancon.py
```

**Sortie :**
- `data/iris_besancon_list.csv` : Liste complète des IRIS de Besançon

## 🔄 Workflow complet

### 1. Préparation des marges (une seule fois)
```bash
python scripts/prepare_margins_from_insee.py
```

### 2. Test du pipeline
```bash
python scripts/test_pipeline.py
```

### 3. Génération de données test (optionnel)
```bash
python scripts/generate_sample_data.py
```

### 4. Analyse complète
```bash
python src/cli.py run --config config.yaml
```

## 📝 Notes

- Les scripts utilisent les données INSEE 2022 pour les marges de référence
- Le centre-ville de Besançon compte 7,341 adultes (18+) selon le recensement 2022
- Les marges sont créées au niveau IRIS avec 3 dimensions : âge, sexe, type d'activité
- Pour modifier les IRIS inclus, éditez la variable `IRIS_CENTER` dans `prepare_margins_from_insee.py`

## 🆘 Dépannage

**Erreur "Fichier non trouvé"** :
- Vérifiez que le fichier recensement existe : `D:\python_work\eqasim-bfc\data\raw\census_2022.csv`
- Adaptez le chemin dans la variable `CENSUS_FILE` si nécessaire

**0 IRIS trouvés** :
- Vérifiez les codes IRIS dans la variable `IRIS_CENTER`
- Les codes doivent être au format complet (9 caractères) : `250560101`

**Population = 0** :
- Vérifiez le mapping des variables (AGED, SEXE, TACT)
- Consultez la documentation : `varmod_indcvi_2022.csv`
