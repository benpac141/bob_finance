# Commandes Rapides - BOB Enquête

## 🚀 **Commande Principale** (Recommandée)

### **Générer TOUS les rapports en une seule fois**

```bash
cd D:\python_work\bob-enquete
python scripts/generate_all_reports.py
```

✅ **Génère en UNE SEULE FOIS** (pas de doublons) :
- 2 rapports PDF (synthèse + enrichi)
- 5 visualisations (dashboard)
- 2 fichiers Excel (budget simple + interactif)

**Tous les fichiers partagent le même timestamp** → Facile à identifier !

---

## 📋 **Commandes Individuelles** (Si besoin spécifique)

### **1. Préparer les Données**
```bash
python scripts/prepare_bob_with_all_respondents.py
```
→ Crée `data/raw/enquete_all_prepared.xlsx` (90 répondants)

---

### **2. Rapport de Synthèse Exécutif** (5 pages)
```bash
python scripts/generate_executive_summary.py
```
→ Crée `outputs/reports/synthese_executive_*.pdf`

---

### **3. Rapport Enrichi** (analyse par profil)
```bash
python scripts/generate_enriched_report.py
```
→ Crée `outputs/reports/rapport_enrichi_*.pdf`

---

### **4. Tableau de Bord** (5 visualisations)
```bash
python scripts/create_dashboard.py
```
→ Crée 5 fichiers PNG dans `outputs/figures/`

---

### **5. Budget Prévisionnel Simple** (4 scénarios)
```bash
python scripts/budget_simulator.py
```
→ Crée `outputs/reports/budget_previsionnel_*.xlsx`

---

### **6. Budget Interactif** (ajustable par nb adhérents)
```bash
python scripts/budget_simulator_interactive.py
```
→ Crée `outputs/reports/budget_interactif_*.xlsx`

---

## 🔍 **Analyses Complémentaires**

### **Comparaison Besançon vs Hors-Besançon**
```bash
python scripts/compare_besancon_vs_hors.py
```

### **Analyse par Profil** (méthodes de calcul)
```bash
python scripts/analyze_interest_by_profile.py
```

---

## 🧪 **Test du Pipeline**
```bash
python scripts/test_complete_pipeline.py
```
⚠️ **Attention** : Génère des doublons (exécute tous les scripts)  
→ Utilisez plutôt `generate_all_reports.py`

---

## 📁 **Fichiers Générés**

### **Avec `generate_all_reports.py`** (Recommandé)

**Timestamp unique** : `20251030_014038`

```
outputs/
├── reports/
│   ├── synthese_executive_20251030_014038.pdf
│   ├── rapport_enrichi_20251030_014038.pdf
│   ├── budget_previsionnel_20251030_014038.xlsx
│   └── budget_interactif_20251030_014038.xlsx
└── figures/
    ├── dashboard_heatmap_20251030_014038.png
    ├── dashboard_barplot_20251030_014038.png
    ├── dashboard_pyramid_20251030_014038.png
    ├── dashboard_contribution_20251030_014038.png
    └── dashboard_summary_20251030_014038.png
```

---

## 🎯 **Cas d'Usage**

### **Pour une Présentation**
```bash
python scripts/generate_all_reports.py
```
→ Ouvrir `synthese_executive_*.pdf` et `dashboard_summary_*.png`

---

### **Pour un Business Plan**
```bash
python scripts/generate_all_reports.py
```
→ Ouvrir `budget_previsionnel_*.xlsx` et `budget_interactif_*.xlsx`

---

### **Pour une Analyse Détaillée**
```bash
python scripts/generate_all_reports.py
```
→ Ouvrir `rapport_enrichi_*.pdf` et tous les dashboards

---

### **Pour Créer un Scénario Personnalisé**

1. Ouvrir `scripts/budget_simulator_interactive.py`
2. Ajouter votre objectif (ligne ~290) :
```python
simulations['1200_adherents'] = generate_simulation(
    1200, df_behaviors, margins, "1200 adherents"
)
```
3. Relancer :
```bash
python scripts/budget_simulator_interactive.py
```

---

## 🗑️ **Nettoyer les Anciens Fichiers**

### **Supprimer les anciens rapports**
```bash
# Windows PowerShell
cd D:\python_work\bob-enquete\outputs\reports
Remove-Item *_2025*.pdf, *_2025*.xlsx -Exclude *_20251030_014038.*
```

### **Supprimer les anciennes figures**
```bash
cd D:\python_work\bob-enquete\outputs\figures
Remove-Item *_2025*.png -Exclude *_20251030_014038.*
```

---

## ⚡ **Workflow Recommandé**

### **1. Première Utilisation**
```bash
# Tout générer
python scripts/generate_all_reports.py

# Consulter les résultats
cd outputs/reports
start synthese_executive_*.pdf
start budget_interactif_*.xlsx
```

### **2. Mise à Jour des Données**
```bash
# Si nouvelles données d'enquête
python scripts/prepare_bob_with_all_respondents.py

# Régénérer tout
python scripts/generate_all_reports.py
```

### **3. Ajustement des Scénarios**
```bash
# Modifier les paramètres dans le script
# Puis régénérer
python scripts/budget_simulator_interactive.py
```

---

## 📊 **Fichiers à Consulter en Priorité**

### **Pour la Décision** 🎯
1. `synthese_executive_*.pdf` (5 pages)
2. `dashboard_summary_*.png` (vue d'ensemble)
3. `budget_interactif_*.xlsx` (onglet "Synthese")

### **Pour l'Analyse** 🔍
1. `rapport_enrichi_*.pdf` (détails par profil)
2. Tous les `dashboard_*.png`
3. `budget_interactif_*.xlsx` (tous les onglets)

### **Pour le Pilotage** 📈
1. `budget_interactif_*.xlsx` (ajuster nb adhérents)
2. `dashboard_contribution_*.png` (profils clés)
3. `budget_previsionnel_*.xlsx` (scénarios)

---

## ✅ **Checklist Avant Présentation**

- [ ] `python scripts/generate_all_reports.py` exécuté
- [ ] Tous les fichiers générés (9 au total)
- [ ] Timestamp unique vérifié
- [ ] `synthese_executive_*.pdf` consulté
- [ ] `dashboard_summary_*.png` consulté
- [ ] `budget_interactif_*.xlsx` consulté
- [ ] Anciens fichiers supprimés (optionnel)

---

## 🆘 **En Cas de Problème**

### **Erreur "File not found"**
```bash
# Vérifier que les données sont préparées
python scripts/prepare_bob_with_all_respondents.py
```

### **Doublons de fichiers**
→ Utilisez `generate_all_reports.py` au lieu de `test_complete_pipeline.py`

### **Fichiers manquants**
```bash
# Régénérer tout
python scripts/generate_all_reports.py
```

---

## 📚 **Documentation**

- `GUIDE_COMPLET_FINAL.md` - Guide complet du projet
- `GUIDE_BUDGET_PREVISIONNEL.md` - Budget simple
- `GUIDE_SIMULATEUR_INTERACTIF.md` - Budget interactif
- `METHODOLOGIE_CALCUL.md` - Détails des calculs
- `SYNTHESE_FINALE.md` - Résultats de l'enquête

---

**Commande à retenir** :
```bash
python scripts/generate_all_reports.py
```

**C'est tout ce dont vous avez besoin !** 🎉

