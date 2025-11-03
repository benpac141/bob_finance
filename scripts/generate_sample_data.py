"""
Script pour générer des données d'exemple pour l'enquête BOB.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
np.random.seed(42)
N_RESPONDENTS = 200

# Définir les IRIS centre-ville
IRIS_CODES = ['211234501', '211234502']

# Définir les modalités
AGE_GROUPS = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
SEXES = ['F', 'M']
CSP = [1, 2, 3]  # 1: Cadres, 2: Professions intermédiaires, 3: Employés/ouvriers
INTERET = ['Oui', 'Non']
COTISATION = ['Oui', 'Non']
MODES = ['Voiture', 'Transports en commun', 'Vélo', 'Marche']

# Générer les données
data = {
    'id_repondant': range(1, N_RESPONDENTS + 1),
    'code_iris': np.random.choice(IRIS_CODES, N_RESPONDENTS),
    'age_group': np.random.choice(AGE_GROUPS, N_RESPONDENTS, p=[0.10, 0.25, 0.22, 0.20, 0.15, 0.08]),
    'sexe': np.random.choice(SEXES, N_RESPONDENTS, p=[0.52, 0.48]),
    'csp': np.random.choice(CSP, N_RESPONDENTS, p=[0.25, 0.30, 0.45]),
    'interet_projet': np.random.choice(INTERET, N_RESPONDENTS, p=[0.65, 0.35]),
    'accepte_cotisation': np.random.choice(COTISATION, N_RESPONDENTS, p=[0.45, 0.55]),
    'mode_transport': np.random.choice(MODES, N_RESPONDENTS, p=[0.45, 0.30, 0.15, 0.10]),
    'distance_travail': np.random.randint(1, 30, N_RESPONDENTS),
    'frequence_deplacement': np.random.choice([2, 3, 4, 5], N_RESPONDENTS, p=[0.05, 0.15, 0.25, 0.55])
}

df = pd.DataFrame(data)

# Sauvegarder en Excel
output_path = Path(__file__).parent.parent / 'data' / 'raw' / 'enquete.xlsx'
output_path.parent.mkdir(parents=True, exist_ok=True)

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Enquete', index=False)

print(f"✓ Fichier d'enquête généré : {output_path}")
print(f"  - {len(df)} répondants")
print(f"  - {len(df.columns)} variables")

# Afficher un aperçu
print("\nAperçu des données :")
print(df.head(10))

# Statistiques descriptives
print("\nRépartition des répondants :")
print(f"  - Par IRIS : {df['code_iris'].value_counts().to_dict()}")
print(f"  - Par âge : {df['age_group'].value_counts().to_dict()}")
print(f"  - Par sexe : {df['sexe'].value_counts().to_dict()}")
print(f"  - Intéressés par le projet : {df['interet_projet'].value_counts().to_dict()}")
print(f"  - Acceptent cotisation : {df['accepte_cotisation'].value_counts().to_dict()}")

