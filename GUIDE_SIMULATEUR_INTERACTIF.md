# Guide - Simulateur de Budget Interactif

## 🎯 Fonctionnalités

Le simulateur **redistribue automatiquement** les adhérents par profil selon :
- ✅ **L'intérêt du profil** (% "Oui" dans l'enquête)
- ✅ **La population du profil** (données INSEE)
- ✅ **Les comportements du profil** (cotisation préférée, fréquence d'usage, prix accepté)

---

## 📊 Résultats des Simulations

### **500 Adhérents** (Année 1)
- **Revenus annuels** : **44,941 €**
  - Cotisations : 5,495 €
  - Locations : 39,445 €
- **Revenu/adhérent** : 90 €/an
- **Distribution** :
  - 25% de 18-24 ans
  - 54% de femmes
  - 61% d'actifs

---

### **1,000 Adhérents** (Année 2)
- **Revenus annuels** : **89,735 €**
  - Cotisations : 11,016 €
  - Locations : 78,719 €
- **Revenu/adhérent** : 90 €/an
- **Distribution** : Identique (proportionnelle)

---

### **1,500 Adhérents** (Année 3)
- **Revenus annuels** : **134,613 €**
  - Cotisations : 16,531 €
  - Locations : 118,082 €
- **Revenu/adhérent** : 90 €/an

---

### **2,000 Adhérents** (Long terme)
- **Revenus annuels** : **179,544 €**
  - Cotisations : 22,064 €
  - Locations : 157,481 €
- **Revenu/adhérent** : 90 €/an

---

## 🔧 Comment Ça Marche

### **1. Distribution Automatique par Profil**

Pour chaque profil (36 au total : 6 âges × 2 sexes × 3 CSP) :

```
Score d'attractivité = % Intérêt × Population INSEE

% Distribution = Score profil / Total scores

Nb adhérents profil = % Distribution × Objectif total
```

**Exemple** : Femmes 25-34 ans Actives
- % Intérêt : 87.5%
- Population : 2,068
- Score : 87.5 × 2,068 = 180,950
- Si objectif = 1,000 et total scores = 1,795,200
- → Distribution = 180,950 / 1,795,200 = 10.1%
- → Adhérents = 10.1% × 1,000 = **101 adhérents**

---

### **2. Comportements par Profil**

#### **Cotisation Préférée**
Extraite des réponses à l'enquête :
- "Oui, entre 1€ et 10€" → 5 €
- "Oui, entre 10€ et 20€" → 15 €
- "Oui, entre 20€ et 30€" → 25 €
- "Non" → 0 €

**Moyenne par profil** : 11.5 €

#### **Fréquence d'Usage** (nb locations/an)
Calculée selon :
- **Expérience** : Si déjà utilisé → +30%
- **Âge** : Jeunes (18-34) → +20%, Seniors (65+) → -20%
- **CSP** : Actifs → +10%, Étudiants → -10%, Retraités → -30%

**Base** : 10 locations/an  
**Moyenne** : 9.6 locations/an

#### **Prix Accepté**
Extrait de "Prix maximum de location" :
- Moyenne : 8.6 €/location
- Utilisé à 80% (prix réel = 80% du max accepté)

---

### **3. Calcul des Revenus**

```
Revenus cotisations = Nb adhérents × Cotisation préférée

Revenus locations = Nb adhérents × Nb locations/an × Prix × 0.8

Revenus totaux = Cotisations + Locations
```

---

## 🚀 Utilisation

### **Générer les Simulations**

```bash
cd D:\python_work\bob-enquete
python scripts/budget_simulator_interactive.py
```

**Sortie** : `outputs/reports/budget_interactif_YYYYMMDD_HHMMSS.xlsx`

---

### **Créer Vos Propres Objectifs**

#### Méthode 1 : Modifier le script

Ouvrez `scripts/budget_simulator_interactive.py` et ajoutez :

```python
# Ligne ~290
simulations['1200_adherents'] = generate_simulation(
    1200,  # Votre objectif
    df_behaviors, margins, "1200 adherents"
)
```

Puis relancez :
```bash
python scripts/budget_simulator_interactive.py
```

#### Méthode 2 : Créer un script personnalisé

```python
from budget_simulator_interactive import *

# Charger les données
df, margins = load_data()
df_behaviors = analyze_profile_behaviors(df)

# Vos objectifs
objectifs = [300, 600, 900, 1200, 1800, 2500]

simulations = {}
for obj in objectifs:
    simulations[f'{obj}_adherents'] = generate_simulation(
        obj, df_behaviors, margins, f"{obj} adherents"
    )

# Exporter
export_simulation_excel(simulations, 'mon_budget.xlsx')
```

---

## 📈 Analyses Disponibles dans Excel

### **Onglet "Synthese"**

| Colonne | Description |
|---------|-------------|
| Scenario | Nom du scénario |
| Nb_Adherents | Objectif d'adhérents |
| Cotisation_Moyenne_EUR | Cotisation moyenne par profil |
| Locations_Moyenne_An | Nb moyen de locations/an |
| Prix_Moyen_EUR | Prix moyen de location |
| Revenus_Cotisations_EUR | Total cotisations |
| Revenus_Locations_EUR | Total locations |
| Revenus_Totaux_EUR | Total revenus |
| Revenu_Par_Adherent_EUR | Revenu moyen/adhérent |

---

### **Onglets par Scénario**

Pour chaque profil (36 lignes) :

| Colonne | Description |
|---------|-------------|
| Profil | Age_Sexe_CSP |
| Age | Tranche d'âge |
| Sexe | F ou M |
| CSP | Actifs / Étudiants / Retraités |
| Population | Population INSEE du profil |
| Interet_% | % d'intérêt dans l'enquête |
| Distribution_% | % de la distribution totale |
| **Nb_Adherents** | **Nombre d'adhérents du profil** |
| Cotisation_EUR | Cotisation préférée |
| Locations_An | Nb de locations/an |
| Prix_Moyen_EUR | Prix moyen accepté |
| Revenus_Cotisations_EUR | Revenus cotisations |
| Revenus_Locations_EUR | Revenus locations |
| **Revenus_Totaux_EUR** | **Revenus totaux du profil** |

**Dernière ligne** : TOTAL (somme de tous les profils)

---

## 💡 Cas d'Usage

### **1. Planifier la Croissance**

Simulez plusieurs années :
- Année 1 : 500 adhérents → 45k€
- Année 2 : 1,000 adhérents → 90k€
- Année 3 : 1,500 adhérents → 135k€
- Année 5 : 2,000 adhérents → 180k€

**Visualisez** la courbe de croissance des revenus.

---

### **2. Identifier les Profils Clés**

Pour chaque objectif, consultez le Top 5 des profils contributeurs.

**Exemple** (1,000 adhérents) :
1. Femmes 18-24 ans Actives : 8,577 € (82 adhérents)
2. Hommes 25-34 ans Actifs : 8,037 € (57 adhérents)
3. Hommes 18-24 ans Actifs : 7,531 € (72 adhérents)

**Action** : Cibler ces profils en priorité !

---

### **3. Optimiser la Stratégie Marketing**

Selon la distribution automatique :
- **25% de 18-24 ans** → Communication sur réseaux sociaux
- **54% de femmes** → Messages adaptés
- **61% d'actifs** → Horaires d'ouverture étendus

---

### **4. Prévoir les Ressources**

**Catalogue d'objets** :
- 1,000 adhérents × 9.6 locations/an = **9,600 locations/an**
- Si durée moyenne = 3 jours → **79 locations/jour**
- Si taux de rotation = 50% → **158 objets minimum**

**Personnel** :
- 1 personne peut gérer ~50 locations/semaine
- 79 locations/jour × 5 jours = 395/semaine
- → **8 ETP nécessaires**

---

## 🔍 Analyses Avancées

### **Sensibilité au Comportement**

Modifiez les comportements dans `analyze_profile_behaviors()` :

```python
# Augmenter la fréquence d'usage de 20%
df_rev['nb_locations_an'] = df_rev['nb_locations_an'] * 1.2

# Augmenter le prix accepté de 10%
df_rev['prix_max_location'] = df_rev['prix_max_location'] * 1.1
```

**Impact** : Revenus × 1.32 !

---

### **Segmentation Fine**

Créer des sous-objectifs par segment :

```python
# Objectif : 1,000 adhérents
# Dont 60% d'actifs (600)
# Dont 40% d'autres (400)

# Filtrer les actifs
df_actifs = df_dist[df_dist['csp'] == 'Actifs']
# Ajuster pour atteindre 600
# ...
```

---

### **Scénarios "Et Si"**

**Et si on doublait la fréquence d'usage ?**
```python
df_rev['nb_locations_an'] = df_rev['nb_locations_an'] * 2
# Revenus locations × 2 !
```

**Et si on augmentait la cotisation de 5€ ?**
```python
df_rev['cotisation_preferee'] = df_rev['cotisation_preferee'] + 5
# Revenus cotisations + (5€ × nb_adherents)
```

---

## 📊 Comparaison des Simulateurs

| Fonctionnalité | Simulateur Simple | Simulateur Interactif |
|----------------|-------------------|----------------------|
| **Objectif** | Scénarios prédéfinis | **Objectif d'adhérents** |
| **Distribution** | Fixe par scénario | **Automatique par profil** |
| **Comportements** | Moyennes globales | **Par profil (enquête)** |
| **Flexibilité** | 4 scénarios | **Illimitée** |
| **Utilisation** | Comparaison rapide | **Planification détaillée** |

**Recommandation** : Utilisez les **deux** !
- Simple → Vue d'ensemble
- Interactif → Planification fine

---

## ✅ Checklist d'Utilisation

- [ ] Simulateur exécuté
- [ ] Fichier Excel généré
- [ ] Onglet "Synthèse" consulté
- [ ] Profils contributeurs identifiés
- [ ] Distribution par âge/sexe/CSP analysée
- [ ] Objectifs personnalisés créés
- [ ] Ressources nécessaires estimées
- [ ] Stratégie marketing adaptée

---

## 🚀 Prochaines Étapes

1. **Définir votre objectif** d'adhérents (500, 1000, 1500, 2000 ?)
2. **Générer la simulation** correspondante
3. **Analyser la distribution** par profil
4. **Adapter votre stratégie** marketing et opérationnelle
5. **Suivre les KPIs** mensuellement et ajuster

---

**Le simulateur interactif est votre outil de pilotage stratégique !** 🎯📊

Ajustez simplement le nombre d'adhérents cible, et tout se recalcule automatiquement selon les profils et leurs comportements réels.

