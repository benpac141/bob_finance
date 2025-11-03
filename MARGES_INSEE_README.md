# Marges INSEE - Centre-ville de Besançon

## 📊 Source des données

**Fichier** : Recensement INSEE 2022  
**Zone** : 11 IRIS du centre-ville de Besançon  
**Population** : 7,341 adultes (18+)

## 🗺️ IRIS inclus

```
250560101, 250560102, 250560103, 250560104
250560302, 250560303, 250560304
250560401, 250560402
250560501, 250560502
```

## 📋 Variables de redressement

### 1. **age_group** : Tranche d'âge
- `18-24` : 18 à 24 ans (26,8%)
- `25-34` : 25 à 34 ans (21,3%)
- `35-44` : 35 à 44 ans (11,9%)
- `45-54` : 45 à 54 ans (11,6%)
- `55-64` : 55 à 64 ans (9,6%)
- `65+` : 65 ans et plus (18,8%)

### 2. **sexe** : Sexe
- `M` : Masculin (46,0%)
- `F` : Féminin (54,0%)

### 3. **csp** : Catégorie socio-professionnelle (basée sur TACT)
- `1` : Actifs occupés (54,8%)
- `2` : Étudiants / Chômeurs (25,8%)
- `3` : Retraités / Autres inactifs (19,4%)

## 📁 Fichier généré

**Emplacement** : `data/margins/margins_center.csv`

**Structure** :
```csv
code_iris,age_group,sexe,csp,population
250560101,18-24,F,1,45
250560101,18-24,F,2,38
...
```

**Statistiques** :
- 288 lignes (combinaisons IRIS × âge × sexe × CSP)
- Population min par cellule : 1
- Population max par cellule : 143
- Population moyenne par cellule : 25,5

## 🔄 Utilisation pour le redressement BOB

### Configuration requise dans `config.yaml`

```yaml
survey:
  weighting_vars:
    - "age_group"
    - "sexe"
    - "csp"
```

### Correspondance avec votre enquête BOB

Assurez-vous que votre fichier d'enquête contient ces variables avec les mêmes modalités :

1. **age_group** : Créer à partir de l'âge des répondants
2. **sexe** : M/F (mapper depuis votre variable genre)
3. **csp** : 1/2/3 (mapper depuis votre variable d'activité)

## 🛠️ Script de préparation

Le fichier a été généré avec :
```bash
python scripts/prepare_margins_from_insee.py
```

Ce script :
1. Charge le recensement INSEE 2022
2. Filtre sur les 11 IRIS centre-ville
3. Crée les tranches d'âge
4. Mappe le sexe (1→M, 2→F)
5. Mappe les CSP depuis TACT (type d'activité)
6. Agrège par IRIS × âge × sexe × CSP
7. Exporte vers CSV

## 📝 Notes

- Les données sont issues du recensement 2022 (données officielles INSEE)
- La population totale centre-ville (adultes 18+) est de 7,341 personnes
- Le centre-ville de Besançon a une forte proportion d'étudiants (26,8% de 18-24 ans)
- La répartition hommes/femmes est légèrement déséquilibrée (46% / 54%)

## ✅ Validation

Pour vérifier la qualité des marges après redressement, le pipeline calculera :
- **Deff** (Design Effect) : doit être < 2.0
- **n_eff** : taille d'échantillon effective
- **Écarts relatifs** : entre marges cibles et obtenues

---

**Date de création** : 29 octobre 2025  
**Source** : INSEE, Recensement 2022

