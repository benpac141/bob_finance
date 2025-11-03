# Application Interactive - Simulateur BOB

## 🎯 Présentation

Une **application web interactive** avec des curseurs pour ajuster les paramètres en temps réel et voir les résultats instantanément !

---

## 🚀 Installation

### **1. Installer Streamlit et Plotly**

```bash
pip install streamlit plotly
```

---

## ▶️ Lancement

### **Commande**

```bash
cd D:\python_work\bob-enquete
python -m streamlit run scripts/app_simulation_interactive.py
```

**L'application s'ouvre automatiquement dans votre navigateur** à l'adresse :
```
http://localhost:8501
```

---

## 🎛️ Fonctionnalités

### **Curseurs Interactifs** (Barre latérale)

#### **1. Nombre d'Adhérents Cible**
- **Min** : 100
- **Max** : 3,000
- **Défaut** : 1,000
- **Pas** : 50

→ Ajustez pour voir l'impact sur les revenus

---

#### **2. Ajustement Cotisation (%)**
- **Min** : -50% (réduction)
- **Max** : +100% (doublement)
- **Défaut** : 0%
- **Pas** : 5%

→ Testez différents niveaux de cotisation

---

#### **3. Ajustement Prix Location (%)**
- **Min** : -50%
- **Max** : +100%
- **Défaut** : 0%
- **Pas** : 5%

→ Évaluez l'impact du prix sur les revenus

---

#### **4. Ajustement Fréquence d'Usage (%)**
- **Min** : -50%
- **Max** : +100%
- **Défaut** : 0%
- **Pas** : 5%

→ Simulez une augmentation de l'usage

---

### **Affichage en Temps Réel**

#### **Métriques Principales**
- 👥 **Adhérents** : Nombre et % de conversion
- 💶 **Cotisations** : Total et par adhérent
- 🔄 **Locations** : Total et fréquence moyenne
- 💰 **Revenus Totaux** : Total et par adhérent

---

#### **4 Onglets d'Analyse**

**1. Vue d'ensemble** 📈
- Répartition des revenus (camembert)
- Distribution par âge (barres)
- Distribution par sexe (camembert)
- Distribution par CSP (barres)

**2. Profils** 👥
- Top 10 des profils contributeurs (tableau)
- Graphique des revenus par profil (barres)

**3. Revenus** 💰
- Revenus par tranche d'âge (barres)
- Revenus par CSP (barres)
- Heatmap revenus (âge × sexe)

**4. Détails** 📊
- Tableau complet des 36 profils
- Filtres par âge, sexe, CSP
- Export CSV

---

## 🎮 Exemples d'Utilisation

### **Scénario 1 : Lancement Prudent**

**Paramètres** :
- Adhérents : 500
- Cotisation : -20% (réduction pour attirer)
- Prix location : -10% (compétitif)
- Fréquence : 0% (base)

**Résultat** : ~35,000 € de revenus

---

### **Scénario 2 : Développement**

**Paramètres** :
- Adhérents : 1,000
- Cotisation : 0%
- Prix location : 0%
- Fréquence : +20% (fidélisation)

**Résultat** : ~108,000 € de revenus

---

### **Scénario 3 : Optimiste**

**Paramètres** :
- Adhérents : 1,500
- Cotisation : +30%
- Prix location : +20%
- Fréquence : +50%

**Résultat** : ~240,000 € de revenus

---

### **Scénario 4 : Stress Test**

**Paramètres** :
- Adhérents : 2,500
- Cotisation : +50%
- Prix location : +50%
- Fréquence : +80%

**Résultat** : Voir les limites du modèle

---

## 📊 Visualisations Disponibles

### **Graphiques Interactifs** (Plotly)

✅ **Camemberts** : Répartition revenus, sexe  
✅ **Barres horizontales** : Top profils, âge, CSP  
✅ **Barres verticales** : Revenus par segment  
✅ **Heatmap** : Revenus croisés (âge × sexe)  

**Interaction** :
- Survolez pour voir les détails
- Cliquez sur la légende pour filtrer
- Zoomez avec la souris
- Exportez en PNG (icône appareil photo)

---

## 💡 Cas d'Usage

### **1. Présentation aux Décideurs**

Lancez l'app et ajustez en direct selon les questions :
- "Et si on avait 800 adhérents ?" → Ajustez le curseur
- "Et si on baissait la cotisation ?" → Ajustez le curseur
- "Quels sont les profils clés ?" → Onglet "Profils"

---

### **2. Planification Stratégique**

Testez différents scénarios :
- Année 1 : 500 adhérents, -20% cotisation
- Année 2 : 1,000 adhérents, 0%
- Année 3 : 1,500 adhérents, +20%

Comparez les revenus et la distribution.

---

### **3. Analyse de Sensibilité**

Identifiez le paramètre le plus impactant :
- Variez **uniquement** la fréquence : +50% → Impact ?
- Variez **uniquement** le prix : +50% → Impact ?
- Variez **uniquement** la cotisation : +50% → Impact ?

**Résultat** : La fréquence a le plus d'impact !

---

### **4. Export pour Rapport**

1. Ajustez les paramètres
2. Capturez les graphiques (icône appareil photo)
3. Téléchargez le CSV (onglet "Détails")
4. Intégrez dans votre rapport

---

## 🔧 Personnalisation

### **Modifier les Limites des Curseurs**

Éditez `scripts/app_simulation_interactive.py` :

```python
# Ligne ~90
nb_adherents = st.sidebar.slider(
    "Nombre d'adhérents cible",
    min_value=100,      # Changez ici
    max_value=5000,     # Changez ici
    value=1000,
    step=100            # Changez le pas
)
```

---

### **Ajouter un Nouveau Curseur**

```python
# Après les curseurs existants
ajust_duree = st.sidebar.slider(
    "Durée moyenne location (jours)",
    min_value=1,
    max_value=7,
    value=3,
    step=1
)

# Utiliser dans les calculs
df_result['revenus_locations'] = df_result['revenus_locations'] * (ajust_duree / 3)
```

---

## 🎨 Captures d'Écran

### **Interface Principale**
```
┌─────────────────────────────────────────────────────────┐
│  📊 Simulateur de Budget Interactif - BOB              │
│  Bibliothèque d'Objets Besançon                        │
├─────────────────────────────────────────────────────────┤
│  👥 Adhérents    💶 Cotisations   🔄 Locations   💰 Total│
│  1,000          11,016 €         78,719 €       89,735 €│
├─────────────────────────────────────────────────────────┤
│  [Onglets: Vue d'ensemble | Profils | Revenus | Détails]│
│                                                          │
│  [Graphiques interactifs...]                            │
└─────────────────────────────────────────────────────────┘
```

### **Barre Latérale**
```
┌─────────────────────┐
│ 🎛️ Paramètres       │
├─────────────────────┤
│ 📈 Objectif         │
│ [====●====] 1,000   │
│                     │
│ 💰 Tarifs           │
│ Cotisation: 0%      │
│ Prix: 0%            │
│                     │
│ 🔄 Fréquence        │
│ Usage: 0%           │
│                     │
│ [🔄 Réinitialiser]  │
└─────────────────────┘
```

---

## ⚡ Raccourcis Clavier

- **R** : Relancer l'application
- **C** : Effacer le cache
- **Ctrl+C** : Arrêter l'application (dans le terminal)

---

## 🆘 Dépannage

### **Erreur "Module not found: streamlit"**
```bash
pip install streamlit plotly
```

### **L'application ne se lance pas**
```bash
# Vérifier l'installation
streamlit --version

# Relancer
streamlit run scripts/app_simulation_interactive.py
```

### **Port déjà utilisé**
```bash
# Utiliser un autre port
streamlit run scripts/app_simulation_interactive.py --server.port 8502
```

### **Données non chargées**
→ Vérifier que `data/raw/enquete_all_prepared.xlsx` existe  
→ Relancer `python scripts/prepare_bob_with_all_respondents.py`

---

## 📚 Documentation Streamlit

- **Site officiel** : https://streamlit.io
- **Documentation** : https://docs.streamlit.io
- **Galerie d'exemples** : https://streamlit.io/gallery

---

## ✅ Checklist

- [ ] Streamlit installé (`pip install streamlit plotly`)
- [ ] Données préparées (`enquete_all_prepared.xlsx` existe)
- [ ] Application lancée (`streamlit run ...`)
- [ ] Navigateur ouvert sur `http://localhost:8501`
- [ ] Curseurs testés
- [ ] Graphiques consultés
- [ ] CSV exporté

---

## 🎉 Avantages

✅ **Interactif** : Ajustez en temps réel  
✅ **Visuel** : Graphiques dynamiques  
✅ **Intuitif** : Interface simple  
✅ **Complet** : 4 onglets d'analyse  
✅ **Exportable** : CSV et PNG  
✅ **Partageable** : URL à partager  

---

**Lancez l'application et explorez les scénarios !** 🚀

```bash
streamlit run scripts/app_simulation_interactive.py
```

