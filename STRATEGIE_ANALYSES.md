# Stratégie d'Analyse BOB - Gestion des Répondants

## Contexte

L'enquête BOB contient **90 répondants** dont :
- **52 habitent à Besançon** (codes postaux 25xxx)
- **38 habitent hors Besançon**

## Problématique

Certaines questions sont **locales** (liées au territoire de Besançon) :
- Intérêt pour une bibliothèque d'objets **à Besançon**
- Acceptation de payer une cotisation pour ce service **à Besançon**

D'autres questions sont **générales** (applicables à tous) :
- Avez-vous déjà utilisé des services de location/prêt ?
- Accepteriez-vous de partager vos objets ?
- Prix maximum acceptable pour une location

## Solution Adoptée

### 1. Conservation de TOUS les répondants (90)

**Principe** : Aucun répondant n'est exclu. Tous sont conservés dans le fichier préparé.

**Fichier** : `data/raw/enquete_all_prepared.xlsx`

**Colonne clé** : `is_besancon` (True/False)

### 2. Redressement sur Besançon uniquement (52)

**Pourquoi ?**
- Les marges INSEE concernent uniquement les IRIS centre-ville de Besançon
- On ne peut pas redresser les hors-Besançon avec ces marges

**Comment ?**
1. Filtrer les 52 répondants Besançon
2. Appliquer le raking avec les marges INSEE
3. Obtenir des poids pour ces 52 personnes
4. Réintégrer les poids dans le dataframe complet (90 lignes)
5. Les 38 hors-Besançon ont un poids de 1.0 (non redressés)

### 3. Analyses différenciées

#### Analyses LOCALES (Besançon uniquement)

**Variables concernées** :
- `interet_projet` : Une bibliothèque d'objets à Besançon vous intéresserait-elle ?
- `accepte_cotisation` : Accepteriez-vous de payer une cotisation ?

**Méthode** :
```python
df_besancon = df_all[df_all['is_besancon']]
freq = weighted_frequency(df_besancon, 'interet_projet', weight_col='weight')
```

**Résultats** :
- Utilisent les poids redressés (102 à 1000)
- Représentent la population du centre-ville de Besançon (25 381 habitants)
- N_eff ≈ 31 (perte d'efficacité de 41%)

#### Analyses GENERALES (Tous les répondants)

**Variables concernées** :
- `deja_utilise_services` : Avez-vous déjà utilisé des services de location/prêt ?
- `partage_oui` : Accepteriez-vous de partager vos objets ?
- `prix_max_location` : Prix maximum acceptable
- `motivations` : Raisons d'utiliser une bibliothèque d'objets
- `criteres` : Critères essentiels

**Méthode** :
```python
freq = weighted_frequency(df_all, 'deja_utilise_services', weight_col='weight')
```

**Résultats** :
- Les 52 Besançon utilisent leurs poids redressés
- Les 38 hors-Besançon ont un poids de 1.0
- Représentent un échantillon mixte (local + régional)

## Justification

### Pourquoi ne pas exclure les hors-Besançon ?

1. **Richesse des données** : Leurs réponses sur les pratiques générales sont précieuses
2. **Comparaisons possibles** : On peut comparer Besançon vs hors-Besançon
3. **Taille d'échantillon** : 90 répondants > 52 pour les analyses générales

### Pourquoi ne pas les redresser ?

1. **Pas de marges disponibles** : Les marges INSEE sont spécifiques au centre-ville
2. **Hétérogénéité territoriale** : Les hors-Besançon viennent de territoires variés
3. **Interprétation claire** : Besançon = redressé, Hors = brut

### Pourquoi poids=1 pour les hors-Besançon ?

1. **Simplicité** : Pas de sur/sous-pondération artificielle
2. **Transparence** : On sait qu'ils ne sont pas redressés
3. **Flexibilité** : On peut les exclure facilement si besoin (`df[df['is_besancon']]`)

## Fichiers Générés

### Script de préparation
```
scripts/prepare_bob_with_all_respondents.py
```
- Charge les 90 répondants
- Crée la colonne `is_besancon`
- Impute les valeurs manquantes (âge, sexe, CSP)
- Attribue des IRIS selon l'emplacement déclaré
- Sauvegarde `enquete_all_prepared.xlsx`

### Script d'analyse
```
scripts/run_analysis_with_filters.py
```
- Charge les 90 répondants
- Redresse les 52 Besançon
- Réintègre les poids
- Génère les figures LOCALES (Besançon)
- Génère les figures GENERALES (Tous)
- Produit le rapport PDF

### Configuration
```
config.yaml
```
- `variables_local` : Questions locales (Besançon uniquement)
- `variables_general` : Questions générales (tous)
- `local_filter` : Filtre pour analyses locales

## Résultats Clés

### Redressement (Besançon)
- **N** : 52 répondants
- **Population cible** : 25 381 habitants
- **Ratio** : 1 répondant ≈ 488 habitants
- **Poids min** : 102.6
- **Poids max** : 1000.0 (cap atteint)
- **Poids moyen** : 366.3
- **Deff** : 1.71
- **N_eff** : 31
- **Perte d'efficacité** : 41.2%

### Intérêt pour le projet (Besançon, pondéré)
- **Oui** : ~69% (après redressement)
- **Peut-être** : ~23%
- **Non** : ~8%

### Intérêt pour le projet (Hors Besançon, brut)
- **Oui** : 39% (15/38)
- **Non** : 39% (15/38)
- **Peut-être** : 18% (7/38)

**→ Les hors-Besançon sont nettement moins intéressés, ce qui valide l'approche de les exclure des analyses locales.**

## Recommandations

### Pour les rapports

1. **Toujours préciser le périmètre** :
   - "Parmi les habitants du centre-ville de Besançon..." (analyses locales)
   - "Parmi l'ensemble des répondants..." (analyses générales)

2. **Mentionner les limites** :
   - Petit échantillon (52 pour Besançon)
   - Perte d'efficacité importante (41%)
   - Convergence non atteinte (écart relatif max 79%)

3. **Valoriser les deux niveaux** :
   - Besançon : Estimation de la demande locale
   - Tous : Compréhension des pratiques et motivations

### Pour améliorer le redressement

1. **Augmenter l'échantillon** : Viser 200+ répondants Besançon
2. **Élargir le territoire** : Redresser sur Besançon Grand (plus de marges)
3. **Simplifier les marges** : Utiliser moins de variables (âge + sexe uniquement)
4. **Post-stratification** : Alternative au raking si convergence difficile

## Commandes Utiles

### Préparer les données
```bash
python scripts/prepare_bob_with_all_respondents.py
```

### Lancer l'analyse complète
```bash
python scripts/run_analysis_with_filters.py
```

### Vérifier les exclusions
```bash
python scripts/simple_exclusion_analysis.py
```

## Conclusion

Cette stratégie permet de :
- ✅ **Conserver tous les répondants** (pas de perte de données)
- ✅ **Redresser correctement** (sur Besançon uniquement)
- ✅ **Analyser à deux niveaux** (local et général)
- ✅ **Interpréter clairement** (périmètre explicite)
- ✅ **Rester transparent** (limites connues et documentées)

L'approche est **pragmatique, rigoureuse et reproductible**.

