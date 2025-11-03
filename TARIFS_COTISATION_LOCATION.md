# 💶 Système de Tarification - Application BOB

## 📋 Vue d'Ensemble

L'application interactive a été mise à jour pour gérer des **tarifs en euros** avec un **système de cotisation à trois niveaux** adapté aux profils des adhérents.

---

## 💰 Tarifs de Cotisation

### **Trois Niveaux de Cotisation**

| Type | Tarif par défaut | Public cible |
|------|------------------|--------------|
| **Solidaire** | 5 € / an | Étudiants, chômeurs, petits budgets |
| **Normal** | 10 € / an | Tarif standard pour la majorité |
| **Soutien** | 20 € / an | Ceux qui souhaitent soutenir davantage |

### **Attribution Automatique par Profil**

Le système attribue automatiquement les tarifs selon le profil démographique :

#### **Tarif Solidaire (80% solidaire, 20% normal)**
- Étudiants / Chômeurs (toutes tranches d'âge)
- Jeunes 18-24 ans (toutes CSP)

#### **Tarif Normal + Soutien (10% solidaire, 60% normal, 30% soutien)**
- Retraités 55+ ans
- Capacité contributive variable

#### **Tarif Normal + Soutien (5% solidaire, 55% normal, 40% soutien)**
- Actifs 45-64 ans
- Revenus plus élevés, plus de soutiens

#### **Tarif Standard (10% solidaire, 80% normal, 10% soutien)**
- Tous les autres profils
- Répartition équilibrée

---

## 🏠 Tarif de Location

### **Prix par Jour**

| Paramètre | Valeur par défaut | Ajustable |
|-----------|-------------------|-----------|
| **Prix moyen location** | 3 € / jour | 0 € à 20 € |

**Utilisation** : Ce prix est appliqué uniformément à toutes les locations, quelle que soit la catégorie d'adhérent.

---

## 🎛️ Interface de l'Application

### **Paramètres Ajustables**

Dans la barre latérale gauche, vous pouvez ajuster :

#### **1. Cotisation annuelle (€)**
```
Tarif Solidaire    : [  5 €] (0-50€)
Tarif Normal       : [ 10 €] (0-100€)
Tarif Soutien      : [ 20 €] (0-200€)
```

#### **2. Prix de location (€/jour)**
```
Prix moyen location: [ 3.0 €] (0-20€)
```

#### **3. Fréquence d'Usage**
```
Ajustement fréquence: [ 0 %] (-50% à +100%)
```

---

## 📊 Affichage des Résultats

### **Section "Répartition des Cotisations"**

Après les métriques principales, une nouvelle section affiche :

```
💶 Répartition des Cotisations

┌─────────────────┬─────────────────┬─────────────────┐
│ Tarif Solidaire │  Tarif Normal   │  Tarif Soutien  │
│      (5€)       │      (10€)      │      (20€)      │
├─────────────────┼─────────────────┼─────────────────┤
│   150 adhérents │   700 adhérents │   150 adhérents │
│      15.0%      │      70.0%      │      15.0%      │
└─────────────────┴─────────────────┴─────────────────┘
```

### **Onglet "Vue d'ensemble"**

Un nouveau graphique en camembert montre la répartition des cotisations :

- 🟠 **Solidaire** (5€)
- 🔵 **Normal** (10€)
- 🟢 **Soutien** (20€)

### **Onglet "Détails"**

Le tableau détaillé inclut maintenant :

| Colonne | Description |
|---------|-------------|
| **Nb Solidaire** | Nombre d'adhérents au tarif solidaire |
| **Nb Normal** | Nombre d'adhérents au tarif normal |
| **Nb Soutien** | Nombre d'adhérents au tarif soutien |
| **Cotis. Moy. (€)** | Cotisation moyenne pour ce profil |

---

## 💡 Exemples de Calcul

### **Exemple 1 : Profil Étudiant 18-24 ans**

**Répartition** : 80% solidaire, 20% normal

Pour 100 adhérents :
- 80 × 5€ = 400€
- 20 × 10€ = 200€
- **Total** : 600€
- **Moyenne** : 6€/adhérent

### **Exemple 2 : Profil Actif 45-54 ans**

**Répartition** : 5% solidaire, 55% normal, 40% soutien

Pour 100 adhérents :
- 5 × 5€ = 25€
- 55 × 10€ = 550€
- 40 × 20€ = 800€
- **Total** : 1,375€
- **Moyenne** : 13.75€/adhérent

### **Exemple 3 : Profil Retraité 65+ ans**

**Répartition** : 10% solidaire, 60% normal, 30% soutien

Pour 100 adhérents :
- 10 × 5€ = 50€
- 60 × 10€ = 600€
- 30 × 20€ = 600€
- **Total** : 1,250€
- **Moyenne** : 12.50€/adhérent

---

## 🔄 Calcul des Revenus

### **Revenus de Cotisations**

```
Revenus Cotisations = Σ (nb_adherents × cotisation_moyenne)
```

Pour chaque profil :
```
cotisation_moyenne = (nb_solidaire × tarif_solidaire + 
                      nb_normale × tarif_normal + 
                      nb_soutien × tarif_soutien) / nb_adherents
```

### **Revenus de Locations**

```
Revenus Locations = Σ (nb_adherents × nb_locations_an × prix_location)
```

**Note** : Le prix de location est le même pour tous les adhérents.

### **Revenus Totaux**

```
Revenus Totaux = Revenus Cotisations + Revenus Locations
```

---

## 🎯 Cas d'Usage

### **Scénario 1 : Tarif Solidaire Renforcé**

**Objectif** : Maximiser l'accessibilité

**Paramètres** :
- Tarif Solidaire : 3€
- Tarif Normal : 8€
- Tarif Soutien : 15€
- Prix location : 2.5€

**Résultat** : Revenus plus faibles, mais plus d'adhérents potentiels

---

### **Scénario 2 : Tarif Équilibré**

**Objectif** : Équilibre accessibilité / viabilité

**Paramètres** :
- Tarif Solidaire : 5€
- Tarif Normal : 10€
- Tarif Soutien : 20€
- Prix location : 3€

**Résultat** : Revenus modérés, bon équilibre

---

### **Scénario 3 : Tarif Soutien**

**Objectif** : Maximiser les revenus

**Paramètres** :
- Tarif Solidaire : 8€
- Tarif Normal : 15€
- Tarif Soutien : 30€
- Prix location : 4€

**Résultat** : Revenus élevés, mais risque de perte d'adhérents

---

## 📈 Impact sur les Budgets

### **Avec 1,000 Adhérents**

#### **Scénario Solidaire** (3€ / 8€ / 15€)
- Cotisations : ~8,500€
- Locations (3€) : ~30,000€
- **Total** : ~38,500€

#### **Scénario Équilibré** (5€ / 10€ / 20€)
- Cotisations : ~10,500€
- Locations (3€) : ~30,000€
- **Total** : ~40,500€

#### **Scénario Soutien** (8€ / 15€ / 30€)
- Cotisations : ~16,000€
- Locations (4€) : ~40,000€
- **Total** : ~56,000€

---

## 🔧 Modifications Techniques

### **Fichier Modifié**

`scripts/app_simulation_interactive.py`

### **Nouvelles Fonctions**

1. **`attribuer_type_cotisation(age_group, csp)`**
   - Détermine le type de cotisation pour un profil
   - Retourne : 'solidaire', 'normale', ou 'soutien'

2. **`calculer_repartition_cotisations(df_result, cotisation_solidaire, cotisation_normale, cotisation_soutien)`**
   - Calcule la répartition des adhérents par type de cotisation
   - Ajoute les colonnes : `nb_solidaire`, `nb_normale`, `nb_soutien`, `cotisation_moyenne`

### **Nouveaux Paramètres d'Entrée**

```python
cotisation_solidaire = st.sidebar.number_input("Tarif Solidaire", value=5)
cotisation_normale = st.sidebar.number_input("Tarif Normal", value=10)
cotisation_soutien = st.sidebar.number_input("Tarif Soutien", value=20)
prix_location = st.sidebar.number_input("Prix moyen location", value=3.0)
```

### **Nouveaux Affichages**

- Section "Répartition des Cotisations" avec 3 métriques
- Graphique en camembert des cotisations
- Colonnes supplémentaires dans le tableau détaillé

---

## ✅ Avantages du Système

### **Pour les Adhérents**

✅ **Équité sociale** : Tarifs adaptés aux capacités contributives  
✅ **Accessibilité** : Tarif solidaire pour les petits budgets  
✅ **Engagement** : Tarif soutien pour ceux qui veulent contribuer davantage  

### **Pour la BOB**

✅ **Viabilité financière** : Revenus diversifiés  
✅ **Inclusivité** : Ouverture à tous les publics  
✅ **Flexibilité** : Tarifs ajustables selon les besoins  
✅ **Transparence** : Répartition claire et visible  

### **Pour l'Analyse**

✅ **Précision** : Calculs basés sur les profils réels  
✅ **Réalisme** : Prise en compte des capacités contributives  
✅ **Simulation** : Test de différents scénarios tarifaires  
✅ **Visualisation** : Graphiques clairs de la répartition  

---

## 🚀 Utilisation

### **Lancer l'Application**

```bash
cd D:\python_work\bob-enquete
python -m streamlit run scripts/app_simulation_interactive.py
```

Ou double-clic sur : `lancer_app.bat`

### **Tester les Tarifs**

1. Ajuster les 3 tarifs de cotisation
2. Ajuster le prix de location
3. Observer la répartition automatique
4. Consulter les revenus calculés
5. Exporter les résultats

---

## 📚 Documentation Associée

- **README_FINAL.md** : Vue d'ensemble du projet
- **LANCEMENT_APP_INTERACTIVE.md** : Guide de l'application
- **GUIDE_SIMULATEUR_INTERACTIF.md** : Guide détaillé du simulateur
- **CORRECTION_APP.md** : Corrections appliquées

---

**Date de mise à jour** : 30 octobre 2025  
**Version** : 2.0 - Tarification en euros avec 3 niveaux  
**Statut** : ✅ Opérationnel


