# Guide d'Utilisation - Simulateur BOB

## 🚀 Lancement de l'Application

### Méthode Simple

1. **Double-cliquez** sur `Simulateur_BOB.exe`
2. Une fenêtre de console s'ouvrira (c'est normal, ne la fermez pas)
3. Votre navigateur s'ouvrira automatiquement avec l'application
4. L'URL sera : `http://localhost:8501`

### Si le Navigateur ne s'Ouvre pas Automatiquement

Si le navigateur ne s'ouvre pas automatiquement :
1. Regardez l'URL dans la console (elle sera affichée)
2. Copiez l'URL (exemple : `http://localhost:8501`)
3. Ouvrez votre navigateur manuellement
4. Collez l'URL dans la barre d'adresse

## 📊 Utilisation de l'Application

### Paramètres Principaux

Dans la barre latérale gauche, vous pouvez ajuster :

- **Nombre d'adhérents cible** : Nombre d'adhérents souhaité (100 à 3000)
- **Tarifs de cotisation** :
  - Tarif Solidaire (pour étudiants, chômeurs)
  - Tarif Normal (tarif standard)
  - Tarif Soutien (pour ceux qui souhaitent soutenir davantage)
- **Prix de location** : Prix moyen de location d'un objet par jour
- **Nombre de locations** : Nombre moyen de locations par adhérent et par an
- **Répartition par profil** : Ajustez les proportions de chaque tarif selon les profils démographiques

### Résultats

L'application affiche automatiquement :

- **KPIs principaux** : Nombre d'adhérents, revenus totaux, etc.
- **Graphiques interactifs** :
  - Répartition des revenus
  - Distribution par âge, sexe, CSP
  - Analyses détaillées par profil
- **Tableaux détaillés** : Données complètes avec filtres

### Export des Résultats

Vous pouvez exporter :
- **PDF** : Rapport complet avec graphiques (bouton "Exporter le Scénario en PDF")
- **CSV** : Données brutes pour analyse dans Excel (bouton "Télécharger en CSV")

## ⚠️ Problèmes Courants

### L'Application ne se Lance pas

**Symptôme** : Rien ne se passe quand vous double-cliquez sur l'exécutable

**Solutions** :
1. **Vérifiez l'antivirus** : Certains antivirus bloquent les exécutables créés par PyInstaller. Ajoutez une exception.
2. **Vérifiez Windows Defender** : Cliquez sur "Plus d'infos" puis "Exécuter quand même" lors de l'avertissement
3. **Vérifiez les fichiers** : Assurez-vous que tous les fichiers sont présents (notamment le dossier `data`)

### Le Port est Déjà Utilisé

**Symptôme** : Erreur "Port 8501 already in use"

**Solutions** :
1. Fermez les autres instances de l'application
2. Fermez toute autre application utilisant le port 8501
3. Redémarrez l'application

### Les Données ne s'Affichent pas

**Symptôme** : L'application se lance mais les données sont vides

**Solutions** :
1. Vérifiez que le dossier `data` est présent à côté de l'exécutable
2. Vérifiez que les fichiers suivants existent :
   - `data/raw/enquete_all_prepared.xlsx`
   - `data/margins/margins_center.csv`
   - `config.yaml`

### L'Application est Lente

**Symptôme** : L'application met du temps à charger ou à réagir

**Solutions** :
1. Fermez les autres applications lourdes
2. Attendez quelques secondes lors du premier lancement (chargement des données)
3. Vérifiez que vous avez suffisamment de RAM disponible (minimum 4 Go recommandé)

## 🔒 Sécurité et Confidentialité

- **Données locales** : Toutes les données restent sur votre ordinateur
- **Pas de connexion Internet** : L'application fonctionne entièrement hors ligne
- **Pas de collecte de données** : Aucune donnée n'est envoyée à l'extérieur

## 💡 Conseils d'Utilisation

### Pour une Meilleure Expérience

1. **Utilisez un navigateur moderne** : Chrome, Firefox, Edge (dernière version)
2. **Écran large recommandé** : L'application est optimisée pour les écrans larges
3. **Sauvegardez vos scénarios** : Utilisez l'export PDF pour garder une trace de vos simulations

### Exploration des Scénarios

1. Commencez par les **valeurs par défaut**
2. Ajustez progressivement les paramètres
3. Observez l'impact sur les revenus totaux
4. Comparez différents scénarios en exportant les PDF

### Interprétation des Résultats

- **Revenus totaux** : Revenus annuels projetés pour la BOB
- **Revenu par adhérent** : Montant moyen généré par adhérent
- **Répartition des cotisations** : Répartition entre les trois tarifs

## 📞 Support

En cas de problème technique :

1. Consultez les **logs dans la console** (fenêtre noire qui s'ouvre)
2. Notez les **messages d'erreur** exacts
3. Vérifiez que tous les **fichiers sont présents**
4. Contactez le développeur avec ces informations

## 📝 Notes Techniques

- **Système d'exploitation** : Windows 10/11
- **Navigateur** : Compatible avec Chrome, Firefox, Edge
- **RAM** : Minimum 4 Go recommandé
- **Espace disque** : Environ 500 Mo pour l'application complète

## 🎯 Exemples d'Utilisation

### Scénario 1 : Lancement Modeste

- **Adhérents** : 500
- **Tarif Solidaire** : 5€
- **Tarif Normal** : 10€
- **Tarif Soutien** : 15€
- **Prix location** : 3€/jour
- **Locations/an** : 8

### Scénario 2 : Objectif Ambitieux

- **Adhérents** : 1500
- **Tarif Solidaire** : 5€
- **Tarif Normal** : 12€
- **Tarif Soutien** : 25€
- **Prix location** : 4€/jour
- **Locations/an** : 12

### Scénario 3 : Modèle Économique Équilibré

- **Adhérents** : 1000
- **Tarif Solidaire** : 7€
- **Tarif Normal** : 15€
- **Tarif Soutien** : 30€
- **Prix location** : 3,50€/jour
- **Locations/an** : 10

---

**Bon usage de l'application ! 📊**


