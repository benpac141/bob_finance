# Bob-Enquête

Outil d'analyse et de redressement d'enquêtes par la méthode du raking (calage sur marges).

## 📋 Description

Ce projet permet de :
- Charger et nettoyer des données d'enquête (format Excel)
- Effectuer un redressement statistique par raking sur des marges de référence (ex: données INSEE par IRIS)
- Produire des analyses descriptives pondérées
- Générer des rapports PDF automatiques avec graphiques

## 🗂️ Structure du projet

```
bob-enquete/
├─ README.md                         # Ce fichier
├─ requirements.txt                  # Dépendances Python
├─ config.yaml                       # Configuration du projet
├─ Makefile                          # Commandes utiles
├─ data/
│  ├─ raw/                           # Données brutes
│  │   └─ enquete.xlsx               # Fichier Excel d'enquête
│  └─ margins/                       # Marges de référence
│      └─ margins_center.csv         # Marges IRIS (population de référence)
├─ outputs/
│  ├─ figures/                       # Graphiques générés (PNG)
│  └─ reports/                       # Rapports PDF autoportants
├─ scripts/
│  ├─ generate_sample_data.py        # Génération de données d'exemple
│  └─ README.md                      # Documentation des scripts
└─ src/
   ├─ raking.py                      # Algorithme de raking/IPF
   ├─ utils.py                       # Fonctions utilitaires
   ├─ load_clean.py                  # Chargement et nettoyage des données
   ├─ analysis.py                    # Analyses statistiques (Deff, n_eff)
   ├─ report_pdf.py                  # Génération de graphiques PNG
   ├─ pdf_report.py                  # Génération de rapports PDF complets
   └─ cli.py                         # Interface en ligne de commande
```

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Installation des dépendances

```bash
# Option 1 : avec Make
make install

# Option 2 : avec pip directement
pip install -r requirements.txt
```

### Génération de données d'exemple

Pour tester le pipeline avec des données fictives :

```bash
python scripts/generate_sample_data.py
```

Cela créera un fichier `data/raw/enquete.xlsx` avec 200 répondants fictifs.

## 📊 Préparation des données

### 1. Fichier d'enquête (`data/raw/enquete.xlsx`)

Votre fichier Excel doit contenir :
- Une colonne identifiant unique (`id_repondant`)
- Les variables de redressement (ex: `age_group`, `sexe`, `csp`)
- Un identifiant géographique (ex: `code_iris`)
- Les variables d'intérêt à analyser

Exemple de structure :

| id_repondant | code_iris | age_group | sexe | csp | mode_transport | distance_travail |
|--------------|-----------|-----------|------|-----|----------------|------------------|
| 1            | 211234501 | 25-34     | F    | 3   | Voiture        | 15               |
| 2            | 211234501 | 45-54     | M    | 5   | Transports     | 8                |

### 2. Fichier de marges (`data/margins/margins_center.csv`)

Fichier CSV contenant les marges de référence issues du **recensement INSEE 2022** pour les 11 IRIS du centre-ville de Besançon :

```csv
code_iris,age_group,sexe,csp,population
250560101,18-24,F,1.0,54
250560101,18-24,F,2.0,143
250560101,25-34,F,1.0,67
...
```

**Population totale** : 7,341 adultes (18+)  
**IRIS inclus** : 250560101, 250560102, 250560103, 250560104, 250560302, 250560303, 250560304, 250560401, 250560402, 250560501, 250560502

**Variables** :
- `age_group` : 18-24, 25-34, 35-44, 45-54, 55-64, 65+
- `sexe` : M (Masculin), F (Féminin)
- `csp` : 1 (Actifs occupés), 2 (Étudiants/Chômeurs), 3 (Retraités/Inactifs)

**Génération** : Utilisez `python scripts/prepare_margins_from_insee.py` pour régénérer depuis le recensement INSEE 2022.

## ⚙️ Configuration

Modifiez le fichier `config.yaml` selon vos besoins :

```yaml
survey:
  weighting_vars:
    - "age_group"
    - "sexe"
    - "csp"
  id_column: "id_repondant"

margins:
  geo_level: "IRIS"
  geo_id_column: "code_iris"
```

## 🎯 Utilisation

### Analyse complète

```bash
# Option 1 : avec Make
make run

# Option 2 : avec Python directement
python src/cli.py run --config config.yaml
```

### Étapes séparées

```bash
# Uniquement l'analyse
make analysis
# ou
python src/cli.py analyze --config config.yaml

# Uniquement le rapport
make report
# ou
python src/cli.py report --config config.yaml
```

### Nettoyage

```bash
make clean
```

## 📈 Méthode de redressement : Raking

Le **raking** (ou calage sur marges) est une méthode de redressement qui ajuste les poids des répondants pour que l'échantillon respecte des marges de référence connues.

### Principe

1. **Initialisation** : tous les répondants ont un poids initial (généralement 1)
2. **Itération** : pour chaque variable de redressement
   - Calculer les totaux pondérés actuels
   - Ajuster les poids pour correspondre aux marges de référence
3. **Convergence** : répéter jusqu'à ce que les marges soient respectées (critère de tolérance)

### Exemple

Si votre échantillon contient 40% de femmes mais que la population de référence en compte 52%, le raking augmentera le poids des femmes et diminuera celui des hommes pour respecter cette marge.

## 📄 Sorties

### Figures (`outputs/figures/`)
- `weights_distribution_{timestamp}.png` : Distribution des poids
- `convergence_{timestamp}.png` : Convergence du raking
- `comparison_{variable}_{timestamp}.png` : Comparaisons avant/après redressement
- `freq_{variable}_{timestamp}.png` : Distributions des variables d'intérêt

### Rapports (`outputs/reports/`)

**Rapports PDF autoportants :**
- `rapport_global_{timestamp}.pdf` : Rapport complet de l'enquête
  - Résumé exécutif
  - Qualité du redressement (Deff, n_eff, perte d'efficacité)
  - Qualité du calage sur marges
  - Analyses descriptives avec graphiques intégrés

- `rapport_non_interesses_{timestamp}.pdf` : Sous-groupe "non intéressés"
- `rapport_non_cotisation_{timestamp}.pdf` : Sous-groupe "refus cotisation"
- `rapport_oui_cotisation_{timestamp}.pdf` : Sous-groupe "accepte cotisation"

**Données exportées :**
- `data_weighted_{timestamp}.csv` : Données avec poids finaux
- `quality_{timestamp}.csv` : Qualité du calage par variable et modalité
- `report_{timestamp}.html` : Rapport HTML léger

### Métriques de qualité

Le pipeline calcule automatiquement :
- **Deff (Design Effect)** : Effet de plan, mesure l'augmentation de variance
- **n_eff** : Taille d'échantillon effective
- **Perte d'efficacité** : % de perte par rapport à un échantillon aléatoire simple
- **CV des poids** : Coefficient de variation des poids

## 🛠️ Développement

### Structure du code

- `load_clean.py` : Chargement et validation des données
- `raking.py` : Implémentation de l'algorithme de raking
- `analysis.py` : Calculs statistiques pondérés
- `report_pdf.py` : Génération de rapports
- `utils.py` : Fonctions utilitaires (chargement config, etc.)
- `cli.py` : Interface en ligne de commande

### Ajouter une nouvelle analyse

1. Ajouter une fonction dans `analysis.py`
2. Appeler la fonction dans `cli.py`
3. Ajouter la visualisation dans `report_pdf.py`

## 📚 Ressources

- [Documentation pandas](https://pandas.pydata.org/docs/)
- [Méthode du raking (INSEE)](https://www.insee.fr/fr/metadonnees/definition/c1208)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)

## 📝 Licence

Ce projet est fourni à des fins d'analyse interne.

## 👤 Auteur

À compléter selon vos besoins.

## 🤝 Contribution

Pour toute question ou amélioration, n'hésitez pas à contribuer !

