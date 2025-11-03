import pandas as pd
import numpy as np

# Charger
df_orig = pd.read_excel('data/raw/enquete_bob.xlsx')
df_prep = pd.read_excel('data/raw/enquete_prepared.xlsx')

print("="*70)
print("ANALYSE DES EXCLUSIONS")
print("="*70)

print(f"\nRepondants originaux : {len(df_orig)}")
print(f"Repondants conserves : {len(df_prep)}")
print(f"Repondants exclus : {len(df_orig) - len(df_prep)}")
print(f"Taux d'exclusion : {(len(df_orig) - len(df_prep))/len(df_orig)*100:.1f}%")

# Analyser les valeurs manquantes dans l'original
print("\n=== VALEURS MANQUANTES DANS L'ORIGINAL ===")
cols_cles = df_orig.columns[:10]
for col in cols_cles:
    n_missing = df_orig[col].isna().sum()
    if n_missing > 0:
        print(f"{col[:50]:50s} : {n_missing:2d} manquants")

# Analyser les modalités problématiques
print("\n=== GENRE ===")
print(df_orig.iloc[:, 1].value_counts(dropna=False))

print("\n=== AGE ===")
print(df_orig.iloc[:, 2].value_counts(dropna=False))

print("\n=== SITUATION PROFESSIONNELLE ===")
print(df_orig.iloc[:, 3].value_counts(dropna=False))

print("\n=== CODE POSTAL ===")
cp_counts = df_orig.iloc[:, 7].value_counts(dropna=False)
print(f"Nombre de CP differents : {len(cp_counts)}")
print("\nRepartition :")
for cp, count in cp_counts.head(15).items():
    if pd.notna(cp):
        cp_str = str(int(cp)) if isinstance(cp, float) else str(cp)
        is_besancon = cp_str.startswith('25')
        marker = "[OK]" if is_besancon else "[HORS]"
        print(f"  {cp_str:10s} : {count:2d} {marker}")

# Compter les exclusions par raison
print("\n=== ESTIMATION DES RAISONS D'EXCLUSION ===")

# Genre non-binaire ou manquant
genre_col = df_orig.iloc[:, 1]
n_genre_pb = (genre_col.isna() | (genre_col == 'Non-binaire')).sum()
print(f"Genre manquant ou non-binaire : {n_genre_pb}")

# Age manquant
n_age_pb = df_orig.iloc[:, 2].isna().sum()
print(f"Age manquant : {n_age_pb}")

# Situation pro manquante
n_situ_pb = df_orig.iloc[:, 3].isna().sum()
print(f"Situation pro manquante : {n_situ_pb}")

# CP hors Besançon
cp_col = df_orig.iloc[:, 7]
n_cp_hors = 0
for cp in cp_col:
    if pd.notna(cp):
        cp_str = str(int(cp)) if isinstance(cp, float) else str(cp)
        if not cp_str.startswith('25'):
            n_cp_hors += 1
    else:
        n_cp_hors += 1
print(f"CP hors Besancon ou manquant : {n_cp_hors}")

print("\n" + "="*70)
print("RECOMMANDATIONS")
print("="*70)

total_exclus = len(df_orig) - len(df_prep)
print(f"\nPour recuperer les {total_exclus} repondants exclus :")

if n_genre_pb > 0:
    print(f"\n1. Genre ({n_genre_pb} exclus)")
    print("   -> Mapper 'Non-binaire' vers M ou F aleatoirement")
    print("   -> Ou creer une categorie 'Autre' dans les marges")

if n_cp_hors > 0:
    print(f"\n2. Code postal ({n_cp_hors} exclus)")
    print("   -> Inclure les CP limitrophes (25220, 25480, etc.)")
    print("   -> Ou elargir la zone geographique des marges")

if n_situ_pb > 0:
    print(f"\n3. Situation professionnelle ({n_situ_pb} exclus)")
    print("   -> Verifier les modalites non mappees")

print("\n" + "="*70)

