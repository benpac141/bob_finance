"""
Script pour analyser pourquoi des répondants sont exclus.
"""

import pandas as pd
from pathlib import Path

# Charger le fichier original
input_file = Path(__file__).parent.parent / "data" / "raw" / "enquete_bob.xlsx"
df = pd.read_excel(input_file)

print("="*70)
print("ANALYSE DES EXCLUSIONS")
print("="*70)

print(f"\nNombre total de repondants : {len(df)}")

# Colonnes clés
col_genre = 'Quels est votre genre ?'
col_age = "Dans quelle tranche d'age vous situez-vous ?"
col_situation = 'Quelle est votre situation professionnelle actuelle ?'
col_cp = 'Quel est le code postal de votre lieu de residence ?'

print("\n=== VALEURS MANQUANTES ===")
print(f"Genre : {df[col_genre].isna().sum()} manquants")
print(f"Age : {df[col_age].isna().sum()} manquants")
print(f"Situation pro : {df[col_situation].isna().sum()} manquants")
print(f"Code postal : {df[col_cp].isna().sum()} manquants")

print("\n=== REPARTITION GENRE ===")
print(df[col_genre].value_counts(dropna=False))

print("\n=== REPARTITION AGE ===")
print(df[col_age].value_counts(dropna=False))

print("\n=== REPARTITION SITUATION PRO ===")
print(df[col_situation].value_counts(dropna=False))

print("\n=== CODES POSTAUX ===")
cp_counts = df[col_cp].value_counts(dropna=False)
print(f"Nombre de CP differents : {len(cp_counts)}")
print("\nTop 10 :")
print(cp_counts.head(10))

# Simuler le filtrage
print("\n" + "="*70)
print("SIMULATION DU FILTRAGE")
print("="*70)

# Créer les variables comme dans le script
from scripts.prepare_bob_for_raking import create_age_group, create_sexe, create_csp, geocode_to_iris

df['age_group'] = df[col_age].apply(create_age_group)
df['sexe'] = df[col_genre].apply(create_sexe)
df['csp'] = df[col_situation].apply(create_csp)
df['code_iris'] = df.apply(
    lambda row: geocode_to_iris(row[col_cp], row.get("Comment definiriez-vous l'emplacement de votre domicile par rapport au centre-ville ?")),
    axis=1
)

print(f"\nApres creation des variables :")
print(f"  age_group manquants : {df['age_group'].isna().sum()}")
print(f"  sexe manquants : {df['sexe'].isna().sum()}")
print(f"  csp manquants : {df['csp'].isna().sum()}")
print(f"  code_iris manquants : {df['code_iris'].isna().sum()}")

# Identifier les exclusions
df['exclu'] = (df['age_group'].isna() | df['sexe'].isna() | 
               df['csp'].isna() | df['code_iris'].isna())

print(f"\nNombre de repondants exclus : {df['exclu'].sum()}")
print(f"Nombre de repondants conserves : {(~df['exclu']).sum()}")

print("\n=== RAISONS D'EXCLUSION ===")
exclus = df[df['exclu']].copy()

raisons = []
for idx, row in exclus.iterrows():
    raison = []
    if pd.isna(row['age_group']):
        raison.append('age')
    if pd.isna(row['sexe']):
        raison.append('sexe')
    if pd.isna(row['csp']):
        raison.append('csp')
    if pd.isna(row['code_iris']):
        raison.append('iris')
    raisons.append(', '.join(raison))

exclus['raison'] = raisons

print("\nRepartition des raisons :")
print(exclus['raison'].value_counts())

print("\n=== DETAIL DES EXCLUSIONS ===")
print(f"\nExclus pour age manquant : {df['age_group'].isna().sum()}")
print(f"Exclus pour sexe manquant/non-binaire : {df['sexe'].isna().sum()}")
print(f"Exclus pour csp manquante : {df['csp'].isna().sum()}")
print(f"Exclus pour code postal hors Besancon : {df['code_iris'].isna().sum()}")

# Détail sur les codes postaux
print("\n=== CODES POSTAUX HORS BESANCON ===")
df_cp_invalide = df[df['code_iris'].isna() & df[col_cp].notna()]
if len(df_cp_invalide) > 0:
    print(f"Nombre : {len(df_cp_invalide)}")
    print("Codes postaux :")
    print(df_cp_invalide[col_cp].value_counts())

print("\n" + "="*70)
print("RECOMMANDATIONS")
print("="*70)

total_exclus = df['exclu'].sum()
if total_exclus > 0:
    print(f"\n{total_exclus} repondants ({total_exclus/len(df)*100:.1f}%) sont exclus.")
    print("\nPour augmenter le nombre de repondants valides :")
    
    if df['sexe'].isna().sum() > 0:
        print(f"  - {df['sexe'].isna().sum()} exclus pour genre non-binaire ou manquant")
        print("    -> Envisager de mapper 'Non-binaire' vers M ou F aleatoirement")
    
    if df['code_iris'].isna().sum() > 0:
        print(f"  - {df['code_iris'].isna().sum()} exclus pour code postal hors Besancon")
        print("    -> Verifier si certains CP limitrophes pourraient etre inclus")
    
    if df['csp'].isna().sum() > 0:
        print(f"  - {df['csp'].isna().sum()} exclus pour situation professionnelle non mappee")
        print("    -> Verifier les modalites non prises en compte")

print("="*70)

