# Méthodologie de Calcul du Nombre de Personnes Intéressées

## 🤔 Votre Question

> "Quand tu calcules le nombre de personnes intéressées, est-ce que tu appliques directement le pourcentage à la population des IRIS ou est-ce que tu regardes le profil de ceux qui ont répondu non ? Par exemple, étudiants oui/non, âge, homme/femme ?"

**Excellente question !** C'est un point méthodologique crucial.

---

## 📊 Ce que fait ACTUELLEMENT l'application

### Méthode Simple (Actuelle)

L'application utilise une **approche globale** :

```python
# Étape 1 : Calculer le pourcentage pondéré
freq = df.groupby('interet_projet')['weight'].sum()
pct_oui = freq['Oui'] / freq.sum() * 100  # → 69.2%

# Étape 2 : Appliquer à la population totale
population_totale = 25_381
nb_interesses = population_totale * (pct_oui / 100)  # → 17,573
```

**Résultat** : 69.2% × 25,381 = **17,573 personnes intéressées**

### ⚠️ Problème de cette approche

Cette méthode **ne tient PAS compte des profils** qui ont répondu "Oui" vs "Non".

**Exemple concret** :
- Si 90% des 18-24 ans disent "Oui" mais qu'ils ne représentent que 10% de la population
- Et que 50% des 65+ disent "Oui" mais qu'ils représentent 30% de la population
- → Le calcul simple **surestime** le nombre total d'intéressés

---

## ✅ Ce qu'il FAUDRAIT faire (Méthode par Profil)

### Méthode Sophistiquée (Recommandée)

Calculer le nombre d'intéressés **par profil démographique**, puis sommer :

```python
# Pour chaque combinaison (âge, sexe, csp)
for age in ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']:
    for sexe in ['M', 'F']:
        for csp in [1, 2, 3]:
            # 1. Filtrer les répondants de ce profil
            df_profil = df[(df['age_group'] == age) & 
                          (df['sexe'] == sexe) & 
                          (df['csp'] == csp)]
            
            # 2. Calculer le % d'intérêt pour ce profil
            if len(df_profil) > 0:
                pct_oui_profil = (df_profil['interet_projet'] == 'Oui').sum() / len(df_profil)
            else:
                pct_oui_profil = 0  # Ou moyenne globale
            
            # 3. Récupérer la population INSEE de ce profil
            pop_profil = margins[(margins['age_group'] == age) & 
                                (margins['sexe'] == sexe) & 
                                (margins['csp'] == csp)]['population'].sum()
            
            # 4. Calculer le nombre d'intéressés pour ce profil
            nb_interesses_profil = pop_profil * pct_oui_profil
            
            # 5. Sommer
            total_interesses += nb_interesses_profil
```

---

## 📈 Comparaison des Deux Méthodes

### Exemple Fictif

Imaginons 2 profils :

| Profil | Population INSEE | % Intérêt (enquête) | Méthode Simple | Méthode par Profil |
|--------|------------------|---------------------|----------------|---------------------|
| **18-24 ans, F, Étudiantes** | 2,000 | 90% | - | 1,800 |
| **65+ ans, M, Retraités** | 3,000 | 40% | - | 1,200 |
| **TOTAL** | 5,000 | 69.2% (moyenne) | **3,460** | **3,000** |

**Écart** : La méthode simple surestime de **460 personnes** (+15%) !

### Pourquoi cet écart ?

La méthode simple fait une **moyenne pondérée globale** qui ne reflète pas les différences de comportement entre profils.

---

## 🔍 Analyse des Profils dans Votre Enquête

Créons un script pour analyser **qui** dit "Oui" vs "Non" :

### Script d'Analyse par Profil

```python
# Analyser l'intérêt par profil démographique
df_besancon = df[df['is_besancon']]

# Par âge
interet_age = pd.crosstab(
    df_besancon['age_group'], 
    df_besancon['interet_projet'],
    normalize='index'
) * 100

# Par sexe
interet_sexe = pd.crosstab(
    df_besancon['sexe'], 
    df_besancon['interet_projet'],
    normalize='index'
) * 100

# Par CSP
interet_csp = pd.crosstab(
    df_besancon['csp'], 
    df_besancon['interet_projet'],
    normalize='index'
) * 100
```

**Résultats attendus** :
- Les 35-44 ans sont-ils plus intéressés que les 65+ ?
- Les femmes sont-elles plus intéressées que les hommes ?
- Les actifs sont-ils plus intéressés que les retraités ?

---

## 💡 Quelle Méthode Utiliser ?

### Méthode Simple (Actuelle)

**Avantages** :
- ✅ Simple à comprendre
- ✅ Rapide à calculer
- ✅ Suffisante si l'échantillon est bien redressé

**Inconvénients** :
- ❌ Ne capture pas les différences entre profils
- ❌ Peut surestimer ou sous-estimer selon les profils

**Quand l'utiliser** :
- Échantillon bien redressé (c'est votre cas !)
- Ordre de grandeur suffisant
- Communication simple

### Méthode par Profil (Recommandée)

**Avantages** :
- ✅ Plus précise
- ✅ Capture les différences entre profils
- ✅ Permet d'identifier les cibles prioritaires

**Inconvénients** :
- ❌ Plus complexe
- ❌ Nécessite suffisamment de répondants par profil
- ❌ Peut être instable si certains profils ont peu de répondants

**Quand l'utiliser** :
- Besoin de précision
- Échantillon suffisant par profil (>10 par case)
- Segmentation marketing

---

## 🎯 Recommandation pour Votre Projet

### Situation Actuelle

Avec **52 répondants Besançon** et **6 âges × 2 sexes × 3 CSP = 36 profils possibles** :

**Moyenne** : 52 / 36 = **1.4 répondants par profil** ❌

→ **Trop peu** pour une analyse fiable par profil complet

### Solutions

#### Option 1 : Simplifier les Profils

Regrouper les variables pour avoir plus de répondants par case :

```python
# Au lieu de 36 profils (6×2×3), utiliser 12 profils (6×2)
# Analyser par âge + sexe uniquement (ignorer CSP)

for age in ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']:
    for sexe in ['M', 'F']:
        # Moyenne : 52 / 12 = 4.3 répondants par profil
        # → Plus raisonnable
```

#### Option 2 : Regrouper les Âges

```python
# 3 grandes tranches d'âge au lieu de 6
ages_regroupes = {
    'Jeunes (18-34)': ['18-24', '25-34'],
    'Adultes (35-54)': ['35-44', '45-54'],
    'Seniors (55+)': ['55-64', '65+']
}

# 3 âges × 2 sexes × 3 CSP = 18 profils
# Moyenne : 52 / 18 = 2.9 répondants par profil
# → Limite acceptable
```

#### Option 3 : Analyse Univariée

Analyser séparément chaque variable :

```python
# % Intérêt par âge (sans croiser avec sexe/csp)
# % Intérêt par sexe (sans croiser avec âge/csp)
# % Intérêt par CSP (sans croiser avec âge/sexe)
```

**Avantage** : Plus de répondants par modalité  
**Inconvénient** : Ne capture pas les interactions (ex: "Femmes 35-44 ans actives")

---

## 🔧 Ce que Je Peux Faire

Je peux créer un script qui :

1. **Analyse l'intérêt par profil** (âge, sexe, CSP)
2. **Compare les deux méthodes** (simple vs par profil)
3. **Identifie les profils les plus/moins intéressés**
4. **Calcule le nombre d'intéressés par méthode**
5. **Évalue la fiabilité** selon le nombre de répondants par profil

Voulez-vous que je crée ce script ?

---

## 📝 Conclusion

### Réponse à Votre Question

**Actuellement** : L'application applique **directement le pourcentage global** (69.2%) à la population totale (25,381).

**Idéalement** : Il faudrait calculer le % d'intérêt **par profil démographique**, puis multiplier par la population INSEE de chaque profil et sommer.

**Problème** : Avec 52 répondants pour 36 profils possibles, l'analyse par profil complet est **trop instable**.

**Solution pragmatique** :
1. Utiliser la méthode simple (actuelle) pour l'estimation globale
2. Faire une analyse univariée (âge, sexe, CSP séparément) pour identifier les cibles
3. Mentionner dans le rapport : "Estimation globale, sans segmentation fine par profil"

### Estimation Finale

**Méthode actuelle (simple)** :
- 69.2% × 25,381 = **~17,573 personnes intéressées**
- Fourchette prudente : **15,000 - 20,000**

**Avec analyse par profil** (si échantillon plus grand) :
- Probablement entre **14,000 - 18,000** (plus précis)
- Permettrait de cibler les profils prioritaires

