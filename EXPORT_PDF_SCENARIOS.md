# 📄 Export PDF des Scénarios - Guide d'Utilisation

## 🎯 Fonctionnalité

L'application interactive permet maintenant d'**exporter les scénarios en PDF** avec :
- ✅ Toutes les **hypothèses** du scénario
- ✅ Les **KPIs** principaux
- ✅ Les **graphiques** visualisés
- ✅ Les **tableaux détaillés** par profil
- ✅ La **répartition des tarifs** par profil

---

## 📦 Installation des Dépendances

Pour activer l'export PDF, installez les bibliothèques nécessaires :

```bash
pip install reportlab kaleido
```

**Note** : `kaleido` est nécessaire pour exporter les graphiques Plotly en images PNG.

---

## 🚀 Utilisation

### **Étape 1 : Configurer votre Scénario**

1. Ajustez les paramètres dans la sidebar :
   - Nombre d'adhérents cible
   - Tarifs de cotisation (Solidaire, Normal, Soutien)
   - Prix de location
   - Nombre de locations/an/adhérent
   - Répartition des tarifs par profil

### **Étape 2 : Générer le PDF**

1. Cliquez sur le bouton **"📄 Exporter le Scénario en PDF"**
   - Situé juste après les métriques principales
   - Bouton bleu (primary) bien visible

2. Attendez la génération :
   - Un spinner indique "Génération du rapport PDF en cours..."
   - Les graphiques sont exportés en PNG
   - Le PDF est créé avec toutes les données

3. Téléchargez le PDF :
   - Un bouton "📥 Télécharger le PDF" apparaît automatiquement
   - Le fichier est aussi sauvegardé dans `outputs/reports/`

---

## 📋 Contenu du PDF

### **Page de Garde**
- Titre : "Rapport de Scénario BOB"
- Date et heure de génération
- Nom du projet

### **Section 1 : Hypothèses du Scénario**

#### **1.1. Paramètres Principaux**
Tableau avec :
- Nombre d'adhérents cible
- Tarif Solidaire (€)
- Tarif Normal (€)
- Tarif Soutien (€)
- Prix location moyen (€/jour)
- Nombre locations/an/adhérent

#### **1.2. Répartition des Tarifs par Profil**
Tableau détaillé montrant pour chaque profil :
- Pourcentage Solidaire
- Pourcentage Normal
- Pourcentage Soutien

**Profils inclus** :
- Jeunes (18-24)
- Étudiants/Chômeurs
- Actifs Jeunes (25-34)
- Actifs Adultes (35-44)
- Actifs Seniors (45-54)
- Actifs Seniors (55-64)
- Retraités (55-64)
- Retraités (65+)
- Retraités (autres)
- Autres profils

### **Section 2 : Indicateurs Clés (KPIs)**

Tableau avec tous les KPIs principaux :
- Nombre total d'adhérents
- Revenus cotisations (€)
- Revenus locations (€)
- Revenus totaux (€)
- Revenu moyen par adhérent (€)
- Cotisation moyenne (€)
- Répartition solidaire (%)
- Répartition normal (%)
- Répartition soutien (%)

### **Section 3 : Visualisations**

Les graphiques suivants sont inclus :
1. **Répartition des Revenus** (camembert)
   - Cotisations vs Locations

2. **Distribution par Âge** (barres horizontales)
   - Nombre d'adhérents par tranche d'âge

3. **Répartition des Cotisations** (camembert)
   - Solidaire / Normal / Soutien avec tarifs

### **Section 4 : Détails par Profil**

Tableau complet avec toutes les données par profil :
- Profil
- Tranche d'âge
- CSP
- Nombre d'adhérents
- Cotisation moyenne (€)
- Nombre de locations/an
- Revenus totaux (€)

---

## 📁 Fichiers Générés

### **PDF Final**
```
outputs/reports/scenario_bob_YYYYMMDD_HHMMSS.pdf
```

**Exemple** : `scenario_bob_20251030_143052.pdf`

### **Graphiques Temporaires**
```
outputs/temp_export/repartition_revenus_YYYYMMDD_HHMMSS.png
outputs/temp_export/distribution_age_YYYYMMDD_HHMMSS.png
outputs/temp_export/repartition_cotisations_YYYYMMDD_HHMMSS.png
```

**Note** : Les fichiers temporaires peuvent être supprimés après génération du PDF.

---

## 🎨 Format du PDF

### **Caractéristiques**
- Format : A4
- Pages : Variable selon le nombre de graphiques
- Couleurs : 
  - Bleu (#1f4788) pour les en-têtes
  - Vert (#2ecc71) pour les KPIs
  - Beige pour les tableaux

### **Style**
- Titres en gras
- Tableaux avec bordures
- Graphiques haute résolution (800x600px, scale=2)
- Formatage français des nombres (virgule pour décimales)

---

## 💡 Exemples d'Utilisation

### **Scénario 1 : Budget Conservateur**

**Hypothèses** :
- 500 adhérents
- Tarifs : 5€ / 10€ / 15€
- Prix location : 2,5€
- 8 locations/an

**Export** : `scenario_bob_conservateur.pdf`

### **Scénario 2 : Budget Optimiste**

**Hypothèses** :
- 2000 adhérents
- Tarifs : 8€ / 15€ / 25€
- Prix location : 4€
- 12 locations/an

**Export** : `scenario_bob_optimiste.pdf`

### **Scénario 3 : Budget Équilibré**

**Hypothèses** :
- 1000 adhérents
- Tarifs : 5€ / 10€ / 20€
- Prix location : 3€
- 10 locations/an

**Export** : `scenario_bob_equilibre.pdf`

---

## 🔧 Dépannage

### **Problème : "ReportLab n'est pas installé"**

**Solution** :
```bash
pip install reportlab
```

### **Problème : "Impossible d'exporter les graphiques"**

**Cause** : Kaleido n'est pas installé

**Solution** :
```bash
pip install kaleido
```

**Alternative** : Les graphiques seront exportés en HTML (moins optimal)

### **Problème : "Erreur lors de la génération du PDF"**

**Causes possibles** :
1. Répertoire de sortie non accessible
2. Graphiques non exportés correctement
3. Données manquantes

**Solutions** :
1. Vérifier les permissions d'écriture dans `outputs/`
2. Vérifier que kaleido est installé
3. Vérifier que tous les paramètres sont définis

### **Problème : "Le PDF est vide ou incomplet"**

**Causes possibles** :
- Graphiques non exportés (kaleido manquant)
- Erreur dans la génération

**Solution** :
- Vérifier les messages d'erreur dans l'interface
- Vérifier que kaleido est installé : `pip install kaleido`

---

## 📊 Structure du Rapport PDF

```
┌─────────────────────────────────┐
│      Page de Garde              │
│  Rapport de Scénario BOB        │
│  Date de génération            │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  1. Hypothèses du Scénario     │
│  - Paramètres principaux        │
│  - Répartition par profil      │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  2. Indicateurs Clés (KPIs)    │
│  - Tableau des KPIs            │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  3. Visualisations              │
│  - Graphique 1: Revenus         │
│  - Graphique 2: Distribution    │
│  - Graphique 3: Cotisations     │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│  4. Détails par Profil          │
│  - Tableau complet              │
└─────────────────────────────────┘
```

---

## ✅ Checklist de Vérification

Avant d'exporter un scénario :

- [ ] Les paramètres sont correctement configurés
- [ ] Les proportions par profil sont définies (total = 100%)
- [ ] Les résultats sont affichés correctement dans l'interface
- [ ] ReportLab est installé (`pip install reportlab`)
- [ ] Kaleido est installé (`pip install kaleido`)
- [ ] Le répertoire `outputs/reports/` existe et est accessible

---

## 🎯 Cas d'Usage

### **1. Présentation au Conseil Municipal**

**Objectif** : Documenter un scénario pour présentation officielle

**Méthode** :
1. Configurer le scénario optimal
2. Exporter en PDF
3. Présenter le PDF aux élus

**Avantage** : Document professionnel et complet

---

### **2. Comparaison de Scénarios**

**Objectif** : Comparer plusieurs scénarios

**Méthode** :
1. Configurer le scénario 1 → Exporter → Nommer `scenario_1.pdf`
2. Configurer le scénario 2 → Exporter → Nommer `scenario_2.pdf`
3. Configurer le scénario 3 → Exporter → Nommer `scenario_3.pdf`
4. Comparer les PDFs côte à côte

**Avantage** : Documentation claire pour comparaison

---

### **3. Archivage des Scénarios**

**Objectif** : Garder une trace des scénarios testés

**Méthode** :
1. Pour chaque scénario intéressant, exporter en PDF
2. Nommer les fichiers avec un nom descriptif après export
3. Archiver dans un dossier dédié

**Avantage** : Traçabilité et historique

---

### **4. Partage avec l'Équipe**

**Objectif** : Partager un scénario avec les collègues

**Méthode** :
1. Configurer le scénario
2. Exporter en PDF
3. Envoyer le PDF par email ou partager via cloud

**Avantage** : Format universel, facile à partager

---

## 📚 Exemple de Rapport Généré

### **Page 1 : Page de Garde**
```
Rapport de Scénario BOB

Bibliothèque d'Objets Besançon

Généré le : 30/10/2025 à 14:30
```

### **Page 2 : Hypothèses**
```
1. Hypothèses du Scénario

Paramètre                    | Valeur
------------------------------|----------
Nombre d'adhérents cible      | 1000
Tarif Solidaire               | 5 €
Tarif Normal                  | 10 €
Tarif Soutien                 | 20 €
Prix location moyen           | 3 €/jour
Nombre locations/an/adhérent  | 10
```

### **Page 3 : KPIs**
```
2. Indicateurs Clés (KPIs)

Indicateur                    | Valeur
------------------------------|----------
Nombre total d'adhérents      | 1000
Revenus cotisations           | 10500 €
Revenus locations             | 30000 €
Revenus totaux                | 40500 €
...
```

---

## 🔄 Améliorations Futures

### **Fonctionnalités à Ajouter**

1. **Export Multiple** : Exporter plusieurs scénarios en un seul PDF
2. **Template Personnalisé** : Choisir un template de PDF
3. **Graphiques Supplémentaires** : Exporter tous les graphiques des onglets
4. **Commentaires** : Ajouter des notes personnalisées dans le PDF
5. **Export Excel** : Export parallèle en format Excel
6. **Comparaison** : Générer un PDF comparant 2 scénarios

---

## 📖 Documentation Associée

- **README_FINAL.md** : Vue d'ensemble du projet
- **LANCEMENT_APP_INTERACTIVE.md** : Guide de l'application
- **TARIFS_COTISATION_LOCATION.md** : Système de tarification
- **CORRECTIONS_V2.2.md** : Corrections récentes

---

## 🎊 Résumé

### **Ce qui est disponible**

✅ Export PDF complet des scénarios  
✅ Hypothèses documentées  
✅ KPIs détaillés  
✅ Graphiques inclus  
✅ Tableaux complets par profil  
✅ Format français (virgules pour décimales)  
✅ Téléchargement direct  
✅ Sauvegarde automatique  

### **Ce qui est requis**

📦 ReportLab (`pip install reportlab`)  
📦 Kaleido (`pip install kaleido`)  

---

**Version** : 2.3  
**Date** : 30 octobre 2025  
**Statut** : ✅ Opérationnel  

🚀 **Testez maintenant : Configurez un scénario et cliquez sur "Exporter le Scénario en PDF" !**

