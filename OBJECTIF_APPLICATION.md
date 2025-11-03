# Objectif de l'Application BOB-Enquête

## 🎯 Objectif Principal

**Évaluer la demande et l'acceptabilité d'une bibliothèque d'objets à Besançon** en analysant les réponses d'une enquête auprès de 90 personnes, tout en corrigeant les biais de l'échantillon pour obtenir des résultats représentatifs de la population du centre-ville.

---

## 🔍 Ce que l'application cherche à savoir

### 1. **Demande Locale (Besançon centre-ville)**

#### Questions clés :
- **Combien d'habitants du centre-ville sont intéressés** par une bibliothèque d'objets ?
- **Quel pourcentage accepterait de payer une cotisation** pour y accéder ?
- **Quel est le montant maximum acceptable** pour cette cotisation ?

#### Résultats obtenus :
- ✅ **69% des habitants du centre-ville sont intéressés** (après redressement)
- ✅ **63.5% accepteraient de payer une cotisation**
- ✅ **Estimation : ~17,500 habitants potentiellement intéressés** (sur 25,381)

---

### 2. **Comportements et Pratiques Générales**

#### Questions clés :
- **Ont-ils déjà utilisé** des services de location ou de prêt d'objets ?
- **Seraient-ils prêts à partager** leurs propres objets avec d'autres ?
- **Quel prix maximum** accepteraient-ils de payer pour louer un objet ?
- **Quelles sont leurs motivations** pour utiliser ce type de service ?
- **Quels critères sont essentiels** pour qu'ils utilisent le service ?

#### Résultats obtenus :
- 📊 **53.8% n'ont jamais utilisé** ce type de service → Potentiel de nouveaux utilisateurs
- 📊 **55.8% acceptent de partager avec conditions** → Besoin d'un cadre clair
- 📊 **61.5% ne veulent pas payer plus de 10€/jour** → Seuil psychologique identifié

---

### 3. **Différences entre Populations**

#### Questions clés :
- **Y a-t-il une différence d'intérêt** entre les habitants de Besançon et ceux des autres territoires ?
- **Les profils démographiques** (âge, sexe, situation professionnelle) influencent-ils l'intérêt ?

#### Résultats obtenus :
- 🔍 **Les Besançonnais sont 1.75× plus intéressés** que les hors-Besançon (+29.8 points)
- 🔍 **Les hors-Besançon sont principalement des étudiants** (84% ont 18-24 ans)
- 🔍 **Les Besançonnais intéressés sont majoritairement des actifs** de 35-44 ans

---

## 🛠️ Comment l'application y répond

### Étape 1 : **Correction des biais d'échantillon**

**Problème** : Les 90 répondants ne représentent pas fidèlement la population réelle du centre-ville (âge, sexe, situation professionnelle différents).

**Solution** : Utilisation du **raking (redressement statistique)** pour ajuster les poids de chaque répondant afin que l'échantillon corresponde aux données INSEE du recensement 2022.

**Résultat** : Chaque répondant reçoit un poids (de 102 à 1000) qui indique combien de personnes il représente dans la population réelle.

---

### Étape 2 : **Analyses différenciées**

**Principe** : Toutes les questions ne concernent pas tout le monde de la même manière.

#### Questions **LOCALES** (Besançon uniquement - 52 répondants)
- Intérêt pour une bibliothèque d'objets **à Besançon**
- Acceptation de payer une cotisation **pour ce service local**

→ **Utilise les poids redressés** pour représenter les 25,381 habitants du centre-ville

#### Questions **GENERALES** (Tous les répondants - 90)
- Avez-vous déjà utilisé des services de location/prêt ?
- Accepteriez-vous de partager vos objets ?
- Quel prix maximum pour une location ?

→ **Utilise tous les répondants** pour avoir plus de données sur les pratiques générales

---

### Étape 3 : **Production de résultats exploitables**

L'application génère automatiquement :

#### 📊 **Graphiques** (PNG)
- Distribution des poids de redressement
- Comparaisons avant/après redressement (âge, sexe, CSP)
- Fréquences des réponses aux questions clés
- Convergence de l'algorithme de redressement

#### 📄 **Rapports PDF**
- Rapport global complet avec toutes les analyses
- Métriques de qualité du redressement
- Interprétations et recommandations

#### 📈 **Données exportées** (CSV)
- Données avec poids finaux pour analyses complémentaires
- Qualité du calage sur marges
- Statistiques comparatives

---

## 💡 Pourquoi cette approche ?

### Avantages

✅ **Représentativité** : Les résultats reflètent la vraie population du centre-ville, pas seulement les répondants

✅ **Précision** : Distinction claire entre demande locale (Besançon) et pratiques générales

✅ **Transparence** : Les limites sont documentées (petit échantillon, convergence imparfaite)

✅ **Reproductibilité** : Le pipeline peut être relancé avec de nouvelles données

✅ **Exploitation** : Résultats directement utilisables pour la prise de décision

---

## 🎯 En résumé

### L'application cherche à répondre à :

**Question stratégique** :  
> "Faut-il créer une bibliothèque d'objets à Besançon ?"

**Réponse apportée** :  
> "Oui, il existe une demande forte (69% d'intérêt) avec une acceptation de cotisation significative (63.5%), représentant environ 17,500 habitants potentiellement intéressés dans le centre-ville."

**Avec les nuances** :
- ⚠️ Le prix doit rester autour de 10€/jour maximum
- ⚠️ Un cadre clair est nécessaire pour le partage d'objets
- ⚠️ Plus de la moitié n'ont jamais utilisé ce type de service (besoin de communication)
- ✅ La cible principale : actifs de 35-44 ans, majoritairement des femmes

---

## 🔄 Utilité pour la Décision

Cette application transforme des **données brutes d'enquête** en **informations stratégiques exploitables** :

1. **Dimensionner le projet** : ~17,500 habitants intéressés
2. **Fixer les tarifs** : Cotisation entre 1€ et 20€, location max 10€/jour
3. **Cibler la communication** : Actifs 35-44 ans, nouveaux utilisateurs
4. **Anticiper les freins** : Prix, expérience, conditions de partage
5. **Valider la pertinence** : Écart de +30 points entre Besançon et hors-Besançon

---

**En une phrase** :  
> L'application BOB-Enquête transforme les réponses de 90 personnes en une estimation fiable de la demande pour une bibliothèque d'objets auprès de 25,381 habitants du centre-ville de Besançon, en corrigeant les biais d'échantillonnage et en distinguant demande locale et pratiques générales.

