# Guide d'utilisation - Enquête BOB

Ce guide vous accompagne pas à pas dans l'utilisation du pipeline d'analyse de l'enquête BOB.

## 📋 Prérequis

1. **Python 3.8+** installé sur votre système
2. **Données d'enquête** au format Excel
3. **Marges de référence** (données INSEE par IRIS) au format CSV

## 🚀 Démarrage rapide

### 1. Installation

```bash
# Cloner ou télécharger le projet
cd bob-enquete

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Test avec données d'exemple

Pour tester le pipeline avant d'utiliser vos vraies données :

```bash
# Générer des données fictives
python scripts/generate_sample_data.py

# Lancer l'analyse complète
python src/cli.py run --config config.yaml
```

Les résultats seront dans `outputs/`.

### 3. Utilisation avec vos données

#### Étape 1 : Préparer vos données

**Fichier d'enquête** (`data/raw/enquete.xlsx`) :
- Format : Excel (.xlsx)
- Feuille : "Enquete" (configurable dans `config.yaml`)
- Colonnes obligatoires :
  - `id_repondant` : identifiant unique
  - `code_iris` : code IRIS du répondant
  - `age_group`, `sexe`, `csp` : variables de redressement
  - `interet_projet`, `accepte_cotisation` : variables BOB
  - Autres variables d'intérêt

**Fichier de marges** (`data/margins/margins_center.csv`) :
- Format : CSV
- Colonnes : `code_iris`, `age_group`, `sexe`, `csp`, `population`
- Doit contenir toutes les combinaisons de modalités avec leurs effectifs de référence

#### Étape 2 : Configurer le projet

Éditez `config.yaml` :

```yaml
# Chemins des fichiers
paths:
  raw_data: "data/raw/enquete.xlsx"
  margins: "data/margins/margins_center.csv"

# Variables de redressement
survey:
  weighting_vars:
    - "age_group"
    - "sexe"
    - "csp"
  id_column: "id_repondant"

# Paramètres du raking
raking:
  max_iterations: 100
  tolerance: 0.001
  min_weight: 0.1
  max_weight: 10.0

# Sous-groupes pour rapports spécifiques
analysis:
  subgroups:
    - name: "non_interesses"
      filter_variable: "interet_projet"
      filter_value: "Non"
    - name: "non_cotisation"
      filter_variable: "accepte_cotisation"
      filter_value: "Non"
    - name: "oui_cotisation"
      filter_variable: "accepte_cotisation"
      filter_value: "Oui"
```

#### Étape 3 : Lancer l'analyse

```bash
python src/cli.py run --config config.yaml
```

Le pipeline va :
1. ✓ Charger et valider les données
2. ✓ Nettoyer l'échantillon
3. ✓ Effectuer le redressement par raking
4. ✓ Calculer les métriques de qualité (Deff, n_eff)
5. ✓ Générer les graphiques
6. ✓ Produire les rapports PDF

## 📊 Comprendre les résultats

### Métriques de qualité

**Deff (Design Effect)** :
- Mesure l'augmentation de variance due au redressement
- Formule : `Deff = 1 + CV²(poids)`
- Interprétation :
  - Deff < 1.5 : ✓ Excellent
  - 1.5 ≤ Deff < 2.0 : ⚠ Acceptable
  - Deff ≥ 2.0 : ⚠ Médiocre (poids très dispersés)

**n_eff (Taille effective)** :
- Taille d'un échantillon aléatoire simple équivalent
- Formule : `n_eff = (Σw)² / Σ(w²)`
- Plus n_eff est proche de n, meilleure est la qualité

**Perte d'efficacité** :
- Pourcentage de perte par rapport à un échantillon non pondéré
- Formule : `(1 - n_eff/n) × 100`

### Rapports générés

1. **rapport_global_YYYYMMDD_HHMMSS.pdf**
   - Vue d'ensemble complète
   - Qualité du redressement
   - Distributions avant/après
   - Analyses descriptives

2. **rapport_non_interesses_YYYYMMDD_HHMMSS.pdf**
   - Focus sur les répondants non intéressés
   - Profil sociodémographique
   - Métriques spécifiques

3. **rapport_non_cotisation_YYYYMMDD_HHMMSS.pdf**
   - Analyse des refus de cotisation
   - Comparaison avec les acceptants

4. **rapport_oui_cotisation_YYYYMMDD_HHMMSS.pdf**
   - Profil des acceptants
   - Motivations et caractéristiques

### Fichiers de données

- **data_weighted_YYYYMMDD_HHMMSS.csv** : Données complètes avec poids finaux
- **quality_YYYYMMDD_HHMMSS.csv** : Écarts entre marges cibles et obtenues

## 🔧 Personnalisation

### Ajouter des variables d'intérêt

Dans `config.yaml` :

```yaml
analysis:
  variables_of_interest:
    - "mode_transport"
    - "distance_travail"
    - "votre_nouvelle_variable"
```

### Ajouter un sous-groupe

Dans `config.yaml` :

```yaml
analysis:
  subgroups:
    - name: "seniors"
      filter_variable: "age_group"
      filter_value: "65+"
      description: "Analyse des seniors"
```

### Modifier les paramètres du raking

```yaml
raking:
  max_iterations: 150        # Plus d'itérations si convergence difficile
  tolerance: 0.0005          # Critère plus strict
  min_weight: 0.2            # Limiter les poids extrêmes
  max_weight: 5.0
```

## ⚠️ Résolution de problèmes

### Le raking ne converge pas

**Causes possibles :**
- Marges incompatibles avec l'échantillon
- Effectifs trop faibles dans certaines cellules
- Variables de redressement trop corrélées

**Solutions :**
1. Augmenter `max_iterations` et `tolerance`
2. Élargir les limites `min_weight` et `max_weight`
3. Regrouper certaines modalités
4. Réduire le nombre de variables de redressement

### Deff trop élevé

**Causes :**
- Échantillon très différent de la population de référence
- Trop de variables de redressement
- Marges trop contraignantes

**Solutions :**
1. Vérifier la qualité de l'échantillon initial
2. Réduire le nombre de variables de redressement
3. Utiliser des marges moins détaillées (regroupement)

### Erreurs de chargement

**"Fichier non trouvé"** :
- Vérifier les chemins dans `config.yaml`
- S'assurer que les fichiers existent

**"Colonne manquante"** :
- Vérifier les noms de colonnes (sensible à la casse)
- S'assurer que toutes les variables requises sont présentes

## 📞 Support

Pour toute question ou problème :
1. Consulter les logs générés pendant l'exécution
2. Vérifier la configuration dans `config.yaml`
3. Examiner les fichiers de qualité dans `outputs/reports/`

## 📚 Ressources

- [Documentation pandas](https://pandas.pydata.org/docs/)
- [Méthode du raking (INSEE)](https://www.insee.fr/fr/metadonnees/definition/c1208)
- [Design Effect (Wikipedia)](https://en.wikipedia.org/wiki/Design_effect)

