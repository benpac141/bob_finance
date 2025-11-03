# 🎨 GUIDE VISUEL - Projet BOB-Enquête

## 📊 Vue d'Ensemble du Projet

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJET BOB-ENQUÊTE                           │
│                  Analyse + Budget + Application                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────┬─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌────────┐          ┌────────────┐        ┌──────────┐
   │ DONNÉES│          │  ANALYSE   │        │ SORTIES  │
   └────────┘          └────────────┘        └──────────┘
        │                     │                     │
        │                     │                     │
   90 répondants      Redressement           9 fichiers
   11 IRIS            Segmentation           + App web
   25,381 hab.        Budgets                + Docs
```

---

## 🔄 Pipeline Complet

```
┌──────────────────────────────────────────────────────────────────────┐
│                         ÉTAPE 1 : DONNÉES                            │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  enquete_bob.xlsx (original)                │
        │  → 90 répondants                            │
        │  → 52 Besançon + 38 hors                    │
        └─────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  prepare_bob_with_all_respondents.py        │
        │  → Mapping des colonnes                     │
        │  → Ajout flag is_besancon                   │
        └─────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  enquete_all_prepared.xlsx                  │
        │  → Données nettoyées                        │
        │  → Variables standardisées                  │
        └─────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                      ÉTAPE 2 : REDRESSEMENT                          │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  margins_center.csv (INSEE)                 │
        │  → 11 IRIS Besançon centre                  │
        │  → Âge, Sexe, CSP                           │
        └─────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  raking.py (IPF)                            │
        │  → Algorithme itératif                      │
        │  → Convergence optimisée                    │
        └─────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  Poids calculés                             │
        │  → Deff = 1.67                              │
        │  → n_eff = 31.1                             │
        └─────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                       ÉTAPE 3 : ANALYSE                              │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  analysis.py                                │
        │  → Statistiques descriptives                │
        │  → Segmentation par profil                  │
        │  → Extrapolation à la population            │
        └─────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  Résultats                                  │
        │  → 69.2% d'intérêt                          │
        │  → ~17,571 personnes intéressées            │
        │  → 3 segments cibles                        │
        └─────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                       ÉTAPE 4 : SORTIES                              │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────┬─────────────┬─────────────┐
        │             │             │             │
        ▼             ▼             ▼             ▼
   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
   │  PDF   │   │ Excel  │   │  PNG   │   │  App   │
   └────────┘   └────────┘   └────────┘   └────────┘
        │             │             │             │
   2 rapports    2 budgets   5 dashboards  Streamlit
```

---

## 📁 Arborescence du Projet

```
bob-enquete/
│
├── 🚀 lancer_app.bat                    ← DOUBLE-CLIC ICI !
│
├── 📄 config.yaml                       ← Configuration
├── 📄 requirements.txt                  ← Dépendances
│
├── 📂 data/
│   ├── 📂 raw/
│   │   ├── 📊 enquete_bob.xlsx         ← Original
│   │   └── 📊 enquete_all_prepared.xlsx ← Préparé
│   └── 📂 margins/
│       └── 📊 margins_center.csv        ← Marges INSEE
│
├── 📂 outputs/
│   ├── 📂 reports/
│   │   ├── 📄 synthese_executive_*.pdf
│   │   ├── 📄 rapport_enrichi_*.pdf
│   │   ├── 📊 budget_previsionnel_*.xlsx
│   │   └── 📊 budget_interactif_*.xlsx
│   └── 📂 figures/
│       ├── 🖼️ dashboard_summary_*.png
│       ├── 🖼️ dashboard_heatmap_*.png
│       ├── 🖼️ dashboard_bars_*.png
│       ├── 🖼️ dashboard_pyramid_*.png
│       └── 🖼️ dashboard_contribution_*.png
│
├── 📂 src/                              ← Modules Python
│   ├── 🐍 utils.py
│   ├── 🐍 load_clean.py
│   ├── 🐍 raking.py
│   ├── 🐍 analysis.py
│   ├── 🐍 pdf_report.py
│   └── 🐍 pdf_report_enriched.py
│
├── 📂 scripts/                          ← Scripts
│   ├── 🎛️ app_simulation_interactive.py ← App web
│   ├── ⚙️ generate_all_reports.py      ← Script master
│   ├── ⚙️ generate_executive_summary.py
│   ├── ⚙️ generate_enriched_report.py
│   ├── ⚙️ create_dashboard.py
│   ├── ⚙️ budget_simulator.py
│   └── ⚙️ budget_simulator_interactive.py
│
└── 📂 Documentation/                    ← 13 guides
    ├── 📖 LIRE_MOI_EN_PREMIER.txt
    ├── 📖 README_FINAL.md
    ├── 📖 INDEX_DOCUMENTATION.md
    ├── 📖 GUIDE_COMPLET_FINAL.md
    └── ... (9 autres guides)
```

---

## 🎯 Flux de Travail Typique

### **Scénario 1 : Présentation Rapide**

```
┌─────────────────────────────────────────────────────────────┐
│  1. Double-clic sur lancer_app.bat                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Application s'ouvre dans le navigateur                  │
│     http://localhost:8501                                   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Ajuster les curseurs                                    │
│     - Nombre d'adhérents : 1,000                            │
│     - Cotisation : 0%                                       │
│     - Prix : 0%                                             │
│     - Fréquence : +20%                                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Explorer les 4 onglets                                  │
│     - Vue d'ensemble                                        │
│     - Profils                                               │
│     - Revenus                                               │
│     - Détails                                               │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Exporter les résultats (CSV)                            │
└─────────────────────────────────────────────────────────────┘

⏱️ Temps total : 15-30 minutes
```

---

### **Scénario 2 : Rapport Complet**

```
┌─────────────────────────────────────────────────────────────┐
│  1. Ouvrir un terminal                                      │
│     cd D:\python_work\bob-enquete                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Lancer le script master                                 │
│     python scripts/generate_all_reports.py                  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Attendre (~30 secondes)                                 │
│     ✅ Préparation des données                              │
│     ✅ Génération synthèse exécutive                        │
│     ✅ Génération rapport enrichi                           │
│     ✅ Création dashboards                                  │
│     ✅ Simulation budget simple                             │
│     ✅ Simulation budget interactif                         │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Consulter les fichiers dans outputs/                   │
│     - 2 PDF (rapports)                                      │
│     - 2 Excel (budgets)                                     │
│     - 5 PNG (dashboards)                                    │
└─────────────────────────────────────────────────────────────┘

⏱️ Temps total : 2-3 minutes
```

---

## 🎛️ Interface de l'Application

```
┌────────────────────────────────────────────────────────────────┐
│  Simulateur BOB - Budget Prévisionnel                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  📊 Vue d'ensemble  👥 Profils  💰 Revenus  📋 Détails        │
│  ═══════════════════════════════════════════════════════════  │
│                                                                │
│  ⚙️ Paramètres de Simulation                                  │
│  ────────────────────────────────────────────────────────────  │
│                                                                │
│  Nombre d'adhérents cibles                                    │
│  ├────────●────────────────────┤ 1,000                        │
│  100                        3,000                             │
│                                                                │
│  Ajustement cotisation (%)                                    │
│  ├──────────────●──────────────┤ 0%                           │
│  -50%                       +100%                             │
│                                                                │
│  Ajustement prix location (%)                                 │
│  ├──────────────●──────────────┤ 0%                           │
│  -50%                       +100%                             │
│                                                                │
│  Ajustement fréquence (%)                                     │
│  ├──────────────────●──────────┤ +20%                         │
│  -50%                       +100%                             │
│                                                                │
│  ────────────────────────────────────────────────────────────  │
│                                                                │
│  📈 Résultats                                                 │
│  ────────────────────────────────────────────────────────────  │
│                                                                │
│  Revenus Totaux : 89,735 €/an                                │
│  ├─ Cotisations : 42,710 €                                    │
│  └─ Locations : 47,025 €                                      │
│                                                                │
│  [Graphique interactif ici]                                   │
│                                                                │
│  ────────────────────────────────────────────────────────────  │
│                                                                │
│  💾 Exporter les résultats (CSV)                              │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 📊 Types de Visualisations

### **1. Heatmap (Âge × Sexe)**

```
        Femmes          Hommes
      ┌────────┬────────┐
18-24 │ 🟢 80% │ 🟡 65% │
      ├────────┼────────┤
25-34 │ 🟢 85% │ 🟡 70% │
      ├────────┼────────┤
35-54 │ 🟢 90% │ 🟢 80% │
      ├────────┼────────┤
55+   │ 🟡 60% │ 🟡 55% │
      └────────┴────────┘

🟢 = Intérêt élevé (>75%)
🟡 = Intérêt moyen (50-75%)
🔴 = Intérêt faible (<50%)
```

---

### **2. Graphique en Barres (Profils)**

```
Femmes 25-54 Actives  ████████████████████ 100%
Actifs 35-54 ans      ██████████████████ 90%
Jeunes 25-34 ans      ████████████████ 80%
Étudiants 18-24 ans   ██████████████ 70%
Retraités 55+ ans     ████████████ 60%
```

---

### **3. Pyramide des Âges**

```
        Hommes              Femmes
55+     ◄─────┤   ├─────►
35-54   ◄──────────┤   ├──────────►
25-34   ◄────────┤   ├────────►
18-24   ◄─────┤   ├─────►
        
        ← Population →
```

---

### **4. Contribution par Segment**

```
Segment A : ████████████████████ 35%
Segment B : ███████████████ 25%
Segment C : ████████████ 20%
Segment D : ████████ 12%
Autres    : ████ 8%
```

---

## 💰 Budgets Prévisionnels

### **Vue d'Ensemble**

```
┌─────────────┬───────────┬────────────┬───────────┬──────────┐
│  Scénario   │ Adhérents │ Cotisation │ Locations │  Total   │
├─────────────┼───────────┼────────────┼───────────┼──────────┤
│ Pessimiste  │    200    │   8,542 €  │  13,000 € │ 21,542 € │
│ Réaliste    │  1,000    │  42,710 €  │  42,561 € │ 85,271 € │
│ Optimiste   │  3,000    │ 128,130 €  │ 116,014 € │244,144 € │
│ Ciblé       │  1,500    │  64,065 €  │  65,979 € │130,044 € │
└─────────────┴───────────┴────────────┴───────────┴──────────┘
```

---

### **Évolution selon le Nombre d'Adhérents**

```
300k €│                                    ●
      │                                 ●
      │                              ●
200k €│                           ●
      │                        ●
      │                     ●
100k €│                  ●
      │               ●
      │            ●
  0k €│         ●
      └─────────────────────────────────────
       200   500   1000  1500  2000  3000
                Nombre d'adhérents
```

---

## 📈 Métriques Clés

### **Enquête**

```
┌────────────────────────────────────────┐
│  Répondants Total        90            │
│  ├─ Besançon             52 (57.8%)    │
│  └─ Hors Besançon        38 (42.2%)    │
│                                        │
│  Population Cible        25,381        │
│  IRIS Couverts           11            │
│                                        │
│  Intérêt (Besançon)      69.2%         │
│  Personnes Intéressées   ~17,571       │
│                                        │
│  Acceptation Cotisation  63.5%         │
│  Personnes Payantes      ~11,157       │
└────────────────────────────────────────┘
```

---

### **Qualité du Redressement**

```
┌────────────────────────────────────────┐
│  Design Effect (Deff)    1.67          │
│  Effective Sample Size   31.1          │
│                                        │
│  Convergence             ✅ Atteinte   │
│  Itérations              247           │
│  Tolérance               0.05          │
│                                        │
│  Poids Min               0.5           │
│  Poids Max               5.0           │
│  Poids Moyen             1.0           │
└────────────────────────────────────────┘
```

---

## 🎯 Segments Cibles

### **Top 3 Prioritaires**

```
┌──────────────────────────────────────────────────────────────┐
│  1️⃣ Femmes 25-54 ans Actives                                │
│  ────────────────────────────────────────────────────────────│
│  Intérêt              ████████████████████ 85-100%          │
│  Acceptation          ████████████████ 70-80%               │
│  Potentiel            ~3,500 personnes                      │
│  Revenu estimé        ~45,000 €/an                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  2️⃣ Actifs 35-54 ans (H+F)                                  │
│  ────────────────────────────────────────────────────────────│
│  Intérêt              ██████████████████ 80-100%            │
│  Acceptation          ███████████████ 65-75%                │
│  Potentiel            ~4,200 personnes                      │
│  Revenu estimé        ~52,000 €/an                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  3️⃣ Jeunes 25-34 ans                                        │
│  ────────────────────────────────────────────────────────────│
│  Intérêt              ████████████████ 80%                  │
│  Acceptation          ████████████ 60%                      │
│  Potentiel            ~2,800 personnes                      │
│  Revenu estimé        ~28,000 €/an                          │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Démarrage en 3 Étapes

```
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 : LIRE LA DOCUMENTATION                            │
│  ───────────────────────────────────────────────────────────│
│  📖 Ouvrir : README_FINAL.md                                │
│  ⏱️ Temps : 5 minutes                                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 2 : LANCER L'APPLICATION                             │
│  ───────────────────────────────────────────────────────────│
│  🚀 Double-clic : lancer_app.bat                            │
│  ⏱️ Temps : 1 minute                                        │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ÉTAPE 3 : EXPLORER LES RÉSULTATS                           │
│  ───────────────────────────────────────────────────────────│
│  🎛️ Ajuster : Les curseurs                                 │
│  📊 Consulter : Les graphiques                              │
│  💾 Exporter : Les données (CSV)                            │
│  ⏱️ Temps : 15-30 minutes                                   │
└─────────────────────────────────────────────────────────────┘

⏱️ TEMPS TOTAL : ~20-40 minutes
```

---

## 📚 Navigation Documentation

```
                    INDEX_DOCUMENTATION.md
                              │
                              ▼
        ┌─────────────────────┬─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   DÉMARRAGE            GUIDES              MÉTHODOLOGIE
        │                     │                     │
        │                     │                     │
   ┌────┴────┐          ┌────┴────┐          ┌────┴────┐
   │         │          │         │          │         │
   ▼         ▼          ▼         ▼          ▼         ▼
README   LANCEMENT  COMPLET  BUDGET   CALCUL  STRATÉGIE
FINAL      APP      FINAL    PREVI
```

---

## ✅ Checklist Rapide

```
Installation :
  ☑ Python 3.8+ installé
  ☑ pip install -r requirements.txt
  ☑ pip install streamlit plotly

Données :
  ☑ enquete_bob.xlsx présent
  ☑ enquete_all_prepared.xlsx généré
  ☑ margins_center.csv créé

Test :
  ☑ python scripts/generate_all_reports.py
  ☑ python -m streamlit run scripts/app_simulation_interactive.py
  ☑ Consulter outputs/

Documentation :
  ☑ Lire README_FINAL.md
  ☑ Consulter INDEX_DOCUMENTATION.md
  ☑ Parcourir les guides
```

---

## 🎊 Résumé en 1 Image

```
┌────────────────────────────────────────────────────────────────┐
│                    PROJET BOB-ENQUÊTE                          │
│                  ✅ TERMINÉ ET OPÉRATIONNEL                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  📊 DONNÉES                                                    │
│  ├─ 90 répondants (52 Besançon + 38 hors)                     │
│  ├─ 11 IRIS (25,381 habitants)                                │
│  └─ Redressement par raking (Deff = 1.67)                     │
│                                                                │
│  🎯 RÉSULTATS                                                  │
│  ├─ 69.2% d'intérêt à Besançon                                │
│  ├─ ~17,571 personnes intéressées                             │
│  └─ 3 segments cibles identifiés                              │
│                                                                │
│  💰 BUDGETS                                                    │
│  ├─ Pessimiste : 21,542 €/an                                  │
│  ├─ Réaliste : 85,271 €/an                                    │
│  ├─ Optimiste : 244,144 €/an                                  │
│  └─ Ciblé : 130,044 €/an                                      │
│                                                                │
│  🚀 LIVRABLES                                                  │
│  ├─ Application web interactive (Streamlit)                   │
│  ├─ 9 fichiers de sortie (PDF, Excel, PNG)                    │
│  ├─ 20 scripts Python fonctionnels                            │
│  └─ 13 documents de documentation (~118 pages)                │
│                                                                │
│  ⏱️ DÉMARRAGE RAPIDE                                          │
│  └─ Double-clic sur : lancer_app.bat                          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

**🎉 Prêt à l'emploi !**

**Commencez par** : Double-clic sur `lancer_app.bat` 🚀


