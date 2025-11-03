# Guide - Budget Prévisionnel BOB

## 🎯 Objectif

Estimer les **revenus potentiels** de la bibliothèque d'objets en fonction de différents scénarios et profils de clients.

---

## 📊 Résultats des Scénarios

### **Scénario PESSIMISTE** 😟
- **Adhérents** : 539
- **Revenus annuels** : **21,542 €**
  - Cotisations : 5,386 €
  - Locations : 16,157 €

**Hypothèses** :
- Taux de conversion : 3% (des intéressés deviennent adhérents)
- Cotisation : 10 €/an
- Locations : 5/an par adhérent à 6 €

---

### **Scénario REALISTE** 😊
- **Adhérents** : 898
- **Revenus annuels** : **85,271 €**
  - Cotisations : 13,464 €
  - Locations : 71,807 €

**Hypothèses** :
- Taux de conversion : 5%
- Cotisation : 15 €/an
- Locations : 10/an par adhérent à 8 €

---

### **Scénario OPTIMISTE** 🚀
- **Adhérents** : 1,436
- **Revenus annuels** : **244,144 €**
  - Cotisations : 28,723 €
  - Locations : 215,421 €

**Hypothèses** :
- Taux de conversion : 8%
- Cotisation : 20 €/an
- Locations : 15/an par adhérent à 10 €

---

### **Scénario CIBLE** 🎯
- **Adhérents** : 1,369
- **Revenus annuels** : **130,044 €**
  - Cotisations : 20,533 €
  - Locations : 109,511 €

**Hypothèses** :
- Taux de conversion **variable par profil** :
  - 10% pour les profils très intéressés (>80%)
  - 7% pour les profils moyennement intéressés (60-80%)
  - 3% pour les profils peu intéressés (<60%)
- Cotisation : 15 €/an
- Locations : 10/an par adhérent à 8 €

---

## 📈 Top 5 Profils Contributeurs (Scénario Réaliste)

| Rang | Profil | Revenus | Adhérents |
|------|--------|---------|-----------|
| 1 | **Femmes 18-24 ans Actives** | 7,107 € | 75 |
| 2 | **Hommes 18-24 ans Actifs** | 6,128 € | 65 |
| 3 | **Femmes 35-44 ans Actives** | 5,064 € | 53 |
| 4 | **Hommes 25-34 ans Actifs** | 4,868 € | 51 |
| 5 | **Femmes 65+ ans Actives** | 4,818 € | 51 |

---

## 🔧 Fichiers Générés

### 1. **Budget Prévisionnel Excel**
📁 `outputs/reports/budget_previsionnel_YYYYMMDD_HHMMSS.xlsx`

**Contenu** :
- **Onglet "Synthese"** : Comparaison des 4 scénarios
- **Onglet "Pessimiste"** : Détail par profil (36 profils)
- **Onglet "Realiste"** : Détail par profil
- **Onglet "Optimiste"** : Détail par profil
- **Onglet "Cible"** : Détail par profil

**Colonnes par profil** :
- Profil (âge + sexe + CSP)
- Population INSEE
- % Intérêt
- Nb Intéressés
- Taux de conversion
- Nb Adhérents
- Revenus Cotisations
- Revenus Locations
- **Revenus Totaux**

---

### 2. **Template de Paramètres**
📁 `outputs/reports/budget_template_parametres.xlsx`

**Utilisation** :
1. Ouvrir le fichier
2. Modifier les valeurs des paramètres
3. Ajouter de nouvelles colonnes pour créer vos scénarios
4. Relancer le script

**Paramètres modifiables** :
- `taux_conversion_%` : 3-10%
- `cotisation_annuelle_EUR` : 10-30 €
- `nb_locations_an` : 5-20
- `prix_location_moyen_EUR` : 5-15 €

---

## 🚀 Comment Utiliser

### **Générer le Budget**

```bash
cd D:\python_work\bob-enquete
python scripts/budget_simulator.py
```

**Sortie** :
- Fichier Excel avec 4 scénarios
- Template de paramètres

---

### **Créer Vos Propres Scénarios**

#### Méthode 1 : Modifier le script

Éditez `scripts/budget_simulator.py` et ajoutez un nouveau scénario :

```python
# Scénario 5 : Votre scénario personnalisé
scenarios['mon_scenario'] = simulate_budget(df_potential, {
    'taux_conversion': 6,  # 6% d'adhésion
    'cotisation_annuelle': 18,  # 18€/an
    'nb_locations_an': 12,  # 12 locations/an
    'prix_location_moyen': 9  # 9€/location
})
```

#### Méthode 2 : Utiliser le template Excel

1. Ouvrir `budget_template_parametres.xlsx`
2. Ajouter une colonne "Mon_Scenario"
3. Remplir les valeurs
4. Utiliser ces valeurs dans votre analyse

---

## 💡 Variables à Faire Varier

### **1. Taux de Conversion** (% intéressés → adhérents)

**Impact** : ×3 entre pessimiste (3%) et optimiste (8%)

**Facteurs d'influence** :
- Qualité de la communication
- Facilité d'inscription
- Offre d'objets disponibles
- Bouche-à-oreille

**Recommandation** : Commencer à 3-5% la 1ère année, viser 8-10% à terme

---

### **2. Cotisation Annuelle** (€/an)

**Impact** : ×2 entre pessimiste (10€) et optimiste (20€)

**Facteurs d'influence** :
- Acceptabilité (63.5% acceptent de payer)
- Services inclus
- Concurrence
- Valeur perçue

**Recommandation** : 15€ (scénario réaliste) avec options 10€ (réduit) et 25€ (premium)

---

### **3. Nombre de Locations/An** (par adhérent)

**Impact** : ×3 entre pessimiste (5) et optimiste (15)

**Facteurs d'influence** :
- Catalogue d'objets
- Disponibilité
- Facilité de réservation
- Satisfaction client

**Recommandation** : Viser 10-12 locations/an (1/mois)

---

### **4. Prix Moyen de Location** (€/jour)

**Impact** : ×1.7 entre pessimiste (6€) et optimiste (10€)

**Facteurs d'influence** :
- Valeur des objets
- Durée de location
- Concurrence (achat/location ailleurs)
- Seuil psychologique (61.5% max 10€)

**Recommandation** : 8€ en moyenne (5-10€ selon objets)

---

## 📊 Analyse de Sensibilité

### **Quel paramètre a le plus d'impact ?**

| Paramètre | Variation | Impact sur Revenus |
|-----------|-----------|-------------------|
| **Nb locations/an** | 5 → 15 | **×3** (le plus important) |
| **Taux conversion** | 3% → 8% | ×2.7 |
| **Cotisation** | 10€ → 20€ | ×2 |
| **Prix location** | 6€ → 10€ | ×1.7 |

**Conclusion** : Priorité à **augmenter le nombre de locations** par adhérent !

---

## 🎯 Recommandations Stratégiques

### **Phase 1 : Lancement (Année 1)**

**Objectif** : 500-600 adhérents

**Tarification** :
- Cotisation : 10-15€/an
- Location : 5-8€/jour
- Offre découverte : 1er mois gratuit

**Revenus estimés** : 20,000 - 30,000 €

---

### **Phase 2 : Développement (Année 2-3)**

**Objectif** : 900-1,200 adhérents

**Tarification** :
- Cotisation : 15€/an (standard) + 25€ (premium)
- Location : 8€/jour en moyenne
- Fidélité : -20% après 10 locations

**Revenus estimés** : 80,000 - 120,000 €

---

### **Phase 3 : Maturité (Année 4+)**

**Objectif** : 1,400-1,800 adhérents

**Tarification** :
- Cotisation : 15-20€/an
- Location : 8-10€/jour
- Abonnements : Forfaits illimités à 50€/mois

**Revenus estimés** : 150,000 - 250,000 €

---

## 🔍 Analyses Complémentaires Possibles

### **Par Profil**

Créer des offres ciblées :
- **Étudiants** : Tarif réduit (5€/an)
- **Familles** : Forfait famille (30€/an pour 2 adultes)
- **Seniors** : Livraison incluse (25€/an)

### **Par Type d'Objet**

Différencier les prix :
- **Petit outillage** : 5€/jour
- **Gros électroménager** : 10€/jour
- **Loisirs** : 8€/jour
- **Événementiel** : 15€/jour

### **Par Saisonnalité**

Adapter les prix :
- **Haute saison** (printemps/été) : +20%
- **Basse saison** (hiver) : -20%
- **Promotions** : Mois thématiques

---

## 📁 Fichiers à Consulter

1. **Budget prévisionnel** : `outputs/reports/budget_previsionnel_*.xlsx`
2. **Template paramètres** : `outputs/reports/budget_template_parametres.xlsx`
3. **Analyse par profil** : Résultats de `analyze_interest_by_profile.py`
4. **Synthèse exécutive** : `outputs/reports/synthese_executive_*.pdf`

---

## 🚀 Commandes Utiles

```bash
# Générer le budget prévisionnel
python scripts/budget_simulator.py

# Régénérer avec nouvelles données
python scripts/prepare_bob_with_all_respondents.py
python scripts/budget_simulator.py

# Voir tous les scénarios
cd outputs/reports
ls budget_previsionnel_*.xlsx
```

---

## 💡 Conseils d'Utilisation

### **Pour la Décision**

✅ Utiliser le **scénario réaliste** comme base (85k€/an)

✅ Prévoir une **marge de sécurité** : -20% (68k€/an)

✅ Fixer un **objectif ambitieux** : scénario optimiste (244k€/an)

### **Pour le Business Plan**

✅ Présenter les **3 scénarios** (pessimiste, réaliste, optimiste)

✅ Détailler les **hypothèses** de chaque scénario

✅ Montrer la **sensibilité** aux paramètres clés

### **Pour le Pilotage**

✅ Suivre les **KPIs** mensuellement :
- Nombre d'adhérents
- Taux de conversion
- Nombre de locations/adhérent
- Panier moyen

✅ Ajuster les **paramètres** selon les résultats réels

---

## ✅ Checklist

- [ ] Budget prévisionnel généré
- [ ] Scénarios comparés
- [ ] Profils contributeurs identifiés
- [ ] Paramètres clés définis
- [ ] Sensibilité analysée
- [ ] Recommandations formulées
- [ ] Business plan intégré

---

**Le simulateur de budget est prêt à l'emploi !** 🎉

Vous pouvez maintenant faire varier tous les paramètres pour affiner vos prévisions.

