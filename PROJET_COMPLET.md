# 📦 Projet bob-enquete - Récapitulatif complet

## ✅ Projet créé avec succès !

Le pipeline d'analyse de l'enquête BOB est maintenant opérationnel.

## 📁 Structure créée

```
bob-enquete/
├── README.md                    # Documentation principale
├── QUICKSTART.md                # Démarrage rapide
├── GUIDE_UTILISATION.md         # Guide détaillé
├── PROJET_COMPLET.md            # Ce fichier
├── requirements.txt             # Dépendances Python
├── config.yaml                  # Configuration
├── Makefile                     # Commandes utiles
├── .gitignore                   # Fichiers à ignorer
│
├── data/
│   ├── raw/
│   │   └── enquete_bob.xlsx     # Données d'enquête (existant)
│   └── margins/
│       └── margins_center.csv   # Marges IRIS centre-ville
│
├── outputs/
│   ├── figures/                 # Graphiques PNG
│   └── reports/                 # Rapports PDF
│
├── scripts/
│   ├── generate_sample_data.py  # Génération de données test
│   ├── test_pipeline.py         # Tests du pipeline
│   └── README.md                # Documentation scripts
│
└── src/
    ├── __init__.py              # Package Python
    ├── utils.py                 # Fonctions utilitaires
    ├── load_clean.py            # Chargement et nettoyage
    ├── raking.py                # Algorithme de raking/IPF
    ├── analysis.py              # Analyses + métriques qualité
    ├── report_pdf.py            # Génération graphiques PNG
    ├── pdf_report.py            # Génération rapports PDF
    └── cli.py                   # Interface ligne de commande
```

## 🎯 Fonctionnalités implémentées

### 1. Chargement et validation des données
- ✅ Import Excel avec validation
- ✅ Nettoyage automatique (doublons, valeurs manquantes)
- ✅ Vérification de cohérence

### 2. Redressement par raking/IPF
- ✅ Algorithme de raking itératif
- ✅ Calage sur marges IRIS
- ✅ Contrôle de convergence
- ✅ Limites de poids configurables

### 3. Métriques de qualité
- ✅ **Deff** (Design Effect) : effet de plan
- ✅ **n_eff** : taille d'échantillon effective
- ✅ **Perte d'efficacité** : % de perte de précision
- ✅ **CV des poids** : coefficient de variation
- ✅ Statistiques complètes des poids

### 4. Analyses statistiques
- ✅ Distributions pondérées
- ✅ Tableaux croisés
- ✅ Comparaisons avant/après redressement
- ✅ Analyses par sous-groupes

### 5. Visualisations (PNG)
- ✅ Distribution des poids
- ✅ Convergence du raking
- ✅ Comparaisons distributions
- ✅ Graphiques par variable d'intérêt

### 6. Rapports PDF autoportants
- ✅ **Rapport global** : analyse complète
- ✅ **Rapport "non intéressés"** : sous-groupe spécifique
- ✅ **Rapport "non cotisation"** : refus cotisation
- ✅ **Rapport "oui cotisation"** : acceptants
- ✅ Graphiques intégrés dans les PDF
- ✅ Tableaux formatés
- ✅ Métriques de qualité affichées

### 7. Exports de données
- ✅ Données pondérées (CSV)
- ✅ Qualité du calage (CSV)
- ✅ Rapport HTML léger

## 🚀 Utilisation

### Test rapide (5 minutes)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Tester le pipeline
python scripts/test_pipeline.py

# 3. Générer des données d'exemple (optionnel)
python scripts/generate_sample_data.py

# 4. Lancer l'analyse
python src/cli.py run --config config.yaml
```

### Avec vos données

1. **Préparer les données** :
   - Mettre votre fichier Excel dans `data/raw/enquete.xlsx`
   - Mettre vos marges IRIS dans `data/margins/margins_center.csv`

2. **Configurer** :
   - Éditer `config.yaml` selon vos besoins
   - Adapter les variables de redressement
   - Définir les sous-groupes d'analyse

3. **Exécuter** :
   ```bash
   python src/cli.py run --config config.yaml
   ```

4. **Consulter les résultats** :
   - Graphiques : `outputs/figures/`
   - Rapports PDF : `outputs/reports/`

## 📊 Sorties générées

### Graphiques PNG (`outputs/figures/`)
- `weights_distribution_YYYYMMDD_HHMMSS.png`
- `convergence_YYYYMMDD_HHMMSS.png`
- `comparison_{variable}_YYYYMMDD_HHMMSS.png`
- `freq_{variable}_YYYYMMDD_HHMMSS.png`

### Rapports PDF (`outputs/reports/`)
- `rapport_global_YYYYMMDD_HHMMSS.pdf`
- `rapport_non_interesses_YYYYMMDD_HHMMSS.pdf`
- `rapport_non_cotisation_YYYYMMDD_HHMMSS.pdf`
- `rapport_oui_cotisation_YYYYMMDD_HHMMSS.pdf`

### Données exportées
- `data_weighted_YYYYMMDD_HHMMSS.csv`
- `quality_YYYYMMDD_HHMMSS.csv`
- `report_YYYYMMDD_HHMMSS.html`

## 🔧 Configuration

Le fichier `config.yaml` permet de configurer :

- **Chemins** : fichiers d'entrée/sortie
- **Variables de redressement** : âge, sexe, CSP, etc.
- **Paramètres du raking** : itérations, tolérance, limites
- **Sous-groupes** : filtres pour rapports spécifiques
- **Variables d'intérêt** : à analyser en détail

## 📚 Documentation

- **README.md** : Documentation complète du projet
- **QUICKSTART.md** : Démarrage rapide en 5 minutes
- **GUIDE_UTILISATION.md** : Guide détaillé pas à pas
- **scripts/README.md** : Documentation des scripts utilitaires

## 🧪 Tests

```bash
# Tester le pipeline
python scripts/test_pipeline.py

# Générer des données de test
python scripts/generate_sample_data.py

# Nettoyer les sorties
make clean
```

## 📦 Dépendances

Toutes les dépendances sont dans `requirements.txt` :
- pandas, numpy : traitement de données
- scipy : calculs statistiques
- matplotlib, seaborn : visualisations
- reportlab : génération PDF
- pyyaml : configuration
- click : interface CLI
- openpyxl : lecture Excel

## ✨ Points forts du pipeline

1. **Reproductible** : Configuration centralisée, logs détaillés
2. **Structuré** : Code modulaire, séparation des responsabilités
3. **Documenté** : Commentaires, docstrings, guides utilisateur
4. **Qualité** : Métriques Deff et n_eff pour évaluer le redressement
5. **Complet** : De l'import des données aux rapports PDF finaux
6. **Flexible** : Configuration YAML, sous-groupes personnalisables
7. **Professionnel** : Rapports PDF autoportants avec graphiques

## 🎓 Concepts clés

### Raking (calage sur marges)
Méthode de redressement qui ajuste les poids pour que l'échantillon respecte des marges de référence connues (ex: données INSEE).

### Design Effect (Deff)
Mesure l'augmentation de variance due au plan de sondage. Deff = 1 + CV²(poids).
- Deff < 1.5 : Excellent
- 1.5 ≤ Deff < 2.0 : Acceptable
- Deff ≥ 2.0 : Médiocre

### Taille effective (n_eff)
Taille d'un échantillon aléatoire simple équivalent en termes de précision.
n_eff = (Σw)² / Σ(w²)

## 🔄 Workflow type

1. Collecte des données d'enquête
2. Obtention des marges IRIS (INSEE)
3. Configuration du pipeline
4. Exécution du redressement
5. Vérification de la qualité (Deff, n_eff)
6. Génération des rapports
7. Analyse des résultats par sous-groupes
8. Export des données pondérées

## 💡 Prochaines étapes possibles

- Ajouter des tests unitaires (pytest)
- Implémenter d'autres méthodes de redressement
- Ajouter des graphiques interactifs (plotly)
- Créer une interface web (Streamlit/Dash)
- Automatiser avec des scripts batch/shell
- Intégrer à un pipeline de données plus large

## 📞 Support

Pour toute question :
1. Consulter la documentation (README.md, GUIDE_UTILISATION.md)
2. Vérifier les logs d'exécution
3. Examiner les fichiers de qualité générés
4. Tester avec des données d'exemple

---

**Projet créé le** : 29 octobre 2025  
**Version** : 1.0.0  
**Statut** : ✅ Opérationnel et testé

