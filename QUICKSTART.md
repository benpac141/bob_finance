# 🚀 Démarrage rapide - bob-enquete

## Installation (2 minutes)

```bash
cd D:\python_work\bob-enquete
pip install -r requirements.txt
```

## Test avec données d'exemple (5 minutes)

```bash
# 1. Générer des données fictives
python scripts/generate_sample_data.py

# 2. Lancer l'analyse complète
python src/cli.py run --config config.yaml
```

## Résultats

Les fichiers générés se trouvent dans `outputs/` :

### 📊 Graphiques (`outputs/figures/`)
- Distribution des poids
- Convergence du raking
- Comparaisons avant/après redressement

### 📄 Rapports PDF (`outputs/reports/`)
- `rapport_global_*.pdf` : Rapport complet
- `rapport_non_interesses_*.pdf` : Sous-groupe "non intéressés"
- `rapport_non_cotisation_*.pdf` : Refus cotisation
- `rapport_oui_cotisation_*.pdf` : Accepte cotisation

### 📈 Métriques affichées
- **Deff** : Effet de plan (idéalement < 1.5)
- **n_eff** : Taille d'échantillon effective
- **Perte d'efficacité** : % de perte de précision

## Utilisation avec vos données

1. **Remplacer** `data/raw/enquete.xlsx` par votre fichier
2. **Mettre à jour** `data/margins/margins_center.csv` avec vos marges IRIS
3. **Adapter** `config.yaml` si nécessaire
4. **Lancer** : `python src/cli.py run --config config.yaml`

## Structure minimale requise

**Fichier d'enquête** (`data/raw/enquete.xlsx`) :
```
id_repondant | code_iris | age_group | sexe | csp | interet_projet | accepte_cotisation | ...
```

**Fichier de marges** (`data/margins/margins_center.csv`) :
```
code_iris | age_group | sexe | csp | population
```

## Aide

- Documentation complète : `README.md`
- Guide détaillé : `GUIDE_UTILISATION.md`
- Scripts utilitaires : `scripts/README.md`

## Commandes utiles

```bash
# Analyse complète
python src/cli.py run --config config.yaml

# Avec Make
make run

# Nettoyage des sorties
make clean
```

## Vérification rapide

Après l'exécution, vérifiez :
- ✓ Convergence atteinte (dans les logs)
- ✓ Deff < 2.0 (qualité acceptable)
- ✓ Rapports PDF générés
- ✓ Graphiques créés

🎉 C'est tout ! Votre pipeline est opérationnel.

