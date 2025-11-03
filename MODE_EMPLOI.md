# Mode d'Emploi - Projet BOB Enquête

## 🎯 Objectif

Analyser l'enquête BOB sur la bibliothèque d'objets à Besançon, en **conservant tous les répondants** mais en les **analysant différemment** selon leur localisation.

## 📋 Prérequis

- Python 3.8+
- Fichier d'enquête : `data/raw/enquete_bob.xlsx` (90 répondants)
- Marges INSEE : `data/margins/margins_center.csv` (centre-ville Besançon)

## 🚀 Démarrage Rapide

### 1. Préparer les données (1ère fois uniquement)

```bash
cd D:\python_work\bob-enquete
python scripts/prepare_bob_with_all_respondents.py
```

**Ce que fait ce script** :
- Charge les 90 répondants de `enquete_bob.xlsx`
- Crée la colonne `is_besancon` (True/False)
- Impute les valeurs manquantes (âge, sexe, CSP)
- Attribue des codes IRIS selon l'emplacement déclaré
- Sauvegarde `enquete_all_prepared.xlsx`

**Résultat** :
```
✓ 90 répondants conservés
  - 52 Besançon (57.8%)
  - 38 Hors-Besançon (42.2%)
```

### 2. Lancer l'analyse complète

```bash
python scripts/run_analysis_with_filters.py
```

**Ce que fait ce script** :
1. Charge les 90 répondants
2. **Redresse les 52 Besançon** avec les marges INSEE
3. Réintègre les poids dans le dataframe complet
4. Génère les figures **LOCALES** (Besançon uniquement)
5. Génère les figures **GENERALES** (tous les répondants)
6. Produit le rapport PDF

**Résultat** :
```
✓ Poids calculés (Besançon) : 102 à 1000
✓ Deff = 1.71, N_eff = 31
✓ Figures générées dans outputs/figures/
✓ Rapport PDF dans outputs/reports/
```

### 3. Comparer Besançon vs Hors-Besançon

```bash
python scripts/compare_besancon_vs_hors.py
```

**Ce que fait ce script** :
- Compare les réponses entre les deux groupes
- Affiche les statistiques descriptives
- Calcule l'écart d'intérêt pour le projet

**Résultat** :
```
✓ Intérêt Besançon : 69.2%
✓ Intérêt Hors-Besançon : 39.5%
✓ Écart : +29.8 points
```

## 📊 Fichiers Générés

### Données
```
data/raw/enquete_all_prepared.xlsx       # 90 répondants préparés
outputs/reports/data_weighted_*.csv      # Données avec poids
```

### Figures (dans `outputs/figures/`)
```
weights_distribution_*.png               # Distribution des poids
convergence_*.png                        # Convergence du raking
comparison_age_group_*.png               # Avant/après âge
comparison_sexe_*.png                    # Avant/après sexe
comparison_csp_*.png                     # Avant/après CSP

freq_local_interet_projet_*.png          # Intérêt (Besançon)
freq_local_accepte_cotisation_*.png      # Cotisation (Besançon)

freq_general_deja_utilise_*.png          # Déjà utilisé (Tous)
freq_general_partage_oui_*.png           # Partage (Tous)
freq_general_prix_max_*.png              # Prix max (Tous)
```

### Rapports
```
outputs/reports/rapport_global_*.pdf     # Rapport PDF complet
```

## 🔧 Configuration

Le fichier `config.yaml` contrôle tous les paramètres :

### Chemins
```yaml
paths:
  raw_data: data/raw/enquete_all_prepared.xlsx
  margins: data/margins/margins_center.csv
  output_figures: outputs/figures
  output_reports: outputs/reports
```

### Variables d'analyse
```yaml
analysis:
  # Variables locales (Besançon uniquement)
  variables_local:
    - "interet_projet"
    - "accepte_cotisation"
  
  # Variables générales (tous les répondants)
  variables_general:
    - "deja_utilise_services"
    - "partage_oui"
    - "prix_max_location"
```

### Paramètres du raking
```yaml
raking:
  max_iterations: 500      # Nombre max d'itérations
  tolerance: 0.01          # Critère de convergence
  min_weight: 0.01         # Poids minimum
  max_weight: 1000.0       # Poids maximum
```

## 📖 Comprendre les Résultats

### Poids de Redressement

**Besançon (52 répondants)** :
- Poids min : 102.6 → Ce répondant représente ~103 personnes
- Poids max : 1000.0 → Ce répondant représente ~1000 personnes (cap atteint)
- Poids moyen : 366.3 → En moyenne, 1 répondant ≈ 366 personnes

**Hors-Besançon (38 répondants)** :
- Poids : 1.0 → Non redressés, comptés brut

### Métriques de Qualité

**Deff (Design Effect)** : 1.71
- Mesure l'effet du plan de sondage
- 1.0 = échantillon parfait
- 1.71 = perte d'efficacité de 71%

**N_eff (Taille Effective)** : 31
- Taille d'échantillon "équivalente"
- 52 répondants → 31 effectifs (perte 41%)

**Convergence** : Non atteinte
- Écart relatif max : 79.5% (âge)
- Raison : Petit échantillon (52) pour grande population (25k)

### Interprétation

#### Questions LOCALES (Besançon uniquement)

**Intérêt pour le projet** :
- 69.2% "Oui" (pondéré)
- Représente ~17,573 habitants du centre-ville
- IC 95% : [±15%] (large car N_eff=31)

**Acceptation cotisation** :
- 63.5% acceptent de payer
- Représente ~16,117 habitants
- Montant modal : 1€ à 10€ (23.1%)

#### Questions GENERALES (Tous les répondants)

**Déjà utilisé des services** :
- 60% "Non jamais"
- Potentiel de nouveaux utilisateurs

**Partage d'objets** :
- 45.6% "Oui avec conditions"
- Nécessite un cadre clair

**Prix maximum** :
- 50% choisissent "10€"
- Seuil psychologique

## ⚠️ Limites et Précautions

### Limites Méthodologiques

1. **Petit échantillon** : 52 répondants pour 25k habitants
   - Marges d'erreur importantes
   - Convergence difficile

2. **Convergence non atteinte** : Écart relatif 79.5%
   - Redressement imparfait
   - Résultats à interpréter avec prudence

3. **Perte d'efficacité** : 41.2%
   - N_eff = 31 au lieu de 52
   - Intervalles de confiance élargis

### Précautions d'Interprétation

✅ **À FAIRE** :
- Mentionner les limites dans les rapports
- Utiliser des fourchettes (ex: "60-75%")
- Croiser avec d'autres sources
- Présenter comme "tendances" plutôt que "certitudes"

❌ **À ÉVITER** :
- Extrapoler au-delà du centre-ville
- Donner des chiffres précis sans IC
- Ignorer les limites méthodologiques
- Comparer avec d'autres territoires

## 🎯 Cas d'Usage

### Cas 1 : Estimer la demande locale

**Question** : Combien d'habitants du centre-ville sont intéressés ?

**Méthode** :
1. Utiliser les résultats LOCAUX (Besançon)
2. Appliquer le pourcentage pondéré (69.2%)
3. Multiplier par la population (25,381)

**Résultat** :
- 69.2% × 25,381 = **~17,573 habitants intéressés**
- Fourchette prudente : 15,000 - 20,000

### Cas 2 : Identifier les freins

**Question** : Quels sont les principaux obstacles ?

**Méthode** :
1. Analyser les réponses GENERALES (tous)
2. Identifier les modalités négatives
3. Quantifier les proportions

**Résultat** :
- **Prix** : 61.5% ne veulent pas payer > 10€
- **Partage** : 34.6% veulent seulement emprunter
- **Expérience** : 53.8% n'ont jamais utilisé

### Cas 3 : Comparer les profils

**Question** : Les hors-Besançon sont-ils différents ?

**Méthode** :
1. Utiliser `compare_besancon_vs_hors.py`
2. Comparer les distributions
3. Calculer les écarts

**Résultat** :
- **Âge** : Hors-Besançon beaucoup plus jeunes (84% 18-24 ans)
- **CSP** : Hors-Besançon majoritairement étudiants (79%)
- **Intérêt** : Écart de +29.8 points en faveur de Besançon

## 🔄 Workflow Complet

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PREPARATION DES DONNEES                                  │
│    python scripts/prepare_bob_with_all_respondents.py       │
│    → enquete_all_prepared.xlsx (90 répondants)              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. ANALYSE COMPLETE                                         │
│    python scripts/run_analysis_with_filters.py              │
│    → Redressement (52 Besançon)                             │
│    → Figures (locales + générales)                          │
│    → Rapport PDF                                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. COMPARAISON (optionnel)                                  │
│    python scripts/compare_besancon_vs_hors.py               │
│    → Statistiques comparatives                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. EXPLOITATION                                             │
│    → Consulter outputs/reports/rapport_global_*.pdf         │
│    → Analyser outputs/figures/*.png                         │
│    → Utiliser outputs/reports/data_weighted_*.csv           │
└─────────────────────────────────────────────────────────────┘
```

## 📞 Aide et Dépannage

### Erreur : "File not found"
→ Vérifier que `enquete_bob.xlsx` est dans `data/raw/`

### Erreur : "Convergence non atteinte"
→ Normal avec 52 répondants, augmenter `max_iterations` dans `config.yaml`

### Erreur : "KeyError: 'is_besancon'"
→ Relancer `prepare_bob_with_all_respondents.py`

### Poids très élevés (>1000)
→ Normal, le ratio est de 1:488 (52 pour 25k)

### Résultats différents à chaque exécution
→ Normal, l'imputation utilise de l'aléatoire (fixer `random_seed` si besoin)

## 📚 Documentation Complémentaire

- `STRATEGIE_ANALYSES.md` : Détails de la stratégie méthodologique
- `SYNTHESE_FINALE.md` : Résultats complets et interprétation
- `ADAPTER_ENQUETE_BOB.md` : Guide de préparation des données
- `README.md` : Vue d'ensemble du projet

## ✅ Checklist Avant Présentation

- [ ] Données préparées (`enquete_all_prepared.xlsx` existe)
- [ ] Analyse lancée (figures et rapport générés)
- [ ] Résultats vérifiés (poids cohérents, figures lisibles)
- [ ] Limites documentées (petit échantillon, convergence)
- [ ] Interprétation prudente (fourchettes, tendances)
- [ ] Comparaison Besançon/Hors effectuée
- [ ] Recommandations formulées

---

**Projet prêt à l'emploi** ✅  
**Pipeline testé et validé** ✅  
**Documentation complète** ✅

